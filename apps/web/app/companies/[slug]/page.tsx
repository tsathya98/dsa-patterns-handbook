import { decodeRouteId } from "@/lib/route-id";
import { notFound } from "next/navigation";
import { getCompanies, getCompanyQuestions } from "@/lib/study";
import { CompanyProfileView } from "@/components/company-directory";
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const slug = decodeRouteId((await params).slug);
  return {
    title:
      getCompanies().find((c) => c.slug === slug)?.name ?? "Company not found",
  };
}
export default async function CompanyPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ view?: string }>;
}) {
  const slug = decodeRouteId((await params).slug);
  const { view } = await searchParams;
  const company = getCompanies().find((c) => c.slug === slug);
  if (!company) notFound();
  return (
    <CompanyProfileView
      key={`${slug}-${view}`}
      company={company}
      initialView={view === "pay" ? "pay" : "questions"}
      questions={getCompanyQuestions(slug)}
    />
  );
}
