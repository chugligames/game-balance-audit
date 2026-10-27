#!/usr/bin/env python3
"""Turn simulation rows (JSONL) into balance findings.

    python3 analyze.py audit.json runs/*.jsonl [--out results]

audit.json says what the designer wants from each metric (see references/audit-config.md).
The script:
  1. summarises every numeric metric per scenario, profile and segment (mean, p10, p50, p90);
  2. runs the checks the config asks for and lists flags, most severe first;
  3. compares every what-if scenario with the baseline: which flags it fixes, which it
     introduces, and how the configured metrics move;
  4. writes <out>/summary.md, <out>/summary.json and <out>/charts.html.

Python 3.7+, standard library only. Rows are plain JSON objects; reserved keys are
scenario, profile and run (added by sim-kit) plus the segment field named in the config.
Numbers and booleans are metrics; strings are labels you can group by.
"""

import argparse
import html
import json
import math
import os
import re
import sys
from collections import OrderedDict

SEVERITY = {"high": 0, "medium": 1, "low": 2, "info": 3}
RESERVED = {"scenario", "profile", "run"}


# ── Loading and basic statistics ─────────────────────────────────────────────


def load_rows(paths):
    rows = []
    for path in paths:
        with open(path) as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError as e:
                    raise SystemExit("%s:%d is not JSON (%s)" % (path, n, e))
    if not rows:
        raise SystemExit("no rows in %s" % ", ".join(paths))
    return rows


def num(v):
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v)):
        return float(v)
    return None


def quantile(sorted_xs, q):
    if not sorted_xs:
        return None
    pos = (len(sorted_xs) - 1) * q
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(sorted_xs) - 1)
    return sorted_xs[lo] + (sorted_xs[hi] - sorted_xs[lo]) * (pos - lo)


def stats(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    n = len(xs)
    mean = sum(xs) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / (n - 1)) if n > 1 else 0.0
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "min": xs[0],
        "p10": quantile(xs, 0.1),
        "p50": quantile(xs, 0.5),
        "p90": quantile(xs, 0.9),
        "max": xs[-1],
    }


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def fmt(x, digits=None):
    if x is None:
        return "–"
    if isinstance(x, str):
        return x
    if digits is None:
        a = abs(x)
        digits = 0 if a >= 100 else 1 if a >= 10 else 2
    return ("%." + str(digits) + "f") % x


def pct(x, signed=False):
    if x is None:
        return "–"
    if isinstance(x, float) and math.isinf(x):
        return "+∞" if x > 0 else "−∞"
    s = "%+.0f%%" if signed else "%.0f%%"
    return (s % (x * 100)).replace("-", "−")


# ── The data, indexed by scenario / profile / segment ────────────────────────


class Data:
    def __init__(self, rows, cfg):
        self.rows = rows
        self.cfg = cfg
        self.seg = cfg.get("segment")
        self.baseline = cfg.get("baseline", "baseline")
        self.scenarios = self._order([r.get("scenario", "baseline") for r in rows], [self.baseline])
        self.profiles = self._order([r.get("profile", "default") for r in rows], cfg.get("profiles", []))
        segs = [r.get(self.seg, "all") if self.seg else "all" for r in rows]
        self.segments = self._segments(segs, cfg.get("segment_order"))
        self.cells = {}
        for r in rows:
            key = (r.get("scenario", "baseline"), r.get("profile", "default"), r.get(self.seg, "all") if self.seg else "all")
            self.cells.setdefault(key, []).append(r)
        skip = RESERVED | ({self.seg} if self.seg else set())
        self.metrics = []
        self.labels = []
        seen = set()
        for r in rows:
            for k, v in r.items():
                if k in skip or k in seen:
                    continue
                seen.add(k)
                (self.labels if isinstance(v, str) else self.metrics).append(k)
        self.metrics = [m for m in self.metrics if any(num(r.get(m)) is not None for r in rows)]
        if self.baseline not in self.scenarios:
            raise SystemExit('no rows for baseline scenario "%s" (have: %s)' % (self.baseline, ", ".join(self.scenarios)))

    @staticmethod
    def _order(values, first):
        out = [v for v in first if v in values]
        for v in values:
            if v not in out:
                out.append(v)
        return out

    @staticmethod
    def _segments(values, given):
        if given:
            return list(given) + [v for v in OrderedDict.fromkeys(values) if v not in given]
        uniq = list(OrderedDict.fromkeys(values))
        if all(num(v) is not None for v in uniq):
            return sorted(uniq, key=float)
        return uniq

    def segs_in(self, spec):
        """spec: None (all), [lo, hi] for numeric segments, or a list of segment values."""
        if spec is None:
            return list(self.segments)
        if isinstance(spec, list) and len(spec) == 2 and all(num(s) is not None for s in spec) and all(num(s) is not None for s in self.segments):
            lo, hi = float(spec[0]), float(spec[1])
            return [s for s in self.segments if lo <= float(s) <= hi]
        return [s for s in self.segments if s in spec]

    def values(self, scenario, profile, seg, metric):
        profiles = self.profiles if profile is None else [profile]
        out = []
        for p in profiles:
            for r in self.cells.get((scenario, p, seg), []):
                x = num(r.get(metric))
                if x is not None:
                    out.append(x)
        return out

    def stat(self, scenario, profile, seg, metric, which="mean", cond=None):
        xs = self.values(scenario, profile, seg, metric)
        if not xs:
            return None
        if which == "rate":
            return sum(1 for x in xs if cond(x)) / len(xs)
        return stats(xs)[which]

    def series(self, scenario, profile, metric, segs, which="mean"):
        return [(s, self.stat(scenario, profile, s, metric, which)) for s in segs]


# ── Checks ───────────────────────────────────────────────────────────────────

COND = re.compile(r"^\s*(<=|>=|==|!=|<|>)\s*(-?[\d.]+)\s*$")


def parse_cond(text):
    m = COND.match(str(text))
    if not m:
        raise SystemExit('cannot read condition "%s" (use e.g. "<= 0" or "> 2")' % text)
    op, thr = m.group(1), float(m.group(2))
    return {
        "<=": lambda x: x <= thr,
        ">=": lambda x: x >= thr,
        "<": lambda x: x < thr,
        ">": lambda x: x > thr,
        "==": lambda x: x == thr,
        "!=": lambda x: x != thr,
    }[op], thr


def seg_name(data, s):
    return "%s %s" % (data.seg or "segment", s)


def flag(out, kind, severity, metric, scenario, profile, message, part="", **evidence):
    """part tells apart two flags of one kind on one metric (e.g. two different targets)."""
    out.append(
        {
            "id": "%s:%s:%s:%s" % (kind, metric, part, profile or "all"),
            "part": part,
            "kind": kind,
            "severity": severity,
            "metric": metric,
            "scenario": scenario,
            "profile": profile,
            "message": message,
            "evidence": evidence,
        }
    )


def check_shape(data, scenario, metric, mcfg, out):
    expect = mcfg.get("expect")
    if expect not in ("rise", "fall", "steady"):
        return
    label = mcfg.get("label", metric)
    segs = data.segs_in(mcfg.get("segments"))
    if len(segs) < 3:
        return
    for profile in data.profiles:
        ser = [(s, v) for s, v in data.series(scenario, profile, metric, segs) if v is not None]
        if len(ser) < 3:
            continue
        names = [s for s, _ in ser]
        vals = [v for _, v in ser]
        n = len(vals)
        scale = mean([abs(v) for v in vals]) or 1.0
        if expect == "steady":
            m = mean(vals)
            sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1))
            cv = sd / abs(m) if m else 0.0
            if cv > mcfg.get("tolerance", 0.15):
                flag(out, "unsteady", "medium", metric, scenario, profile,
                     "%s swings by %s (coefficient of variation) across %ss; expected steady" % (label, pct(cv), data.seg or "segment"),
                     cv=cv, values=ser)
            continue
        sign = 1 if expect == "rise" else -1
        v = [sign * x for x in vals]
        k = max(1, n // 3)
        first, last = mean(v[:k]), mean(v[-k:])
        growth = (last - first) / abs(first) if first else (float("inf") if last > first else 0.0)
        want = mcfg.get("min_growth", 0.25)
        word = "rises" if expect == "rise" else "falls"
        unit = data.seg or "segment"
        shaped = growth >= want
        if not shaped:
            if growth < -0.05:
                kind, sev = "reversed", "high"
                msg = "%s %s from the first third of %ss (%s) to the last third (%s): the opposite of what the design expects" % (
                    label, "falls" if expect == "rise" else "rises", unit, fmt(sign * first), fmt(sign * last))
            else:
                kind, sev = "flat", "medium"
                msg = "%s %s by only %s from the first third of %ss (%s) to the last third (%s); the design expects at least %s" % (
                    label, word, ("%.1f%%" % (max(growth, 0.0) * 100)), unit, fmt(sign * first), fmt(sign * last), pct(want))
            flag(out, kind, sev, metric, scenario, profile, msg,
                 growth=growth, first_third=sign * first, last_third=sign * last, values=ser)
        total = v[-1] - v[0]
        if shaped and total > 0 and n >= 6:
            q = max(1, int(round(n * 0.25)))
            early = (max(v[: q + 1]) - v[0]) / total
            if early > mcfg.get("front_load", 0.6):
                flag(out, "front-loaded", "medium", metric, scenario, profile,
                     "%s: %s of the whole change has happened by %s, the first quarter" % (label, pct(early), seg_name(data, names[q])),
                     share=early, values=ser)
        steps = [v[i + 1] - v[i] for i in range(n - 1)]
        floor = max(0.1 * scale, 1e-9)
        rel = lambda i: steps[i] / max(abs(v[i]), floor)
        move = lambda i: "%s→%s (%s → %s)" % (names[i], names[i + 1], fmt(vals[i]), fmt(vals[i + 1]))
        breathers = set(mcfg.get("breathers", []))
        dip = mcfg.get("dip", 0.15)
        dips = [move(i) for i in range(n - 1) if -rel(i) > dip and names[i + 1] not in breathers]
        if dips:
            flag(out, "dips", "low", metric, scenario, profile,
                 "%s goes against the expected direction (%s) by more than %s at %ss %s"
                 % (label, expect, pct(dip), data.seg or "segment", ", ".join(dips[:6]) + (" …" if len(dips) > 6 else "")),
                 dips=dips)
        abs_steps = sorted(abs(x) for x in steps)
        med = quantile(abs_steps, 0.5) or 0.0
        jumps = [move(i) for i in range(n - 1) if steps[i] > max(3 * med, 1e-9) and rel(i) > mcfg.get("spike", 0.25)]
        if jumps:
            flag(out, "spike", "medium", metric, scenario, profile,
                 "%s %s sharply at %ss %s, more than 3× a typical step" % (label, "jumps up" if expect == "rise" else "drops", data.seg or "segment", ", ".join(jumps)),
                 jumps=jumps)
        run, longest, at = 0, 0, None
        for i, st in enumerate(steps):
            run = run + 1 if abs(st) <= 0.03 * scale else 0
            if run > longest:
                longest, at = run, i
        if longest >= mcfg.get("plateau", 3):
            flag(out, "plateau", "low", metric, scenario, profile,
                 "%s barely changes for %d %ss in a row (%s to %s)" % (label, longest + 1, data.seg or "segment", names[at - longest + 1], names[at + 1]),
                 length=longest + 1)


def check_binds(data, scenario, metric, mcfg, out):
    if "binds" not in mcfg:
        return
    cond, thr = parse_cond(mcfg["binds"])
    label = mcfg.get("label", metric)
    segs = data.segs_in(mcfg.get("segments"))
    lo, hi = mcfg.get("binds_range", [0.01, 0.9])
    for profile in data.profiles:
        xs = [x for s in segs for x in data.values(scenario, profile, s, metric)]
        if not xs:
            continue
        rate = sum(1 for x in xs if cond(x)) / len(xs)
        per = [(s, data.stat(scenario, profile, s, metric, "rate", cond)) for s in segs]
        if rate < lo:
            closest = min(xs) if ">" not in mcfg["binds"] else max(xs)
            how = "never happens in any of the %ss" % (data.seg or "row") if rate == 0 else "happens in only %s of %ss" % (pct(rate), data.seg or "row")
            flag(out, "never-binds", "high" if rate == 0 else "medium", metric, scenario, profile,
                 "%s %s %s, so this limit puts no pressure on the player (closest it gets: %s)"
                 % (label, mcfg["binds"].strip(), how, fmt(closest)),
                 rate=rate, closest=closest, per_segment=per)
        elif rate > hi:
            flag(out, "always-binds", "medium", metric, scenario, profile,
                 "%s %s in %s of %ss: the limit is hit almost all the time" % (label, mcfg["binds"].strip(), pct(rate), data.seg or "row"),
                 rate=rate, per_segment=per)


def interval(xs, which):
    """95% interval for a mean or a rate, so a miss inside sampling noise isn't called a miss."""
    n = len(xs)
    if which != "mean" or n < 2:
        return None
    m = sum(xs) / n
    if all(x in (0.0, 1.0) for x in xs):
        return wilson(sum(xs), n)
    h = 1.96 * stats(xs)["sd"] / math.sqrt(n)
    return (m - h, m + h)


def check_targets(data, scenario, cfg, out):
    for t in cfg.get("targets", []):
        metric = t["metric"]
        mcfg = cfg.get("metrics", {}).get(metric, {})
        label = t.get("label") or mcfg.get("label", metric)
        which = t.get("stat", "mean")
        cond = parse_cond(mcfg["binds"])[0] if which == "rate" else None
        segs = data.segs_in(t.get("segments"))
        profiles = [t["profile"]] if t.get("profile") else data.profiles
        lo_t, hi_t = t.get("min", -float("inf")), t.get("max", float("inf"))
        for profile in profiles:
            if profile not in data.profiles:
                continue
            clear, close = [], []
            for s in segs:
                x = data.stat(scenario, profile, s, metric, which, cond)
                if x is None or lo_t <= x <= hi_t:
                    continue
                ci = interval(data.values(scenario, profile, s, metric), which)
                if ci and ci[1] >= lo_t and ci[0] <= hi_t:
                    close.append((s, x))
                else:
                    clear.append((s, x))
            if not clear and not close:
                continue
            want = "%s–%s" % (fmt(t.get("min")), fmt(t.get("max"))) if "min" in t and "max" in t else ("≥ %s" % fmt(t["min"]) if "min" in t else "≤ %s" % fmt(t["max"]))
            one = (lambda s, x: fmt(x)) if not data.seg else (lambda s, x: "%s: %s" % (s, fmt(x)))
            shown = ", ".join(one(s, x) for s, x in clear[:8]) + (" …" if len(clear) > 8 else "")
            if close:
                shown += ("; " if shown else "") + "borderline (inside sampling noise, run more): " + ", ".join(one(s, x) for s, x in close[:8])
            count = " (missed in %d of %d %ss)" % (len(clear) + len(close), len(segs), data.seg) if data.seg else ""
            flag(out, "off-target", t.get("severity", "high") if clear else "low", metric, scenario, profile,
                 "%s: %s %s, target %s%s" % (label, which, shown, want, count),
                 part=label, target=t, misses=clear + close, clear=clear, borderline=close)


def group_table(data, scenario, g):
    metric, by = g["metric"], g["by"]
    profiles = g.get("profiles") or ([g["profile"]] if g.get("profile") else data.profiles)
    vals = OrderedDict()
    for p in profiles:
        for s in data.segments:
            for r in data.cells.get((scenario, p, s), []):
                x = num(r.get(metric))
                if x is None or r.get(by) is None:
                    continue
                vals.setdefault(r.get(by), []).append(x)
    keys = sorted(vals, key=lambda k: (num(k) is None, num(k) if num(k) is not None else str(k)))
    fair = g.get("fair", "even")
    fair = 1.0 / len(keys) if fair == "even" and keys else float(fair) if fair != "even" else None
    table = []
    for k in keys:
        xs = vals[k]
        n = len(xs)
        m = sum(xs) / n
        if all(x in (0.0, 1.0) for x in xs):
            lo, hi = wilson(sum(xs), n)
        else:
            st = stats(xs)
            h = 1.96 * st["sd"] / math.sqrt(n) if n > 1 else 0
            lo, hi = m - h, m + h
        table.append({"group": k, "mean": m, "lo": lo, "hi": hi, "n": n})
    return table, fair


def check_groups(data, scenario, cfg, out):
    for g in cfg.get("groups", []):
        table, fair = group_table(data, scenario, g)
        if fair is None:
            continue
        tol = g.get("tolerance", 0.03)
        label = g.get("label", "%s by %s" % (g["metric"], g["by"]))
        for row in table:
            off = row["mean"] - fair
            if abs(off) > tol and (row["lo"] > fair or row["hi"] < fair):
                where = g.get("profile") or (", ".join(g["profiles"]) if g.get("profiles") else None)
                flag(out, "uneven", "high" if abs(off) > 2 * tol else "medium", g["metric"], scenario, where,
                     "%s: %s = %s has %s (95%% CI %s–%s, n=%d) against a fair %s ± %s"
                     % (label, g["by"], row["group"], fmt(row["mean"], 3), fmt(row["lo"], 3), fmt(row["hi"], 3), row["n"], fmt(fair, 3), fmt(tol, 3)),
                     part="%s · %s=%s" % (label, g["by"], row["group"]), group=row["group"], by=g["by"], value=row["mean"], fair=fair, table=table)


def check_skill(data, scenario, cfg, out):
    sk = cfg.get("skill")
    if not sk:
        return
    metric = sk["metric"]
    strong = mean([x for s in data.segments for x in data.values(scenario, sk["strong"], s, metric)])
    weak = mean([x for s in data.segments for x in data.values(scenario, sk["weak"], s, metric)])
    if strong is None or weak is None:
        return
    gap = strong - weak
    label = sk.get("label", metric)
    if gap < sk.get("min_gap", 0.1):
        flag(out, "luck-dominated", "medium", metric, scenario, None,
             "%s: the %s player averages %s and the %s player %s, a gap of only %s. Skill barely changes the result"
             % (label, sk["strong"], fmt(strong, 3), sk["weak"], fmt(weak, 3), fmt(gap, 3)),
             strong=strong, weak=weak, gap=gap)
    if "max_gap" in sk and gap > sk["max_gap"]:
        flag(out, "skill-wall", "medium", metric, scenario, None,
             "%s: %s averages %s against %s for %s, a gap of %s. Weaker players have little chance"
             % (label, sk["strong"], fmt(strong, 3), fmt(weak, 3), sk["weak"], fmt(gap, 3)),
             strong=strong, weak=weak, gap=gap)


def check_capped(data, scenario, out):
    n = sum(1 for (sc, _, _), rs in data.cells.items() if sc == scenario for r in rs if r.get("capped"))
    if n:
        flag(out, "capped", "high", "capped", scenario, None,
             "%d rows hit the simulation's step limit: the game got stuck or never ended for some bots" % n, rows=n)


def check_constant(data, scenario, cfg, out):
    for m in data.metrics:
        if m == "capped":
            continue
        xs = [x for (sc, _, _), rs in data.cells.items() if sc == scenario for r in rs for x in [num(r.get(m))] if x is not None]
        if xs and min(xs) == max(xs):
            flag(out, "constant", "info", m, scenario, None,
                 "%s is %s in every row: either it measures nothing here, or something never happens (which may be a finding)"
                 % (cfg.get("metrics", {}).get(m, {}).get("label", m), fmt(xs[0])), value=xs[0])


def run_checks(data, scenario):
    cfg = data.cfg
    out = []
    for metric, mcfg in cfg.get("metrics", {}).items():
        if metric not in data.metrics:
            continue
        check_shape(data, scenario, metric, mcfg, out)
        check_binds(data, scenario, metric, mcfg, out)
    check_targets(data, scenario, cfg, out)
    check_groups(data, scenario, cfg, out)
    check_skill(data, scenario, cfg, out)
    check_capped(data, scenario, out)
    check_constant(data, scenario, cfg, out)
    out.sort(key=lambda f: (SEVERITY[f["severity"]], f["metric"], str(f["profile"])))
    return out


# ── Comparing what-ifs with the baseline ─────────────────────────────────────


def gauge(f):
    """The one number that says how bad a flag is, to show how a what-if moved it."""
    e = f["evidence"]
    k = f["kind"]
    if k == "off-target":
        return len(e["clear"]), "clear misses"
    if k in ("never-binds", "always-binds"):
        return e["rate"], "rate"
    if k in ("flat", "reversed"):
        return e["growth"], "growth"
    if k == "uneven":
        return e["value"], "value"
    if k in ("luck-dominated", "skill-wall"):
        return e["gap"], "gap"
    if k == "dips":
        return len(e["dips"]), "dips"
    if k == "spike":
        return len(e["jumps"]), "jumps"
    return None, None


def compare(data, flags):
    base = {f["id"]: f for f in flags[data.baseline]}
    out = OrderedDict()
    for sc in data.scenarios:
        if sc == data.baseline:
            continue
        mine = {f["id"]: f for f in flags[sc]}
        moves = []
        for metric, mcfg in data.cfg.get("metrics", {}).items():
            if metric not in data.metrics:
                continue
            segs = data.segs_in(mcfg.get("segments"))
            k = max(1, len(segs) // 3)
            for p in data.profiles:
                b = [v for _, v in data.series(data.baseline, p, metric, segs)]
                w = [v for _, v in data.series(sc, p, metric, segs)]
                if not any(x is not None for x in w):
                    continue
                bm, wm = mean(b), mean(w)
                moves.append(
                    {
                        "metric": metric,
                        "profile": p,
                        "base": bm,
                        "whatif": wm,
                        "change": (wm - bm) / abs(bm) if bm else None,
                        "base_first": mean(b[:k]),
                        "base_last": mean(b[-k:]),
                        "whatif_first": mean(w[:k]),
                        "whatif_last": mean(w[-k:]),
                    }
                )
        still = []
        for i in mine:
            if i in base and mine[i]["severity"] != "info":
                f = dict(mine[i])
                f["before"], _ = gauge(base[i])
                f["after"], f["gauge"] = gauge(mine[i])
                still.append(f)
        out[sc] = {
            "fixed": [base[i] for i in base if i not in mine and base[i]["severity"] != "info"],
            "new": [mine[i] for i in mine if i not in base and mine[i]["severity"] != "info"],
            "still": still,
            "moves": moves,
        }
    return out


# ── Output ───────────────────────────────────────────────────────────────────


def merged(flags, profiles, focus=None):
    """One line per finding: the same check on the same metric for several profiles
    collapses into one, worded from the focus profile (or the most severe one)."""
    groups = OrderedDict()
    for f in flags:
        key = (f["kind"], f["metric"], f.get("part", ""))
        groups.setdefault(key, []).append(f)
    out = []
    for fs in groups.values():
        top = min(SEVERITY[f["severity"]] for f in fs)
        pick = [f for f in fs if SEVERITY[f["severity"]] == top]
        lead = next((f for f in pick if f["profile"] == focus), pick[0])
        who = [f["profile"] for f in fs if f["profile"]]
        if not who:
            where = "all"
        elif len(profiles) > 1 and set(who) == set(profiles):
            where = "%s (and every other profile)" % lead["profile"]
        elif len(who) > 1:
            where = "%s (also %s)" % (lead["profile"], ", ".join(w for w in who if w != lead["profile"]))
        else:
            where = who[0]
        out.append(dict(lead, where=where, profiles=who))
    out.sort(key=lambda f: SEVERITY[f["severity"]])
    return out


def md_flags(data, flags):
    rows = merged([f for f in flags if f["severity"] != "info"], data.profiles, data.cfg.get("focus_profile"))
    if not rows:
        return "No flags.\n"
    lines = ["| Severity | Check | Player profile | Finding |", "|---|---|---|---|"]
    for f in rows:
        lines.append("| %s | %s | %s | %s |" % (f["severity"], f["kind"], f["where"], f["message"].replace("|", "\\|")))
    return "\n".join(lines) + "\n"


def short(data, flags):
    rows = merged(flags, data.profiles, data.cfg.get("focus_profile"))
    out = []
    for f in rows:
        name = "%s on `%s`%s (%s)" % (f["kind"], f["metric"], " · " + f["part"] if f.get("part") else "", f["where"])
        if f.get("gauge") and f["before"] != f["after"]:
            show = (lambda x: pct(x)) if f["gauge"] in ("rate", "growth") else (lambda x: fmt(x, 3) if isinstance(x, float) else str(x))
            name += ": %s %s → %s" % (f["gauge"], show(f["before"]), show(f["after"]))
        out.append(name)
    return "; ".join(out)


def write_markdown(data, flags, cmp, path):
    cfg = data.cfg
    runs = {}
    for (sc, p, _), rs in data.cells.items():
        runs.setdefault((sc, p), set()).update(r.get("run") for r in rs)
    nruns = sorted({len(v) for v in runs.values()})
    L = ["# Balance summary: %s" % cfg.get("title", "game"), ""]
    L.append("%d rows · baseline `%s` + %d what-if scenario(s) · player profiles: %s · %s runs each"
             % (len(data.rows), data.baseline, len(data.scenarios) - 1, ", ".join(data.profiles), "/".join(map(str, nruns))))
    L += ["", "## Flags in the baseline", "", md_flags(data, flags[data.baseline])]
    info = [f for f in flags[data.baseline] if f["severity"] == "info"]
    if info:
        L += ["Never changes: " + "; ".join("`%s` = %s" % (f["metric"], fmt(f["evidence"]["value"])) for f in info), ""]

    if data.seg and len(data.segments) > 1:
        L += ["## Baseline by %s" % data.seg, "", "Mean per %s, with the 10th–90th percentile range in brackets." % data.seg, ""]
        shown = [m for m in cfg.get("metrics", {}) if m in data.metrics] or data.metrics[:6]
        for m in shown:
            mcfg = cfg.get("metrics", {}).get(m, {})
            note = []
            if mcfg.get("expect"):
                note.append("expected to %s" % mcfg["expect"])
            if mcfg.get("binds"):
                note.append("limit hit when %s" % mcfg["binds"].strip())
            L += ["### %s (`%s`)%s" % (mcfg.get("label", m), m, " · " + ", ".join(note) if note else ""), ""]
            L.append("| %s | %s |" % (data.seg, " | ".join(data.profiles)))
            L.append("|---|" + "---|" * len(data.profiles))
            for s in data.segments:
                cells = []
                for p in data.profiles:
                    xs = data.values(data.baseline, p, s, m)
                    st = stats(xs)
                    cells.append("–" if not st else "%s (%s–%s)" % (fmt(st["mean"]), fmt(st["p10"]), fmt(st["p90"])))
                L.append("| %s | %s |" % (s, " | ".join(cells)))
            L.append("")

    for g in cfg.get("groups", []):
        table, fair = group_table(data, data.baseline, g)
        L += ["## %s" % g.get("label", "%s by %s" % (g["metric"], g["by"])), ""]
        L += ["| %s | %s | 95%% CI | n |" % (g["by"], g["metric"]), "|---|---|---|---|"]
        for row in table:
            L.append("| %s | %s | %s–%s | %d |" % (row["group"], fmt(row["mean"], 3), fmt(row["lo"], 3), fmt(row["hi"], 3), row["n"]))
        if fair is not None:
            L += ["", "Fair value: %s ± %s." % (fmt(fair, 3), fmt(g.get("tolerance", 0.03), 3))]
        L.append("")

    if cmp:
        L += ["## What-ifs against the baseline", ""]
        for sc, c in cmp.items():
            L += ["### `%s`" % sc, ""]
            L.append("- **Fixes:** " + (short(data, c["fixed"]) or "nothing flagged in the baseline"))
            L.append("- **Introduces:** " + ("; ".join("%s (%s): %s" % (f["kind"], f["where"], f["message"]) for f in merged(c["new"], data.profiles, data.cfg.get("focus_profile"))) or "no new flags"))
            L.append("- **Still flagged:** " + (short(data, c["still"]) or "none"))
            by_metric = OrderedDict()
            for mv in c["moves"]:
                by_metric.setdefault(mv["metric"], []).append(mv)
            focus = data.cfg.get("focus_profile") or data.profiles[0]
            segmented = bool(data.seg) and len(data.segments) > 1
            table, same = [], []
            for metric, mvs in by_metric.items():
                if all(mv["base"] == mv["whatif"] for mv in mvs):
                    same.append(metric)
                    continue
                lead = next((mv for mv in mvs if mv["profile"] == focus), mvs[0])
                change = " · ".join("%s %s" % (mv["profile"], pct(mv["change"], True) if mv["change"] is not None else "%s → %s" % (fmt(mv["base"]), fmt(mv["whatif"]))) for mv in mvs)
                if segmented:
                    table.append("| %s | %s → %s | %s → %s | %s |" % (
                        metric, fmt(lead["base_first"]), fmt(lead["base_last"]), fmt(lead["whatif_first"]), fmt(lead["whatif_last"]), change))
                else:
                    table.append("| %s | %s | %s | %s |" % (metric, fmt(lead["base"]), fmt(lead["whatif"]), change))
            if table:
                head = "Baseline, %s (first third → last third)" % focus if segmented else "Baseline, %s" % focus
                L += ["", "| Metric | %s | What-if, %s | Change in the mean, by profile |" % (head, focus), "|---|---|---|---|"] + table
            if same:
                L += ["", "Unchanged: " + ", ".join("`%s`" % m for m in same) + "."]
            L.append("")
    with open(path, "w") as f:
        f.write("\n".join(L))


PALETTE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#666666", "#8C6D31"]


def nice_ticks(lo, hi, count=4):
    """Round tick values (1, 2, 2.5 or 5 × a power of ten) covering lo..hi."""
    span = (hi - lo) or abs(hi) or 1.0
    raw = span / count
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    start = math.floor(lo / step) * step
    ticks = []
    t = start
    while t <= hi + step * 0.999:
        ticks.append(round(t, 10))
        t += step
    return ticks


def svg_chart(title, segs, series, threshold=None, bands=(), width=640, height=240):
    """series: [(name, [(seg, value)], color, dashed)]; bands: [(first seg, last seg, min, max)].
    Inline SVG with point tooltips."""
    pad_l, pad_r, pad_t, pad_b = 48, 12, 28, 28
    vals = [v for _, pts, _, _ in series for _, v in pts if v is not None]
    if threshold is not None:
        vals.append(threshold)
    for b in bands:
        vals += [x for x in b[2:] if x is not None]
    if not vals:
        return ""
    lo, hi = min(vals), max(vals)
    if lo >= 0 and lo < 0.4 * hi:
        lo = 0.0
    ticks = nice_ticks(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    if hi == lo:
        hi = lo + 1
    n = len(segs)
    x = lambda i: pad_l + (width - pad_l - pad_r) * (i / max(1, n - 1))
    y = lambda v: pad_t + (height - pad_t - pad_b) * (1 - (v - lo) / (hi - lo))
    idx = {s: i for i, s in enumerate(segs)}
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (width, height, html.escape(title))]
    out.append('<text x="%d" y="16" class="t">%s</text>' % (pad_l, html.escape(title)))
    for v in ticks:
        out.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="g"/>' % (pad_l, width - pad_r, y(v), y(v)))
        out.append('<text x="%d" y="%.1f" class="a" text-anchor="end">%s</text>' % (pad_l - 6, y(v) + 4, ("%.2f" % v).rstrip("0").rstrip(".")))
    step = max(1, n // 12)
    for i, s in enumerate(segs):
        if i % step == 0 or i == n - 1:
            out.append('<text x="%.1f" y="%d" class="a" text-anchor="middle">%s</text>' % (x(i), height - 8, html.escape(str(s))))
    for b0, b1, bmin, bmax in bands:
        i0 = idx.get(b0, 0)
        i1 = idx.get(b1, n - 1)
        top = y(bmax if bmax is not None else hi)
        bot = y(bmin if bmin is not None else lo)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="band"><title>target %s–%s</title></rect>' % (x(i0) - 3, top, max(6, x(i1) - x(i0) + 6), bot - top, b0, b1))
    if threshold is not None:
        out.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="thr"><title>limit %s</title></line>' % (pad_l, width - pad_r, y(threshold), y(threshold), fmt(threshold)))
    for name, pts, color, dashed in series:
        coords = [(x(idx[s]), y(v), s, v) for s, v in pts if v is not None and s in idx]
        if not coords:
            continue
        d = " ".join("%s%.1f,%.1f" % ("M" if i == 0 else "L", cx, cy) for i, (cx, cy, _, _) in enumerate(coords))
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="2"%s/>' % (d, color, ' stroke-dasharray="5 4"' if dashed else ""))
        for cx, cy, s, v in coords:
            out.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"><title>%s · %s: %s</title></circle>' % (cx, cy, color, html.escape(name), html.escape(str(s)), fmt(v)))
    out.append("</svg>")
    legend = "".join('<span><i style="background:%s"></i>%s</span>' % (c, html.escape(nm)) for nm, _, c, _ in series)
    return '<figure>%s<figcaption>%s</figcaption></figure>' % ("".join(out), legend)


def write_charts(data, path):
    cfg = data.cfg
    if not data.seg or len(data.segments) < 2:
        return False
    metrics = [m for m in cfg.get("metrics", {}) if m in data.metrics]
    focus = cfg.get("focus_profile") or data.profiles[0]
    # Up to 8 lines stay readable: the baseline plus `chart_scenarios` from the config, else the first 7 what-ifs.
    picked = [sc for sc in cfg.get("chart_scenarios", []) if sc in data.scenarios and sc != data.baseline]
    shown = [data.baseline] + (picked or [sc for sc in data.scenarios if sc != data.baseline])[:7]
    parts = []
    for m in metrics:
        mcfg = cfg["metrics"][m]
        thr = parse_cond(mcfg["binds"])[1] if "binds" in mcfg else None
        bands = []
        for t in cfg.get("targets", []):
            if t["metric"] == m and t.get("stat", "mean") == "mean" and t.get("profile") in (None, focus):
                sg = data.segs_in(t.get("segments"))
                if sg:
                    bands.append((sg[0], sg[-1], t.get("min"), t.get("max")))
        label = mcfg.get("label", m)
        series = [(p, data.series(data.baseline, p, m, data.segments), PALETTE[i % len(PALETTE)], False) for i, p in enumerate(data.profiles)]
        parts.append(svg_chart("%s · baseline, by player profile" % label, data.segments, series, thr, bands))
        if len(shown) > 1:
            series = [(sc, data.series(sc, focus, m, data.segments), PALETTE[i % len(PALETTE)], i > 0) for i, sc in enumerate(shown)]
            parts.append(svg_chart("%s · what-ifs (%s player)" % (label, focus), data.segments, series, thr, bands))
    doc = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s balance charts</title><style>
:root{--bg:#fff;--fg:#1d1d1f;--muted:#6e6e73;--grid:#e5e5ea;--band:rgba(0,158,115,.10)}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#f2f2f7;--muted:#a1a1a6;--grid:#2c2c2e;--band:rgba(0,158,115,.18)}}
body{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif;margin:0 auto;max-width:720px;padding:16px}
figure{margin:0 0 28px}svg{width:100%%;height:auto}.t{fill:var(--fg);font-weight:600;font-size:13px}.a{fill:var(--muted);font-size:11px}
.g{stroke:var(--grid)}.thr{stroke:#D55E00;stroke-dasharray:3 3}.band{fill:var(--band)}
figcaption{display:flex;flex-wrap:wrap;gap:12px;color:var(--muted);font-size:12px}figcaption i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px}
</style></head><body><h1>%s</h1><p>Dashed orange line: the limit a constraint metric binds at. Green band: the designer's target. Hover a point for its value.</p>%s</body></html>""" % (
        html.escape(cfg.get("title", "Game")), html.escape(cfg.get("title", "Game")), "".join(parts))
    with open(path, "w") as f:
        f.write(doc)
    return True


def main():
    ap = argparse.ArgumentParser(description="Turn simulation rows into balance findings.")
    ap.add_argument("config", help="audit.json")
    ap.add_argument("runs", nargs="+", help="JSONL files written by the sim")
    ap.add_argument("--out", default="results", help="folder for summary.md, summary.json, charts.html")
    a = ap.parse_args()
    with open(a.config) as f:
        cfg = json.load(f)
    data = Data(load_rows(a.runs), cfg)
    missing = [m for m in cfg.get("metrics", {}) if m not in data.metrics]
    if missing:
        sys.stderr.write("warning: metrics in the config but not in any row: %s\n" % ", ".join(missing))
    flags = OrderedDict((sc, run_checks(data, sc)) for sc in data.scenarios)
    cmp = compare(data, flags)
    os.makedirs(a.out, exist_ok=True)
    write_markdown(data, flags, cmp, os.path.join(a.out, "summary.md"))
    charts = write_charts(data, os.path.join(a.out, "charts.html"))
    summary = {
        "title": cfg.get("title"),
        "segment": data.seg,
        "segments": data.segments,
        "scenarios": data.scenarios,
        "profiles": data.profiles,
        "flags": flags,
        "compare": cmp,
        "means": {
            sc: {p: {m: dict(data.series(sc, p, m, data.segments)) for m in data.metrics} for p in data.profiles}
            for sc in data.scenarios
        },
    }
    with open(os.path.join(a.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1, default=str)
    base = [f for f in flags[data.baseline] if f["severity"] != "info"]
    print("%d rows, %d scenario(s), %d profile(s), %d segment(s)" % (len(data.rows), len(data.scenarios), len(data.profiles), len(data.segments)))
    print("baseline flags: %d (%s)" % (len(base), ", ".join("%d %s" % (sum(1 for f in base if f["severity"] == s), s) for s in ("high", "medium", "low") if any(f["severity"] == s for f in base)) or "none"))
    focus = cfg.get("focus_profile")
    for f in merged(base, data.profiles, focus):
        print("  [%s] %s: %s" % (f["severity"], f["where"], f["message"]))
    for sc, c in cmp.items():
        print("%s: fixes %d, introduces %d, still %d (counted per profile)" % (sc, len(c["fixed"]), len(c["new"]), len(c["still"])))
    print("wrote %s/summary.md, summary.json%s" % (a.out, ", charts.html" if charts else ""))


if __name__ == "__main__":
    main()
