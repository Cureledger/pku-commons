import type { PkuScore } from "@/lib/types";
import { EyeglassesMark } from "@/components/eyeglasses-mark";
import { PhebeMark } from "@/components/phebe-mark";

export function ScoreLines({
  score,
  menuUrl,
}: {
  score: PkuScore;
  menuUrl?: string;
}) {
  return (
    <ul className="mt-3 grid gap-1 text-sm text-ink">
      <li>
        <span className="font-extrabold text-purple">{score.mains}</span>{" "}
        {score.mains === 1 ? "main" : "mains"}
      </li>
      <li>
        <span className="font-extrabold text-purple">{score.beyond}</span>{" "}
        {score.beyond === 1 ? "plate" : "plates"}
      </li>
      <li>
        <span className="font-extrabold text-purple">
          {score.substitutes ? "[yes]" : "[]"}
        </span>{" "}
        accommodation
      </li>
      <li className="flex items-center gap-1.5">
        <span className="font-extrabold text-purple">
          {score.mntFoodCheck ? "[yes]" : "[]"}
        </span>
        <PhebeMark size={16} alt="Phebe" />
      </li>
      {menuUrl ? (
        <li>
          <a
            href={menuUrl}
            target="_blank"
            rel="noreferrer"
            className="pointer-events-auto inline-flex items-center gap-1.5 font-semibold text-purple no-underline hover:text-purple-deep"
          >
            <EyeglassesMark size={16} />
            View menu
          </a>
        </li>
      ) : null}
    </ul>
  );
}
