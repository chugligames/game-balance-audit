"""Unit tests for scripts/analyze.py (Python 3.7+, standard library only).
    python3 -m unittest discover -s tests -v"""
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "game-balance-audit", "scripts")
sys.path.insert(0, SCRIPTS)
import analyze as A  # noqa: E402


def rows(scenario, profile, values, metric="m", seg="day", runs=1, extra=None):
    out = []
    for run in range(runs):
        for i, v in enumerate(values):
            r = {"scenario": scenario, "profile": profile, "run": run, seg: i + 1, metric: v}
            r.update(extra or {})
            out.append(r)
    return out


class Statistics(unittest.TestCase):
    def test_quantile_interpolates(self):
        self.assertEqual(A.quantile([1, 2, 3, 4], 0.5), 2.5)
        self.assertEqual(A.quantile([7], 0.9), 7)

    def test_stats(self):
        st = A.stats([1, 2, 3, 4, 5])
        self.assertEqual(st["mean"], 3)
        self.assertAlmostEqual(st["sd"], math.sqrt(2.5))
        self.assertEqual((st["min"], st["max"]), (1, 5))

    def test_wilson_matches_known_interval(self):
        lo, hi = A.wilson(5, 10)
        self.assertAlmostEqual(lo, 0.2366, places=3)
        self.assertAlmostEqual(hi, 0.7634, places=3)

    def test_parse_cond(self):
        f, thr = A.parse_cond("<= 0")
        self.assertTrue(f(0) and not f(1))
        self.assertEqual(thr, 0)
        with self.assertRaises(SystemExit):
            A.parse_cond("about 3")


class Checks(unittest.TestCase):
    def data(self, rs, cfg):
        return A.Data(rs, cfg)

    def kinds(self, d, scenario="baseline"):
        return {f["kind"] for f in A.run_checks(d, scenario)}

    def test_flat_curve_is_flagged_and_rising_is_not(self):
        cfg = {"segment": "day", "metrics": {"m": {"expect": "rise"}}}
        flat = self.data(rows("baseline", "p", [10, 10.5, 10, 10.4, 10.2, 10.3]), cfg)
        self.assertIn("flat", self.kinds(flat))
        rising = self.data(rows("baseline", "p", [10, 12, 14, 16, 18, 20]), cfg)
        self.assertNotIn("flat", self.kinds(rising))

    def test_reversed_and_spike(self):
        cfg = {"segment": "day", "metrics": {"m": {"expect": "rise"}}}
        self.assertIn("reversed", self.kinds(self.data(rows("baseline", "p", [20, 18, 16, 14, 12, 10]), cfg)))
        self.assertIn("spike", self.kinds(self.data(rows("baseline", "p", [10, 11, 12, 13, 40, 41]), cfg)))

    def test_never_binds(self):
        cfg = {"segment": "day", "metrics": {"free": {"binds": "<= 0"}}}
        d = self.data(rows("baseline", "p", [30, 25, 20], metric="free"), cfg)
        self.assertIn("never-binds", self.kinds(d))

    def test_target_inside_noise_is_borderline(self):
        # 3 wins in 10 against a 0.4–0.6 target: a miss, but the interval overlaps the target
        rs = []
        for run in range(10):
            rs.append({"scenario": "baseline", "profile": "p", "run": run, "level": 1, "won": 1 if run < 3 else 0})
        cfg = {"segment": "level", "targets": [{"metric": "won", "min": 0.4, "max": 0.6}]}
        f = [x for x in A.run_checks(self.data(rs, cfg), "baseline") if x["kind"] == "off-target"]
        self.assertEqual(f[0]["severity"], "low")
        self.assertEqual(len(f[0]["evidence"]["borderline"]), 1)

    def test_uneven_seat_and_exclude(self):
        rs = []
        for run in range(400):
            rs.append({"scenario": "baseline", "profile": "t", "run": run, "seat": 1, "strategy": "a", "won": 1 if run % 10 < 7 else 0})
            rs.append({"scenario": "baseline", "profile": "t", "run": run, "seat": 2, "strategy": "ref", "won": 0 if run % 10 < 7 else 1})
        cfg = {"groups": [{"metric": "won", "by": "seat", "fair": "even", "tolerance": 0.03}]}
        self.assertIn("uneven", self.kinds(self.data(rs, cfg)))
        cfg = {"groups": [{"metric": "won", "by": "strategy", "fair": 0.5, "tolerance": 0.03, "exclude": ["ref"]}]}
        flags = [f for f in A.run_checks(self.data(rs, cfg), "baseline") if f["kind"] == "uneven"]
        self.assertEqual([f["evidence"]["group"] for f in flags], ["a"])

    def test_constant_metric_is_reported(self):
        d = self.data(rows("baseline", "p", [0, 0, 0], metric="sells"), {"segment": "day"})
        self.assertIn("constant", self.kinds(d))


class Goals(unittest.TestCase):
    def setUp(self):
        rs = []
        # baseline: 1 ad a day; "harder": 2 ads a day but 30% quit; "kinder": 0 ads
        for sc, ads, quit_every in (("baseline", 1, 0), ("harder", 2, 3), ("kinder", 0, 0)):
            for run in range(30):
                for day in range(1, 6):
                    rs.append({"scenario": sc, "profile": "p", "run": run, "day": day, "ads": ads,
                               "quit": 1 if quit_every and run % quit_every == 0 and day == 5 else 0})
        self.cfg = {
            "segment": "day",
            "goals": [{"name": "ads", "metric": "ads", "profile": "p", "direction": "max"}],
            "constraints": [{"name": "quit", "metric": "quit", "profile": "p", "aggregate": "any", "max": 0.2}],
        }
        self.data = A.Data(rs, self.cfg)

    def test_measure_sums_per_run(self):
        v, pm, n = A.measure(self.data, "harder", {"metric": "ads", "profile": "p"})
        self.assertEqual((v, n), (10.0, 30))
        v, _, _ = A.measure(self.data, "harder", {"metric": "quit", "aggregate": "any"})
        self.assertAlmostEqual(v, 10 / 30)

    def test_per_segment_then_min(self):
        v, _, n = A.measure(self.data, "harder", {"metric": "quit", "per": "segment", "aggregate": "max"})
        self.assertAlmostEqual(v, 10 / 30)
        self.assertEqual(n, 5)

    def test_scorecard_respects_constraints(self):
        card = A.scorecard(self.data)
        by = {r["scenario"]: r for r in card["rows"]}
        self.assertFalse(by["harder"]["ok"])  # more ads, but too many quit
        self.assertTrue(by["baseline"]["pareto"])  # best among those that keep the constraint
        self.assertFalse(by["kinder"]["pareto"])  # dominated by the baseline
        self.assertEqual(card["rows"][0]["scenario"], "baseline")

    def test_exact_check_agrees_and_disagrees(self):
        cfg = dict(self.cfg, exact=[{"name": "ads", "metric": "ads", "value": 5}, {"name": "wrong", "metric": "ads", "value": 6, "tolerance": 0.1}])
        out = {e["name"]: e for e in A.exact_checks(A.Data(self.data.rows, cfg))}
        self.assertTrue(out["ads"]["agrees"])
        self.assertFalse(out["wrong"]["agrees"])


class EndToEnd(unittest.TestCase):
    def test_cli_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs = os.path.join(tmp, "runs.jsonl")
            with open(runs, "w") as f:
                for r in rows("baseline", "p", [1, 2, 3, 4, 5, 6], runs=5) + rows("what-if", "p", [2, 4, 6, 8, 10, 12], runs=5):
                    f.write(json.dumps(r) + "\n")
            cfg = os.path.join(tmp, "audit.json")
            with open(cfg, "w") as f:
                json.dump({"segment": "day", "metrics": {"m": {"expect": "rise"}}, "goals": [{"name": "m", "metric": "m"}]}, f)
            out = subprocess.run([sys.executable, os.path.join(SCRIPTS, "analyze.py"), cfg, runs, "--out", os.path.join(tmp, "res")],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            for name in ("summary.md", "summary.json", "charts.html"):
                self.assertTrue(os.path.exists(os.path.join(tmp, "res", name)), name)
            with open(os.path.join(tmp, "res", "summary.json")) as f:
                summary = json.load(f)
            self.assertEqual(summary["scorecard"]["rows"][0]["scenario"], "what-if")


if __name__ == "__main__":
    unittest.main()
