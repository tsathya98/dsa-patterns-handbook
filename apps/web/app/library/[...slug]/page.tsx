import Link from "next/link";
import { notFound } from "next/navigation";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeSlug from "rehype-slug";
import { ArrowLeft, FileText } from "lucide-react";
import { getDocument, resolveDocumentLink } from "@/lib/content";
import { getNoteGroups, getStudyCatalog } from "@/lib/study";
import { DocumentTools } from "@/components/document-tools";
import GithubSlugger from "github-slugger";
export const dynamic = "force-dynamic";
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  return {
    title:
      getDocument((await params).slug.join("/"))?.title ?? "Document not found",
  };
}
export default async function DocumentPage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const doc = getDocument((await params).slug.join("/"));
  if (!doc) notFound();
  const catalog = getStudyCatalog();
  const note = catalog.notes.find((note) => note.id === doc.id);
  const linkedProblems = catalog.problems.filter(
    (p) => p.documentId === doc.id,
  );
  const problem = note?.docType === "concept" ? undefined : linkedProblems[0];
  const slugger = new GithubSlugger();
  let inCode = false;
  const headings = doc.content.split("\n").flatMap((line) => {
    if (line.startsWith("```")) {
      inCode = !inCode;
      return [];
    }
    const match = !inCode && line.match(/^(#{1,3})\s+(.+)$/);
    if (!match) return [];
    const title = match[2]
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/[*`]/g, "");
    const id = slugger.slug(title);
    return match[1].length > 1 ? [{ id, title }] : [];
  });
  const back =
    doc.bucket === "System design"
      ? "/system-design"
      : doc.bucket === "AI field notes"
        ? "/ai-ml"
        : doc.bucket === "DSA"
          ? problem
            ? "/problems"
            : "/concepts"
          : doc.bucket === "Cheat sheets"
            ? "/cheat-sheets"
            : doc.bucket === "Study plans"
              ? "/roadmap"
              : "/library";
  const kind =
    doc.bucket === "System design"
      ? "system-design"
      : doc.bucket === "AI field notes"
        ? "ai-ml"
        : doc.bucket === "DSA" && !problem
          ? "concepts"
          : undefined;
  const sequence = kind
    ? getNoteGroups(kind)
        .flatMap((group) => group.notes)
        .filter((n) => n.categoryLabel !== "Career reference")
    : [];
  const index = sequence.findIndex((n) => n.id === doc.id);
  const following = index >= 0 ? sequence[index + 1] : undefined;
  return (
    <div className="page-container document-container">
      <Link className="back-link" href={back}>
        <ArrowLeft size={14} />{" "}
        {problem
          ? "Coding practice"
          : doc.bucket === "AI field notes"
            ? "AI & ML"
            : doc.bucket === "DSA"
              ? "DSA concepts"
              : doc.bucket === "Study plans"
                ? "Study plan"
                : doc.bucket}
      </Link>
      <div className="source-notice">
        <FileText size={16} />
        <span>{doc.bucket.toUpperCase()}</span>
        <span>
          {Math.max(1, Math.ceil(doc.content.split(/\s+/).length / 220))} min
          read
        </span>
      </div>
      {doc.id.includes("company_tiers_and_compensation") && (
        <p className="study-data-note">
          This is the saved career reference. Pay bands, company roles, and
          work-life descriptions have not been reverified as current market data
          or openings.
        </p>
      )}
      <DocumentTools
        id={doc.id}
        legacyPath={note?.path ?? `${doc.id}.md`}
        problem={problem}
        hasCode={/```(?:python|py)\b/.test(doc.content)}
      />
      {!!headings.length && (
        <details className="reader-contents">
          <summary>On this page</summary>
          <nav>
            {headings.map((heading) => (
              <a key={heading.id} href={`#${heading.id}`}>
                {heading.title}
              </a>
            ))}
          </nav>
        </details>
      )}
      <article className="markdown">
        <Markdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex, rehypeSlug]}
          components={{
            a: ({ href, children }) => (
              <a href={resolveDocumentLink(doc.path, href ?? "")}>{children}</a>
            ),
          }}
        >
          {doc.content}
        </Markdown>
      </article>
      {note?.docType === "concept" && linkedProblems.length > 0 && (
        <section className="study-panel">
          <h2>Practice this concept</h2>
          <nav className="study-shortcuts" aria-label="Related practice">
            {linkedProblems.map((p) => (
              <Link key={p.number} href={`/problems?q=${p.number}`}>
                {p.title} →
              </Link>
            ))}
          </nav>
        </section>
      )}
      <nav className="guide-pagination" aria-label="Continue studying">
        <Link href={back}>
          Back to{" "}
          {problem
            ? "coding practice"
            : doc.bucket === "AI field notes"
              ? "AI / ML"
              : doc.bucket.toLowerCase()}
        </Link>
        {following && (
          <Link href={`/library/${following.id}`}>
            <span>NEXT GUIDE</span>
            {following.shortTitle}
          </Link>
        )}
      </nav>
    </div>
  );
}
