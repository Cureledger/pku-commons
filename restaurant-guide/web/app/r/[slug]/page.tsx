import Link from "next/link";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { FavoriteHeart } from "@/components/heart";
import {
  LiveScoreDots,
  PhotoProvider,
  RestaurantPhotos,
} from "@/components/restaurant-photos";
import { RestaurantReviews } from "@/components/restaurant-reviews";
import { ScoreLines } from "@/components/score-lines";
import { AWARD_DISCLAIMER, loadRestaurants } from "@/lib/restaurants";
import { loadReviews } from "@/lib/reviews";
import type { PkuPick } from "@/lib/types";
import {
  courseLabel,
  groupPicks,
  loadPkuCard,
  splitHighlightedPicks,
} from "@/lib/pku";

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
  const reviews = loadReviews(restaurant.slug);
  const { highlighted, updates } = splitHighlightedPicks(entry?.picks ?? []);
  const groups = groupPicks(highlighted);
  const updateGroups = groupPicks(updates);

  return (
    <main className="mx-auto max-w-3xl px-7 py-12">
      <PhotoProvider slug={restaurant.slug} seed={restaurant.photos ?? []}>
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
        <Suspense>
          <LiveScoreDots score={score} />
        </Suspense>
      </div>
      {restaurant.blurb ? (
        <p className="mt-3 text-lg text-ink-soft">{restaurant.blurb}</p>
      ) : restaurant.cuisine ? (
        <p className="mt-3 text-lg text-ink-soft">{restaurant.cuisine}</p>
      ) : null}
      {restaurant.address ? (
        <p className="mt-2 text-ink-soft">{restaurant.address}</p>
      ) : null}

      <Suspense>
        <RestaurantPhotos />
      </Suspense>

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

      <Suspense>
        <RestaurantReviews slug={restaurant.slug} seed={reviews} />
      </Suspense>

      {groups.length || updateGroups.length ? (
        <section className="mt-12 border-t border-line pt-10">
          {groups.length ? (
            <>
              <h2 className="text-2xl font-extrabold text-purple">
                Ask about these
              </h2>
              <PickGroups groups={groups} />
            </>
          ) : null}
          {updateGroups.length ? (
            <div className={groups.length ? "mt-12" : undefined}>
              <h2 className="text-2xl font-extrabold text-purple">
                Also on the menu
              </h2>
              <PickGroups groups={updateGroups} />
            </div>
          ) : null}
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
      </PhotoProvider>
    </main>
  );
}

function PickGroups({
  groups,
}: {
  groups: { course: PkuPick["course"]; picks: PkuPick[] }[];
}) {
  return (
    <>
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
                  <p className="mt-1 text-sm text-ink-soft">{d.description}</p>
                ) : null}
                {d.hold ? (
                  <p className="mt-1 text-sm font-semibold text-purple">
                    Hold the: {d.hold}
                  </p>
                ) : null}
                {d.note ? (
                  <p className="mt-1 text-sm italic text-ink">{d.note}</p>
                ) : null}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </>
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
