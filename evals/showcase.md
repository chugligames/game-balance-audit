# With and without the skill

The same three prompts, run through Claude Code once **with** this skill and once
**without** it, with nothing else changed. All six reports are published unedited, with the
files each run produced. The one change: the absolute path to the skill on our machine
(three places) is replaced by `<skill>`, the placeholder the skill's own docs use.

| Example | With the skill | Without |
|---|---|---|
| Slot (spreadsheets) | [`examples/tiny-slot/audits/with-skill/REPORT.md`](../examples/tiny-slot/audits/with-skill/REPORT.md) | [`without-skill/REPORT.md`](../examples/tiny-slot/audits/without-skill/REPORT.md) |
| Loot drops (code snippet) | [`examples/loot-drops/audits/with-skill/REPORT.md`](../examples/loot-drops/audits/with-skill/REPORT.md) | [`without-skill/REPORT.md`](../examples/loot-drops/audits/without-skill/REPORT.md) |
| Market Day (rulebook) | [`examples/market-day/audits/with-skill/REPORT.md`](../examples/market-day/audits/with-skill/REPORT.md) | [`without-skill/REPORT.md`](../examples/market-day/audits/without-skill/REPORT.md) |

**How it was run.** `claude plugin eval . --tag showcase --scaffold`, Claude Code 2.1.311,
2026-10-27. The eval tool runs each case once with the plugin and once in a no-plugin
baseline arm.
- **Prompts:** the ones in `evals/<case>/case.yaml`. They are plain requests that don't
  name the planted problems.
- **Grading:** the report must exist, a regex must find the key number, and an LLM judge
  (the tool's default judge model, three votes) applies a six-point rubric.
- **Sample size:** one run per arm, so treat this as a worked comparison, not a statistic.

## Scores

| Example | Arm | Score | Checks passed | Turns | Minutes | Cost (USD) |
|---|---|---|---|---|---|---|
| Loot drops | with the skill | 1.00 | 3 of 3 | 15 | 4 | 0.89 |
| Loot drops | without | 1.00 | 3 of 3 | 8 | 1 | 0.30 |
| Slot | with the skill | 1.00 | 3 of 3 | 19 | 12 | 1.24 |
| Slot | without | 0.40 | 2 of 3 | 8 | 2 | 0.32 |
| Market Day | with the skill | 0.40 | 2 of 3 | 36 | 23 | 1.63 |
| Market Day | without | 0.20 | 1 of 3 | 19 | 21 | 0.79 |

Mean score: 0.80 with the skill, 0.53 without. Total cost of the six runs: $5.17.

## What we see, read by a person

The judge's verdicts are only part of the story, and one of them is wrong in plain
Claude's disfavour. Our reading of each pair:

- **Plain Claude finds the planted bugs.** On the slot and the loot chest it computed the
  exact answers (RTP 449/432; 69.5 pulls; the 91st pull) and named the causes, as well as
  the skill did. **The judge failed plain Claude's slot report, but by our reading it meets
  all six points of the rubric.** The eval tool itself warns that LLM judges are noisy on
  long reports. Read both and decide for yourself. A strong model reading a small
  spreadsheet or formula carefully doesn't need this skill to get the maths right.
- **The skill goes past the planted bug.** Its slot audit simulated 30 days of play for
  three kinds of player and found that **even at a correct 96%, the 500-coin daily gift
  keeps regular players' balances rising**. That defeats the designer's goal, and it
  tested gift rules that fix it. It did this in both of our runs. In one of its two runs,
  plain Claude noted the gift in passing with a break-even calculation, but it didn't model
  balances or test a fix in either.
- **The skill tests alternatives and shows its failures.** Every problem gets three
  suggestions with before → after numbers. Natural fixes that fail are reported as
  failures. In Market Day, "finish the round" doesn't change the seat edge, and paying
  coins for big sales instead of an extra turn backfires (from 59% to 68%).
- **The skill leaves a re-runnable audit:** seeded simulators, `audit.json`, exact-against-
  simulated checks with intervals, and the commands to reproduce every number. Plain Claude's
  reports can be re-run too: each lists its scripts, and Market Day gives intervals. None
  states its seeds, writes the goals down as checks, or tests a simulation against the
  exact answer.
- **Market Day failed the rubric in both arms.** By our reading, the skill's report missed
  only the designer's "about 20 minutes" length, which it never checked. (The skill now
  tells it to; see the changelog.) Plain Claude's report also missed comebacks (who
  leads at half time) and the length, and wrote no game model.
- **The skill costs more.** It took up to 6× the time and 2–4× the cost of plain Claude on
  these examples.

**In short:** the skill doesn't make the model better at spotting a planted bug. It makes
the audit **goal-driven, complete and checkable.** It tests alternatives, covers second-order
effects, and leaves numbers anyone can reproduce. That matters most on real games, which
aren't small enough to check by eye.

## A disclosure about the first attempt

The first run of this comparison (same day) had a grading mistake on our side. The LLM
judge was configured with `focus: files`, which shows it only the names of the files a run
wrote, not their contents. It failed every report in both arms. We fixed the configuration
(`focus: { source: file, path: balance-audit/REPORT.md }`) and ran everything again. The
scores and reports above come from that second run. The first run's reports reached the
same findings.
