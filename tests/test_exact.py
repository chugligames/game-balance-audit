"""The known-answer examples: the exact maths in evals/reference must match the example
files, and a fixed-seed simulation must land within its 95% interval of the exact value."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "evals", "reference")
ANALYZE = os.path.join(ROOT, "skills", "game-balance-audit", "scripts", "analyze.py")
sys.path.insert(0, os.path.join(REF, "tiny-slot"))
import exact as slot  # noqa: E402

sys.path.pop(0)
del sys.modules["exact"]
sys.path.insert(0, os.path.join(REF, "loot-drops"))
import exact as loot  # noqa: E402


class ExactAnswers(unittest.TestCase):
    def test_slot_by_enumeration(self):
        e = slot.exact()
        self.assertEqual(e["outcomes"], 1728)
        self.assertEqual(e["rtp"], F(449, 432))
        self.assertEqual(e["hit_rate"], F(67, 216))
        self.assertEqual(e["big_win_rate"], F(5, 1728))

    def test_slot_sheet_total_is_the_reel_1_shortcut(self):
        # The sheet's 96.0% is what you get if every reel were reel 1: the planted mistake.
        with open(os.path.join(ROOT, "examples", "tiny-slot", "paytable.csv")) as f:
            total = [line for line in f if line.startswith('"TOTAL RTP"')][0]
        self.assertAlmostEqual(float(total.strip().split(",")[-1]), 553 / 576, places=4)

    def test_pity_distribution(self):
        e = loot.exact()
        self.assertAlmostEqual(float(e["mean"]), 69.499537, places=5)
        self.assertAlmostEqual(float(e["beyond_90"]), 0.00041218, places=7)
        self.assertEqual(e["last"], 91)
        self.assertEqual(sum(loot.distribution()), 1)


@unittest.skipIf(shutil.which("node") is None, "needs Node")
class SimulationAgrees(unittest.TestCase):
    def check(self, name, runs):
        here = os.path.join(REF, name)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "runs.jsonl")
            subprocess.run(["node", os.path.join(here, "sim.mjs"), "--runs", str(runs), "--scenario", "baseline", "--out", out],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run([sys.executable, ANALYZE, os.path.join(here, "audit.json"), out, "--out", os.path.join(tmp, "res")],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with open(os.path.join(tmp, "res", "summary.json")) as f:
                exact = json.load(f)["exact"]
        self.assertTrue(exact)
        for e in exact:
            self.assertTrue(e["agrees"], "%s: simulated %s ± %s, exact %s" % (e["name"], e["simulated"], e["pm"], e["exact"]))

    def test_slot(self):
        self.check("tiny-slot", 40)

    def test_loot(self):
        self.check("loot-drops", 100)


if __name__ == "__main__":
    unittest.main()
