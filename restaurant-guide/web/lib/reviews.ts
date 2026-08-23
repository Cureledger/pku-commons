import { readFileSync } from "fs";
import path from "path";
import type { Review, ReviewFile, ReviewSummary } from "./types";

const REVIEWS_PATH = path.join(process.cwd(), "..", "data", "reviews.json");

export function loadReviewFile(): ReviewFile {
  return JSON.parse(readFileSync(REVIEWS_PATH, "utf8")) as ReviewFile;
}

export function loadReviews(slug: string): Review[] {
  return loadReviewFile()
    .reviews.filter((review) => review.slug === slug)
    .sort((a, b) => b.addedAt - a.addedAt);
}

export function summarizeReviews(reviews: Review[]): ReviewSummary | null {
  if (!reviews.length) return null;
  const total = reviews.reduce((sum, review) => sum + review.stars, 0);
  return {
    slug: reviews[0].slug,
    average: Math.round((total / reviews.length) * 10) / 10,
    count: reviews.length,
  };
}

export function loadReviewSummaries(): Map<string, ReviewSummary> {
  const bySlug = new Map<string, Review[]>();
  for (const review of loadReviewFile().reviews) {
    const list = bySlug.get(review.slug) ?? [];
    list.push(review);
    bySlug.set(review.slug, list);
  }
  const summaries = new Map<string, ReviewSummary>();
  for (const [slug, list] of bySlug) {
    const summary = summarizeReviews(list);
    if (summary) summaries.set(slug, summary);
  }
  return summaries;
}
