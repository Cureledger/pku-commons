export function StarMark({
  filled = false,
  size = 16,
}: {
  filled?: boolean;
  size?: number;
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      aria-hidden="true"
      className="shrink-0"
    >
      <path
        d="M12 3.4 14.6 9l6 .6-4.5 4 1.4 5.8L12 16.6 6.5 19.4 7.9 13.6 3.4 9.6 9.4 9 12 3.4Z"
        fill={filled ? "currentColor" : "none"}
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function Stars({
  value,
  size = 16,
}: {
  value: number;
  size?: number;
}) {
  const rounded = Math.round(value);
  return (
    <ul className="flex items-center gap-0.5" aria-label={`${value} of 5 stars`}>
      {Array.from({ length: 5 }, (_, i) => (
        <li key={i}>
          <StarMark filled={i < rounded} size={size} />
        </li>
      ))}
    </ul>
  );
}
