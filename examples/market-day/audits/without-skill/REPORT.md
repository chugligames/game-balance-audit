# Market Day: Balance Audit

*Audit date: 2026-10-27. Method: I implemented RULES.md as a Python simulator, wrote seven bot
strategies, ran about 600,000 simulated games, and tested rule changes. Everything here can be
re-run (see "Reproduce" at the end).*

## Verdict

| Question | Answer |
|---|---|
| Is going first an advantage? | **Yes, a big one, at every player count.** Seat 1 wins 57–60% of 2-player games, 42–44% of 3-player games and 32–36% of 4-player games. Fair would be 50/33/25%. |
| Does one strategy always win? | **No.** No strategy wins every time. The strongest bot found by search wins 63% of 2-player games and 29% of 4-player games against a mixed field. That is good play, not a broken strategy. |
| Does the game reward more than one way to play? | **Only partly.** Chasing Spice and Saffron, selling sets of 3 and watching opponents all work. Two strategies the rules seem to invite are traps: collecting Rice and Lentils (4–9% win rate) and holding out for a Big sale (11–14%). |
| Are games close at the end? | **At 2 players, often not.** The average 2-player game is won by 12 coins out of about 105 in play, and only 18% of games end within 3 coins. 3 and 4 players are closer: 25–35% of games end within 3 coins. |

**Most important fix:** deal later seats a bigger starting hand: **3 / 4 / 4 / 5 cards** for
seats 1–4. In testing, this brought seat 1's edge from +7–11 points down to within about ±2
points at every player count (details below).

## How the audit was done

- **Simulator** (`sim.py`): implements every rule in RULES.md: 54-card deck, coin stacks
  that fall to 1 coin each when empty, the 7-card hand limit, Big-sale extra turns, and the
  game ending when the market can't be refilled.
- **Bots:**
  - **Greedy:** takes cards that build its sets, sells at 3 of a kind, and sells early if
    an opponent is collecting the same good.
  - **QuickPairs:** sells every pair right away.
  - **BigSale:** holds out for 4+ cards to get the extra turn.
  - **Saffron:** only collects the expensive goods.
  - **Cheap:** collects the common Rice and Lentils, aiming for Big sales.
  - **Denier:** like Greedy, but also takes cards opponents need.
  - **Random:** picks a random legal move.
- **Strategy search:** a random search over 40 versions of a bot with adjustable settings
  (preference for each good, when to sell, how much to block opponents, endgame timing). Each
  version played 1,000 games against a mixed field at 2 and 4 players, to look for anything
  that dominates.
- **Sample sizes:** 4,000 games per cell for the main tables. The 95% margin of error is
  ±1.5 points at 2 and 3 players and ±1.3 at 4. The fix tests used 2,000 games per cell
  (about ±2 points).

### Rule interpretations (please confirm. These are gaps in RULES.md.)

1. **When exactly does the game end?** I assumed it ends straight after the Take that empties
   the deck, and that unsold cards score nothing. I also tested "finish the round", where play
   continues until every player has had the same number of turns.
2. **Are hands secret?** I assumed starting hands are secret but cards taken from the market
   are public, so players can track them. The rules don't say.
3. **Discards** are removed from the game. The rules don't say where they go.
4. **Ties** are split evenly in the statistics. The rules have no tie-breaker.

## Finding 1: Going first is a big advantage

Seat win rates when every player uses the same bot (4,000 games each):

| Players | Bot | Seat 1 | Seat 2 | Seat 3 | Seat 4 | Fair |
|---|---|---|---|---|---|---|
| 2 | Greedy | **58.1%** | 41.9% | | | 50% |
| 2 | QuickPairs | **58.4%** | 41.6% | | | 50% |
| 2 | Denier | **58.6%** | 41.4% | | | 50% |
| 3 | Greedy | **42.2%** | 31.9% | 25.9% | | 33.3% |
| 3 | QuickPairs | **43.1%** | 32.9% | 24.0% | | 33.3% |
| 3 | Denier | **43.6%** | 30.0% | 26.3% | | 33.3% |
| 4 | Greedy | **36.3%** | 25.5% | 20.1% | 18.1% | 25% |
| 4 | QuickPairs | **34.6%** | 26.1% | 21.4% | 17.9% | 25% |
| 4 | Denier | **35.1%** | 24.6% | 20.8% | 19.5% | 25% |

Even the Random bot shows seat 1 ahead (53% at 2 players, 39% at 3, 29% at 4). For comparison,
many published games keep the first-seat edge within about 2–3 points, so +8 to +11 points is
the kind of gap publishers' playtesters tend to notice.

**Why it happens.** There are three causes, and they add up:

- **First pick of the opening market.** If the opening 5 cards include Saffron or Spice, seat
  1 takes it.
- **First access to the best coins.** Coin stacks pay most to whoever sells first: the first
  Saffron sold earns 9 coins, the last earns 7, and Spice runs from 6 down to 3. Seat 1 is
  ahead in every race to complete a set.
- **Extra turns.** The game stops the moment the deck runs out, part-way through a round.
  Earlier seats therefore average more turns: 30.6 vs 30.1 at 2 players, and 14.2 / 14.0 /
  13.7 / 13.4 at 4 players. In the Greedy mirror, seat 1 averages 54.3 coins against 51.0 for
  seat 2 at 2 players, and 27.6 against 23.2 for seat 4 at 4 players.

**Fixes tested** (difference between seat 1's win rate and a fair share, in percentage
points; 2,000 games per cell):

| Variant | 2p | 3p | 4p | Comment |
|---|---|---|---|---|
| As written | +7 to +10 | +9 to +11 | +7 to +9 | |
| Finish the round (equal turns) | +6 to +9 | +8 to +10 | +6 to +8 | Helps only a little. Turn count is not the main cause. |
| **Starting hands 3/4/4/5 by seat** | **−1 to +2** | **+1 to +2** | **−2 to −1** | **Recommended.** All seats within about ±3 points of fair. |
| 3/4/4/5 + finish the round | −2 to +1 | 0 to +1 | −4 to −2 | Over-corrects at 4 players. Seat 4 wins 29–30%. |
| 3/4/5/6 + finish the round | −2 to +1 | −7 to −5 | −7 to −6 | Over-corrects badly. |

With 3/4/4/5 at 4 players, seat 4 wins 26–29% against a fair 25%, so it leans slightly the
other way. If playtests show the same, try **3/4/4/4** at 4 players. I did not simulate that
variant.

## Finding 2: No strategy always wins, but some are traps

**2-player head-to-head** (seats alternate; win rate of the row bot against the column bot;
4,000 games each):

| | Random | Greedy | QuickPairs | BigSale | Saffron | Cheap | Denier |
|---|---|---|---|---|---|---|---|
| **Greedy** | 100% | – | 68% | 87% | 71% | 97% | 54% |
| **Denier** | 100% | 47% | 66% | 87% | 67% | 97% | – |
| **QuickPairs** | 100% | 33% | – | 81% | 58% | 94% | 37% |
| **Saffron** | 100% | 29% | 42% | 74% | – | 93% | 33% |
| **BigSale** | 96% | 13% | 21% | – | 27% | 91% | 13% |
| **Cheap** | 63% | 3% | 6% | 9% | 7% | – | 4% |

**Win rate of one bot playing against Greedy opponents**, seats rotated:

| Bot | 2p (fair 50%) | 3p (fair 33%) | 4p (fair 25%) |
|---|---|---|---|
| Denier | 46% | 30% | 23% |
| QuickPairs | 31% | 25% | 23% |
| Saffron | 29% | 24% | 22% |
| BigSale | 13% | 13% | 11% |
| Cheap | 4% | 4% | 5% |

What this shows:

- **Nothing dominates.** Greedy and Denier are nearly even with each other (54/46). The best
  bot from the strategy search won 63% at 2 players and 29% at 4 players. That bot prefers
  Spice and Saffron, sells at 4, blocks moderately and races opponents. Every result needs
  real decisions to reach, which is healthy.
- **Most of the coins are in the expensive goods.**
  - **Saffron:** 11% of the deck, but 36% of the coins in the stacks (31 of 86).
  - **4-card sale values:** Rice 8, Lentils 11, Cloth 14, Spice 18, Saffron 31.
  - **Result:** strong bots all lean toward Spice and Saffron. Rice and Lentils are mostly
    filler or cards you take to block.
- **"Collect the cheap stuff" is a trap.** It wins 4–9% of games. There are 15 Rice cards,
  but Rice's whole stack is worth only 10 coins.
- **"Hunt for Big sales" is a trap.** It wins 11–14% of games. The extra turn rarely makes
  up for leaving cards unsold for so long, and it only comes up about once per game. Because
  of the 7-card hand limit, you can never chain two Big sales.
- **The designer's goal of "more than one way to play" is only partly met.** The working
  strategies differ in when they sell and how much they block. They do not differ in which
  goods they collect.

**A fix I tested that did *not* work.** I made the stacks flatter (Rice 4-3-3-2-2-1,
Lentils 5-4-3-3-2, Saffron 7-6-5-5) to make the cheap goods worth collecting. The cheap and
Big-sale bots got *worse* (Cheap 1–2%, BigSale 5–6%). Raising per-card values does not make
a cheap-goods strategy work. What these strategies need is a reward for **volume**.

Ideas to playtest (not simulated):

- Make the Big sale give a bonus coin token (for example +3 or +5) instead of, or as well
  as, the extra turn.
- Lower the Big-sale threshold to 3 cards for Rice and Lentils only.

## Finding 3: Close games

| Players | Average winning margin (Greedy mirror) | Games won by 3 coins or less |
|---|---|---|
| 2 | 12.4 coins (winner averages about 59 of the 105 coins in play) | 18% |
| 3 | 9.2 coins | 25% |
| 4 | 8.4 coins | 26% |

With the other bots, 2 players show 11–18 coin margins and 4 players show 6.6–8.4 coin margins.
The 2-player game in particular tends to be decided before the end. A big reason is that
whoever wins the race for the first Saffron and Spice sales gets a large lead (the first two
Saffron cards sold earn 17 coins). Making the top Saffron coins smaller (for example 8/7/7/6)
would probably tighten games and weaken the race. I did not simulate that change.

## Recommendations, in priority order

1. **Starting hands of 3 / 4 / 4 / 5 by seat.** Tested. This fixes the first-player problem
   at every player count.
2. **Write down the end-of-game rule, hidden-hand rule, discard rule and tie-breaker.** These
   are the four gaps listed under "Rule interpretations".
3. **Give volume a reward** so Rice and Lentils become a real strategy. For example, a Big
   sale earns a bonus token. Not tested; flatter stacks were tested and did not help.
4. **Consider cutting the top Saffron coins** to tighten 2-player games. Not tested.

## Limits of this audit

- **Bots aren't people.** They play a fixed heuristic, don't bluff, and don't plan many turns
  ahead. Strong human players will probably widen the gap between strategies; the
  first-player advantage should hold, because every bot showed it.
- **Hidden information is simplified.** Bots know every card an opponent took from the
  market, and nothing more.
- **Several results are untested ideas.** Recommendations 3 and 4, and the 3/4/4/4 variant,
  were not simulated.
- **The search was small.** It tried 40 bot settings, so a stronger line of play may exist.
  Still, no setting came close to "always wins".

## Reproduce

```
cd balance-audit
python3 experiments.py 4000 all   # seat, matchup, coin and search tables (~15 min)
python3 fixes.py 2000             # rule-fix tables (~8 min)
```

Raw output is saved in `results.txt` and `fixes.txt`.
