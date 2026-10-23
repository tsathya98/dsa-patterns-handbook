"use client";
import Link from "next/link";
import { ArrowRight, Brain, Building2, Code2, Network } from "lucide-react";
import type { Problem } from "@/lib/study";
import { useStudy } from "./study-state";
import { useProgress } from "./progress";
export function WorkspaceHome({
  problems,
  topics,
  counts,
}: {
  problems: Problem[];
  topics: { slug: string; title: string }[];
  counts: {
    concepts: number;
    systemDesign: number;
    companies: number;
    profiles: number;
  };
}) {
  const study = useStudy();
  const progress = useProgress();
  const last = topics.find((topic) => topic.slug === progress.last);
  const solved75 = problems.filter(
    (p) => p.in75 && study.problemStatus[`lc-${p.number}`] === "solved",
  ).length;
  const solved150 = problems.filter(
    (p) => p.in150 && study.problemStatus[`lc-${p.number}`] === "solved",
  ).length;
  return (
    <div className="page-container study-page learner-home">
      <div className="page-heading">
        <div className="eyebrow">INTERVIEW PREPARATION</div>
        <h1>What are you studying today?</h1>
        <p>
          Choose a subject, follow its study order, then practice. Your notes
          and progress stay with you.
        </p>
      </div>
      {last && (
        <section className="study-panel continue-panel">
          <div>
            <span className="eyebrow">LAST AI / ML LESSON</span>
            <h2>{last.title}</h2>
          </div>
          <Link className="primary-button" href={`/topics/${last.slug}`}>
            Resume lesson <ArrowRight size={16} />
          </Link>
        </section>
      )}
      <div className="learning-path-grid">
        <section className="workspace-module">
          <Code2 size={25} />
          <h2>Coding interviews</h2>
          <p>
            Learn a pattern, solve problems, and revisit the ones that need
            another pass.
          </p>
          <span className="path-count">
            {counts.concepts} concept guides · {problems.length} problems
          </span>
          <Link className="primary-button" href="/concepts">
            Learn DSA concepts <ArrowRight size={15} />
          </Link>
          <Link href="/problems?plan=75">
            Practice LeetCode 75 <ArrowRight size={14} />
          </Link>
          <div className="path-progress">
            {study.ready
              ? `${solved75} / 75 solved · ${solved150} / 150 solved`
              : "Loading your progress..."}
          </div>
        </section>
        <section className="workspace-module">
          <Network size={25} />
          <h2>System design</h2>
          <p>
            Start with the interview framework, work through the fundamentals,
            then design a complete system.
          </p>
          <span className="path-count">
            {counts.systemDesign} guides · HLD & LLD
          </span>
          <Link className="primary-button" href="/system-design">
            Study system design <ArrowRight size={15} />
          </Link>
        </section>
        <section className="workspace-module">
          <Brain size={25} />
          <h2>AI & ML</h2>
          <p>
            Choose a track in deep learning, GenAI, computer vision, or
            classical ML. Apply it in a system design guide.
          </p>
          <span className="path-count">28 lessons · 5 applied guides</span>
          <Link className="primary-button" href="/ai-ml">
            Choose a learning track <ArrowRight size={15} />
          </Link>
        </section>
      </div>
      <div className="home-secondary">
        <Link className="study-panel" href="/companies">
          <Building2 size={22} />
          <div>
            <h2>Preparing for a specific company?</h2>
            <p>
              {counts.companies} question banks, plus {counts.profiles} saved
              pay and role profiles.
            </p>
          </div>
          <ArrowRight size={18} />
        </Link>
        <Link className="study-panel" href="/roadmap">
          <div>
            <h2>Need a study plan?</h2>
            <p>
              Choose a practice list and set a routine for learning and review.
            </p>
          </div>
          <ArrowRight size={18} />
        </Link>
      </div>
      <nav className="study-shortcuts" aria-label="Study shortcuts">
        <Link href="/tracker">Review queue</Link>
        <Link href="/problems?plan=150">Top Interview 150</Link>
        <Link href="/problems?plan=hw">Course exercises</Link>
        <Link href="/cheat-sheets">Cheat sheets</Link>
        <Link href="/playground">Python playground</Link>
        <Link href="/focus">Focus timer</Link>
      </nav>
    </div>
  );
}
