export function CameraMark({ size = 28 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      aria-hidden="true"
      className="shrink-0"
    >
      <path
        d="M8.2 7.1 9 5.6h6l.8 1.5H19a1.8 1.8 0 0 1 1.8 1.8v8.2A1.8 1.8 0 0 1 19 18.9H5a1.8 1.8 0 0 1-1.8-1.8V8.9A1.8 1.8 0 0 1 5 7.1h3.2Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinejoin="round"
      />
      <circle
        cx="12"
        cy="12.6"
        r="3.1"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
      />
    </svg>
  );
}
