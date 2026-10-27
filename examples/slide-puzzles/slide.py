"""Slide Mini: the rules of a Rush Hour-style sliding block puzzle (made up for the
game-balance-audit skill).

The board is 6x6. Each block is a run of the same letter, 2 or 3 cells long, lying
across or down. Blocks slide along their own direction only. Slide block X (always
across, on row 3) out through the gap on the right edge to solve the level.
"""

SIZE = 6
EXIT_ROW = 2


def parse(rows):
    """rows: 6 strings of 6 characters, '.' for empty. Returns a state: a tuple of
    (letter, row, col, length, across) per block, sorted by letter."""
    cells = {}
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch != ".":
                cells.setdefault(ch, []).append((r, c))
    blocks = []
    for ch, pos in sorted(cells.items()):
        rs = {p[0] for p in pos}
        r0, c0 = min(pos)
        blocks.append((ch, r0, c0, len(pos), len(rs) == 1))
    return tuple(blocks)


def occupied(state):
    taken = set()
    for ch, r, c, n, across in state:
        for k in range(n):
            taken.add((r, c + k) if across else (r + k, c))
    return taken


def moves(state):
    """Every legal slide as (block index, distance); negative is left or up."""
    taken = occupied(state)
    out = []
    for i, (ch, r, c, n, across) in enumerate(state):
        for step in (-1, 1):
            d = step
            while True:
                if across:
                    cell = (r, c + d) if step < 0 else (r, c + n - 1 + d)
                else:
                    cell = (r + d, c) if step < 0 else (r + n - 1 + d, c)
                if not (0 <= cell[0] < SIZE and 0 <= cell[1] < SIZE) or cell in taken:
                    break
                out.append((i, d))
                d += step
    return out


def apply(state, move):
    i, d = move
    ch, r, c, n, across = state[i]
    block = (ch, r, c + d, n, across) if across else (ch, r + d, c, n, across)
    return state[:i] + (block,) + state[i + 1 :]


def solved(state):
    for ch, r, c, n, across in state:
        if ch == "X":
            return c + n == SIZE
    return False


def render(state):
    grid = [["."] * SIZE for _ in range(SIZE)]
    for ch, r, c, n, across in state:
        for k in range(n):
            if across:
                grid[r][c + k] = ch
            else:
                grid[r + k][c] = ch
    return ["".join(row) for row in grid]
