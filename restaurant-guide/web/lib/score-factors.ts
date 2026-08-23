import type { ScoreFactor } from "./types";

export const SCORE_FACTORS: { id: ScoreFactor; label: string; line: string }[] = [
  {
    id: "publishedMenu",
    label: "Published menu",
    line: "Restaurant posts a current menu.",
  },
  {
    id: "main",
    label: "A main",
    line: "Restaurant offers a low-protein main.",
  },
  {
    id: "beyond",
    label: "Plates beyond potato and salad",
    line: "Restaurant offers low-protein plates beyond potato and salad.",
  },
  {
    id: "accommodation",
    label: "Accommodation",
    line: "Restaurant will substitute on request.",
  },
  {
    id: "offMenu",
    label: "Off-menu",
    line: "Restaurant will cook off menu with sufficient notice.",
  },
  {
    id: "award",
    label: "Award",
    line: "Restaurant has received a third party award.",
  },
  {
    id: "phebeVerified",
    label: "Phebe-verified",
    line: "Restaurant has been verified by the Phebe community.",
  },
];
