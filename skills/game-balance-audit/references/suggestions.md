# Finding three suggestions for a problem

Every problem area gets exactly three suggestions, each tested in the simulator. Make them
**different in kind** where the problem allows, so the designer gets real choices and not
three sizes of one idea:

1. **Tune:** change a number (a cost, a count, a rate, a cap).
2. **Rule:** change how something works (an end condition, what happens when full, a
   catch-up rule).
3. **Content or structure:** change what's in the game or its order (a level, a card, an
   order list, the unlock calendar).

For each suggestion, write it so it could be implemented today, with the actual numbers
("orders on days 8–14 ask for one tier higher" rather than "make later days harder"). Add
it to the simulator as a scenario, run it, and report: the problem's key metric before →
after for each player type, the flags it fixes and the ones it introduces, its cost or
risk, and your confidence.

## Levers by problem

| Problem | Tune | Rule | Content or structure |
|---|---|---|---|
| **Too easy / no tension** (a limit never binds, flat curve) | Raise demand (order size, goal counts, targets); lower supply (drop odds, cap, moves); the cap matters more than the rate when players fill it between sessions | Make mistakes cost something (junk that takes space, a fee to undo); time-limited goals; demands that need two things at once | Add a blocker or new obstacle in later segments; introduce a new mechanic per chapter that adds load; reveal more of the board or deck later |
| **Too hard / wall** | The reverse: more moves, fewer colours, smaller goals, a bigger cap | Pity or catch-up: after N fails, an easier variant or a free helper; a first-session energy grant | Insert a breather; move the segment later; split it into a teaching step plus the hard step |
| **Spike** | Smooth the one segment toward its neighbours | Grant a helper on that segment only | Swap it with a later segment; put a breather after it |
| **Front-loaded** (tight early, eases later) | Spread the lever over time (rising junk %, rising order tier) instead of a one-off | Re-apply the limit later (cells re-seal, new blockers arrive) | Move the early-tightness feature to where tension should peak |
| **Plateau** (several segments alike) | Vary one dimension per segment | Add one new rule per segment group | Reorder, cut or merge look-alike segments |
| **Seat advantage** | Compensation for later seats (points, a resource, a card) | Equal turns at the end; bid or draft for first seat; reversed order in round two | Asymmetric starting setups |
| **Dominant strategy or card** | Raise its cost, lower its payoff, lower its count | Diminishing returns; a counter that answers it; limit how often it can be used | Add options that compete with it; change what it enables. Find the cause first: the dominant thing is often a timing edge, not a number |
| **Dead option** | Lower its cost, raise its payoff | Give it a niche (a situation where it's best) | Remove it, or merge it with another |
| **Runaway leader** | Shrink rewards as a player's lead grows | Catch-up for the trailing player; hidden scores; rewards that go to the trailing player first | Shorter game; scoring that peaks late |
| **Luck over skill** | Lower variance (smaller drop ranges, bigger hands) | More information (preview the next refill, a reroll) | Fewer random events per game |
| **Skill wall** | Smaller gap between good and adequate play | Hints, an undo, a teaching segment | Move the segment later; add a preceding level that teaches the idea |
| **Inflation** (currency piles up) | Raise sink prices, lower income | Spending with a deadline; upkeep costs | New things worth buying at the right time |
| **Unsolvable or trivial puzzle** | – | – | Replace with a generated candidate of measured difficulty; reorder |

## Choosing what to recommend

- Prefer the suggestion that fixes the problem for the **focus player** without breaking
  another check. Then the cheapest to build, then the most reversible.
- If none of the three fixes it on its own, say so, and test a combination.
- Run all the recommended picks together as one scenario before writing the report.
  Fixes interact (a bigger order and a smaller board can turn a ramp into a wall).
- Record failed suggestions in one line ("cutting saffron's coins does nothing: the edge
  comes from selling first"). That saves the designer a wasted iteration.
