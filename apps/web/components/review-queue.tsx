"use client";
import Link from "next/link";
import { useState } from "react";
import type { Problem, StudyNote, StudyStatus } from "@/lib/study";
import { useStudy } from "./study-state";
export function ReviewQueue({
  problems,
  notes,
}: {
  problems: Problem[];
  notes: StudyNote[];
}) {
  const study = useStudy();
  const [query, setQuery] = useState("");
  const all = [
    ...problems,
    ...study.customProblems.filter(
      (p) => !problems.some((known) => known.number === p.number),
    ),
  ];
  const pending = all.filter(
    (p) => study.problemStatus[`lc-${p.number}`] === "review",
  );
  // Problem documents share their problem status; do not show them twice.
  const problemPaths = new Set(pending.map((p) => p.docPath));
  const guides = notes.filter(
    (n) =>
      !problemPaths.has(n.path) && study.documentStatus[n.path] === "review",
  );
  const matching = (title: string) =>
    title.toLowerCase().includes(query.toLowerCase());
  return (
    <div className="page-container study-page">
      <div className="page-heading">
        <div className="eyebrow">YOUR STUDY</div>
        <h1>Review queue</h1>
        <p>
          Problems and guides you marked for another pass. Revisit the work,
          then mark it studied or solved.
        </p>
      </div>
      <div className="catalog-toolbar">
        <label className="catalog-search">
          <input
            aria-label="Search review queue"
            placeholder="Find something to revisit..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <span>
          {pending.length} problems · {guides.length} guides
        </span>
      </div>
      {!study.ready ? (
        <p role="status">Loading your review queue...</p>
      ) : pending.length + guides.length === 0 ? (
        <div className="empty-state">
          <h2>Nothing waiting for review.</h2>
          <p>
            Mark a problem or guide as Review while studying to add it here.
          </p>
          <Link className="primary-button" href="/problems">
            Choose a practice problem
          </Link>
        </div>
      ) : (
        <>
          {!!pending.length && (
            <section>
              <div className="section-heading">
                <h2>Coding problems</h2>
              </div>
              <div className="review-list">
                {pending
                  .filter((p) => matching(`${p.number} ${p.title}`))
                  .map((p) => (
                    <article key={p.number}>
                      <div>
                        <Link
                          href={
                            p.documentId
                              ? `/library/${p.documentId}`
                              : `/problems?q=${p.number}`
                          }
                        >
                          <h3>
                            #{p.number} · {p.title}
                          </h3>
                        </Link>
                        <p>{p.pattern || p.topic}</p>
                        {p.url && (
                          <a href={p.url} target="_blank" rel="noreferrer">
                            Practice on LeetCode ↗
                          </a>
                        )}
                      </div>
                      <select
                        aria-label={`Review status for ${p.title}`}
                        value="review"
                        onChange={(e) =>
                          study.setStatus(p, e.target.value as StudyStatus)
                        }
                      >
                        <option value="review">Review</option>
                        <option value="solved">Solved</option>
                        <option value="todo">To do</option>
                      </select>
                    </article>
                  ))}
              </div>
            </section>
          )}
          {!!guides.length && (
            <section>
              <div className="section-heading">
                <h2>Study guides</h2>
              </div>
              <div className="review-list">
                {guides
                  .filter((n) => matching(n.title))
                  .map((note) => (
                    <article key={note.id}>
                      <Link href={`/library/${note.id}`}>
                        <h3>{note.shortTitle}</h3>
                        <p>{note.categoryLabel}</p>
                      </Link>
                      <select
                        aria-label={`Review status for ${note.shortTitle}`}
                        value="review"
                        onChange={(e) =>
                          study.setDocStatus(
                            note.path,
                            e.target.value as StudyStatus,
                          )
                        }
                      >
                        <option value="review">Review</option>
                        <option value="solved">Studied</option>
                        <option value="todo">To study</option>
                      </select>
                    </article>
                  ))}
              </div>
            </section>
          )}
          {!pending.some((p) => matching(`${p.number} ${p.title}`)) &&
            !guides.some((n) => matching(n.title)) && (
              <div className="empty-state">
                <h2>No review items match.</h2>
                <button className="text-button" onClick={() => setQuery("")}>
                  Clear search
                </button>
              </div>
            )}
        </>
      )}
      <nav className="study-shortcuts" aria-label="Continue studying">
        <Link href="/problems">All coding problems</Link>
        <Link href="/concepts">DSA concepts</Link>
        <Link href="/system-design">System design</Link>
        <Link href="/ai-ml?saved=1">Saved AI / ML lessons</Link>
      </nav>
    </div>
  );
}
