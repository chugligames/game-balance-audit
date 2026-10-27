# Writing `REPORT.md`

The reader is a designer. They want to know what players will run into, how sure you are,
and what to change. Write plainly, put numbers in tables, and name the player model behind
every number.

## Template

```markdown
# Balance audit: <game>

<Two or three sentences: the state of the game's balance and the one change that matters most.>

**How this was measured.** <Source: code imported / rules written as code / running build.>
<Player models, one line each.> <Runs per scenario and what that means for precision.>
<Calibration: what was checked against real data, and the gap.> Details: `game-model.md`.

**Open questions for the designer** (if any): <rule gaps or intent you had to assume>.

## Problems, most harmful first

### 1. <The problem as a player would notice it> · <severity>

**What happens.** <One paragraph: what players experience, for which player type, where.>

| <segment> | <metric> (careless) | (typical) | (expert) | Target |
|---|---|---|---|---|

**Why it matters.** <The design intent it breaks, or the benchmark it misses (with source).>

**Three suggestions, each tested** (<N> runs, same seeds as the baseline):

| | Change | <key metric>, before → after | Fixes / breaks | Cost |
|---|---|---|---|---|
| A | <tune: the exact change> | … | … | … |
| B | <rule: …> | … | … | … |
| C | <content: …> | … | … | … |

**Recommendation:** <A, B, C, or a combination, and why>. <Anything the simulator can't
show, and the playtest that would.>

### 2. …

## Recommended changes together

<The recommended picks run together as one scenario: the before → after table for the
main metrics, and anything the combination breaks that the single changes didn't.>

## Also noticed

<Lower-severity flags in one line each.>

## What this audit can't tell you

<Feel, clarity, memory, social play; the specific playtest questions that would answer them.>

## Re-running it

`<the exact commands>`
```

## Severity

| Severity | Meaning |
|---|---|
| **Blocker** | A player can't progress: an unwinnable level, an unsolvable puzzle, a game that never ends |
| **High** | Breaks a stated design intent for the focus player (no tension where it should be, a wall where there shouldn't be, a seat or strategy that wins well beyond noise) |
| **Medium** | A curve problem a player will notice over time (spikes, front-loading, a plateau, a weak comeback) |
| **Low** | Polish, or borderline results that need more runs |

## Style

- Lead each problem with what a player experiences, not with the metric's name.
- Round numbers sensibly (whole percentages, one decimal for small values) and give
  ranges when variance matters.
- Say when an effect is within sampling noise.
- Don't bury failures: if a natural fix didn't work in the simulator, say so in one line.
