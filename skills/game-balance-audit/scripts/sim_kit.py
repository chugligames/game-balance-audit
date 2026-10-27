"""sim_kit.py: zero-dependency helpers for game balance simulations (Python 3.7+).

The Python twin of sim-kit.mjs. A simulation is the game's own rules (imported from
its code wherever possible), some player models ("bots") and many seeded runs. Each
run returns rows, one per segment (a day, a level, a turn or a whole game), and every
row becomes one line of JSONL that analyze.py reads.

    from sim_kit import args, simulate
    simulate(play=play_one, params=BASE, scenarios=WHAT_IFS, profiles=PLAYERS, opts=args())

    python3 sim.py --runs 200 --out runs/base.jsonl
    python3 sim.py --scenario P1-b --set deck_size=40 --print won,turns
"""

import copy
import json
import zlib
import os
import random
import sys
import time


class Rng(random.Random):
    """random.Random plus the helpers sims keep needing. Seeded, so runs replay."""

    def __init__(self, seed=1):
        super().__init__(seed)
        self.base_seed = seed

    def int(self, n):
        """0 ... n-1"""
        return self.randrange(n)

    def range(self, lo, hi):
        """lo ... hi, both included"""
        return self.randint(lo, hi)

    def chance(self, p):
        return self.random() < p

    def pick(self, xs):
        return xs[self.randrange(len(xs))]

    def weighted(self, pairs):
        """pairs: [(value, weight), ...]"""
        total = sum(w for _, w in pairs)
        x = self.random() * total
        for v, w in pairs:
            x -= w
            if x < 0:
                return v
        return pairs[-1][0]

    def fork(self):
        """An independent stream, e.g. one for the deck and one for the bot."""
        return Rng(self.getrandbits(32))

    def child(self, key):
        """A stream fixed by this run's seed and a key (a level, a day), whatever happened
        before. Give each segment its own child so that a what-if which changes level 8
        leaves the luck of levels 9-15 exactly as it was in the baseline."""
        return Rng(zlib.crc32(("%s:%s" % (self.base_seed, key)).encode()))


def rng(seed=1):
    return Rng(seed)


class seeded_global_random:
    """Game code that calls random.random() / random.choice() becomes repeatable:
        with seeded_global_random(rand): result = game.play_turn(...)"""

    def __init__(self, rand):
        self.rand = rand

    def __enter__(self):
        self.saved = random.getstate()
        random.seed(self.rand.getrandbits(32))

    def __exit__(self, *exc):
        random.setstate(self.saved)


def _value(v):
    if v is None:
        return True
    try:
        return json.loads(v)
    except ValueError:
        return v


def args(argv=None):
    """Options every sim understands (same as sim-kit.mjs):
    --runs N, --seed S, --out file.jsonl, --scenario a,b, --profile a,b,
    --set key=value (repeatable; JSON values), --print m1,m2, --by field (segment for --print).
    Any other --flag value lands on the result as-is."""
    argv = sys.argv[1:] if argv is None else argv
    o = {"runs": 100, "seed": 1, "out": None, "scenarios": None, "profiles": None, "set": {}, "print": None}

    def lst(v):
        return [s.strip() for s in str(v).split(",") if s.strip()]

    i = 0
    while i < len(argv):
        k = argv[i]
        v = None
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            v = argv[i + 1]
            i += 1
        if k == "--runs":
            o["runs"] = int(v)
        elif k == "--seed":
            o["seed"] = int(v)
        elif k == "--out":
            o["out"] = v
        elif k in ("--scenario", "--scenarios"):
            o["scenarios"] = (o["scenarios"] or []) + lst(v)
        elif k in ("--profile", "--profiles"):
            o["profiles"] = (o["profiles"] or []) + lst(v)
        elif k == "--print":
            o["print"] = lst(v)
        elif k == "--set":
            key, _, val = v.partition("=")
            o["set"][key] = _value(val)
        elif k.startswith("--"):
            o[k[2:].replace("-", "_")] = _value(v)
        i += 1
    return o


def simulate(play, params=None, scenarios=None, profiles=None, opts=None):
    """Plays every scenario x profile x run and writes the rows.
    play(rand=, params=, profile=, profile_name=, scenario=, run=) returns a row dict or a list of them.
    Run r gets the same seed in every scenario and profile ("common random numbers"),
    so a gap between scenarios comes from the change, not from luck. Every row gets
    scenario, profile and run added; a --set adds "+key=value" to the scenario name."""
    opts = opts if opts is not None else args()
    params = params or {}
    profiles = profiles or {"default": {}}
    every = {"baseline": {}}
    every.update(scenarios or {})
    names = opts["scenarios"] or list(every)
    who = opts["profiles"] or list(profiles)
    tag = "".join("+%s=%s" % (k, json.dumps(v)) for k, v in opts["set"].items())
    rows = []
    for name in names:
        if name not in every:
            raise SystemExit('no scenario "%s" (have: %s)' % (name, ", ".join(every)))
        p = dict(params)
        p.update(every[name])
        p.update(opts["set"])
        for pname in who:
            if pname not in profiles:
                raise SystemExit('no profile "%s" (have: %s)' % (pname, ", ".join(profiles)))
            t0 = time.time()
            for run in range(opts["runs"]):
                rand = Rng(opts["seed"] * 1000003 + run)
                out = play(rand=rand, params=p, profile=profiles[pname], profile_name=pname, scenario=name + tag, run=run)
                for row in out if isinstance(out, list) else [out]:
                    full = {"scenario": name + tag, "profile": pname, "run": run}
                    full.update(row)
                    rows.append(full)
            sys.stderr.write("%s / %s: %d runs in %.1fs\n" % (name + tag, pname, opts["runs"], time.time() - t0))
    if opts["out"]:
        write_rows(opts["out"], rows)
    if opts["print"]:
        print(summary(rows, opts["print"], opts.get("by") or guess_segment(rows)))
    return rows


SEGMENT_NAMES = ["segment", "day", "level", "round", "turn", "stage", "chapter", "game"]


def guess_segment(rows):
    return next((k for k in SEGMENT_NAMES if rows and k in rows[0]), "segment")


def write_rows(path, rows):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    sys.stderr.write("wrote %d rows to %s\n" % (len(rows), path))


def summary(rows, metrics, segment="segment"):
    """A quick look while iterating: mean of each metric per segment, per scenario and profile."""
    groups = {}
    for r in rows:
        key = "%s / %s" % (r["scenario"], r["profile"])
        groups.setdefault(key, {}).setdefault(r.get(segment, "all"), []).append(r)
    lines = []
    for key, segs in groups.items():
        lines.append("\n" + key)
        lines.append(segment.ljust(8) + "".join(m.rjust(12) for m in metrics))
        for seg in sorted(segs, key=lambda s: (isinstance(s, str), s)):
            cells = []
            for m in metrics:
                xs = [float(r[m]) for r in segs[seg] if isinstance(r.get(m), (int, float))]
                cells.append(("%.2f" % (sum(xs) / len(xs)) if xs else "-").rjust(12))
            lines.append(str(seg).ljust(8) + "".join(cells))
    return "\n".join(lines)


# ── Generic player models ────────────────────────────────────────────────────
# They play any game object with these methods:
#   actions(s) -> legal actions       apply(s, a, rand) -> next state (may mutate s)
#   over(s) -> bool                   seat(s) -> whose turn (optional, default 0)
#   value(s, seat) -> number, higher is better for that seat (needed by lookahead)
#   clone(s) -> copy (optional, default copy.deepcopy)
# A policy is a function (state, actions, rand, seat) -> action.


def _argmax(xs, f, rand):
    best, top = [], None
    for x in xs:
        v = f(x)
        if top is None or v > top:
            top, best = v, [x]
        elif v == top:
            best.append(x)
    return rand.pick(best) if best else xs[0]


def _clone(game):
    return getattr(game, "clone", None) or copy.deepcopy


def random_bot():
    """Picks any legal action. A floor, not a player: real people are never this random."""
    return lambda s, acts, rand, seat=0: rand.pick(acts)


def greedy(score):
    """Takes the action with the best immediate score(s, a, seat). Ties break at random."""
    return lambda s, acts, rand, seat=0: _argmax(acts, lambda a: score(s, a, seat), rand)


def sloppy(policy, mistake_rate):
    """Plays like `policy`, but makes a random move with probability `mistake_rate`."""
    return lambda s, acts, rand, seat=0: rand.pick(acts) if rand.chance(mistake_rate) else policy(s, acts, rand, seat)


def lookahead(game, rollouts=16, max_steps=200, playout=None, determinize=None, candidates=0, prior=None):
    """Flat Monte Carlo: tries each action, plays `rollouts` quick games from there with
    `playout` (random by default) and keeps the action with the best average value.
    A strong, game-agnostic "expert". Cost: actions x rollouts x game length.
      determinize(state, seat, rand) -> a copy with everything `seat` can't see re-dealt
        (deck order, other hands). Without it the bot sees hidden cards and cheats.
      candidates + prior(state, action, seat): only search the `candidates` actions a
        cheap heuristic likes best. Much faster when there are many legal moves.
    Search is slow in Python; for a search-based expert, Node is often several times faster."""
    clone = _clone(game)
    follow = playout or random_bot()

    def policy(s, acts, rand, seat=0):
        pool = acts
        if candidates and prior and len(acts) > candidates:
            ranked = sorted(((prior(s, a, seat), i, a) for i, a in enumerate(acts)), key=lambda t: (-t[0], t[1]))
            pool = [t[2] for t in ranked[:candidates]]

        def avg(a):
            total = 0.0
            for _ in range(rollouts):
                start = determinize(s, seat, rand) if determinize else clone(s)
                nxt = game.apply(start, a, rand)
                total += game.value(play_game(game, nxt, follow, rand, max_steps)["state"], seat)
            return total / rollouts

        return _argmax(pool, avg, rand)

    return policy


def play_game(game, state, policies, rand, max_steps=10000, on_step=None):
    """Plays one game to the end (or max_steps). `policies` is one policy, or a list with one per seat.
    Returns {"state", "steps", "capped"}: capped means it never ended, a finding in itself."""
    steps = 0
    while not game.over(state) and steps < max_steps:
        acts = game.actions(state)
        if not acts:
            break
        seat = game.seat(state) if hasattr(game, "seat") else 0
        policy = policies[seat] if isinstance(policies, (list, tuple)) else policies
        a = policy(state, acts, rand, seat)
        if on_step:
            on_step(state, a, seat, steps)
        state = game.apply(state, a, rand)
        steps += 1
    return {"state": state, "steps": steps, "capped": steps >= max_steps and not game.over(state)}


def decision_impact(game, state, rand, rollouts=24, max_steps=200, playout=None, determinize=None):
    """How much the choice at this moment matters: each option's average outcome over
    `rollouts` playouts. `spread` (best - average option) near zero, game after game,
    means the decisions don't change anything. Counting options does not show that."""
    clone = _clone(game)
    follow = playout or random_bot()
    seat = game.seat(state) if hasattr(game, "seat") else 0
    values = []
    for a in game.actions(state):
        total = 0.0
        for _ in range(rollouts):
            nxt = game.apply(determinize(state, seat, rand) if determinize else clone(state), a, rand)
            total += game.value(play_game(game, nxt, follow, rand, max_steps)["state"], seat)
        values.append(total / rollouts)
    if not values:
        return {"options": 0, "best": 0, "mean": 0, "spread": 0}
    mean = sum(values) / len(values)
    return {"options": len(values), "best": max(values), "mean": mean, "spread": max(values) - mean}
