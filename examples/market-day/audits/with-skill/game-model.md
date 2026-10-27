# Market Day: the game as simulated

Source: RULES.md written as code in `sim/sim.mjs` (no game code exists). Toolkit imported from the
game-balance-audit skill folder.

**Actions.** Take one market card (refill from deck; discard down to 7), or Sell 2+ cards of one good
(top coin per card, 1 coin once a stack is empty). Selling 4+ gives another turn.
**End.** A Take that can't refill the market ends the game at once. Total Takes per game is fixed:
deck after setup + 1 = 44 (2p), 41 (3p), 38 (4p).
**Randomness.** Deck order only. Hands are hidden: the expert re-deals unseen cards before each rollout.
**Params.** counts, stacks, handStart, marketSize, handLimit, minSell, emptyStackValue, bigSale,
bigSaleExtraTurn, bigSaleBonus, finishRound, startCoins / startCoinsByN, extraStartCards.

## Player models
- **steady**: greedy; takes the card whose next coin is worth most; sells a whole set at 3+, at 2 when the hand is full or the deck is nearly out.
- **quick**: sells any pair at once. **bigsale**: holds for 4-card sets. **luxury**: chases Spice/Saffron, sells them in pairs.
- **careless**: steady with 30% random moves. **expert**: flat Monte Carlo (24 rollouts, steady playouts, top 6 moves), hidden cards re-dealt.

## Assumptions (open questions for the designer)
- A1. The game ends immediately when the market can't refill; no finishing the round. (Tested both ways: it makes no difference to seat advantage.)
- A2. Unsold cards score 0. Ties are shared wins (5% of 2p games).
- A3. Over the hand limit, you discard the good you hold fewest of, cheapest first.
- A4. Discarded cards leave the game. You may take a card and sell it on a later turn only.
- A5. Hands are hidden; coins are public.

## Checks
- Replay: `TRACE=1 node sim/sim.mjs --runs 1 --profile mirror-2p --scenario baseline` traced a full game.
  Coin values, refill, hand limit and end trigger matched the rules move by move.
- Exact: Takes per game 44/41/38 reproduced in every game.
- Bot sanity: expert beats careless 75% and steady 62% (2p, 1,000 games each).
- No real playtest data, so the findings describe bots, not people.
- Constant metrics: `bigSales` is 0 for steady/quick bots (they never hold 4). The expert makes about 1 big sale a game.
