# Balance summary: Market Day

174000 rows · baseline `baseline` + 7 what-if scenario(s) · player profiles: mirror-2p, mirror-3p, mirror-4p, mirror-quick-2p, mirror-expert-2p, quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p, all-4p, expert-vs-steady-2p, expert-vs-careless-2p · 1000 runs each

## Exact answers against the simulation

Each exact value is computed without sampling (enumeration, or a Markov chain); the simulation should land within its 95% interval of it. A ✗ means the simulator, or its reading of the rules, is wrong.

| Quantity | Exact | Simulated (95% interval) | Samples | Agrees |
|---|---|---|---|---|
| Takes per game, 2p (deck 43 + the final take) | 44.000000 | 44.000000 ± 0.000000 | 2000 | ✓ |
| Takes per game, 3p (deck 40 + 1) | 41.000000 | 41.000000 ± 0.000000 | 3000 | ✓ |
| Takes per game, 4p (deck 37 + 1) | 38.000000 | 38.000000 ± 0.000000 | 4000 | ✓ |

## Scenarios against the design goals

Each goal is measured per player over the segments it names, then averaged over runs (± is a 95% interval). ▲/▼: better/worse than the baseline beyond noise. ✗: breaks a constraint. Best trade-off: no other scenario that keeps every constraint is at least as good on every goal and better on one. Weighted change: the goals' changes from the baseline, weighted as in audit.json, only to sort the table.

| Scenario | Seat 1 win rate, 2p (fair 0.50) (lower is better) | Seat 1 win rate, 3p (fair 0.33) (lower is better) | Seat 1 win rate, 4p (fair 0.25) (lower is better) | Seat 1 win rate, expert mirror 2p (lower is better) | Expert win rate vs steady (higher is better) | Winning gap in coins, 2p (lower is better) | Seat 1 2p within 0.45-0.55 (0.45–0.55) | Seat 1 4p within 0.20-0.30 (0.20–0.30) | Last seat 4p within 0.20-0.30 (0.20–0.30) | Weighted change | Best trade-off |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `P1-a start coins 0/3 at 2p 0/2/4 at 3p 0/2/4/6 at 4p` | 0.48 ± 0.03 (−18%) ▲ | 0.36 ± 0.03 (−21%) ▲ | 0.23 ± 0.03 (−34%) ▲ | – | – | 11.0 ± 0.39 (−2%) | ✓ 0.48 | ✓ 0.23 | ✓ 0.26 | +75% | yes |
| `PICKS P1-a + P2-b` | 0.48 ± 0.03 (−18%) ▲ | 0.36 ± 0.03 (−21%) ▲ | 0.23 ± 0.03 (−34%) ▲ | – | – | 11.0 ± 0.39 (−2%) | ✓ 0.48 | ✓ 0.23 | ✓ 0.26 | +75% | yes |
| `P1-c later seats start with extra cards 0/1/1/2` | 0.44 ± 0.03 (−25%) ▲ | 0.29 ± 0.03 (−36%) ▲ | 0.22 ± 0.03 (−38%) ▲ | – | – | 11.5 ± 0.40 (+3%) | ✗ 0.44 | ✓ 0.22 | ✓ 0.28 | +97% |  |
| `P1-b finish the round so all have equal turns` | 0.58 ± 0.03 (−2%) | 0.44 ± 0.03 (−2%) | 0.34 ± 0.03 (−4%) | – | – | 11.1 ± 0.40 (−1%) | ✗ 0.58 | ✗ 0.34 | ✗ 0.17 | +10% |  |
| `baseline` | 0.59 ± 0.03 | 0.45 ± 0.03 | 0.35 ± 0.03 | 0.58 ± 0.03 | 0.62 ± 0.03 | 11.2 ± 0.40 | ✗ 0.59 | ✗ 0.35 | ✗ 0.16 | +0% |  |
| `P2-a big sale gives +3 coins not an extra turn` | 0.59 ± 0.03 | 0.45 ± 0.03 | 0.35 ± 0.03 | – | – | 11.2 ± 0.40 | ✗ 0.59 | ✗ 0.35 | ✗ 0.16 | +0% |  |
| `P2-b big sale needs 5 cards` | 0.59 ± 0.03 | 0.45 ± 0.03 | 0.35 ± 0.03 | – | – | 11.2 ± 0.40 | ✗ 0.59 | ✗ 0.35 | ✗ 0.16 | +0% |  |
| `P2-c hand limit 6` | 0.64 ± 0.03 (+8%) | 0.48 ± 0.03 (+6%) | 0.40 ± 0.03 (+13%) | – | – | 11.2 ± 0.40 | ✗ 0.64 | ✗ 0.40 | ✗ 0.13 | −27% |  |


## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | uneven | mirror-2p | Seat advantage, 2p (steady bots): seat = seat 1 has 0.591 (95% CI 0.561–0.621, n=1000) against a fair 0.500 ± 0.030 |
| high | uneven | mirror-2p | Seat advantage, 2p (steady bots): seat = seat 2 has 0.409 (95% CI 0.379–0.439, n=1000) against a fair 0.500 ± 0.030 |
| high | uneven | mirror-3p | Seat advantage, 3p (steady bots): seat = seat 1 has 0.453 (95% CI 0.422–0.483, n=1000) against a fair 0.333 ± 0.030 |
| high | uneven | mirror-3p | Seat advantage, 3p (steady bots): seat = seat 3 has 0.226 (95% CI 0.200–0.251, n=1000) against a fair 0.333 ± 0.030 |
| high | uneven | mirror-4p | Seat advantage, 4p (steady bots): seat = seat 1 has 0.352 (95% CI 0.324–0.381, n=1000) against a fair 0.250 ± 0.030 |
| high | uneven | mirror-4p | Seat advantage, 4p (steady bots): seat = seat 4 has 0.160 (95% CI 0.137–0.182, n=1000) against a fair 0.250 ± 0.030 |
| high | uneven | mirror-expert-2p | Seat advantage, 2p (expert bots): seat = seat 1 has 0.581 (95% CI 0.550–0.611, n=1000) against a fair 0.500 ± 0.030 |
| high | uneven | mirror-expert-2p | Seat advantage, 2p (expert bots): seat = seat 2 has 0.419 (95% CI 0.389–0.450, n=1000) against a fair 0.500 ± 0.030 |
| medium | rarely-used | mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p) | Big sales (> 0) happens in only none of games: an option or reward players almost never use |
| medium | uneven | mirror-4p | Seat advantage, 4p (steady bots): seat = seat 3 has 0.219 (95% CI 0.194–0.244, n=1000) against a fair 0.250 ± 0.030 |
| medium | uneven | quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p | Each strategy head-to-head against steady, 2p: strategy = bigsale has 0.588 (95% CI 0.557–0.618, n=1000) against a fair 0.500 ± 0.050 |

Never changes: `bigSales` = 0.00 (mirror-2p); `bigSales` = 0.00 (mirror-3p); `bigSales` = 0.00 (mirror-4p); `bigSales` = 0.00 (mirror-quick-2p); `bigSales` = 0.00 (quick-vs-steady-2p); `game` = 1.00; `players` = 4.00 (all-4p); `players` = 2.00 (bigsale-vs-steady-2p); `players` = 2.00 (expert-vs-careless-2p); `players` = 2.00 (expert-vs-steady-2p); `players` = 2.00 (luxury-vs-steady-2p); `players` = 2.00 (mirror-2p); `players` = 3.00 (mirror-3p); `players` = 4.00 (mirror-4p); `players` = 2.00 (mirror-expert-2p); `players` = 2.00 (mirror-quick-2p); `players` = 2.00 (quick-vs-steady-2p); `takesTotal` = 38.0 (all-4p); `takesTotal` = 44.0 (bigsale-vs-steady-2p); `takesTotal` = 44.0 (expert-vs-careless-2p); `takesTotal` = 44.0 (expert-vs-steady-2p); `takesTotal` = 44.0 (luxury-vs-steady-2p); `takesTotal` = 44.0 (mirror-2p); `takesTotal` = 41.0 (mirror-3p); `takesTotal` = 38.0 (mirror-4p); `takesTotal` = 44.0 (mirror-expert-2p); `takesTotal` = 44.0 (mirror-quick-2p); `takesTotal` = 44.0 (quick-vs-steady-2p)

## Seat advantage, 2p (steady bots)

| seat | won | 95% CI | n |
|---|---|---|---|
| seat 1 | 0.591 | 0.561–0.621 | 1000 |
| seat 2 | 0.409 | 0.379–0.439 | 1000 |

Fair value: 0.500 ± 0.030.

## Seat advantage, 3p (steady bots)

| seat | won | 95% CI | n |
|---|---|---|---|
| seat 1 | 0.453 | 0.422–0.483 | 1000 |
| seat 2 | 0.322 | 0.294–0.350 | 1000 |
| seat 3 | 0.226 | 0.200–0.251 | 1000 |

Fair value: 0.333 ± 0.030.

## Seat advantage, 4p (steady bots)

| seat | won | 95% CI | n |
|---|---|---|---|
| seat 1 | 0.352 | 0.324–0.381 | 1000 |
| seat 2 | 0.269 | 0.242–0.296 | 1000 |
| seat 3 | 0.219 | 0.194–0.244 | 1000 |
| seat 4 | 0.160 | 0.137–0.182 | 1000 |

Fair value: 0.250 ± 0.030.

## Seat advantage, 2p (expert bots)

| seat | won | 95% CI | n |
|---|---|---|---|
| seat 1 | 0.581 | 0.550–0.611 | 1000 |
| seat 2 | 0.419 | 0.389–0.450 | 1000 |

Fair value: 0.500 ± 0.030.

## Each strategy head-to-head against steady, 2p

| strategy | won | 95% CI | n |
|---|---|---|---|
| bigsale | 0.588 | 0.557–0.618 | 1000 |
| luxury | 0.470 | 0.439–0.501 | 1000 |
| quick | 0.538 | 0.508–0.569 | 1000 |
| steady | 0.468 | 0.450–0.486 | 3000 |

Fair value: 0.500 ± 0.050.

## Four strategies at one 4p table

| strategy | won | 95% CI | n |
|---|---|---|---|
| bigsale | 0.221 | 0.196–0.247 | 1000 |
| luxury | 0.251 | 0.224–0.278 | 1000 |
| quick | 0.270 | 0.243–0.298 | 1000 |
| steady | 0.257 | 0.231–0.284 | 1000 |

Fair value: 0.250 ± 0.040.

## What-ifs against the baseline

### `P1-a start coins 0/3 at 2p 0/2/4 at 3p 0/2/4/6 at 4p`

- **Fixes:** uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 1 (mirror-2p); uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 2 (mirror-2p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 1 (mirror-3p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 3 (mirror-3p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 1 (mirror-4p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 4 (mirror-4p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 1 (mirror-expert-2p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 2 (mirror-expert-2p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 3 (mirror-4p)
- **Introduces:** uneven (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): Each strategy head-to-head against steady, 2p: strategy = quick has 0.550 (95% CI 0.520–0.580, n=1000) against a fair 0.500 ± 0.050
- **Still flagged:** rarely-used on `bigSales` (mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p)); uneven on `won` · Each strategy head-to-head against steady, 2p · strategy=bigsale (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): value 0.588 → 0.587

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| score | 53.9 | 55.4 | mirror-2p +3% · mirror-3p +6% · mirror-4p +12% · all-4p +12% |
| winGap | 11.2 | 11.0 | mirror-2p −2% · mirror-3p −4% · mirror-4p −3% · all-4p −5% |
| tie | 0.05 | 0.04 | mirror-2p −15% · mirror-3p +18% · mirror-4p −20% · all-4p +13% |

Unchanged: `won`, `bigSales`, `saffronSold`, `cardsWasted`.

| Seat advantage, 2p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.591 | 0.484 (0.454–0.515) |
| seat 2 | 0.409 | 0.515 (0.485–0.546) |

Fair: 0.500.

| Seat advantage, 3p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.453 | 0.357 (0.328–0.387) |
| seat 2 | 0.322 | 0.331 (0.302–0.360) |
| seat 3 | 0.226 | 0.311 (0.283–0.340) |

Fair: 0.333.

| Seat advantage, 4p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.352 | 0.231 (0.206–0.257) |
| seat 2 | 0.269 | 0.247 (0.221–0.273) |
| seat 3 | 0.219 | 0.265 (0.238–0.292) |
| seat 4 | 0.160 | 0.257 (0.230–0.284) |

Fair: 0.250.

| Each strategy head-to-head against steady, 2p: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.588 | 0.587 (0.557–0.617) |
| luxury | 0.470 | 0.476 (0.446–0.507) |
| quick | 0.538 | 0.550 (0.520–0.580) |
| steady | 0.468 | 0.462 (0.445–0.480) |

Fair: 0.500.

| Four strategies at one 4p table: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.221 | 0.232 (0.206–0.258) |
| luxury | 0.251 | 0.263 (0.237–0.290) |
| quick | 0.270 | 0.261 (0.234–0.288) |
| steady | 0.257 | 0.244 (0.218–0.270) |

Fair: 0.250.

### `P1-b finish the round so all have equal turns`

- **Fixes:** uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 1 (mirror-expert-2p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 2 (mirror-expert-2p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 3 (mirror-4p)
- **Introduces:** no new flags
- **Still flagged:** uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 1 (mirror-2p): value 0.591 → 0.582; uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 2 (mirror-2p): value 0.409 → 0.418; uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 1 (mirror-3p): value 0.453 → 0.442; uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 3 (mirror-3p): value 0.226 → 0.238; uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 1 (mirror-4p): value 0.352 → 0.337; uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 4 (mirror-4p): value 0.160 → 0.172; rarely-used on `bigSales` (mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p)); uneven on `won` · Each strategy head-to-head against steady, 2p · strategy=bigsale (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): value 0.588 → 0.588

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| score | 53.9 | 54.1 | mirror-2p +0% · mirror-3p +1% · mirror-4p +2% · all-4p +1% |
| winGap | 11.2 | 11.1 | mirror-2p −1% · mirror-3p +0% · mirror-4p −2% · all-4p −2% |
| saffronSold | 2.57 | 2.60 | mirror-2p +1% · mirror-3p +2% · mirror-4p +4% · all-4p +2% |
| cardsWasted | 2.02 | 1.96 | mirror-2p −3% · mirror-3p +1% · mirror-4p +3% · all-4p +1% |
| tie | 0.05 | 0.05 | mirror-2p +15% · mirror-3p +0% · mirror-4p +2% · all-4p +2% |

Unchanged: `won`, `bigSales`.

| Seat advantage, 2p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.591 | 0.582 (0.552–0.611) |
| seat 2 | 0.409 | 0.418 (0.389–0.448) |

Fair: 0.500.

| Seat advantage, 3p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.453 | 0.442 (0.412–0.472) |
| seat 2 | 0.322 | 0.320 (0.291–0.348) |
| seat 3 | 0.226 | 0.238 (0.212–0.264) |

Fair: 0.333.

| Seat advantage, 4p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.352 | 0.337 (0.309–0.366) |
| seat 2 | 0.269 | 0.268 (0.241–0.294) |
| seat 3 | 0.219 | 0.223 (0.198–0.248) |
| seat 4 | 0.160 | 0.172 (0.149–0.195) |

Fair: 0.250.

| Each strategy head-to-head against steady, 2p: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.588 | 0.588 (0.558–0.618) |
| luxury | 0.470 | 0.468 (0.437–0.499) |
| quick | 0.538 | 0.544 (0.514–0.575) |
| steady | 0.468 | 0.467 (0.449–0.484) |

Fair: 0.500.

| Four strategies at one 4p table: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.221 | 0.220 (0.195–0.245) |
| luxury | 0.251 | 0.255 (0.228–0.282) |
| quick | 0.270 | 0.271 (0.244–0.299) |
| steady | 0.257 | 0.254 (0.227–0.280) |

Fair: 0.250.

### `P1-c later seats start with extra cards 0/1/1/2`

- **Fixes:** uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 3 (mirror-3p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 1 (mirror-expert-2p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 2 (mirror-expert-2p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 3 (mirror-4p)
- **Introduces:** uneven (mirror-3p): Seat advantage, 3p (steady bots): seat = seat 2 has 0.407 (95% CI 0.378–0.437, n=1000) against a fair 0.333 ± 0.030
- **Still flagged:** rarely-used on `bigSales` (mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p)): rate 0% → 0%; uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 1 (mirror-2p): over-corrected: value 0.591 → 0.442; uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 2 (mirror-2p): over-corrected: value 0.409 → 0.558; uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 1 (mirror-3p): over-corrected: value 0.453 → 0.288; uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 1 (mirror-4p): over-corrected: value 0.352 → 0.219; uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 4 (mirror-4p): over-corrected: value 0.160 → 0.281; uneven on `won` · Each strategy head-to-head against steady, 2p · strategy=bigsale (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): value 0.588 → 0.562

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| score | 53.9 | 54.0 | mirror-2p +0% · mirror-3p +0% · mirror-4p +1% · all-4p −0% |
| winGap | 11.2 | 11.5 | mirror-2p +3% · mirror-3p −2% · mirror-4p −4% · all-4p +2% |
| bigSales | 0.00 | 0.00 | mirror-2p 0.00 → 0.00 · mirror-3p 0.00 → 0.01 · mirror-4p 0.00 → 0.02 · all-4p +15% |
| saffronSold | 2.57 | 2.56 | mirror-2p −1% · mirror-3p +1% · mirror-4p +4% · all-4p −1% |
| cardsWasted | 2.02 | 1.97 | mirror-2p −2% · mirror-3p −0% · mirror-4p −5% · all-4p −0% |
| tie | 0.05 | 0.03 | mirror-2p −41% · mirror-3p +29% · mirror-4p −14% · all-4p −4% |

Unchanged: `won`.

| Seat advantage, 2p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.591 | 0.442 (0.411–0.472) |
| seat 2 | 0.409 | 0.558 (0.528–0.589) |

Fair: 0.500.

| Seat advantage, 3p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.453 | 0.288 (0.261–0.316) |
| seat 2 | 0.322 | 0.407 (0.378–0.437) |
| seat 3 | 0.226 | 0.304 (0.276–0.332) |

Fair: 0.333.

| Seat advantage, 4p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.352 | 0.219 (0.194–0.244) |
| seat 2 | 0.269 | 0.268 (0.241–0.295) |
| seat 3 | 0.219 | 0.232 (0.206–0.257) |
| seat 4 | 0.160 | 0.281 (0.254–0.309) |

Fair: 0.250.

| Each strategy head-to-head against steady, 2p: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.588 | 0.562 (0.532–0.593) |
| luxury | 0.470 | 0.467 (0.437–0.497) |
| quick | 0.538 | 0.527 (0.497–0.557) |
| steady | 0.468 | 0.481 (0.464–0.499) |

Fair: 0.500.

| Four strategies at one 4p table: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.221 | 0.240 (0.214–0.267) |
| luxury | 0.251 | 0.231 (0.205–0.256) |
| quick | 0.270 | 0.290 (0.262–0.318) |
| steady | 0.257 | 0.239 (0.213–0.265) |

Fair: 0.250.

### `P2-a big sale gives +3 coins not an extra turn`

- **Fixes:** uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 1 (mirror-expert-2p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 2 (mirror-expert-2p)
- **Introduces:** no new flags
- **Still flagged:** uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 1 (mirror-2p); uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 2 (mirror-2p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 1 (mirror-3p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 3 (mirror-3p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 1 (mirror-4p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 4 (mirror-4p); uneven on `won` · Each strategy head-to-head against steady, 2p · strategy=bigsale (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): value 0.588 → 0.683; rarely-used on `bigSales` (mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p)); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 3 (mirror-4p)

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| score | 53.9 | 53.9 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p +1% |
| winGap | 11.2 | 11.2 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p +0% |
| bigSales | 0.00 | 0.00 | mirror-2p 0.00 → 0.00 · mirror-3p 0.00 → 0.00 · mirror-4p 0.00 → 0.00 · all-4p −8% |
| saffronSold | 2.57 | 2.57 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p −0% |
| cardsWasted | 2.02 | 2.02 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p −0% |
| tie | 0.05 | 0.05 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p +11% |

Unchanged: `won`.

| Each strategy head-to-head against steady, 2p: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.588 | 0.683 (0.655–0.712) |
| luxury | 0.470 | 0.469 (0.438–0.500) |
| quick | 0.538 | 0.538 (0.508–0.569) |
| steady | 0.468 | 0.436 (0.419–0.454) |

Fair: 0.500.

| Four strategies at one 4p table: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.221 | 0.242 (0.216–0.268) |
| luxury | 0.251 | 0.253 (0.226–0.279) |
| quick | 0.270 | 0.265 (0.237–0.292) |
| steady | 0.257 | 0.241 (0.215–0.267) |

Fair: 0.250.

### `P2-b big sale needs 5 cards`

- **Fixes:** uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 1 (mirror-expert-2p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 2 (mirror-expert-2p); uneven on `won` · Each strategy head-to-head against steady, 2p · strategy=bigsale (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p)
- **Introduces:** rarely-used (all-4p (also bigsale-vs-steady-2p)): Big sales (> 0) happens in only none of games: an option or reward players almost never use; uneven (all-4p): Four strategies at one 4p table: strategy = bigsale has 0.209 (95% CI 0.184–0.234, n=1000) against a fair 0.250 ± 0.040
- **Still flagged:** uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 1 (mirror-2p); uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 2 (mirror-2p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 1 (mirror-3p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 3 (mirror-3p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 1 (mirror-4p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 4 (mirror-4p); rarely-used on `bigSales` (mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p)); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 3 (mirror-4p)

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| score | 53.9 | 53.9 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p −0% |
| winGap | 11.2 | 11.2 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p +0% |
| bigSales | 0.00 | 0.00 | mirror-2p 0.00 → 0.00 · mirror-3p 0.00 → 0.00 · mirror-4p 0.00 → 0.00 · all-4p −100% |
| saffronSold | 2.57 | 2.57 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p −1% |
| cardsWasted | 2.02 | 2.02 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p −0% |
| tie | 0.05 | 0.05 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p +6% |

Unchanged: `won`.

| Each strategy head-to-head against steady, 2p: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.588 | 0.511 (0.481–0.541) |
| luxury | 0.470 | 0.460 (0.429–0.490) |
| quick | 0.538 | 0.538 (0.508–0.569) |
| steady | 0.468 | 0.497 (0.479–0.515) |

Fair: 0.500.

| Four strategies at one 4p table: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.221 | 0.209 (0.184–0.234) |
| luxury | 0.251 | 0.263 (0.236–0.290) |
| quick | 0.270 | 0.276 (0.249–0.304) |
| steady | 0.257 | 0.251 (0.225–0.278) |

Fair: 0.250.

### `P2-c hand limit 6`

- **Fixes:** uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 1 (mirror-expert-2p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 2 (mirror-expert-2p)
- **Introduces:** uneven (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): Each strategy head-to-head against steady, 2p: strategy = luxury has 0.440 (95% CI 0.409–0.470, n=1000) against a fair 0.500 ± 0.050
- **Still flagged:** uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 1 (mirror-2p): value 0.591 → 0.635; uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 2 (mirror-2p): value 0.409 → 0.364; uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 1 (mirror-3p): value 0.453 → 0.478; uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 3 (mirror-3p): value 0.226 → 0.211; uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 1 (mirror-4p): value 0.352 → 0.400; uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 4 (mirror-4p): value 0.160 → 0.130; rarely-used on `bigSales` (mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p)); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 3 (mirror-4p): value 0.219 → 0.218; uneven on `won` · Each strategy head-to-head against steady, 2p · strategy=bigsale (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): value 0.588 → 0.580

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| score | 53.9 | 54.0 | mirror-2p +0% · mirror-3p +0% · mirror-4p +1% · all-4p +0% |
| winGap | 11.2 | 11.2 | mirror-2p +0% · mirror-3p +4% · mirror-4p −2% · all-4p −5% |
| bigSales | 0.00 | 0.00 | mirror-2p 0.00 → 0.00 · mirror-3p 0.00 → 0.00 · mirror-4p 0.00 → 0.00 · all-4p −30% |
| saffronSold | 2.57 | 2.57 | mirror-2p −0% · mirror-3p +3% · mirror-4p +3% · all-4p +1% |
| cardsWasted | 2.02 | 1.92 | mirror-2p −5% · mirror-3p −3% · mirror-4p −2% · all-4p +0% |
| tie | 0.05 | 0.03 | mirror-2p −37% · mirror-3p +2% · mirror-4p −14% · all-4p −21% |

Unchanged: `won`.

| Seat advantage, 2p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.591 | 0.635 (0.606–0.665) |
| seat 2 | 0.409 | 0.364 (0.335–0.394) |

Fair: 0.500.

| Seat advantage, 3p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.453 | 0.478 (0.448–0.509) |
| seat 2 | 0.322 | 0.310 (0.282–0.338) |
| seat 3 | 0.226 | 0.211 (0.187–0.236) |

Fair: 0.333.

| Seat advantage, 4p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.352 | 0.400 (0.370–0.429) |
| seat 2 | 0.269 | 0.253 (0.226–0.279) |
| seat 3 | 0.219 | 0.218 (0.193–0.244) |
| seat 4 | 0.160 | 0.130 (0.109–0.150) |

Fair: 0.250.

| Each strategy head-to-head against steady, 2p: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.588 | 0.580 (0.549–0.610) |
| luxury | 0.470 | 0.440 (0.409–0.470) |
| quick | 0.538 | 0.513 (0.483–0.543) |
| steady | 0.468 | 0.489 (0.472–0.507) |

Fair: 0.500.

| Four strategies at one 4p table: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.221 | 0.257 (0.230–0.283) |
| luxury | 0.251 | 0.237 (0.211–0.264) |
| quick | 0.270 | 0.271 (0.243–0.298) |
| steady | 0.257 | 0.235 (0.210–0.261) |

Fair: 0.250.

### `PICKS P1-a + P2-b`

- **Fixes:** uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 1 (mirror-2p); uneven on `won` · Seat advantage, 2p (steady bots) · seat=seat 2 (mirror-2p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 1 (mirror-3p); uneven on `won` · Seat advantage, 3p (steady bots) · seat=seat 3 (mirror-3p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 1 (mirror-4p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 4 (mirror-4p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 1 (mirror-expert-2p); uneven on `won` · Seat advantage, 2p (expert bots) · seat=seat 2 (mirror-expert-2p); uneven on `won` · Seat advantage, 4p (steady bots) · seat=seat 3 (mirror-4p); uneven on `won` · Each strategy head-to-head against steady, 2p · strategy=bigsale (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p)
- **Introduces:** rarely-used (all-4p (also bigsale-vs-steady-2p)): Big sales (> 0) happens in only none of games: an option or reward players almost never use; uneven (quick-vs-steady-2p, bigsale-vs-steady-2p, luxury-vs-steady-2p): Each strategy head-to-head against steady, 2p: strategy = quick has 0.550 (95% CI 0.520–0.580, n=1000) against a fair 0.500 ± 0.050
- **Still flagged:** rarely-used on `bigSales` (mirror-2p (also luxury-vs-steady-2p, mirror-3p, mirror-4p, mirror-quick-2p, quick-vs-steady-2p))

| Metric | Baseline, mirror-2p | What-if, mirror-2p | Change in the mean, by profile |
|---|---|---|---|
| score | 53.9 | 55.4 | mirror-2p +3% · mirror-3p +6% · mirror-4p +12% · all-4p +12% |
| winGap | 11.2 | 11.0 | mirror-2p −2% · mirror-3p −4% · mirror-4p −3% · all-4p −3% |
| bigSales | 0.00 | 0.00 | mirror-2p 0.00 → 0.00 · mirror-3p 0.00 → 0.00 · mirror-4p 0.00 → 0.00 · all-4p −100% |
| saffronSold | 2.57 | 2.57 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p −1% |
| cardsWasted | 2.02 | 2.02 | mirror-2p +0% · mirror-3p +0% · mirror-4p +0% · all-4p −0% |
| tie | 0.05 | 0.04 | mirror-2p −15% · mirror-3p +18% · mirror-4p −20% · all-4p −4% |

Unchanged: `won`.

| Seat advantage, 2p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.591 | 0.484 (0.454–0.515) |
| seat 2 | 0.409 | 0.515 (0.485–0.546) |

Fair: 0.500.

| Seat advantage, 3p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.453 | 0.357 (0.328–0.387) |
| seat 2 | 0.322 | 0.331 (0.302–0.360) |
| seat 3 | 0.226 | 0.311 (0.283–0.340) |

Fair: 0.333.

| Seat advantage, 4p (steady bots): seat | Baseline | What-if (95% CI) |
|---|---|---|
| seat 1 | 0.352 | 0.231 (0.206–0.257) |
| seat 2 | 0.269 | 0.247 (0.221–0.273) |
| seat 3 | 0.219 | 0.265 (0.238–0.292) |
| seat 4 | 0.160 | 0.257 (0.230–0.284) |

Fair: 0.250.

| Each strategy head-to-head against steady, 2p: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.588 | 0.513 (0.483–0.543) |
| luxury | 0.470 | 0.470 (0.440–0.501) |
| quick | 0.538 | 0.550 (0.520–0.580) |
| steady | 0.468 | 0.489 (0.471–0.506) |

Fair: 0.500.

| Four strategies at one 4p table: strategy | Baseline | What-if (95% CI) |
|---|---|---|
| bigsale | 0.221 | 0.224 (0.198–0.249) |
| luxury | 0.251 | 0.268 (0.241–0.295) |
| quick | 0.270 | 0.269 (0.241–0.296) |
| steady | 0.257 | 0.239 (0.213–0.265) |

Fair: 0.250.
