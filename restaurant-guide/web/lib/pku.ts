import { readFileSync, statSync } from "fs";
import path from "path";
import type {
  PkuFile,
  PkuPick,
  PkuRestaurant,
  PkuScore,
  Restaurant,
} from "./types";
import { loadRestaurant, loadRestaurants } from "./restaurants";

export { SCORE_FACTORS } from "./score-factors";

const PKU_PATH = path.join(process.cwd(), "..", "data", "pku.json");

let pkuCache: PkuFile | null = null;
let pkuMtime = 0;

export function loadPkuFile(): PkuFile {
  const mtime = statSync(PKU_PATH).mtimeMs;
  if (!pkuCache || mtime !== pkuMtime) {
    pkuCache = JSON.parse(readFileSync(PKU_PATH, "utf8")) as PkuFile;
    pkuMtime = mtime;
  }
  return pkuCache;
}

export function loadPkuRestaurant(slug: string): PkuRestaurant | undefined {
  const restaurant = loadRestaurant(slug);
  const keys = new Set(
    [
      slug,
      restaurant?.slug,
      restaurant?.chain,
      ...(restaurant?.aliases ?? []),
    ].filter((s): s is string => Boolean(s)),
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
  const potatoOrSalad = picks.filter((p) => p.kind === "potato_or_salad").length;
  const plates = beyond + potatoOrSalad;
  const substitutes = Boolean(entry?.substitutes);
  const mntFoodCheck = Boolean(entry?.mnt_food_check);
  const publishedMenu = Boolean(restaurant?.menu_urls?.length);
  const hasAward = Boolean(restaurant?.awards?.length);
  const phebeVerified = Boolean(
    entry?.phebe_verified || restaurant?.photos?.length,
  );

  const flags = [
    publishedMenu,
    mains >= 1,
    beyond >= 1,
    substitutes,
    mntFoodCheck,
    hasAward,
    phebeVerified,
  ];
  const total = flags.filter(Boolean).length;

  return {
    total,
    max: 7,
    mains,
    plates,
    beyond,
    substitutes,
    mntFoodCheck,
    publishedMenu,
    hasAward,
    phebeVerified,
  };
}

export interface PkuCard {
  restaurant: Restaurant;
  entry: PkuRestaurant | undefined;
  score: PkuScore;
}

function awardRank(restaurant: Restaurant): number {
  const tiers = (restaurant.awards ?? []).map((award) => award.tier);
  if (tiers.includes("Three Stars")) return 3;
  if (tiers.includes("Two Stars")) return 2;
  if (tiers.includes("One Star")) return 1;
  if (tiers.includes("Bib Gourmand")) return 0;
  return -1;
}

export function loadPkuCards(
  cityId?: string,
  requirePicks = true,
): PkuCard[] {
  const pkuBySlug = new Map(
    loadPkuFile().restaurants.map((entry) => [entry.slug, entry]),
  );
  return loadRestaurants()
    .filter((restaurant) => !cityId || restaurant.city_id === cityId)
    .map((restaurant) => {
      const entry =
        pkuBySlug.get(restaurant.slug) ??
        (restaurant.chain ? pkuBySlug.get(restaurant.chain) : undefined) ??
        restaurant.aliases?.map((alias) => pkuBySlug.get(alias)).find(Boolean);
      return { restaurant, entry, score: scorePku(entry, restaurant) };
    })
    .filter((card) => {
      if (!requirePicks) return true;
      if ((card.entry?.picks.length ?? 0) > 0) return true;
      return (
        card.restaurant.provenance?.source === "operator_import" &&
        Boolean(card.restaurant.menu_urls?.length)
      );
    })
    .sort((a, b) => {
      if (b.score.total !== a.score.total) return b.score.total - a.score.total;
      if (b.score.mains !== a.score.mains) return b.score.mains - a.score.mains;
      if (b.score.plates !== a.score.plates) return b.score.plates - a.score.plates;
      const awardDelta = awardRank(b.restaurant) - awardRank(a.restaurant);
      if (awardDelta) return awardDelta;
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

export function splitHighlightedPicks(picks: PkuPick[]): {
  highlighted: PkuPick[];
  updates: PkuPick[];
} {
  return {
    highlighted: picks.filter((p) => !p.update),
    updates: picks.filter((p) => p.update),
  };
}
