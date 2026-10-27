"""Exact what-ifs: one lever at a time, hard pity fixed to >= 90 so the promise holds."""
from fractions import Fraction as F
from exact import chances, first_legendary, stats, epic_rate
def show(name, **kw):
    p = chances(**kw); s = stats(first_legendary(p))
    print(f"{name:42s} mean {float(s['mean']):6.2f} rate {float(s['rate'])*100:5.3f}% median {s['median']:3d} p90 {s['p90']:3d} longest {s['longest']:3d} P(>60) {float(s['over60'])*100:5.1f}% P(>90) {float(s['over90'])*100:.3f}%  gems/leg {float(s['mean'])*160:,.0f}")
show('baseline')
show('fix: hard pity >= 90', hard_op='>=')
for b in [6,7,8,9,10]:
    show(f'base {b/10}%', base_l=F(b,1000), hard_op='>=')
for sf in [70,68,66,65,64,62]:
    show(f'soft pity from {sf}', soft_from=sf, hard_op='>=')
for st in [6,8,10]:
    for sf in [66,70]:
        show(f'soft from {sf} step {st}%', soft_from=sf, step=F(st,100), hard_op='>=')
