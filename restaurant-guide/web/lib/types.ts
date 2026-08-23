export interface RestaurantContact {
  email: string | null;
  phone: string | null;
  chef: string | null;
}

export interface RestaurantAward {
  program: string;
  /** The tier label VERBATIM as the program publishes it -- "Selected",
   *  "Bib Gourmand", "Green Star". Never an internal slug, never a
   *  compound: two recognitions are two entries. */
  tier: string;
  year?: string;
  edition?: string;
  citation?: string;
}

export interface RestaurantProvenance {
  /** How this record arrived: award | local_list | association |
   *  community | self_submitted | operator_import | visit.
   *  None of these ranks above another. */
  source: string;
  added_by: string;
  added_utc: string;
  citations: string[];
  also_found_via?: string[];
}

export interface RestaurantCensus {
  status: string;
  snapshot_id: string | null;
  counts: Record<string, number> | null;
  census_version: string | null;
  note: string;
}

export interface RestaurantAccommodation {
  status: string;
  value: string | null;
  verified_by: string | null;
  verified_utc: string | null;
  method: string | null;
  evidence: string | null;
  expires_utc: string | null;
  note: string;
}

export interface Restaurant {
  restaurant_id: string;
  city_id: string;
  slug: string;
  name: string;
  /** A list. A restaurant can hold several recognitions, and most hold none. */
  awards: RestaurantAward[];
  /** Which local-list category this restaurant was found under. A tag, not a
   *  rating: "Best Tapas" reports the FORMAT is compose-your-own. */
  harvest_categories?: string[];
  /** Prior slugs. Captured menus may be filed under one of these. */
  aliases?: string[];
  cuisine?: string | null;
  /** One-line style line. Awards go here in prose, not as tags. */
  blurb?: string | null;
  /** Public photo URLs, latest first. Filled from disk when present. */
  photos?: string[];
  address: string | null;
  website: string | null;
  menu_urls?: string[];
  reservation_platform: string | null;
  reservation_url?: string | null;
  contact?: RestaurantContact;
  provenance: RestaurantProvenance;
  signals?: Record<string, unknown>;
  notes: string | null;
  census: RestaurantCensus;
  accommodation: RestaurantAccommodation;
}

export interface RestaurantRegistry {
  schema_version: string;
  restaurant_count: number;
  updated_utc: string;
  restaurants: Restaurant[];
}

export interface MenuDish {
  name: string;
  description?: string;
  menu_section?: string;
  price_usd?: number;
}

export interface MenuSnapshot {
  snapshot_id: string;
  source_url: string;
  fetched_utc: string;
  menu_label: string;
  dishes: MenuDish[];
}

export type PkuCourse = "starter" | "main" | "side";
export type PkuKind = "main" | "beyond" | "potato_or_salad";

export interface PkuPick {
  name: string;
  description: string;
  course: PkuCourse;
  kind: PkuKind;
  hold?: string;
  note?: string;
  /** Appended after a rescan; shown below the first highlighted picks. */
  update?: boolean;
}

export interface PkuRestaurant {
  slug: string;
  picks: PkuPick[];
  mnt_food_check?: boolean;
  substitutes?: boolean;
  phebe_verified?: boolean;
}

export interface PkuFile {
  version: string;
  restaurants: PkuRestaurant[];
}

export type ScoreFactor =
  | "publishedMenu"
  | "main"
  | "beyond"
  | "accommodation"
  | "offMenu"
  | "award"
  | "phebeVerified";

export interface Review {
  id: string;
  slug: string;
  stars: number;
  body: string;
  by?: string;
  addedAt: number;
}

export interface ReviewFile {
  version: string;
  reviews: Review[];
}

export interface ReviewSummary {
  slug: string;
  average: number;
  count: number;
}

export interface PkuScore {
  total: number;
  max: number;
  mains: number;
  plates: number;
  beyond: number;
  substitutes: boolean;
  mntFoodCheck: boolean;
  publishedMenu: boolean;
  hasAward: boolean;
  phebeVerified: boolean;
}
