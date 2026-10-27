"""Ladoo Spin: 30 days of play per run, one row per day.
  python3 sim.py --runs 200 --out ../runs/baseline.jsonl
  TRACE_DAY=3 python3 sim.py --runs 1 --profile regular   # prints every spin of day 3
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "<skill>/scripts")
from sim_kit import simulate, args
import slot

PARAMS = {
    "pays": dict(slot.PAYS),
    "edits": [],            # reel-strip edits: [reel(1-3), stop(1-12), symbol]
    "noChilli1": False,     # rule: lone CHILLI on reel 1 pays nothing
    "gift": 500,            # free coins a day
    "giftMode": "flat",     # flat: +gift every day; floor: top the balance up to `gift` if below it
    "startCoins": 500,
    "maxBet": 100,
    "days": 30,
    "bigAt": 40,
}

# Player models (assumptions, see game-model.md). bet: fixed coins a spin, or betShare of
# balance (clamped 1..maxBet). buy: chance they buy a pack when they can't afford a spin.
PROFILES = {
    "flat-1":  {"spins": 1000, "bet": 1, "buy": 0, "pack": 0},   # measuring profile for exact checks
    "casual":  {"spins": 60,  "bet": 10, "buy": 0.0, "pack": 0},
    "regular": {"spins": 200, "bet": 25, "buy": 0.1, "pack": 2000},
    "keen":    {"spins": 400, "betShare": 0.05, "buy": 0.3, "pack": 5000},
}

SCENARIOS = {
    # P1: RTP
    "P1-A pays: MANGOx3 10->6, LADOOx3 200->207": {"pays": dict(slot.PAYS, MMM=6, LLL=207)},
    "P1-B strip: reel 2 stop 7 MANGO->CHILLI": {"edits": [[2, 7, "CHILLI"]]},
    "P1-C rule: lone CHILLI pays 0, CHILLIx2 5->4": {"noChilli1": True, "pays": dict(slot.PAYS, CHILLI2=4)},
    # P2: daily gift outruns the house edge (tested on top of P1-A)
    "P2-A gift 500->150 (+P1-A)": {"pays": dict(slot.PAYS, MMM=6, LLL=207), "gift": 150},
    "P2-B gift tops up to 500 (+P1-A)": {"pays": dict(slot.PAYS, MMM=6, LLL=207), "giftMode": "floor"},
    "P2-C max bet 100->500 (+P1-A)": {"pays": dict(slot.PAYS, MMM=6, LLL=207), "maxBet": 500},
}

_cache = {}


def table(p):
    key = (tuple(sorted(p["pays"].items())), tuple(map(tuple, p["edits"])), p["noChilli1"])
    if key not in _cache:
        reels = slot.load_reels()
        for reel, stop, sym in p["edits"]:
            reels[reel - 1][stop - 1] = sym
        pays = dict(p["pays"])
        if p["noChilli1"]:
            pays["CHILLI1"] = 0
        _cache[key] = (reels, [slot.evaluate((a, b, c), pays) for a in reels[0] for b in reels[1] for c in reels[2]])
    return _cache[key]


def play(rand, params, profile, profile_name, **_):
    p = params
    reels, outcomes = table(p)
    trace = os.environ.get("TRACE_DAY")
    bal, rows = p["startCoins"], []
    for day in range(1, p["days"] + 1):
        r = rand.child(day)
        start = bal
        if p["giftMode"] == "floor":
            bal = max(bal, p["gift"])
        else:
            bal += p["gift"]
        gift = bal - start
        bet_sum = won = hits = big = spins = 0
        out = bought = 0
        for i in range(profile["spins"]):
            if "betShare" in profile:
                bet = max(1, min(p["maxBet"], int(bal * profile["betShare"])))
            else:
                bet = min(profile["bet"], p["maxBet"])
            if bal < bet:
                out = 1
                if profile["buy"] and r.chance(profile["buy"]):
                    bought += 1
                    bal += profile["pack"]
                else:
                    break
            a, b, c = r.int(12), r.int(12), r.int(12)
            k, m = outcomes[a * 144 + b * 12 + c]
            bal += bet * m - bet
            bet_sum += bet
            won += bet * m
            spins += 1
            hits += m > 0
            big += m >= p["bigAt"]
            if trace and int(trace) == day:
                print("day %d spin %d bet %d  %-6s %-6s %-6s -> %-28s x%-3d bal %d" % (
                    day, i + 1, bet, reels[0][a], reels[1][b], reels[2][c], slot.LABELS[k], m, bal))
        rows.append({"day": day, "spins": spins, "coinIn": bet_sum, "won": won,
                     "rtp": won / bet_sum if bet_sum else 0, "hitRate": hits / spins if spins else 0,
                     "bigRate": big / spins if spins else 0, "bigWins": big, "hits": hits,
                     "netExGift": won - bet_sum, "drift": gift + won - bet_sum, "netDay": bal - start, "balance": bal, "gift": gift,
                     "outOfCoins": out, "purchases": bought, "lowBalance": int(bal < 500)})
    return rows


if __name__ == "__main__":
    simulate(play, PARAMS, SCENARIOS, PROFILES, args())
