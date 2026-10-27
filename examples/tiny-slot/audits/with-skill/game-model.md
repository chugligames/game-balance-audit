# Ladoo Spin: the game as the simulator models it

Source: `reels.csv`, `paytable.csv`, `README.md` (no code exists). The rules are written as
code in `sim/slot.py`, and the 30-day player simulation is in `sim/sim.py`.

## Rules
- There are 3 reels of 12 stops each, and every stop is equally likely: 12³ = 1,728 outcomes.
- Only the centre line pays. If it matches several paytable lines, only the highest one pays.
  A win pays bet × multiplier, and the bet is deducted on every spin.
- Paytable lines (`slot.PAYS`):
  - LADOO×3 pays 200, DIYA×3 50, CHAI×3 25, MANGO×3 10.
  - Any three of {LADOO, DIYA, CHAI, MANGO} pays 2.
  - CHILLI on reels 1 and 2 (reel 3 anything) pays 5.
  - CHILLI on reel 1 pays 1.
- Bets are 1 to 100 coins. The daily gift is 500 coins and the starting balance is 500 coins. Coins can be bought in the shop.

## Symbol counts (from `reels.csv`)
| Symbol | Reel 1 | Reel 2 | Reel 3 |
|---|---|---|---|
| MANGO | 4 | 3 | 3 |
| BLANK | 4 | 1 | 5 |
| CHILLI | 1 | 3 | 0 |
| DIYA | 1 | 2 | 2 |
| CHAI | 1 | 2 | 1 |
| LADOO | 1 | 1 | 1 |

## Segment and row
One segment is one day, and each run covers 30 days. Each row records:
- the day's spins, coins bet (`coinIn`), coins won, `rtp`, `hitRate` and `bigRate` (40× or more);
- `drift` (gift + wins − bets: what happens to free coins, purchases excluded);
- `netDay` (purchases included), the end-of-day `balance`, `outOfCoins` (couldn't afford the next spin) and `purchases`.

## Params (what-ifs can change them)
- `pays` (every multiplier) and `edits` (reel-strip changes).
- `noChilli1`: a lone CHILLI on reel 1 pays nothing.
- `gift` and `giftMode` (`flat`: +gift every day; `floor`: top the balance up to `gift` if it is below it).
- `startCoins`, `maxBet` and `bigAt`.

## Player models (all assumptions; the README gives no bet sizes or session lengths)
| Profile | Spins/day | Bet | When out of coins |
|---|---|---|---|
| flat-1 | 1,000 | 1 | never runs out. A measuring profile for the exact checks |
| casual | 60 | 10 | stops for the day |
| regular | 200 | 25 | buys a 2,000-coin pack with p = 0.1, otherwise stops |
| keen | 400 | 5% of balance (1 to max bet) | buys a 5,000-coin pack with p = 0.3, otherwise stops |

There is no quit model: nobody stops playing for good. The purchase probabilities are dials, not
data.

## Checks on the simulator
1. **Replay.** `TRACE_DAY=1 python3 sim/sim.py --runs 1 --profile regular --scenario baseline`
   prints every spin. I checked the first 25 spins by hand against the rules, and all were paid correctly
   (for example, MANGO DIYA MANGO pays "three sweets" ×2, CHILLI LADOO BLANK pays ×1, and MANGO CHILLI MANGO pays nothing).
2. **Exact against simulated** (flat-1, seed 1, 200 runs × 30 days × 1,000 spins = 6 M spins):
   | Quantity | Exact | Simulated (95% interval) |
   |---|---|---|
   | RTP | 449/432 = 1.03935 | 1.0359 ± 0.0046 ✓ |
   | Hit rate | 67/216 = 0.310185 | 0.309816 ± 0.000351 (just outside) |
   | Big-win rate | 5/1728 = 0.002894 | 0.002878 ± 0.000042 ✓ |

   The hit-rate miss is about 2 standard errors. A second seed (seed 2, 6 M spins) gives a
   hit rate of 0.310199 and an RTP of 1.0423, both matching the exact values, so I read the miss as sampling noise, not a bug.
   The random-number generator is a seeded `random.Random.randrange(12)`, which is unbiased.
3. **Metrics that never change** (from the analyser): the casual and flat-1 players never run out of coins.
   That is a real result, not a bug: their daily gift is larger than anything they can lose.

## Assumptions
- DIYA counts as a "sweet", because the paytable row lists it. If it shouldn't, see the open questions in REPORT.md.
- "CHILLI on reel 1 only" pays whenever reel 1 shows CHILLI and nothing better pays.
  The CHILLI CHILLI line outranks it under the highest-win-only rule.
- The daily gift is credited at the start of each day, whatever the balance (`giftMode: flat`).
- The player profiles are invented. Use the break-even table in REPORT.md to plug in real bet data.
