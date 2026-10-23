import { redirect } from "next/navigation";
import { WorkspaceHome } from "@/components/workspace-home";
import { getTopics } from "@/lib/content";
import { getStudyCatalog, getCompanies, getNoteGroups } from "@/lib/study";
export default async function Home({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; track?: string; saved?: string }>;
}) {
  const params = await searchParams;
  if (params.q || params.track || params.saved) {
    const query = new URLSearchParams();
    for (const [key, value] of Object.entries(params))
      if (value) query.set(key, value);
    redirect(`/ai-ml?${query}`);
  }
  return (
    <WorkspaceHome
      problems={getStudyCatalog().problems}
      topics={getTopics().map(({ slug, title }) => ({ slug, title }))}
      counts={{
        concepts: getNoteGroups("concepts").flatMap((g) => g.notes).length,
        systemDesign: getNoteGroups("system-design").flatMap((g) => g.notes)
          .length,
        companies: getCompanies().filter((c) => c.questions > 0).length,
        profiles: getStudyCatalog().companyProfiles.length,
      }}
    />
  );
}
