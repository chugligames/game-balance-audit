# Balance summary: Market Day

132000 rows · baseline `baseline` + 5 what-if scenario(s) · player profiles: mirror-2p, mirror-3p, saffron-vs-steady, hoarder-vs-steady, quick-vs-steady · 2000 runs each

## Scenarios against the design goals

Each goal is measured per player over the segments it names, then averaged over runs (± is a 95% interval). ▲/▼: better/worse than the baseline beyond noise. ✗: breaks a constraint. Best trade-off: no other scenario that keeps every constraint is at least as good on every goal and better on one. Weighted change: the goals' changes from the baseline, weighted as in audit.json, only to sort the table.

| Scenario | Half-time leader wins, 2 players (lower is better) | Seat 1 wins, 2 players (0.47–0.53) | Seat 3 wins, 3 players (0.30–0.37) | Saffron plan vs steady (≤ 0.55) | Quick-sell plan vs steady (≤ 0.55) | Weighted change | Best trade-off |
|---|---|---|---|---|---|---|---|
| `baseline` | 0.83 ± 0.02 | ✗ 0.53 | ✗ 0.28 | ✗ 0.64 | ✗ 0.59 | +0% |  |
| `big-sale-+3-coins` | 0.83 ± 0.02 | ✗ 0.53 | ✗ 0.28 | ✗ 0.64 | ✗ 0.59 | +0% |  |
| `later-seat-coins` | 0.84 ± 0.02 (+0%) | ✓ 0.50 | ✓ 0.31 | ✗ 0.64 | ✗ 0.60 | −0% |  |
| `equal-turns` | 0.84 ± 0.02 (+0%) | ✓ 0.52 | ✗ 0.29 | ✗ 0.64 | ✗ 0.60 | −0% |  |
| `second-seat-+2` | 0.84 ± 0.02 (+1%) | ✓ 0.50 | ✗ 0.26 | ✗ 0.63 | ✗ 0.59 | −1% |  |
| `saffron-7-6-5-5` | 0.86 ± 0.02 (+3%) | ✗ 0.55 | ✗ 0.27 | ✗ 0.63 | ✗ 0.65 | −3% |  |


## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | uneven | saffron-vs-steady, hoarder-vs-steady, quick-vs-steady | Strategy against the steady player: strategy = hoarder has 0.365 (95% CI 0.344–0.386, n=2000) against a fair 0.500 ± 0.050 |
| high | uneven | saffron-vs-steady, hoarder-vs-steady, quick-vs-steady | Strategy against the steady player: strategy = saffron has 0.641 (95% CI 0.620–0.662, n=2000) against a fair 0.500 ± 0.050 |
| medium | off-target | mirror-2p | Comebacks stay possible: mean 0.83, target ≤ 0.75 |
| medium | uneven | mirror-2p | Seat advantage, 2 players: seat = 1 has 0.530 (95% CI 0.509–0.552, n=2000) against a fair 0.500 ± 0.020 |
| medium | uneven | mirror-2p | Seat advantage, 2 players: seat = 2 has 0.470 (95% CI 0.448–0.491, n=2000) against a fair 0.500 ± 0.020 |
| medium | uneven | mirror-3p | Seat advantage, 3 players: seat = 1 has 0.374 (95% CI 0.353–0.395, n=2000) against a fair 0.333 ± 0.030 |
| medium | uneven | mirror-3p | Seat advantage, 3 players: seat = 3 has 0.276 (95% CI 0.256–0.295, n=2000) against a fair 0.333 ± 0.030 |
| medium | uneven | saffron-vs-steady, hoarder-vs-steady, quick-vs-steady | Strategy against the steady player: strategy = quick has 0.594 (95% CI 0.572–0.615, n=2000) against a fair 0.500 ± 0.050 |

Never changes: `extraTurns` = 0.00 (mirror-2p); `extraTurns` = 0.00 (mirror-3p); `extraTurns` = 0.00 (quick-vs-steady); `extraTurns` = 0.00 (saffron-vs-steady)

## Seat advantage, 2 players

| seat | won | 95% CI | n |
|---|---|---|---|
| 1 | 0.530 | 0.509–0.552 | 2000 |
| 2 | 0.470 | 0.448–0.491 | 2000 |

Fair value: 0.500 ± 0.020.

## Seat advantage, 3 players

| seat | won | 95% CI | n |
|---|---|---|---|
| 1 | 0.374 | 0.353–0.395 | 2000 |
| 2 | 0.350 | 0.330–0.371 | 2000 |
| 3 | 0.276 | 0.256–0.295 | 2000 |

Fair value: 0.333 ± 0.030.

## Strategy against the steady player

| strategy | won | 95% CI | n |
|---|---|---|---|
| hoarder | 0.365 | 0.344–0.386 | 2000 |
| quick | 0.594 | 0.572–0.615 | 2000 |
| saffron | 0.641 | 0.620–0.662 | 2000 |
| steady | 0.467 | 0.454–0.479 | 6000 |

Fair value: 0.500 ± 0.050.

## What-ifs against the baseline

### `saffron-7-6-5-5`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p): value 0.530 → 0.548; uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p): value 0.470 → 0.452; uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p): value 0.374 → 0.398; uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p): value 0.276 → 0.271; uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.379; uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.594 → 0.650; uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.641 → 0.635; off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p)

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 46.3 | mirror-2p −6% · mirror-3p −5% · saffron-vs-steady −7% · quick-vs-steady −7% |
| turns | 28.9 | 28.9 | mirror-2p +0% · mirror-3p −0% · saffron-vs-steady +0% · quick-vs-steady +0% |
| halfLeaderWon | 0.83 | 0.86 | mirror-2p +3% · mirror-3p +1% · saffron-vs-steady +0% · quick-vs-steady +0% |

| Seat advantage, 2 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.530 | 0.548 (0.527–0.570) |
| 2 | 0.470 | 0.452 (0.430–0.473) |

Fair: 0.500.

| Seat advantage, 3 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.374 | 0.398 (0.377–0.419) |
| 2 | 0.350 | 0.331 (0.311–0.351) |
| 3 | 0.276 | 0.271 (0.252–0.290) |

Fair: 0.333.

| Strategy against the steady player: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| hoarder | 0.365 | 0.379 (0.358–0.399) |
| quick | 0.594 | 0.650 (0.630–0.671) |
| saffron | 0.641 | 0.635 (0.614–0.656) |
| steady | 0.467 | 0.445 (0.433–0.458) |

Fair: 0.500.

### `equal-turns`

- **Fixes:** uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p)
- **Introduces:** no new flags
- **Still flagged:** uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.362; uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.641 → 0.638; off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p): value 0.530 → 0.523; uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p): value 0.470 → 0.477; uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p): value 0.276 → 0.288; uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.594 → 0.596

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 49.7 | mirror-2p +1% · mirror-3p +1% · saffron-vs-steady +1% · quick-vs-steady +0% |
| turns | 28.9 | 29.1 | mirror-2p +1% · mirror-3p +2% · saffron-vs-steady +1% · quick-vs-steady +1% |
| halfLeaderWon | 0.83 | 0.84 | mirror-2p +0% · mirror-3p −2% · saffron-vs-steady −0% · quick-vs-steady −0% |

| Seat advantage, 2 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.530 | 0.523 (0.501–0.545) |
| 2 | 0.470 | 0.477 (0.455–0.499) |

Fair: 0.500.

| Seat advantage, 3 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.374 | 0.362 (0.342–0.383) |
| 2 | 0.350 | 0.350 (0.329–0.370) |
| 3 | 0.276 | 0.288 (0.268–0.307) |

Fair: 0.333.

| Strategy against the steady player: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| hoarder | 0.365 | 0.362 (0.341–0.384) |
| quick | 0.594 | 0.596 (0.575–0.617) |
| saffron | 0.641 | 0.638 (0.617–0.659) |
| steady | 0.467 | 0.468 (0.455–0.480) |

Fair: 0.500.

### `big-sale-+3-coins`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady); off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p); uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p); uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p); uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.438; uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady)

Unchanged: `coins`, `turns`, `halfLeaderWon`.

| Strategy against the steady player: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| hoarder | 0.365 | 0.438 (0.417–0.460) |
| quick | 0.594 | 0.594 (0.572–0.615) |
| saffron | 0.641 | 0.641 (0.620–0.662) |
| steady | 0.467 | 0.442 (0.430–0.455) |

Fair: 0.500.

### `second-seat-+2`

- **Fixes:** uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p); uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p)
- **Introduces:** uneven (mirror-3p): Seat advantage, 3 players: seat = 2 has 0.389 (95% CI 0.368–0.410, n=2000) against a fair 0.333 ± 0.030
- **Still flagged:** uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p): value 0.276 → 0.258; uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.366; uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.641 → 0.634; off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p); uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.594 → 0.595

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 50.4 | mirror-2p +2% · mirror-3p +2% · saffron-vs-steady +2% · quick-vs-steady +2% |
| halfLeaderWon | 0.83 | 0.84 | mirror-2p +1% · mirror-3p −1% · saffron-vs-steady −0% · quick-vs-steady −0% |

Unchanged: `turns`.

| Seat advantage, 2 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.530 | 0.501 (0.479–0.522) |
| 2 | 0.470 | 0.499 (0.478–0.521) |

Fair: 0.500.

| Seat advantage, 3 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.374 | 0.354 (0.333–0.375) |
| 2 | 0.350 | 0.389 (0.368–0.410) |
| 3 | 0.276 | 0.258 (0.238–0.277) |

Fair: 0.333.

| Strategy against the steady player: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| hoarder | 0.365 | 0.366 (0.346–0.387) |
| quick | 0.594 | 0.595 (0.574–0.616) |
| saffron | 0.641 | 0.634 (0.613–0.655) |
| steady | 0.467 | 0.468 (0.456–0.481) |

Fair: 0.500.

### `later-seat-coins`

- **Fixes:** uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p); uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p); uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p)
- **Introduces:** no new flags
- **Still flagged:** uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.365; uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.641 → 0.640; off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p); uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.594 → 0.600

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 50.3 | mirror-2p +2% · mirror-3p +3% · saffron-vs-steady +2% · quick-vs-steady +2% |
| turns | 28.9 | 28.9 | mirror-2p −0% · mirror-3p +0% · saffron-vs-steady −0% · quick-vs-steady −0% |
| halfLeaderWon | 0.83 | 0.84 | mirror-2p +0% · mirror-3p −1% · saffron-vs-steady +0% · quick-vs-steady −0% |

| Seat advantage, 2 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.530 | 0.503 (0.481–0.524) |
| 2 | 0.470 | 0.497 (0.476–0.519) |

Fair: 0.500.

| Seat advantage, 3 players: seat | Baseline | What-if (95% CI) |
|---|---|---|
| 1 | 0.374 | 0.349 (0.329–0.370) |
| 2 | 0.350 | 0.345 (0.325–0.366) |
| 3 | 0.276 | 0.305 (0.285–0.326) |

Fair: 0.333.

| Strategy against the steady player: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| hoarder | 0.365 | 0.365 (0.345–0.386) |
| quick | 0.594 | 0.600 (0.579–0.621) |
| saffron | 0.641 | 0.640 (0.619–0.661) |
| steady | 0.467 | 0.465 (0.452–0.477) |

Fair: 0.500.
