# Logic puzzles

Sliding-block and Rush Hour-likes, Sokoban-likes, nonograms, Sudoku variants, any pack of
deterministic puzzles with a solution. Luck plays no part. Difficulty comes from search.
The audit asks: **is every puzzle solvable, and does the pack get harder in the order the
designer intends?**

## Two kinds of measurement

1. **A solver** (breadth-first search, A*, or a constraint solver) gives the facts:
   solvable or not, the shortest solution, how many positions a full search visits,
   whether the solution is unique (for puzzles that promise one).
2. **Bounded players** estimate what a person experiences. A person doesn't search
   exhaustively. They follow a heuristic, look a move or two ahead, avoid repeating
   themselves, and give up. Model several: careless (shallow, many slips, little
   patience), typical (one move of lookahead, some slips) and the solver itself as the
   expert. Record whether they solve it and how many moves they use.

Use both. Solution length alone misranks puzzles: a short solution that first needs a move
*away* from the goal ("deceptive") is much harder for people than its length suggests, and
a long solution that repeats one idea is easier.

## Metrics per puzzle

| Metric | Why it matters |
|---|---|
| `optimal` (shortest solution, −1 if none) | Solvability and a first difficulty proxy |
| `explored` (positions a full search visits) | How big the search is |
| `branching` (legal moves at the start, or average along the solution) | How many choices a person juggles |
| `solved` by each bounded player | Difficulty as experienced |
| `moves` used when solved | Wandering: how lost a player gets |
| `solutions` (count, capped) | Uniqueness, for puzzle types that promise it |
| `deadEnds` (share of moves from the start that make it unsolvable or much longer) | Traps |

## Problems this family usually has

- **Unsolvable puzzles.** The worst possible finding: always the first problem area.
- **Ordering:** a puzzle far harder than its neighbours, or an easy one late in the pack.
- **Disagreeing proxies:** short-but-deceptive puzzles the bounded players can't solve.
  Report these as "harder than they look", which is often good design, as long as the
  order reflects it.
- **Multiple solutions** where the genre promises one (nonograms, Sudoku).
- **Trivial puzzles:** solvable in one or two moves, or by the first move a person tries.

## Levers

Reorder the pack (often the cheapest fix); replace a puzzle with one of the same type
and the right difficulty (generate candidates and pick by measured difficulty); add or
remove a blocking piece; move the goal; split a hard puzzle into a teaching puzzle plus
the hard one.

## What the simulator can't tell you

Whether the "aha" feels satisfying, whether the rules are clear, whether a deceptive
puzzle feels clever or cheap. Bounded players are rough stand-ins. When there's real
data (solve rates, time to solve, hint use), calibrate against it.
