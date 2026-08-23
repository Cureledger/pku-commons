import { readFileSync } from "fs";
import path from "path";
import type {
  PkuFile,
  PkuPick,
  PkuRestaurant,
  PkuScore,
  Restaurant,
  ScoreFactor,
} from "./types";
import { loadRestaurant, loadRestaurants } from "./restaurants";

export const SCORE_FACTORS: { id: ScoreFactor; label: string; line: string }[] = [
  {
    id: "publishedMenu",
    label: "Published menu",
    line: "Restaurant posts a current menu.",
  },
  {
    id: "main",
    label: "A main",
    line: "Restaurant offers a low-protein main.",
  },
  {
    id: "beyond",
    label: "Plates beyond potato and salad",
    line: "Restaurant offers low-protein plates beyond potato and salad.",
  },
  {
    id: "accommodation",
    label: "Accommodation",
    line: "Restaurant will substitute on request.",
  },
  {
    id: "offMenu",
    label: "Off-menu",
    line: "Restaurant will cook off menu with sufficient notice.",
  },
  {
    id: "award",
    label: "Award",
    line: "Restaurant has received a third party award.",
  },
  {
    id: "phebeVerified",
    label: "Phebe-verified",
    line: "Restaurant has been verified by the Phebe community.",
  },
];

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
  const potatoOrSalad = picks.filter((p) => p.kind === "potato_or_salad").length;
  const plates = beyond + potatoOrSalad;
  const substitutes = Boolean(entry?.substitutes);
  const mntFoodCheck = Boolean(entry?.mnt_food_check);
  const publishedMenu = Boolean(restaurant?.menu_urls?.length);
  const hasAward = Boolean(restaurant?.awards?.length);
  const phebeVerified = Boolean(entry?.phebe_verified);

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

export function loadPkuCards(): PkuCard[] {
  return loadRestaurants()
    .map((restaurant) => {
      const entry = loadPkuRestaurant(restaurant.slug);
      return { restaurant, entry, score: scorePku(entry, restaurant) };
    })
    .filter((card) => (card.entry?.picks.length ?? 0) > 0)
    .sort((a, b) => {
      if (b.score.total !== a.score.total) return b.score.total - a.score.total;
      if (b.score.mains !== a.score.mains) return b.score.mains - a.score.mains;
      if (b.score.plates !== a.score.plates) return b.score.plates - a.score.plates;
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
