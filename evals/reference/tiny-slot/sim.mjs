// Reference simulator for examples/tiny-slot: spins straight from the CSVs. One row per run
// of 10,000 one-coin spins; seed 1, so every number repeats.
//   node sim.mjs --runs 100 --out runs/all.jsonl
import { readFileSync } from 'node:fs';
import { args, simulate } from '../../../skills/game-balance-audit/scripts/sim-kit.mjs';

const rows = readFileSync(new URL('../../../examples/tiny-slot/reels.csv', import.meta.url), 'utf8').trim().split('\n').slice(1).map((l) => l.split(','));
const BASE_REELS = [1, 2, 3].map((i) => rows.map((r) => r[i]));
const SWEETS = new Set(['LADOO', 'DIYA', 'CHAI', 'MANGO']);

const PARAMS = { spins: 10000, three: { LADOO: 200, DIYA: 50, CHAI: 25, MANGO: 10 }, any: 2, chilli2: 5, chilli1: 1, swap: null };
// What-ifs: one stop changed, or one pay changed.
const SCENARIOS = {
  'reel 2: a CHILLI becomes BLANK': { swap: [1, 'CHILLI', 'BLANK'] },
  'any three sweets pays 1.5': { any: 1.5 },
  'three MANGO pays 5': { three: { LADOO: 200, DIYA: 50, CHAI: 25, MANGO: 5 } },
  'three MANGO pays 6': { three: { LADOO: 200, DIYA: 50, CHAI: 25, MANGO: 6 } }, // exact: 449/432 - 4/48 = 413/432 = 0.9560
};

function pays(p, a, b, c) {
  if (a === b && b === c && a in p.three) return p.three[a];
  if (SWEETS.has(a) && SWEETS.has(b) && SWEETS.has(c)) return p.any;
  if (a === 'CHILLI' && b === 'CHILLI') return p.chilli2;
  if (a === 'CHILLI') return p.chilli1;
  return 0;
}

function play({ rand, params: p }) {
  const reels = BASE_REELS.map((r) => [...r]);
  if (p.swap) reels[p.swap[0]][reels[p.swap[0]].indexOf(p.swap[1])] = p.swap[2];
  const r = rand.child('spins');
  let paid = 0, hits = 0, big = 0;
  for (let i = 0; i < p.spins; i++) {
    const w = pays(p, r.pick(reels[0]), r.pick(reels[1]), r.pick(reels[2]));
    paid += w;
    hits += w > 0;
    big += w >= 40;
  }
  return { rtp: paid / p.spins, hitRate: hits / p.spins, bigRate: big / p.spins };
}

simulate({ params: PARAMS, scenarios: SCENARIOS, profiles: { 'one-coin spins': {} }, play }, args());
