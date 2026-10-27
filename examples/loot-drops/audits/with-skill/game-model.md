# Game model: the Royal Chest (`drops.js`)

## What a pull does
One pull costs 160 gems (bought with real money). Each pull:
1. Both counters go up by one: `sinceLegendary`, `sinceEpic`.
2. **Legendary** if `rand() < legendaryChance(sinceLegendary)`. That resets both counters.
3. Otherwise **epic** if `sinceEpic >= 10` (epic pity) or `rand() < 0.06`. That resets `sinceEpic`.
4. Otherwise **rare**.

`legendaryChance(n)`, where n counts this pull:
- n ≤ 75: 0.4%
- 76 ≤ n ≤ 90: 0.4% + 5 points × (n − 76), so 0.4% at 76, 5.4% at 77 … 70.4% at 90
- n > 90: 100% (**`>`, not `>=`**, so the guarantee lands on pull 91)

The Rates screen shows `RATES_TEXT`: "Legendary: 0.4% (1.6% overall with pity; guaranteed
within 90 pulls). Epic: 6% (guaranteed within 10 pulls)."

## Segment
One **cycle** = a fresh player (both counters 0) pulling until their first legendary. The
legendary chain doesn't depend on epics, so every cycle is identical in distribution and
the long-run rate is 1 ÷ mean cycle length.

## Params (what a fix can change)
`baseLegendary` 0.004 · `baseEpic` 0.06 · `softFrom` 76 · `softStep` 0.05 · `hardPity` 90 ·
`hardInclusive` false (the game's `>`) · `epicPity` 10 · gems per pull 160.

## How it is simulated
- `sim/exact.py`: exact answers as fractions. The pulls-to-legendary distribution is
  P(first on n) = pₙ ∏ₖ₍ₙ₎(1 − pₖ). The long-run epic rate is a renewal-reward sum over one
  legendary cycle, with the probability mass tracked over `sinceEpic`.
- `sim/sim.mjs`: the **baseline imports the game's own `pull()`** from `../../drops.js`,
  with `Math.random` seeded through `withSeededMathRandom`. The what-ifs use `pullWith(params)`,
  a line-for-line transcription with the constants as params.
- Seeds: `--seed 1`, 20,000 runs per scenario, with common random numbers across scenarios.

## Checks (step 4)
| Check | Result |
|---|---|
| Transcription: `pullWith(baseline)` against the game's `pull()`, same seed, 200,000 pulls | 0 mismatches |
| Exact against simulated, 8 quantities (`results/summary.md`) | all inside the 95% interval |
| Long run, game's own `pull()`, 5,000,000 pulls, seed 11 | legendary 1.441% (exact 1.4389%); epic 12.319% (exact 12.317%) |
| Longest cycle seen in 20,000 baseline runs | 91 pulls (9 runs went past 90; exact expectation 8.2) |
| Metric that never moves: `emptyTen` | Always 0. Epic pity really does guarantee an epic or better within 10 pulls (longest rare streak 9) |
| Real data | None available. There are no player decisions to model: the pull outcomes are exact |

## Assumptions
- `rand()` is uniform on [0, 1). The game's real random number generator is not tested.
- Players are not modelled as deciding anything: a pull's outcome doesn't depend on skill. The
  revenue effect of a change is shown only as gems per legendary (160 × mean pulls).
  Whether players spend more or less when legendaries come sooner is **not** modelled.
- "About 60 pulls on average" is read as a mean of 55–65.
