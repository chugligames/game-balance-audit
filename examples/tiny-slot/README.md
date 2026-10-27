# Ladoo Spin

A tiny three-reel slot for a social casino app, made up for trying the skill. The game is
**two spreadsheets and these notes**. There is no code.

- `reels.csv`: the three reel strips, 12 stops each.
- `paytable.csv`: what each combination pays, with the designer's own probability and
  return-to-player (RTP) columns.

**How it plays.** Bet coins (1 to 100 per spin). Each reel stops on one of its 12 stops,
each equally likely. Only the centre line pays, and only its highest win counts. Wins pay
the bet × the paytable value.

**How it makes money.** Coins are play money: they can't be cashed out. Everyone gets 500
free coins a day, and coins are sold in the shop. We want a regular player's balance to
drift *down*, so that keen players buy coins.

**What the designer wants.**
- RTP of 96%: every 100 coins bet return 96 on average.
- A win on about 3 spins in 10.
- A big win (40× or more) every few hundred spins, so there's something to chase.
