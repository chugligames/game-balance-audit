// Spice Route: the drop formula for the Royal Chest (made up for the game-balance-audit skill).
// One pull costs 160 gems. The in-game "Rates" screen shows RATES_TEXT.

export const BASE = { legendary: 0.004, epic: 0.06 };
export const SOFT_PITY_FROM = 76; // from the 76th pull without a legendary, the chance climbs
export const SOFT_PITY_STEP = 0.05; // by 5 percentage points a pull
export const HARD_PITY = 90; // a legendary is guaranteed within 90 pulls
export const EPIC_PITY = 10; // and an epic or better within every 10
export const GEMS_PER_PULL = 160;

export const RATES_TEXT =
  'Legendary: 0.4% (1.6% overall with pity; guaranteed within 90 pulls). Epic: 6% (guaranteed within 10 pulls).';

/** Chance of a legendary on this pull. `pulls` counts this pull among those since the last legendary. */
export function legendaryChance(pulls) {
  if (pulls > HARD_PITY) return 1;
  if (pulls >= SOFT_PITY_FROM) return Math.min(1, BASE.legendary + SOFT_PITY_STEP * (pulls - SOFT_PITY_FROM));
  return BASE.legendary;
}

/** One pull. `state` = { sinceLegendary, sinceEpic }, both 0 for a new player. */
export function pull(state, rand = Math.random) {
  state.sinceLegendary += 1;
  state.sinceEpic += 1;
  if (rand() < legendaryChance(state.sinceLegendary)) {
    state.sinceLegendary = 0;
    state.sinceEpic = 0;
    return 'legendary';
  }
  if (state.sinceEpic >= EPIC_PITY || rand() < BASE.epic) {
    state.sinceEpic = 0;
    return 'epic';
  }
  return 'rare';
}
