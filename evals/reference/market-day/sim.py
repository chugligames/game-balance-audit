"""Reference harness for examples/market-day (rulebook only): one row per seat per game.
    python3 sim.py --runs 2000 --out runs/all.jsonl

Assumptions where the rules are silent (an agent under test should log its own):
- The game ends the moment the market can't be refilled after a Take, mid-round.
- A tie for most coins splits the win.
- Over the hand limit, a player discards the cards they hold the fewest of."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../skills/game-balance-audit/scripts"))
from sim_kit import args, simulate  # noqa: E402

GOODS = {"rice": 15, "lentils": 13, "cloth": 11, "spice": 9, "saffron": 6}
COINS = {"rice": [3, 2, 2, 1, 1, 1], "lentils": [4, 3, 2, 2, 1], "cloth": [5, 4, 3, 2, 1], "spice": [6, 5, 4, 3], "saffron": [9, 8, 7, 7]}
PARAMS = {"coins": COINS, "goods": GOODS, "hand_limit": 7, "big_sale": 4, "big_sale_reward": "extra-turn", "equal_turns": False, "second_seat_bonus": 0,
          "start_coins": {}}  # e.g. {"2": [0, 2], "3": [0, 1, 2]}: coins each seat starts with, by player count

# Player strategies. `sell_at`: smallest set worth selling; `like`: how much they chase each good.
STRATEGIES = {
    "steady": {"sell_at": 3, "like": {}},
    "quick": {"sell_at": 2, "like": {}},
    "hoarder": {"sell_at": 4, "like": {}},
    "saffron": {"sell_at": 3, "like": {"saffron": 2.5, "spice": 1.5}, "sell_now": {"saffron": 2}},
}

# A profile is a table: which strategies sit down. Seats rotate every game, so each
# strategy plays from each seat equally often.
PROFILES = {
    "mirror-2p": ["steady", "steady"],
    "mirror-3p": ["steady", "steady", "steady"],
    "saffron-vs-steady": ["saffron", "steady"],
    "hoarder-vs-steady": ["hoarder", "steady"],
    "quick-vs-steady": ["quick", "steady"],
}


def top_coins(stack, k):
    return sum(stack[:k]) + max(0, k - len(stack))


def choose(st, me, strat, p):
    hand = st["hands"][me]
    counts = {g: hand.count(g) for g in GOODS}
    # Sell when a set is big enough (or a liked good is ready early).
    best_sell = None
    for g, n in counts.items():
        need = strat.get("sell_now", {}).get(g, strat["sell_at"])
        if n >= max(2, need):
            value = top_coins(st["coins"][g], n) + (6 if n >= p["big_sale"] else 0)
            if not best_sell or value > best_sell[0]:
                best_sell = (value, g)
    if best_sell:
        return ("sell", best_sell[1])
    # Otherwise take the market card that best grows a set worth selling.
    def worth(g):
        stack = st["coins"][g]
        price = stack[0] if stack else 1
        return price * strat["like"].get(g, 1.0) * (1 + counts[g])
    if not st["market"]:
        sells = [g for g, n in counts.items() if n >= 2]
        return ("sell", max(sells, key=lambda g: counts[g])) if sells else None
    return ("take", max(range(len(st["market"])), key=lambda i: worth(st["market"][i])))


def play(rand, params, profile, run, **_):
    p = params
    n = len(profile)
    shift = run % n  # rotate seats
    seats = [profile[(i + shift) % n] for i in range(n)]
    r = rand.child(run)
    deck = [g for g, k in p["goods"].items() for _ in range(k)]
    r.shuffle(deck)
    st = {"deck": deck, "market": [deck.pop() for _ in range(5)], "hands": [[deck.pop() for _ in range(3)] for _ in range(n)],
          "coins": {g: list(v) for g, v in p["coins"].items()}, "score": [0] * n}
    st["score"][1 % n] += p["second_seat_bonus"]
    for i, c in enumerate(p["start_coins"].get(str(n), [])):
        st["score"][i] += c
    turns, extra, half_leader = [0] * n, [0] * n, None
    total_turns_guess = (len(deck) + 5) * 1.6
    seat, over, played = 0, False, 0
    while not over:
        again = True
        while again and not over:
            again = False
            act = choose(st, seat, STRATEGIES[seats[seat]], p)
            turns[seat] += 1
            played += 1
            if act is None:
                over = True
                break
            if act[0] == "take":
                st["hands"][seat].append(st["market"].pop(act[1]))
                if st["deck"]:
                    st["market"].append(st["deck"].pop())
                elif not p["equal_turns"]:
                    over = True
                hand = st["hands"][seat]
                while len(hand) > p["hand_limit"]:
                    hand.remove(min(set(hand), key=hand.count))
            else:
                g = act[1]
                k = st["hands"][seat].count(g)
                st["hands"][seat] = [c for c in st["hands"][seat] if c != g]
                stack = st["coins"][g]
                st["score"][seat] += top_coins(stack, k)
                del stack[:k]
                if k >= p["big_sale"]:
                    if p["big_sale_reward"] == "extra-turn":
                        again = True
                        extra[seat] += 1
                    else:
                        st["score"][seat] += p["big_sale_reward"]
            if half_leader is None and played >= total_turns_guess / 2:
                top = max(st["score"])
                half_leader = st["score"].index(top) if st["score"].count(top) == 1 else -1
        seat = (seat + 1) % n
        if p["equal_turns"] and not st["deck"] and len(st["market"]) < 5 and seat == 0:
            over = True
    top = max(st["score"])
    winners = [i for i in range(n) if st["score"][i] == top]
    rows = []
    for i in range(n):
        row = {"seat": i + 1, "strategy": seats[i], "won": (1.0 / len(winners)) if i in winners else 0.0,
               "coins": st["score"][i], "turns": turns[i], "extraTurns": extra[i], "margin": st["score"][i] - max(st["score"][j] for j in range(n) if j != i)}
        if i == 0 and half_leader is not None and half_leader >= 0:
            row["halfLeaderWon"] = 1.0 if half_leader in winners else 0.0
        rows.append(row)
    return rows


SCENARIOS = {
    "saffron-7-6-5-5": {"coins": dict(COINS, saffron=[7, 6, 5, 5])},
    "equal-turns": {"equal_turns": True},
    "big-sale-+3-coins": {"big_sale_reward": 3},
    "second-seat-+2": {"second_seat_bonus": 2},
    "later-seat-coins": {"start_coins": {"2": [0, 2], "3": [0, 1, 2], "4": [0, 1, 2, 3]}},
}
simulate(play=play, params=PARAMS, scenarios=SCENARIOS, profiles=PROFILES, opts=args())
