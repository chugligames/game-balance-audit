"""Tests candidate rule fixes quoted in REPORT.md. Usage: python3 fixes.py [games]"""
import sys

from experiments import fmt_seats, run

G = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

SEAT_VARIANTS = [
    ("As written", {}),
    ("Finish the round", {"finish_round": True}),
    ("Hands 3/4/4/5 by seat", {"hand": [3, 4, 4, 5]}),
    ("Hands 3/4/4/5 + finish round", {"hand": [3, 4, 4, 5], "finish_round": True}),
    ("Hands 3/4/5/6 + finish round", {"hand": [3, 4, 5, 6], "finish_round": True}),
]

print("## Seat fixes: seat win rates, mirror matches (%d games each)" % G)
for label, rules in SEAT_VARIANTS:
    print("\n### " + label)
    for n in (2, 3, 4):
        for s in ("Greedy", "QuickPairs", "Denier"):
            r = run(n, [s] * n, G, seed=n * 31, rules=rules)
            print("n=%d %-10s %s   first-seat edge %+.1f pts" % (
                n, s, fmt_seats(r), 100 * (r["seat"][0] - 1.0 / n)), flush=True)

COIN_VARIANTS = [
    ("As written", {}),
    ("Flatter stacks", {"coins": {
        "Rice": [4, 3, 3, 2, 2, 1], "Lentils": [5, 4, 3, 3, 2], "Cloth": [5, 4, 3, 2, 1],
        "Spice": [6, 5, 4, 3], "Saffron": [7, 6, 5, 5]}}),
]
print("\n## Strategy diversity: rotated-seat head-to-head win rate of X vs Greedy, 2p and 4p")
for label, rules in COIN_VARIANTS:
    out = []
    for s in ("Cheap", "BigSale", "Saffron", "QuickPairs", "Denier"):
        for n in (2, 4):
            r = run(n, [s] + ["Greedy"] * (n - 1), G, seed=5, rules=rules, rotate=True)
            out.append("%s(%dp) %.0f%%" % (s, n, 100 * r["strat"][s] / G))
    print("%-16s %s" % (label, ", ".join(out)), flush=True)
