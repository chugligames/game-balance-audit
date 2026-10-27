"""Exact odds for the Royal Chest, as fractions, transcribed from drops.js."""
from fractions import Fraction as F
import json, sys

def chances(base_l=F(4,1000), soft_from=76, step=F(5,100), hard=90, hard_op='>'):
    def p(n):
        if (n > hard) if hard_op == '>' else (n >= hard): return F(1)
        if n >= soft_from: return min(F(1), base_l + step * (n - soft_from))
        return base_l
    return p

def first_legendary(p, limit=400):
    dist, surv = {}, F(1)
    for n in range(1, limit + 1):
        q = p(n); dist[n] = surv * q; surv *= 1 - q
        if surv == 0: break
    return dist

def stats(dist):
    mean = sum(n * q for n, q in dist.items())
    cum, med, p90 = F(0), None, None
    for n in sorted(dist):
        cum += dist[n]
        if med is None and cum >= F(1, 2): med = n
        if p90 is None and cum >= F(9, 10): p90 = n
    tail = lambda k: sum(q for n, q in dist.items() if n > k)
    return dict(mean=mean, median=med, p90=p90, longest=max(dist), rate=1 / mean,
                over60=tail(60), over75=tail(75), over90=tail(90), within90=1 - tail(90))

def epic_rate(p, base_e=F(6,100), epic_pity=10):
    # Renewal-reward over one legendary cycle: expected epics per cycle / expected pulls per cycle.
    # State within a cycle: e = sinceEpic before this pull. Track probability mass over e.
    mass = {0: F(1)}; epics = F(0); pulls = F(0); n = 0
    while mass:
        n += 1; q = p(n); new = {}
        for e, m in mass.items():
            pulls += m
            e1 = e + 1
            rest = m * (1 - q)  # no legendary
            if rest == 0: continue
            if e1 >= epic_pity:
                epics += rest; new[0] = new.get(0, 0) + rest
            else:
                epics += rest * base_e; new[0] = new.get(0, 0) + rest * base_e
                new[e1] = new.get(e1, 0) + rest * (1 - base_e)
        mass = {k: v for k, v in new.items() if v}
    return epics / pulls

if __name__ == '__main__':
    out = {}
    variants = {
        'baseline': dict(),
        'hard pity >= 90': dict(hard_op='>='),
    }
    for name, kw in variants.items():
        p = chances(**kw); s = stats(first_legendary(p)); s['epicRate'] = epic_rate(p)
        out[name] = s
        print(f"\n== {name}")
        for k, v in s.items():
            print(f"  {k:10s} {v if isinstance(v,int) else f'{float(v):.6f}'}" + (f"  ({v})" if isinstance(v,F) and v.denominator < 10**6 else ''))
