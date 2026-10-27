# Balance summary: Ladoo Spin

168000 rows · baseline `baseline` + 6 what-if scenario(s) · player profiles: flat-1, casual, regular, keen · 200 runs each

## Exact answers against the simulation

Each exact value is computed without sampling (enumeration, or a Markov chain); the simulation should land within its 95% interval of it. A ✗ means the simulator, or its reading of the rules, is wrong.

| Quantity | Exact | Simulated (95% interval) | Samples | Agrees |
|---|---|---|---|---|
| RTP | 1.039352 | 1.035908 ± 0.004580 | 200 | ✓ |
| Hit rate | 0.310185 | 0.309816 ± 0.000351 | 200 | ✗ |
| Big-win rate (40x+) | 0.002894 | 0.002878 ± 0.000042 | 200 | ✓ |

## Scenarios against the design goals

Each goal is measured per player over the segments it names, then averaged over runs (± is a 95% interval). ▲/▼: better/worse than the baseline beyond noise. ✗: breaks a constraint. Best trade-off: no other scenario that keeps every constraint is at least as good on every goal and better on one. Weighted change: the goals' changes from the baseline, weighted as in audit.json, only to sort the table.

| Scenario | Regular player's free-coin drift per day: gift + wins - bets (want negative) (lower is better) | Coin purchases per keen player, 30 days (higher is better) | RTP 95.5-96.5% (0.95–0.96) | Hit rate ~3 in 10 (27-33%) (0.27–0.33) | Big win every few hundred spins (1/500 to 1/150) (0.00–0.01) | Casual player out of coins on <=10% of days (assumed guardrail) (≤ 0.10) | Weighted change | Best trade-off |
|---|---|---|---|---|---|---|---|---|
| `P2-A gift 500->150 (+P1-A)` | 22.0 ± 33.7 (−97%) ▲ | 4.56 ± 0.25 (+228%) ▲ | ✓ 0.96 | ✓ 0.31 | ✓ 0.00 | ✓ 0.01 | +422% | yes |
| `P2-B gift tops up to 500 (+P1-A)` | 49.6 ± 30.5 (−93%) ▲ | 3.64 ± 0.23 (+162%) ▲ | ✓ 0.96 | ✓ 0.31 | ✓ 0.00 | ✓ 0.00 | +347% |  |
| `P2-C max bet 100->500 (+P1-A)` | 319 ± 44.3 (−53%) ▲ | 4.29 ± 0.24 (+209%) ▲ | ✓ 0.96 | ✓ 0.31 | ✓ 0.00 | ✓ 0.00 | +316% |  |
| `P1-A pays: MANGOx3 10->6, LADOOx3 200->207` | 319 ± 44.3 (−53%) ▲ | 3.17 ± 0.22 (+128%) ▲ | ✓ 0.96 | ✓ 0.31 | ✓ 0.00 | ✓ 0.00 | +235% |  |
| `P1-C rule: lone CHILLI pays 0, CHILLIx2 5->4` | 299 ± 43.2 (−56%) ▲ | 3.65 ± 0.23 (+162%) ▲ | ✗ 0.95 | ✗ 0.25 | ✓ 0.00 | ✓ 0.00 | +275% |  |
| `P1-B strip: reel 2 stop 7 MANGO->CHILLI` | 305 ± 43.2 (−55%) ▲ | 3.27 ± 0.24 (+136%) ▲ | ✗ 0.95 | ✓ 0.28 | ✓ 0.00 | ✓ 0.00 | +246% |  |
| `baseline` | 683 ± 48.6 | 1.39 ± 0.17 | ✗ 1.04 | ✓ 0.31 | ✓ 0.00 | ✓ 0.00 | +0% |  |


## Flags in the baseline

| Severity | Check | Player profile | Finding |
|---|---|---|---|
| high | off-target | regular | Regular player's balance drifts down: mean 1: 701, 2: 563, 3: 910, 4: 543, 5: 756, 6: 757, 7: 697, 8: 706 …, target ≤ 0.00 (missed in 30 of 30 days) |
| high | never-binds | casual (also flat-1) | Ran out of coins (purchase moment) > 0 never happens in any of the days, so this limit puts no pressure on the player (closest it gets: 0.00) |
| high | exact-mismatch | all | Hit rate: the simulation gives 0.309816 ± 0.000351 but the exact value is 0.310185. Fix the simulator before trusting anything else |
| medium | rarely-used | regular (and every other profile) | Coin packs bought (> 0) happens in only 1% of days: an option or reward players almost never use |

Never changes: `coinIn` = 600 (casual); `coinIn` = 1000 (flat-1); `gift` = 500; `lowBalance` = 0.00 (casual); `lowBalance` = 0.00 (flat-1); `outOfCoins` = 0.00 (casual); `outOfCoins` = 0.00 (flat-1); `purchases` = 0.00 (casual); `purchases` = 0.00 (flat-1); `spins` = 60.0 (casual); `spins` = 1000 (flat-1)

## Baseline by day

Mean per day, with the 10th–90th percentile range in brackets.

### Coin balance at end of day (`balance`)

| day | flat-1 | casual | regular | keen |
|---|---|---|---|---|
| 1 | 1026 (813–1272) | 984 (720–1281) | 1311 (0.00–4097) | 1890 (0.00–5121) |
| 2 | 1568 (1253–1934) | 1473 (1060–1911) | 1954 (0.00–5615) | 2977 (0.00–8127) |
| 3 | 2102 (1728–2530) | 1999 (1429–2603) | 2914 (0.00–7337) | 4463 (0.00–15546) |
| 4 | 2636 (2215–3095) | 2518 (1839–3503) | 3497 (0.00–8150) | 5596 (0.00–22725) |
| 5 | 3194 (2740–3748) | 3073 (2268–4514) | 4273 (0.00–10030) | 7624 (0.00–28954) |
| 6 | 3744 (3254–4320) | 3586 (2629–5044) | 5041 (0.00–11835) | 8989 (0.00–36971) |
| 7 | 4272 (3732–4888) | 4108 (3040–5725) | 5747 (0.00–12700) | 10582 (0.00–39812) |
| 8 | 4835 (4241–5468) | 4628 (3410–6382) | 6463 (45.0–13538) | 12456 (0.00–42137) |
| 9 | 5382 (4794–6035) | 5153 (3907–6845) | 7154 (490–14475) | 14547 (0.00–43157) |
| 10 | 5912 (5207–6722) | 5600 (4308–7516) | 7753 (1468–16128) | 16235 (0.00–49981) |
| 11 | 6462 (5700–7294) | 6146 (4698–8251) | 8513 (1658–17532) | 19059 (0.00–55543) |
| 12 | 7004 (6236–7842) | 6695 (5189–8626) | 9500 (2298–18005) | 21034 (19.0–61170) |
| 13 | 7538 (6751–8396) | 7260 (5726–9250) | 10307 (2795–19432) | 22338 (10.9–63476) |
| 14 | 8054 (7300–9003) | 7784 (6136–10140) | 10889 (2665–20260) | 22921 (7.90–63636) |
| 15 | 8577 (7753–9492) | 8248 (6519–10551) | 11299 (2485–20730) | 23498 (0.00–72526) |
| 16 | 9104 (8222–9945) | 8874 (7097–11118) | 12304 (3092–22170) | 25929 (8.60–77801) |
| 17 | 9636 (8678–10533) | 9357 (7517–11823) | 12904 (3320–22935) | 27182 (7.80–78778) |
| 18 | 10174 (9266–11200) | 9872 (7960–12434) | 13604 (3398–24702) | 28910 (6.30–79891) |
| 19 | 10699 (9732–11816) | 10368 (8446–12965) | 14141 (4105–25925) | 30034 (9.70–82404) |
| 20 | 11206 (10228–12337) | 10870 (8847–13400) | 14695 (4242–26910) | 31205 (0.00–84406) |
| 21 | 11739 (10810–12943) | 11380 (9317–13942) | 15448 (5130–26987) | 32952 (19.7–83909) |
| 22 | 12275 (11185–13465) | 11892 (9836–14478) | 15979 (5295–27972) | 34455 (0.00–87954) |
| 23 | 12806 (11704–14050) | 12438 (10188–15200) | 16520 (5958–29002) | 36072 (12.6–88109) |
| 24 | 13336 (12185–14560) | 12962 (10629–15839) | 17212 (5850–29530) | 38851 (23.0–87868) |
| 25 | 13862 (12718–15043) | 13480 (11139–16401) | 17877 (6870–30200) | 39767 (19.9–90413) |
| 26 | 14394 (13238–15636) | 13997 (11582–16906) | 18498 (7088–30700) | 41626 (29.9–97584) |
| 27 | 14944 (13728–16122) | 14525 (12045–17464) | 19054 (7570–31160) | 43454 (29.9–98793) |
| 28 | 15496 (14314–16674) | 15049 (12574–18579) | 19757 (8328–32217) | 45805 (27.8–104584) |
| 29 | 16041 (14821–17328) | 15619 (12944–19081) | 20720 (8700–35405) | 48751 (26.9–106993) |
| 30 | 16577 (15311–17780) | 16130 (13367–19776) | 21480 (9420–35542) | 50906 (33.9–109625) |

### Ran out of coins (purchase moment) (`outOfCoins`) · limit hit when > 0

| day | flat-1 | casual | regular | keen |
|---|---|---|---|---|
| 1 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.49 (0.00–1.00) | 0.26 (0.00–1.00) |
| 2 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.41 (0.00–1.00) | 0.23 (0.00–1.00) |
| 3 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.30 (0.00–1.00) | 0.20 (0.00–1.00) |
| 4 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.26 (0.00–1.00) | 0.20 (0.00–1.00) |
| 5 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.20 (0.00–1.00) | 0.23 (0.00–1.00) |
| 6 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.14 (0.00–1.00) | 0.17 (0.00–1.00) |
| 7 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.14 (0.00–1.00) | 0.18 (0.00–1.00) |
| 8 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.10 (0.00–1.00) | 0.18 (0.00–1.00) |
| 9 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.10 (0.00–0.10) | 0.20 (0.00–1.00) |
| 10 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.06 (0.00–0.00) | 0.18 (0.00–1.00) |
| 11 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.04 (0.00–0.00) | 0.15 (0.00–1.00) |
| 12 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.03 (0.00–0.00) | 0.11 (0.00–1.00) |
| 13 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.03 (0.00–0.00) | 0.10 (0.00–1.00) |
| 14 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.03 (0.00–0.00) | 0.10 (0.00–1.00) |
| 15 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.02 (0.00–0.00) | 0.17 (0.00–1.00) |
| 16 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.13 (0.00–1.00) |
| 17 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.17 (0.00–1.00) |
| 18 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.12 (0.00–1.00) |
| 19 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.11 (0.00–1.00) |
| 20 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.17 (0.00–1.00) |
| 21 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.09 (0.00–0.00) |
| 22 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.17 (0.00–1.00) |
| 23 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.12 (0.00–1.00) |
| 24 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.12 (0.00–1.00) |
| 25 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.07 (0.00–0.00) |
| 26 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.09 (0.00–0.00) |
| 27 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.10 (0.00–0.00) |
| 28 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.07 (0.00–0.00) |
| 29 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.06 (0.00–0.00) |
| 30 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.07 (0.00–0.00) |

### Coin packs bought (`purchases`)

| day | flat-1 | casual | regular | keen |
|---|---|---|---|---|
| 1 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.06 (0.00–0.00) | 0.10 (0.00–0.10) |
| 2 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.04 (0.00–0.00) | 0.07 (0.00–0.00) |
| 3 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.03 (0.00–0.00) | 0.04 (0.00–0.00) |
| 4 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.02 (0.00–0.00) | 0.07 (0.00–0.00) |
| 5 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.10 (0.00–0.00) |
| 6 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.04 (0.00–0.00) |
| 7 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.08 (0.00–0.00) |
| 8 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.06 (0.00–0.00) |
| 9 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.09 (0.00–0.00) |
| 10 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.06 (0.00–0.00) |
| 11 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.03 (0.00–0.00) |
| 12 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.04 (0.00–0.00) |
| 13 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.04 (0.00–0.00) |
| 14 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.03 (0.00–0.00) |
| 15 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.04 (0.00–0.00) |
| 16 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.05 (0.00–0.00) |
| 17 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.08 (0.00–0.00) |
| 18 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.03 (0.00–0.00) |
| 19 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.03 (0.00–0.00) |
| 20 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.06 (0.00–0.00) |
| 21 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.03 (0.00–0.00) |
| 22 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.05 (0.00–0.00) |
| 23 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.04 (0.00–0.00) |
| 24 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.04 (0.00–0.00) |
| 25 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) |
| 26 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.03 (0.00–0.00) |
| 27 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) | 0.04 (0.00–0.00) |
| 28 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) |
| 29 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.01 (0.00–0.00) |
| 30 | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.00 (0.00–0.00) | 0.02 (0.00–0.00) |

## What-ifs against the baseline

### `P1-A pays: MANGOx3 10->6, LADOOx3 200->207`

- **Fixes:** rarely-used on `purchases` (keen)
- **Introduces:** no new flags
- **Still flagged:** off-target on `drift` · Regular player's balance drifts down (regular): clear misses 30 → 23; never-binds on `outOfCoins` (casual (also flat-1)); rarely-used on `purchases` (regular (also casual, flat-1)): rate 1% → 2%

| Metric | Baseline, regular (first third → last third) | What-if, regular | Change in the mean, by profile |
|---|---|---|---|
| balance | 4611 → 18255 | 2852 → 9763 | flat-1 −14% · casual −9% · regular −44% · keen −61% |
| outOfCoins | 0.22 → 0.01 | 0.43 → 0.13 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +206% · keen +143% |
| purchases | 0.02 → 0.00 | 0.03 → 0.02 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +179% · keen +128% |

### `P1-B strip: reel 2 stop 7 MANGO->CHILLI`

- **Fixes:** rarely-used on `purchases` (keen)
- **Introduces:** no new flags
- **Still flagged:** off-target on `drift` · Regular player's balance drifts down (regular): clear misses 30 → 20; never-binds on `outOfCoins` (casual (also flat-1)); rarely-used on `purchases` (regular (also casual, flat-1)): rate 1% → 2%

| Metric | Baseline, regular (first third → last third) | What-if, regular | Change in the mean, by profile |
|---|---|---|---|
| balance | 4611 → 18255 | 2964 → 9546 | flat-1 −15% · casual −9% · regular −45% · keen −70% |
| outOfCoins | 0.22 → 0.01 | 0.41 → 0.12 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +187% · keen +176% |
| purchases | 0.02 → 0.00 | 0.04 → 0.01 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +208% · keen +136% |

### `P1-C rule: lone CHILLI pays 0, CHILLIx2 5->4`

- **Fixes:** rarely-used on `purchases` (keen)
- **Introduces:** no new flags
- **Still flagged:** off-target on `drift` · Regular player's balance drifts down (regular): clear misses 30 → 20; never-binds on `outOfCoins` (casual (also flat-1)); rarely-used on `purchases` (regular (also casual, flat-1)): rate 1% → 3%

| Metric | Baseline, regular (first third → last third) | What-if, regular | Change in the mean, by profile |
|---|---|---|---|
| balance | 4611 → 18255 | 2804 → 9457 | flat-1 −15% · casual −9% · regular −46% · keen −64% |
| outOfCoins | 0.22 → 0.01 | 0.44 → 0.13 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +209% · keen +177% |
| purchases | 0.02 → 0.00 | 0.04 → 0.02 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +215% · keen +162% |

### `P2-A gift 500->150 (+P1-A)`

- **Fixes:** never-binds on `outOfCoins` (casual); rarely-used on `purchases` (regular (also keen))
- **Introduces:** no new flags
- **Still flagged:** off-target on `drift` · Regular player's balance drifts down (regular): clear misses 30 → 1; never-binds on `outOfCoins` (flat-1); rarely-used on `purchases` (casual (also flat-1))

| Metric | Baseline, regular (first third → last third) | What-if, regular | Change in the mean, by profile |
|---|---|---|---|
| balance | 4611 → 18255 | 1450 → 3826 | flat-1 −76% · casual −72% · regular −77% · keen −74% |
| outOfCoins | 0.22 → 0.01 | 0.67 → 0.47 | flat-1 0.00 → 0.00 · casual 0.00 → 0.01 · regular +582% · keen +257% |
| purchases | 0.02 → 0.00 | 0.07 → 0.04 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +596% · keen +228% |

### `P2-B gift tops up to 500 (+P1-A)`

- **Fixes:** rarely-used on `purchases` (keen)
- **Introduces:** no new flags
- **Still flagged:** off-target on `drift` · Regular player's balance drifts down (regular): clear misses 30 → 1; never-binds on `outOfCoins` (casual (also flat-1)); rarely-used on `purchases` (regular (also casual, flat-1)): rate 1% → 5%

| Metric | Baseline, regular (first third → last third) | What-if, regular | Change in the mean, by profile |
|---|---|---|---|
| balance | 4611 → 18255 | 1770 → 4173 | flat-1 −93% · casual −86% · regular −73% · keen −67% |
| outOfCoins | 0.22 → 0.01 | 0.59 → 0.36 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +449% · keen +172% |
| purchases | 0.02 → 0.00 | 0.05 → 0.04 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +496% · keen +162% |

### `P2-C max bet 100->500 (+P1-A)`

- **Fixes:** rarely-used on `purchases` (keen)
- **Introduces:** no new flags
- **Still flagged:** off-target on `drift` · Regular player's balance drifts down (regular): clear misses 30 → 23; never-binds on `outOfCoins` (casual (also flat-1)); rarely-used on `purchases` (regular (also casual, flat-1)): rate 1% → 2%

| Metric | Baseline, regular (first third → last third) | What-if, regular | Change in the mean, by profile |
|---|---|---|---|
| balance | 4611 → 18255 | 2852 → 9763 | flat-1 −14% · casual −9% · regular −44% · keen −66% |
| outOfCoins | 0.22 → 0.01 | 0.43 → 0.13 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +206% · keen +220% |
| purchases | 0.02 → 0.00 | 0.03 → 0.02 | flat-1 0.00 → 0.00 · casual 0.00 → 0.00 · regular +179% · keen +209% |
