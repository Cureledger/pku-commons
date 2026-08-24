import { CityDirectory } from "@/components/city-directory";
import { CITIES, cityBySlug } from "@/lib/cities";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return CITIES.map((city) => ({ city: city.slug }));
}

export default async function CityPage({
  params,
}: {
  params: Promise<{ city: string }>;
}) {
  const { city: slug } = await params;
  const city = cityBySlug(slug);
  if (!city) notFound();
  return <CityDirectory city={city} />;
}
