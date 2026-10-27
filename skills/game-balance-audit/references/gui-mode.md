# GUI mode: driving the running game

Use the real build when the rules can't be imported (a compiled engine build, a
minified bundle, server-side logic), or to check that the simulator matches the real game.
It is slow: dozens of runs, not thousands. So use it to calibrate a model, not to replace
one.

## Ways in, best first

1. **A debug hook** (ask the designer first). A few lines in a development build that
   expose state and actions, e.g. `window.__sim = { state(), actions(), act(a), seed(n) }`.
   With that, a browser script can play hundreds of quick games. Never add it to a
   production build.
2. **Browser automation without a hook.** Use whatever browser tool this environment has
   (Playwright, a browser MCP, or the user's browser extension) to read the page and click.
   Prefer reading state from the DOM or an exposed store over screenshots. Canvas games
   need screenshots and coordinates. That is slow and fragile, so keep the sample small.
3. **The game's own test or replay mode**, if it has one.

## What to measure

- The same metrics as the simulator, for the same segments, with the same player script.
- Enough runs to compare means: with 20 runs a rate is good to about ±20 points. Calibrate
  big effects, not fine ones.
- Time per action, from the real animations: it feeds session-length estimates.

## Calibrating the simulator

Run the same scripted player in the build and in the simulator for 3–5 segments, then put
the numbers side by side in `game-model.md`. Where they disagree, find the rule the
simulator has wrong before trusting any finding that depends on it.

## Safety

Use a local or staging build, never a live one with real players' data. Don't sign in to
real accounts, buy anything or trigger anything that sends messages. Seed or reset the game
between runs so results repeat.
