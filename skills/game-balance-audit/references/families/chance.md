# Chance systems: slots, loot tables, gacha, dice

Paytables, reel strips, drop tables with pity counters, dice and card odds: anything where
the balance question is "what does chance pay out, how often, and how swingy is it". These
systems are usually small enough to **compute exactly**. Do that first, and use simulation
to cross-check and to cover what the exact maths can't reach (a player's balance over a
month, how daily gifts interact with spending).

## Exact before estimated

- **Small, equally likely outcome spaces** (reel stops, dice, a deck): enumerate them, or
  multiply symbol counts. A 3-reel slot with 12 stops a reel has 12³ = 1,728 outcomes.
  Compute RTP, hit rate and big-win rate as **fractions** (Python's `fractions.Fraction`),
  so nobody has to trust floating point.
- **Counters and streaks** (pity, "guaranteed within N", win streaks): the pulls to a drop
  form a chain. With per-pull chances pₙ, P(the first drop is on pull n) = pₙ ∏ᵢ₍ₙ₎ (1 − pᵢ).
  The mean, median, 90th percentile, longest possible streak, and the chance of passing a
  promised guarantee all follow exactly.
- **Bigger state spaces** (multi-counter pity, bonus rounds with retriggers): dynamic
  programming over the states, or a Markov chain solved with fractions. Only when the
  state space is too large, simulate.

Then **simulate anyway**, written straight from the rules (the game's own code where it
exists), with a stated seed and number of iterations, and report the simulated value
with its 95% interval next to the exact one. Put the exact value in `audit.json` under
`exact` (see `references/audit-config.md`); the analyser checks that the interval
contains it. Disagreement means the simulator, or your reading of the rules, is wrong. Fix
that before anything else. Agreement is what lets a reader trust the rest of the audit.

## Inputs you'll meet

- **Spreadsheets** (CSV or exported sheets): reel strips, paytables, drop tables, economy
  sheets. Read the raw data columns (strips, weights, prices), and **recompute every
  derived column** (probabilities, RTP contributions, totals) yourself. Hand-made sheets
  are often wrong: a shortcut that treats unequal reels as equal, a stale count after a
  strip changed, overlapping wins counted twice. For `.xlsx`, ask for a CSV export, or read
  the XML inside the file with the standard library (it is a zip).
- **Code snippets** (a drop formula, a damage roll): import or transcribe them exactly,
  including comparison operators. `>` against `>=` at a pity boundary is a classic bug.
- **A design doc or a Rates screen:** every number a player is shown is a claim to check
  against the formula.

## Metrics

| Metric | Why it matters |
|---|---|
| RTP (return to player): average paid back per unit bet | Above 1 in a play-money economy is an inflation loop: every spin creates currency |
| Hit rate; big-win rate (e.g. 40× or more) | How often play feels rewarding, and how often there's a story to tell |
| Standard deviation per spin | Volatility: how far a balance swings, how fast players go broke |
| Mean, median and 90th-percentile pulls to a drop; the longest possible streak | What players actually experience. The mean alone hides that most players reach pity |
| Overall ("consolidated") drop rate = 1 ÷ mean pulls | The figure Rates screens usually advertise |
| Currency per item (pulls × price) | What a drop costs players and earns the game |
| Balance over time for player profiles (daily gifts, bet sizes, purchases) | Whether the economy drains, holds or inflates |

## Problems this family usually has

- **The sheet's totals are wrong.** The stated RTP or rate doesn't follow from the
  sheet's own raw data.
- **A published claim is false.** The odds or guarantees shown to players don't match the
  formula. App stores require disclosed odds for paid random items, so treat this as a
  blocker, not polish.
- **Inflation:** RTP above 1, or sources that outrun sinks, so currency piles up and prices
  stop meaning anything.
- **Boundary bugs:** an off-by-one at a pity threshold or a cap.
- **Experience off target:** the average looks fine, but the median player needs far more
  (or the volatility is so high that most sessions are losses).

## Levers

Reel strip counts (most precise: one stop changes RTP by a known fraction); pay values;
which combinations pay; pity start, step and hard cap; base rates; price per pull; daily
gifts. Recompute exactly after each change. Exact what-ifs are cheap, so test many.

## Limits

Exact maths and simulation estimate how a system behaves. They are **not** certification.
Real-money gambling games need an accredited test lab and the regulator's approval in each
market. This skill's output is design analysis only. It doesn't certify fairness,
randomness or legal compliance, and it can't test the game's random number generator.
