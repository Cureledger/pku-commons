import Link from "next/link";
import { EyeglassesMark } from "@/components/eyeglasses-mark";
import { FavoriteHeart } from "@/components/heart";
import { HeartMark } from "@/components/heart-mark";
import { PhebeMark } from "@/components/phebe-mark";
import { ReviewStars } from "@/components/restaurant-reviews";
import { ScoreDots } from "@/components/score-dots";
import { ScoreLines } from "@/components/score-lines";
import type { City } from "@/lib/cities";
import { AWARD_DISCLAIMER, restaurantMeta } from "@/lib/restaurants";
import { SCORE_FACTORS, loadPkuCards } from "@/lib/pku";
import { loadReviewSummaries } from "@/lib/reviews";

export function CityDirectory({ city }: { city: City }) {
  const cards = loadPkuCards(city.id, city.requirePicks);
  const reviewSummaries = loadReviewSummaries();

  return (
    <main>
      <section className="bg-green">
        <div className="mx-auto max-w-[1120px] px-7 py-16 md:py-20">
          <Link
            href="/"
            className="text-sm font-semibold text-purple no-underline hover:text-purple-deep"
          >
            Map
          </Link>
          <p className="mt-6 text-xs font-bold uppercase tracking-[0.12em] text-purple">
            Phebe Eats
          </p>
          <h1 className="mt-3 text-4xl font-extrabold text-purple sm:text-5xl">
            {city.line}
          </h1>
        </div>
      </section>

      <section className="border-b border-line bg-green-pale">
        <div className="mx-auto max-w-[1120px] px-7 py-8">
          <div className="mx-auto max-w-xl rounded-2xl border border-purple/30 bg-white px-7 py-6">
            <div className="flex items-center justify-center gap-4">
              <p className="text-xs font-bold uppercase tracking-[0.12em] text-purple">
                Our scale
              </p>
              <ul
                className="flex items-center gap-1"
                aria-label="Seven dots, five filled"
              >
                {Array.from({ length: 7 }, (_, i) => (
                  <li key={i}>
                    <span
                      className={`block h-2.5 w-2.5 rounded-full ${
                        i < 5
                          ? "bg-purple"
                          : "border border-purple/35 bg-transparent"
                      }`}
                    />
                  </li>
                ))}
              </ul>
            </div>
            <ul className="mt-4 grid gap-1.5 text-sm text-ink">
              {SCORE_FACTORS.map((factor) => (
                <li key={factor.id} className="flex items-baseline gap-2">
                  <span
                    className="mt-1 inline-block h-2.5 w-2.5 shrink-0 rounded-full bg-purple"
                    aria-hidden
                  />
                  {factor.line}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="border-b border-line bg-green-pale">
        <dl className="mx-auto flex max-w-[1120px] flex-col gap-1 px-7 py-4 text-sm text-ink">
          <div className="flex items-baseline gap-x-2">
            <dt className="shrink-0 font-extrabold text-purple">main</dt>
            <dd>Entrees and main dishes.</dd>
          </div>
          <div className="flex items-baseline gap-x-2">
            <dt className="shrink-0 font-extrabold text-purple">plates</dt>
            <dd>Sides, starters, desserts.</dd>
          </div>
          <div className="flex items-baseline gap-x-2">
            <dt className="shrink-0 font-extrabold text-purple">
              [] accommodation
            </dt>
            <dd>Restaurant will substitute.</dd>
          </div>
          <div className="flex items-center gap-x-2">
            <dt className="flex shrink-0 items-center gap-1.5 font-extrabold text-purple">
              [] <PhebeMark size={16} alt="" />
            </dt>
            <dd>Restaurant will cook off-menu.</dd>
          </div>
          <div className="flex items-center gap-x-2">
            <dt className="flex shrink-0 items-center gap-1.5 font-extrabold text-purple">
              <EyeglassesMark size={16} />
            </dt>
            <dd>View menu.</dd>
          </div>
          <div className="flex items-center gap-x-2">
            <dt className="flex shrink-0 items-center gap-1.5 font-extrabold text-purple">
              <HeartMark size={16} />
            </dt>
            <dd>Add to Phebe favorites.</dd>
          </div>
        </dl>
      </section>

      <section className="mx-auto max-w-[1120px] px-7 py-10">
        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {cards.map(({ restaurant: r, score }) => {
            const meta = restaurantMeta(r);
            return (
            <li key={r.slug}>
              <article className="relative h-full rounded-2xl border border-line bg-white p-5 transition-colors hover:border-green-deep/40 hover:bg-green-pale">
                <Link
                  href={`/r/${r.slug}`}
                  className="absolute inset-0 z-0 rounded-2xl"
                  aria-label={r.name}
                />
                <div className="pointer-events-none relative z-10">
                  <div className="flex items-start justify-between gap-3">
                    <h2 className="text-xl font-extrabold text-purple">
                      {r.name}
                    </h2>
                    <span className="pointer-events-auto shrink-0">
                      <FavoriteHeart label={r.name} />
                    </span>
                  </div>
                  <div className="mt-2">
                    <ScoreDots score={score} size="sm" />
                  </div>
                  {meta ? (
                    <p className="mt-2 text-sm text-ink-soft">{meta}</p>
                  ) : null}
                  {reviewSummaries.has(r.slug) ? (
                    <div className="mt-2">
                      <ReviewStars
                        average={reviewSummaries.get(r.slug)!.average}
                        count={reviewSummaries.get(r.slug)!.count}
                      />
                    </div>
                  ) : null}
                  {r.blurb ? (
                    <p className="mt-2 text-sm text-ink-soft">{r.blurb}</p>
                  ) : null}
                  <ScoreLines score={score} menuUrl={r.menu_urls?.[0]} />
                </div>
              </article>
            </li>
            );
          })}
        </ul>
      </section>
      <p className="mt-10 text-xs leading-relaxed text-ink/60">
        {AWARD_DISCLAIMER}
      </p>
    </main>
  );
}
