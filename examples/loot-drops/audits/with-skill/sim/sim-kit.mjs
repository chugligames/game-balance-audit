// sim-kit.mjs: zero-dependency helpers for game balance simulations (Node 18+).
//
// A simulation is the game's own rules (imported from its code wherever possible),
// some player models ("bots") and many seeded runs. Each run returns rows, one per
// segment (a day, a level, a turn or a whole game), and every row becomes one line
// of JSONL that analyze.py reads.
//
//   import { args, simulate } from './sim-kit.mjs';
//   simulate({ params: BASE, scenarios: WHAT_IFS, profiles: PLAYERS, play: playOne }, args());
//
//   node sim.mjs --runs 200 --out runs/base.jsonl
//   node sim.mjs --scenario P1-b --set orderScale=1.4 --print energy,minFree

import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname } from 'node:path';

function hash(seed, key) {
  let h = 2166136261 ^ (seed >>> 0);
  for (const ch of String(key)) h = Math.imul(h ^ ch.charCodeAt(0), 16777619);
  return h >>> 0;
}

/** Seeded random numbers (mulberry32): the same seed always replays the same run. */
export function rng(seed = 1) {
  const base = seed >>> 0;
  let a = base;
  const next = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  return {
    next,
    /** 0 … n−1 */
    int: (n) => Math.floor(next() * n),
    /** lo … hi, both included */
    range: (lo, hi) => lo + Math.floor(next() * (hi - lo + 1)),
    chance: (p) => next() < p,
    pick: (xs) => xs[Math.floor(next() * xs.length)],
    /** pairs: [[value, weight], …] */
    weighted(pairs) {
      let total = 0;
      for (const [, w] of pairs) total += w;
      let x = next() * total;
      for (const [v, w] of pairs) if ((x -= w) < 0) return v;
      return pairs[pairs.length - 1][0];
    },
    /** Shuffles in place and returns the array. */
    shuffle(xs) {
      for (let i = xs.length - 1; i > 0; i--) {
        const j = Math.floor(next() * (i + 1));
        [xs[i], xs[j]] = [xs[j], xs[i]];
      }
      return xs;
    },
    /** An independent stream, e.g. one for the deck and one for the bot. */
    fork: () => rng(Math.floor(next() * 4294967296)),
    /**
     * A stream fixed by this run's seed and a key (a level, a day), whatever happened
     * before. Give each segment its own child so that a what-if which changes level 8
     * leaves the luck of levels 9–15 exactly as it was in the baseline.
     */
    child: (key) => rng(hash(base, key)),
  };
}

/**
 * Game code that calls Math.random() becomes repeatable inside fn().
 * Use it when the sim imports the game's own rule functions.
 */
export function withSeededMathRandom(rand, fn) {
  const real = Math.random;
  Math.random = rand.next;
  try {
    return fn();
  } finally {
    Math.random = real;
  }
}

function parseValue(v) {
  if (v === undefined) return true;
  try {
    return JSON.parse(v);
  } catch {
    return v;
  }
}

/**
 * Options every sim understands:
 *   --runs N            runs per scenario and profile (default 100)
 *   --seed S            base seed (default 1)
 *   --out file.jsonl    where the rows go (default: none, print only)
 *   --scenario a,b      only these scenarios ('baseline' is always defined)
 *   --profile a,b       only these player profiles
 *   --set key=value     override one param for a quick what-if (repeatable; JSON values)
 *   --print m1,m2       print the mean of these metrics per segment when done
 *   --by field          the segment field for --print (default: day, level, turn… whichever rows have)
 * Any other --flag value lands on the result as-is.
 */
export function args(argv = process.argv.slice(2)) {
  const o = { runs: 100, seed: 1, out: null, scenarios: null, profiles: null, set: {}, print: null };
  const list = (v) => String(v).split(',').map((s) => s.trim()).filter(Boolean);
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    const hasValue = i + 1 < argv.length && !argv[i + 1].startsWith('--');
    const v = hasValue ? argv[++i] : undefined;
    if (k === '--runs') o.runs = Number(v);
    else if (k === '--seed') o.seed = Number(v);
    else if (k === '--out') o.out = v;
    else if (k === '--scenario' || k === '--scenarios') o.scenarios = [...(o.scenarios || []), ...list(v)];
    else if (k === '--profile' || k === '--profiles') o.profiles = [...(o.profiles || []), ...list(v)];
    else if (k === '--print') o.print = list(v);
    else if (k === '--set') {
      const at = v.indexOf('=');
      o.set[v.slice(0, at)] = parseValue(v.slice(at + 1));
    } else if (k.startsWith('--')) o[k.slice(2)] = parseValue(v);
  }
  return o;
}

/**
 * Plays every scenario × profile × run and writes the rows.
 *   params     the game's tunable numbers (what a what-if changes)
 *   scenarios  { name: overrides } for what-ifs; 'baseline' is {} unless given
 *   profiles   { name: player model } passed through to play()
 *   play       ({ rand, params, profile, profileName, scenario, run }) => row | row[]
 * Run r gets the same seed in every scenario and profile ("common random numbers"),
 * so a gap between two scenarios comes from the change, not from luck.
 * Every row gets { scenario, profile, run } added. A --set adds "+key=value" to the
 * scenario name so quick what-ifs never overwrite the baseline's rows.
 */
export function simulate(spec, opts = args()) {
  const { play, params = {}, scenarios = {}, profiles = { default: {} } } = spec;
  const all = { baseline: {}, ...scenarios };
  const names = opts.scenarios || Object.keys(all);
  const who = opts.profiles || Object.keys(profiles);
  const tag = Object.entries(opts.set || {}).map(([k, v]) => `+${k}=${JSON.stringify(v)}`).join('');
  const rows = [];
  for (const name of names) {
    if (!(name in all)) throw new Error(`no scenario "${name}" (have: ${Object.keys(all).join(', ')})`);
    const p = { ...params, ...all[name], ...(opts.set || {}) };
    for (const profileName of who) {
      if (!(profileName in profiles)) throw new Error(`no profile "${profileName}" (have: ${Object.keys(profiles).join(', ')})`);
      const t0 = Date.now();
      for (let run = 0; run < opts.runs; run++) {
        const rand = rng(opts.seed * 1000003 + run);
        const out = play({ rand, params: p, profile: profiles[profileName], profileName, scenario: name + tag, run });
        for (const row of [].concat(out)) rows.push({ scenario: name + tag, profile: profileName, run, ...row });
      }
      process.stderr.write(`${name + tag} / ${profileName}: ${opts.runs} runs in ${((Date.now() - t0) / 1000).toFixed(1)}s\n`);
    }
  }
  if (opts.out) writeRows(opts.out, rows);
  if (opts.print) console.log(summary(rows, opts.print, opts.by || spec.segment || guessSegment(rows)));
  return rows;
}

/** Writes rows as JSONL, creating the folder if needed. */
export function writeRows(path, rows) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, rows.map((r) => JSON.stringify(r)).join('\n') + '\n');
  process.stderr.write(`wrote ${rows.length} rows to ${path}\n`);
}

const SEGMENT_NAMES = ['segment', 'day', 'level', 'round', 'turn', 'stage', 'chapter', 'game'];
const guessSegment = (rows) => SEGMENT_NAMES.find((k) => rows.length && k in rows[0]) || 'segment';

/** A quick look while iterating: mean of each metric per segment, per scenario and profile. */
export function summary(rows, metrics, segment = 'segment') {
  const groups = new Map();
  for (const r of rows) {
    const key = `${r.scenario} / ${r.profile}`;
    if (!groups.has(key)) groups.set(key, new Map());
    const seg = r[segment] ?? 'all';
    const g = groups.get(key);
    if (!g.has(seg)) g.set(seg, []);
    g.get(seg).push(r);
  }
  const lines = [];
  for (const [key, segs] of groups) {
    lines.push(`\n${key}`);
    lines.push([segment.padEnd(8), ...metrics.map((m) => m.padStart(12))].join(''));
    for (const [seg, rs] of [...segs].sort((a, b) => (typeof a[0] === 'number' && typeof b[0] === 'number' ? a[0] - b[0] : String(a[0]).localeCompare(String(b[0]))))) {
      const cells = metrics.map((m) => {
        const xs = rs.map((r) => Number(r[m])).filter((x) => !Number.isNaN(x));
        return (xs.length ? (xs.reduce((s, x) => s + x, 0) / xs.length).toFixed(2) : '-').padStart(12);
      });
      lines.push([String(seg).padEnd(8), ...cells].join(''));
    }
  }
  return lines.join('\n');
}

// ── Generic player models ────────────────────────────────────────────────────
// They play any game written to this small interface:
//   actions(s) → legal actions        apply(s, a, rand) → next state (may mutate s)
//   over(s) → boolean                 seat(s) → whose turn (optional, default 0)
//   value(s, seat) → number, higher is better for that seat (needed by lookahead)
//   clone(s) → copy (optional, default structuredClone)
// A policy is (state, actions, rand, seat) => action.

function argmax(xs, f, rand) {
  let best = [];
  let top = -Infinity;
  for (const x of xs) {
    const v = f(x);
    if (v > top) {
      top = v;
      best = [x];
    } else if (v === top) best.push(x);
  }
  return best.length ? rand.pick(best) : xs[0];
}

export const bots = {
  /** Picks any legal action. A floor, not a player: real people are never this random. */
  random: () => (s, acts, rand) => rand.pick(acts),
  /** Takes the action with the best immediate score(s, a, seat). Ties break at random. */
  greedy: (score) => (s, acts, rand, seat) => argmax(acts, (a) => score(s, a, seat), rand),
  /** Plays like `policy`, but makes a random move with probability `mistakeRate`. */
  sloppy: (policy, mistakeRate) => (s, acts, rand, seat) =>
    rand.chance(mistakeRate) ? rand.pick(acts) : policy(s, acts, rand, seat),
  /**
   * Flat Monte Carlo: tries each action, plays `rollouts` quick games from there with
   * `playout` (random by default) and keeps the action with the best average value.
   * A strong, game-agnostic "expert". Cost: actions × rollouts × game length.
   *   determinize(state, seat, rand) → a copy with everything `seat` can't see re-dealt
   *     (deck order, other hands). Without it the bot sees hidden cards and cheats.
   *   candidates + prior(state, action, seat): only search the `candidates` actions a
   *     cheap heuristic likes best. Much faster when there are many legal moves.
   */
  lookahead: (game, { rollouts = 16, maxSteps = 200, playout = null, determinize = null, candidates = 0, prior = null } = {}) => (s, acts, rand, seat) => {
    const clone = game.clone || structuredClone;
    const follow = playout || bots.random();
    let pool = acts;
    if (candidates && prior && acts.length > candidates) {
      pool = acts.map((a) => [prior(s, a, seat), a]).sort((x, y) => y[0] - x[0]).slice(0, candidates).map((x) => x[1]);
    }
    return argmax(
      pool,
      (a) => {
        let sum = 0;
        for (let i = 0; i < rollouts; i++) {
          const start = determinize ? determinize(s, seat, rand) : clone(s);
          const next = game.apply(start, a, rand);
          sum += game.value(playGame(game, next, follow, rand, { maxSteps }).state, seat);
        }
        return sum / rollouts;
      },
      rand,
    );
  },
};

/**
 * Plays one game to the end (or maxSteps). `policies` is one policy, or one per seat.
 * Returns { state, steps, capped }: capped means it never ended, a finding in itself.
 */
export function playGame(game, state, policies, rand, { maxSteps = 10000, onStep = null } = {}) {
  let steps = 0;
  while (!game.over(state) && steps < maxSteps) {
    const acts = game.actions(state);
    if (!acts.length) break;
    const seat = game.seat ? game.seat(state) : 0;
    const policy = Array.isArray(policies) ? policies[seat] : policies;
    const a = policy(state, acts, rand, seat);
    if (onStep) onStep(state, a, seat, steps);
    state = game.apply(state, a, rand);
    steps++;
  }
  return { state, steps, capped: steps >= maxSteps && !game.over(state) };
}

/**
 * How much the choice at this moment matters: each option's average outcome over
 * `rollouts` playouts. `spread` (best − average option) near zero, game after game,
 * means the decisions don't change anything. Counting options does not show that;
 * this does.
 */
export function decisionImpact(game, state, rand, { rollouts = 24, maxSteps = 200, playout = null, determinize = null } = {}) {
  const clone = game.clone || structuredClone;
  const follow = playout || bots.random();
  const seat = game.seat ? game.seat(state) : 0;
  const acts = game.actions(state);
  const values = acts.map((a) => {
    let sum = 0;
    for (let i = 0; i < rollouts; i++) {
      const next = game.apply(determinize ? determinize(state, seat, rand) : clone(state), a, rand);
      sum += game.value(playGame(game, next, follow, rand, { maxSteps }).state, seat);
    }
    return sum / rollouts;
  });
  if (!values.length) return { options: 0, best: 0, mean: 0, spread: 0 };
  const best = Math.max(...values);
  const mean = values.reduce((s, x) => s + x, 0) / values.length;
  return { options: values.length, best, mean, spread: best - mean };
}
