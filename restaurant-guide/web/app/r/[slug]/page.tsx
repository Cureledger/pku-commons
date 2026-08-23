import Link from "next/link";
import { notFound } from "next/navigation";
import { FavoriteHeart } from "@/components/heart";
import { ScoreLines } from "@/components/score-lines";
import { AWARD_DISCLAIMER, loadRestaurants } from "@/lib/restaurants";
import { courseLabel, groupPicks, loadPkuCard } from "@/lib/pku";

export function generateStaticParams() {
  return loadRestaurants().map((r) => ({ slug: r.slug }));
}

export default async function RestaurantPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const card = loadPkuCard(slug);
  if (!card) notFound();

  const { restaurant, entry, score } = card;
  const groups = entry ? groupPicks(entry.picks) : [];

  return (
    <main className="mx-auto max-w-3xl px-7 py-12">
      <Link
        href="/"
        className="text-sm font-semibold text-purple no-underline hover:text-purple-deep"
      >
        All restaurants
      </Link>
      <div className="mt-6 flex items-start justify-between gap-4">
        <div className="flex items-start gap-2">
          <h1 className="text-4xl font-extrabold text-purple">
            {restaurant.name}
          </h1>
          <FavoriteHeart label={restaurant.name} size={22} />
        </div>
        <p className="shrink-0 text-2xl font-extrabold text-purple">
          {score.total}/{score.max}
        </p>
      </div>
      {restaurant.blurb ? (
        <p className="mt-3 text-lg text-ink-soft">{restaurant.blurb}</p>
      ) : restaurant.cuisine ? (
        <p className="mt-3 text-lg text-ink-soft">{restaurant.cuisine}</p>
      ) : null}
      {restaurant.address ? (
        <p className="mt-2 text-ink-soft">{restaurant.address}</p>
      ) : null}

      <div className="mt-8 text-base">
        <ScoreLines score={score} menuUrl={restaurant.menu_urls?.[0]} />
      </div>

      {restaurant.reservation_url ? (
        <a
          href={restaurant.reservation_url}
          target="_blank"
          rel="noreferrer"
          className="mt-10 inline-flex items-center justify-center rounded-full bg-green px-8 py-3.5 text-base font-bold text-purple-deep no-underline hover:bg-green-deep hover:text-white"
        >
          Reserve
        </a>
      ) : null}

      {groups.length ? (
        <section className="mt-12 border-t border-line pt-10">
          <h2 className="text-2xl font-extrabold text-purple">
            Ask about these
          </h2>
          {groups.map((group) => (
            <div key={group.course} className="mt-8">
              <h3 className="text-xs font-bold uppercase tracking-[0.12em] text-green-deep">
                {courseLabel(group.course)}
              </h3>
              <ul className="mt-4 grid gap-5">
                {group.picks.map((d) => (
                  <li key={`${group.course}-${d.name}`}>
                    <div className="flex items-start justify-between gap-3">
                      <p className="font-extrabold text-purple">{d.name}</p>
                      <FavoriteHeart label={d.name} />
                    </div>
                    {d.description ? (
                      <p className="mt-1 text-sm text-ink-soft">
                        {d.description}
                      </p>
                    ) : null}
                    {d.hold ? (
                      <p className="mt-1 text-sm font-semibold text-purple">
                        Hold the: {d.hold}
                      </p>
                    ) : null}
                    {d.note ? (
                      <p className="mt-1 text-sm italic text-ink">
                        {d.note}
                      </p>
                    ) : null}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </section>
      ) : null}

      <dl className="mt-12 grid gap-6 border-t border-line pt-8 sm:grid-cols-2">
        {restaurant.website ? (
          <Fact label="Website">
            <a
              href={restaurant.website}
              className="font-semibold text-purple"
              target="_blank"
              rel="noreferrer"
            >
              {restaurant.website.replace(/^https?:\/\//, "").replace(/\/$/, "")}
            </a>
          </Fact>
        ) : null}
        {restaurant.contact?.phone ? (
          <Fact label="Phone">
            <a href={`tel:${restaurant.contact.phone}`} className="text-ink">
              {restaurant.contact.phone}
            </a>
          </Fact>
        ) : null}
        {restaurant.contact?.chef ? (
          <Fact label="Chef">{restaurant.contact.chef}</Fact>
        ) : null}
      </dl>
      <p className="mt-10 text-xs leading-relaxed text-ink/60">{AWARD_DISCLAIMER}</p>
    </main>
  );
}

function Fact({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <dt className="text-xs font-bold uppercase tracking-[0.12em] text-green-deep">
        {label}
      </dt>
      <dd className="mt-1 text-base">{children}</dd>
    </div>
  );
}
