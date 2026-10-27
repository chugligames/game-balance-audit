# Changelog

All notable changes to this skill. Versions follow [semantic versioning](https://semver.org):
while it's below 1.0, a minor version can change how audits are configured.

## 0.3.0 (2026-10-28)

### Added
- **Exact before estimated.** For chance systems (slots, loot tables, gacha, dice) the
  skill computes exact answers as fractions, simulates anyway, and checks that they agree.
  New `references/families/chance.md`.
- `exact` in `audit.json`: the analyser checks that the simulation's 95% interval contains
  each exact value, and flags a mismatch as the first problem.
- Spreadsheets and code snippets as inputs, with a rule to recompute every derived column.
- Two known-answer examples:
  - `tiny-slot`: spreadsheets; exact RTP 449/432;
  - `loot-drops`: a drop formula with pity; exact mean 69.50 pulls.
  Each comes with an exact answer key and an eval case.
- Unit tests for the analyser and both toolkits, including exact maths against a
  fixed-seed simulation, run by GitHub Actions on every push.
- An issue template, "Report a wrong calculation".
- A copy of `LICENSE` inside the skill folder, so installed copies carry it.
- A published with-and-without comparison on the showcase examples (`evals/showcase.md`),
  with all six reports unedited in `examples/<example>/audits/`.
- `examples/loot-drops/package.json` marks it an ES module, so Node 18 can load it.

### Changed
- `analyze.py` caches cell values and statistics. On 364,000 rows it went from over 7
  minutes to 14 seconds, with identical output.
- The strategy reference makes the agent measure minutes per game whenever the designer
  names a playtime (the showcase's Market Day audit missed it).
- Eval graders read the report itself (`focus: { source: file, ... }`). The first showcase
  run's judge saw only file names.

## 0.2.0 (2026-10-27)

### Changed
- **Audits follow the designer's goals, not player comfort.** New
  `references/design-goals.md`:
  - lenses for ad-supported, IAP, hybrid, premium, subscription, tabletop, competitive and
    teaching games;
  - watch / pay / wait / quit response models, with sensitivity checks;
  - platform rules (AdMob opt-in, disclosure of odds).

### Added
- A scorecard in `analyze.py`: every scenario against the goals (with 95% intervals) and
  constraints, with best trade-offs and bar charts.
- More checks:
  - skill gaps between strategies at one table;
  - `exclude` for reference strategies;
  - rarely used options;
  - per-profile constants;
  - group tables for every what-if, with over-corrections marked.
- `determinize` (re-deal hidden cards) and `candidates` (search the best few moves) in the
  toolkits' lookahead bot.
- Sourced monetisation and engagement benchmarks.

### Fixed
- `SKILL.md` frontmatter strings are quoted, so strict YAML parsers (the skills CLI) accept
  them.

## 0.1.0 (2026-10-27)

- First version: the workflow, JS and Python simulation toolkits, `analyze.py`
  (curve, limit, target, fairness and skill checks; what-if comparisons; charts), references
  for four game families, four example games with planted problems, and eval cases.
