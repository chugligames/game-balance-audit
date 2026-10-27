# Rulebook mode: the game exists only on paper

Board and card game designers often have rules, card lists and a prototype, but no code.
Write the rules as a simulator yourself, with `sim_kit.py` (Python) or `sim-kit.mjs`
(JavaScript). Prefer JavaScript when you'll need a search-based expert player: Python is
often several times slower for search, and expert tables can take tens of minutes.

Ask what the designer is optimising for (`references/design-goals.md`): fairness, close
games, the length on the box, replayability, accessibility for new players. Those become
the scorecard's goals and constraints.

## Turning rules into code

1. **Inventory first.** List every component with its count (cards, tokens, tiles,
   dice) and every number in the rules. These become `params`.
2. **The game interface.** Write `start(rand)`, `actions(s)`, `apply(s, a, rand)`,
   `over(s)`, `seat(s)` and `value(s, seat)` (see `references/simulator.md`). Keep state a
   plain dict or tuple so it copies cheaply.
3. **One rule, one place.** Put each rule in one function named after the rulebook's
   section ("Big sale"), so the designer can check the code against the text.
4. **Seats and end of game.** Model turn order and the end condition exactly, including
   whether the round finishes. Seat advantage often comes from here.

## The assumptions log

Rulebooks leave gaps: ties, what happens when a supply runs out, whether the round
finishes after the end trigger, what a player may discard. For each gap:

- write the question and the assumption you made in `game-model.md` under **Assumptions**;
- choose the reading most players would use at the table;
- if an assumption could change a finding (end-of-game timing changes seat advantage),
  make it a param and run both readings. Report it as "depends on how you rule X".

List the open questions at the top of the report: answering them is useful to the
designer even before any balance change.

## Players at a real table

Bots never forget the rules, miscount or play to be nice. Ask the designer how their
playtesters actually play (cautious? aggressive? do they block each other?) and build
archetypes that match. If the game depends on negotiation, bluffing or table talk, say
plainly that the simulator covers only the mechanical part.

## Check against reality

If the designer has playtest results (who won, final scores, game length), compare a few
numbers with the simulator's before trusting it, and report the gap.
