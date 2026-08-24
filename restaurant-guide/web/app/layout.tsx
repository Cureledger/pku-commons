import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Phebe Eats",
  description: "Eating out around the world with PKU.",
  icons: {
    icon: "/images/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className={inter.className}>
        <header className="sticky top-0 z-40 border-b border-green-deep/20 bg-green-pale">
          <div className="mx-auto flex max-w-[1120px] items-center px-7 py-4">
            <Link href="/" className="flex items-center gap-2.5 no-underline">
              <Image
                src="/images/phebe-logo-transparent.png"
                alt=""
                width={36}
                height={36}
                className="h-9 w-9"
                priority
              />
              <Image
                src="/images/wordmark-purple.png"
                alt="Phebe"
                width={120}
                height={36}
                className="h-9 w-auto"
                priority
              />
              <span className="text-sm font-bold text-purple">Eats</span>
            </Link>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
