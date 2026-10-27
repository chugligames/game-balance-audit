// Reference simulator for examples/loot-drops: imports the game's own drops.js. One row per
// run of 20,000 pulls; seed 1.
//   node sim.mjs --runs 400 --out runs/all.jsonl
import { args, simulate, withSeededMathRandom } from '../../../skills/game-balance-audit/scripts/sim-kit.mjs';
import * as D from '../../../examples/loot-drops/drops.js';

function play({ rand, params: p }) {
  const r = rand.child('pulls');
  const state = { sinceLegendary: 0, sinceEpic: 0 };
  let legendaries = 0, beyond90 = 0, epicGapMax = 0, gap = 0, streak = 0;
  withSeededMathRandom(r, () => {
    for (let i = 0; i < p.pulls; i++) {
      streak++;
      gap++;
      const got = D.pull(state);
      if (got === 'legendary') {
        legendaries++;
        if (streak > 90) beyond90++;
        streak = 0;
      }
      if (got !== 'rare') {
        epicGapMax = Math.max(epicGapMax, gap);
        gap = 0;
      }
    }
  });
  return { pullsPerLegendary: (p.pulls - streak) / legendaries, beyond90: beyond90 / legendaries, epicGapMax, legendaries };
}

simulate({ params: { pulls: 20000 }, profiles: { 'one player': {} }, play }, args());
