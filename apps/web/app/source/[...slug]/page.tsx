import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { getSource } from "@/lib/content";
export const dynamic = "force-dynamic";
export default async function SourcePage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const source = getSource((await params).slug.join("/"));
  if (!source) notFound();
  return (
    <div className="page-container">
      <Link className="back-link" href={`/library/${source.documentId}`}>
        <ArrowLeft size={14} /> Back to the walkthrough
      </Link>
      <div className="page-heading">
        <div className="eyebrow">PYTHON SOURCE</div>
        <h1>{source.title}</h1>
        <p>
          Read the implementation alongside its walkthrough, or use the
          playground to try changes.
        </p>
        <Link
          className="secondary-button"
          href={`/playground?document=${encodeURIComponent(source.documentId)}`}
        >
          Open in Python playground
        </Link>
      </div>
      <div className="code-block" style={{ marginTop: 25 }}>
        <pre>
          <code>{source.code}</code>
        </pre>
      </div>
    </div>
  );
}
