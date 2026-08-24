/** Destinations from guide.michelin.com country hubs and city editions. */
export interface MichelinDestination {
  id: string;
  name: string;
  lat: number;
  lng: number;
  country: string;
  region?: string;
}

export const MICHELIN_DESTINATIONS: MichelinDestination[] = [
  { id: "asheville", name: "Asheville", lat: 35.6, lng: -82.55, country: "us", region: "nc" },
  { id: "copenhagen", name: "Copenhagen", lat: 55.68, lng: 12.57, country: "dk" },
  { id: "new-york", name: "New York", lat: 40.71, lng: -74.01, country: "us", region: "ny" },
  { id: "chicago", name: "Chicago", lat: 41.88, lng: -87.63, country: "us", region: "il" },
  { id: "san-francisco", name: "San Francisco", lat: 37.77, lng: -122.42, country: "us", region: "ca" },
  { id: "los-angeles", name: "Los Angeles", lat: 34.05, lng: -118.24, country: "us", region: "ca" },
  { id: "washington", name: "Washington", lat: 38.91, lng: -77.04, country: "us", region: "dc" },
  { id: "miami", name: "Miami", lat: 25.76, lng: -80.19, country: "us", region: "fl" },
  { id: "atlanta", name: "Atlanta", lat: 33.75, lng: -84.39, country: "us", region: "ga" },
  { id: "new-orleans", name: "New Orleans", lat: 29.95, lng: -90.07, country: "us", region: "la" },
  { id: "austin", name: "Austin", lat: 30.27, lng: -97.74, country: "us", region: "tx" },
  { id: "houston", name: "Houston", lat: 29.76, lng: -95.37, country: "us", region: "tx" },
  { id: "dallas", name: "Dallas", lat: 32.78, lng: -96.8, country: "us", region: "tx" },
  { id: "san-antonio", name: "San Antonio", lat: 29.42, lng: -98.49, country: "us", region: "tx" },
  { id: "denver", name: "Denver", lat: 39.74, lng: -104.99, country: "us", region: "co" },
  { id: "nashville", name: "Nashville", lat: 36.16, lng: -86.78, country: "us", region: "tn" },
  { id: "charleston", name: "Charleston", lat: 32.78, lng: -79.93, country: "us", region: "sc" },
  { id: "orlando", name: "Orlando", lat: 28.54, lng: -81.38, country: "us", region: "fl" },
  { id: "san-diego", name: "San Diego", lat: 32.72, lng: -117.16, country: "us", region: "ca" },
  { id: "toronto", name: "Toronto", lat: 43.65, lng: -79.38, country: "ca" },
  { id: "mexico-city", name: "Mexico City", lat: 19.43, lng: -99.13, country: "mx" },
  { id: "lima", name: "Lima", lat: -12.05, lng: -77.04, country: "pe" },
  { id: "buenos-aires", name: "Buenos Aires", lat: -34.6, lng: -58.38, country: "ar" },
  { id: "london", name: "London", lat: 51.51, lng: -0.13, country: "gb" },
  { id: "dublin", name: "Dublin", lat: 53.35, lng: -6.26, country: "ie" },
  { id: "paris", name: "Paris", lat: 48.86, lng: 2.35, country: "fr" },
  { id: "lyon", name: "Lyon", lat: 45.76, lng: 4.84, country: "fr" },
  { id: "amsterdam", name: "Amsterdam", lat: 52.37, lng: 4.9, country: "nl" },
  { id: "brussels", name: "Brussels", lat: 50.85, lng: 4.35, country: "be" },
  { id: "luxembourg", name: "Luxembourg", lat: 49.61, lng: 6.13, country: "lu" },
  { id: "berlin", name: "Berlin", lat: 52.52, lng: 13.4, country: "de" },
  { id: "munich", name: "Munich", lat: 48.14, lng: 11.58, country: "de" },
  { id: "zurich", name: "Zurich", lat: 47.38, lng: 8.54, country: "ch" },
  { id: "vienna", name: "Vienna", lat: 48.21, lng: 16.37, country: "at" },
  { id: "prague", name: "Prague", lat: 50.08, lng: 14.44, country: "cz" },
  { id: "budapest", name: "Budapest", lat: 47.5, lng: 19.04, country: "hu" },
  { id: "warsaw", name: "Warsaw", lat: 52.23, lng: 21.01, country: "pl" },
  { id: "krakow", name: "Krakow", lat: 50.06, lng: 19.94, country: "pl" },
  { id: "stockholm", name: "Stockholm", lat: 59.33, lng: 18.07, country: "se" },
  { id: "oslo", name: "Oslo", lat: 59.91, lng: 10.75, country: "no" },
  { id: "helsinki", name: "Helsinki", lat: 60.17, lng: 24.94, country: "fi" },
  { id: "reykjavik", name: "Reykjavik", lat: 64.15, lng: -21.94, country: "is" },
  { id: "tallinn", name: "Tallinn", lat: 59.44, lng: 24.75, country: "ee" },
  { id: "riga", name: "Riga", lat: 56.95, lng: 24.11, country: "lv" },
  { id: "vilnius", name: "Vilnius", lat: 54.69, lng: 25.28, country: "lt" },
  { id: "rome", name: "Rome", lat: 41.9, lng: 12.5, country: "it" },
  { id: "milan", name: "Milan", lat: 45.46, lng: 9.19, country: "it" },
  { id: "madrid", name: "Madrid", lat: 40.42, lng: -3.7, country: "es" },
  { id: "barcelona", name: "Barcelona", lat: 41.39, lng: 2.17, country: "es" },
  { id: "lisbon", name: "Lisbon", lat: 38.72, lng: -9.14, country: "pt" },
  { id: "athens", name: "Athens", lat: 37.98, lng: 23.73, country: "gr" },
  { id: "istanbul", name: "Istanbul", lat: 41.01, lng: 28.98, country: "tr" },
  { id: "dubai", name: "Dubai", lat: 25.2, lng: 55.27, country: "ae" },
  { id: "abu-dhabi", name: "Abu Dhabi", lat: 24.45, lng: 54.38, country: "ae" },
  { id: "doha", name: "Doha", lat: 25.29, lng: 51.53, country: "qa" },
  { id: "riyadh", name: "Riyadh", lat: 24.71, lng: 46.68, country: "sa" },
  { id: "tokyo", name: "Tokyo", lat: 35.68, lng: 139.69, country: "jp" },
  { id: "osaka", name: "Osaka", lat: 34.69, lng: 135.5, country: "jp" },
  { id: "kyoto", name: "Kyoto", lat: 35.01, lng: 135.77, country: "jp" },
  { id: "fukuoka", name: "Fukuoka", lat: 33.59, lng: 130.4, country: "jp" },
  { id: "seoul", name: "Seoul", lat: 37.57, lng: 126.98, country: "kr" },
  { id: "beijing", name: "Beijing", lat: 39.9, lng: 116.41, country: "cn" },
  { id: "shanghai", name: "Shanghai", lat: 31.23, lng: 121.47, country: "cn" },
  { id: "guangzhou", name: "Guangzhou", lat: 23.13, lng: 113.26, country: "cn" },
  { id: "hong-kong", name: "Hong Kong", lat: 22.32, lng: 114.17, country: "hk" },
  { id: "macau", name: "Macau", lat: 22.2, lng: 113.54, country: "mo" },
  { id: "taipei", name: "Taipei", lat: 25.03, lng: 121.57, country: "tw" },
  { id: "singapore", name: "Singapore", lat: 1.35, lng: 103.82, country: "sg" },
  { id: "bangkok", name: "Bangkok", lat: 13.76, lng: 100.5, country: "th" },
  { id: "phuket", name: "Phuket", lat: 7.88, lng: 98.4, country: "th" },
  { id: "kuala-lumpur", name: "Kuala Lumpur", lat: 3.14, lng: 101.69, country: "my" },
  { id: "penang", name: "Penang", lat: 5.41, lng: 100.33, country: "my" },
  { id: "manila", name: "Manila", lat: 14.6, lng: 120.98, country: "ph" },
  { id: "ho-chi-minh", name: "Ho Chi Minh City", lat: 10.82, lng: 106.63, country: "vn" },
  { id: "hanoi", name: "Hanoi", lat: 21.03, lng: 105.85, country: "vn" },
  { id: "auckland", name: "Auckland", lat: -36.85, lng: 174.76, country: "nz" },
  { id: "ljubljana", name: "Ljubljana", lat: 46.06, lng: 14.51, country: "si" },
  { id: "zagreb", name: "Zagreb", lat: 45.81, lng: 15.98, country: "hr" },
  { id: "belgrade", name: "Belgrade", lat: 44.79, lng: 20.45, country: "rs" },
  { id: "valletta", name: "Valletta", lat: 35.9, lng: 14.51, country: "mt" },
];

export function project(lat: number, lng: number): { x: number; y: number } {
  return { x: lng + 180, y: 90 - lat };
}

export function destinationCityId(destination: MichelinDestination): string {
  return [destination.id, destination.region, destination.country]
    .filter(Boolean)
    .join("-");
}
