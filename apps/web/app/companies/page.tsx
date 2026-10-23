import { CompanyDirectory } from "@/components/company-directory";
import { getCompanies } from "@/lib/study";
export const metadata = { title: "Companies, pay & roles" };
export default async function CompaniesPage({
  searchParams,
}: {
  searchParams: Promise<{ view?: string }>;
}) {
  const { view } = await searchParams;
  return (
    <CompanyDirectory
      key={view}
      companies={getCompanies()}
      initialView={view === "pay" ? "pay" : "questions"}
    />
  );
}
