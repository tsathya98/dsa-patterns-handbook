import { Catalog } from "@/components/catalog";
import { getTopics, getTracks } from "@/lib/content";
import { getNoteGroups } from "@/lib/study";
export const metadata = { title: "AI & ML" };
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; track?: string; saved?: string }>;
}) {
  const params = await searchParams;
  return (
    <Catalog
      key={`${params.q}-${params.track}-${params.saved}`}
      topics={getTopics()}
      tracks={getTracks()}
      initialQuery={params.q}
      initialTrack={params.track}
      savedOnly={params.saved === "1"}
      fieldGuides={getNoteGroups("ai-ml").flatMap((group) => group.notes)}
    />
  );
}
