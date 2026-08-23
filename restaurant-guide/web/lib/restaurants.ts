import { existsSync, readdirSync, readFileSync } from "fs";
import path from "path";
import type {
  MenuSnapshot,
  Restaurant,
  RestaurantAward,
  RestaurantRegistry,
} from "./types";

// The OPEN registry, not the 15-restaurant Michelin seed. Membership needs
// only a source and a citation -- see ADDING.md.
const REGISTRY_PATH = path.join(process.cwd(), "..", "data", "restaurants.json");
const MENUS_DIR = path.join(process.cwd(), "..", "data", "menus");

export function loadRegistry(): RestaurantRegistry {
  const raw = readFileSync(REGISTRY_PATH, "utf8");
  return JSON.parse(raw) as RestaurantRegistry;
}

export function loadRestaurants(): Restaurant[] {
  return loadRegistry().restaurants;
}

/** Restaurants that have at least one captured menu snapshot on disk. */
export function loadRestaurantsWithMenus(): Restaurant[] {
  return loadRestaurants().filter((r) => loadLatestMenu(r) !== null);
}

export function loadRestaurant(slug: string): Restaurant | undefined {
  const all = loadRestaurants();
  return (
    all.find((r) => r.slug === slug) ??
    all.find((r) => (r.aliases ?? []).includes(slug))
  );
}

/** Every slug a restaurant's menus might be filed under: its own, then any
 *  prior slug. A rename must not hide a captured menu. */
export function menuSlugs(r: Restaurant): string[] {
  return [r.slug, ...(r.aliases ?? [])];
}

export function loadLatestMenu(slugOrRestaurant: string | Restaurant): MenuSnapshot | null {
  if (typeof slugOrRestaurant !== "string") {
    for (const s of menuSlugs(slugOrRestaurant)) {
      const hit = loadLatestMenu(s);
      if (hit) return hit;
    }
    return null;
  }
  const slug = slugOrRestaurant;
  const dir = path.join(MENUS_DIR, slug);
  if (!existsSync(dir)) return null;
  const files = readdirSync(dir).filter(
    (f) => f.endsWith(".json") && !f.includes(".census."),
  );
  if (!files.length) return null;
  files.sort();
  const raw = readFileSync(path.join(dir, files[files.length - 1]), "utf8");
  return JSON.parse(raw) as MenuSnapshot;
}

/** Render an award referentially: the program's own words, verbatim.
 *  Michelin's current term for the non-starred tier is "Selected" -- NOT
 *  "Recommended", which is legacy usage and misdescribes the accolade.
 *  Word mark in plain text only: no roundel, no Bibendum, no star glyphs. */
export function awardLabel(award: RestaurantAward): string {
  return [award.program, award.tier].filter(Boolean).join(" ");
}

export function awardLabels(r: Restaurant): string[] {
  return (r.awards ?? []).map(awardLabel);
}

export const AWARD_DISCLAIMER =
  "Award names are the trademarks of their respective programs and are used " +
  "referentially to identify restaurants. Phebe is not affiliated with, " +
  "endorsed by, or sponsored by any of them.";

export function menuLabel(label: string): string {
  if (label === "sample_undated") return "Sample menu";
  if (label === "dinner") return "Dinner";
  if (label === "lunch") return "All day";
  if (label === "brunch") return "Brunch";
  return label;
}

export function formatPrice(price: number | undefined): string | null {
  if (price == null) return null;
  return Number.isInteger(price) ? `$${price}` : `$${price.toFixed(2)}`;
}
