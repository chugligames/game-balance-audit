// Merge Mini: the rules of a tiny merge-2 game (made up for the game-balance-audit skill).

export const CONFIG = {
  cols: 6,
  rows: 7,
  maxEnergy: 100,
  regenMinutes: 2, // +1 energy every 2 minutes
  tapCost: 1,
  generators: {
    oven: { chain: 'bread', cell: 0, drops: [[1, 0.85], [2, 0.15]] },
    loom: { chain: 'cloth', cell: 5, drops: [[1, 0.9], [2, 0.1]] },
  },
  chains: {
    bread: ['flour', 'dough', 'bun', 'loaf', 'cake', 'tiered cake', 'wedding cake'],
    cloth: ['thread', 'yarn', 'ribbon', 'scarf', 'shawl', 'quilt', 'tapestry'],
  },
  sellPrice: (tier) => tier, // coins
};

// Each day's orders: an order asks for `count` items of a chain at a tier.
export const DAYS = [
  /* 1 */ [{ chain: 'bread', tier: 2, count: 1 }, { chain: 'cloth', tier: 2, count: 1 }, { chain: 'bread', tier: 3, count: 1 }],
  /* 2 */ [{ chain: 'bread', tier: 3, count: 1 }, { chain: 'cloth', tier: 3, count: 1 }, { chain: 'cloth', tier: 2, count: 2 }],
  /* 3 */ [{ chain: 'bread', tier: 4, count: 1 }, { chain: 'cloth', tier: 3, count: 2 }, { chain: 'bread', tier: 3, count: 1 }],
  /* 4 */ [{ chain: 'cloth', tier: 4, count: 1 }, { chain: 'bread', tier: 4, count: 1 }, { chain: 'bread', tier: 3, count: 2 }],
  /* 5 */ [{ chain: 'bread', tier: 5, count: 1 }, { chain: 'cloth', tier: 4, count: 2 }, { chain: 'bread', tier: 4, count: 1 }],
  /* 6 */ [{ chain: 'cloth', tier: 4, count: 1 }, { chain: 'bread', tier: 3, count: 2 }, { chain: 'cloth', tier: 3, count: 1 }],
  /* 7 */ [{ chain: 'bread', tier: 4, count: 1 }, { chain: 'cloth', tier: 3, count: 2 }, { chain: 'bread', tier: 3, count: 1 }],
  /* 8 */ [{ chain: 'cloth', tier: 4, count: 2 }, { chain: 'bread', tier: 4, count: 1 }],
  /* 9 */ [{ chain: 'bread', tier: 5, count: 1 }, { chain: 'cloth', tier: 5, count: 1 }, { chain: 'bread', tier: 3, count: 1 }],
  /* 10 */ [{ chain: 'bread', tier: 6, count: 1 }, { chain: 'cloth', tier: 5, count: 1 }, { chain: 'cloth', tier: 4, count: 1 }],
];

/** A fresh board: generators in their cells, everything else empty. */
export function newBoard(config = CONFIG) {
  const cells = Array(config.cols * config.rows).fill(null);
  for (const [name, g] of Object.entries(config.generators)) cells[g.cell] = { gen: name };
  return { cells, coins: 0 };
}

const dist = (config, a, b) =>
  Math.abs((a % config.cols) - (b % config.cols)) + Math.abs(Math.floor(a / config.cols) - Math.floor(b / config.cols));

export function emptyCells(board) {
  return board.cells.flatMap((c, i) => (c === null ? [i] : []));
}

/** Tap a generator: a new item lands in the empty cell nearest to it. Returns the cell, or -1 if the board is full. */
export function tap(board, genName, rand = Math.random, config = CONFIG) {
  const g = config.generators[genName];
  const free = emptyCells(board);
  if (!free.length) return -1;
  const cell = free.reduce((best, i) => (dist(config, i, g.cell) < dist(config, best, g.cell) ? i : best));
  let x = rand();
  let tier = g.drops[g.drops.length - 1][0];
  for (const [t, p] of g.drops) {
    if ((x -= p) < 0) {
      tier = t;
      break;
    }
  }
  board.cells[cell] = { chain: g.chain, tier };
  return cell;
}

/** Drag item `from` onto item `to`. Equal items merge into the next tier at `to`. */
export function merge(board, from, to, config = CONFIG) {
  const a = board.cells[from];
  const b = board.cells[to];
  if (!a || !b || from === to || a.gen || b.gen) return false;
  if (a.chain !== b.chain || a.tier !== b.tier || a.tier >= config.chains[a.chain].length) return false;
  board.cells[to] = { chain: a.chain, tier: a.tier + 1 };
  board.cells[from] = null;
  return true;
}

/** Cells that would fill an order, or null if the board can't fill it yet. */
export function findOrder(board, order) {
  const cells = [];
  board.cells.forEach((c, i) => {
    if (c && c.chain === order.chain && c.tier === order.tier && cells.length < order.count) cells.push(i);
  });
  return cells.length === order.count ? cells : null;
}

/** Deliver an order: its items leave the board and pay coins. */
export function deliver(board, order) {
  const cells = findOrder(board, order);
  if (!cells) return false;
  for (const i of cells) board.cells[i] = null;
  board.coins += order.count * 2 ** order.tier;
  return true;
}

export function sell(board, cell, config = CONFIG) {
  const c = board.cells[cell];
  if (!c || c.gen) return false;
  board.coins += config.sellPrice(c.tier);
  board.cells[cell] = null;
  return true;
}

/** Energy after `minutes` of rest. */
export function regen(energy, minutes, config = CONFIG) {
  return Math.min(config.maxEnergy, energy + Math.floor(minutes / config.regenMinutes));
}
