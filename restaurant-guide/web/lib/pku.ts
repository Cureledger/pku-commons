import { readFileSync } from "fs";
import path from "path";
import type {
  PkuFile,
  PkuPick,
  PkuRestaurant,
  PkuScore,
  Restaurant,
} from "./types";
import { loadRestaurant, loadRestaurants } from "./restaurants";

const PKU_PATH = path.join(process.cwd(), "..", "data", "pku.json");

export function loadPkuFile(): PkuFile {
  return JSON.parse(readFileSync(PKU_PATH, "utf8")) as PkuFile;
}

export function loadPkuRestaurant(slug: string): PkuRestaurant | undefined {
  const restaurant = loadRestaurant(slug);
  const keys = new Set(
    [slug, restaurant?.slug, ...(restaurant?.aliases ?? [])].filter(
      (s): s is string => Boolean(s),
    ),
  );
  return loadPkuFile().restaurants.find((r) => keys.has(r.slug));
}

export function scorePku(
  entry: PkuRestaurant | undefined,
  restaurant?: Restaurant,
): PkuScore {
  const picks = entry?.picks ?? [];
  const mains = picks.filter((p) => p.kind === "main").length;
  const beyond = picks.filter((p) => p.kind === "beyond").length;
  const substitutes = Boolean(entry?.substitutes);
  const mntFoodCheck = Boolean(entry?.mnt_food_check);
  const publishedMenu = Boolean(restaurant?.menu_urls?.length);

  let total = 0;
  if (beyond + mains >= 1) total += 1;
  if (beyond + mains >= 3) total += 1;
  if (mains >= 1) total += 1;
  if (mains >= 2) total += 1;
  if (substitutes) total += 1;
  if (mntFoodCheck) total += 1;
  if (publishedMenu) total += 1;

  return {
    total,
    max: 7,
    mains,
    beyond,
    substitutes,
    mntFoodCheck,
    publishedMenu,
  };
}

export interface PkuCard {
  restaurant: Restaurant;
  entry: PkuRestaurant | undefined;
  score: PkuScore;
}

export function loadPkuCards(): PkuCard[] {
  return loadRestaurants()
    .map((restaurant) => {
      const entry = loadPkuRestaurant(restaurant.slug);
      return { restaurant, entry, score: scorePku(entry, restaurant) };
    })
    .filter((card) => (card.entry?.picks.length ?? 0) > 0)
    .sort((a, b) => {
      if (b.score.mntFoodCheck !== a.score.mntFoodCheck) {
        return Number(b.score.mntFoodCheck) - Number(a.score.mntFoodCheck);
      }
      if (b.score.total !== a.score.total) return b.score.total - a.score.total;
      if (b.score.mains !== a.score.mains) return b.score.mains - a.score.mains;
      if (b.score.beyond !== a.score.beyond) return b.score.beyond - a.score.beyond;
      return a.restaurant.name.localeCompare(b.restaurant.name);
    });
}

export function loadPkuCard(slug: string): PkuCard | undefined {
  const restaurant = loadRestaurant(slug);
  if (!restaurant) return undefined;
  const entry = loadPkuRestaurant(slug);
  return { restaurant, entry, score: scorePku(entry, restaurant) };
}

export function courseLabel(course: PkuPick["course"]): string {
  if (course === "starter") return "Starter";
  if (course === "main") return "Main";
  return "Side";
}

export function groupPicks(picks: PkuPick[]): { course: PkuPick["course"]; picks: PkuPick[] }[] {
  const order: PkuPick["course"][] = ["starter", "main", "side"];
  return order
    .map((course) => ({ course, picks: picks.filter((p) => p.course === course) }))
    .filter((group) => group.picks.length);
}
