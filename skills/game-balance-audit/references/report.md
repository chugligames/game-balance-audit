# Writing `REPORT.md`

The reader is a designer. They want to know what players will run into, how sure you are,
and what to change. Write plainly, put numbers in tables, and name the player model behind
every number.

## Template

```markdown
# Balance audit: <game>

<Two or three sentences: the state of the game's balance and the one change that matters most.>

**Design goals.** <How the game makes money or why it exists; the primary goal; the
guardrails; who matters. Say whether the designer stated them or you inferred them.>

| Scenario | <goal 1> | <goal 2> | <constraint> | Best trade-off |
|---|---|---|---|---|
<the scorecard rows that matter: baseline, the recommended picks, notable trade-offs>

**How this was measured.** <Source: code imported / rules written as code / running build.>
<Player models, one line each.> <Runs per scenario and what that means for precision.>
<Calibration: what was checked against real data, and the gap.> Details: `game-model.md`.

**Open questions for the designer** (if any): <rule gaps or intent you had to assume>.

## Problems, most harmful first

### 1. <The problem as a player would notice it> · <severity>

**What happens.** <One paragraph: what players experience, for which player type, where,
and which design goal it hurts.>

| <segment> | <metric> (careless) | (typical) | (expert) | Target |
|---|---|---|---|---|

**Why it matters.** <The design intent it breaks, or the benchmark it misses (with source).>

**Three suggestions, each tested** (<N> runs, same seeds as the baseline):

| | Change | <key metric>, before → after | Effect on the goals (from the scorecard) | Fixes / breaks | Cost |
|---|---|---|---|---|---|
| A | <tune: the exact change> | … | … | … | … |
| B | <rule: …> | … | … | … | … |
| C | <content: …> | … | … | … | … |

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
| **High** | Breaks a guardrail or costs the primary goal (players quitting at a wall, no revenue moments in an ad-funded game, a seat or strategy that wins well beyond noise in a tabletop game) |
| **Medium** | A curve problem a player will notice over time (spikes, front-loading, a plateau, a weak comeback) |
| **Low** | Polish, or borderline results that need more runs |

## Style

- Lead each problem with what a player experiences and the goal it costs, not with the
  metric's name.
- Trade-offs are stated in the designer's units ("−0.8 rewarded ads per player per day",
  "+4 minutes per game"), never hidden inside "better balance".
- Round numbers sensibly (whole percentages, one decimal for small values) and give
  ranges when variance matters.
- Say when an effect is within sampling noise.
- Don't bury failures: if a natural fix didn't work in the simulator, say so in one line.
