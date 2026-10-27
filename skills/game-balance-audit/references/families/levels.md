# Level-based puzzle games

Match-3, bubble shooters, tile and block puzzles with a move limit or score target:
anything played as a sequence of separate levels with a pass or fail. The audit asks:
**how likely is each kind of player to beat each level, and does that follow the
designer's curve?**

## What to model

- The board rules exactly as the game runs them: matching, special pieces, gravity,
  refill odds, shuffles when stuck, blockers and their layers.
- Each level's definition from the game's own files: moves, colours, goals, layout.
- **Retries and boosters**, if the business model relies on them: how many attempts a
  player makes, and what a booster does.

## Player models

A random player is the floor, not a person. Build at least:

- **careless:** any valid move, or a greedy move with a high slip rate;
- **typical:** greedy on what the move itself does for the goal, with a slip rate;
- **expert:** plays each move out on a copy, chains and specials included, and prefers
  moves that keep options open.

Bots are not humans. Studios that do this at scale calibrate: they fit bot win rates to
real pass rates from analytics, then predict human pass rates for new levels. If
analytics exist, do the same for a handful of levels and report the fit. If not, report
bot win rates as **relative** difficulty (an ordering and the size of the gaps), not as
promises about players.

## Metrics per level attempt

| Metric | Why it matters |
|---|---|
| `won` (0/1) | Win rate per level and player type: the main curve |
| `movesLeft` on a win | How close the margin is; near zero means wins are luck |
| `goalDone` (share of the goal done on a loss) | Near misses feel unfair or motivating |
| `attempts` (with a retry model) | What players experience: attempts per win |
| `cascades`, `specials` | How much of the outcome is luck from the refill |
| `shuffles` | Dead boards: a sign the colour count is too high for the layout |

## Problems this family usually has

- **Spikes and walls:** a level far harder than its neighbours, or one even the expert
  almost never wins.
- **Hard levels in the wrong place:** the designer's sawtooth (hard every N levels, then
  a breather) doesn't match where the hard levels actually are.
- **Plateaus:** several levels in a row that play the same.
- **Luck-dominated levels:** typical and expert win rates are close, and `movesLeft` is
  spread wide: the refill decides, not the player.
- **Skill walls:** the expert wins easily, the typical player almost never, so the level
  needs knowledge most players don't have.

## Levers

Moves; number of colours (one of the strongest levers); goal counts; blocker placement
and layers; starting layout; refill bias toward goal colours; specials available from the
start; reordering levels; inserting a breather. Test each per level. With per-level random
streams (`rand.child(level)`), editing one level doesn't disturb the others.

## What the simulator can't tell you

Whether a loss feels fair, whether a goal is clear, whether a level is fun or only hard.
