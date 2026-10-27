// Reference harness for examples/merge-mini: the answer key for the eval, kept out of the
// example folder so an agent under test builds its own.
//   node sim.mjs --runs 100 --out runs/all.jsonl
import { args, simulate, withSeededMathRandom } from '../../../skills/game-balance-audit/scripts/sim-kit.mjs';
import * as G from '../../../examples/merge-mini/game.mjs';

const PARAMS = { regenMinutes: G.CONFIG.regenMinutes, rows: G.CONFIG.rows, orderScale: 1, finaleTier: 0 };

// What-ifs: three answers to each problem the baseline shows.
const SCENARIOS = {
  'smaller-board': { rows: 4 },
  'orders-x1.5-from-6': { orderScale: 1.5 },
  'slower-regen': { regenMinutes: 4 },
};

const PROFILES = {
  careless: { waste: 0.3, sessions: [21 * 60] },
  twice: { waste: 0.15, sessions: [8 * 60, 21 * 60] },
  efficient: { waste: 0, sessions: [8 * 60, 13 * 60, 21 * 60] },
};

const SECONDS = { tap: 1.2, merge: 1.5, deliver: 3, sell: 2 };
const SESSION_MAX = 30 * 60;

function ordersFor(day, p) {
  return G.DAYS[day - 1].map((o) => ({ ...o, count: day >= 6 ? Math.round(o.count * p.orderScale) || 1 : o.count }));
}

function play({ rand, params: p, profile }) {
  const config = { ...G.CONFIG, rows: p.rows, regenMinutes: p.regenMinutes };
  const board = G.newBoard(config);
  let energy = config.maxEnergy;
  let clock = 8 * 60; // installs at 8:00 on calendar day 0, so day 1 is open
  let lastRest = clock;
  const rows = [];
  let day = 1;
  let orders = ordersFor(1, p);
  let stat = fresh();
  function fresh() {
    return { taps: 0, merges: 0, sells: 0, outOfEnergy: 0, minFree: G.emptyCells(board).length };
  }
  const unlockedThrough = (minute) => Math.floor((minute - 6 * 60) / 1440) + 1; // day n opens at 6:00 on calendar day n-1
  const freePerDay = profile.sessions.reduce((sum, m, i, all) => {
    const gap = i === 0 ? all[all.length - 1] - 1440 : all[i - 1];
    return sum + Math.min(config.maxEnergy, Math.floor((m - gap) / config.regenMinutes));
  }, 0);

  for (let cal = 0; cal < 30 && day <= G.DAYS.length; cal++) {
    for (const start of profile.sessions) {
      const t0 = cal * 1440 + start;
      if (t0 < clock) continue;
      energy = G.regen(energy, t0 - lastRest, config);
      let spent = 0;
      while (day <= G.DAYS.length && day <= unlockedThrough(t0) && spent < SESSION_MAX) {
        const act = step(board, orders, profile, rand, config, energy);
        if (act === 'out') {
          stat.outOfEnergy++;
          break;
        }
        if (act === 'tap') {
          energy -= config.tapCost;
          stat.taps++;
        }
        if (act === 'merge') stat.merges++;
        if (act === 'sell') stat.sells++;
        spent += SECONDS[act] || 1;
        stat.minFree = Math.min(stat.minFree, G.emptyCells(board).length);
        if (orders.length === 0) {
          rows.push({ day, ...stat, energyShare: stat.taps / freePerDay, daysLate: cal - (day - 1) });
          day++;
          if (day <= G.DAYS.length) orders = ordersFor(day, p);
          stat = fresh();
        }
      }
      clock = t0 + spent / 60;
      lastRest = clock;
    }
  }
  return rows;
}

// One action by a sensible player. Returns what it did.
function step(board, orders, profile, rand, config, energy) {
  for (let i = 0; i < orders.length; i++) {
    if (G.deliver(board, orders[i])) {
      orders.splice(i, 1);
      return 'deliver';
    }
  }
  const reserved = {};
  for (const o of orders) reserved[`${o.chain}:${o.tier}`] = (reserved[`${o.chain}:${o.tier}`] || 0) + o.count;
  const top = {};
  for (const o of orders) top[o.chain] = Math.max(top[o.chain] || 0, o.tier);
  const merge = findPair(board, (c, n) => c.tier < (top[c.chain] || 0) && n - (reserved[`${c.chain}:${c.tier}`] || 0) >= 2);
  if (merge && G.merge(board, merge[0], merge[1], config)) return 'merge';
  if (G.emptyCells(board).length === 0) {
    const any = findPair(board, () => true);
    if (any && G.merge(board, any[0], any[1], config)) return 'merge';
    const junk = board.cells.findIndex((c) => c && !c.gen && !reserved[`${c.chain}:${c.tier}`]);
    if (junk >= 0 && G.sell(board, junk, config)) return 'sell';
    return 'out';
  }
  if (energy < config.tapCost) return 'out';
  // Tap the generator whose chain is furthest from its orders (in tier-1 units).
  const need = {};
  for (const o of orders) need[o.chain] = (need[o.chain] || 0) + o.count * 2 ** (o.tier - 1);
  for (const c of board.cells) if (c && !c.gen && need[c.chain] !== undefined) need[c.chain] -= 2 ** (c.tier - 1);
  const gens = Object.keys(config.generators);
  let gen = gens.reduce((a, b) => ((need[config.generators[b].chain] || 0) > (need[config.generators[a].chain] || 0) ? b : a));
  if (rand.chance(profile.waste)) gen = rand.pick(gens);
  withSeededMathRandom(rand, () => G.tap(board, gen, Math.random, config));
  return 'tap';
}

function findPair(board, ok) {
  const seen = new Map();
  const counts = new Map();
  board.cells.forEach((c) => {
    if (c && !c.gen) counts.set(`${c.chain}:${c.tier}`, (counts.get(`${c.chain}:${c.tier}`) || 0) + 1);
  });
  let best = null;
  board.cells.forEach((c, i) => {
    if (!c || c.gen) return;
    const k = `${c.chain}:${c.tier}`;
    if (!ok(c, counts.get(k))) return;
    if (seen.has(k) && (!best || c.tier < best[2])) best = [seen.get(k), i, c.tier];
    if (!seen.has(k)) seen.set(k, i);
  });
  return best;
}

simulate({ params: PARAMS, scenarios: SCENARIOS, profiles: PROFILES, play }, args());
