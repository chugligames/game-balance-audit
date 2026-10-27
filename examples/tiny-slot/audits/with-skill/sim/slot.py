"""Ladoo Spin rules, written from reels.csv, paytable.csv and README.md.
Every reel stop equally likely; centre line only; only the highest win pays."""
import csv, os
from fractions import Fraction
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.normpath(os.path.join(HERE, "..", ".."))
SWEETS = {"LADOO", "DIYA", "CHAI", "MANGO"}   # as listed on the paytable row (DIYA included)


def load_reels(path=os.path.join(GAME, "reels.csv")):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return [[r["reel_%d" % i] for r in rows] for i in (1, 2, 3)]


# Pays, per coin bet. Keys are params so a what-if can change any of them.
PAYS = {"LLL": 200, "DDD": 50, "CCC": 25, "MMM": 10, "SWEETS": 2, "CHILLI2": 5, "CHILLI1": 1}
LABELS = {"LLL": "LADOO LADOO LADOO", "DDD": "DIYA DIYA DIYA", "CCC": "CHAI CHAI CHAI",
          "MMM": "MANGO MANGO MANGO", "SWEETS": "any three sweets", "CHILLI2": "CHILLI CHILLI on reels 1-2",
          "CHILLI1": "CHILLI on reel 1 only", None: "no win"}


def wins(line, pays=PAYS):
    """All paytable lines the centre line matches (key, multiplier)."""
    a, b, c = line
    out = []
    if a == b == c:
        k = {"LADOO": "LLL", "DIYA": "DDD", "CHAI": "CCC", "MANGO": "MMM"}.get(a)
        if k:
            out.append(k)
    if a in SWEETS and b in SWEETS and c in SWEETS:
        out.append("SWEETS")
    if a == "CHILLI" and b == "CHILLI":
        out.append("CHILLI2")
    if a == "CHILLI":
        out.append("CHILLI1")   # 'reel 1 only' read as 'CHILLI on reel 1, line pays nothing better'
    return [(k, pays[k]) for k in out]


def evaluate(line, pays=PAYS):
    """The single paying combination (highest win only) and its multiplier."""
    ws = wins(line, pays)
    if not ws:
        return None, 0
    return max(ws, key=lambda kv: kv[1])


def exact(reels, pays=PAYS, big=40):
    """Enumerate every outcome. Returns fractions."""
    n = len(reels[0]) * len(reels[1]) * len(reels[2])
    counts = Counter()
    ev = ev2 = Fraction(0)
    for a in reels[0]:
        for b in reels[1]:
            for c in reels[2]:
                k, m = evaluate((a, b, c), pays)
                counts[k] += 1
    p = {k: Fraction(v, n) for k, v in counts.items()}
    rtp = sum(p[k] * (pays[k] if k else 0) for k in p)
    ex2 = sum(p[k] * (pays[k] if k else 0) ** 2 for k in p)
    hit = 1 - p.get(None, 0)
    bigp = sum(p[k] for k in p if k and pays[k] >= big)
    return {"n": n, "counts": counts, "p": p, "rtp": rtp, "hit": hit, "big": bigp,
            "sd": (ex2 - rtp ** 2) ** 0.5 if False else float(ex2 - rtp ** 2) ** 0.5}
