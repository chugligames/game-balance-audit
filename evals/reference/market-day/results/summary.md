# Balance summary: Market Day

110000 rows · baseline `baseline` + 4 what-if scenario(s) · player profiles: mirror-2p, mirror-3p, saffron-vs-steady, hoarder-vs-steady, quick-vs-steady · 2000 runs each

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
- **Introduces:** uneven (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): Strategy against the steady player: strategy = steady has 0.445 (95% CI 0.433–0.458, n=6000) against a fair 0.500 ± 0.050
- **Still flagged:** uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p): value 0.530 → 0.548; uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p): value 0.470 → 0.452; uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p): value 0.374 → 0.398; uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p): value 0.276 → 0.271; uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.379; uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.594 → 0.650; uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.641 → 0.635; off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p)

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 46.3 | mirror-2p −6% · mirror-3p −5% · saffron-vs-steady −7% · hoarder-vs-steady −5% · quick-vs-steady −7% |
| turns | 28.9 | 28.9 | mirror-2p +0% · mirror-3p −0% · saffron-vs-steady +0% · hoarder-vs-steady +0% · quick-vs-steady +0% |
| halfLeaderWon | 0.83 | 0.86 | mirror-2p +3% · mirror-3p +1% · saffron-vs-steady +0% · hoarder-vs-steady +1% · quick-vs-steady +0% |

### `equal-turns`

- **Fixes:** uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p)
- **Introduces:** no new flags
- **Still flagged:** uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.362; uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.641 → 0.638; off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p): value 0.530 → 0.523; uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p): value 0.470 → 0.477; uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p): value 0.276 → 0.288; uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.594 → 0.596

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 49.7 | mirror-2p +1% · mirror-3p +1% · saffron-vs-steady +1% · hoarder-vs-steady +1% · quick-vs-steady +0% |
| turns | 28.9 | 29.1 | mirror-2p +1% · mirror-3p +2% · saffron-vs-steady +1% · hoarder-vs-steady +1% · quick-vs-steady +1% |
| halfLeaderWon | 0.83 | 0.84 | mirror-2p +0% · mirror-3p −2% · saffron-vs-steady −0% · hoarder-vs-steady −0% · quick-vs-steady −0% |

### `big-sale-+3-coins`

- **Fixes:** nothing flagged in the baseline
- **Introduces:** uneven (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): Strategy against the steady player: strategy = steady has 0.442 (95% CI 0.430–0.455, n=6000) against a fair 0.500 ± 0.050
- **Still flagged:** uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady); off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p); uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p); uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p); uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.438; uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady)

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 49.4 | mirror-2p +0% · mirror-3p +0% · saffron-vs-steady +0% · hoarder-vs-steady +16% · quick-vs-steady +0% |
| turns | 28.9 | 28.9 | mirror-2p +0% · mirror-3p +0% · saffron-vs-steady +0% · hoarder-vs-steady +1% · quick-vs-steady +0% |
| halfLeaderWon | 0.83 | 0.83 | mirror-2p +0% · mirror-3p +0% · saffron-vs-steady +0% · hoarder-vs-steady −0% · quick-vs-steady +0% |

### `second-seat-+2`

- **Fixes:** uneven on `won` · Seat advantage, 2 players · seat=1 (mirror-2p); uneven on `won` · Seat advantage, 2 players · seat=2 (mirror-2p); uneven on `won` · Seat advantage, 3 players · seat=1 (mirror-3p)
- **Introduces:** uneven (mirror-3p): Seat advantage, 3 players: seat = 2 has 0.389 (95% CI 0.368–0.410, n=2000) against a fair 0.333 ± 0.030
- **Still flagged:** uneven on `won` · Seat advantage, 3 players · seat=3 (mirror-3p): value 0.276 → 0.258; uneven on `won` · Strategy against the steady player · strategy=hoarder (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.365 → 0.366; uneven on `won` · Strategy against the steady player · strategy=saffron (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.641 → 0.634; off-target on `halfLeaderWon` · Comebacks stay possible (mirror-2p); uneven on `won` · Strategy against the steady player · strategy=quick (saffron-vs-steady, hoarder-vs-steady, quick-vs-steady): value 0.594 → 0.595

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| coins | 49.4 | 50.4 | mirror-2p +2% · mirror-3p +2% · saffron-vs-steady +2% · hoarder-vs-steady +2% · quick-vs-steady +2% |
| halfLeaderWon | 0.83 | 0.84 | mirror-2p +1% · mirror-3p −1% · saffron-vs-steady −0% · hoarder-vs-steady +1% · quick-vs-steady −0% |

Unchanged: `turns`.
