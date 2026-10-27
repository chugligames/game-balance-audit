# Balance summary: Match-3 Mini

18000 rows · baseline `baseline` + 3 what-if scenario(s) · player profiles: novice, typical, expert · 100 runs each

## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | off-target | expert | Every level is winnable by a strong player: mean 8: 0.02, target ≥ 0.15 (missed in 1 of 15 levels) |
| high | off-target | typical | Levels 6–9: mean 6: 0.99, 8: 0.00, target 0.55–0.92 (missed in 2 of 4 levels) |
| high | off-target | typical | Hard level 10: mean 10: 1.00, target 0.25–0.40 (missed in 1 of 1 levels) |
| high | off-target | typical | Levels 11–14: mean 14: 0.14, target 0.45–0.85 (missed in 1 of 4 levels) |
| high | off-target | typical | Hard level 15: mean 15: 0.07, target 0.25–0.40 (missed in 1 of 1 levels) |
| medium | flat | expert | Win rate falls by only 29.4% from the first third of levels (0.97) to the last third (0.69); the design expects at least 30% |
| medium | spike | typical (and every other profile) | Win rate drops sharply at levels 7→8 (0.80 → 0.00), more than 3× a typical step |
| medium | front-loaded | novice | Win rate: 93% of the whole change has happened by level 5, the first quarter |
| low | dips | typical (and every other profile) | Win rate goes against the expected direction (fall) by more than 15% at levels 8→9 (0.00 → 0.70), 9→10 (0.70 → 1.00) |
| low | plateau | typical (and every other profile) | Win rate barely changes for 4 levels in a row (1 to 4) |
| low | off-target | typical | Hard level 5: mean borderline (inside sampling noise, run more): 5: 0.47, target 0.25–0.40 (missed in 1 of 1 levels) |

## Baseline by level

Mean per level, with the 10th–90th percentile range in brackets.

### Win rate (`won`) · expected to fall

| level | novice | typical | expert |
|---|---|---|---|
| 1 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 2 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 3 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 4 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 5 | 0.12 (0.00–1.00) | 0.47 (0.00–1.00) | 0.87 (0.00–1.00) |
| 6 | 0.85 (0.00–1.00) | 0.99 (1.00–1.00) | 1.00 (1.00–1.00) |
| 7 | 0.67 (0.00–1.00) | 0.80 (0.00–1.00) | 0.99 (1.00–1.00) |
| 8 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.02 (0.00–0.00) |
| 9 | 0.39 (0.00–1.00) | 0.70 (0.00–1.00) | 0.89 (0.00–1.00) |
| 10 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 11 | 0.56 (0.00–1.00) | 0.84 (0.00–1.00) | 0.93 (1.00–1.00) |
| 12 | 0.49 (0.00–1.00) | 0.78 (0.00–1.00) | 0.96 (1.00–1.00) |
| 13 | 0.34 (0.00–1.00) | 0.50 (0.00–1.00) | 0.88 (0.00–1.00) |
| 14 | 0.04 (0.00–0.00) | 0.14 (0.00–1.00) | 0.36 (0.00–1.00) |
| 15 | 0.05 (0.00–0.00) | 0.07 (0.00–0.00) | 0.31 (0.00–1.00) |

### Moves left at the end (`movesLeft`)

| level | novice | typical | expert |
|---|---|---|---|
| 1 | 12.9 (9.00–16.0) | 14.7 (12.0–17.0) | 16.1 (14.0–18.0) |
| 2 | 12.8 (9.00–16.0) | 14.6 (11.0–17.0) | 16.2 (14.0–18.0) |
| 3 | 12.5 (8.90–16.0) | 14.2 (11.0–17.0) | 15.9 (13.0–18.0) |
| 4 | 12.6 (9.00–16.0) | 13.8 (11.0–17.0) | 16.1 (14.0–18.0) |
| 5 | 0.32 (0.00–0.10) | 1.43 (0.00–4.00) | 3.66 (0.00–7.00) |
| 6 | 5.43 (0.00–12.0) | 8.34 (2.90–13.0) | 10.7 (5.90–16.0) |
| 7 | 2.99 (0.00–8.10) | 4.42 (0.00–10.0) | 8.48 (3.00–13.0) |
| 8 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.04 (0.00–0.00) |
| 9 | 1.27 (0.00–5.00) | 2.65 (0.00–7.10) | 5.28 (0.00–10.0) |
| 10 | 9.61 (5.00–14.0) | 12.0 (8.00–16.0) | 13.9 (10.0–17.0) |
| 11 | 2.62 (0.00–8.00) | 5.44 (0.00–10.0) | 8.24 (1.90–13.1) |
| 12 | 1.99 (0.00–6.00) | 3.08 (0.00–8.00) | 7.14 (2.00–12.0) |
| 13 | 1.46 (0.00–5.00) | 1.79 (0.00–6.00) | 5.29 (0.00–10.1) |
| 14 | 0.14 (0.00–0.00) | 0.45 (0.00–0.10) | 1.14 (0.00–4.10) |
| 15 | 0.09 (0.00–0.00) | 0.11 (0.00–0.00) | 0.87 (0.00–4.00) |

### Share of the goal done (`goalDone`)

| level | novice | typical | expert |
|---|---|---|---|
| 1 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 2 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 3 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 4 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 5 | 0.83 (0.68–1.00) | 0.93 (0.82–1.00) | 0.99 (0.98–1.00) |
| 6 | 0.97 (0.89–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 7 | 0.95 (0.84–1.00) | 0.98 (0.94–1.00) | 1.00 (1.00–1.00) |
| 8 | 0.51 (0.33–0.70) | 0.59 (0.45–0.74) | 0.70 (0.52–0.87) |
| 9 | 0.84 (0.54–1.00) | 0.95 (0.79–1.00) | 0.98 (0.95–1.00) |
| 10 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 11 | 0.94 (0.82–1.00) | 0.98 (0.94–1.00) | 0.99 (1.00–1.00) |
| 12 | 0.94 (0.82–1.00) | 0.98 (0.89–1.00) | 1.00 (1.00–1.00) |
| 13 | 0.90 (0.79–1.00) | 0.94 (0.79–1.00) | 0.99 (0.97–1.00) |
| 14 | 0.70 (0.41–0.95) | 0.73 (0.41–1.00) | 0.85 (0.68–1.00) |
| 15 | 0.74 (0.57–0.95) | 0.80 (0.62–0.95) | 0.91 (0.75–1.00) |

## What-ifs against the baseline

### `L8-easier`

- **Fixes:** off-target on `won` · Every level is winnable by a strong player (expert); dips on `won` (expert)
- **Introduces:** no new flags
- **Still flagged:** off-target on `won` · Levels 6–9 (typical): clear misses 2 → 1; off-target on `won` · Hard level 10 (typical); off-target on `won` · Levels 11–14 (typical); off-target on `won` · Hard level 15 (typical); flat on `won` (expert); spike on `won` (typical (and every other profile)): jumps 1 → 2; front-loaded on `won` (novice); plateau on `won` (typical (and every other profile)); dips on `won` (typical (also novice)): dips 2 → 1; off-target on `won` · Hard level 5 (typical)

| Metric | Baseline, typical (first third → last third) | What-if, typical | Change in the mean, by profile |
|---|---|---|---|
| won | 0.89 → 0.47 | 0.89 → 0.47 | novice +5% · typical +7% · expert +8% |
| movesLeft | 11.7 → 2.17 | 11.7 → 2.17 | novice +2% · typical +4% · expert +6% |
| goalDone | 0.99 → 0.89 | 0.99 → 0.89 | novice +3% · typical +3% · expert +2% |

### `L10-hard`

- **Fixes:** spike on `won` (typical)
- **Introduces:** no new flags
- **Still flagged:** off-target on `won` · Every level is winnable by a strong player (expert); off-target on `won` · Levels 6–9 (typical); off-target on `won` · Hard level 10 (typical); off-target on `won` · Levels 11–14 (typical); off-target on `won` · Hard level 15 (typical); flat on `won` (expert); spike on `won` (expert (also novice)): jumps 2 → 3; front-loaded on `won` (novice); dips on `won` (typical (and every other profile)): dips 2 → 1; plateau on `won` (typical (and every other profile)); off-target on `won` · Hard level 5 (typical)

| Metric | Baseline, typical (first third → last third) | What-if, typical | Change in the mean, by profile |
|---|---|---|---|
| won | 0.89 → 0.47 | 0.89 → 0.47 | novice −12% · typical −9% · expert −7% |
| movesLeft | 11.7 → 2.17 | 11.7 → 2.17 | novice −13% · typical −12% · expert −11% |
| goalDone | 0.99 → 0.89 | 0.99 → 0.89 | novice −2% · typical −2% · expert −1% |

### `L2-4-varied`

- **Fixes:** plateau on `won` (novice)
- **Introduces:** no new flags
- **Still flagged:** off-target on `won` · Every level is winnable by a strong player (expert); off-target on `won` · Levels 6–9 (typical); off-target on `won` · Hard level 10 (typical); off-target on `won` · Levels 11–14 (typical); off-target on `won` · Hard level 15 (typical); flat on `won` (expert); spike on `won` (typical (and every other profile)); front-loaded on `won` (novice); dips on `won` (typical (and every other profile)); plateau on `won` (typical (also expert)); off-target on `won` · Hard level 5 (typical)

| Metric | Baseline, typical (first third → last third) | What-if, typical | Change in the mean, by profile |
|---|---|---|---|
| won | 0.89 → 0.47 | 0.89 → 0.47 | novice −1% · typical −0% · expert +0% |
| movesLeft | 11.7 → 2.17 | 10.5 → 2.17 | novice −10% · typical −6% · expert −5% |
| goalDone | 0.99 → 0.89 | 0.99 → 0.89 | novice −0% · typical −0% · expert +0% |
