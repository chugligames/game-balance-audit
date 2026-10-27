# Building the simulator

## The contract: rows of JSONL

Whatever language the simulator is in, it writes one JSON object per line: one row per
**segment** (a day, a level, a game) per run. `analyze.py` reads nothing else.

```json
{"scenario": "baseline", "profile": "twice", "run": 17, "day": 6, "taps": 88, "minFree": 3, "outOfEnergy": 1, "chain": "bread"}
```

- `scenario`, `profile` and `run` are added by the toolkit's `simulate`.
- The segment field can have any name (`day`, `level`, `game`). Name it in `audit.json`.
  Leave it out for one-shot games such as a board game where each run is one game.
- Numbers are metrics. Booleans count as 0/1. Strings are labels the analyser can group
  by (`seat`, `strategy`, `chain`).
- `capped: true` marks a run that hit the step limit without ending. The analyser flags it.
- Multiplayer games: write one row per seat per game, carrying `seat`, `strategy` and
  `won` (1, 0, or 1/k for a k-way tie).

## The toolkit

`scripts/sim-kit.mjs` (Node 18+) and `scripts/sim_kit.py` (Python 3.7+) are twins with no
dependencies. Copy the one you need into `balance-audit/sim/`, or import it from the skill's
folder.

| JavaScript | Python | What it does |
|---|---|---|
| `rng(seed)` | `rng(seed)` | Seeded randomness: `next/random`, `int(n)`, `range(lo, hi)`, `chance(p)`, `pick(xs)`, `weighted(pairs)`, `shuffle(xs)` |
| `rand.child(key)` | `rand.child(key)` | A stream fixed by the run's seed and a key, whatever ran before. One per segment |
| `rand.fork()` | `rand.fork()` | A fresh stream from the current position, e.g. for a bot's own coin flips |
| `withSeededMathRandom(rand, fn)` | `seeded_global_random(rand)` | Makes imported game code that calls `Math.random()` / `random.random()` repeatable |
| `args()` | `args()` | `--runs --seed --out --scenario --profile --set key=value --print m1,m2 --by field` |
| `simulate(spec, opts)` | `simulate(play=…, params=…, scenarios=…, profiles=…, opts=…)` | Runs every scenario × profile × run, adds `scenario/profile/run`, writes JSONL |
| `bots.random/greedy/sloppy/lookahead` | `random_bot/greedy/sloppy/lookahead` | Player models for games written to the game interface below. `lookahead` takes `determinize` (re-deal what the player can't see before each rollout) and `candidates` + `prior` (search only the best few moves) |
| `playGame(game, state, policies, rand)` | `play_game(…)` | Plays a game to the end (or a step limit) |
| `decisionImpact(game, state, rand)` | `decision_impact(…)` | How much the choice at one moment changes the outcome |

Name scenarios after the change they make (`'P2-a forwards 3/6/10% gone nightly'`), so the
report can quote them. Don't put commas in names: `--scenario a,b` splits on them.

`simulate` gives run *r* the same seed in every scenario and profile ("common random
numbers"). A difference between the baseline and a what-if then comes from the change,
not from luck. `--set key=value` makes a quick what-if from the command line and tags its
scenario name, so its rows never mix with the baseline's.

## Three shapes of simulator

### Progression games (days, chapters): a loop over time

```js
import { args, simulate, withSeededMathRandom } from './sim-kit.mjs';
import * as G from '../../src/game/rules.js';          // the game's own rules

const PARAMS = { regenMinutes: 3, orderScale: 1 };      // every number a fix may change
const PROFILES = {
  careless: { waste: 0.3, sessions: [21 * 60] },        // once a day, 30% wrong taps
  twice:    { waste: 0.15, sessions: [8 * 60, 21 * 60] },
  keen:     { waste: 0, sessions: [8 * 60, 13 * 60, 21 * 60], ads: true },
};

function play({ rand, params, profile }) {
  const rows = [];
  // Walk the calendar: at each session, refill energy for the time away, then let the bot
  // act until it runs out, finishes the open days or hits the session's time limit.
  // When a day's work is done, push { day, taps, merges, minFree, outOfEnergy, … }.
  return rows;
}

simulate({ params: PARAMS, scenarios: {}, profiles: PROFILES, play }, args());
```

Give the bot a per-action time cost (a tap about 1 s, a drag about 1.5 s) so session
length is realistic, and model the calendar exactly as the game unlocks content. The
family reference lists what to record.

### Level games: one attempt per level

```js
function play({ rand, params, profile }) {
  return LEVELS.map((base) => {
    const def = { ...base, ...(params.edits?.[base.level] || {}) };   // what-ifs edit single levels
    const r = rand.child(base.level);                                // this level's own luck
    const s = M.startLevel(def, r.next);
    while (!M.won(s) && !M.lost(s)) M.play(s, profile.pick(s, M.validMoves(s), r), r.next);
    return { level: def.level, won: M.won(s) ? 1 : 0, movesLeft: s.moves };
  });
}
```

To model players who retry, loop attempts until a win or a give-up point and record
`attempts`.

### Turn-based and multiplayer games: the game interface

Write the rules as an object with `actions(s)`, `apply(s, a, rand)`, `over(s)`,
`seat(s)` (whose turn) and `value(s, seat)` (higher is better for that seat; the final
score margin, or 1/0 for a win). The generic bots and `playGame` then work unchanged:

```python
expert = lookahead(GAME, rollouts=24)          # flat Monte Carlo
typical = sloppy(greedy(score_now), 0.15)      # best immediate score, 15% slips
result = play_game(GAME, GAME.start(r), [expert, typical], r)
```

**Hidden information.** A lookahead bot must not see the deck order or other players'
hands. Pass `determinize: (state, seat, rand) => copy with hidden cards re-dealt`;
otherwise the expert cheats and every finding about skill is inflated.

**Response models.** Free-to-play simulators also decide, at each wall, whether the player
watches, pays, waits or quits (`references/design-goals.md`). Keep those probabilities in
`params` so the audit can vary them, and stop a run's rows when the player quits.

## Wrapping existing code

- **Import the pure rule modules**: board, merge, orders, scoring, level loading. If a
  module pulls in the DOM, a framework or build-time virtual modules, import the files
  below it instead, or stub the one import that breaks (say so in `game-model.md`).
- **TypeScript:** run the simulator with `npx tsx sim/sim.ts` (no build step).
- **Randomness inside game code:** wrap calls with `withSeededMathRandom(rand, () => …)`
  (JS) or `with seeded_global_random(rand):` (Python). Check by running the same seed
  twice: the rows must be identical.
- **Wall-clock time inside game code** (`Date.now()`, timers): pass a simulated clock in if
  the code allows it. Otherwise model regeneration and unlocks in the simulator from the
  game's own constants, and note it as re-implemented.
- **Content tables** (orders, levels, decks) come straight from the game's files. Never
  retype them.
- **Engines** (Unity, Godot, Unreal): find the rules that don't touch the engine (often a
  plain C# or GDScript class) and drive them from a test runner, writing the same rows. If
  everything is inside engine objects, use GUI mode for a small calibration sample and model
  the rest from the rules.

## Speed

- Profile first: one expert move often costs more than everything else together.
- Cache what doesn't depend on luck (a level's optimal solution, a deck's card values).
- Avoid deep clones in hot loops: clone only what a move changes.
- Run expensive player models with fewer runs, and say so; keep cheap ones at full count.
- Long runs: start them in the background, one process per scenario, and analyse the
  JSONL files together.

## Before trusting it

Run through the checklist in SKILL.md step 4 (replay, known answers, bot sanity, real
data, metrics that never move), and write what you checked into `game-model.md`.
