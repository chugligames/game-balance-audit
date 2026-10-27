"""Runs every experiment quoted in REPORT.md. Usage: python3 experiments.py [games]"""
import random
import sys
import time
from collections import Counter, defaultdict

from sim import COINS, GOODS, STRATS, make, play, winners

N_GAMES = int(sys.argv[1]) if len(sys.argv) > 1 else 4000


def ci(p, n):
    return 1.96 * (p * (1 - p) / n) ** 0.5


def run(n, names, games, seed, rules=None, rotate=False):
    """names[i] plays seat i (or rotates through seats if rotate). Returns stats."""
    rng = random.Random(seed)
    seat_win = [0.0] * n
    strat_win = defaultdict(float)
    strat_seats = Counter()
    margins = []
    scores = []
    coin_by_good = Counter()
    bigs = 0
    for k in range(games):
        order = names[k % n:] + names[:k % n] if rotate else names
        bots = [make(x) for x in order]
        g = play(n, bots, rng, rules)
        w = winners(g)
        for i in w:
            seat_win[i] += 1.0 / len(w)
            strat_win[order[i]] += 1.0 / len(w)
        for x in order:
            strat_seats[x] += 1
        s = sorted(g.score, reverse=True)
        margins.append(s[0] - s[1])
        scores.append(g.score)
        bigs += sum(g.big_sales)
    return dict(seat=[x / games for x in seat_win], strat=strat_win, seats=strat_seats,
                margins=margins, scores=scores, games=games, bigs=bigs / games)


def fmt_seats(r):
    return " ".join("%.1f%%" % (100 * x) for x in r["seat"])


def section(t):
    print("\n## " + t, flush=True)


def seat_tests(games, rules=None, strats=("Greedy", "QuickPairs", "BigSale", "Saffron", "Denier", "Random")):
    for n in (2, 3, 4):
        for s in strats:
            r = run(n, [s] * n, games, seed=hash((n, s)) % 10**6, rules=rules)
            m = r["margins"]
            close = sum(1 for x in m if x <= 3) / len(m)
            print("n=%d %-10s seats: %s  (fair=%.1f%%, ±%.1f)  mean margin %.1f, ≤3 pts %.0f%%"
                  % (n, s, fmt_seats(r), 100.0 / n, 100 * ci(1.0 / n, games),
                     sum(m) / len(m), 100 * close), flush=True)


def vs_field(games, field="Greedy"):
    for n in (2, 3, 4):
        row = []
        for s in STRATS:
            names = [s] + [field] * (n - 1)
            r = run(n, names, games, seed=7 + n, rotate=True)
            row.append("%s %.0f%%" % (s, 100 * r["strat"][s] / games))
        print("n=%d one X vs %d×%s (fair %.0f%%): %s" % (n, n - 1, field, 100.0 / n, ", ".join(row)), flush=True)


def round_robin(games):
    print("2-player head to head, seat-rotated, row's win rate vs column:")
    print("%-10s " % "" + " ".join("%10s" % s for s in STRATS))
    for a in STRATS:
        cells = []
        for b in STRATS:
            if a == b:
                cells.append("%10s" % "-")
                continue
            r = run(2, [a, b], games, seed=11, rotate=True)
            cells.append("%9.0f%%" % (100 * r["strat"][a] / games))
        print("%-10s " % a + " ".join(cells), flush=True)


def coin_share(games):
    for n in (2, 4):
        r = run(n, ["Greedy"] * n, games, seed=3)
        tot = sum(sum(s) for s in r["scores"]) / games
        print("n=%d Greedy mirror: avg total coins/game %.1f, avg winner score %.1f"
              % (n, tot, sum(max(s) for s in r["scores"]) / games))
    print("Coin supply per good:", {x: sum(COINS[x]) for x in GOODS},
          "4-card sale values:", {x: sum(COINS[x][:4]) for x in GOODS})


def search(games, n, rounds):
    """Random search for the strongest Heuristic parameters vs a mixed field."""
    import sim
    rng = random.Random(99)
    field = ["Greedy", "QuickPairs", "Saffron", "BigSale", "Denier"]
    best = []
    for _ in range(rounds):
        params = dict(
            pref={x: round(rng.uniform(0.2, 2.0), 2) for x in GOODS},
            sell_at=rng.choice([2, 3, 4]), deny=round(rng.uniform(0, 1.5), 2),
            race=rng.choice([0, 1, 2, 3]), endgame=rng.choice([0.5, 1, 2, 3]),
            big_hunt=rng.random() < 0.5)
        wins = 0.0
        grng = random.Random(5)
        for k in range(games):
            opps = [field[(k + j) % len(field)] for j in range(n - 1)]
            seat = k % n
            bots = [make(o) for o in opps]
            bots.insert(seat, sim.Heuristic("X", **params))
            g = play(n, bots, grng)
            w = winners(g)
            if seat in w:
                wins += 1.0 / len(w)
        best.append((wins / games, params))
    best.sort(key=lambda t: -t[0])
    return best


if __name__ == "__main__":
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    t = time.time()
    if which in ("all", "seat"):
        section("Seat win rates, mirror matches (%d games each)" % N_GAMES)
        seat_tests(N_GAMES)
    if which in ("all", "field"):
        section("One strategy vs a field of Greedy (%d games each)" % N_GAMES)
        vs_field(N_GAMES)
        vs_field(N_GAMES, field="Saffron")
    if which in ("all", "rr"):
        section("Round robin")
        round_robin(N_GAMES)
    if which in ("all", "coins"):
        section("Coins")
        coin_share(N_GAMES)
    if which in ("all", "search"):
        for n in (2, 4):
            section("Strategy search n=%d" % n)
            for wr, p in search(N_GAMES // 4, n, 40)[:5]:
                print("%.1f%% %s" % (100 * wr, p), flush=True)
    print("\n(elapsed %.0fs)" % (time.time() - t))
