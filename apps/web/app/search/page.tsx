import Link from "next/link";
import { getDocuments, getTopics } from "@/lib/content";
import { getStudyCatalog, getCompanies } from "@/lib/study";
export const metadata = { title: "Search the workspace" };
export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q = "" } = await searchParams;
  const needle = q.trim().toLowerCase();
  const has = (text: string) => {
    if (!needle) return false;
    const normalized = text.toLowerCase();
    const words = normalized.split(/[^a-z0-9]+/);
    return needle
      .split(/\s+/)
      .every((term) =>
        term.length <= 3 ? words.includes(term) : normalized.includes(term),
      );
  };
  const topics = getTopics().filter((t) =>
    has(
      `${t.title} ${t.summary} ${t.explanations?.map((s) => `${s.title} ${s.paragraphs.join(" ")}`).join(" ")}`,
    ),
  );
  const catalog = getStudyCatalog();
  const problems = catalog.problems.filter((p) =>
    has(`${p.number} ${p.title} ${p.pattern} ${p.topic}`),
  );
  const problemDocs = new Set(problems.map((p) => p.documentId));
  const notes = getDocuments().filter(
    (d) =>
      d.bucket !== "Companies" &&
      !problemDocs.has(d.id) &&
      has(`${d.title} ${d.path}`),
  );
  const companies = getCompanies().filter((c) =>
    has(
      `${c.name} ${c.profiles.map((p) => p.aiRoles + " " + p.aiFocus).join(" ")}`,
    ),
  );
  const groups = [
    {
      title: "AI / ML lessons",
      rows: topics.map((t) => ({
        href: `/topics/${t.slug}`,
        title: t.title,
        description: t.summary,
      })),
    },
    {
      title: "Coding problems",
      rows: problems.map((p) => ({
        href: p.documentId
          ? `/library/${p.documentId}`
          : `/problems?q=${p.number}`,
        title: `#${p.number}: ${p.title}`,
        description: p.topic,
      })),
    },
    {
      title: "Concepts and field guides",
      rows: notes.map((n) => ({
        href: `/library/${n.id}`,
        title: n.title,
        description: n.bucket,
      })),
    },
    {
      title: "Companies and roles",
      rows: companies.map((c) => ({
        href: `/companies/${c.slug}`,
        title: c.name,
        description: `${c.questions} questions · ${c.profiles.length} pay / role profiles`,
      })),
    },
  ];
  return (
    <div className="page-container study-page">
      <div className="page-heading">
        <div className="eyebrow">ALL STUDY MATERIAL</div>
        <h1>Search the workspace</h1>
        <p>
          Find problems, concepts, system design, AI / ML lessons, and companies
          together.
        </p>
      </div>
      <form className="workspace-search-form" action="/search">
        <input
          name="q"
          aria-label="Workspace search query"
          defaultValue={q}
          placeholder="Try binary search, RAG, Google, or 88"
        />
        <button className="primary-button">Search</button>
      </form>
      {needle && groups.every((group) => group.rows.length === 0) && (
        <div className="empty-state">
          <h2>No results for “{q}”.</h2>
          <p>Try a broader concept, problem number, or company name.</p>
        </div>
      )}
      {!needle ? (
        <div className="empty-state">
          <h2>Enter a concept, question, or company.</h2>
        </div>
      ) : (
        groups
          .filter((group) => group.rows.length > 0)
          .map((group) => (
            <section className="search-result-group" key={group.title}>
              <div className="section-heading">
                <h2>{group.title}</h2>
                <span>{group.rows.length} matches</span>
              </div>
              <div className="document-list">
                {group.rows.slice(0, 30).map((row) => (
                  <Link href={row.href} key={row.href + "-" + row.title}>
                    <div>
                      <h3>{row.title}</h3>
                      <p>{row.description}</p>
                    </div>
                    <span>↗</span>
                  </Link>
                ))}
              </div>
              {group.rows.length > 30 && (
                <p>
                  Showing the first 30 matches. Use a more specific search to
                  narrow the results.
                </p>
              )}
            </section>
          ))
      )}
    </div>
  );
}
