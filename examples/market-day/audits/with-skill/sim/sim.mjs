// Market Day simulator: the rules in RULES.md written as code.
//   node sim/sim.mjs --runs 400 --out runs/baseline.jsonl
//   TRACE=1 node sim/sim.mjs --runs 1 --profile mirror-2p --scenario baseline   (prints every move)
import { args, simulate, bots, playGame } from '<skill>/scripts/sim-kit.mjs';

const GOODS = ['Rice', 'Lentils', 'Cloth', 'Spice', 'Saffron'];

// Every number in the rulebook. What-ifs override these.
const PARAMS = {
  counts: [15, 13, 11, 9, 6],                                  // Components: goods cards
  stacks: [[3, 2, 2, 1, 1, 1], [4, 3, 2, 2, 1], [5, 4, 3, 2, 1], [6, 5, 4, 3], [9, 8, 7, 7]],
  handStart: 3, marketSize: 5, handLimit: 7,
  minSell: [2, 2, 2, 2, 2],                                    // Sell: 2 or more of one good
  emptyStackValue: 1,                                          // after a stack runs out
  bigSale: 4, bigSaleExtraTurn: true, bigSaleBonus: 0,         // Big sale: 4+ cards → another turn
  finishRound: false,                                          // Assumption A1: game ends at once
  startCoins: [0, 0, 0, 0],                                    // seat compensation (none in the rules)
  extraStartCards: [0, 0, 0, 0],
};

// ── Rules ────────────────────────────────────────────────────────────────────
function makeGame(P) {
  const G = {
    start(rand, n) {
      const deck = [];
      P.counts.forEach((c, g) => { for (let i = 0; i < c; i++) deck.push(g); });
      rand.shuffle(deck);
      const hands = [];
      for (let p = 0; p < n; p++) {                            // Setup: deal 3 each
        const h = [0, 0, 0, 0, 0];
        for (let i = 0; i < P.handStart + (P.extraStartCards[p] || 0); i++) h[deck.pop()]++;
        hands.push(h);
      }
      const market = [];
      for (let i = 0; i < P.marketSize; i++) market.push(deck.pop());
      return {
        n, deck, market, hands, coins: ((P.startCoinsByN && P.startCoinsByN[n]) || P.startCoins).slice(0, n).map((x) => x || 0),
        stacks: P.stacks.map((s) => s.slice()), turn: 0, over: false, ended: -1,
        finalTurnsLeft: -1, steps: 0, takes: Array(n).fill(0), sells: Array(n).fill(0),
        bigSales: Array(n).fill(0), soldBy: hands.map(() => [0, 0, 0, 0, 0]), turnsTaken: Array(n).fill(0),
      };
    },
    clone: (s) => ({
      ...s, deck: s.deck.slice(), market: s.market.slice(), hands: s.hands.map((h) => h.slice()),
      coins: s.coins.slice(), stacks: s.stacks.map((x) => x.slice()), takes: s.takes.slice(),
      sells: s.sells.slice(), bigSales: s.bigSales.slice(), soldBy: s.soldBy.map((x) => x.slice()),
      turnsTaken: s.turnsTaken.slice(),
    }),
    seat: (s) => s.turn,
    over: (s) => s.over,
    actions(s) {
      const h = s.hands[s.turn];
      const acts = [];
      const seen = new Set();
      for (const g of s.market) if (!seen.has(g)) { seen.add(g); acts.push({ t: 'take', g }); }
      for (let g = 0; g < 5; g++) for (let k = P.minSell[g]; k <= h[g]; k++) acts.push({ t: 'sell', g, k });
      return acts;
    },
    apply(s, a) {
      const p = s.turn;
      const h = s.hands[p];
      let again = false;
      s.steps++; s.turnsTaken[p]++;
      if (a.t === 'take') {                                    // Take
        s.market.splice(s.market.indexOf(a.g), 1);
        h[a.g]++; s.takes[p]++;
        if (s.deck.length) s.market.push(s.deck.pop());
        else if (s.ended < 0) endTrigger(s);                   // End: market can't be refilled
        while (sum(h) > P.handLimit) h[discardChoice(s, h)]--; // discard down to 7
      } else {                                                 // Sell
        h[a.g] -= a.k; s.sells[p]++; s.soldBy[p][a.g] += a.k;
        for (let i = 0; i < a.k; i++) s.coins[p] += s.stacks[a.g].length ? s.stacks[a.g].shift() : P.emptyStackValue;
        if (a.k >= P.bigSale) {                                // Big sale
          s.bigSales[p]++; s.coins[p] += P.bigSaleBonus;
          again = P.bigSaleExtraTurn;
        }
      }
      if (s.ended >= 0) {
        if (s.ended === s.steps) { if (s.finalTurnsLeft <= 0) { s.over = true; return s; } }
        else if (!again && --s.finalTurnsLeft <= 0) { s.over = true; return s; }
      }
      if (!again) s.turn = (p + 1) % s.n;
      // a player with nothing legal (empty market, no pair) ends the game
      if (!G.actions(s).length) s.over = true;
      return s;
    },
    value(s, seat) {                                           // win (ties shared) + a little margin
      const best = Math.max(...s.coins.filter((_, i) => i !== seat));
      return (s.coins[seat] > best ? 1 : s.coins[seat] === best ? 0.5 : 0) + (s.coins[seat] - best) / 100;
    },
  };
  function endTrigger(s) {
    s.ended = s.steps;
    // A1 variant: everyone after the trigger gets one more turn so all have had equal turns
    s.finalTurnsLeft = P.finishRound ? (s.n - 1 - s.turn) : 0;
  }
  // Assumption A3: discard the card of the good you hold fewest of, cheapest first
  function discardChoice(s, h) {
    let best = -1, key = Infinity;
    for (let g = 0; g < 5; g++) if (h[g]) {
      const k = h[g] * 10 + topCoin(s, g);
      if (k < key) { key = k; best = g; }
    }
    return best;
  }
  function topCoin(s, g, i = 0) { return s.stacks[g].length > i ? s.stacks[g][i] : P.emptyStackValue; }
  G.topCoin = topCoin;
  G.saleValue = (s, g, k) => { let v = 0; for (let i = 0; i < k; i++) v += topCoin(s, g, i); return v; };
  // Hidden information: re-deal the deck and the other hands from the cards this seat can't see
  G.determinize = (s, seat, rand) => {
    const c = G.clone(s);
    const pool = c.deck.slice();
    for (let p = 0; p < c.n; p++) if (p !== seat) for (let g = 0; g < 5; g++) for (let i = 0; i < c.hands[p][g]; i++) pool.push(g);
    rand.shuffle(pool);
    for (let p = 0; p < c.n; p++) if (p !== seat) {
      const size = sum(c.hands[p]);
      c.hands[p] = [0, 0, 0, 0, 0];
      for (let i = 0; i < size; i++) c.hands[p][pool.pop()]++;
    }
    c.deck = pool;
    return c;
  };
  return G;
}
const sum = (xs) => xs.reduce((a, b) => a + b, 0);

// ── Player models ────────────────────────────────────────────────────────────
// A greedy trader with weights. sellAt: smallest set it sells (per good); taste: how much it
// wants each good; endgame: sells any legal set once the deck is this short.
function trader(G, P, { sellAt = [3, 3, 3, 3, 3], taste = [1, 1, 1, 1, 1], endgame = 4 } = {}) {
  return (s, acts, rand, seat) => {
    const h = s.hands[seat];
    const late = s.deck.length <= endgame * s.n;
    const full = sum(h) >= P.handLimit;
    let best = null, bv = -Infinity;
    for (const a of acts) {
      let v;
      if (a.t === 'sell') {
        if (a.k !== h[a.g]) continue;                          // sell the whole set
        const ready = a.k >= sellAt[a.g] || late || (full && a.k >= 2);
        if (!ready) continue;
        v = 100 + G.saleValue(s, a.g, a.k) + (a.k >= P.bigSale && P.bigSaleExtraTurn ? 6 : 0) + P.bigSaleBonus * (a.k >= P.bigSale);
      } else {
        // what the card would add to the set if sold later; less if the hand is full
        v = taste[a.g] * G.topCoin(s, a.g, h[a.g]) * (h[a.g] + 1 >= 2 ? 1.2 : 1) - (full ? 3 : 0) + rand.next() * 0.01;
      }
      if (v > bv) { bv = v; best = a; }
    }
    return best || acts.find((a) => a.t === 'take') || acts[0];
  };
}

function makePolicies(G, P, n, rand) {
  const steady = trader(G, P);
  return {
    steady,
    quick: trader(G, P, { sellAt: [2, 2, 2, 2, 2] }),
    bigsale: trader(G, P, { sellAt: [4, 4, 4, 4, 4], endgame: 2 }),
    luxury: trader(G, P, { sellAt: [4, 3, 3, 2, 2], taste: [0.2, 0.4, 0.8, 1.3, 1.6] }),
    careless: bots.sloppy(steady, 0.3),
    expert: bots.lookahead(G, { rollouts: 24, playout: steady, determinize: G.determinize, candidates: 6, prior: (s, a, seat) => (a.t === 'sell' ? G.saleValue(s, a.g, a.k) : G.topCoin(s, a.g, s.hands[seat][a.g])) }),
  };
}

// Tables. rotate: seat order shifts by one each run so every strategy sits in every seat.
const PROFILES = {
  'mirror-2p': { lineup: ['steady', 'steady'] },
  'mirror-3p': { lineup: ['steady', 'steady', 'steady'] },
  'mirror-4p': { lineup: ['steady', 'steady', 'steady', 'steady'] },
  'mirror-quick-2p': { lineup: ['quick', 'quick'] },
  'mirror-expert-2p': { lineup: ['expert', 'expert'], expensive: true },
  'quick-vs-steady-2p': { lineup: ['quick', 'steady'], rotate: true },
  'bigsale-vs-steady-2p': { lineup: ['bigsale', 'steady'], rotate: true },
  'luxury-vs-steady-2p': { lineup: ['luxury', 'steady'], rotate: true },
  'all-4p': { lineup: ['steady', 'quick', 'bigsale', 'luxury'], rotate: true },
  'expert-vs-careless-2p': { lineup: ['expert', 'careless'], rotate: true, expensive: true },
  'expert-vs-steady-2p': { lineup: ['expert', 'steady'], rotate: true, expensive: true },
};

const TRACE = process.env.TRACE;

function play({ rand, params, profile, profileName, run }) {
  const G = makeGame(params);
  const n = profile.lineup.length;
  const shift = profile.rotate ? run % n : 0;
  const lineup = profile.lineup.map((_, i) => profile.lineup[(i + shift) % n]);
  const pol = makePolicies(G, params, n, rand);
  const deal = rand.child('deal');
  const botRand = rand.child('bots');
  let s = G.start(deal, n);
  const deckStart = s.deck.length;
  let leader = -1, leadChanges = 0, halfLeader = null;
  const onStep = (st, a, seat) => {
    if (TRACE) console.error(`[${st.steps}] seat ${seat} (${lineup[seat]}) hand ${fmt(st.hands[seat])} market ${st.market.map((g) => 'RLCSF'[g]).join('')} deck ${st.deck.length} coins ${st.coins.join('/')} → ${a.t} ${GOODS[a.g]}${a.k ? ' x' + a.k : ''}`);
  };
  const policies = lineup.map((name) => pol[name]);
  // Track leader and half-time leader by stepping manually
  let steps = 0, capped = false;
  while (!G.over(s)) {
    if (steps++ > 2000) { capped = true; break; }
    const acts = G.actions(s);
    if (!acts.length) break;
    const seat = G.seat(s);
    const a = policies[seat](s, acts, botRand, seat);
    onStep(s, a, seat);
    s = G.apply(s, a, deal);
    const top = Math.max(...s.coins);
    const leaders = s.coins.map((c, i) => (c === top ? i : -1)).filter((i) => i >= 0);
    if (leaders.length === 1 && top > 0 && leaders[0] !== leader) { if (leader >= 0) leadChanges++; leader = leaders[0]; }
    if (halfLeader === null && s.deck.length <= deckStart / 2) halfLeader = leaders.length === 1 ? leaders[0] : -1;
  }
  const top = Math.max(...s.coins);
  const winners = s.coins.map((c, i) => (c === top ? i : -1)).filter((i) => i >= 0);
  if (TRACE) console.error(`END coins ${s.coins.join('/')} hands ${s.hands.map(fmt).join(' | ')}`);
  return lineup.map((name, seat) => {
    const others = Math.max(...s.coins.filter((_, i) => i !== seat));
    const row = {
      game: 1, players: n, seat: `seat ${seat + 1}`, strategy: name,
      won: winners.includes(seat) ? 1 / winners.length : 0,
      score: s.coins[seat], margin: s.coins[seat] - others,
      takes: s.takes[seat], sells: s.sells[seat], bigSales: s.bigSales[seat], turns: s.turnsTaken[seat],
      saffronSold: s.soldBy[seat][4], riceSold: s.soldBy[seat][0], cardsWasted: sum(s.hands[seat]),
      takesTotal: sum(s.takes), steps: s.steps, tie: winners.length > 1 ? 1 : 0,
      winGap: top - [...s.coins].sort((a, b) => b - a)[1],
    };
    if (seat === 0) { row.halfLeaderWon = halfLeader >= 0 ? (winners.includes(halfLeader) ? 1 : 0) : null; row.leadChanges = leadChanges; }
    if (row.halfLeaderWon === null) delete row.halfLeaderWon;
    if (capped) row.capped = true;
    return row;
  });
}
const fmt = (h) => h.map((c, g) => (c ? 'RLCSF'[g] + c : '')).join('') || '-';   // F = saFfron

// What-ifs, named after the change. Filled in after the baseline.
const SCENARIOS = {
  'A1 finish the round': { finishRound: true },
  // P1 first-seat advantage
  'P1-a start coins 0/3 at 2p 0/2/4 at 3p 0/2/4/6 at 4p': { startCoinsByN: { 2: [0, 3], 3: [0, 2, 4], 4: [0, 2, 4, 6] } },
  'P1-b finish the round so all have equal turns': { finishRound: true },
  'P1-c later seats start with extra cards 0/1/1/2': { extraStartCards: [0, 1, 1, 2] },
  // P2 big sale: hoarding for the extra turn
  'P2-a big sale gives +3 coins not an extra turn': { bigSaleExtraTurn: false, bigSaleBonus: 3 },
  'P2-b big sale needs 5 cards': { bigSale: 5 },
  'P2-c hand limit 6': { handLimit: 6 },
  'PICKS P1-a + P2-b': { startCoinsByN: { 2: [0, 3], 3: [0, 2, 4], 4: [0, 2, 4, 6] }, bigSale: 5 },
};

const opts = args();
if (!opts.profiles) opts.profiles = Object.keys(PROFILES).filter((k) => !PROFILES[k].expensive || opts.expensive);
simulate({ params: PARAMS, scenarios: SCENARIOS, profiles: PROFILES, play }, opts);

export { SCENARIOS, PROFILES, PARAMS };
