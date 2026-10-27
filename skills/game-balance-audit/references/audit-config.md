# `audit.json`: the designer's intent as checks

`analyze.py` knows nothing about games. `audit.json` tells it what each metric means and
what the designer wants. Write it from the intent you gathered in step 1. Every check
here should trace back to something the designer said, or to a family default you named
in the report.

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
| `chart_scenarios` | Which what-ifs to draw against the baseline in `charts.html` (up to 7). Default: the first 7 |

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

Use `rise`/`fall` on difficulty proxies (energy per day, moves needed, solution length,
win rate with `fall`) and `binds` on every limit the design relies on for tension (board
space, energy, hand size, moves).

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
interval excludes `fair`. `fair: "even"` means 1 ÷ number of groups (seat win rate at a
3-player table: 0.333). Use it for seat advantage, strategy dominance, a card's win rate
when drafted, a character's win rate.

## `skill`: does being better matter?

```json
{ "metric": "won", "strong": "expert", "weak": "careless", "min_gap": 0.1, "max_gap": 0.8 }
```

Flags *luck-dominated* when the strong player's average beats the weak player's by less
than `min_gap`, and *skill-wall* when it beats it by more than `max_gap`.

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
