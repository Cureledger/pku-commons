"use client";

import { useEffect, useMemo, useState } from "react";
import { StarMark, Stars } from "@/components/star-mark";
import type { Review } from "@/lib/types";

function storageKey(slug: string): string {
  return `phebe-reviews:${slug}`;
}

function loadLocal(slug: string): Review[] {
  try {
    const raw = localStorage.getItem(storageKey(slug));
    if (!raw) return [];
    return JSON.parse(raw) as Review[];
  } catch {
    return [];
  }
}

function saveLocal(slug: string, reviews: Review[]): void {
  localStorage.setItem(storageKey(slug), JSON.stringify(reviews.slice(0, 48)));
}

function mergeReviews(seed: Review[], local: Review[]): Review[] {
  const seen = new Set(local.map((review) => review.id));
  return [...local, ...seed.filter((review) => !seen.has(review.id))].sort(
    (a, b) => b.addedAt - a.addedAt,
  );
}

export function RestaurantReviews({
  slug,
  seed,
}: {
  slug: string;
  seed: Review[];
}) {
  const [local, setLocal] = useState<Review[]>([]);
  const [stars, setStars] = useState(0);
  const [body, setBody] = useState("");

  useEffect(() => {
    setLocal(loadLocal(slug));
  }, [slug]);

  const reviews = useMemo(() => mergeReviews(seed, local), [seed, local]);
  const average = reviews.length
    ? Math.round(
        (reviews.reduce((sum, review) => sum + review.stars, 0) /
          reviews.length) *
          10,
      ) / 10
    : 0;

  function post() {
    const text = body.trim();
    if (!stars || !text) return;
    const next: Review = {
      id: `${Date.now()}`,
      slug,
      stars,
      body: text,
      addedAt: Date.now(),
    };
    setLocal((prev) => {
      const list = [next, ...prev];
      saveLocal(slug, list);
      return list;
    });
    setStars(0);
    setBody("");
  }

  return (
    <section className="mt-12">
      <div className="flex items-center gap-3">
        <h2 className="text-2xl font-extrabold text-purple">Reviews</h2>
        {reviews.length ? (
          <div className="flex items-center gap-2 text-purple">
            <Stars value={average} size={16} />
            <span className="text-sm font-semibold">{average}</span>
          </div>
        ) : null}
      </div>

      <form
        className="mt-5"
        onSubmit={(e) => {
          e.preventDefault();
          post();
        }}
      >
        <div className="flex items-center gap-1 text-purple">
          {Array.from({ length: 5 }, (_, i) => {
            const value = i + 1;
            return (
              <button
                key={value}
                type="button"
                onClick={() => setStars(value)}
                aria-label={`${value} star${value === 1 ? "" : "s"}`}
                aria-pressed={stars === value}
                className="rounded-sm p-0.5 hover:bg-green-pale"
              >
                <StarMark filled={value <= stars} size={22} />
              </button>
            );
          })}
        </div>
        <textarea
          value={body}
          onChange={(e) => setBody(e.target.value)}
          rows={3}
          aria-label="Review"
          className="mt-3 w-full resize-y rounded-lg border border-line bg-white px-3 py-2 text-sm text-ink outline-none focus:border-purple"
        />
        <button
          type="submit"
          disabled={!stars || !body.trim()}
          className="mt-3 rounded-full bg-green px-5 py-2 text-sm font-bold text-purple-deep disabled:opacity-40"
        >
          Post
        </button>
      </form>

      {reviews.length ? (
        <ul className="mt-8 grid gap-6">
          {reviews.map((review) => (
            <li key={review.id}>
              <div className="flex items-center gap-2 text-purple">
                <Stars value={review.stars} size={14} />
                {review.by ? (
                  <span className="text-sm font-semibold">{review.by}</span>
                ) : null}
              </div>
              <p className="mt-2 text-ink">{review.body}</p>
            </li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}

export function ReviewStars({
  average,
  count,
  size = 14,
}: {
  average: number;
  count: number;
  size?: number;
}) {
  if (!count) return null;
  return (
    <div className="flex items-center gap-1.5 text-purple">
      <Stars value={average} size={size} />
      <span className="text-xs font-semibold">{average}</span>
    </div>
  );
}
