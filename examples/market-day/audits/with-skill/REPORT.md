# Balance audit: Market Day

Market Day has one serious balance problem: **turn order decides too many games**. Seat 1
wins 59% of 2-player games, 45% at 3 players (fair: 33%) and 35% at 4 (fair: 25%). Expert
bots show it too, so it isn't a quirk of simple play. **No strategy always wins.** Holding
cards for 4-card big sales is the best plan at 2 players (59% against a steady seller), but
the worst at 4. The most important change is to give later seats a few starting coins:
**+3 for seat 2 at 2 players, and +2/+4/+6 for seats 2/3/4 at 3–4 players.** In the
simulator that brings every seat to within about 3 points of fair.

**Design goals** (from your note in RULES.md): be fair at every player count, keep games
close to the end, and reward more than one way to play. The audit treats fairness as the
primary goal. Each seat's win rate should be within 5 points of fair at every player
count. The other two goals are guardrails.

| Scenario | Seat 1 wins 2p (fair .50) | 3p (fair .33) | 4p (fair .25) | Last seat 4p | Best plan vs steady, 2p |
|---|---|---|---|---|---|
| Baseline | **.59** | **.45** | **.35** | **.16** | bigsale .59 |
| P1-a start coins (recommended) | .48 | .36 | .23 | .26 | bigsale .59 |
| P1-b finish the round | .58 | .44 | .34 | .17 | bigsale .59 |
| P1-c extra starting cards | .44 | .29 | .22 | .28 (seat 2 at 3p .41) | bigsale .56 |
| P1-a + P2-b together | .48 | .36 | .23 | .26 | quick .55, bigsale .51 |

**How this was measured.** I wrote the rules as code (`sim/sim.mjs`); there is no game code
to import. The player models:
- **steady**: a sensible greedy seller (sells sets of 3+).
- **quick**: sells every pair at once.
- **bigsale**: holds for 4-card sets.
- **luxury**: chases Spice and Saffron.
- **careless**: steady with 30% random moves.
- **expert**: Monte Carlo lookahead that can't see hidden cards.

Each table is 1,000 games with seed 1, the same deals in every scenario. A win rate is
therefore good to about ±3 points (95%). There is no playtest data to calibrate against.
The simulator reproduces the exact number of Takes per game (44 / 41 / 38), and a full
game was traced move by move against the rules. Details are in `game-model.md`.

**Open questions for you** (the rules don't say):
1. Does the game end immediately when the market can't refill, or does the round finish?
   I tested both, and it makes no difference to the seat problem.
2. Are unsold cards worth nothing at the end?
3. How are ties broken? 5% of 2p games tie.
4. Is the discard when over 7 cards your choice, and does the card leave the game?
5. Are hands secret?

## Problems, most harmful first

### 1. The first player wins far too often, at every player count · High

**What happens.** With identical bots in every seat, the first player wins about 1 game in
6 more than fair, and the advantage runs all the way down the table. At 4 players the last
seat wins only 16% against a fair 25%. A publisher's playtesters will notice this within an
evening. It breaks the "fair at every player count" goal.

| Players | Seat 1 | Seat 2 | Seat 3 | Seat 4 | Fair |
|---|---|---|---|---|---|
| 2 (steady) | .59 | .41 | | | .50 |
| 2 (expert mirror) | .58 | .42 | | | .50 |
| 3 (steady) | .45 | .32 | .23 | | .33 |
| 4 (steady) | .35 | .27 | .22 | .16 | .25 |

**Why.** The cause is not extra turns. Seat 1 takes only 0.4 more turns per game than seat 2
at 2p, and making everyone have equal turns (P1-b) changes nothing. The advantage is
**tempo**: the first player gets first pick of the market and first claim on the top coins
of each stack. Coin stacks fall steeply (Cloth 5→1, Lentils 4→1), so whoever sells a good
first earns noticeably more for it. Seat 1 ends 2p games about 2.8 coins ahead on average.

**Three suggestions, each tested** (1,000 games per table, same deals):

| | Change | Seat win rates, before → after | Side effects | Cost |
|---|---|---|---|---|
| A | **Tune: starting coins for later seats.** 2p: seat 2 starts with 3. 3p: 0/2/4. 4p: 0/2/4/6. | 2p .59/.41 → .48/.52. 3p .45/.32/.23 → .36/.33/.31. 4p .35/.27/.22/.16 → .23/.25/.27/.26 | Strategy results unchanged; games just as close (winner leads by 11.0 coins, was 11.2) | One setup line; uses coin tokens you already have |
| B | **Rule: finish the round** so everyone has had the same number of turns | 2p .58/.42, 3p .44, 4p .34/.17. **No real effect** | None | Recorded because it is the obvious fix and it fails. The advantage isn't the last turn |
| C | **Structure: later seats start with extra cards** (seat 2 +1, seat 3 +1, seat 4 +2) | 2p .44/.56 (overshoots). 3p .29/**.41**/.30. 4p .22/.27/.23/.28 | Creates a new favourite seat (seat 2 at 3p) | Uneven; harder to tune per count |

Doses I also tried: one flat schedule of 0/2/4/6 at every count leaves 2p at .54/.46. Using
0/3/5/7 fixes 2p but pushes seat 1 at 4p down to .20, and 0/3/6/9 over-corrects at 3–4p
(last seat at 4p wins .32). That is why A uses a different schedule per player count.

**Recommendation: A.** It is the only option that is fair at all three counts at once.
Playtest whether people find the coin handicap fiddly. A rule like "seat 2 takes 3 coins
from the bank" is the simplest wording.

### 2. Holding for big sales is the best 2-player plan, and the worst 4-player plan · Medium

**What happens.** Against a steady seller, the plans finish as follows:

| Plan | 2-player win rate | 4-player win rate (all four plans at one table, fair .25) |
|---|---|---|
| bigsale | **.59** | **.22** |
| quick | .54 | .27 |
| luxury | .47 | .25 |
| steady | baseline | .26 |

This isn't a strategy that always wins, which answers your worry. But at 2 players one plan
is clearly better, and its value flips with player count. In a 4-player game, cards you hold
are cards other players don't take, and other players sell first and take the top coins. The
expert bot finds big sales on its own, about once a game. Chasing Saffron is not dominant:
its high coins (9/8/7/7) are offset by there being only 6 cards.

**Three suggestions, each tested:**

| | Change | bigsale vs steady 2p, before → after | 4p table | Side effects |
|---|---|---|---|---|
| A | Tune: a big sale gives +3 coins instead of another turn | .59 → **.68** (worse) | .22 → .24 | The obvious fix backfires. The 4-card payout is the edge, and the extra turn is worth only about 1 coin (+1 coin .57, +2 .62, +3 .68, +5 .76) |
| B | **Rule: a big sale needs 5 cards** | .59 → **.51** | .22 → .21 | The 2p plans tighten to .46–.55. But no bot ever sells 5 at once, so the big sale becomes almost a dead rule |
| C | Structure: hand limit 6 | .59 → .56 | .22 → .26 | **Makes seat advantage worse** (2p seat 1 .64, 4p .40) and luxury drops to .44 |

**Recommendation:** B if you're happy for the big sale to become rare at 2 players. That
narrows the 2p plans from a 12-point spread to 9. Otherwise, leave this until Problem 1 is
fixed; it is the smaller issue. Avoid C.

## Recommended changes together

Running P1-a (start coins) and P2-b (big sale at 5) together keeps every seat within 3 points
of fair. 2p is .48/.52, 3p .36/.33/.31, 4p .23/.25/.27/.26. In heads-up play, the four plans
land between .47 and .55 against steady (quick .55, bigsale .51, luxury .47), and at 4p
between .22 and .27. The two changes don't interfere with each other.
**Not yet checked with expert bots.** The 45-minute budget ran out before the expert tables
for P1-a, P2-b and the combination finished, so the "after" numbers above come from the
greedy bots only. The baseline seat advantage is the same for experts (.58) as for greedy
bots (.59), so I expect the fix to carry over. Confirm it with
`node sim/sim.mjs --runs 1000 --scenario "PICKS P1-a + P2-b" --profile mirror-expert-2p,expert-vs-steady-2p --out runs/expert-picks.jsonl`
(about 5 minutes).

## Also noticed

- **Close games:** the 2p winner leads by about 11 coins out of about 54. The half-time leader
  goes on to win 71% of the time (78% between experts; 55% at 4p). The lead changes about 3
  times a game. That is reasonably close, but there is no catch-up rule, so any edge carries
  through. Worth watching in playtests.
- **Skill matters:** expert beats careless 75%, and beats steady 62%. Luck doesn't swamp
  decisions.
- About 2 cards per player go unsold at the end of the game (assumption A2).

## What this audit can't tell you

- Whether people actually play the way the bots do. Do they hoard for big sales? Do they
  notice the race for top coins?
- Whether the coin handicap feels fair or fussy.
- Table talk, and whether games are fun.

Playtest at 4 players with seat order recorded. With the fix, seat 4 should win about a
quarter of games. Ask players whether the start coins felt noticeable.

## Re-running it

```bash
cd balance-audit
node sim/sim.mjs --runs 1000 --expensive --scenario baseline --out runs/baseline.jsonl
node sim/sim.mjs --runs 1000 --scenario "<scenario names, comma-separated>" --out runs/whatifs.jsonl
python3 <skill>/scripts/analyze.py audit.json runs/*.jsonl --out results
TRACE=1 node sim/sim.mjs --runs 1 --profile mirror-2p --scenario baseline   # step through one game
```
Quick what-if: `node sim/sim.mjs --runs 2000 --profile mirror-2p,mirror-4p --set 'startCoins=[0,2,4,6]' --print won --by seat`.
