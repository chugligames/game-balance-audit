# Balance summary: Spice Route: Royal Chest

120000 rows · baseline `baseline` + 5 what-if scenario(s) · player profiles: player · 20000 runs each

## Exact answers against the simulation

Each exact value is computed without sampling (enumeration, or a Markov chain); the simulation should land within its 95% interval of it. A ✗ means the simulator, or its reading of the rules, is wrong.

| Quantity | Exact | Simulated (95% interval) | Samples | Agrees |
|---|---|---|---|---|
| Mean pulls (baseline) | 69.499537 | 69.420650 ± 0.317141 | 20000 | ✓ |
| P(>60 pulls) (baseline) | 0.786249 | 0.786050 ± 0.005684 | 20000 | ✓ |
| P(>90 pulls) (baseline) | 0.000412 | 0.000450 ± 0.000294 | 20000 | ✓ |
| Mean pulls (P1-A) | 69.499124 | 69.420200 ± 0.317135 | 20000 | ✓ |
| Mean pulls (P1-B) | 62.128412 | 61.800900 ± 0.373494 | 20000 | ✓ |
| Mean pulls (P2-A) | 59.911500 | 59.645200 ± 0.383322 | 20000 | ✓ |
| Mean pulls (P2-B) | 60.606112 | 60.555850 ± 0.256452 | 20000 | ✓ |
| Mean pulls (P2-C) | 60.892364 | 60.845250 ± 0.257290 | 20000 | ✓ |

## Scenarios against the design goals

Each goal is measured per player over the segments it names, then averaged over runs (± is a 95% interval). ▲/▼: better/worse than the baseline beyond noise. ✗: breaks a constraint. Best trade-off: no other scenario that keeps every constraint is at least as good on every goal and better on one. Weighted change: the goals' changes from the baseline, weighted as in audit.json, only to sort the table.

| Scenario | Mean pulls to legendary (target ~60) (lower is better) | Gems per legendary (revenue) (higher is better) | Share needing >90 pulls (≤ 0.00) | Empty ten-pull (≤ 0.00) | Mean pulls 55-65 (55.0–65.0) | Weighted change | Best trade-off |
|---|---|---|---|---|---|---|---|
| `P1-B base legendary 0.7%` | 61.8 ± 0.37 (−11%) ▲ | 9888 ± 59.8 (−11%) ▼ | ✓ 0.00 | ✓ 0.00 | ✓ 61.8 | −0% | yes |
| `P2-B soft pity from 64` | 60.6 ± 0.26 (−13%) ▲ | 9689 ± 41.0 (−13%) ▼ | ✓ 0.00 | ✓ 0.00 | ✓ 60.6 | −0% | yes |
| `P2-C soft pity from 66 step 10%` | 60.8 ± 0.26 (−12%) ▲ | 9735 ± 41.2 (−12%) ▼ | ✓ 0.00 | ✓ 0.00 | ✓ 60.8 | −0% | yes |
| `P2-A base legendary 0.8%` | 59.6 ± 0.38 (−14%) ▲ | 9543 ± 61.3 (−14%) ▼ | ✓ 0.00 | ✓ 0.00 | ✓ 59.6 | −0% | yes |
| `P1-A hard pity >= 90` | 69.4 ± 0.32 | 11107 ± 50.7 | ✓ 0.00 | ✓ 0.00 | ✗ 69.4 | +0% |  |
| `baseline` | 69.4 ± 0.32 | 11107 ± 50.7 | ✗ 0.00 | ✓ 0.00 | ✗ 69.4 | +0% |  |


## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | off-target | player | Never more than 90 pulls: mean 0.00, target ≤ 0.00 |
| high | off-target | player | Legendary in about 60 pulls on average: mean 69.4, target 55.0–65.0 |

Never changes: `emptyTen` = 0.00

## What-ifs against the baseline

### `P1-A hard pity >= 90`

- **Fixes:** off-target on `over90` · Never more than 90 pulls (player)
- **Introduces:** no new flags
- **Still flagged:** off-target on `pulls` · Legendary in about 60 pulls on average (player)

| Metric | Baseline, player | What-if, player | Change in the mean, by profile |
|---|---|---|---|
| pulls | 69.4 | 69.4 | player −0% |
| over90 | 0.00 | 0.00 | player −100% |

Unchanged: `emptyTen`.

### `P1-B base legendary 0.7%`

- **Fixes:** off-target on `over90` · Never more than 90 pulls (player); off-target on `pulls` · Legendary in about 60 pulls on average (player)
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, player | What-if, player | Change in the mean, by profile |
|---|---|---|---|
| pulls | 69.4 | 61.8 | player −11% |
| over90 | 0.00 | 0.00 | player −100% |

Unchanged: `emptyTen`.

### `P2-A base legendary 0.8%`

- **Fixes:** off-target on `over90` · Never more than 90 pulls (player); off-target on `pulls` · Legendary in about 60 pulls on average (player)
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, player | What-if, player | Change in the mean, by profile |
|---|---|---|---|
| pulls | 69.4 | 59.6 | player −14% |
| over90 | 0.00 | 0.00 | player −100% |

Unchanged: `emptyTen`.

### `P2-B soft pity from 64`

- **Fixes:** off-target on `over90` · Never more than 90 pulls (player); off-target on `pulls` · Legendary in about 60 pulls on average (player)
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, player | What-if, player | Change in the mean, by profile |
|---|---|---|---|
| pulls | 69.4 | 60.6 | player −13% |
| over90 | 0.00 | 0.00 | player −100% |

Unchanged: `emptyTen`.

### `P2-C soft pity from 66 step 10%`

- **Fixes:** off-target on `over90` · Never more than 90 pulls (player); off-target on `pulls` · Legendary in about 60 pulls on average (player)
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, player | What-if, player | Change in the mean, by profile |
|---|---|---|---|
| pulls | 69.4 | 60.8 | player −12% |
| over90 | 0.00 | 0.00 | player −100% |

Unchanged: `emptyTen`.
