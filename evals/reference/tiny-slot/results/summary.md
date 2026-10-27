# Balance summary: Ladoo Spin

500 rows · baseline `baseline` + 4 what-if scenario(s) · player profiles: one-coin spins · 100 runs each

## Exact answers against the simulation

Each exact value is computed without sampling (enumeration, or a Markov chain); the simulation should land within its 95% interval of it. A ✗ means the simulator, or its reading of the rules, is wrong.

| Quantity | Exact | Simulated (95% interval) | Samples | Agrees |
|---|---|---|---|---|
| RTP | 1.039352 | 1.037437 ± 0.011454 | 100 | ✓ |
| Hit rate | 0.310185 | 0.310092 ± 0.000977 | 100 | ✓ |
| Big-win rate | 0.002894 | 0.002889 ± 0.000101 | 100 | ✓ |

## Scenarios against the design goals

Each goal is measured per player over the segments it names, then averaged over runs (± is a 95% interval). ▲/▼: better/worse than the baseline beyond noise. ✗: breaks a constraint. Best trade-off: no other scenario that keeps every constraint is at least as good on every goal and better on one. Weighted change: the goals' changes from the baseline, weighted as in audit.json, only to sort the table.

| Scenario | RTP (target 0.96, below 1 so coins drain) (lower is better) | RTP within 0.95–0.97 (0.95–0.97) | Hit rate about 3 in 10 (0.27–0.33) | Weighted change | Best trade-off |
|---|---|---|---|---|---|
| `three MANGO pays 6` | 0.95 ± 0.01 (−8%) ▲ | ✓ 0.95 | ✓ 0.31 | +8% | yes |
| `three MANGO pays 5` | 0.93 ± 0.01 (−10%) ▲ | ✗ 0.93 | ✓ 0.31 | +10% |  |
| `any three sweets pays 1.5` | 0.94 ± 0.01 (−10%) ▲ | ✗ 0.94 | ✓ 0.31 | +10% |  |
| `reel 2: a CHILLI becomes BLANK` | 1.01 ± 0.01 (−3%) ▲ | ✗ 1.01 | ✓ 0.31 | +3% |  |
| `baseline` | 1.04 ± 0.01 | ✗ 1.04 | ✓ 0.31 | +0% |  |


## Flags in the baseline

No flags.

## What-ifs against the baseline

### `reel 2: a CHILLI becomes BLANK`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, one-coin spins | What-if, one-coin spins | Change in the mean, by profile |
|---|---|---|---|
| rtp | 1.04 | 1.01 | one-coin spins −3% |

Unchanged: `hitRate`, `bigRate`.

### `any three sweets pays 1.5`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, one-coin spins | What-if, one-coin spins | Change in the mean, by profile |
|---|---|---|---|
| rtp | 1.04 | 0.94 | one-coin spins −10% |

Unchanged: `hitRate`, `bigRate`.

### `three MANGO pays 5`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, one-coin spins | What-if, one-coin spins | Change in the mean, by profile |
|---|---|---|---|
| rtp | 1.04 | 0.93 | one-coin spins −10% |

Unchanged: `hitRate`, `bigRate`.

### `three MANGO pays 6`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** none

| Metric | Baseline, one-coin spins | What-if, one-coin spins | Change in the mean, by profile |
|---|---|---|---|
| rtp | 1.04 | 0.95 | one-coin spins −8% |

Unchanged: `hitRate`, `bigRate`.
