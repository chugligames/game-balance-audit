# Balance summary: Merge Mini

24000 rows · baseline `baseline` + 7 what-if scenario(s) · player profiles: careless, twice, efficient · 100 runs each

## Scenarios against the design goals

Each goal is measured per player over the segments it names, then averaged over runs (± is a 95% interval). ▲/▼: better/worse than the baseline beyond noise. ✗: breaks a constraint. Best trade-off: no other scenario that keeps every constraint is at least as good on every goal and better on one. Weighted change: the goals' changes from the baseline, weighted as in audit.json, only to sort the table.

| Scenario | Rewarded ads per player, 10 days (higher is better) | Days played (higher is better) | Twice-a-day players who quit (≤ 0.15) | Once-a-day players who quit (≤ 0.25) | Weighted change | Best trade-off |
|---|---|---|---|---|---|---|
| `orders-x1.5 + cap-60` | 1.59 ± 0.22 ▲ | 10.0 ± 0.00 | ✓ 0.01 | ✓ 0.01 | +2000% | yes |
| `orders-x1.5 + cap-60, quit x2` | 1.59 ± 0.22 ▲ | 10.0 ± 0.00 | ✓ 0.01 | ✓ 0.02 | +2000% | yes |
| `orders-x1.5 + cap-60 + ad 30` | 1.49 ± 0.19 ▲ | 10.0 ± 0.00 | ✓ 0.01 | ✓ 0.01 | +1874% |  |
| `orders-x1.5-from-6` | 0.16 ± 0.07 ▲ | 10.0 ± 0.00 | ✓ 0.00 | ✓ 0.00 | +201% |  |
| `baseline` | 0.00 ± 0.00 | 10.0 ± 0.00 | ✓ 0.00 | ✓ 0.00 | +0% |  |
| `smaller-board` | 0.00 ± 0.00 | 10.0 ± 0.00 | ✓ 0.00 | ✓ 0.00 | +0% |  |
| `slower-regen` | 0.00 ± 0.00 | 10.0 ± 0.00 | ✓ 0.00 | ✓ 0.00 | +0% |  |
| `cap-60` | 0.00 ± 0.00 | 10.0 ± 0.00 | ✓ 0.00 | ✓ 0.00 | +0% |  |


## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | off-target | twice | 2–3 ads a day from the second week: mean 8: 0.00, 9: 0.00, 10: 0.00, target ≥ 2.00 (missed in 3 of 3 days) |
| high | off-target | twice | Twice-a-day player uses most of their energy on days 8–10: mean 8: 0.11, 9: 0.16, 10: 0.25, target ≥ 0.60 (missed in 3 of 3 days) |
| high | never-binds | twice (and every other profile) | Fewest empty cells <= 0 never happens in any of the days, so this limit puts no pressure on the player (closest it gets: 30.0) |
| high | off-target | twice | Board feels crowded from day 6: mean 6: 33.4, 7: 33.5, 8: 32.3, 9: 31.4, 10: 30.4, target ≤ 4.00 (missed in 5 of 5 days) |
| high | never-binds | twice (and every other profile) | Times out of energy > 0 never happens in any of the days, so this limit puts no pressure on the player (closest it gets: 0.00) |
| medium | flat | twice (and every other profile) | Rewarded ads watched rises by only 0.0% from the first third of days (0.00) to the last third (0.00); the design expects at least 25% |
| medium | flat | twice (and every other profile) | Fewest empty cells falls by only 7.5% from the first third of days (33.4) to the last third (30.9); the design expects at least 25% |
| low | plateau | twice (and every other profile) | Rewarded ads watched barely changes for 8 days in a row (3 to 10) |
| low | dips | twice (and every other profile) | Share of the day's free energy used goes against the expected direction (rise) by more than 15% at days 5→6 (0.18 → 0.09) |
| low | dips | twice (and every other profile) | Energy spent goes against the expected direction (rise) by more than 15% at days 5→6 (35.4 → 17.9) |

Never changes: `adPrompts` = 0.00; `adsWatched` = 0.00; `daysLate` = 0.00; `outOfEnergy` = 0.00; `played` = 1.00; `quit` = 0.00; `sells` = 0.00

## Baseline by day

Mean per day, with the 10th–90th percentile range in brackets.

### Energy spent (`taps`) · expected to rise

| day | careless | twice | efficient |
|---|---|---|---|
| 1 | 7.52 (6.00–9.00) | 7.27 (6.00–8.00) | 7.12 (6.00–8.00) |
| 2 | 10.6 (9.00–12.0) | 10.8 (10.0–12.0) | 10.8 (9.00–12.0) |
| 3 | 17.8 (16.0–19.0) | 17.8 (16.0–19.0) | 17.8 (16.0–19.0) |
| 4 | 21.2 (19.0–23.1) | 21.3 (20.0–23.0) | 21.1 (19.0–23.0) |
| 5 | 35.2 (32.9–37.1) | 35.4 (33.0–38.0) | 35.4 (33.0–38.0) |
| 6 | 17.9 (16.0–19.1) | 17.9 (16.0–19.1) | 17.8 (16.0–19.0) |
| 7 | 17.5 (15.9–19.0) | 17.7 (16.0–19.0) | 17.8 (16.0–19.0) |
| 8 | 21.3 (20.0–23.0) | 21.4 (19.9–23.0) | 21.5 (20.0–23.0) |
| 9 | 32.0 (30.0–34.0) | 31.9 (29.9–34.0) | 31.7 (30.0–34.0) |
| 10 | 49.2 (46.0–52.0) | 49.6 (47.0–53.0) | 49.8 (47.0–52.1) |

### Share of the day's free energy used (`energyShare`) · expected to rise

| day | careless | twice | efficient |
|---|---|---|---|
| 1 | 0.08 (0.06–0.09) | 0.04 (0.03–0.04) | 0.02 (0.02–0.03) |
| 2 | 0.11 (0.09–0.12) | 0.05 (0.05–0.06) | 0.04 (0.03–0.04) |
| 3 | 0.18 (0.16–0.19) | 0.09 (0.08–0.10) | 0.06 (0.05–0.06) |
| 4 | 0.21 (0.19–0.23) | 0.11 (0.10–0.12) | 0.07 (0.06–0.08) |
| 5 | 0.35 (0.33–0.37) | 0.18 (0.17–0.19) | 0.12 (0.11–0.13) |
| 6 | 0.18 (0.16–0.19) | 0.09 (0.08–0.10) | 0.06 (0.05–0.06) |
| 7 | 0.18 (0.16–0.19) | 0.09 (0.08–0.10) | 0.06 (0.05–0.06) |
| 8 | 0.21 (0.20–0.23) | 0.11 (0.10–0.12) | 0.07 (0.07–0.08) |
| 9 | 0.32 (0.30–0.34) | 0.16 (0.15–0.17) | 0.11 (0.10–0.11) |
| 10 | 0.49 (0.46–0.52) | 0.25 (0.23–0.27) | 0.17 (0.16–0.17) |

### Fewest empty cells (`minFree`) · expected to fall, limit hit when <= 0

| day | careless | twice | efficient |
|---|---|---|---|
| 1 | 36.3 (36.0–37.0) | 36.4 (36.0–38.0) | 36.4 (36.0–38.0) |
| 2 | 35.4 (35.0–36.0) | 35.4 (35.0–36.0) | 35.4 (35.0–37.0) |
| 3 | 33.6 (33.0–34.1) | 33.5 (33.0–35.0) | 33.2 (33.0–34.0) |
| 4 | 33.5 (33.0–35.0) | 33.4 (33.0–35.0) | 33.5 (33.0–35.0) |
| 5 | 31.4 (31.0–33.0) | 31.4 (31.0–32.0) | 31.3 (31.0–32.1) |
| 6 | 33.4 (33.0–35.0) | 33.4 (33.0–34.1) | 33.3 (33.0–34.1) |
| 7 | 33.4 (33.0–34.1) | 33.5 (33.0–35.0) | 33.3 (33.0–34.0) |
| 8 | 32.4 (32.0–33.0) | 32.3 (32.0–34.0) | 32.5 (32.0–34.0) |
| 9 | 31.4 (31.0–32.0) | 31.4 (31.0–32.1) | 31.3 (31.0–33.0) |
| 10 | 30.6 (30.0–32.0) | 30.4 (30.0–32.0) | 30.3 (30.0–31.1) |

### Times out of energy (`outOfEnergy`) · limit hit when > 0

| day | careless | twice | efficient |
|---|---|---|---|
| 1 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 2 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 3 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 4 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 5 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 6 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 7 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 8 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 9 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 10 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |

### Days behind the calendar (`daysLate`)

| day | careless | twice | efficient |
|---|---|---|---|
| 1 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 2 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 3 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 4 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 5 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 6 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 7 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 8 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 9 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 10 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |

### Rewarded ads watched (`adsWatched`) · expected to rise

| day | careless | twice | efficient |
|---|---|---|---|
| 1 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 2 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 3 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 4 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 5 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 6 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 7 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 8 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 9 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 10 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |

## What-ifs against the baseline

### `smaller-board`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** dips (twice (also efficient)): Fewest empty cells goes against the expected direction (fall) by more than 15% at days 5→6 (13.4 → 15.4)
- **Still flagged:** off-target on `adsWatched` · 2–3 ads a day from the second week (twice); off-target on `energyShare` · Twice-a-day player uses most of their energy on days 8–10 (twice); never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` · Board feels crowded from day 6 (twice); never-binds on `outOfEnergy` (twice (and every other profile)); flat on `adsWatched` (twice (and every other profile)); flat on `minFree` (twice (and every other profile)): growth 8% → 16%; plateau on `adsWatched` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| minFree | 33.4 → 30.9 | 15.4 → 12.9 | careless −55% · twice −56% |

Unchanged: `taps`, `energyShare`, `outOfEnergy`, `daysLate`, `adsWatched`.

### `orders-x1.5-from-6`

- **Fixes:** never-binds on `outOfEnergy` (twice (and every other profile)); flat on `adsWatched` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))
- **Introduces:** spike (twice (and every other profile)): Rewarded ads watched jumps up sharply at days 9→10 (0.00 → 0.16), more than 3× a typical step; spike (twice (and every other profile)): Share of the day's free energy used jumps up sharply at days 4→5 (0.11 → 0.18), 8→9 (0.18 → 0.32), 9→10 (0.32 → 0.49), more than 3× a typical step; spike (twice (and every other profile)): Energy spent jumps up sharply at days 4→5 (21.3 → 35.4), 8→9 (35.7 → 63.7), 9→10 (63.7 → 98.7), more than 3× a typical step; plateau (twice): Fewest empty cells barely changes for 4 days in a row (5 to 8)
- **Still flagged:** off-target on `adsWatched` · 2–3 ads a day from the second week (twice); off-target on `energyShare` · Twice-a-day player uses most of their energy on days 8–10 (twice); never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` · Board feels crowded from day 6 (twice); flat on `minFree` (twice (and every other profile)): growth 8% → 13%; plateau on `adsWatched` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| taps | 19.5 → 40.8 | 19.5 → 81.2 | careless +58% · twice +58% |
| energyShare | 0.10 → 0.20 | 0.10 → 0.41 | careless +58% · twice +58% |
| minFree | 33.4 → 30.9 | 33.4 → 29.0 | careless −4% · twice −4% |
| outOfEnergy | 0.00 → 0.00 | 0.00 → 0.13 | careless 0.00 → 0.04 · twice 0.00 → 0.04 |
| daysLate | 0.00 → 0.00 | 0.00 → 0.00 | careless 0.00 → 0.01 · twice 0.00 → 0.00 |
| adsWatched | 0.00 → 0.00 | 0.00 → 0.08 | careless 0.00 → 0.01 · twice 0.00 → 0.02 |

### `slower-regen`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** off-target on `adsWatched` · 2–3 ads a day from the second week (twice); off-target on `energyShare` · Twice-a-day player uses most of their energy on days 8–10 (twice); never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` · Board feels crowded from day 6 (twice); never-binds on `outOfEnergy` (twice (and every other profile)); flat on `adsWatched` (twice (and every other profile)); flat on `minFree` (twice (and every other profile)); plateau on `adsWatched` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))

Unchanged: `taps`, `energyShare`, `minFree`, `outOfEnergy`, `daysLate`, `adsWatched`.

### `cap-60`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** off-target on `adsWatched` · 2–3 ads a day from the second week (twice); off-target on `energyShare` · Twice-a-day player uses most of their energy on days 8–10 (twice); never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` · Board feels crowded from day 6 (twice); never-binds on `outOfEnergy` (twice (and every other profile)); flat on `adsWatched` (twice (and every other profile)); flat on `minFree` (twice (and every other profile)); plateau on `adsWatched` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| energyShare | 0.10 → 0.20 | 0.16 → 0.34 | careless +67% · twice +67% |

Unchanged: `taps`, `minFree`, `outOfEnergy`, `daysLate`, `adsWatched`.

### `orders-x1.5 + cap-60`

- **Fixes:** never-binds on `outOfEnergy` (twice (and every other profile)); flat on `adsWatched` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))
- **Introduces:** spike (twice (and every other profile)): Rewarded ads watched jumps up sharply at days 8→9 (0.00 → 0.56), 9→10 (0.56 → 1.03), more than 3× a typical step; spike (twice (and every other profile)): Share of the day's free energy used jumps up sharply at days 4→5 (0.18 → 0.29), 8→9 (0.30 → 0.53), 9→10 (0.53 → 0.82), more than 3× a typical step; spike (twice (and every other profile)): Energy spent jumps up sharply at days 4→5 (21.3 → 35.4), 8→9 (35.7 → 63.7), 9→10 (63.7 → 98.4), more than 3× a typical step; plateau (twice): Fewest empty cells barely changes for 4 days in a row (5 to 8)
- **Still flagged:** off-target on `adsWatched` · 2–3 ads a day from the second week (twice); off-target on `energyShare` · Twice-a-day player uses most of their energy on days 8–10 (twice): clear misses 3 → 2; never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` · Board feels crowded from day 6 (twice); flat on `minFree` (twice (and every other profile)): growth 8% → 14%; plateau on `adsWatched` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| taps | 19.5 → 40.8 | 19.5 → 81.0 | careless +58% · twice +58% |
| energyShare | 0.10 → 0.20 | 0.16 → 0.68 | careless +163% · twice +163% |
| minFree | 33.4 → 30.9 | 33.4 → 28.9 | careless −4% · twice −4% |
| outOfEnergy | 0.00 → 0.00 | 0.00 → 0.66 | careless 0.00 → 0.35 · twice 0.00 → 0.34 |
| daysLate | 0.00 → 0.00 | 0.00 → 0.00 | careless 0.00 → 0.10 · twice 0.00 → 0.00 |
| adsWatched | 0.00 → 0.00 | 0.00 → 0.80 | careless 0.00 → 0.20 · twice 0.00 → 0.20 |

### `orders-x1.5 + cap-60 + ad 30`

- **Fixes:** never-binds on `outOfEnergy` (twice (and every other profile)); flat on `adsWatched` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))
- **Introduces:** spike (twice (and every other profile)): Rewarded ads watched jumps up sharply at days 8→9 (0.00 → 0.56), 9→10 (0.56 → 0.93), more than 3× a typical step; spike (twice (and every other profile)): Share of the day's free energy used jumps up sharply at days 4→5 (0.18 → 0.29), 8→9 (0.30 → 0.53), 9→10 (0.53 → 0.82), more than 3× a typical step; spike (twice (and every other profile)): Energy spent jumps up sharply at days 4→5 (21.3 → 35.4), 8→9 (35.7 → 63.7), 9→10 (63.7 → 98.3), more than 3× a typical step; plateau (twice): Fewest empty cells barely changes for 4 days in a row (5 to 8)
- **Still flagged:** off-target on `adsWatched` · 2–3 ads a day from the second week (twice); off-target on `energyShare` · Twice-a-day player uses most of their energy on days 8–10 (twice): clear misses 3 → 2; never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` · Board feels crowded from day 6 (twice); flat on `minFree` (twice (and every other profile)): growth 8% → 13%; plateau on `adsWatched` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| taps | 19.5 → 40.8 | 19.5 → 81.0 | careless +58% · twice +58% |
| energyShare | 0.10 → 0.20 | 0.16 → 0.68 | careless +163% · twice +163% |
| minFree | 33.4 → 30.9 | 33.4 → 28.9 | careless −4% · twice −4% |
| outOfEnergy | 0.00 → 0.00 | 0.00 → 0.65 | careless 0.00 → 0.33 · twice 0.00 → 0.34 |
| daysLate | 0.00 → 0.00 | 0.00 → 0.00 | careless 0.00 → 0.10 · twice 0.00 → 0.00 |
| adsWatched | 0.00 → 0.00 | 0.00 → 0.75 | careless 0.00 → 0.19 · twice 0.00 → 0.19 |

### `orders-x1.5 + cap-60, quit x2`

- **Fixes:** never-binds on `outOfEnergy` (twice (and every other profile)); flat on `adsWatched` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))
- **Introduces:** spike (twice (and every other profile)): Rewarded ads watched jumps up sharply at days 8→9 (0.00 → 0.56), 9→10 (0.56 → 1.03), more than 3× a typical step; spike (twice (and every other profile)): Share of the day's free energy used jumps up sharply at days 4→5 (0.18 → 0.29), 8→9 (0.30 → 0.53), 9→10 (0.53 → 0.82), more than 3× a typical step; spike (twice (and every other profile)): Energy spent jumps up sharply at days 4→5 (21.3 → 35.4), 8→9 (35.7 → 63.7), 9→10 (63.7 → 98.4), more than 3× a typical step; plateau (twice): Fewest empty cells barely changes for 4 days in a row (5 to 8)
- **Still flagged:** off-target on `adsWatched` · 2–3 ads a day from the second week (twice); off-target on `energyShare` · Twice-a-day player uses most of their energy on days 8–10 (twice): clear misses 3 → 2; never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` · Board feels crowded from day 6 (twice); flat on `minFree` (twice (and every other profile)): growth 8% → 14%; plateau on `adsWatched` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| taps | 19.5 → 40.8 | 19.5 → 81.0 | careless +58% · twice +58% |
| energyShare | 0.10 → 0.20 | 0.16 → 0.68 | careless +163% · twice +163% |
| minFree | 33.4 → 30.9 | 33.4 → 28.9 | careless −4% · twice −4% |
| outOfEnergy | 0.00 → 0.00 | 0.00 → 0.66 | careless 0.00 → 0.35 · twice 0.00 → 0.34 |
| daysLate | 0.00 → 0.00 | 0.00 → 0.00 | careless 0.00 → 0.10 · twice 0.00 → 0.00 |
| adsWatched | 0.00 → 0.00 | 0.00 → 0.80 | careless 0.00 → 0.20 · twice 0.00 → 0.20 |
