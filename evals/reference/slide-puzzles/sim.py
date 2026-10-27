"""Reference harness for examples/slide-puzzles: one row per level per run.
    python3 sim.py --runs 50 --out runs/all.jsonl"""
import json
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../skills/game-balance-audit/scripts"))
sys.path.insert(0, os.path.join(HERE, "../../../examples/slide-puzzles"))
import slide as S  # noqa: E402
from sim_kit import args, simulate  # noqa: E402

LEVELS = json.load(open(os.path.join(HERE, "../../../examples/slide-puzzles/levels.json")))
SOLVE = {}


def solve(start):
    """Breadth-first search: the shortest solution and how many positions it had to look at."""
    if start in SOLVE:
        return SOLVE[start]
    seen = {start: 0}
    q = deque([start])
    answer = (None, 0)
    while q:
        s = q.popleft()
        if S.solved(s):
            answer = (seen[s], len(seen))
            break
        for m in S.moves(s):
            t = S.apply(s, m)
            if t not in seen:
                seen[t] = seen[s] + 1
                q.append(t)
    else:
        answer = (None, len(seen))
    SOLVE[start] = answer
    return answer


def blockers(s):
    """Blocks between X and the exit: the heuristic a person uses first."""
    x = next(b for b in s if b[0] == "X")
    taken = {}
    for ch, r, c, n, across in s:
        for k in range(n):
            taken[(r, c + k) if across else (r + k, c)] = ch
    return len({taken[(S.EXIT_ROW, c)] for c in range(x[2] + x[3], S.SIZE) if (S.EXIT_ROW, c) in taken})


# A person who can look `depth` moves ahead, slips with `mistake` and gives up after `patience` moves.
PROFILES = {
    "novice": {"depth": 0, "mistake": 0.5, "patience": 120},
    "typical": {"depth": 1, "mistake": 0.2, "patience": 200},
    "expert": {"depth": None},
}


def lookahead_score(s, depth):
    if S.solved(s):
        return -100
    score = blockers(s) * 10 - len(S.moves(s)) * 0.1
    if depth == 0:
        return score
    return min([score] + [lookahead_score(S.apply(s, m), depth - 1) for m in S.moves(s)])


def pack(params):
    """The level list after a what-if: params may reorder levels or swap in new boards."""
    rows = {lv["level"]: lv["rows"] for lv in LEVELS}
    for k, v in params.get("replace", {}).items():
        rows[int(k)] = v
    order = params.get("order") or sorted(rows)
    return [{"level": i + 1, "rows": rows[n]} for i, n in enumerate(order)]


def play(rand, params, profile, **_):
    rows = []
    for lv in pack(params):
        r = rand.child(lv["rows"])  # luck follows the board, so moving a level keeps its luck
        start = S.parse(lv["rows"])
        optimal, explored = solve(start)
        row = {"level": lv["level"], "solvable": 1 if optimal is not None else 0, "optimal": optimal, "explored": explored, "branching": len(S.moves(start))}
        if profile["depth"] is None:
            row.update(solved=1 if optimal is not None else 0, moves=optimal or 0)
        else:
            s, seen, used = start, {start}, 0
            while not S.solved(s) and used < profile["patience"]:
                options = [m for m in S.moves(s) if S.apply(s, m) not in seen] or S.moves(s)
                if r.chance(profile["mistake"]):
                    m = r.pick(options)
                else:
                    scored = [(lookahead_score(S.apply(s, m), profile["depth"]), m) for m in options]
                    top = min(sc for sc, _ in scored)
                    m = r.pick([m for sc, m in scored if sc == top])
                s = S.apply(s, m)
                seen.add(s)
                used += 1
            row.update(solved=1 if S.solved(s) else 0, moves=used if S.solved(s) else 0)
        rows.append(row)
    return rows


SOLVABLE_9 = ["J.HGEE", "J.HG..", "XXB...", "AKB.DD", "AKIIIL", "CC.FFL"]
HARDER_12 = ["DDDHHC", "BB...C", "XX.I.C", "GGFI..", "EKF.LL", "EKAAJJ"]
SCENARIOS = {
    "fix-L9": {"replace": {"9": SOLVABLE_9}},
    "move-L6-last": {"order": [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 6]},
    "replace-L10": {"replace": {"10": HARDER_12}},
}
simulate(play=play, params={}, scenarios=SCENARIOS, profiles=PROFILES, opts=args())
