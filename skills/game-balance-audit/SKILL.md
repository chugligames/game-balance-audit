---
name: game-balance-audit
description: "Audits a game's balance by simulation, against what the designer optimises for: ad or purchase revenue and engagement in free-to-play, completion in premium games, fairness and tension in tabletop. Reads the game's code, a spreadsheet or a rulebook (or a running web build), simulates it with bots from careless to expert over hundreds of seeded runs, checks difficulty curves, walls and monetisation moments, win rate per level, seat advantage, dominant strategies and luck versus skill, and writes an audit with three suggestions per problem, each tested in the simulator and scored on the designer's goals. For merge-2 and energy economies, match-3 and level-based games, logic puzzles, strategy, board and card games, and chance systems (slots, loot tables, gacha), with exact odds where possible. Use when someone wants a balance or economy audit, says a game is too easy or too hard, wants bots to playtest it, or asks about difficulty, monetisation, odds, first-player advantage or a dominant strategy."
license: MIT
compatibility: "Simulations run on Node 18+ or Python 3.7+ with the standard library only. Works from source code, a rulebook, or a running web build."
metadata:
  author: Chugli Games
  version: "0.3.0"
---

# Game balance audit

Measure the game; don't guess at it. Most balance advice is a designer's hunch in a
confident voice. This skill builds a small simulator for the game in front of you, lets
bots play it hundreds of times, compares what happens with what the designer wants, and
only recommends a change after the simulator has shown what that change does.

**The designer's goals decide what a problem is.** A wall that makes players wait is a
bug in a paid game and the main revenue moment in an ad-funded one; a 55% first-player
win rate is a flaw for a tabletop publisher and irrelevant in a solo puzzle pack. Never
assume the goal is "make it comfortable for the player".

The skill's scripts live next to this file, in `scripts/`. When this file says `<skill>`,
it means this file's own folder.

## What you hand back

A `balance-audit/` folder, at the game's repository root (or next to the rulebook):

| File | What it is |
|---|---|
| `REPORT.md` | The audit: the design goals, then problems ranked by how much they hurt those goals, each with its evidence and three tested suggestions scored on every goal |
| `game-model.md` | How the game works, as the simulator models it, and every assumption made |
| `audit.json` | What the designer wants, written as goals, constraints and checks the analyser runs |
| `sim/` | The simulator. Anyone can re-run it |
| `runs/*.jsonl` | Raw results, one row per segment (day, level, game…) per run |
| `results/` | `summary.md`, `summary.json` and `charts.html` from the analyser |

Never edit the game's own files. If the work is in a git repository, offer to do it on a
new branch. If a simulation needs a hook inside the game (see GUI mode), ask first.

## The workflow

### 1. Find out what you are auditing, and what the designer is optimising for

- **Design goals first.** Read `references/design-goals.md`. Establish how the game makes
  money (or why it exists), the primary goal as a number, the guardrails that must not
  break, and which players matter. Infer from the repo before asking (ad SDKs, store
  libraries, "watch an ad" strings, energy and ad caps, a component list in a rulebook),
  then confirm in one short question. If nobody can answer, use the lens's defaults and say
  so at the top of the report.
- **Source.** Code you can import (best), a code snippet (a drop or damage formula), a
  spreadsheet (reel strips, paytables, drop tables, economy sheets: recompute every derived
  column yourself), a rulebook or design document (write the rules as code, see
  `references/rulebook-mode.md`), or only a running build (drive it in a browser, see
  `references/gui-mode.md`).
- **Family.** It decides what to measure. Read the matching reference before going on:

  | Family | Examples | Read |
  |---|---|---|
  | Economy and progression | merge-2, idle, farming, anything with energy, timers or daily unlocks | `references/families/economy.md` |
  | Level-based puzzles | match-3, bubble shooters, move-limited or score-target levels | `references/families/levels.md` |
  | Logic puzzles | sliding blocks, Sokoban-likes, nonograms, puzzle packs with one solution | `references/families/puzzles.md` |
  | Strategy, board and card games | 2–5 players, drafting, deckbuilders, race and area games | `references/families/strategy.md` |
  | Chance systems | slots and paytables, loot tables and gacha with pity, dice and card odds | `references/families/chance.md` |

  A game can belong to two families (a merge-2 game with levels). Read both.
- **The intended experience.** Beyond the business goals: which days or levels should
  feel hard, who the target player is (how often they play, how good they are), what must
  never happen. Find it in the README, design docs, code comments or level notes; ask at
  most three short questions in total (goals included) if it isn't written down.
- **Scope.** Which segments (days 1–21, levels 1–60) and which player types matter.

### 2. Model the game (`game-model.md`)

Write down, briefly: the actions a player can take; what each costs and produces
(sources and sinks); every limit (board space, energy, moves, hand size, turn order);
where randomness enters; what a segment is (a day, a level, a game) and how one ends;
what is time-gated (timers, daily unlocks, regeneration); every moment the game earns or
offers a choice (an ad for energy, "+5 moves", a refill, a shop) with its reward and cap.
List every number a fix might want to change. They become the simulator's `params`. Add an **Assumptions** list for
anything the code or rules leave open, and keep it current.

### 3. Build the simulator (`sim/`)

Read `references/simulator.md` first. The essentials:

- **Use the game's own rule code** wherever you can import it. Re-implement only what is
  tied to the UI, and say which parts you re-implemented. A simulator that re-implements
  the rules audits your reading of the game, not the game.
- Use the toolkit: `<skill>/scripts/sim-kit.mjs` (JavaScript or TypeScript games, and
  anything needing a search-based expert, which is far faster in Node) or
  `<skill>/scripts/sim_kit.py` (Python games, and rulebooks without heavy search). For other
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

1. **Replay.** Give the simulator a trace switch (e.g. `TRACE_DAY=8` prints every move of
   day 8 with the board and open goals), step one seeded run and check each move against
   the rules. Bugs here are the commonest source of false findings, and you'll use the
   switch again whenever a number looks odd.
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

**Games that earn at certain moments** (ads, purchases, refills) also need a **response
model**: at each wall the player watches, pays, waits or quits, with probabilities that are
params and a quit chance that grows with early, frequent or long walls. Without it the
simulator can't see revenue or churn, and every recommendation drifts toward "make it
easier". See `references/design-goals.md`. Run the key scenarios at a low, middle and high
quit rate when the rate is an assumption.

**Bots don't adapt to rule changes.** When a what-if rewards a behaviour, include a player
model that pursues it, and re-tune the reference bot's thresholds, or the gain is measured
against opponents who ignore the new rule.

### 6. Run the baseline and analyse it

Write `audit.json` (`references/audit-config.md`): the design goals and guardrails as
`goals` and `constraints`, and the intended experience as metric checks and targets.
Then:

```bash
node sim/sim.mjs --runs 200 --out runs/baseline.jsonl          # or python3 sim/sim.py …
python3 <skill>/scripts/analyze.py audit.json runs/baseline.jsonl --out results
```

How many runs? A rate measured over N runs is good to about ±1/√N: 100 runs ±10
points, 400 runs ±5, 2,000 runs ±2. Use enough runs that the effects you care about
are bigger than that. The analyser marks target misses that fall inside sampling noise
as *borderline*. Re-run those with more runs before reporting them.

Read `results/summary.md` (it opens with the scorecard: every scenario against the design
goals) and open `results/charts.html`. The flags are a starting point, not the audit.

### 7. Turn flags into problem areas, each with three tested suggestions

Group related flags into **problem areas**: one problem each, as the designer would name
it. For example, "never-binds on free cells", "off-target on crowding" and "flat free
cells" are all "the board never gets crowded". Rank them by harm to the design goals:
broken guardrails and impossible content first, then the primary goal, then the intended
experience, then polish. A flag that hurts no goal isn't a problem (in an ad-funded game,
an energy wall can be the point). Report the top 5–7 in full and list the rest.

For **every** problem area, give exactly three suggestions. Draw them from
`references/suggestions.md` and from the family reference, and make them different in
kind where you can: one that tunes a number, one that changes a rule, one that changes
content or structure. Then **test each one**:

1. Add it to the simulator as a scenario (`scenarios: { 'P2-b orders x1.5 from day 6': {...} }`).
2. Run it with the same seeds as the baseline, and analyse baseline and what-ifs together:
   `python3 <skill>/scripts/analyze.py audit.json runs/*.jsonl --out results`.
3. Read its row in the scorecard (its value on every goal, the constraints it breaks)
   and its section under "What-ifs against the baseline": which flags it fixes, which it
   introduces, and how the key metrics move for each player type.

Score every suggestion on every goal. One that helps players but costs the primary goal
(free energy in an ad-funded game) is a **trade-off**: show its price in the designer's
units and don't recommend it unless the designer asks. Recommend from the scorecard's best
trade-offs.

A suggestion that doesn't move the problem's metric is not a suggestion. Before dropping
it, check whether you tested the right version or dose of it (raising the *biggest* order
does far more than raising the smallest). Then replace it, or keep it only if it is worth
recording that the obvious fix fails, and say so. Obvious fixes
fail more often than you'd think. After picking one per area, run the picks **together** as
one scenario: fixes interact. If a suggestion can't be simulated (feel, clarity,
memory load), say so and give the playtest that would test it.

### 8. Write the report

Use the template in `references/report.md`. Plain language, for a designer: what a player
would notice, the numbers that show it (with the player model named), and the three
suggestions with their before → after results. End with what the simulator can't tell
you and the playtest that would.

## Rules that keep an audit honest

- **Exact before estimated.** When the outcomes can be enumerated (reels, dice, a deck) or
  form a simple chain (pity counters), compute the exact answer as fractions, then simulate
  anyway and put the exact values under `exact` in `audit.json`. The analyser checks that the
  simulation's 95% interval contains them. Report both. Agreement is what lets a reader
  trust the rest; disagreement means the simulator is wrong, and it comes first.
- **Reproducible by anyone.** State the seed, the number of runs or iterations, and a 95%
  interval for every simulated number. Hand back the commands that regenerate it.

- **Goals before verdicts.** Every problem and recommendation names the goal it serves.
  When goals pull against each other (more ad views, more players quitting), show the
  trade-off across scenarios; don't pretend there is a free win.
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
- **Assumptions are dials, not facts.** Probabilities of watching, paying or quitting are
  rarely known; run the decision at a low, middle and high value and say which
  recommendations survive all three.
- **Stay inside platform rules.** Rewarded ads are opt-in; odds on paid random items are
  disclosed; no fake timers or hidden costs. Pressure comes from honest choices.
- **The designer decides.** Recommend; don't rewrite the game. Hand back the simulator so
  they can try their own ideas.

## Reference files

| File | Read it when |
|---|---|
| `references/design-goals.md` | **Always, in step 1**: business models, goals and guardrails, response models, platform rules |
| `references/simulator.md` | Building the simulator: toolkit API, wrapping existing code, rows, speed |
| `references/audit-config.md` | Writing `audit.json` and reading the analyser's flags |
| `references/families/*.md` | Deciding what to model and measure for the game's family |
| `references/suggestions.md` | Finding three suggestions for a problem |
| `references/rulebook-mode.md` | The game exists only as rules on paper |
| `references/gui-mode.md` | Only a running build is available, or to calibrate against it |
| `references/report.md` | Writing `REPORT.md` |
| `references/benchmarks.md` | Comparing with other games, with sources |
