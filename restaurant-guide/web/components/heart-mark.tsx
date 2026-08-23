export function HeartMark({
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
        d="M12 20.4s-7.2-4.4-9.3-8.6C1.2 8.8 2.6 5.8 5.7 5.3c1.9-.3 3.6.6 4.5 2.1C11.1 5.9 12.8 5 14.7 5.3c3.1.5 4.5 3.5 3 6.5-2.1 4.2-9.3 8.6-9.3 8.6z"
        fill={filled ? "currentColor" : "none"}
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinejoin="round"
      />
    </svg>
  );
}
