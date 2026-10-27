# Match-3 Mini

A tiny match-3, made up for trying the skill. `match3.mjs` holds the rules and
`levels.json` the level list. There is no UI.

**How it plays.** Swap two neighbouring tiles to line up three or more of a colour.
Matches clear, tiles fall, new ones drop in, and chains can follow. Each level gives a
number of moves and a goal: collect enough tiles of one or two colours. If no move is
possible, the board reshuffles.

**How it makes money.** In-app purchases. When a level is lost, the game offers +5 moves for
900 coins (`OFFER` in `match3.mjs`); coins are sold in the shop. We want the hard levels
to be where players buy moves, without most of them quitting there.

**What the designer wants.**
- Win rates for a typical player should drift down from about 90% on level 1 to about
  45% on level 15.
- Every fifth level (5, 10, 15) is a "hard level", around 25–40% for a typical player,
  and the level after it is a breather.
- Each early level should feel a little different from the one before.
