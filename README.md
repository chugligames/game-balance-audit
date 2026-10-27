# game-balance-audit

[![tests](https://github.com/chugligames/game-balance-audit/actions/workflows/test.yml/badge.svg)](https://github.com/chugligames/game-balance-audit/actions/workflows/test.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent skill that audits a game's balance by **simulation and exact maths, not
opinion**, against what *you* are optimising for.

Point your coding agent at a game: its code, a spreadsheet, a rulebook, or a running web
build. It will:

1. **Work out your goals.** How the game makes money, or why it exists, decides what counts
   as a problem:
   - free-to-play: rewarded ads or purchases against engagement and players quitting;
   - premium: completion and satisfaction;
   - tabletop: fairness, close games, length on the box, more than one way to win.
2. **Compute exactly where it can.** Reel strips, dice and pity counters have exact
   answers, worked out as fractions.
3. **Simulate the rest.** It builds a small simulator, reusing your game's own rule code,
   or writing your rulebook or spreadsheet as code. Bots from careless to expert play it
   hundreds of times with fixed seeds. For free-to-play games they also decide, at each
   wall, whether to watch an ad, pay, wait or quit. Every simulated number comes with its
   95% interval, and is checked against the exact answer when there is one.
4. **Check the results** against your goals and intended experience:
   - difficulty curves, walls and revenue moments, win rate per level;
   - seat advantage, dominant strategies, runaway leaders, luck versus skill;
   - payout rates and drop odds, against what the sheet or the Rates screen claims.
5. **Write an audit** that ranks the problems and gives **three suggestions for each**.
   Every suggestion is tested and scored on your goals, with before → after numbers. A
   scorecard shows which changes are the best trade-offs.

It works for merge-2 and energy economies, match-3 and other level-based games, logic
puzzles, strategy, board and card games, and chance systems (slots, loot tables, gacha),
on web, mobile or tabletop.

## Install

**In Claude Code** (one step; updates with the repo):

```
/plugin marketplace add chugligames/game-balance-audit
/plugin install game-balance-audit@chugligames
```

The same from a terminal: `claude plugin marketplace add chugligames/game-balance-audit`,
then `claude plugin install game-balance-audit@chugligames`.

**Other agents.** The skill is a plain `SKILL.md` folder in the open
[Agent Skills](https://agentskills.io) format, which other coding agents read too. The
`skills` CLI installs it for Claude Code or for the agent you name with `-a`:

```bash
npx skills add chugligames/game-balance-audit            # into this project
npx skills add chugligames/game-balance-audit -g         # for all your projects
```

**By hand:** copy `skills/game-balance-audit/` into your agent's skills folder (for Claude
Code, `.claude/skills/`).

Simulations need **Node 18+ or Python 3.7+**. There are no packages to install. Everything
runs on your machine.

## Use it

Open your agent in the game's folder (or next to your rulebook or sheets) and ask in plain
words:

> Audit the balance of this game. It's free-to-play with rewarded ads; I want players
> watching 2–3 ads a day by week two without many quitting.

> Here's my rulebook (RULES.md). Is there a first-player advantage, and is any strategy
> dominant? It should play in about 30 minutes at 2–5 players.

> reels.csv and paytable.csv are our slot. Is the RTP really 96%?

Tell it what you're optimising for if you can. If you don't, it looks for clues (ad SDKs,
shop code, energy caps, a component list), then asks you one short question or states its
assumption at the top of the report.

**What you get:** a `balance-audit/` folder.

| File | What it is |
|---|---|
| `REPORT.md` | The audit: your goals, exact answers against the simulation, a scorecard of every change tried, problems ranked by harm to your goals, and three tested suggestions for each |
| `game-model.md` | How the simulator models your game, which parts reuse your code, every assumption, and the checks it passed |
| `audit.json` | Your goals, limits, exact values and intended experience, written as checks |
| `sim/` | The simulator. Re-run it after every change, or add your own what-ifs |
| `results/` | `summary.md`, `summary.json` and `charts.html` |

Your game's own files are never edited. In a git repo, the agent offers to work on a
branch.

**How long it takes:** often 30–90 minutes of agent time, depending on the game and how
long its simulations take. Search-based "expert" bots for card and board games are the
slowest part.

## Reproducible by design

- **Fixed seeds.** A run is a pure function of its seed, and each segment (a day, a level)
  gets its own random stream. A what-if that changes level 8 leaves the luck of every other
  level exactly as it was.
- **Stated sizes and intervals.** Every simulated number reports its runs and a 95%
  interval. Target misses that fall inside sampling noise are marked "borderline", not
  reported as findings.
- **Exact answers checked.** When the outcome space is small enough to enumerate, the exact
  value goes into the audit, and the analyser checks that the simulation's interval
  contains it. A mismatch is the first problem reported.
- **Tested.** `tests/` covers the statistics, the checks, the toolkits and the
  known-answer examples (exact maths against a fixed-seed simulation), on every push.

## Examples with known answers

Six small made-up games, each with balance problems planted on purpose. Two have answers
you can verify by hand.

| Example | Input | Kind of game | Known answer |
|---|---|---|---|
| `examples/tiny-slot` | **spreadsheets** (reel strips, paytable) | 3-reel social-casino slot | RTP = **449/432 = 103.94%** by enumerating all 1,728 outcomes. The sheet's 96.0% treats every reel as if it were reel 1 |
| `examples/loot-drops` | **a code snippet** (drop formula with pity) | loot chest, gems sold for money | **69.50** pulls per legendary (1.44%, not the advertised 1.6%). The "guaranteed within 90" promise fails in 1 streak in 2,426 (`>` instead of `>=`) |
| `examples/market-day` | **a design doc** (rulebook only) | 2–4 player card game | seat advantage, a dominant early-selling strategy, a runaway leader |
| `examples/merge-mini` | code | merge-2, rewarded ads | no ad moments at all; a board that never fills |
| `examples/match3-mini` | code | match-3, "+5 moves" sold on a loss | an unwinnable level; a hard level that isn't |
| `examples/slide-puzzles` | code | Rush Hour-style pack, paid app | an unsolvable level; deceptive short levels |

How the exact answers agree with the simulation (fixed seed 1, from the answer keys in
`evals/reference/`):

| Quantity | Exact | Simulated (95% interval) | Samples |
|---|---|---|---|
| Slot RTP | 1.039352 | 1.0374 ± 0.0115 | 1,000,000 spins |
| Slot hit rate | 0.310185 | 0.31009 ± 0.00098 | 1,000,000 spins |
| Slot big-win rate (40× or more) | 0.002894 | 0.002889 ± 0.000101 | 1,000,000 spins |
| Pulls per legendary | 69.4995 | 69.37 ± 0.13 | 8,000,000 pulls |
| Streaks that need a 91st pull | 0.000412 | 0.00045 ± 0.00013 | about 115,000 streaks |

Each example's `audits/` folder holds the skill's real, unedited output on it.

## With and without the skill

*Being filled in: the same prompts run through Claude Code with and without the skill
(`claude plugin eval`, with a no-plugin baseline arm), with both reports published
unedited.*

## Limitations

- **Not certification.** For real-money gambling, payout and fairness need an accredited
  test lab and each regulator's approval. This skill does design analysis only. It doesn't
  certify RTP, test a random number generator, or establish legal compliance. The same
  goes for odds-disclosure rules: it can show that a Rates screen is wrong, not that one is
  compliant.
- **Simulated numbers are estimates.** Each comes with its interval and run count. Exact
  answers are only as right as the rules they were computed from. Read `game-model.md` to
  see what the agent assumed.
- **Bots aren't people.** They don't forget, misread, get bored or tell each other things.
  Player models (how often someone watches an ad, quits at a wall, or slips) are
  assumptions. The skill varies them and says which conclusions survive. Calibrate against
  real analytics or playtests before trusting absolute numbers.
- **Inputs it handles poorly:**
  - **Real-time and physics-driven games**, where aim, reflexes and timing decide outcomes.
  - **Logic locked inside an engine build.** Driving the running game works, but slowly,
    with small samples.
  - **Deep strategy games**, where the bots can't play near human strength. Seat and
    strategy results then describe the bots.
  - **Negotiation, bluffing, table talk and kingmaking.**
  - **Player-driven markets and trading.**
  - **Live-ops systems** (events, personalised offers), unless you describe them.
- **The agent can make mistakes.** The skill makes it replay its simulator against the
  rules, check known answers and calibrate where it can, but a wrong reading of an
  ambiguous rule can still slip through. That's why every assumption is listed.
- **Time.** On a slow machine, large simulations take tens of minutes, and Python search
  bots are slow.

## Why we built this

We're [Chugli Games](https://chugligames.com), a small studio making story games set in
Indian homes. While balancing our 21-day merge game, *A Big Fat Indian Wedding*, we kept
getting confident balance advice, from people and from AI, that didn't survive contact
with the numbers. A board we thought was getting tight never filled up once in thousands
of simulated days. A fix that sounded obvious changed nothing. So we wrote a simulator for
our own game, and then turned the method into this skill, so any designer can get numbers
they can check instead of opinions.

## How it works

```
skills/game-balance-audit/
  SKILL.md                 the workflow the agent follows
  scripts/sim-kit.mjs      simulation toolkit for JS/TS games: seeded runs, per-segment luck, bots, what-ifs
  scripts/sim_kit.py       the same for Python, rulebooks and everything else
  scripts/analyze.py       results → exact checks, scorecard, flags, what-if comparisons, charts (Python 3.7+, stdlib only)
  references/              design goals by business model, building the simulator, what to measure per kind of
                           game (including chance systems), a catalogue of fixes, report template, sourced benchmarks
examples/                  six made-up games with planted problems, and the skill's unedited audits of them
evals/                     a `claude plugin eval` case per example, with answer keys in evals/reference/
tests/                     unit tests, run on every push
```

## Contributing

Found a number that's wrong? Use the
[**Report a wrong calculation**](https://github.com/chugligames/game-balance-audit/issues/new?template=wrong-calculation.yml)
issue form: correctness is the point of this skill, and every report gets a public fix.
For anything else, issues and pull requests are welcome. Run the tests with
`python3 -m unittest discover -s tests` and `node --test tests/sim-kit.test.mjs`.

See [CHANGELOG.md](CHANGELOG.md) for what changed in each release.

## Licence

MIT © Chugli Games. See [LICENSE](LICENSE).
