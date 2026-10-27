# Balance summary: Merge Mini

12000 rows · baseline `baseline` + 3 what-if scenario(s) · player profiles: careless, twice, efficient · 100 runs each

## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | off-target | twice | Twice-a-day player uses most of their energy on days 8–10 (mean) misses the target ≥ 0.60 in 3 of 3 days: 8: 0.11, 9: 0.16, 10: 0.25 |
| high | never-binds | twice (and every other profile) | Fewest empty cells <= 0 never happens in any of the days, so this limit puts no pressure on the player (closest it gets: 30.0) |
| high | off-target | twice | Board feels crowded from day 6 (mean) misses the target ≤ 4.00 in 5 of 5 days: 6: 33.4, 7: 33.5, 8: 32.3, 9: 31.4, 10: 30.4 |
| high | never-binds | twice (and every other profile) | Times out of energy > 0 never happens in any of the days, so this limit puts no pressure on the player (closest it gets: 0.00) |
| medium | flat | twice (and every other profile) | Fewest empty cells falls by only 8% from the first third of days (33.4) to the last third (30.9); the design expects at least 25% |
| low | dips | twice (and every other profile) | Share of the day's free energy used goes the wrong way by more than 15% between days 5→6 −49% |
| low | dips | twice (and every other profile) | Energy spent goes the wrong way by more than 15% between days 5→6 −49% |

Never changes: `daysLate` = 0.00; `outOfEnergy` = 0.00; `sells` = 0.00

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

## What-ifs against the baseline

### `smaller-board`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** dips (twice (also efficient)): Fewest empty cells goes the wrong way by more than 15% between days 5→6 −15%
- **Still flagged:** off-target on `energyShare` (twice); never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` (twice); never-binds on `outOfEnergy` (twice (and every other profile)); flat on `minFree` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| minFree | 33.4 → 30.9 | 15.4 → 12.9 | careless −55% · twice −56% · efficient −56% |

Unchanged: `taps`, `energyShare`, `outOfEnergy`, `daysLate`.

### `orders-x1.5-from-6`

- **Fixes:** never-binds on `outOfEnergy` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))
- **Introduces:** spike (twice (and every other profile)): Share of the day's free energy used jumps sharply between days 4→5 +66%, 8→9 +79%, 9→10 +55% (more than 3× a typical step); spike (twice (and every other profile)): Energy spent jumps sharply between days 4→5 +66%, 8→9 +79%, 9→10 +55% (more than 3× a typical step); plateau (twice): Fewest empty cells barely changes for 4 days in a row (5 to 8)
- **Still flagged:** off-target on `energyShare` (twice); never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` (twice); flat on `minFree` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| taps | 19.5 → 40.8 | 19.5 → 81.2 | careless +58% · twice +58% · efficient +58% |
| energyShare | 0.10 → 0.20 | 0.10 → 0.41 | careless +58% · twice +58% · efficient +58% |
| minFree | 33.4 → 30.9 | 33.4 → 28.9 | careless −4% · twice −4% · efficient −4% |
| outOfEnergy | 0.00 → 0.00 | 0.00 → 0.29 | careless 0.00 → 0.08 · twice 0.00 → 0.10 · efficient 0.00 → 0.11 |
| daysLate | 0.00 → 0.00 | 0.00 → 0.00 | careless 0.00 → 0.02 · twice 0.00 → 0.00 · efficient 0.00 → 0.00 |

### `slower-regen`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** no new flags
- **Still flagged:** off-target on `energyShare` (twice); never-binds on `minFree` (twice (and every other profile)); off-target on `minFree` (twice); never-binds on `outOfEnergy` (twice (and every other profile)); flat on `minFree` (twice (and every other profile)); dips on `energyShare` (twice (and every other profile)); dips on `taps` (twice (and every other profile))

| Metric | Baseline, twice (first third → last third) | What-if, twice | Change in the mean, by profile |
|---|---|---|---|
| energyShare | 0.10 → 0.20 | 0.10 → 0.20 | careless +0% · twice +0% · efficient +9% |

Unchanged: `taps`, `minFree`, `outOfEnergy`, `daysLate`.
