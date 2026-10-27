# Merge Mini

A tiny merge-2 game, made up for trying the skill. `game.mjs` holds its rules the way a
real web game keeps its logic module: board, generators, merging, orders and energy.
There is no UI.

**How it plays.** Tap the oven or the loom to make a tier-1 item (1 energy). Drag two
equal items together to make the next tier. Each day brings a list of orders; deliver
them all to finish the day. Energy refills by 1 every 2 minutes up to 100. A new day
unlocks every morning.

**What the designer wants.**
- Days 1–2 are a gentle start.
- From day 3 each day should take more effort than the one before, so day 10 feels
  like a finale.
- By days 8–10 a player who plays twice a day should use most of their free energy,
  and sometimes run out.
- The board should start to feel crowded from about day 6, so players have to think
  about what to keep.
