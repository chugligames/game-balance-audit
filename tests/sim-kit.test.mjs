// Unit tests for scripts/sim-kit.mjs:  node --test tests/sim-kit.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { rng, args, simulate, bots, playGame, decisionImpact, withSeededMathRandom } from '../skills/game-balance-audit/scripts/sim-kit.mjs';

test('same seed, same numbers; child ignores what ran before', () => {
  const a = rng(7), b = rng(7);
  assert.deepEqual([a.next(), a.next()], [b.next(), b.next()]);
  const c = rng(5);
  for (let i = 0; i < 100; i++) c.next();
  assert.equal(c.child(3).next(), rng(5).child(3).next());
  assert.notEqual(rng(5).child(3).next(), rng(5).child(4).next());
});

test('helpers stay in range; shuffle is a permutation', () => {
  const r = rng(1);
  for (let i = 0; i < 200; i++) {
    const x = r.int(4);
    assert.ok(x >= 0 && x < 4);
    const y = r.range(2, 3);
    assert.ok(y === 2 || y === 3);
  }
  assert.deepEqual([...r.shuffle([1, 2, 3, 4, 5])].sort(), [1, 2, 3, 4, 5]);
  let a = 0;
  for (let i = 0; i < 4000; i++) if (r.weighted([['a', 3], ['b', 1]]) === 'a') a++;
  assert.ok(Math.abs(a / 4000 - 0.75) < 0.03);
});

test('withSeededMathRandom restores Math.random and repeats', () => {
  const real = Math.random;
  const x = withSeededMathRandom(rng(3), () => Math.random());
  const y = withSeededMathRandom(rng(3), () => Math.random());
  assert.equal(x, y);
  assert.equal(Math.random, real);
});

test('simulate: rows, tags and common random numbers', () => {
  const play = ({ rand, params }) => [1, 2].map((day) => ({ day, x: rand.child(day).next() * params.k }));
  const quiet = process.stderr.write;
  process.stderr.write = () => true;
  try {
    const rows = simulate({ params: { k: 1 }, scenarios: { double: { k: 2 } }, profiles: { p: {} }, play }, args(['--runs', '3']));
    assert.equal(rows.length, 12);
    const base = rows.filter((r) => r.scenario === 'baseline').map((r) => r.x * 2);
    const dbl = rows.filter((r) => r.scenario === 'double').map((r) => r.x);
    base.forEach((x, i) => assert.ok(Math.abs(x - dbl[i]) < 1e-12));
    const set = simulate({ params: { k: 1 }, play: ({ params }) => ({ k: params.k }) }, args(['--runs', '1', '--set', 'k=5']));
    assert.equal(set[0].scenario, 'baseline+k=5');
  } finally {
    process.stderr.write = quiet;
  }
});

const toy = {
  start: (r) => ({ deck: r.shuffle(Array.from({ length: 10 }, (_, i) => i + 1)), score: [0, 0], turn: 0 }),
  actions: () => ['take', 'pass'],
  apply: (s, a) => {
    const t = { deck: [...s.deck], score: [...s.score], turn: s.turn };
    if (a === 'take') t.score[t.turn % 2] += t.deck.pop() - 5;
    t.turn++;
    return t;
  },
  over: (s) => s.turn >= 6,
  seat: (s) => s.turn % 2,
  value: (s, seat) => s.score[seat] - s.score[1 - seat],
};

test('lookahead that cannot peek is weaker than one that can', () => {
  const redeal = (s, seat, r) => ({ deck: r.shuffle([...s.deck]), score: [...s.score], turn: s.turn });
  const wins = (bot) => {
    let w = 0;
    for (let i = 0; i < 150; i++) {
      const r = rng(i);
      if (toy.value(playGame(toy, toy.start(r), [bot, bots.random()], r).state, 0) > 0) w++;
    }
    return w / 150;
  };
  assert.ok(wins(bots.lookahead(toy, { rollouts: 12 })) > wins(bots.lookahead(toy, { rollouts: 12, determinize: redeal })) + 0.15);
});

test('playGame reports a capped game; decisionImpact measures choices', () => {
  const endless = { ...toy, over: () => false };
  const r = rng(1);
  const res = playGame(endless, toy.start(r), bots.random(), r, { maxSteps: 20 });
  assert.equal(res.capped, true);
  assert.equal(res.steps, 20);
  const d = decisionImpact(toy, toy.start(rng(2)), rng(2), { rollouts: 8 });
  assert.equal(d.options, 2);
  assert.ok(d.spread >= 0);
});
