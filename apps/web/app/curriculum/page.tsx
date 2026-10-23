import { redirect } from "next/navigation";
// Preserve existing bookmarks while keeping one AI / ML learning home.
export default async function Curriculum({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; track?: string; saved?: string }>;
}) {
  const params = await searchParams;
  const query = new URLSearchParams();
  for (const key of ["q", "track", "saved"] as const)
    if (params[key]) query.set(key, params[key]);
  redirect(`/ai-ml${query.size ? `?${query}` : ""}`);
}
