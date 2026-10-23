"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowRight, ArrowUpRight, Search } from "lucide-react";
import type { StudyNote, StudyStatus } from "@/lib/study";
import { useStudy } from "./study-state";
export function StudyHub({
  title,
  description,
  groups,
  kind,
}: {
  title: string;
  description: string;
  groups: { title: string; notes: StudyNote[] }[];
  kind: string;
}) {
  const study = useStudy();
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const notes = groups.flatMap((g) => g.notes);
  const studied = notes.filter(
    (note) => study.documentStatus[note.path] === "solved",
  ).length;
  const nextNote = notes.find(
    (note) =>
      note.categoryLabel !== "Career reference" &&
      study.documentStatus[note.path] !== "solved",
  );
  const filtered = notes.filter(
    (n) =>
      (category === "all" || n.categoryLabel === category) &&
      `${n.title} ${n.summary} ${n.pattern}`
        .toLowerCase()
        .includes(query.toLowerCase()),
  );
  return (
    <div className="page-container study-page">
      <div className="page-heading">
        <div className="eyebrow">
          {kind === "system-design"
            ? "ARCHITECTURE & DISTRIBUTED SYSTEMS"
            : "YOUR STUDY HANDBOOK"}
        </div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {(kind === "concepts" || kind === "system-design") &&
        !query &&
        category === "all" &&
        nextNote && (
          <section className="study-panel continue-panel">
            <div>
              <span className="eyebrow">
                {studied ? "CONTINUE STUDYING" : "START HERE"}
              </span>
              <h2>{nextNote.shortTitle}</h2>
              <p>
                {studied} of {notes.length} guides studied. Follow the groups
                below in order.
              </p>
            </div>
            <Link className="primary-button" href={`/library/${nextNote.id}`}>
              Read guide <ArrowRight size={16} />
            </Link>
          </section>
        )}
      {kind === "concepts" && (
        <p className="learning-advice">
          Read a concept, trace its example, then{" "}
          <Link href="/problems?plan=75">practice LeetCode 75</Link>. Use{" "}
          <Link href="/cheat-sheets">cheat sheets</Link> when you need a quick
          reminder.
        </p>
      )}
      {kind === "roadmap" && (
        <section className="study-panel study-routine">
          <h2>A routine for each study session</h2>
          <ol>
            <li>
              <strong>Learn.</strong> Read one concept in{" "}
              <Link href="/concepts">DSA</Link>,{" "}
              <Link href="/system-design">system design</Link>, or{" "}
              <Link href="/ai-ml">AI / ML</Link>.
            </li>
            <li>
              <strong>Practice.</strong> Solve a problem, sketch a design, or
              trace a model without the guide. Use the{" "}
              <Link href="/playground">Python playground</Link> for coding.
            </li>
            <li>
              <strong>Review.</strong> Record what you missed and mark difficult
              material for the <Link href="/tracker">review queue</Link>.
            </li>
          </ol>
          <p>
            For coding, choose one list below. The lists overlap, and solving a
            shared problem updates both.
          </p>
        </section>
      )}
      {kind === "roadmap" && (
        <div className="study-metrics">
          {[
            ["/problems?plan=75", "LeetCode 75", "75"],
            ["/problems?plan=150", "Top Interview 150", "150"],
            ["/problems?plan=hw", "Course exercises", "30"],
            ["/tracker", "Review queue", "↗"],
          ].map(([href, label, count]) => (
            <Link key={href} href={href}>
              <span>{label}</span>
              <strong>{count}</strong>
            </Link>
          ))}
        </div>
      )}
      <div className="study-filters">
        <label className="catalog-search">
          <Search size={16} />
          <input
            aria-label={`Search ${title}`}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search concepts, patterns, and cases..."
          />
        </label>
        <select
          aria-label="Guide category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="all">All categories</option>
          {groups.map((g) => (
            <option key={g.title}>{g.title}</option>
          ))}
        </select>
        <span>{filtered.length} guides</span>
      </div>
      <div className="hub-layout hub-single">
        <div>
          {groups
            .filter((g) => category === "all" || category === g.title)
            .map((g) => {
              const rows = filtered.filter((n) => n.categoryLabel === g.title);
              if (!rows.length) return null;
              return (
                <section className="hub-group" key={g.title}>
                  <div className="section-heading">
                    <h2>{g.title}</h2>
                    <span>{rows.length} guides</span>
                  </div>
                  <div className="note-card-grid">
                    {rows.map((note) => (
                      <article className="note-card" key={note.id}>
                        <Link href={`/library/${note.id}`}>
                          <h3>
                            {note.shortTitle} <ArrowUpRight size={15} />
                          </h3>
                          <p>{note.summary}</p>
                        </Link>
                        <div className="note-card-bottom">
                          <Link href={`/library/${note.id}`}>
                            Read guide <ArrowRight size={13} />
                          </Link>
                          <select
                            aria-label={`Study status for ${note.shortTitle}`}
                            disabled={!study.ready}
                            value={study.documentStatus[note.path] ?? "todo"}
                            onChange={(e) =>
                              study.setDocStatus(
                                note.path,
                                e.target.value as StudyStatus,
                              )
                            }
                          >
                            <option value="todo">To study</option>
                            <option value="solved">Studied</option>
                            <option value="review">Review</option>
                          </select>
                        </div>
                      </article>
                    ))}
                  </div>
                </section>
              );
            })}
          {!filtered.length && (
            <div className="empty-state">
              <h3>No guides match this search.</h3>
              <p>Try another concept or category.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
