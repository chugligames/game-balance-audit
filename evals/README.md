# Evals

One case per example game. Each copies its example into an empty workspace, asks for an
audit in plain words (without naming the planted problems) and grades
`balance-audit/REPORT.md`.

```bash
claude plugin eval . --scaffold --allow-tools Bash Write Edit --no-publish --keep-temp
claude plugin eval . --case market-day --scaffold --allow-tools Bash Write Edit --no-publish
```

- Each case is a full agent run with simulations (often 20–60 minutes and many turns),
  so a full suite run costs real usage. Start with one case.
- `--scaffold` runs each case's `scaffold.sh`, which copies `examples/<case>/` in.
- The planted problems, and the numbers an honest audit should find, come from the
  answer-key simulators in `reference/` (one per example, with its `audit.json` and
  results). Those files are not copied into the workspace.

| Case | Planted problems | Answer key |
|---|---|---|
| merge-mini | board never crowded; energy never runs out; days 6–8 easier than day 5 | `reference/merge-mini` |
| match3-mini | level 8 unwinnable; level 10 not hard; levels 1–4 alike; level 14/15 too hard | `reference/match3-mini` |
| slide-puzzles | level 9 unsolvable; level 6 misplaced; level 10 trivial; levels 8 and 11 deceptive (found by the bots, not planted) | `reference/slide-puzzles` |
| market-day | first seat 53% (2p), last seat 28% (3p); early selling and saffron dominate; half-time leader wins ~83%; cutting saffron's coins doesn't fix it | `reference/market-day` |
