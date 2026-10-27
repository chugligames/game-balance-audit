# Balance summary: Slide Mini

4320 rows · baseline `baseline` + 3 what-if scenario(s) · player profiles: novice, typical, expert · 30 runs each

## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | off-target | expert | No pushover from level 8 on: mean 10: 1.00, target ≥ 6.00 (missed in 1 of 5 levels) |
| high | off-target | expert | Every level can be solved: mean 9: 0.00, target ≥ 1.00 (missed in 1 of 12 levels) |
| medium | spike | typical (and every other profile) | Positions a full search visits jumps up sharply at levels 5→6 (3222 → 25788), 10→11 (128 → 10344), more than 3× a typical step |
| medium | spike | typical (and every other profile) | Shortest solution (moves) jumps up sharply at levels 5→6 (6.00 → 20.0), 10→11 (1.00 → 11.0), more than 3× a typical step |
| medium | spike | expert (also novice) | Solve rate drops sharply at levels 8→9 (1.00 → 0.00), more than 3× a typical step |
| medium | off-target | typical | A typical player can get through each level: mean 8: 0.03, 9: 0.00, 11: 0.03, target ≥ 0.20 (missed in 3 of 12 levels) |
| low | dips | typical (and every other profile) | Positions a full search visits goes against the expected direction (rise) by more than 15% at levels 6→7 (25788 → 6412), 7→8 (6412 → 2960), 8→9 (2960 → 561), 9→10 (561 → 128) |
| low | dips | typical (and every other profile) | Shortest solution (moves) goes against the expected direction (rise) by more than 15% at levels 6→7 (20.0 → 7.00), 8→10 (8.00 → 1.00) |
| low | dips | typical (and every other profile) | Solve rate goes against the expected direction (fall) by more than 15% at levels 6→7 (0.37 → 0.97), 9→10 (0.00 → 1.00), 11→12 (0.03 → 0.97) |
| low | plateau | typical (and every other profile) | Solve rate barely changes for 5 levels in a row (1 to 5) |

## Baseline by level

Mean per level, with the 10th–90th percentile range in brackets.

### Shortest solution (moves) (`optimal`) · expected to rise

| level | novice | typical | expert |
|---|---|---|---|
| 1 | 2.00 (2.00–2.00) | 2.00 (2.00–2.00) | 2.00 (2.00–2.00) |
| 2 | 3.00 (3.00–3.00) | 3.00 (3.00–3.00) | 3.00 (3.00–3.00) |
| 3 | 4.00 (4.00–4.00) | 4.00 (4.00–4.00) | 4.00 (4.00–4.00) |
| 4 | 5.00 (5.00–5.00) | 5.00 (5.00–5.00) | 5.00 (5.00–5.00) |
| 5 | 6.00 (6.00–6.00) | 6.00 (6.00–6.00) | 6.00 (6.00–6.00) |
| 6 | 20.0 (20.0–20.0) | 20.0 (20.0–20.0) | 20.0 (20.0–20.0) |
| 7 | 7.00 (7.00–7.00) | 7.00 (7.00–7.00) | 7.00 (7.00–7.00) |
| 8 | 8.00 (8.00–8.00) | 8.00 (8.00–8.00) | 8.00 (8.00–8.00) |
| 9 | – | – | – |
| 10 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 11 | 11.0 (11.0–11.0) | 11.0 (11.0–11.0) | 11.0 (11.0–11.0) |
| 12 | 13.0 (13.0–13.0) | 13.0 (13.0–13.0) | 13.0 (13.0–13.0) |

### Positions a full search visits (`explored`) · expected to rise

| level | novice | typical | expert |
|---|---|---|---|
| 1 | 267 (267–267) | 267 (267–267) | 267 (267–267) |
| 2 | 497 (497–497) | 497 (497–497) | 497 (497–497) |
| 3 | 749 (749–749) | 749 (749–749) | 749 (749–749) |
| 4 | 2467 (2467–2467) | 2467 (2467–2467) | 2467 (2467–2467) |
| 5 | 3222 (3222–3222) | 3222 (3222–3222) | 3222 (3222–3222) |
| 6 | 25788 (25788–25788) | 25788 (25788–25788) | 25788 (25788–25788) |
| 7 | 6412 (6412–6412) | 6412 (6412–6412) | 6412 (6412–6412) |
| 8 | 2960 (2960–2960) | 2960 (2960–2960) | 2960 (2960–2960) |
| 9 | 561 (561–561) | 561 (561–561) | 561 (561–561) |
| 10 | 128 (128–128) | 128 (128–128) | 128 (128–128) |
| 11 | 10344 (10344–10344) | 10344 (10344–10344) | 10344 (10344–10344) |
| 12 | 13437 (13437–13437) | 13437 (13437–13437) | 13437 (13437–13437) |

### Solve rate (`solved`) · expected to fall

| level | novice | typical | expert |
|---|---|---|---|
| 1 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 2 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 3 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 4 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 5 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 6 | 0.07 (0.00–0.00) | 0.37 (0.00–1.00) | 1.00 (1.00–1.00) |
| 7 | 0.53 (0.00–1.00) | 0.97 (1.00–1.00) | 1.00 (1.00–1.00) |
| 8 | 0.17 (0.00–1.00) | 0.03 (0.00–0.00) | 1.00 (1.00–1.00) |
| 9 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 10 | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) | 1.00 (1.00–1.00) |
| 11 | 0.03 (0.00–0.00) | 0.03 (0.00–0.00) | 1.00 (1.00–1.00) |
| 12 | 0.27 (0.00–1.00) | 0.97 (1.00–1.00) | 1.00 (1.00–1.00) |

### Moves used when solved (`moves`)

| level | novice | typical | expert |
|---|---|---|---|
| 1 | 3.93 (2.00–8.00) | 12.7 (3.90–20.1) | 2.00 (2.00–2.00) |
| 2 | 5.83 (3.00–9.30) | 12.2 (5.00–21.0) | 3.00 (3.00–3.00) |
| 3 | 13.0 (4.00–21.6) | 11.1 (5.80–22.1) | 4.00 (4.00–4.00) |
| 4 | 17.5 (7.00–28.4) | 15.5 (6.90–23.1) | 5.00 (5.00–5.00) |
| 5 | 30.3 (13.9–49.0) | 20.6 (9.00–30.1) | 6.00 (6.00–6.00) |
| 6 | 6.43 (0.00–0.00) | 53.7 (0.00–174) | 20.0 (20.0–20.0) |
| 7 | 37.0 (0.00–108) | 54.7 (18.0–140) | 7.00 (7.00–7.00) |
| 8 | 8.20 (0.00–36.4) | 0.63 (0.00–0.00) | 8.00 (8.00–8.00) |
| 9 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) |
| 10 | 2.43 (1.00–5.10) | 16.8 (2.00–35.6) | 1.00 (1.00–1.00) |
| 11 | 2.47 (0.00–0.00) | 3.10 (0.00–0.00) | 11.0 (11.0–11.0) |
| 12 | 21.6 (0.00–90.5) | 90.4 (40.9–146) | 13.0 (13.0–13.0) |

## What-ifs against the baseline

### `fix-L9`

- **Fixes:** off-target on `solved` · Every level can be solved (expert); spike on `solved` (expert (also novice)); dips on `solved` (expert)
- **Introduces:** flat (expert): Solve rate falls by only 0.0% from the first third of levels (1.00) to the last third (1.00); the design expects at least 20%
- **Still flagged:** off-target on `optimal` · No pushover from level 8 on (expert); spike on `explored` (typical (and every other profile)); spike on `optimal` (typical (and every other profile)); off-target on `solved` · A typical player can get through each level (typical): clear misses 3 → 2; dips on `explored` (typical (and every other profile)): dips 4 → 3; dips on `optimal` (typical (and every other profile)); plateau on `solved` (typical (and every other profile)); dips on `solved` (typical (also novice))

| Metric | Baseline, typical (first third → last third) | What-if, typical | Change in the mean, by profile |
|---|---|---|---|
| optimal | 3.50 → 8.33 | 3.50 → 8.50 | novice +2% · typical +2% · expert +2% |
| explored | 995 → 6118 | 995 → 6896 | novice +5% · typical +5% · expert +5% |
| solved | 1.00 → 0.50 | 1.00 → 0.75 | novice +8% · typical +12% · expert +9% |
| moves | 12.9 → 27.6 | 12.9 → 45.1 | novice +25% · typical +24% · expert +11% |

### `move-L6-last`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** flat (expert): Solve rate falls by only 0.0% from the first third of levels (1.00) to the last third (1.00); the design expects at least 20%; spike (typical): Solve rate drops sharply at levels 6→7 (0.97 → 0.03), 9→10 (1.00 → 0.03), 11→12 (0.97 → 0.37), more than 3× a typical step
- **Still flagged:** off-target on `optimal` · No pushover from level 8 on (expert); off-target on `solved` · Every level can be solved (expert); spike on `explored` (typical (and every other profile)); spike on `optimal` (typical (and every other profile)); spike on `solved` (expert (also novice)); off-target on `solved` · A typical player can get through each level (typical); dips on `explored` (typical (and every other profile)): dips 4 → 3; dips on `optimal` (typical (and every other profile)): dips 2 → 1; dips on `solved` (typical (and every other profile)): dips 3 → 2; plateau on `solved` (typical (and every other profile))

| Metric | Baseline, typical (first third → last third) | What-if, typical | Change in the mean, by profile |
|---|---|---|---|
| solved | 1.00 → 0.50 | 1.00 → 0.59 | novice +0% · typical +0% · expert +0% |

Unchanged: `optimal`, `explored`, `moves`.

### `replace-L10`

- **Fixes:** off-target on `optimal` · No pushover from level 8 on (expert)
- **Introduces:** no new flags
- **Still flagged:** off-target on `solved` · Every level can be solved (expert); spike on `explored` (typical (and every other profile)); spike on `optimal` (typical (and every other profile)); spike on `solved` (expert (also novice)); off-target on `solved` · A typical player can get through each level (typical); dips on `explored` (typical (and every other profile)): dips 4 → 3; dips on `optimal` (typical (and every other profile)): dips 2 → 1; dips on `solved` (typical (and every other profile)); plateau on `solved` (typical (and every other profile))

| Metric | Baseline, typical (first third → last third) | What-if, typical | Change in the mean, by profile |
|---|---|---|---|
| optimal | 3.50 → 8.33 | 3.50 → 12.0 | novice +14% · typical +14% · expert +14% |
| explored | 995 → 6118 | 995 → 8212 | novice +13% · typical +13% · expert +13% |
| solved | 1.00 → 0.50 | 1.00 → 0.49 | novice −5% · typical −0% · expert +0% |
| moves | 12.9 → 27.6 | 12.9 → 43.4 | novice +24% · typical +22% · expert +14% |
