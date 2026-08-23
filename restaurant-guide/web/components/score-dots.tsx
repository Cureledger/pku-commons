import type { PkuScore, ScoreFactor } from "@/lib/types";
import { SCORE_FACTORS } from "@/lib/pku";

const FACTOR_ON: Record<ScoreFactor, (score: PkuScore) => boolean> = {
  publishedMenu: (s) => s.publishedMenu,
  main: (s) => s.mains >= 1,
  beyond: (s) => s.beyond >= 1,
  accommodation: (s) => s.substitutes,
  offMenu: (s) => s.mntFoodCheck,
  award: (s) => s.hasAward,
  phebeVerified: (s) => s.phebeVerified,
};

export function ScoreDots({
  score,
  size = "md",
}: {
  score: PkuScore;
  size?: "sm" | "md";
}) {
  const onLabels = SCORE_FACTORS.filter((f) => FACTOR_ON[f.id](score)).map(
    (f) => f.label,
  );
  const dim = size === "sm" ? "h-2.5 w-2.5" : "h-3 w-3";

  return (
    <ul
      className="flex items-center gap-1"
      aria-label={
        onLabels.length
          ? `${onLabels.join(", ")}`
          : "No scale factors yet"
      }
    >
      {SCORE_FACTORS.map((factor) => {
        const on = FACTOR_ON[factor.id](score);
        return (
          <li key={factor.id}>
            <span
              className={`block rounded-full ${dim} ${
                on ? "bg-purple" : "border border-purple/35 bg-transparent"
              }`}
              title={factor.label}
            />
            <span className="sr-only">
              {factor.label}: {on ? "yes" : "no"}
            </span>
          </li>
        );
      })}
    </ul>
  );
}
