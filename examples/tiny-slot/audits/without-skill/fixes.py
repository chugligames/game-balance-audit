"""Search simple paytable edits that bring exact RTP to ~96% while keeping hit rate and big-win cadence."""
import itertools
# hit counts per line from enumerate.py (exact, out of 1728)
H = {"LADOO": 1, "DIYA": 4, "CHAI": 2, "MANGO": 36, "SWEETS": 349, "CC": 36, "C1": 108}
base = {"LADOO": 200, "DIYA": 50, "CHAI": 25, "MANGO": 10, "SWEETS": 2, "CC": 5, "C1": 1}
res = []
for mango, cc, diya, chai in itertools.product(range(5, 11), range(2, 6), (40, 45, 50), (20, 25)):
    p = dict(base, MANGO=mango, CC=cc, DIYA=diya, CHAI=chai)
    rtp = sum(H[k] * p[k] for k in H) / 1728
    changes = sum(p[k] != base[k] for k in p)
    if 0.95 <= rtp <= 0.965 and changes <= 2:
        res.append((changes, abs(rtp - .96), rtp, {k: v for k, v in p.items() if v != base[k]}))
for r in sorted(res, key=lambda r: (r[0], r[1]))[:10]: print(f"{r[2]:.4f}", r[3])
