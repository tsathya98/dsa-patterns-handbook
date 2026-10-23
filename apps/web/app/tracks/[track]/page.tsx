import { notFound } from "next/navigation";
import { Catalog } from "@/components/catalog";
import { getTopics, getTracks } from "@/lib/content";
export const dynamicParams = false;

export function generateStaticParams() {
  return getTracks().map((track) => ({ track: track.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ track: string }>;
}) {
  const { track: id } = await params;
  const track = getTracks().find((track) => track.id === id);
  return {
    title: track?.title ?? "Track not found",
    description: track?.description,
  };
}

export default async function TrackPage({
  params,
}: {
  params: Promise<{ track: string }>;
}) {
  const { track: id } = await params;
  if (!getTracks().some((track) => track.id === id)) notFound();
  return (
    <Catalog
      key={id}
      topics={getTopics()}
      tracks={getTracks()}
      initialTrack={id}
      trackPage
    />
  );
}
