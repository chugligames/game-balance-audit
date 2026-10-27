# game-balance-audit

An agent skill that audits a game's balance by **simulation, not opinion**, against what
*you* are optimising for.

Point your coding agent at a game: its code, a rulebook, or a running web build. It will:

1. **Work out your goals.** How the game makes money, or why it exists, decides what counts
   as a problem:
   - free-to-play: rewarded ads or purchases against engagement and players quitting;
   - premium: completion and satisfaction;
   - tabletop: fairness, close games, length on the box, more than one way to win.
2. **Build a small simulator**, reusing your game's own rule code wherever it can, or writing
   your rulebook as code.
3. **Let bots play it** hundreds of times, from careless to expert. For free-to-play games
   the bots also decide, at each wall, whether to watch an ad, pay, wait or quit.
4. **Check the results** against your goals and your intended experience. That covers
   difficulty curves, walls and revenue moments, win rate per level, seat advantage,
   dominant strategies, runaway leaders, and luck versus skill.
5. **Write an audit** that ranks the problems and gives **three suggestions for each**.
   Every suggestion is tested in the simulator and scored on your goals, with before → after
   numbers. A scorecard shows which changes are the best trade-offs.

It works for merge-2 and energy economies, match-3 and other level-based games, logic
puzzles, and strategy, board and card games, on web, mobile or tabletop.

## Install

**Claude Code, as a plugin** (recommended; it updates with the repo):

```bash
claude plugin marketplace add chugligames/game-balance-audit
claude plugin install game-balance-audit@chugligames
```

**Claude Code or another agent that reads `SKILL.md`, via the skills CLI:**

```bash
npx skills add chugligames/game-balance-audit            # into this project
npx skills add chugligames/game-balance-audit -g         # for all your projects
```

**By hand:** copy `skills/game-balance-audit/` into your project's `.claude/skills/`, or
your agent's skills folder.

Simulations need **Node 18+ or Python 3.7+**. There are no packages to install. Everything
runs on your machine.

## Use it

Open your agent in the game's folder (or next to your rulebook) and ask in plain words:

> Audit the balance of this game. It's free-to-play with rewarded ads; I want players
> watching 2–3 ads a day by week two without many quitting.

> Here's my rulebook (RULES.md). Is there a first-player advantage, and is any strategy
> dominant? It should play in about 30 minutes at 2–5 players.

> Levels 1–40 are in `levels/`. Where are the spikes, and which levels are unwinnable?
> It's a paid game, so no monetisation.

Tell it what you're optimising for if you can. If you don't, it looks for clues: ad SDKs,
shop code, energy caps, a component list. Then it asks you one short question, or states
its assumption at the top of the report.

**What you get:** a `balance-audit/` folder.

| File | What it is |
|---|---|
| `REPORT.md` | The audit: your goals, a scorecard of every change tried, problems ranked by how much they hurt your goals, and three tested suggestions for each |
| `game-model.md` | How the simulator models your game, which parts reuse your code, and every assumption it made |
| `audit.json` | Your goals, limits and intended experience, written as checks |
| `sim/` | The simulator. Re-run it after every change, or add your own what-ifs |
| `results/` | `summary.md`, `summary.json` and `charts.html` (curves, scorecard bars, fairness bars) |

Your game's own files are never edited. In a git repo, the agent offers to work on a
branch.

**How long it takes:** often 30–90 minutes of agent time, depending on the game and how
long its simulations take. Search-based "expert" bots for card and board games are the
slowest part.

## Try it on the examples

Four small made-up games, each with balance problems planted on purpose and its own
business model. Copy one into an empty folder, ask for an audit, and compare with the
answer key in `evals/reference/`.

| Example | Kind of game | Business model | What's in it |
|---|---|---|---|
| `examples/merge-mini` | merge-2 economy (JavaScript) | rewarded ads | rules module, 10 days of orders, design notes |
| `examples/match3-mini` | match-3 levels (JavaScript) | "+5 moves" sold on a loss | rules module, 15 levels, design notes |
| `examples/slide-puzzles` | logic puzzles (Python) | paid app, no ads | Rush Hour-style rules, a 12-level pack |
| `examples/market-day` | tabletop card game | pitched to publishers | a rulebook only, no code |

`evals/` holds one case per example for `claude plugin eval` (see `evals/README.md`).

## Why simulation

Most balance advice, from people or from AI, is a hunch in a confident voice. A
simulator shows what actually happens, for which kind of player, how sure you can be, and
whether a fix works. Often the obvious fix doesn't. In `market-day`, cutting the dominant
card's value barely changes its win rate, because its real edge is selling first.

What a simulator can't tell you: whether the game feels good, whether players understand
it, how real people respond to an ad offer, or anything about bluffing and table talk. The
audit says so, treats guesses (like how often players watch or quit) as dials it varies,
and lists the playtest questions that would settle them.

## How it works

```
skills/game-balance-audit/
  SKILL.md                 the workflow the agent follows
  scripts/sim-kit.mjs      simulation toolkit for JS/TS games: seeded runs, per-segment luck, bots, what-ifs
  scripts/sim_kit.py       the same for Python, rulebooks and everything else
  scripts/analyze.py       results → scorecard, flags, what-if comparisons and charts (Python 3.7+, stdlib only)
  references/              design goals by business model, building the simulator, what to measure per
                           kind of game, a catalogue of fixes, report template, sourced benchmarks
```

## Feedback

Issues and pull requests are welcome. If you run it on your game, an issue telling us what
it found, and what it got wrong, helps the most.

## Licence

MIT © Chugli Games
