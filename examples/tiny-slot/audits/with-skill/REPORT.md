# Balance audit: Ladoo Spin

**Not balanced the way you want.** Players get back 103.9% of what they bet, not 96%, so
every spin creates coins and every type of player gets richer. The paytable sheet says 96%
only because it works out every reel's odds as if all three reels were reel 1. The hit rate
(31%) and big-win rate (1 in 346 spins) are on target.

Two changes matter:
1. **Change two pays: MANGO×3 from 10 to 6 and LADOO×3 from 200 to 207.** That gives exactly 96.01%, with the hit rate and big wins unchanged.
2. **Shrink the daily gift.** At 96% RTP, a player has to bet 12,500 coins a day before the 500 free coins stop
   growing their balance. Your regular player won't drift down otherwise.

**Design goals** (from the README): coins are play money and revenue comes from coin sales.
You want:
- a regular player's balance to drift **down**, so that keen players buy;
- RTP of 96%;
- a win on about 3 spins in 10;
- a 40× or bigger win every few hundred spins.

I added one guardrail of my own: a casual player shouldn't run out of coins on more than 10% of days.

| Scenario | Exact RTP | Hit rate | Big win (40×+) | Regular player: free-coin drift per day¹ | Regular: days out of coins | Keen: packs bought in 30 days | Casual: days out of coins |
|---|---|---|---|---|---|---|---|
| **Current** | **103.94%** ✗ | 31.0% | 1 in 346 | **+683 ± 49** | 8% | 1.39 ± 0.17 | 0% |
| P1-A pays fix | 96.01% ✓ | 31.0% | 1 in 346 | +319 ± 44 | 25% | 3.17 ± 0.22 | 0% |
| P1-A + P2-A gift 150 | 96.01% ✓ | 31.0% | 1 in 346 | **+22 ± 34** | 56% | **4.56 ± 0.25** | 1% |
| P1-A + P2-B gift tops up to 500 | 96.01% ✓ | 31.0% | 1 in 346 | +50 ± 31 | 45% | 3.64 ± 0.23 | 0% |

¹ Drift is gift + wins − bets per day, with purchases left out. The ± figures are 95% intervals over 200 runs.

**How this was measured.**
- **Rules.** There is no code, so I wrote the rules from the two CSVs and the README (`sim/slot.py`).
- **Exact odds.** I enumerated all 1,728 reel outcomes and computed RTP, hit rate and big-win rate as exact fractions.
- **Simulation.** I simulated 30 days of play (`sim/sim.py`) for each player model, 200 runs per scenario, seed 1, with the same seeds in every scenario. The player models are:
  - **flat-1:** 1,000 spins at 1 coin. It is a measuring profile, used to check the simulation against the exact odds.
  - **casual:** 60 spins/day at 10 coins.
  - **regular:** 200 spins/day at 25 coins. When out of coins, it buys a 2,000-coin pack 10% of the time.
  - **keen:** 400 spins/day, betting 5% of its balance (capped at 100). When out of coins, it buys a 5,000-coin pack 30% of the time.
- **Assumptions.** All player models and purchase chances are my assumptions. You have no analytics yet, and I didn't model players quitting for good.
- **Checks.** The simulated RTP and big-win rate agree with the exact values. The simulated hit rate was about 2 standard errors off on seed 1 and matched on seed 2, so I read that as sampling noise. Details: `game-model.md`.

**Open questions for the designer.**
- (a) Is DIYA meant to count as a "sweet"? The paytable lists it, so I counted it. Without it, RTP falls to 79.9% and the hit rate to 19%.
- (b) How much does a real regular player bet per day? That one number decides whether the balance drifts down (see Problem 2).

## Problems, most harmful first

### 1. Players win back more than they bet: RTP is 103.9%, not 96% · High

**What happens.** Every 100 coins bet return 103.94 on average (exactly 449/432). So the
slot itself creates coins, before the daily gift. Every player model ends 30 days far richer than
it started:

| Player model | Median balance on day 30 | 90th percentile on day 30 |
|---|---|---|
| casual | 15,780 | 19,920 |
| regular | 21,150 | 35,700 |
| keen | 43,975 | 111,166 |

Even the keen player, who bets the most, gains about 1,450 free coins a day. Coin packs are hardly ever
needed: a keen player buys 1.4 in 30 days, and only because big bets swing the balance to zero.
This breaks the stated 96% target and the "drift down so keen players buy" goal, which is the primary revenue goal.

**Why the sheet says 96%.** Every probability on the sheet is worked out as if reels 2 and 3 had
reel 1's symbols. For example, (4/12)³ for MANGO×3, when reels 2 and 3 have only 3 MANGOs each. Its arithmetic
is otherwise right, but the inputs are wrong:

| Line | Pays | Sheet probability | Real probability (count of 1,728) | Real RTP share |
|---|---|---|---|---|
| LADOO×3 | 200 | 0.000579 | 0.000579 (1) | 11.57% |
| DIYA×3 | 50 | 0.000579 | **0.002315 (4)** | **11.57%** |
| CHAI×3 | 25 | 0.000579 | **0.001157 (2)** | 2.89% |
| MANGO×3 | 10 | **0.037037** | 0.020833 (36) | 20.83% |
| any three sweets | 2 | **0.159722** | 0.201968 (349) | **40.39%** |
| CHILLI CHILLI (reels 1–2) | 5 | **0.006944** | 0.020833 (36) | **10.42%** |
| CHILLI on reel 1 | 1 | 0.076389 | 0.062500 (108) | 6.25% |
| **Total** | | **96.01%** | | **103.94%** |

If odds are ever shown to players, the sheet's numbers would be wrong disclosures.

**Three suggestions, each tested exactly and with 200 runs × 30 days on the same seeds as the current game.**

| | Change | RTP, before → after (exact) | Hit rate | Big win | Regular drift/day | Fixes / breaks | Cost |
|---|---|---|---|---|---|---|---|
| A | **Tune pays:** MANGO×3 10→6, LADOO×3 200→207 | 103.94% → **96.01%** (553/576) | 31.0% (same) | 1 in 346 (same) | +683 → +319 | Fixes RTP. Breaks nothing | A slightly bigger jackpot; the MANGO line feels smaller |
| B | **Strip:** reel 2 stop 7 MANGO→CHILLI | → 95.49% (275/288) | 28.2% | 1 in 346 | +305 | RTP 0.01 point below a 95.5% floor; hit rate stays inside "about 3 in 10" | One-stop change, easy to ship |
| C | **Rule:** a lone CHILLI on reel 1 pays nothing; CHILLI CHILLI 5→4 | → 95.60% (413/432) | **24.8%** | 1 in 346 | +299 | Fixes RTP but drops the hit rate to 1 in 4 | Fewer small wins |

These are the closest single-stop changes. Many others fix RTP but change the big wins.
For example, LADOO→MANGO on reel 1 gives 96.6% but makes big wins 1 in 432 and halves volatility.

**Recommendation: A.** It is the only option that lands on 96% while leaving the hit rate and big-win rate
exactly where you want them. A one-pay alternative, MANGO×3 10→6 alone, gives 95.6%.

### 2. The 500-coin daily gift outweighs the house edge, so balances still grow at 96% · High

**What happens.** At 96.01% RTP, the house keeps 3.99% of every coin bet. Free coins only drift
down once a player bets more than 500 ÷ 0.0399 ≈ **12,500 coins a day**, which is 125 spins at the maximum bet.

| Coins bet per day | Expected free-coin drift/day at 96.01% |
|---|---|
| 600 (casual: 60 × 10) | +476 |
| 5,000 (regular: 200 × 25) | +300 (simulated: +319 ± 44) |
| 12,500 | 0 |
| 40,000 (400 × max bet) | −1,096 |

With fix A alone, the regular player's median balance is about 10,000 coins on day 30, and the casual player's about 14,250.
The keen player does drift down, to a median of 322, but only because they scale their bets up as they get richer.
This hurts the primary goal: a regular player has no reason to buy.

**Three suggestions, each tested** (all on top of fix A; 200 runs; same seeds):

| | Change | Regular drift/day, after fix A → after | Regular: days out of coins | Keen packs / 30 days | Casual days out of coins | Cost |
|---|---|---|---|---|---|---|
| A | **Tune:** daily gift 500 → 150 | +319 → **+22 ± 34** | 25% → 56% | 3.17 → **4.56** | 0% → 1% | Casual balances still grow (median 3,790 on day 30); a smaller headline gift |
| B | **Rule:** the gift tops the balance up to 500 instead of adding 500 | +319 → +50 ± 31 | 25% → 45% | 3.17 → 3.64 | 0% | No hoarding (casual median 1,040 on day 30); nobody is ever left with nothing |
| C | **Content:** raise the maximum bet 100 → 500 | +319 → +319 (no change) | 25% (no change) | 3.17 → 4.29 | 0% | Changes only big bettors; does nothing for the regular player |

C is an inert lever for the regular player, who never bets near the cap. It is recorded because it's the obvious idea.
A is the scorecard's only best trade-off: it keeps every constraint, and no other scenario does better on both goals.
B is the safer one for retention: it never leaves a player at zero, and it stops casual players hoarding.

**Recommendation: A or B, depending on how much churn risk you'll take.**
- A brings in the most purchases.
- With A, though, the 25-coin regular player runs dry on 56% of days. The simulator has no quit model, so it can't tell whether that sells coin packs or loses the player.
- Without data I'd ship B, then tune the top-up level (500 → 300) if drift is still positive.

Either way, **check what real regulars bet per day.** Everything in this section scales with
that number, through the break-even table above.

## Recommended changes together

Fix 1A + fix 2A is the "P2-A" row. Fix 1A + fix 2B is the "P2-B" row. Both keep:
- RTP at 96.01%;
- the hit rate at 31.0%;
- big wins at 1 in 346 spins.

Neither combination breaks anything that the single changes didn't. See the table at the top.

## Also noticed

- **Volatility.** The standard deviation per spin is 5.7× the bet, and nearly half of RTP (40%) comes from the 2× "three sweets" line.
  Most wins are small, and the big two (LADOO and DIYA) carry 23% of RTP between them.
  This is fine for "something to chase", but it means a 25-coin regular player's day swings by ±1,000 coins or more. That spread, not drift, is what empties wallets today.
- **Disclosure.** The sheet's probability column is wrong. Don't reuse it on any odds screen.

## What this audit can't tell you

- **Whether running dry makes a player buy or leave.** Playtest or A/B test: with the gift at 150 or the top-up rule, compare
  day-7 retention and payer conversion against the current gift.
- **Real bet sizes and spins per day.** These set the break-even point. Pull them from analytics as soon as there are any.
- **Feel.** Whether 2× "three sweets" wins on 20% of spins read as wins or as losses disguised as wins, and whether
  a 207× LADOO line looks odd next to round numbers.
- **Certification.** This is design analysis only, not fairness or legal certification, and it doesn't test your random-number generator.

## Re-running it

```bash
cd balance-audit
python3 sim/sim.py --runs 200 --seed 1 --out runs/all.jsonl          # ~5 min
python3 <skill>/scripts/analyze.py audit.json runs/all.jsonl --out results
TRACE_DAY=1 python3 sim/sim.py --runs 1 --profile regular --scenario baseline   # spin-by-spin replay
```

Exact odds for any what-if: `table(params)` in `sim/sim.py`, or `exact(reels, pays)` in `sim/slot.py`.
