# Economy and progression games

Merge-2, idle and clicker games, farming and town builders, and anything with energy,
timers, daily unlocks or a currency that flows in and out. The audit asks: **what does each
segment demand**, **when does a limit bite** for the people who actually play this way,
and, in free-to-play, **what happens at that moment**: do they watch, pay, wait or quit?
Read `references/design-goals.md` first. In an ad-funded game the energy wall is usually
the product, not the problem.

## What to model

- **Producers and costs:** generators or actions, what each costs (energy, coins, time)
  and its drop table (tier odds, chance of junk).
- **The space or inventory limit:** board cells, storage, item caps, and what happens
  when it's full (can't produce, must sell, must wait).
- **Demand:** orders, quests or goals per segment, from the game's own content files.
  Note which need several items at once.
- **Energy and timers:** cap, regeneration rate, refills (ads, chests, gems, level-ups),
  and anything that pauses regeneration.
- **The calendar:** when segments unlock (install day, daily at a set hour, after a
  timer), and how many open at install.
- **Monetisation moments:** every place the game offers an ad or a purchase (out of
  energy, a refill shop, a booster, a time skip), its reward, and its daily cap.
- **Currencies:** every source and sink, so the simulator can track the balance over time.

## Player models

Vary two things separately:

- **How well they play:** careless (20–30% of producer taps on the wrong producer; merges
  only obvious pairs), typical, efficient (never wastes; merges with a plan).
- **How they play over a day:** session times and length. Common profiles: once a day in
  the evening; twice a day (morning and evening); three times with ads and refills.
  `references/benchmarks.md` has sourced session counts and lengths.

Free-to-play games also need a **response model** at each wall: watch, pay, wait or quit
(`references/design-goals.md`). Without one, the simulator only sees players getting stuck,
never the revenue or the churn.

Then run two passes:

1. **Unlimited energy:** what each segment demands (taps, merges, minutes of play). This
   is the content's difficulty curve, free of time-gating.
2. **Real energy and calendar:** when the player runs out, how long they wait, whether they
   fall behind the calendar, and what they spend to keep going.

## Metrics to record per segment

| Metric | Why it matters |
|---|---|
| `taps` / energy spent | The core effort curve |
| `energyShare` = energy spent ÷ free energy the profile gets that day | Pressure as the player feels it |
| `outOfEnergy` (count), `waitMinutes` | Walls, and how long they last |
| `minFree` (fewest empty cells), `fullBoard` (actions taken with a full board) | Whether space ever forces a decision |
| `sells`, `usefulSells` (sold something an order needed) | Whether space costs anything |
| `merges`, `minutes` of play | Session length against genre norms |
| `daysLate` (calendar days behind) | Whether the free player keeps up |
| currency earned / spent / held | Inflation: piles of unspent currency mean its sinks are too weak |
| `wasted` (items never used) | Whether a mistake costs anything |
| `adPrompts`, `adsWatched`, `capReached` (0/1) | Revenue moments, revenue, and whether the daily ad cap is used up |
| `purchases`, currency spent on refills | Purchase moments taken |
| `quit` (0/1, then the run ends), `played` (1 per day the player opened the game) | Churn and engagement, from the response model |

## Problems this family usually has

- **Pressure never binds.** The board never fills or energy never runs out for the
  target player, so mistakes are free and nothing needs planning. (`binds` → never-binds)
- **Flat or reversed curve.** Later segments ask for no more than early ones, or less.
- **Front-loaded tightness.** A feature (sealed cells, a small starting board) makes early
  segments hard and disappears, the reverse of a ramp.
- **A wall at the wrong moment.** For premium games, any wall that stops a session the
  player wanted to continue. For free-to-play, a wall *before* the player is invested
  (first session, before the hook lands) risks quitting rather than watching. A wall that
  never comes means no revenue moment at all.
- **The ad cap.** If the target player reaches the daily ad cap early, more pressure earns
  nothing more and only adds waiting and quit risk. If they rarely reach it, ad inventory
  is going unused.
- **Inert levers.** Regeneration speed doesn't matter to someone who fills the cap
  between sessions; the cap and the session pattern do.
- **Inflation.** A currency piles up with nothing worth buying.
- **Unequal paths.** One producer chain is ordered far more than another, so half the
  content barely matters.
- **Things with no way out.** A new item that is never ordered (junk, blockers, spam)
  piles up from segment to segment, so at almost any drop rate the board jams a few
  segments later. Give it an exit (it clears at the end of a day, it can be merged away,
  or it sells for something) and test the rate again.

## Levers (see also `references/suggestions.md`)

Order size and tier; how many orders need two items at once; junk or blocker drops that
take space; the board's size or sealed cells that open later; how many orders show at
once; the energy cap (often stronger than regeneration speed); first-session energy;
unlock timing; sinks for surplus currency; time-limited orders. Monetisation levers: the
ad reward size, the daily ad cap, when in the day or the run the first wall comes, refill
prices, and whether watching gets the player back into the *same* session. Test where each
lands on the curve and on every goal in the scorecard, not just its average.

## What the simulator can't tell you

Whether a crowded board feels tense or annoying; whether players read the orders;
whether waiting feels fair. Hand these to a playtest with a specific question.
