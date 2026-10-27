"""Exact enumeration of all 12^3 outcomes for Ladoo Spin. Usage: python3 enumerate.py reels.csv"""
import csv, sys, itertools
from collections import Counter
from fractions import Fraction
rows = list(csv.DictReader(open(sys.argv[1])))
reels = [[r[f"reel_{i}"] for r in rows] for i in (1, 2, 3)]
SWEETS = {"LADOO", "DIYA", "CHAI", "MANGO"}
TRIPLE = {"LADOO": 200, "DIYA": 50, "CHAI": 25, "MANGO": 10}

def pays(a, b, c):
    """All paytable lines the centre line qualifies for; highest one counts."""
    wins = []
    if a == b == c and a in TRIPLE: wins.append((TRIPLE[a], f"{a} x3"))
    if {a, b, c} <= SWEETS: wins.append((2, "any three sweets"))
    if a == b == "CHILLI": wins.append((5, "CHILLI CHILLI reels 1+2"))
    if a == "CHILLI": wins.append((1, "CHILLI reel 1"))
    return max(wins) if wins else (0, "no win")

N = 12 ** 3
hits = Counter(); paysum = Counter()
dist = Counter()
for a, b, c in itertools.product(*reels):
    p, name = pays(a, b, c)
    hits[name] += 1; paysum[name] += p; dist[p] += 1
total = sum(paysum.values())
print(f"{'line':28}{'hits':>6}{'prob':>10}{'rtp':>9}")
for k in sorted(hits, key=lambda k: -paysum[k]):
    print(f"{k:28}{hits[k]:>6}{hits[k]/N:>10.6f}{paysum[k]/N:>9.4f}")
print("RTP", total, "/", N, "=", total / N)
hit = N - hits["no win"]
print("hit rate", hit, "/", N, "=", hit / N, " 1 in", N / hit)
big = sum(n for p, n in dist.items() if p >= 40)
print("big wins (>=40x)", big, "/", N, ("1 in %.0f" % (N / big)) if big else "never")
mean = Fraction(total, N)
var = sum(n * (p - mean) ** 2 for p, n in dist.items()) / N
print("pay distribution", sorted(dist.items()), "SD per unit bet", float(var) ** 0.5)
for i, r in enumerate(reels, 1): print(f"reel {i}", Counter(r))
