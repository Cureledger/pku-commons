import Link from "next/link";
import { EyeglassesMark } from "@/components/eyeglasses-mark";
import { FavoriteHeart } from "@/components/heart";
import { HeartMark } from "@/components/heart-mark";
import { PhebeMark } from "@/components/phebe-mark";
import { ScoreLines } from "@/components/score-lines";
import { AWARD_DISCLAIMER } from "@/lib/restaurants";
import { loadPkuCards } from "@/lib/pku";

export default function HomePage() {
  const cards = loadPkuCards();

  return (
    <main>
      <section className="bg-green">
        <div className="mx-auto max-w-[1120px] px-7 py-16 md:py-20">
          <p className="text-xs font-bold uppercase tracking-[0.12em] text-purple">
            Phebe Eats
          </p>
          <h1 className="mt-3 text-4xl font-extrabold text-purple sm:text-5xl">
            Eating low-pro in Asheville
          </h1>
        </div>
      </section>

      <section className="border-b border-line bg-green-pale">
        <dl className="mx-auto grid max-w-[1120px] gap-5 px-7 py-6 text-sm text-ink sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
          <div>
            <dt className="font-extrabold text-purple">main</dt>
            <dd className="mt-0.5">A real entree.</dd>
          </div>
          <div>
            <dt className="font-extrabold text-purple">plates</dt>
            <dd className="mt-0.5">Beyond potato and salad.</dd>
          </div>
          <div>
            <dt className="font-extrabold text-purple">[] accommodation</dt>
            <dd className="mt-0.5">They will substitute.</dd>
          </div>
          <div>
            <dt className="flex items-center gap-1.5 font-extrabold text-purple">
              [] <PhebeMark size={16} alt="" />
            </dt>
            <dd className="mt-0.5">They will cook off-menu.</dd>
          </div>
          <div>
            <dt className="flex items-center gap-1.5 font-extrabold text-purple">
              <EyeglassesMark size={16} />
            </dt>
            <dd className="mt-0.5">View menu.</dd>
          </div>
          <div>
            <dt className="flex items-center gap-1.5 font-extrabold text-purple">
              <HeartMark size={16} />
            </dt>
            <dd className="mt-0.5">Add to Phebe favorites.</dd>
          </div>
        </dl>
      </section>

      <section className="mx-auto max-w-[1120px] px-7 py-10">
        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {cards.map(({ restaurant: r, score }) => (
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
                    <div className="flex shrink-0 items-center gap-1">
                      <p className="text-sm font-extrabold text-purple">
                        {score.total}/{score.max}
                      </p>
                      <span className="pointer-events-auto">
                        <FavoriteHeart label={r.name} />
                      </span>
                    </div>
                  </div>
                  {r.blurb ? (
                    <p className="mt-2 text-sm text-ink-soft">{r.blurb}</p>
                  ) : null}
                  <ScoreLines score={score} menuUrl={r.menu_urls?.[0]} />
                </div>
              </article>
            </li>
          ))}
        </ul>
      </section>
      <p className="mt-10 text-xs leading-relaxed text-ink/60">{AWARD_DISCLAIMER}</p>
    </main>
  );
}
