"""The exact answer for examples/tiny-slot, by enumerating every outcome (12 x 12 x 12 = 1,728
equally likely stops). Small enough to check by hand from the symbol counts.
    python3 exact.py"""
import csv
import os
from fractions import Fraction as F
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "../../../examples/tiny-slot")
SWEETS = {"LADOO", "DIYA", "CHAI", "MANGO"}
THREE = {"LADOO": 200, "DIYA": 50, "CHAI": 25, "MANGO": 10}


def reels():
    with open(os.path.join(GAME, "reels.csv")) as f:
        rows = list(csv.DictReader(f))
    return [[r["reel_%d" % i] for r in rows] for i in (1, 2, 3)]


def pays(a, b, c):
    """The paytable's rules, highest win only."""
    if a == b == c and a in THREE:
        return THREE[a], "three %s" % a
    if a in SWEETS and b in SWEETS and c in SWEETS:
        return 2, "any three sweets"
    if a == "CHILLI" and b == "CHILLI":
        return 5, "CHILLI CHILLI"
    if a == "CHILLI":
        return 1, "CHILLI on reel 1"
    return 0, "no win"


def exact():
    r = reels()
    n = 0
    total = F(0)
    square = F(0)
    by_line = {}
    hits = big = 0
    for a, b, c in product(*r):
        w, line = pays(a, b, c)
        n += 1
        total += w
        square += w * w
        by_line[line] = by_line.get(line, 0) + 1
        hits += w > 0
        big += w >= 40
    rtp = total / n
    return {
        "outcomes": n,
        "rtp": rtp,
        "hit_rate": F(hits, n),
        "big_win_rate": F(big, n),
        "sd_per_spin": float(square / n - rtp * rtp) ** 0.5,
        "lines": {k: F(v, n) for k, v in by_line.items()},
    }


if __name__ == "__main__":
    e = exact()
    print("outcomes:", e["outcomes"])
    print("RTP: %s = %.4f%%" % (e["rtp"], float(e["rtp"]) * 100))
    print("hit rate: %s = %.4f" % (e["hit_rate"], float(e["hit_rate"])))
    print("big win (>= 40x): %s = 1 in %.1f" % (e["big_win_rate"], 1 / float(e["big_win_rate"])))
    print("standard deviation per 1-coin spin: %.4f" % e["sd_per_spin"])
    for line, p in sorted(e["lines"].items(), key=lambda kv: -kv[1]):
        print("  %-22s %-10s %.6f" % (line, p, float(p)))
