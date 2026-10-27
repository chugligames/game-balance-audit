// Royal Chest simulator. Baseline runs the game's own pull() from ../../drops.js;
// what-ifs run pullWith(params), a transcription checked against pull() by `--check`.
import { args, simulate, withSeededMathRandom, rng } from './sim-kit.mjs';
import * as D from '../../drops.js';

const PARAMS = {
  game: true, // true = use the game's own pull()
  baseLegendary: D.BASE.legendary, baseEpic: D.BASE.epic,
  softFrom: D.SOFT_PITY_FROM, softStep: D.SOFT_PITY_STEP,
  hardPity: D.HARD_PITY, hardInclusive: false, // false = the game's `pulls > HARD_PITY`
  epicPity: D.EPIC_PITY,
};

function pullWith(p, state, rand) {
  state.sinceLegendary += 1; state.sinceEpic += 1;
  const n = state.sinceLegendary;
  const hard = p.hardInclusive ? n >= p.hardPity : n > p.hardPity;
  const ch = hard ? 1 : n >= p.softFrom ? Math.min(1, p.baseLegendary + p.softStep * (n - p.softFrom)) : p.baseLegendary;
  if (rand() < ch) { state.sinceLegendary = 0; state.sinceEpic = 0; return 'legendary'; }
  if (state.sinceEpic >= p.epicPity || rand() < p.baseEpic) { state.sinceEpic = 0; return 'epic'; }
  return 'rare';
}

const SCENARIOS = {
  'P1-A hard pity >= 90': { game: false, hardInclusive: true },
  'P1-B base legendary 0.7%': { game: false, hardInclusive: true, baseLegendary: 0.007 },
  'P2-A base legendary 0.8%': { game: false, hardInclusive: true, baseLegendary: 0.008 },
  'P2-B soft pity from 64': { game: false, hardInclusive: true, softFrom: 64 },
  'P2-C soft pity from 66 step 10%': { game: false, hardInclusive: true, softFrom: 66, softStep: 0.10 },
};

// One run = one new player pulling until their first legendary (one 'cycle').
function play({ rand, params }) {
  const r = rand.child('cycle');
  const state = { sinceLegendary: 0, sinceEpic: 0 };
  const step = params.game ? () => withSeededMathRandom(r, () => D.pull(state)) : () => pullWith(params, state, () => r.next());
  let pulls = 0, epics = 0, gap = 0, maxGap = 0, out;
  do {
    out = step(); pulls++;
    gap = out === 'rare' ? gap + 1 : 0; maxGap = Math.max(maxGap, gap);
    if (out === 'epic') epics++;
    if (pulls > 1000) return [{ pulls, capped: true }];
  } while (out !== 'legendary');
  return [{ pulls, over60: pulls > 60 ? 1 : 0, over90: pulls > 90 ? 1 : 0, epics, epicShare: epics / pulls,
            maxRareStreak: maxGap, emptyTen: maxGap >= 10 ? 1 : 0, gems: pulls * D.GEMS_PER_PULL }];
}

if (process.argv.includes('--check')) {
  // Transcription check: same seed, game's pull() vs pullWith(baseline params), 200k pulls.
  const a = rng(7), b = rng(7), sa = { sinceLegendary: 0, sinceEpic: 0 }, sb = { ...sa };
  let diff = 0;
  for (let i = 0; i < 200000; i++) {
    const x = withSeededMathRandom(a, () => D.pull(sa)), y = pullWith(PARAMS, sb, () => b.next());
    if (x !== y) diff++;
  }
  console.log(`transcription mismatches over 200000 pulls: ${diff}`);
  // Long-run epic-or-better and legendary rates from the game's own pull().
  const c = rng(11), s = { sinceLegendary: 0, sinceEpic: 0 }; const cnt = { legendary: 0, epic: 0, rare: 0 };
  const N = 5_000_000; for (let i = 0; i < N; i++) cnt[withSeededMathRandom(c, () => D.pull(s))]++;
  console.log(`long run ${N} pulls (seed 11): legendary ${(cnt.legendary / N * 100).toFixed(3)}%  epic ${(cnt.epic / N * 100).toFixed(3)}%`);
  process.exit(0);
}

simulate({ params: PARAMS, scenarios: SCENARIOS, profiles: { player: {} }, play }, args());
