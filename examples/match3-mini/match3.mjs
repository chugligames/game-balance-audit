// Match-3 Mini: the rules of a tiny match-3 (made up for the game-balance-audit skill).

export const SIZE = 7;
/** On a loss the game offers extra moves for coins (coins are bought in the shop). */
export const OFFER = { extraMoves: 5, price: 900 };
export const COLORS = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'];

/** A level in play: a board with no ready-made matches, the moves left and the goals still open. */
export function startLevel(def, rand = Math.random) {
  const s = { size: SIZE, palette: COLORS.slice(0, def.colors), grid: [], moves: def.moves, goals: { ...def.goals }, shuffles: 0 };
  do {
    s.grid = Array.from({ length: SIZE * SIZE }, () => s.palette[Math.floor(rand() * s.palette.length)]);
    while (findMatches(s).length) for (const i of findMatches(s)) s.grid[i] = s.palette[Math.floor(rand() * s.palette.length)];
  } while (!validSwaps(s).length);
  return s;
}

const neighbours = (i) => {
  const out = [];
  if ((i % SIZE) < SIZE - 1) out.push(i + 1);
  if (i + SIZE < SIZE * SIZE) out.push(i + SIZE);
  return out;
};

/** Every cell that is part of a horizontal or vertical line of 3 or more. */
export function findMatches(s) {
  const hit = new Set();
  const g = s.grid;
  for (let r = 0; r < SIZE; r++) {
    for (let c = 0; c < SIZE; c++) {
      const i = r * SIZE + c;
      if (c <= SIZE - 3 && g[i] && g[i] === g[i + 1] && g[i] === g[i + 2]) [i, i + 1, i + 2].forEach((k) => hit.add(k));
      if (r <= SIZE - 3 && g[i] && g[i] === g[i + SIZE] && g[i] === g[i + 2 * SIZE]) [i, i + SIZE, i + 2 * SIZE].forEach((k) => hit.add(k));
    }
  }
  return [...hit];
}

/** Swaps that make at least one match: [[a, b], …]. */
export function validSwaps(s) {
  const out = [];
  for (let i = 0; i < SIZE * SIZE; i++) {
    for (const j of neighbours(i)) {
      if (s.grid[i] === s.grid[j]) continue;
      [s.grid[i], s.grid[j]] = [s.grid[j], s.grid[i]];
      if (findMatches(s).length) out.push([i, j]);
      [s.grid[i], s.grid[j]] = [s.grid[j], s.grid[i]];
    }
  }
  return out;
}

/**
 * Plays one move. Clears matches, drops tiles, refills from the top and repeats
 * until the board settles. Returns { cleared: {color: n}, cascades }.
 */
export function play(s, [a, b], rand = Math.random) {
  [s.grid[a], s.grid[b]] = [s.grid[b], s.grid[a]];
  s.moves--;
  const cleared = {};
  let cascades = -1;
  let hits = findMatches(s);
  while (hits.length) {
    cascades++;
    for (const i of hits) {
      cleared[s.grid[i]] = (cleared[s.grid[i]] || 0) + 1;
      s.grid[i] = null;
    }
    for (let c = 0; c < SIZE; c++) {
      const col = [];
      for (let r = SIZE - 1; r >= 0; r--) if (s.grid[r * SIZE + c]) col.push(s.grid[r * SIZE + c]);
      for (let r = SIZE - 1, k = 0; r >= 0; r--, k++) s.grid[r * SIZE + c] = col[k] || s.palette[Math.floor(rand() * s.palette.length)];
    }
    hits = findMatches(s);
  }
  for (const [color, n] of Object.entries(cleared)) if (color in s.goals) s.goals[color] = Math.max(0, s.goals[color] - n);
  while (!validSwaps(s).length) {
    s.shuffles++;
    for (let i = s.grid.length - 1; i > 0; i--) {
      const j = Math.floor(rand() * (i + 1));
      [s.grid[i], s.grid[j]] = [s.grid[j], s.grid[i]];
    }
    while (findMatches(s).length) for (const i of findMatches(s)) s.grid[i] = s.palette[Math.floor(rand() * s.palette.length)];
  }
  return { cleared, cascades: Math.max(0, cascades) };
}

export const won = (s) => Object.values(s.goals).every((n) => n === 0);
export const lost = (s) => !won(s) && s.moves <= 0;
