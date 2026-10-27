"""Market Day simulator for the balance audit.

Implements RULES.md as written. Rule interpretations (see REPORT.md):
  * The game ends the moment a Take leaves the market short because the deck is empty.
    Cards left in hands score nothing.
  * Market takes are public, so bots know every card an opponent took from the market
    (but not their 3 starting cards). Discards are face-down/out of the game.
  * A big-sale extra turn can itself be another Sell (rarely possible with a 7-card cap).
"""
import random
import sys
from collections import Counter

GOODS = ["Rice", "Lentils", "Cloth", "Spice", "Saffron"]
DECK = {"Rice": 15, "Lentils": 13, "Cloth": 11, "Spice": 9, "Saffron": 6}
COINS = {
    "Rice": [3, 2, 2, 1, 1, 1],
    "Lentils": [4, 3, 2, 2, 1],
    "Cloth": [5, 4, 3, 2, 1],
    "Spice": [6, 5, 4, 3],
    "Saffron": [9, 8, 7, 7],
}
HAND_LIMIT = 7
MARKET = 5


class Game:
    def __init__(self, n, rng, rules=None):
        self.rules = dict(rules or {})
        self.n = n
        self.rng = rng
        deck = [g for g in GOODS for _ in range(self.rules.get("deck", DECK)[g])]
        rng.shuffle(deck)
        self.deck = deck
        coins = self.rules.get("coins", COINS)
        self.stacks = {g: list(coins[g]) for g in GOODS}
        hand_size = self.rules.get("hand", 3)
        if isinstance(hand_size, (list, tuple)):
            sizes = list(hand_size)[:n]
        else:
            sizes = [hand_size] * n
        self.hands = [Counter() for _ in range(n)]
        self.public = [Counter() for _ in range(n)]  # cards seen going into each hand
        for i in range(n):
            for _ in range(sizes[i]):
                self.hands[i][self.deck.pop()] += 1
        self.market = [self.deck.pop() for _ in range(MARKET)]
        self.score = [0] * n
        self.over = False
        self.turns = [0] * n
        self.big_sales = [0] * n
        self.sales = [0] * n

    # ---- helpers for bots ----
    def coin_at(self, good, k):
        """Value of the k-th card (0-based) sold from the current stack."""
        s = self.stacks[good]
        return s[k] if k < len(s) else 1

    def sale_value(self, good, count):
        return sum(self.coin_at(good, k) for k in range(count))

    # ---- actions ----
    def do_take(self, p, idx, discard_fn):
        card = self.market.pop(idx)
        self.hands[p][card] += 1
        self.public[p][card] += 1
        if sum(self.hands[p].values()) > HAND_LIMIT:
            d = discard_fn(self, p)
            self.hands[p][d] -= 1
            if self.public[p][d] > 0:
                self.public[p][d] -= 1
        if self.deck:
            self.market.append(self.deck.pop())
        elif not getattr(self, "finishing", False):
            self.over = True

    def do_sell(self, p, good, count):
        assert count >= 2 and self.hands[p][good] >= count
        self.hands[p][good] -= count
        self.public[p][good] = max(0, self.public[p][good] - count)
        for _ in range(count):
            self.score[p] += self.stacks[good].pop(0) if self.stacks[good] else 1
        self.sales[p] += 1
        big = self.rules.get("big_sale", 4)
        if big and count >= big:
            self.big_sales[p] += 1
            return True
        return False


def play(n, bots, rng, rules=None, max_chain=10):
    g = Game(n, rng, rules)
    p = 0
    while not g.over:
        chain = 0
        again = True
        while again and not g.over:
            again = False
            g.turns[p] += 1
            act = bots[p].act(g, p)
            if act[0] == "sell":
                again = g.do_sell(p, act[1], act[2])
                chain += 1
                if chain > max_chain:
                    again = False
            else:
                g.do_take(p, act[1], bots[p].discard)
        p = (p + 1) % n
        if g.over and g.rules.get("finish_round") and p != 0:
            g.over = False  # keep playing to the end of the round from the shrinking market
            g.finishing = True
        if getattr(g, "finishing", False) and (p == 0 or not g.market):
            g.over = True
    return g


# ---------------------------------------------------------------- bots
class Bot:
    name = "base"

    def sellable(self, g, p):
        return [(x, c) for x, c in g.hands[p].items() if c >= 2]

    def discard(self, g, p):
        h = g.hands[p]
        return min((x for x in h if h[x] > 0), key=lambda x: (h[x] * g.coin_at(x, 0), g.coin_at(x, 0)))


class RandomBot(Bot):
    name = "Random"

    def act(self, g, p):
        opts = [("take", i) for i in range(len(g.market))]
        for x, c in self.sellable(g, p):
            for k in range(2, c + 1):
                opts.append(("sell", x, k))
        return g.rng.choice(opts)


class Heuristic(Bot):
    """Parametric bot. Everything 'strategic' is a knob so we can search the space.

    pref[good]     multiplier on how much it wants each good
    sell_at        sell a set once it reaches this many cards (2..5)
    deny           weight on taking cards opponents (publicly) are collecting
    race           if an opponent publicly holds >= this many of a good I hold, sell it now
    endgame        when deck <= endgame * n, dump every set
    """

    def __init__(self, name, pref=None, sell_at=3, deny=0.0, race=2, endgame=1.0, big_hunt=False):
        self.name = name
        self.pref = pref or {x: 1.0 for x in GOODS}
        self.sell_at = sell_at
        self.deny = deny
        self.race = race
        self.endgame = endgame
        self.big_hunt = big_hunt

    def card_value(self, g, p, x):
        have = g.hands[p][x]
        mine = g.coin_at(x, have) * self.pref[x]
        if have == 0:
            mine *= 0.6  # singletons only pay if a second copy turns up
        opp = 0.0
        if self.deny:
            for q in range(g.n):
                if q != p and g.public[q][x] >= 1:
                    opp = max(opp, g.coin_at(x, g.public[q][x]))
        return mine + self.deny * opp

    def act(self, g, p):
        sets = self.sellable(g, p)
        endgame = len(g.deck) <= self.endgame * g.n
        best_sell = None
        for x, c in sets:
            want = endgame or c >= self.sell_at
            if self.big_hunt and c >= 4:
                want = True
            if not want and self.race:
                for q in range(g.n):
                    if q != p and g.public[q][x] >= self.race:
                        want = True
            if c >= HAND_LIMIT - 1:
                want = True
            if want:
                v = g.sale_value(x, c) + (100 if c >= 4 else 0)
                if best_sell is None or v > best_sell[0]:
                    best_sell = (v, x, c)
        if best_sell:
            return ("sell", best_sell[1], best_sell[2])
        vals = [self.card_value(g, p, x) for x in g.market]
        return ("take", max(range(len(vals)), key=lambda i: vals[i]))


def make(name):
    one = {x: 1.0 for x in GOODS}
    if name == "Random":
        return RandomBot()
    if name == "Greedy":  # balanced, sells at 3 or when raced
        return Heuristic("Greedy")
    if name == "QuickPairs":  # sells any pair straight away
        return Heuristic("QuickPairs", sell_at=2)
    if name == "BigSale":  # holds for 4-of-a-kind and the extra turn
        return Heuristic("BigSale", sell_at=4, race=0, big_hunt=True)
    if name == "Saffron":  # only cares about Saffron and Spice
        pref = {"Rice": 0.1, "Lentils": 0.1, "Cloth": 0.3, "Spice": 1.0, "Saffron": 1.5}
        return Heuristic("Saffron", pref=pref, sell_at=2)
    if name == "Cheap":  # deliberately collects the common cheap goods
        pref = {"Rice": 2.0, "Lentils": 1.5, "Cloth": 1.0, "Spice": 0.3, "Saffron": 0.3}
        return Heuristic("Cheap", pref=pref, sell_at=4, race=0, big_hunt=True)
    if name == "Denier":  # hate-drafts
        return Heuristic("Denier", deny=1.0)
    raise KeyError(name)


STRATS = ["Random", "Greedy", "QuickPairs", "BigSale", "Saffron", "Cheap", "Denier"]


def winners(g):
    m = max(g.score)
    return [i for i, s in enumerate(g.score) if s == m]


if __name__ == "__main__":
    rng = random.Random(1)
    g = play(2, [make("Greedy"), make("Greedy")], rng)
    print(g.score, g.turns, len(g.deck))
