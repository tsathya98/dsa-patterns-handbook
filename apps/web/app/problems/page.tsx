import { ProblemBoard } from "@/components/problem-board";
import { getStudyCatalog } from "@/lib/study";
export const metadata = { title: "Problems & practice" };
export default async function ProblemsPage({
  searchParams,
}: {
  searchParams: Promise<{ plan?: string; q?: string }>;
}) {
  const { plan = "all", q = "" } = await searchParams;
  return (
    <ProblemBoard
      key={`${plan}-${q}`}
      problems={getStudyCatalog().problems}
      initialQuery={q}
      initialPlan={
        ["all", "75", "150", "hw", "notes"].includes(plan) ? plan : "all"
      }
    />
  );
}
