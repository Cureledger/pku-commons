import { existsSync, readdirSync, readFileSync, statSync } from "fs";
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
const PHOTO_DIR = path.join(process.cwd(), "public", "images", "restaurants");

const PHOTO_EXT = /\.(png|jpe?g|webp|gif)$/i;

export function loadRestaurantPhotos(slug: string): string[] {
  const dir = path.join(PHOTO_DIR, slug);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((name) => PHOTO_EXT.test(name))
    .sort()
    .reverse()
    .map((name) => `/images/restaurants/${slug}/${encodeURIComponent(name)}`);
}

let registryCache: RestaurantRegistry | null = null;
let restaurantCache: Restaurant[] | null = null;
let registryMtime = 0;

export function loadRegistry(): RestaurantRegistry {
  const mtime = statSync(REGISTRY_PATH).mtimeMs;
  if (!registryCache || mtime !== registryMtime) {
    registryCache = JSON.parse(readFileSync(REGISTRY_PATH, "utf8")) as RestaurantRegistry;
    restaurantCache = null;
    registryMtime = mtime;
  }
  return registryCache;
}

export function loadRestaurants(): Restaurant[] {
  loadRegistry();
  if (!restaurantCache) {
    restaurantCache = loadRegistry().restaurants.map((restaurant) => ({
      ...restaurant,
      photos: restaurant.photos?.length
        ? restaurant.photos
        : loadRestaurantPhotos(restaurant.slug),
    }));
  }
  return restaurantCache;
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

/** Michelin price indication, shown verbatim. */
export function priceTier(restaurant: { price_tier?: string | null }): string | null {
  const tier = restaurant.price_tier?.trim();
  return tier || null;
}

export function restaurantMeta(restaurant: {
  price_tier?: string | null;
  cuisine?: string | null;
}): string | null {
  const parts = [priceTier(restaurant), restaurant.cuisine?.trim()].filter(
    (part): part is string => Boolean(part),
  );
  return parts.length ? parts.join(" · ") : null;
}
