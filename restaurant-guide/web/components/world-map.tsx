"use client";

import Link from "next/link";
import { useState } from "react";
import {
  MICHELIN_DESTINATIONS,
  project,
} from "@/lib/michelin-destinations";

export interface MapCity {
  slug: string;
  name: string;
  path: string;
  count: number;
  featured?: boolean;
}

export function WorldMap({ cities }: { cities: MapCity[] }) {
  const [hoverId, setHoverId] = useState<string | null>(null);
  const cityBySlug = new Map(cities.map((city) => [city.slug, city]));
  const hovered = MICHELIN_DESTINATIONS.find((d) => d.id === hoverId);
  const hoveredCity = hovered ? cityBySlug.get(hovered.id) : undefined;

  return (
    <div>
      <div className="overflow-hidden rounded-2xl border border-line bg-[#d7ebc4]">
        <svg
          viewBox="0 15 360 140"
          className="block h-auto w-full"
          aria-label="World map of cities. Click a pin to open that city's restaurants."
        >
          <image
            href="/images/world-land.svg"
            x="0"
            y="0"
            width="360"
            height="180"
          />
          {MICHELIN_DESTINATIONS.map((destination) => {
            const city = cityBySlug.get(destination.id);
            if (!city) return null;
            const { x, y } = project(destination.lat, destination.lng);
            const isOpen = city.featured || city.count > 0;
            const isHover = hoverId === destination.id;
            const r = isOpen ? 2.35 : 1.15;
            return (
              <a
                key={destination.id}
                href={city.path}
                aria-label={city.name}
                className="cursor-pointer"
                onMouseEnter={() => setHoverId(destination.id)}
                onMouseLeave={() => setHoverId(null)}
              >
                <circle cx={x} cy={y} r={5.5} fill="transparent" />
                {isOpen ? (
                  <circle
                    cx={x}
                    cy={y}
                    r={isHover ? 4.2 : 3.6}
                    fill="#e6affc"
                    opacity={0.55}
                  />
                ) : null}
                <circle
                  cx={x}
                  cy={y}
                  r={isHover ? r + 0.45 : r}
                  fill={isOpen ? "#4f1964" : "#975ab6"}
                  stroke="#f7faf3"
                  strokeWidth={isOpen ? 0.45 : 0.28}
                />
              </a>
            );
          })}
        </svg>
      </div>

      <p className="mt-4 min-h-[1.5rem] text-center text-sm text-ink-soft">
        {hoveredCity ? (
          <Link
            href={hoveredCity.path}
            className="font-semibold text-purple no-underline hover:text-purple-deep"
          >
            {hoveredCity.name}
          </Link>
        ) : null}
      </p>
    </div>
  );
}
