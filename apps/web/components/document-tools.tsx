"use client";
import Link from "next/link";
import type { Problem, StudyStatus } from "@/lib/study";
import { useStudy } from "./study-state";
export function DocumentTools({
  id,
  legacyPath,
  problem,
  hasCode,
}: {
  id: string;
  legacyPath: string;
  problem?: Problem;
  hasCode: boolean;
}) {
  const study = useStudy();
  const status = problem
    ? (study.problemStatus[`lc-${problem.number}`] ?? "todo")
    : (study.documentStatus[legacyPath] ?? "todo");
  return (
    <section className="document-study-tools">
      <div className="document-tool-row">
        <label>
          Study status
          <select
            aria-label="Document study status"
            disabled={!study.ready}
            value={status}
            onChange={(e) =>
              problem
                ? study.setStatus(problem, e.target.value as StudyStatus)
                : study.setDocStatus(legacyPath, e.target.value as StudyStatus)
            }
          >
            <option value="todo">To study</option>
            <option value="solved">Studied</option>
            <option value="review">Review</option>
          </select>
        </label>
        {hasCode && (
          <Link
            className="secondary-button"
            href={`/playground?document=${encodeURIComponent(id)}`}
          >
            Open Python in playground
          </Link>
        )}
        {problem?.url && (
          <a
            className="secondary-button"
            href={problem.url}
            target="_blank"
            rel="noreferrer"
          >
            Practice on LeetCode ↗
          </a>
        )}
      </div>
      <details className="reader-notes">
        <summary>Personal notes</summary>
        <textarea
          aria-label="Personal document notes"
          placeholder="What to remember, mistakes, and follow-up questions..."
          value={study.notes[legacyPath] ?? ""}
          onChange={(e) => study.setNote(legacyPath, e.target.value)}
        />
        <small>
          Saved in this browser. Export a backup from the problem tracker.
        </small>
      </details>
      {study.warning && <p role="status">{study.warning}</p>}
    </section>
  );
}
