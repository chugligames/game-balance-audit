# Royal Chest balance audit (`drops.js`)

**Bottom line:** The chest misses 2 of the README's 3 goals, and the Rates screen says 3 things
that are not true. Because the odds disclosure covers paid random items, fix the Rates screen
before the next release, even if the balance numbers stay as they are.

| Goal (README) | Result | Status |
|---|---|---|
| A legendary in about 60 pulls on average | **69.5 pulls** on average (11,120 gems); median 80 | ❌ Fails |
| A legendary in no more than 90 pulls | **91 pulls** is possible (about 1 in 2,440 legendary cycles) | ❌ Fails |
| The Rates screen is true | 3 false statements (see F3) | ❌ Fails |
| An epic or better at least every 10 pulls | The longest gap is 10 | ✅ Passes |

## How I checked this

- **Exact figures:** I took `legendaryChance(k)` for every value of k and computed the exact
  distribution of pulls until a legendary. See `run.mjs`.
- **Simulation:** I ran 20 million pulls through the real `pull()` function, imported unchanged
  from `../drops.js`. Results: 1.439% legendary, 12.31% epic, 86.25% rare. The longest run
  without a legendary was 91 pulls, and the longest run without an epic or better was 10. The
  simulation agrees with the exact figures.
- **Fix options:** I computed the same figures for each proposed setting. See `opt.mjs`.
- To re-run: `node balance-audit/run.mjs` and `node balance-audit/opt.mjs`.

## Findings

### F1. Hard pity triggers on pull 91, not pull 90 (off-by-one bug)
`legendaryChance` uses `if (pulls > HARD_PITY) return 1;`. The pull counter already counts the
current pull, so the guarantee doesn't fire until `pulls === 91`. On pull 90 the chance is only
0.004 + 0.05 × 14 = 70.4%. About 0.04% of legendary cycles reach pull 91. That sounds rare, but
across a large player base it happens to many real players, and every one of them can point to
the "guaranteed within 90" promise.
**Fix:** change `>` to `>=`. This changes nothing else: the average stays at 69.5 pulls and the
worst case becomes exactly 90.

### F2. Soft pity starts one pull later than the comment says
The comment says the chance climbs "from the 76th pull". In the code, `SOFT_PITY_STEP * (pulls - SOFT_PITY_FROM)`
equals 0 on pull 76, so the first increase comes on pull 77. Either the comment or the
constant is off by one. This doesn't affect the README goals on its own, but it is the same
kind of mistake as F1.

### F3. The Rates screen (`RATES_TEXT`) is false in 3 places
| Claim | Actual | Direction |
|---|---|---|
| "1.6% overall with pity" | **1.44%** (1 in 69.5) | Overstates the odds in the game's favor. This is the most serious one: players are told their odds are better than they are |
| "guaranteed within 90 pulls" | Within **91** (F1) | Overstates |
| "Epic: 6% (guaranteed within 10 pulls)" | The base roll is 5.98% (the 6% roll only happens when the legendary roll fails). With pity, epics are **12.3%** of all pulls | Understates. Harmless to players, but still not accurate |

**Fix:** generate `RATES_TEXT` from the constants and the computed overall rate, rather than
writing the numbers by hand. Then show both the base rate and the overall rate for each tier,
for example: "Legendary: 0.4% base, 1.44% overall incl. pity; guaranteed by pull 90.
Epic: 6% base, 12.3% overall incl. pity; an epic or better guaranteed every 10 pulls."

### F4. The average is about 70 pulls, not about 60
Exact figures for the current curve: average 69.5 pulls, median 80. 74% of players reach soft
pity without a legendary, so for most players soft pity is what delivers the legendary, not
luck. The base 0.4% rate almost never pays out early: only 21% get a legendary within 60 pulls.
The expected cost is **11,120 gems per legendary**, against about 9,600 at the 60-pull target.
That is roughly 16% more expensive than designed.

**Smallest fix that hits the target:** keep `BASE.legendary = 0.004` and `SOFT_PITY_STEP = 0.05`,
set `SOFT_PITY_FROM = 63`, and apply F1.

| Setting | Average pulls | Overall rate | Worst case |
|---|---|---|---|
| Current code | 69.50 | 1.439% | 91 |
| F1 only (`>=`) | 69.50 | 1.439% | 90 |
| F1 + `SOFT_PITY_FROM = 63` | **59.85** | **1.671%** | 83 (hard pity never fires) |
| F1 + `SOFT_PITY_FROM = 64` | 60.61 | 1.650% | 84 |

Other combinations are in `opt.mjs`. With `SOFT_PITY_FROM = 63`, the real overall rate (about
1.67%) also comes close to the 1.6% the Rates screen advertises now. The 1.6% may have been
worked out for an earlier soft-pity start. The text still has to show the actual number.
One consequence: with this curve the chance reaches 100% at pull 83, so hard pity at 90 is
never actually used. That is fine, but the designer should know it.

### F5. The 10-pull epic guarantee works
`sinceEpic` resets on legendaries too, so "epic or better" is counted correctly. In 20 million
simulated pulls, the longest gap was exactly 10. No change needed.

## Minor notes
- `pull()` changes `state` directly and calls `rand()` a second time only when the legendary
  roll fails. Both are fine, but anyone porting this to the server must keep the same order of
  random draws, or the rates will drift.
- No tests cover any of this. A unit test should check that `legendaryChance(HARD_PITY) === 1`,
  and another should check that the overall rate in `RATES_TEXT` matches the exact calculation.
  Either one would have caught F1 and F3.
