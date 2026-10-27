# Design goals: what the designer is optimising for

An audit judges a game against what its maker wants. The same simulation can lead to
opposite verdicts. An energy wall on Day 3 is a bug in a paid game; in an ad-supported
game it is the main revenue moment. A first player who wins 55% is a flaw for a tabletop
publisher, and irrelevant in a solo puzzle pack. Settle the goals before judging anything.
They decide which flags are problems, which suggestions are on the table and how to rank
them.

**Never default to "make it comfortable for the player".** That is one goal among several,
and often not the one that pays for the game.

## Find out four things

1. **How the game makes money** (or why it exists): rewarded ads, in-app purchases, both,
   a one-off price, a subscription, a boxed or crowdfunded tabletop game, a competitive or
   esports title, a free passion project, a teaching tool.
2. **The primary goal, as a number the simulator can report:** rewarded ads watched per
   player per day, days played, the share of games within 2 points of a tie, minutes per
   game.
3. **Guardrails:** what must not happen. Examples: "players quit at the wall", "someone who
   plays twice a day can't finish", "first player wins over 55%", "a 4-player game runs
   past 45 minutes", "the ad cap is reached before Day 3".
4. **Who matters:** the target player's sessions and skill, and which players carry the
   business (the many free players who watch ads, or the few who pay).

**Infer before you ask.** Look in the repo for:
- ad SDKs in the dependencies (AdMob, AppLovin MAX, Unity Ads, ironSource/LevelPlay, Meta
  Audience Network);
- store or billing libraries;
- strings like "watch an ad", "free refill" and "no ads";
- energy, lives or timer systems, shop and price tables, caps such as `ADS_PER_DAY`.

A rulebook with a component list points to tabletop, and a store price to premium. Then
state what you inferred and confirm it in one short question. If nobody can answer, use
the lens's defaults below, and say so at the top of the report.

## Lenses

| Business model | Usual primary goals | Usual guardrails | What the simulator must emit |
|---|---|---|---|
| **Ad-supported free-to-play** (rewarded ads) | Rewarded ads watched per player per day, up to the cap; days played; share of players who reach the daily ad cap | Players who quit at walls; the core player can still finish; the ad cap (pressure past it earns nothing, players just wait) | `adPrompts` (times out of energy or lives), `adsWatched`, `waitMinutes`, `quit` (0/1), `daysPlayed`, `capReached` |
| **In-app purchase free-to-play** | Purchase opportunities at moments of high intent (lost by one move, one item short, out of energy mid-goal); spending on sinks | Quitting at hard levels; inflation of soft currency; "pay to win" in PvP | `nearMisses`, `offersShown`, `purchases` (from a response model), soft currency earned, spent and held |
| **Hybrid** (ads and IAP) | Both of the above. Ads from the many, purchases from the few | The same, plus ads that cannibalise purchases (a free refill that replaces a paid one) | Both sets, split by player type |
| **Premium** (paid once) | Completion; a smooth, satisfying curve; sessions that end on the player's terms | Walls, grind, difficulty spikes | Win rate or effort per segment, attempts, time to finish |
| **Subscription / live service** | Weeks retained; content consumed per week, not faster than it ships | Running out of content; burnout | Segments per week, time to exhaust content |
| **Tabletop** (boxed or crowdfunded) | Fairness between seats and strategies; tension (close finishes, lead changes, comebacks); length on the box; replayability (several viable strategies); new players can compete | Component count and cost; rules complexity; downtime between turns; the playtime printed on the box | Seat and strategy win rates, margin, lead changes, half-time-leader wins, turns and minutes per game per player count |
| **Competitive PvP** | Every option viable (win rates in the publisher's band); variety in what people play | One dominant pick; a skill ceiling too low to compete on | Win and pick rates per option, skill gap |
| **Teaching / puzzle pack** | Success with effort; a steady learning curve; completion | Unsolvable or deceptive steps without a lead-in | Solve rate, attempts, moves over optimal |

## Player response models (games that earn at certain moments)

Bots don't decide to watch an ad, pay or quit. A free-to-play audit needs an explicit model
of those decisions, because they are where the game makes money. At each wall (out of
energy or lives, a lost level with an offer), the player picks one of:

- **watch** an ad (while under the daily cap);
- **pay**;
- **wait** for regeneration or the next session;
- **quit** for good. The run stops; record `quit: 1` and stop adding rows.

Make each probability a param, and let quitting grow with what drives it:
- how early in the player's life the wall comes;
- how many walls they've hit recently;
- how long the wait is;
- whether the ad cap is already used up.

Take starting values from `references/benchmarks.md` where a sourced number exists. Where
none does, label the value as an assumption, and run a **sensitivity check**: the same
scenarios at a low, middle and high value. A recommendation that holds only for one
assumed quit rate must say so. Useful anchors (sources in `benchmarks.md`):

- **Watching at a wall.** Unity's 2024 report puts the watch rate at about 38% for ad
  placements shown when the player runs out of resources, against about 24% between
  levels. About 25–45% of daily players watch at least one rewarded ad.
- **Quitting at a wall.** No public number exists for energy walls. For difficulty walls,
  two randomised experiments (EA's match-3, and Ascarza et al.'s lives-based puzzle game
  with about 300k players) found that **easing hard spots raised engagement by 4–20%
  without lowering revenue**, and in one case raised it. Almost no early quitter ever paid.
  So a stricter wall must earn more in ad views and purchases than it loses in future
  watchers and payers who quit. Model that cost; don't assume it away.
- **Paying.** On a given day about 0.2–1% of daily players pay in median casual and
  puzzle games, and about 4.5% in top IAP-led portfolios.

```js
// One wall, one decision. Probabilities are params so the audit can vary them.
function atWall(p, player, rand) {
  const tired = Math.min(1, player.wallsToday / p.wallsBeforeAnnoyed);
  const quit = p.quitBase + p.quitPerWall * tired + (player.day <= p.newPlayerDays ? p.quitNewPlayer : 0);
  if (player.adsToday < p.adCap && rand.chance(p.watch)) return 'watch';
  if (rand.chance(p.pay)) return 'pay';
  return rand.chance(quit) ? 'quit' : 'wait';
}
```

## Writing goals into `audit.json`

Goals and constraints become a scorecard: every scenario, ranked by the designer's goals,
with the constraints it breaks marked (see `references/audit-config.md`).

```json
"goals": [
  { "name": "Rewarded ads per player", "metric": "adsWatched", "profile": "twice", "aggregate": "sum", "direction": "max", "weight": 2 },
  { "name": "Days played", "metric": "played", "profile": "twice", "aggregate": "sum", "direction": "max" }
],
"constraints": [
  { "name": "Players who quit by Day 7", "metric": "quit", "profile": "twice", "segments": [1, 7], "aggregate": "any", "max": 0.1 },
  { "name": "Twice-a-day player finishes on time", "metric": "daysLate", "profile": "twice", "aggregate": "max", "stat": "mean", "max": 0.5 }
]
```

A tabletop game's scorecard might use goals "share of games decided by 3 points or less"
(max), "half-time leader wins" (min) and "minutes per 4-player game" (target band as a
constraint), with constraints on seat win rates.

## How goals change the audit

- **What counts as a problem.** A flag matters only if it hurts a goal or breaks a
  guardrail. In an ad-supported game, "players run out of energy on Day 3" is a finding
  about *where* and *how often* the revenue moment happens. It is a problem only if they
  quit there instead of watching, or if it comes before they care enough to watch.
  Conversely, "energy never runs out" is a revenue problem: no ad prompts at all.
- **What counts as a fix.** Every suggestion is scored on every goal. A change that helps
  players but costs the primary goal (free energy in an ad-funded game) is a **trade-off**,
  shown with its price ("−0.8 ads per player per day"). It isn't recommended unless the
  designer asks for it.
- **How to recommend.** Choose from the scorecard's best trade-offs: no other scenario
  that keeps the constraints does better on every goal. State the trade-off in the
  designer's units (ads per day, minutes per game, quit rate). When goals pull against
  each other (more ads, more quits), show the curve across scenarios rather than claiming
  a free win.
- **Ad caps.** If the target player already reaches the daily ad cap, more pressure earns
  nothing more. It only adds waiting and quit risk. Then the levers are *when* the cap is
  reached (earlier means more ad-days), the cap itself, or a second placement.

## Rules of the platform are hard constraints

- **Rewarded ads must be opt-in, and declining must leave the game playable.**
  - Google AdMob: rewarded ads "must only be served after a user affirmatively and
    unambiguously opts in", and skipping one "must not impede or interfere with the normal
    usage of the platform, website or app".
  - No copy may nudge the player ("watch this ad to support us").

  So every ad-gated refill needs a non-ad path (wait, or pay), and **a simulation must
  never model an ad as the only way past a wall**. The design lever is how attractive
  watching is compared with waiting
  ([AdMob policy](https://support.google.com/admob/answer/7313578)).
- **Interstitials** (non-rewarded full-screen ads): Google Play doesn't allow them at the
  start of a level or of a content segment. They carry several times the churn per
  impression of rewarded ads.
- **Paid random items** (loot boxes, gacha): Apple (Review Guideline 3.1.1) and Google Play
  require the odds to be disclosed before purchase, and some countries regulate or ban
  them. Random rewards from an ad need disclosed odds too.
- **Games for children** have stricter ad rules (app-store family programmes, COPPA in
  the US).

Recommendations stay inside these rules, and never rely on tricks that misstate what the
player gets: fake timers, hidden costs, misleading odds.
