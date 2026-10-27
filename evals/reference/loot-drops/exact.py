"""The exact answer for examples/loot-drops: the number of pulls to a legendary is a renewal
process, so its distribution follows from the per-pull chances alone (a product of
"didn't drop" terms). Exact fractions, no sampling.
    python3 exact.py"""
from fractions import Fraction as F

BASE = F(4, 1000)
SOFT_FROM, STEP, HARD = 76, F(5, 100), 90
GEMS = 160


def chance(n):
    """drops.js legendaryChance, exactly (note `> HARD`, as written)."""
    if n > HARD:
        return F(1)
    if n >= SOFT_FROM:
        return min(F(1), BASE + STEP * (n - SOFT_FROM))
    return BASE


def distribution():
    """P(the first legendary comes on pull n), n = 1, 2, …"""
    out, alive, n = [], F(1), 0
    while alive > 0:
        n += 1
        p = chance(n)
        out.append(alive * p)
        alive *= 1 - p
    return out


def exact():
    d = distribution()
    mean = sum((i + 1) * p for i, p in enumerate(d))
    cum, median, p90 = F(0), None, None
    for i, p in enumerate(d):
        cum += p
        if median is None and cum >= F(1, 2):
            median = i + 1
        if p90 is None and cum >= F(9, 10):
            p90 = i + 1
    return {"mean": mean, "rate": 1 / mean, "beyond_90": sum(d[90:]), "last": len(d), "median": median, "p90": p90, "gems": mean * GEMS}


if __name__ == "__main__":
    e = exact()
    print("mean pulls per legendary: %.6f (exact fraction has a %d-digit denominator)" % (float(e["mean"]), len(str(e["mean"].denominator))))
    print("overall legendary rate: %.4f%% (Rates screen says 1.6%%)" % (100 * float(e["rate"])))
    print("chance a streak needs pull 91: %.6f%% = 1 in %.0f (Rates screen says guaranteed within 90)" % (100 * float(e["beyond_90"]), 1 / float(e["beyond_90"])))
    print("longest possible streak: %d pulls" % e["last"])
    print("median pulls: %d, 90th percentile: %d" % (e["median"], e["p90"]))
    print("gems per legendary on average: %.1f (at 1.6%% it would be %.0f)" % (float(e["gems"]), 160 / 0.016))
