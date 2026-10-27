# Strategy, board and card games

Two to five players taking turns: board games, drafting and set collection, deckbuilders,
race games, area control, competitive card games. The audit asks: **is the game fair
between seats, does no single strategy or card dominate, does skill matter, and does it
stay interesting to the end?**

## What to model

- Every rule, including setup, turn order, end condition and tie-breaks.
  Rulebooks leave gaps; log each assumption (`references/rulebook-mode.md`).
- **Hidden information:** decks, hands, face-down tiles. Bots may only see what a player
  sees.
- The game as the game interface (`actions`, `apply`, `over`, `seat`, `value`), so the
  toolkit's generic bots and `playGame` work.

## Player models

- **Strategy archetypes:** named, simple plans that a real player might follow (rush,
  hoard, sell early, chase one resource). Each is a greedy policy with different weights.
  These find dominant strategies.
- **A strong player:** `lookahead` (flat Monte Carlo) with `determinize`: a function that
  re-deals everything the player can't see (deck order, other hands) before each rollout.
  Without it the bot cheats and every skill finding is inflated. In a toy test, a
  lookahead bot that could see the deck beat a random player 88% of the time, against
  52–56% when it couldn't. Use `candidates` with a cheap `prior` to search only the most
  promising moves. **Write search-based experts in JavaScript** if you can: Python is often
  several times slower here, and expert tables can take tens of minutes.
- **A weak player:** sloppy greedy, or random among sensible moves.

Run these tables:

- **Mirror tables** (every seat plays the same archetype) for seat advantage. Seat
  differences are then the game's, not the bots'.
- **Archetype vs baseline**, with seats rotated each game so every archetype sits in every
  seat equally often. This finds dominant and dead strategies.
- **Strong vs weak**, for how much skill matters: put both bots at one table (a `strategy`
  label on each row) and use `skill` with `by: "strategy"`.
- **Re-tune after a rule change.** Archetypes are fixed policies. When a what-if rewards a
  behaviour (bonus tokens for big sales), add or re-tune an archetype that pursues it, and
  re-tune the baseline bot's thresholds too. Otherwise the gain is measured against
  opponents who ignore the new rule.
- Every player count the game supports. Balance at 2 players says little about 4.

## Metrics per seat per game

| Metric | Why it matters |
|---|---|
| `won` (1 / 0 / 1÷k on a k-way tie), `seat`, `strategy` | Seat advantage, dominance |
| final `score`, `margin` to the best other player | Close games or blowouts |
| `turns`, game length, and **minutes per game** (turns × seconds per turn: ask the designer, or assume 20–30 s for simple turns and say so) | Too long, too short, too variable. If the designer names a playtime ("about 20 minutes", the time on the box), check it at every player count: it's a goal, not a detail |
| `halfLeaderWon` (on one row per game) | Runaway leader: how often the midgame leader wins |
| `leadChanges` | Whether the lead moves around |
| `decisionImpact` at sampled turns | Whether choices matter, or the game plays itself |
| per-option counts (card bought, action used) | Dead options nobody takes (check with `used`) |

## Problems this family usually has

- **Seat advantage:** the first (or last) seat wins more than 1÷players beyond noise.
  The size that matters is small: 2–3 points at 2 players is noticeable over many plays.
- **Dominant strategy:** one archetype beats the others well beyond noise. **Dead
  options:** cards or actions that strong bots never pick.
- **Runaway leader:** the half-time leader almost always wins, so the second half is a
  formality.
- **Luck over skill, or skill wall:** the strong player barely beats the weak one, or
  always does.
- **Length:** games that drag, or vary wildly in length.

## Levers

Seat compensation (extra resource or points for later seats, a different starting hand,
bidding for first); end conditions that give everyone equal turns; costs, values and
counts of the dominant option, and of its counters; diminishing returns; catch-up rules
(bonuses for the trailing player, rewards that shrink as you lead); hidden scoring; more
or less information; removing or changing dead options.

The obvious fix often fails. Making a dominant card weaker may change nothing if the
real advantage is the timing it allows (selling first, playing first). Test every
suggestion and look for the cause in the what-if results.

## What the simulator can't tell you

Negotiation, bluffing, table talk, kingmaking between people, and whether the game is
fun. Bots also find strategies people don't, and miss ones people do. A dominant strategy
that bots find but humans don't is a risk to note, not a fact about play.
