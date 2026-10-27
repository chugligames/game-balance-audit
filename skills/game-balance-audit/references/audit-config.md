# `audit.json`: the designer's intent as checks

`analyze.py` knows nothing about games. `audit.json` tells it what the designer is
optimising for (`goals`, `constraints`), what each metric means and what the intended
experience is (`metrics`, `targets`, `groups`, `skill`). Write it from step 1. Every entry
should trace back to something the designer said, or to a default you named in the report.

```json
{
  "title": "Merge Mini",
  "segment": "day",
  "baseline": "baseline",
  "profiles": ["careless", "twice", "efficient"],
  "focus_profile": "twice",
  "metrics": {
    "taps":        { "label": "Energy spent", "expect": "rise", "segments": [3, 10] },
    "minFree":     { "label": "Fewest empty cells", "binds": "<= 0", "expect": "fall", "segments": [3, 10] },
    "outOfEnergy": { "label": "Times out of energy", "binds": "> 0", "segments": [8, 10] }
  },
  "targets": [
    { "metric": "energyShare", "segments": [8, 10], "profile": "twice", "min": 0.6, "label": "Most of the day's energy used on days 8–10" }
  ],
  "groups": [
    { "metric": "won", "by": "seat", "profile": "mirror-2p", "fair": "even", "tolerance": 0.02, "label": "Seat advantage" }
  ],
  "skill": { "metric": "won", "strong": "expert", "weak": "careless", "min_gap": 0.1 }
}
```

## Top level

| Key | Meaning |
|---|---|
| `title` | Shown on the summary and charts |
| `segment` | The row field that orders progress (`day`, `level`). Leave it out for one-shot games |
| `segment_order` | Explicit order for text segments (`["tutorial", "chapter-1", …]`) |
| `baseline` | The scenario the others are compared with (default `baseline`) |
| `profiles` | Order of player profiles in tables and charts |
| `focus_profile` | The player the design is built around. The report leads with them |
| `compare_profiles` | Profiles shown in the what-if tables. Default: the focus profile and those named in goals, constraints and targets |
| `chart_scenarios` | Which what-ifs to draw against the baseline in `charts.html` (up to 7). Default: the first 7 |

## `goals` and `constraints`: the scorecard

Each turns a metric into **one number per scenario**: within each run the metric is
aggregated over the segments named (`aggregate`: `sum` by default when there are segments,
or `mean`, `max`, `min`, `last`, `any`), then `stat` (`mean` by default, or `p10`, `p50`,
`p90`) is taken over runs, for `profile` (or the list `profiles`, or all).
`when: "> 0"` first turns the metric into 0/1, so `"aggregate": "any"` gives "the share of
players who ever hit it". `where: {"seat": 1}` keeps only matching rows (seat 1's win
rate; one strategy's games). `per: "segment"` reverses the order: each segment's mean over
runs first, then the aggregate across segments. Use it for "the hardest level's win rate"
(`"per": "segment", "aggregate": "min"`).

```json
"goals": [
  { "name": "Rewarded ads per player", "metric": "adsWatched", "profile": "twice", "direction": "max", "weight": 2 },
  { "name": "Days played", "metric": "played", "profile": "twice", "direction": "max" }
],
"constraints": [
  { "name": "Quit by Day 7", "metric": "quit", "profile": "twice", "segments": [1, 7], "aggregate": "any", "max": 0.1 }
]
```

| Key | Meaning |
|---|---|
| `name` | Shown in the scorecard |
| `direction` | Goals: `max` (default) or `min` |
| `weight` | Goals: how much this goal counts when the scorecard is sorted (default 1). Sorting only: the "best trade-off" column ignores weights |
| `min`, `max` | Constraints: the bounds a scenario must stay within |

The scorecard opens `summary.md`. For each scenario it shows each goal's value ± a 95%
interval, its change from the baseline (▲/▼ when beyond noise) and each constraint (✓/✗).
**Best trade-off** marks scenarios that keep every constraint and that no other such
scenario beats on every goal. `charts.html` draws one bar chart per goal.

## `metrics`: what each metric should do

Keyed by row field. All keys are optional except the field name itself.

| Key | Check it runs |
|---|---|
| `label` | Human name used in every message |
| `segments` | `[lo, hi]` (numbers) or a list of segment values: only check these. Use it to leave out tutorial days |
| `expect: "rise"` / `"fall"` | **Curve shape.** Flags *flat* (the last third moves less than `min_growth`, default 25%, from the first third), *reversed* (moves the wrong way), *front-loaded* (more than `front_load`, default 60%, of the change done in the first quarter), *dips* (a step against the direction bigger than `dip`, default 15%), *spike* (a step more than 3× the typical step and more than `spike`, default 25%), *plateau* (`plateau`, default 3, or more steps that barely move) |
| `breathers` | Segments where a dip is intended (the level after a hard one). They aren't flagged |
| `expect: "steady"` | Flags *unsteady* if the coefficient of variation across segments is over `tolerance` (default 15%) |
| `binds: "<= 0"` | **Constraint pressure.** The condition that means "the limit was hit" (`<= 0` free cells, `> 0` times out of energy). Flags *never-binds* (under 1% of rows) and *always-binds* (over 90%). Change the band with `binds_range: [0.05, 0.6]` |

| `used: "> 0"` | **Options nobody uses.** The condition that means "this option, reward or rule was used" (a big sale, a booster, a card bought). Flags *rarely-used* below `used_min` (default 5%) of rows |

Use `rise`/`fall` on difficulty proxies (energy per day, moves needed, solution length,
win rate with `fall`), `binds` on every limit the design relies on for tension (board
space, energy, hand size, moves), and `used` on options and rewards that should matter.

## `targets`: numbers the designer named

```json
{ "metric": "won", "profile": "typical", "segments": [10, 10], "min": 0.25, "max": 0.40, "label": "Hard level 10", "stat": "mean", "severity": "high" }
```

- `stat`: `mean` (default), `p10`, `p50`, `p90`, or `rate` (share of rows where the
  metric's `binds` condition holds).
- `profile`: whose number it is. Leave it out to check every profile.
- `severity`: `high` (default), `medium` or `low`.
- A miss whose 95% interval still overlaps the target is reported as **borderline**, with
  low severity: it may be sampling noise. Re-run with more runs before treating it as real.

## `groups`: fairness between seats, strategies or options

```json
{ "metric": "won", "by": "strategy", "profiles": ["saffron-vs-steady", "quick-vs-steady"], "fair": 0.5, "tolerance": 0.05, "label": "Strategy against the steady player" }
```

Averages `metric` for each value of the label `by` (pooled over `profile` or `profiles`)
and flags *uneven* when a group is further than `tolerance` from `fair` **and** its 95%
interval excludes `fair`. `exclude: ["steady"]` leaves a reference strategy out of the
flags (it still shows in the table). Each what-if gets the same table, before → after,
and a flag that swings past fair is marked *over-corrected*. `fair: "even"` means 1 ÷ number of groups (seat win rate at a
3-player table: 0.333). Use it for seat advantage, strategy dominance, a card's win rate
when drafted, a character's win rate.

## `skill`: does being better matter?

```json
{ "metric": "won", "strong": "expert", "weak": "careless", "min_gap": 0.1, "max_gap": 0.8 }
```

Flags *luck-dominated* when the strong player's average beats the weak player's by less
than `min_gap`, and *skill-wall* when it beats it by more than `max_gap`. `strong` and
`weak` are profiles, or, with `by` (e.g. `"by": "strategy"` plus `profile`), values of
a label at the same tables (an expert and a careless bot sitting at one table).

## Always on

- **capped:** rows marked `capped` (a run that never ended).
- **constant:** a metric that is the same in every row. Either it measures nothing, or it
  records something that never happens. Look into which; the second is often a finding.

## Reading the output

`analyze.py` prints the baseline's flags (the same finding for several player types is
merged into one line) and writes:

- `results/summary.md`: flags, per-segment tables with 10th–90th percentile ranges,
  group tables, and for each what-if the flags it **fixes**, **introduces** and leaves
  **still** flagged (with the gauge moving, e.g. `clear misses 2 → 1`), plus how the
  configured metrics change for every player type.
- `results/summary.json`: the same, for reading programmatically.
- `results/charts.html`: each configured metric across segments by player type, and
  the what-ifs for the focus player, with target bands and limits drawn in.

Flags are evidence, not the audit. Two flags can be the same problem, and a problem can
have no flag (something the bots can't feel). The report is your judgment, built on them.
