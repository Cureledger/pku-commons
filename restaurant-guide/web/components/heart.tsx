"use client";

import { useState } from "react";
import { HeartMark } from "@/components/heart-mark";

export function FavoriteHeart({
  label,
  size = 18,
}: {
  label: string;
  size?: number;
}) {
  const [saved, setSaved] = useState(false);

  return (
    <button
      type="button"
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        setSaved((v) => !v);
      }}
      aria-pressed={saved}
      aria-label={
        saved
          ? `Remove ${label} from Phebe favorites`
          : `Add ${label} to Phebe favorites`
      }
      className="shrink-0 rounded-full p-1 text-purple hover:bg-green-pale"
    >
      <HeartMark filled={saved} size={size} />
    </button>
  );
}
