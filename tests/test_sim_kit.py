"""Unit tests for scripts/sim_kit.py."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "game-balance-audit", "scripts"))
import sim_kit as K  # noqa: E402


class Toy:
    """Take the top card (points) or pass, 2 players, 6 turns, hidden deck."""

    def start(self, r):
        deck = list(range(1, 11))
        r.shuffle(deck)
        return {"deck": deck, "score": [0, 0], "turn": 0}

    def actions(self, s):
        return ["take", "pass"]

    def apply(self, s, a, r):
        s = {"deck": list(s["deck"]), "score": list(s["score"]), "turn": s["turn"]}
        if a == "take":
            s["score"][s["turn"] % 2] += s["deck"].pop() - 5
        s["turn"] += 1
        return s

    def over(self, s):
        return s["turn"] >= 6

    def seat(self, s):
        return s["turn"] % 2

    def value(self, s, seat):
        return s["score"][seat] - s["score"][1 - seat]


class Randomness(unittest.TestCase):
    def test_same_seed_same_numbers(self):
        a, b = K.rng(7), K.rng(7)
        self.assertEqual([a.random() for _ in range(5)], [b.random() for _ in range(5)])

    def test_child_ignores_what_ran_before(self):
        a = K.rng(5)
        for _ in range(100):
            a.random()
        self.assertEqual(a.child(3).random(), K.rng(5).child(3).random())
        self.assertNotEqual(K.rng(5).child(3).random(), K.rng(5).child(4).random())

    def test_helpers(self):
        r = K.rng(1)
        self.assertTrue(all(0 <= r.int(4) < 4 for _ in range(200)))
        self.assertTrue(all(2 <= r.range(2, 3) <= 3 for _ in range(200)))
        self.assertEqual(r.weighted([("only", 1)]), "only")
        counts = {"a": 0, "b": 0}
        for _ in range(4000):
            counts[r.weighted([("a", 3), ("b", 1)])] += 1
        self.assertAlmostEqual(counts["a"] / 4000, 0.75, delta=0.03)


class Simulate(unittest.TestCase):
    def test_rows_tags_and_common_random_numbers(self):
        def play(rand, params, **_):
            return [{"day": d, "x": rand.child(d).random() * params["k"]} for d in (1, 2)]

        opts = K.args(["--runs", "3"])
        rows = K.simulate(play=play, params={"k": 1}, scenarios={"double": {"k": 2}}, profiles={"p": {}}, opts=opts)
        self.assertEqual(len(rows), 2 * 3 * 2)
        base = [r["x"] for r in rows if r["scenario"] == "baseline"]
        double = [r["x"] for r in rows if r["scenario"] == "double"]
        self.assertEqual([round(2 * x, 12) for x in base], [round(x, 12) for x in double])

    def test_set_tags_the_scenario(self):
        opts = K.args(["--runs", "1", "--set", "k=5", "--scenario", "baseline"])
        rows = K.simulate(play=lambda params, **_: {"k": params["k"]}, params={"k": 1}, opts=opts)
        self.assertEqual(rows[0]["scenario"], "baseline+k=5")
        self.assertEqual(rows[0]["k"], 5)


class Bots(unittest.TestCase):
    def test_lookahead_without_peeking_is_weaker_than_with(self):
        g = Toy()

        def redeal(s, seat, r):
            t = {"deck": list(s["deck"]), "score": list(s["score"]), "turn": s["turn"]}
            r.shuffle(t["deck"])
            return t

        def wins(bot):
            w = 0
            for i in range(150):
                r = K.rng(i)
                res = K.play_game(g, g.start(r), [bot, K.random_bot()], r)
                w += g.value(res["state"], 0) > 0
            return w / 150

        peek = wins(K.lookahead(g, rollouts=12))
        fair = wins(K.lookahead(g, rollouts=12, determinize=redeal))
        self.assertGreater(peek, fair + 0.15)

    def test_candidates_limit_the_search(self):
        g = Toy()
        bot = K.lookahead(g, rollouts=2, candidates=1, prior=lambda s, a, seat: 1 if a == "pass" else 0)
        r = K.rng(1)
        s = g.start(r)
        self.assertEqual(bot(s, g.actions(s), r, 0), "pass")

    def test_play_game_reports_capped(self):
        class Endless(Toy):
            def over(self, s):
                return False

            def actions(self, s):
                return ["pass"]

        g = Endless()
        r = K.rng(1)
        res = K.play_game(g, g.start(r), K.random_bot(), r, max_steps=20)
        self.assertTrue(res["capped"])
        self.assertEqual(res["steps"], 20)


if __name__ == "__main__":
    unittest.main()
