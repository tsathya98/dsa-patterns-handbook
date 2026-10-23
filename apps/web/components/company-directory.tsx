"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowUpRight, Building2, Search } from "lucide-react";
import type { Company, CompanyProfile, CompanyQuestion } from "@/lib/study";
import { Pagination } from "./problem-board";
const referenceNote =
  "Pay, role, equity, and work-life notes are saved repository estimates. They have not been reverified as current offers or openings. Ranges retain their original currencies and locations.";
export function CompanyDirectory({
  companies,
  initialView = "questions",
}: {
  companies: Company[];
  initialView?: string;
}) {
  const [view, setView] = useState(initialView);
  const [query, setQuery] = useState("");
  const [tier, setTier] = useState("all");
  const [wlb, setWlb] = useState("all");
  const [domain, setDomain] = useState("all");
  const [page, setPage] = useState(1);
  const profiles = companies.flatMap((c) =>
    c.profiles.map((p) => ({ ...p, questions: c.questions })),
  );
  function match(c: Company) {
    return (
      `${c.name} ${c.profiles.map((p) => `${p.location} ${p.seniorLvl} ${p.aiRoles} ${p.aiFocus} ${p.interviewFocus} ${p.tags.join(" ")}`).join(" ")}`
        .toLowerCase()
        .includes(query.toLowerCase()) &&
      ((tier === "all" && wlb === "all" && domain === "all") ||
        c.profiles.some(profileMatch))
    );
  }
  function profileMatch(p: CompanyProfile) {
    return (
      (tier === "all" || p.tier === tier) &&
      (wlb === "all" || p.wlb === wlb) &&
      (domain === "all" || p.tags.includes(domain))
    );
  }
  const filtered = companies.filter((c) => c.questions > 0 && match(c));
  const payRows = profiles.filter(
    (p) =>
      profileMatch(p) &&
      `${p.name} ${p.location} ${p.seniorLvl} ${p.aiRoles} ${p.aiFocus} ${p.interviewFocus} ${p.tags.join(" ")}`
        .toLowerCase()
        .includes(query.toLowerCase()),
  );
  const count = view === "pay" ? payRows.length : filtered.length;
  const pages = Math.max(1, Math.ceil(count / 24));
  const current = Math.min(page, pages);
  return (
    <div className="page-container study-page">
      <div className="page-heading">
        <div className="eyebrow">COMPANY PREPARATION</div>
        <h1>Companies, pay & roles</h1>
        <p>
          Find a question bank, inspect recorded interview patterns, and compare
          saved Senior and Staff role notes.
        </p>
      </div>
      <p className="collection-counts">
        {companies.filter((c) => c.questions > 0).length} question banks ·{" "}
        {profiles.length} saved pay and role profiles
      </p>
      <div className="study-tabs" aria-label="Company views">
        <button
          aria-pressed={view === "questions"}
          onClick={() => {
            setView("questions");
            setPage(1);
          }}
        >
          Question banks
        </button>
        <button
          aria-pressed={view === "pay"}
          onClick={() => {
            setView("pay");
            setPage(1);
          }}
        >
          Pay & role comparison
        </button>
        <Link href="/library/system-design/00_company_tiers_and_compensation_guide">
          Full career guide <ArrowUpRight size={14} />
        </Link>
      </div>
      <div className="study-filters">
        <label className="catalog-search">
          <Search size={16} />
          <input
            aria-label="Search companies and roles"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            placeholder="Company, role, location, AI focus..."
          />
        </label>
        <details className="advanced-filters">
          <summary>Filter saved role profiles</summary>
          <div>
            <select
              aria-label="Company tier"
              value={tier}
              onChange={(e) => {
                setTier(e.target.value);
                setPage(1);
              }}
            >
              <option value="all">All saved tiers</option>
              {[...new Set(profiles.map((p) => p.tier))].map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
            <select
              aria-label="Work-life balance"
              value={wlb}
              onChange={(e) => {
                setWlb(e.target.value);
                setPage(1);
              }}
            >
              <option value="all">All WLB notes</option>
              {[...new Set(profiles.map((p) => p.wlb))].map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
            <select
              aria-label="Role focus"
              value={domain}
              onChange={(e) => {
                setDomain(e.target.value);
                setPage(1);
              }}
            >
              <option value="all">All role focus areas</option>
              {[
                "GenAI",
                "Agents",
                "Computer Vision",
                "RecSys & ML",
                "AI Infra",
                "FDE",
              ].map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </div>
        </details>
        <button
          className="text-button"
          onClick={() => {
            setQuery("");
            setTier("all");
            setWlb("all");
            setDomain("all");
            setPage(1);
          }}
        >
          Clear filters
        </button>
      </div>
      <p className="study-data-note">
        {view === "pay"
          ? referenceNote
          : "Question frequencies and periods come from the saved banks. Use them to choose practice topics; they do not predict an interview."}
      </p>
      <div className="study-result-heading">
        <span>
          {count} matching {view === "pay" ? "profiles" : "companies"}
        </span>
      </div>
      {view === "questions" ? (
        <div className="company-grid">
          {filtered.slice((current - 1) * 24, current * 24).map((c) => (
            <Link
              className="company-card"
              href={`/companies/${c.slug}`}
              key={c.slug}
            >
              <div className="company-card-heading">
                <Building2 size={20} />
                <span>{c.questions} questions</span>
                <ArrowUpRight size={17} />
              </div>
              <h2>{c.name}</h2>
              {c.profiles[0] ? (
                <>
                  <p>{c.profiles[0].aiDomain}</p>
                  <div className="company-card-pay">
                    <span>Senior total comp</span>
                    <strong>{c.profiles[0].seniorTC}</strong>
                    <small>{c.profiles[0].location}</small>
                  </div>
                  <span className="company-card-footer">
                    Pay, roles, and question bank
                  </span>
                </>
              ) : (
                <>
                  <p>
                    Recorded problem frequency, difficulty, and reporting
                    periods.
                  </p>
                  <span className="company-card-footer">
                    Open question bank
                  </span>
                </>
              )}
            </Link>
          ))}
        </div>
      ) : (
        <div className="table-scroll study-table-wrap">
          <table className="study-table pay-table">
            <thead>
              <tr>
                <th>Company / location</th>
                <th>Senior base</th>
                <th>Senior total</th>
                <th>Staff total</th>
                <th>Roles & interview focus</th>
              </tr>
            </thead>
            <tbody>
              {payRows.slice((current - 1) * 24, current * 24).map((p) => (
                <tr key={`${p.slug}-${p.location}`}>
                  <td>
                    <Link href={`/companies/${p.slug}?view=pay`}>
                      <h3>{p.name}</h3>
                    </Link>
                    <p>{p.location}</p>
                    <span>{p.seniorLvl}</span>
                    <small>
                      {p.tier} · {p.wlb} WLB note
                    </small>
                  </td>
                  <td>{p.seniorBase}</td>
                  <td>
                    {p.seniorTC}
                    <small>{p.equityType}</small>
                  </td>
                  <td>{p.staffTC}</td>
                  <td>
                    <p>{p.aiRoles}</p>
                    <small>{p.interviewFocus}</small>
                    <Link href={`/companies/${p.slug}?view=pay`}>
                      Role profile <ArrowUpRight size={12} />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {!count && (
        <div className="empty-state">
          <h3>No companies match these filters.</h3>
          <p>Clear filters to see the complete directory.</p>
        </div>
      )}
      <Pagination page={current} pages={pages} onChange={setPage} />
    </div>
  );
}
export function CompanyProfileView({
  company,
  questions,
  initialView = "questions",
}: {
  company: Company;
  questions: CompanyQuestion[];
  initialView?: string;
}) {
  const [view, setView] = useState(
    (initialView === "pay" || !questions.length) && company.profiles.length
      ? "pay"
      : "questions",
  );
  return (
    <div className="page-container study-page">
      <Link className="back-link" href="/companies">
        ← All companies
      </Link>
      <div className="page-heading">
        <div className="eyebrow">COMPANY STUDY PLAN</div>
        <h1>{company.name}</h1>
        <p>
          {questions.length} recorded questions
          {company.profiles.length
            ? ` · ${company.profiles.length} pay and role ${company.profiles.length === 1 ? "profile" : "profiles"}`
            : ""}
          . Open a local walkthrough where one exists, or practice on LeetCode.
        </p>
      </div>
      <div className="study-tabs" aria-label="Company sections">
        <button
          aria-pressed={view === "questions"}
          onClick={() => setView("questions")}
        >
          Question bank ({questions.length})
        </button>
        {!!company.profiles.length && (
          <button aria-pressed={view === "pay"} onClick={() => setView("pay")}>
            Pay & roles ({company.profiles.length})
          </button>
        )}
      </div>
      {view === "pay" && !!company.profiles.length && (
        <>
          <p className="study-data-note">{referenceNote}</p>
          <div className="company-profile-grid">
            {company.profiles.map((p) => (
              <section
                className="study-panel company-profile"
                key={`${p.name}-${p.location}`}
              >
                <div className="eyebrow">
                  {p.tier} / {p.location}
                </div>
                <h2>{p.name}</h2>
                <p>{p.seniorLvl}</p>
                <dl className="pay-bands">
                  <div>
                    <dt>Senior base</dt>
                    <dd>{p.seniorBase}</dd>
                  </div>
                  <div>
                    <dt>Senior total comp</dt>
                    <dd>{p.seniorTC}</dd>
                  </div>
                  <div>
                    <dt>Staff total comp</dt>
                    <dd>{p.staffTC}</dd>
                  </div>
                </dl>
                <p>{p.equityType}</p>
                <h3>AI / ML roles</h3>
                <p>{p.aiRoles}</p>
                <h3>Domain focus</h3>
                <p>{p.aiFocus}</p>
                <h3>Interview preparation</h3>
                <p>{p.interviewFocus}</p>
                <h3>Saved WLB note: {p.wlb}</h3>
                <p>{p.wlbNote}</p>
                <Link
                  className="text-button"
                  href="/library/system-design/00_company_tiers_and_compensation_guide"
                >
                  Read the original career notes <ArrowUpRight size={13} />
                </Link>
              </section>
            ))}
          </div>
        </>
      )}
      {view === "questions" && <CompanyQuestionTable questions={questions} />}
    </div>
  );
}
function CompanyQuestionTable({ questions }: { questions: CompanyQuestion[] }) {
  const [query, setQuery] = useState("");
  const [difficulty, setDifficulty] = useState("all");
  const [period, setPeriod] = useState("all");
  const [sort, setSort] = useState("frequency");
  const [page, setPage] = useState(1);
  const filtered = questions
    .filter(
      (q) =>
        (difficulty === "all" || q.difficulty === difficulty) &&
        (period === "all" || q.period === period) &&
        q.title.toLowerCase().includes(query.toLowerCase()),
    )
    .sort((a, b) =>
      sort === "frequency"
        ? b.frequency - a.frequency
        : a.title.localeCompare(b.title),
    );
  const pages = Math.max(1, Math.ceil(filtered.length / 40));
  const current = Math.min(page, pages);
  return (
    <section className="company-question-section">
      <div className="section-heading">
        <h2>Questions by company</h2>
        <span>{filtered.length} questions</span>
      </div>
      <div className="study-filters">
        <label className="catalog-search">
          <Search size={16} />
          <input
            aria-label="Search company questions"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            placeholder="Find a question..."
          />
        </label>
        <select
          aria-label="Company question difficulty"
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
          aria-label="Recorded period"
          value={period}
          onChange={(e) => {
            setPeriod(e.target.value);
            setPage(1);
          }}
        >
          <option value="all">All recorded periods</option>
          {[...new Set(questions.map((q) => q.period))].sort().map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
        <select
          aria-label="Sort company questions"
          value={sort}
          onChange={(e) => {
            setSort(e.target.value);
            setPage(1);
          }}
        >
          <option value="frequency">Most recorded first</option>
          <option value="title">Title A to Z</option>
        </select>
      </div>
      <div className="table-scroll study-table-wrap">
        <table className="study-table">
          <thead>
            <tr>
              <th>Question</th>
              <th>Difficulty</th>
              <th>Recorded frequency</th>
              <th>Period in source</th>
              <th>Study links</th>
            </tr>
          </thead>
          <tbody>
            {filtered.slice((current - 1) * 40, current * 40).map((q, i) => (
              <tr key={`${q.url}-${q.period}-${i}`}>
                <td>
                  <h3>{q.title}</h3>
                  {q.number && <small>LC {q.number}</small>}
                </td>
                <td>
                  <span
                    className={`difficulty difficulty-${q.difficulty.toLowerCase()}`}
                  >
                    {q.difficulty}
                  </span>
                </td>
                <td className="mono">{q.frequency}</td>
                <td>{q.period}</td>
                <td>
                  <div className="table-links">
                    <a href={q.url} target="_blank" rel="noreferrer">
                      LeetCode <ArrowUpRight size={12} />
                    </a>
                    {q.documentId && (
                      <Link href={`/library/${q.documentId}`}>
                        Local walkthrough
                      </Link>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {!filtered.length && (
        <div className="empty-state">
          <h3>
            {questions.length
              ? "No questions match this search."
              : "No question bank is stored for this company."}
          </h3>
          <p>
            {questions.length
              ? "Try another title or filter."
              : "The saved pay and role notes remain available above."}
          </p>
        </div>
      )}
      <Pagination page={current} pages={pages} onChange={setPage} />
      <p className="study-data-note">
        Periods such as “0 - 3 months” are labels from the saved source. They
        are not relative to today.
      </p>
    </section>
  );
}
