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
- **A strong player:** `lookahead` (flat Monte Carlo) with determinisation: before each
  rollout, reshuffle every card the player can't see. Without it the bot cheats and every
  skill finding is inflated.
- **A weak player:** sloppy greedy, or random among sensible moves.

Run these tables:

- **Mirror tables** (every seat plays the same archetype) for seat advantage. Seat
  differences are then the game's, not the bots'.
- **Archetype vs baseline**, with seats rotated each game so every archetype sits in every
  seat equally often. This finds dominant and dead strategies.
- **Strong vs weak**, for how much skill matters.
- Every player count the game supports. Balance at 2 players says little about 4.

## Metrics per seat per game

| Metric | Why it matters |
|---|---|
| `won` (1 / 0 / 1÷k on a k-way tie), `seat`, `strategy` | Seat advantage, dominance |
| final `score`, `margin` to the best other player | Close games or blowouts |
| `turns`, game length | Too long, too short, too variable |
| `halfLeaderWon` (on one row per game) | Runaway leader: how often the midgame leader wins |
| `leadChanges` | Whether the lead moves around |
| `decisionImpact` at sampled turns | Whether choices matter, or the game plays itself |
| per-option counts (card bought, action used) | Dead options nobody takes |

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
