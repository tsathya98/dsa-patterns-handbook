"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { ArrowUpRight, Search } from "lucide-react";
import type { Problem, StudyStatus } from "@/lib/study";
import { StudyBackup, useStudy } from "./study-state";
const plans = [
  ["all", "All problems"],
  ["75", "LeetCode 75"],
  ["150", "Top Interview 150"],
  ["hw", "Course problems"],
  ["notes", "With walkthroughs"],
] as const;
export function ProblemBoard({
  problems,
  initialPlan = "all",
  initialQuery = "",
}: {
  problems: Problem[];
  initialPlan?: string;
  initialQuery?: string;
}) {
  const study = useStudy();
  const [plan, setPlan] = useState(initialPlan);
  const [query, setQuery] = useState(initialQuery);
  const [difficulty, setDifficulty] = useState("all");
  const [topic, setTopic] = useState("all");
  const [company, setCompany] = useState("all");
  const [status, setStatus] = useState("all");
  const [page, setPage] = useState(1);
  const all = useMemo(
    () => [
      ...problems,
      ...study.customProblems.filter(
        (p) => !problems.some((x) => x.number === p.number),
      ),
    ],
    [problems, study.customProblems],
  );
  const getStatus = (p: Problem) =>
    study.problemStatus[`lc-${p.number}`] ?? "todo";
  const inPlan = (p: Problem, value: string) =>
    value === "75"
      ? p.in75
      : value === "150"
        ? p.in150
        : value === "hw"
          ? p.inHW
          : value === "notes"
            ? !!p.documentId
            : true;
  const filtered = all
    .filter(
      (p) =>
        inPlan(p, plan) &&
        (difficulty === "all" || p.difficulty === difficulty) &&
        (topic === "all" || p.topic === topic) &&
        (company === "all" || p.companies.includes(company)) &&
        (status === "all" || getStatus(p) === status) &&
        (/^\d+$/.test(query.trim())
          ? p.number === Number(query)
          : `${p.title} ${p.topic} ${p.pattern}`
              .toLowerCase()
              .includes(query.toLowerCase())),
    )
    .sort((a, b) =>
      company === "all"
        ? a.number - b.number
        : (b.companyFreq[company] ?? 0) - (a.companyFreq[company] ?? 0),
    );
  const pages = Math.max(1, Math.ceil(filtered.length / 40));
  const currentPage = Math.min(page, pages);
  const rows = filtered.slice((currentPage - 1) * 40, currentPage * 40);
  return (
    <div className="page-container study-page">
      <div className="page-heading">
        <div className="eyebrow">CODING INTERVIEW WORKSPACE</div>
        <h1>Problems & practice</h1>
        <p>
          LeetCode lists, course exercises, local walkthroughs, and your own
          problem log.
        </p>
      </div>
      <nav className="study-shortcuts" aria-label="Coding study steps">
        <Link href="/concepts">Learn a concept</Link>
        <span>→</span>
        <span>Practice a problem</span>
        <span>→</span>
        <Link href="/tracker">Review mistakes</Link>
      </nav>
      <div className="study-tabs" aria-label="Problem lists">
        {plans.map(([id, label]) => (
          <button
            key={id}
            aria-pressed={plan === id}
            onClick={() => {
              setPlan(id);
              setPage(1);
            }}
          >
            {label}
            <span>{all.filter((p) => inPlan(p, id)).length}</span>
          </button>
        ))}
      </div>
      <div className="practice-progress">
        {study.ready
          ? all.filter((p) => inPlan(p, plan) && getStatus(p) === "solved")
              .length
          : "..."}{" "}
        of {all.filter((p) => inPlan(p, plan)).length} solved in this list
        <Link href="/tracker">
          Review queue ({all.filter((p) => getStatus(p) === "review").length})
        </Link>
      </div>
      <div className="study-filters problem-filters">
        <label className="catalog-search">
          <Search size={16} />
          <input
            aria-label="Search problems"
            placeholder="Problem number, title, or pattern"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
          />
        </label>
        <select
          aria-label="Problem topic"
          value={topic}
          onChange={(e) => {
            setTopic(e.target.value);
            setPage(1);
          }}
        >
          <option value="all">All topics</option>
          {[...new Set(all.map((p) => p.topic))].sort().map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
        <select
          aria-label="Difficulty"
          value={difficulty}
          onChange={(e) => {
            setDifficulty(e.target.value);
            setPage(1);
          }}
        >
          <option value="all">All difficulties</option>
          {["Easy", "Medium", "Hard"].map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
        <select
          aria-label="Problem status"
          value={status}
          onChange={(e) => {
            setStatus(e.target.value);
            setPage(1);
          }}
        >
          <option value="all">All statuses</option>
          <option value="todo">To do</option>
          <option value="solved">Solved</option>
          <option value="review">Review</option>
        </select>
        <select
          aria-label="Company frequency"
          value={company}
          onChange={(e) => {
            setCompany(e.target.value);
            setPage(1);
          }}
        >
          <option value="all">All companies</option>
          {[...new Set(all.flatMap((p) => p.companies))].sort().map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
        <button
          className="text-button"
          onClick={() => {
            setQuery("");
            setDifficulty("all");
            setTopic("all");
            setCompany("all");
            setStatus("all");
            setPage(1);
          }}
        >
          Clear filters
        </button>
      </div>
      <div className="study-result-heading">
        <span>{filtered.length} matching problems</span>
        <Link href="/companies">
          Browse all company banks <ArrowUpRight size={14} />
        </Link>
      </div>
      <div className="table-scroll study-table-wrap">
        <table className="study-table">
          <thead>
            <tr>
              <th>Problem</th>
              <th>Difficulty</th>
              <th>Pattern / topic</th>
              <th>Practice</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((p) => (
              <tr key={p.number}>
                <td>
                  <span className="mono muted">{p.displayNum}</span>
                  <h3>{p.title}</h3>
                  <div className="problem-membership">
                    {p.in75 && <span>LC 75</span>}
                    {p.in150 && <span>Top 150</span>}
                    {p.inHW && <span>Course</span>}
                    {company !== "all" && (
                      <span>{p.companyFreq[company]} recorded appearances</span>
                    )}
                  </div>
                  <details className="problem-notes">
                    <summary>My notes</summary>
                    <textarea
                      aria-label={`Notes for ${p.title}`}
                      value={study.notes[p.docPath || `lc-${p.number}`] ?? ""}
                      onChange={(e) =>
                        study.setNote(
                          p.docPath || `lc-${p.number}`,
                          e.target.value,
                        )
                      }
                      placeholder="Approach, mistake, next review..."
                    />
                  </details>
                </td>
                <td>
                  <span
                    className={`difficulty difficulty-${p.difficulty.toLowerCase()}`}
                  >
                    {p.difficulty}
                  </span>
                </td>
                <td>{p.pattern || p.topic}</td>
                <td>
                  <div className="table-links">
                    {p.documentId && (
                      <Link href={`/library/${p.documentId}`}>Walkthrough</Link>
                    )}
                    {p.url && (
                      <a href={p.url} target="_blank" rel="noreferrer">
                        LeetCode <ArrowUpRight size={12} />
                      </a>
                    )}
                    {!p.documentId && (
                      <span className="muted">No local guide yet</span>
                    )}
                  </div>
                </td>
                <td>
                  <select
                    aria-label={`Status for ${p.title}`}
                    disabled={!study.ready}
                    value={getStatus(p)}
                    onChange={(e) =>
                      study.setStatus(p, e.target.value as StudyStatus)
                    }
                  >
                    <option value="todo">To do</option>
                    <option value="solved">Solved</option>
                    <option value="review">Review</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {!rows.length && (
        <div className="empty-state">
          <h3>No problems match these filters.</h3>
          <p>Clear a filter or select another list.</p>
        </div>
      )}
      <Pagination page={currentPage} pages={pages} onChange={setPage} />
      <p className="study-data-note">
        Recorded company frequency comes from the repository question banks. It
        is historical reference data, not a prediction of your interview.
      </p>
      <details className="study-panel custom-problem">
        <summary>Add a problem to your practice log</summary>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const form = e.currentTarget;
            const values = new FormData(form);
            const number = Number(values.get("number"));
            const title = String(values.get("title")).trim();
            const topic = String(values.get("topic")).trim();
            if (!Number.isSafeInteger(number) || number < 1 || !title || !topic)
              return;
            const existing = all.find((p) => p.number === number);
            const p: Problem = existing ?? {
              number,
              displayNum: `#${number}`,
              title,
              topic,
              pattern: topic,
              difficulty: String(values.get("difficulty")),
              url: `https://leetcode.com/problemset/?search=${number}`,
              docPath: "",
              documentId: null,
              summary: "",
              in75: false,
              in150: false,
              inHW: false,
              defaultSolved: false,
              companies: [],
              companyFreq: {},
            };
            if (!existing) {
              study.addProblem(p);
              study.setStatus(p, "todo");
            }
            setPlan("all");
            setQuery(String(number));
            setPage(1);
            form.reset();
          }}
        >
          <label>
            LeetCode number
            <input name="number" type="number" min="1" required />
          </label>
          <label>
            Title
            <input name="title" required />
          </label>
          <label>
            Pattern
            <input name="topic" required />
          </label>
          <label>
            Difficulty
            <select name="difficulty">
              <option>Easy</option>
              <option>Medium</option>
              <option>Hard</option>
            </select>
          </label>
          <button className="primary-button" disabled={!study.ready}>
            Add to log
          </button>
        </form>
      </details>
      <StudyBackup />
      <details className="study-panel">
        <summary>Bring progress from the original hub</summary>
        <p className="study-data-note">
          If you used the old viewer as a local file, open that same file and
          reload it, select Export progress, then import the downloaded JSON
          here. Browser storage belongs to the original page origin and cannot
          be transferred automatically from a local file. The original hub
          served from this website shares progress directly with these pages.
        </p>
        <Link
          className="text-button"
          href="/legacy/viewer.html"
          target="_blank"
        >
          Open the original hub ↗
        </Link>
      </details>
    </div>
  );
}
export function Pagination({
  page,
  pages,
  onChange,
}: {
  page: number;
  pages: number;
  onChange: (page: number) => void;
}) {
  return (
    <div className="study-pagination">
      <button
        className="secondary-button"
        disabled={page <= 1}
        onClick={() => onChange(page - 1)}
      >
        Previous
      </button>
      <span>
        Page {page} of {pages}
      </span>
      <button
        className="secondary-button"
        disabled={page >= pages}
        onClick={() => onChange(page + 1)}
      >
        Next
      </button>
    </div>
  );
}
