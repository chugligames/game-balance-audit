# Balance summary: Spice Route: Royal Chest

400 rows · baseline `baseline` + 0 what-if scenario(s) · player profiles: one player · 400 runs each

## Exact answers against the simulation

Each exact value is computed without sampling (enumeration, or a Markov chain); the simulation should land within its 95% interval of it. A ✗ means the simulator, or its reading of the rules, is wrong.

| Quantity | Exact | Simulated (95% interval) | Samples | Agrees |
|---|---|---|---|---|
| Mean pulls per legendary | 69.499537 | 69.370454 ± 0.131979 | 400 | ✓ |
| Share of streaks that need pull 91 | 0.000412 | 0.000452 ± 0.000127 | 400 | ✓ |

## Scenarios against the design goals

Each goal is measured per player over the segments it names, then averaged over runs (± is a 95% interval). ▲/▼: better/worse than the baseline beyond noise. ✗: breaks a constraint. Best trade-off: no other scenario that keeps every constraint is at least as good on every goal and better on one. Weighted change: the goals' changes from the baseline, weighted as in audit.json, only to sort the table.

| Scenario | Rates screen: 1.6% overall (62.5 pulls) (61.5–63.5) | Rates screen: guaranteed within 90 pulls (≤ 0.00) | Rates screen: an epic or better within 10 pulls (≤ 10.0) | Weighted change | Best trade-off |
|---|---|---|---|---|---|
| `baseline` | ✗ 69.4 | ✗ 0.00 | ✓ 10.0 | +0% |  |


## Flags in the baseline

No flags.

Never changes: `epicGapMax` = 10.0
