# Balance audit: Spice Route, the Royal Chest

The Royal Chest misses all three of its legendary promises. The Rates screen claims two
things the formula doesn't do. The guarantee is "within 90 pulls", but the code guarantees
on pull **91** (`pulls > HARD_PITY`). The screen says "1.6% overall", but the true figure is
**1.44%**. And the designer's target of about 60 pulls is missed, at **69.5** on average,
with the median player needing **80**. The epic promise holds exactly.

The most important change is the one-character fix `>` → `>=`, plus a Rates text that
matches the formula. That is a disclosure problem, so it should ship whatever you decide
about the 60-pull target.

**Design goals.** Taken from the README; I didn't need to infer anything. The chest earns
through gem purchases (160 gems a pull). The primary goal is revenue, measured here as gems
spent per legendary (160 × mean pulls). The guardrails, all from the designer:
1. A legendary in about 60 pulls on average (read as 55–65).
2. Never more than 90 pulls.
3. The Rates screen is true.
4. An epic or better in every 10 pulls.

Goal 1 and revenue pull against each other. Every fix that reaches 60 pulls costs 12–14%
of gems per legendary.

| Scenario | Mean pulls (exact) | Overall legendary rate | Median / 90th pct / longest | Gems per legendary | ≤ 90 pulls always | Mean 55–65 | Best trade-off |
|---|---|---|---|---|---|---|---|
| baseline | 69.50 | 1.439% | 80 / 84 / **91** | 11,120 | ✗ (1 in 2,426) | ✗ | |
| P1-A hard pity `>=` 90 | 69.50 | 1.439% | 80 / 84 / 90 | 11,120 (±0%) | ✓ | ✗ | (if 60 is dropped) |
| P1-B base 0.7% + `>=` | 62.13 | 1.610% | 78 / 84 / 90 | 9,941 (−11%) | ✓ | ✓ | yes |
| P2-A base 0.8% + `>=` | 59.91 | 1.669% | 78 / 84 / 90 | 9,586 (−14%) | ✓ | ✓ | yes |
| **P2-B soft pity from 64 + `>=`** | 60.61 | 1.650% | 68 / 72 / 84 | 9,697 (−13%) | ✓ | ✓ | yes |
| P2-C soft from 66, step 10% + `>=` | 60.89 | 1.642% | 69 / 72 / 76 | 9,743 (−12%) | ✓ | ✓ | yes |

**How this was measured.** I worked the odds out exactly, as fractions, from the formula
(`sim/exact.py`). I then checked them with a seeded simulator (`sim/sim.mjs`). Its baseline
imports and runs the game's own `pull()` from `drops.js`; its what-ifs run a transcription
of `pull()` that matched the original on 200,000 of 200,000 pulls with the same seed. Each
scenario has 20,000 simulated players, each pulling from a fresh account until their first
legendary (seed 1). That gives mean pulls to about ±0.3 and rates to about ±0.6 points.
All 8 exact values fall inside the simulation's 95% interval. A 5-million-pull run of the
game's own code (seed 11) gave a legendary rate of 1.441% (exact 1.4389%) and an
epic rate of 12.32% (exact 12.317%). The chest needs no skill, so there is one player model.
I had no real player data to compare against. Details: `game-model.md`.

**Open questions for the designer.**
1. Is "about 60" a mean (as I read it) or what a typical player should see (the median)?
   This changes which fix is best.
2. Is a 12–14% drop in gems per legendary acceptable, or is 69.5 the number you actually
   want, with the text corrected to match?

## Problems, most harmful first

### 1. The Rates screen makes two claims the formula breaks · Blocker (disclosure)

**What happens.** "Guaranteed within 90 pulls": the hard pity check is `pulls > 90`, so the
guarantee fires on pull 91. Soft pity takes the chance to 70.4% at pull 90, not 100%, so
**1 in 2,426 legendary runs** (0.0412%, exact) needs 91 pulls. In 20,000 simulated players,
9 needed 91 (8.2 expected). At any real player count this happens every day, to a paying
player who can count, and the screen shows they were promised otherwise.

"1.6% overall with pity": the true overall rate is 1 ÷ 69.50 = **1.439%**. 1.6% would need a
mean of 62.5 pulls. App stores require the odds of paid random items to be disclosed, and
an overstated rate is the kind of claim that draws complaints and store action.

| Claim on the Rates screen | Formula, exact | Simulated (20,000 players, 95% CI) | True? |
|---|---|---|---|
| Legendary 0.4% base | 0.4% on pulls 1–76 | — | ✓ |
| 1.6% overall with pity | 1.439% | 1.441% (5M pulls) | ✗ |
| Guaranteed within 90 pulls | longest 91; P(> 90) = 0.0412% | 0.045% ± 0.029% | ✗ |
| Epic 6% base | 6% | — | ✓ |
| Epic or better within 10 pulls | longest rare streak 9 | 0 of 120,000 players saw 10 | ✓ |

**Three suggestions, each tested** (exact, and 20,000 runs on the same seeds):

| | Change | Longest / overall rate, before → after | Effect on goals | Fixes / breaks | Cost |
|---|---|---|---|---|---|
| A | **Tune:** `if (pulls >= HARD_PITY) return 1;` and change the text to "1.4% overall" | 91 → 90; 1.439% (now stated honestly) | Gems per legendary unchanged (11,120) | Fixes both false claims. The 60-pull target is still missed | None |
| B | **Rule:** make 1.6% true: base 0.4% → 0.7%, plus A's `>=` | 91 → 90; 1.439% → 1.610% | Mean 62.1 (meets the target); gems per legendary −11% | Fixes both claims and the target. The text's "0.4%" must become "0.7%" | −1,179 gems per legendary |
| C | **Structure:** generate `RATES_TEXT` from the formula (the chain in `sim/exact.py`), and add a unit test that asserts P(> `HARD_PITY`) = 0 | — (stops future drift) | None by itself | Stops the text and the formula drifting apart. Not simulatable | A build step and a test |

**Recommendation:** A now, whatever you decide on Problem 2. Then C, so the next tuning pass
can't make the screen untrue again. B only if you want to keep the "1.6%" wording; it is a
version of Problem 2's fix.

### 2. A legendary takes 69.5 pulls on average, not about 60, and most players wait 80 · High

**What happens.** For pulls 1–75 the chance is a flat 0.4%, so **74% of players reach soft
pity** without a legendary, and **79% need more than 60 pulls**. The mean is 69.5, but that
hides the experience: the median player needs **80 pulls (12,800 gems)** and the 90th
percentile needs 84. Only 21% get a legendary within 60 pulls. "Reachable at about 60" is
true for about one player in five.

| | Mean | Median | 90th pct | P(within 60) | Target |
|---|---|---|---|---|---|
| Baseline (exact) | 69.50 | 80 | 84 | 21.4% | mean ≈ 60 |

**Three suggestions, each tested** (each includes Problem 1's `>=` fix; exact values, and
20,000 runs on the same seeds, which agree):

| | Change | Mean / median / longest, before → after | P(within 60) | Gems per legendary | Rates text becomes |
|---|---|---|---|---|---|
| A | **Tune:** base legendary 0.4% → 0.8% | 69.5 / 80 / 91 → **59.9** / 78 / 90 | 21% → 38% | 11,120 → 9,586 (−14%) | 0.8%, 1.67% overall, within 90 |
| B | **Rule:** soft pity starts at pull 64 instead of 76 (same 5-point step) | 69.5 / 80 / 91 → **60.6** / 68 / 84 | 21% (unchanged) | 11,120 → 9,697 (−13%) | 0.4%, 1.65% overall, within 84 |
| C | **Structure:** a shorter, steeper pity window: soft pity from 66, 10 points a pull | 69.5 / 80 / 91 → **60.9** / 69 / 76 | 21% (unchanged) | 11,120 → 9,743 (−12%) | 0.4%, 1.64% overall, within 76 |

All three meet the target and keep every guardrail. They differ in how the wait feels:
- **A** gets there through lucky early pulls: 38% of players hit a legendary by pull 60,
  but the median player still waits 78. That is more "I got lucky" stories, but the
  typical player sees almost no change.
- **B** moves the whole pack: the median drops from 80 to 68, and nobody waits past 84.
  The typical wait comes closest to the stated intent.
- **C** is the most predictable: everyone gets one by 76, the median is 69, and it costs
  the least gems. But nearly every legendary comes from pity, so the 0.4% base rate stops
  meaning much.

**Recommendation:** B (soft pity from 64, `>=`), if the designer accepts the 13% drop in
gems per legendary. It is the only option that makes "about 60" what a typical player sees,
and it ends the guarantee at pull 84, well inside the promised 90. If revenue per legendary
can't drop, keep the current odds, apply Problem 1-A, and change the design target to
about 70.

The simulator can't tell you whether a sooner legendary makes players pull (and buy gems)
**more** often. That decides whether the −13% is a real loss. It needs an A/B test on
gem spend per payer over 30 days, not a simulation.

## Recommended changes together

P2-B already includes P1-A, so the combined change is: `SOFT_PITY_FROM = 64`,
`if (pulls >= HARD_PITY) return 1;`, and the text "Legendary: 0.4% (1.65% overall with
pity; guaranteed within 84 pulls). Epic: 6% (12.2% overall; guaranteed within 10 pulls)."

| Metric | Before | After |
|---|---|---|
| Mean pulls to legendary | 69.50 | 60.61 |
| Median / 90th pct / longest | 80 / 84 / 91 | 68 / 72 / 84 |
| Overall legendary rate | 1.439% | 1.650% |
| Overall epic rate | 12.32% | 12.21% |
| Epic or better in every 10 pulls | ✓ | ✓ |
| Gems per legendary | 11,120 | 9,697 |

Nothing else broke. The epic guarantee is untouched, because a legendary still resets the
epic counter.

## Also noticed

- **The epic line mixes bases (low).** The legendary line gives an overall rate, but the epic
  line gives only the 6% base; the overall epic rate is 12.3%. The screen is true, but
  showing "12.3% overall" next to it would make the two lines read the same way.
- **The soft pity comment is off by one (low).** The comment says the chance climbs "from the
  76th pull", but at pull 76 it is still 0.4% (`STEP × 0`); the first rise is at pull 77.
  It's harmless now, but it is the same kind of boundary slip as the hard pity bug. Keep it
  in mind if the comment ever feeds the Rates text.
- **The `Math.min(1, …)` in soft pity never applies** under the current constants (the chance
  reaches only 70.4% by pull 90). It would apply with the soft-pity fixes above.

## What this audit can't tell you

- **Whether 60 pulls feels reachable.** That depends on how many pulls a player gets for free
  each week. Playtest question: after two weeks, do free-to-play testers think a legendary
  is in reach?
- **Spending response.** Whether faster legendaries raise or lower gem purchases per payer
  (see Problem 2).
- **Randomness and compliance.** The game's random number generator isn't tested, and this
  is design analysis, not certification of the disclosure. Check each store's and region's
  rules (some require per-item rates).

## Re-running it

```bash
cd balance-audit
python3 sim/exact.py                    # exact odds (fractions), baseline and the >= fix
python3 sim/search.py                   # exact what-ifs over base rate, soft pity start and step
node sim/sim.mjs --check                # transcription check + 5M-pull long run of the game's pull()
node sim/sim.mjs --runs 20000 --seed 1 --out runs/all.jsonl
python3 <skill>/scripts/analyze.py audit.json runs/all.jsonl --out results
```
