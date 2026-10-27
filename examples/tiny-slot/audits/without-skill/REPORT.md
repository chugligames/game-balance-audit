# Ladoo Spin: balance audit

**Verdict: not balanced the way you want.** The real return to player (RTP) is **103.9%**, not 96%.
Players' balances drift **up**, so keen players have no reason to buy coins. The other two targets
(hit rate and big-win frequency) are met.

| Target (README)                    | Designer's sheet | Actual (exact)              | Status |
|------------------------------------|------------------|-----------------------------|--------|
| RTP 96%                            | 96.01%           | **103.94%** (1796 / 1728)   | FAIL: above 100% |
| Win on about 3 in 10 spins         | 28.2%            | **31.0%** (536 / 1728, 1 in 3.2) | OK |
| Big win (≥40×) every few hundred   | 1 in 864         | **1 in 346** (5 / 1728)     | OK |

## Method

The game has only 12 × 12 × 12 = 1,728 equally likely outcomes, so I counted every one of them
exactly. I didn't simulate. The script is `balance-audit/enumerate.py` (run it with
`python3 balance-audit/enumerate.py reels.csv`). Rules applied as the README describes: centre line
only, one stop per reel, and only the highest qualifying win pays. "Any three sweets" therefore never
stacks on top of a matching triple, and "CHILLI on reel 1" doesn't pay when "CHILLI CHILLI" does.

## Per-line breakdown (actual reels)

| Combination              | Pays | Hits / 1728 | Probability | RTP share | Designer's sheet |
|--------------------------|-----:|------------:|------------:|----------:|-----------------:|
| LADOO ×3                 | 200  | 1           | 0.000579    | 11.57%    | 11.57% |
| DIYA ×3                  | 50   | 4           | 0.002315    | 11.57%    | 2.89% |
| CHAI ×3                  | 25   | 2           | 0.001157    | 2.89%     | 1.45% |
| MANGO ×3                 | 10   | 36          | 0.020833    | 20.83%    | 37.04% |
| Any three sweets (mixed) | 2    | 349         | 0.201968    | 40.39%    | 31.94% |
| CHILLI CHILLI (reels 1+2)| 5    | 36          | 0.020833    | 10.42%    | 3.47% |
| CHILLI on reel 1 only    | 1    | 108         | 0.062500    | 6.25%     | 7.64% |
| **Total**                |      | **536**     |             | **103.94%** | 96.01% |

## Root cause: the sheet was built from reel 1 copied three times

If reel 1's strip is used for all three reels, every probability and RTP figure in `paytable.csv`
comes out exactly, row for row, totalling 96.01%. But reels 2 and 3 are different strips:

| Symbol | Reel 1 | Reel 2 | Reel 3 |
|--------|:-----:|:-----:|:-----:|
| MANGO  | 4 | 3 | 3 |
| DIYA   | 1 | 2 | 2 |
| CHAI   | 1 | 2 | 1 |
| LADOO  | 1 | 1 | 1 |
| CHILLI | 1 | **3** | 0 |
| BLANK  | 4 | **1** | 5 |

Reel 2 has three CHILLIs and only one BLANK, while the sheet assumed one CHILLI and four BLANKs. That
raises CHILLI CHILLI from 12 to 36 hits and makes mixed-sweet lines more likely. The extra DIYA and
CHAI stops also double or quadruple those triples. Together these outweigh the drop in MANGO ×3.

## What this means for the economy

At 103.9% the average player gains about 3.9% of everything they bet. A max-bet (100-coin) player
expects about **+394 coins per 100 spins**. Swings are large (SD ≈ 5.7× the bet per spin), so this
won't show over a short session. Over a long run the effect is clear, by a normal approximation:

| Spins | Chance a player is ahead at 103.9% | at 96% |
|------:|:----:|:----:|
| 100    | ~53% | ~47% |
| 1,000  | ~59% | ~41% |
| 10,000 | ~76% | ~24% |

At the current settings, regular players pile up coins on top of the 500 a day they get free. That is
the opposite of the "drift down so keen players buy" goal. It's also hard to fix after launch, because
any coins already in players' balances stay there.

## Fixes (pick one)

1. **Lower the MANGO ×3 pay from 10 to 6.** This is a one-cell change. Exact RTP becomes **95.6%**
   (1652 / 1728). Hit rate (31.0%) and big-win frequency (1 in 346) are unchanged, because only the
   pay changes, not how often lines hit. Equivalent alternatives at 95.6%: MANGO 7 + CHILLI CHILLI 4,
   MANGO 8 + CHILLI CHILLI 3, or MANGO 9 + CHILLI CHILLI 2 (from `balance-audit/fixes.py`). No
   integer change to one or two cells lands closer to 96.0%.
2. **Make all three reels match reel 1.** This reproduces the designer's sheet exactly (96.01%), but
   the hit rate drops to 28.2% and big wins to 1 in 864. That's still about 3 in 10, but "every few
   hundred" becomes a stretch.
3. Re-tune the reel 2/3 strips by hand (e.g. swap two of reel 2's CHILLIs for BLANKs), then re-run
   `enumerate.py`. This is more flexible, but every edit has to be counted again.

My recommendation is fix 1, because it keeps the feel the designer described and moves only the
return. Whichever you choose, rebuild the paytable's probability column from the real three strips,
not from reel 1. `enumerate.py` does that in under a second.

## Caveats

- I read "any three sweets (… mixed)" and the CHILLI lines using the README's "only the highest win
  counts" rule. Under any other reading of those lines the RTP is still above 100%: the counts that
  break it (CHILLI CHILLI, DIYA ×3, mixed sweets) don't depend on the reading.
- The "chance ahead" figures use a normal approximation. They show direction and rough size, not
  exact odds.
- Bet size (1–100) scales wins and losses equally, so it doesn't change RTP.
