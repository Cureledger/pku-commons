import Link from "next/link";
import { WorldMap } from "@/components/world-map";
import { CITIES, FEATURED_CITIES } from "@/lib/cities";
import { loadPkuCards } from "@/lib/pku";

const HERO_POINTS = [
  "Restaurant meals are a rare treat for PKUers on diet, made even harder by not knowing where to go.",
  "Not all restaurants publish their menus, which makes it even harder for PKU families to plan a special outing.",
  "Phebe Eats integrates with the Phebe App so you can log your restaurant meals and favorites.",
  "Phebe Eats makes it easy to stay on track, even when you're on the go.",
];

export default function HomePage() {
  const cities = CITIES.map((city) => ({
    slug: city.slug,
    name: city.name,
    path: city.path,
    count: loadPkuCards(city.id, city.requirePicks).length,
    featured: Boolean(city.feature),
  }));

  return (
    <main>
      <section className="bg-green">
        <div className="mx-auto max-w-[1120px] px-7 py-8 md:py-12">
          <h1 className="text-4xl font-extrabold text-purple sm:text-5xl">
            Eating out around the world with PKU
          </h1>
          <ul className="mt-6 max-w-3xl list-disc space-y-2 pl-5 text-base text-purple sm:text-lg">
            {HERO_POINTS.map((point) => (
              <li key={point}>{point}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="mx-auto max-w-[1120px] px-7 py-6 md:py-8">
        <WorldMap cities={cities} />
      </section>

      <section className="mx-auto max-w-[1120px] px-7 pb-14">
        <h2 className="text-xs font-bold uppercase tracking-[0.12em] text-purple">
          Featured Cities
        </h2>
        <ul className="mt-4 grid gap-4 sm:grid-cols-2">
          {FEATURED_CITIES.map((city) => (
            <li key={city.id}>
              <Link
                href={city.path}
                className="block h-full rounded-2xl border border-line bg-white p-5 no-underline transition-colors hover:border-green-deep/40 hover:bg-green-pale"
              >
                <h3 className="text-2xl font-extrabold text-purple">
                  {city.name}
                </h3>
                <p className="mt-2 text-sm text-ink-soft">{city.feature}</p>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
