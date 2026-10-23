"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowUpRight, FileText, Search } from "lucide-react";
import { Pagination } from "./problem-board";
import type { Document } from "@/lib/content";
export function Library({ documents }: { documents: Document[] }) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);
  const [bucket, setBucket] = useState("All material");
  const buckets = ["All material", ...new Set(documents.map((d) => d.bucket))];
  const filtered = documents.filter(
    (d) =>
      (bucket === "All material" || d.bucket === bucket) &&
      `${d.title} ${d.path}`.toLowerCase().includes(query.toLowerCase()),
  );
  const pages = Math.max(1, Math.ceil(filtered.length / 30));
  const current = Math.min(page, pages);
  return (
    <div className="page-container">
      <div className="page-heading">
        <div className="eyebrow">REFERENCE</div>
        <h1>All reference material</h1>
        <p>
          Search the complete reference collection. For a guided study order,
          open a subject from the navigation.
        </p>
      </div>
      <div className="library-buckets">
        {buckets.map((b) => (
          <button
            key={b}
            aria-pressed={bucket === b}
            onClick={() => {
              setBucket(b);
              setPage(1);
            }}
          >
            {b}
            <span>
              {b === "All material"
                ? documents.length
                : documents.filter((d) => d.bucket === b).length}
            </span>
          </button>
        ))}
      </div>
      <div className="catalog-toolbar">
        <label className="catalog-search">
          <Search size={17} />
          <input
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            placeholder="Search reference material..."
            aria-label="Search study library"
          />
        </label>
        <span className="mono muted">{filtered.length} documents</span>
      </div>
      <div className="document-list">
        {filtered.slice((current - 1) * 30, current * 30).map((d) => (
          <Link
            href={d.bucket === "Companies" ? `/${d.id}` : `/library/${d.id}`}
            key={d.id}
          >
            <FileText size={18} />
            <div>
              <h3>{d.title}</h3>
            </div>
            <span className="library-bucket-tag">{d.bucket}</span>
            <ArrowUpRight size={17} />
          </Link>
        ))}
      </div>
      {filtered.length > 0 && (
        <Pagination page={current} pages={pages} onChange={setPage} />
      )}
      {!filtered.length && (
        <div className="empty-state">
          <h3>No documents match this search.</h3>
          <p>Try another title or subject.</p>
        </div>
      )}
    </div>
  );
}
