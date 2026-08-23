import Image from "next/image";

export function PhebeMark({
  size = 16,
  alt = "",
}: {
  size?: number;
  alt?: string;
}) {
  return (
    <Image
      src="/images/phebe-logo-transparent.png"
      alt={alt}
      width={size}
      height={size}
      className="inline-block align-[-0.15em]"
    />
  );
}
