---
name: game-balance-audit
description: Audits a game's balance by simulation instead of opinion. Reads the game's code or a rulebook (or drives a running web build), builds a small simulator that plays it with bots from careless to expert over hundreds of seeded runs, checks the results against what the designer wants (difficulty curves, energy and board pressure, win rate per level, seat advantage, dominant strategies, comebacks, luck versus skill) and writes an audit that ranks the problems and gives three suggestions for each, every one tested in the simulator before it is recommended. Use for merge-2 and energy economies, match-3 and other level-based games, logic puzzles, and strategy, board and card games, on web, mobile or tabletop. Use when someone asks for a balance or economy audit, says a game is too easy or too hard, wants bots to playtest it, or asks about difficulty curves, first-player advantage or a dominant strategy.
license: MIT
compatibility: Simulations run on Node 18+ or Python 3.7+ with the standard library only. Works from source code, a rulebook, or a running web build.
metadata:
  author: Chugli Games
  version: "0.1.0"
---

# Game balance audit

Measure the game; don't guess at it. Most balance advice is a designer's hunch in a
confident voice. This skill builds a small simulator for the game in front of you, lets
bots play it hundreds of times, compares what happens with what the designer wants, and
only recommends a change after the simulator has shown what that change does.

The skill's scripts live next to this file, in `scripts/`. When this file says `<skill>`,
it means this file's own folder.

## What you hand back

A `balance-audit/` folder, at the game's repository root (or next to the rulebook):

| File | What it is |
|---|---|
| `REPORT.md` | The audit: problems ranked by how much they hurt players, each with its evidence and three tested suggestions |
| `game-model.md` | How the game works, as the simulator models it, and every assumption made |
| `audit.json` | What the designer wants, written as checks the analyser runs |
| `sim/` | The simulator. Anyone can re-run it |
| `runs/*.jsonl` | Raw results, one row per segment (day, level, game…) per run |
| `results/` | `summary.md`, `summary.json` and `charts.html` from the analyser |

Never edit the game's own files. If the work is in a git repository, offer to do it on a
new branch. If a simulation needs a hook inside the game (see GUI mode), ask first.

## The workflow

### 1. Find out what you are auditing

- **Source.** Code you can import (best), a rulebook or design document (write the rules
  as code, see `references/rulebook-mode.md`), or only a running build (drive it in a
  browser, see `references/gui-mode.md`).
- **Family.** It decides what to measure. Read the matching reference before going on:

  | Family | Examples | Read |
  |---|---|---|
  | Economy and progression | merge-2, idle, farming, anything with energy, timers or daily unlocks | `references/families/economy.md` |
  | Level-based puzzles | match-3, bubble shooters, move-limited or score-target levels | `references/families/levels.md` |
  | Logic puzzles | sliding blocks, Sokoban-likes, nonograms, puzzle packs with one solution | `references/families/puzzles.md` |
  | Strategy, board and card games | 2–5 players, drafting, deckbuilders, race and area games | `references/families/strategy.md` |

  A game can belong to two families (a merge-2 game with levels). Read both.
- **Intent.** An audit measures the game against what the designer wants. Find it in the
  README, design docs, code comments or level notes. If it isn't written down, ask at
  most three short questions, for example: "Which days or levels should feel hard?",
  "Who is the target player: how often do they play, and how good are they?", "What
  must never happen?" If nobody can answer, use the family's defaults from its
  reference file and say in the report that you did.
- **Scope.** Which segments (days 1–21, levels 1–60) and which player types matter.

### 2. Model the game (`game-model.md`)

Write down, briefly: the actions a player can take; what each costs and produces
(sources and sinks); every limit (board space, energy, moves, hand size, turn order);
where randomness enters; what a segment is (a day, a level, a game) and how one ends;
what is time-gated (timers, daily unlocks, regeneration). List every number a fix might
want to change. They become the simulator's `params`. Add an **Assumptions** list for
anything the code or rules leave open, and keep it current.

### 3. Build the simulator (`sim/`)

Read `references/simulator.md` first. The essentials:

- **Use the game's own rule code** wherever you can import it. Re-implement only what is
  tied to the UI, and say which parts you re-implemented. A simulator that re-implements
  the rules audits your reading of the game, not the game.
- Use the toolkit: `<skill>/scripts/sim-kit.mjs` (JavaScript or TypeScript games) or
  `<skill>/scripts/sim_kit.py` (everything else, including rulebooks). For other
  languages (C#, GDScript, Lua), write the simulator in the game's language and emit the
  same JSONL rows.
- **Seeded randomness only.** Give each segment its own stream with `rand.child(segment)`,
  so a change to level 8 leaves the luck of levels 9–15 exactly as it was. Without this,
  every what-if also reshuffles the luck of everything after it, and you will "measure"
  noise.
- Every tunable number is a param, so a what-if is just a scenario: `{ name: overrides }`.
- One row per segment per run, with the metrics your family reference lists.

### 4. Check the simulator before you trust it

Do these before any analysis, and write the results into `game-model.md`:

1. **Replay.** Step one seeded run by hand (print the state every few actions) and check
   it against the rules. Bugs here are the commonest source of false findings.
2. **Known answers.** Anything the designer or the game's tests already know (level 1 is
   always won, a day takes about 40 taps, the first player wins about 52%) must come out
   right.
3. **Bot sanity.** The expert must beat the careless player. If not, the bots or the
   rules are wrong.
4. **Real data, when it exists.** Analytics, playtest notes or a recorded session: put the
   simulator's number next to the real one for a few segments. Report the gap; if it is
   large, say the findings describe the bots, not people.
5. **Metrics that never move.** The analyser lists metrics that are the same in every row.
   Each is either broken, or something that never happens in the game (the board never
   fills up, nobody ever sells). Find out which.

### 5. Choose the player models

At least three, spanning skill: a **careless** player (makes mistakes, plays badly), a
**typical** one and an **expert** (see `bots.lookahead` in the toolkit, or an exact solver
for logic puzzles). Economy games also vary *how often* people play: once a day, twice a
day, three times with ads. Multiplayer games add strategy archetypes and mirror tables
(see the strategy reference). Name the player model behind every number you report.
Bots are not people: they never forget an order, misread a tile or get bored. Anything
that depends on those goes in the report as a playtest question, not as a finding.

### 6. Run the baseline and analyse it

Write `audit.json` from the designer's intent (`references/audit-config.md`), then:

```bash
node sim/sim.mjs --runs 200 --out runs/baseline.jsonl          # or python3 sim/sim.py …
python3 <skill>/scripts/analyze.py audit.json runs/baseline.jsonl --out results
```

How many runs? A rate measured over N runs is good to about ±1/√N: 100 runs ±10
points, 400 runs ±5, 2,000 runs ±2. Use enough runs that the effects you care about
are bigger than that. The analyser marks target misses that fall inside sampling noise
as *borderline*. Re-run those with more runs before reporting them.

Read `results/summary.md` and open `results/charts.html` for the curves. The flags are
a starting point, not the audit.

### 7. Turn flags into problem areas, each with three tested suggestions

Group related flags into **problem areas**: one player-facing problem each. For example,
"never-binds on free cells", "off-target on crowding" and "flat free cells" are all
"the board never gets crowded". Rank them by harm to players: walls and impossible
levels first, then broken intent, then polish. Report the top 5–7 in full and list the
rest.

For **every** problem area, give exactly three suggestions. Draw them from
`references/suggestions.md` and from the family reference, and make them different in
kind where you can: one that tunes a number, one that changes a rule, one that changes
content or structure. Then **test each one**:

1. Add it to the simulator as a scenario (`scenarios: { 'P2-b orders x1.5 from day 6': {...} }`).
2. Run it with the same seeds as the baseline, and analyse baseline and what-ifs together:
   `python3 <skill>/scripts/analyze.py audit.json runs/*.jsonl --out results`.
3. Read its section under "What-ifs against the baseline": which flags it fixes, which it
   introduces, and how the key metrics move for each player type.

A suggestion that doesn't move the problem's metric is not a suggestion. Replace it, or
keep it only if it is worth recording that the obvious fix fails, and say so. Obvious fixes
fail more often than you'd think. After picking one per area, run the picks **together** as
one scenario: fixes interact. If a suggestion can't be simulated (feel, clarity,
memory load), say so and give the playtest that would test it.

### 8. Write the report

Use the template in `references/report.md`. Plain language, for a designer: what a player
would notice, the numbers that show it (with the player model named), and the three
suggestions with their before → after results. End with what the simulator can't tell
you and the playtest that would.

## Rules that keep an audit honest

- **No finding without a number, and no number without its player model and run count.**
- **Separate difficulty from time-gating.** For economy games, run once with unlimited
  energy to see what each day asks for, then again with the real energy and session
  patterns to see when it binds.
- **Check where a fix lands.** A change that tightens day 1 and fades by day 3 is not a
  difficulty ramp. Look at the whole curve, not the average.
- **Look for inert levers.** Slower regeneration does nothing for a player who already
  fills the energy cap between sessions; more colours do nothing on a level nobody can
  win anyway. The what-if table shows this. Say it plainly.
- **Solution length is not difficulty.** Short puzzles can be deceptive; long ones can be
  one obvious idea repeated. Use bots as well as a solver.
- **Counting options says nothing about how much a choice matters.** If you need that, use
  `decisionImpact` / `decision_impact` from the toolkit, which compares what each option leads to.
- **Benchmarks only with sources.** `references/benchmarks.md` has sourced numbers;
  quote them with the source, and say when a number comes from a different kind of game.
- **The designer decides.** Recommend; don't rewrite the game. Hand back the simulator so
  they can try their own ideas.

## Reference files

| File | Read it when |
|---|---|
| `references/simulator.md` | Building the simulator: toolkit API, wrapping existing code, rows, speed |
| `references/audit-config.md` | Writing `audit.json` and reading the analyser's flags |
| `references/families/*.md` | Deciding what to model and measure for the game's family |
| `references/suggestions.md` | Finding three suggestions for a problem |
| `references/rulebook-mode.md` | The game exists only as rules on paper |
| `references/gui-mode.md` | Only a running build is available, or to calibrate against it |
| `references/report.md` | Writing `REPORT.md` |
| `references/benchmarks.md` | Comparing with other games, with sources |
