# game-balance-audit

An agent skill that audits a game's balance by **simulation, not opinion**.

Point it at a game (its code, a rulebook, or a running web build) and it:

1. works out how the game plays and what you want from it (which days or levels should
   feel hard, what must never happen);
2. builds a small simulator, reusing your game's own rule code wherever it can;
3. lets bots, from careless to expert, play hundreds of seeded games, days or levels;
4. checks the results against your intent: difficulty curves, walls, limits that never
   bite, win rate per level, seat advantage, dominant strategies, runaway leaders, luck
   versus skill;
5. writes an audit that ranks the problems and gives **three suggestions for each, every
   one tested in the simulator** before it is recommended, with before → after numbers.

It works for merge-2 and energy economies, match-3 and other level-based games, logic
puzzles, and strategy, board and card games, on web, mobile or tabletop.

## Install

As an agent skill (Claude Code and other agents that read `SKILL.md`):

```bash
npx skills add chugligames/game-balance-audit
```

As a Claude Code plugin:

```bash
claude plugin marketplace add chugligames/game-balance-audit
claude plugin install game-balance-audit@chugligames
```

Needs Node 18+ or Python 3.7+ to run simulations. No packages to install.

## Use

In your game's repository, or next to your rulebook:

> Audit the balance of this game. Days 1–3 should be easy, and it should get steadily
> harder until day 21.

> Here's my rulebook (RULES.md). Is there a first-player advantage, and is any strategy
> dominant?

> Levels 1–40 are in `levels/`. Where are the spikes, and which levels are unwinnable?

You get a `balance-audit/` folder: `REPORT.md` (the audit), `game-model.md` (how the
simulator models your game, and every assumption), `audit.json` (your intent as checks),
the simulator itself, raw results and charts. Re-run it after every change.

## What's inside

```
skills/game-balance-audit/
  SKILL.md                 the workflow the agent follows
  scripts/sim-kit.mjs      simulation toolkit for JS/TS games (seeded runs, bots, what-if scenarios)
  scripts/sim_kit.py       the same for Python, rulebooks and everything else
  scripts/analyze.py       turns results into flags, what-if comparisons and charts (stdlib only)
  references/              how to build the simulator, what to measure per game family,
                           a catalogue of fixes, report template, sourced benchmarks
examples/                  four small made-up games with planted balance problems
evals/                     test prompts and reference simulators for the examples
```

## Try it on the examples

Each example hides a few balance problems. Ask your agent to audit one and compare with
`evals/evals.json`:

| Example | Family | What's in it |
|---|---|---|
| `examples/merge-mini` | merge-2 economy (JavaScript) | rules module, 10 days of orders, design intent |
| `examples/match3-mini` | match-3 levels (JavaScript) | rules module, 15 levels, design intent |
| `examples/slide-puzzles` | logic puzzles (Python) | Rush Hour-style rules, a 12-level pack |
| `examples/market-day` | tabletop card game | a rulebook only, no code |

## Why simulation

Most balance advice, from people or from AI, is a hunch in a confident voice. A
simulator shows what actually happens, for which kind of player, how sure you can be, and
whether a fix works. Often the obvious fix doesn't: in `market-day`, cutting the
dominant card's value barely changes its win rate, because its real edge is selling first.

What a simulator can't tell you: whether the game feels good, whether players understand
it, or anything about bluffing and table talk. The audit says so and lists the playtest
questions that would answer it.

## Licence

MIT © Chugli Games
