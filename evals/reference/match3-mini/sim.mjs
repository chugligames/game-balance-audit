// Reference harness for examples/match3-mini: one row per level attempt.
//   node sim.mjs --runs 200 --out runs/all.jsonl
import { readFileSync } from 'node:fs';
import { args, simulate } from '../../../skills/game-balance-audit/scripts/sim-kit.mjs';
import * as M from '../../../examples/match3-mini/match3.mjs';

const LEVELS = JSON.parse(readFileSync(new URL('../../../examples/match3-mini/levels.json', import.meta.url)));

// What-ifs edit single levels: { "<level>": { field: value } }.
const SCENARIOS = {
  'L8-easier': { edits: { 8: { moves: 20, colors: 5, goals: { blue: 22, purple: 14 } } } },
  'L10-hard': { edits: { 10: { moves: 18, colors: 6, goals: { red: 24, yellow: 14 } } } },
  'L2-4-varied': { edits: { 2: { moves: 18, goals: { blue: 16 } }, 3: { colors: 5, moves: 22, goals: { green: 14 } }, 4: { moves: 18, goals: { yellow: 10, red: 10 } } } },
};

const goalValue = (s, cleared) => Object.entries(cleared).reduce((sum, [c, n]) => sum + Math.min(n, s.goals[c] || 0), 0);

const PROFILES = {
  // Any legal swap: the floor, not a person.
  novice: { pick: (s, swaps, rand) => rand.pick(swaps) },
  // Sees only the tiles the swap itself lines up; slips 15% of the time.
  typical: {
    pick(s, swaps, rand) {
      if (rand.chance(0.15)) return rand.pick(swaps);
      return best(swaps, rand, ([a, b]) => {
        [s.grid[a], s.grid[b]] = [s.grid[b], s.grid[a]];
        const hits = M.findMatches(s);
        [s.grid[a], s.grid[b]] = [s.grid[b], s.grid[a]];
        return hits.filter((i) => {
          const c = i === a ? s.grid[b] : i === b ? s.grid[a] : s.grid[i];
          return (s.goals[c] || 0) > 0;
        }).length;
      });
    },
  },
  // Plays each swap out on a copy, chains included, and prefers moves low on the board.
  expert: {
    pick(s, swaps, rand) {
      return best(swaps, rand, (sw) => {
        const copy = { ...s, grid: [...s.grid], goals: { ...s.goals } };
        const before = { ...copy.goals };
        const r = M.play(copy, sw, rand.fork().next);
        return goalValue({ goals: before }, r.cleared) + Math.max(sw[0], sw[1]) / 1000;
      });
    },
  },
};

function best(xs, rand, f) {
  let top = -Infinity;
  let pool = [];
  for (const x of xs) {
    const v = f(x);
    if (v > top) [top, pool] = [v, [x]];
    else if (v === top) pool.push(x);
  }
  return rand.pick(pool);
}

function play({ rand, params, profile }) {
  return LEVELS.map((base) => {
    const r = rand.child(base.level); // each level keeps its own luck in every scenario
    const def = { ...base, ...((params.edits || {})[base.level] || {}) };
    const s = M.startLevel(def, r.next);
    const total = Object.values(s.goals).reduce((a, b) => a + b, 0);
    let cascades = 0;
    while (!M.won(s) && !M.lost(s)) cascades += M.play(s, profile.pick(s, M.validSwaps(s), r), r.next).cascades;
    const left = Object.values(s.goals).reduce((a, b) => a + b, 0);
    return { level: def.level, won: M.won(s) ? 1 : 0, movesLeft: M.won(s) ? s.moves : 0, goalDone: 1 - left / total, cascades, shuffles: s.shuffles };
  });
}

simulate({ params: {}, scenarios: SCENARIOS, profiles: PROFILES, play }, args());
