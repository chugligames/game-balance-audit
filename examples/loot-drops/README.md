# Spice Route: the Royal Chest

The drop formula from a made-up mobile game, for trying the skill. All there is to audit is
`drops.js`, a snippet the way it sits in the game's code, and these notes.

**How it makes money.** Gems are sold for real money. A chest pull costs 160 gems, and
legendary spices are what players pull for. App stores require the odds of paid random
items to be disclosed, so the Rates screen shows `RATES_TEXT`.

**What the designer wants.**
- A legendary should feel reachable: about 60 pulls on average, and never more than 90.
- What the Rates screen says must be true.
- An epic or better at least every 10 pulls, so a ten-pull never feels empty.
