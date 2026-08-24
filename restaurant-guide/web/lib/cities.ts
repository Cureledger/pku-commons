import {
  MICHELIN_DESTINATIONS,
  destinationCityId,
} from "@/lib/michelin-destinations";

export interface City {
  id: string;
  slug: string;
  name: string;
  path: string;
  line: string;
  feature?: string;
  requirePicks: boolean;
}

const FEATURES: Record<string, string> = {
  asheville:
    "The site of Camp Phebe in 2027. Arguably the best place in the world to eat low protein.",
  copenhagen: "Site of 2026 ESPKU Conference.",
};

export const CITIES: City[] = MICHELIN_DESTINATIONS.map((destination) => ({
  id: destinationCityId(destination),
  slug: destination.id,
  name: destination.name,
  path: `/${destination.id}`,
  line: `Eating low-pro in ${destination.name}`,
  feature: FEATURES[destination.id],
  requirePicks: ["asheville", "copenhagen", "dublin", "orlando"].includes(
    destination.id,
  ),
}));

export const FEATURED_CITIES = CITIES.filter((city) => city.feature);

export function cityById(id: string): City {
  return CITIES.find((city) => city.id === id) ?? CITIES[0];
}

export function cityBySlug(slug: string): City | undefined {
  return CITIES.find((city) => city.slug === slug);
}
