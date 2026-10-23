"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  Bookmark,
  Check,
  Copy,
  CheckCheck,
  Code2,
} from "lucide-react";
import katex from "katex";
import { Architecture } from "./architecture";
import { SourceFigure } from "./source-figure";
import { Lab } from "./labs";
import { useProgress } from "./progress";
import type { Topic, Track } from "@/lib/content";
const sections = [
  "Architecture",
  "10-second brief",
  "Mathematical formalism",
  "Tensor flow",
  "Interview traps",
  "Implementation",
];
export function TopicGuide({
  topic,
  track,
  previous,
  next,
  suggested,
  position,
  total,
}: {
  topic: Topic;
  track: Track;
  previous?: { slug: string; title: string };
  next?: { slug: string; title: string };
  suggested?: { slug: string; title: string };
  position: number;
  total: number;
}) {
  const progress = useProgress();
  const [copied, setCopied] = useState(false);
  const [copyError, setCopyError] = useState("");
  useEffect(() => {
    if (progress.ready) progress.visit(topic.slug);
  }, [topic.slug, progress.ready]);
  async function copy() {
    try {
      await navigator.clipboard.writeText(topic.code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopyError("Copy is unavailable. Select the code to copy it.");
    }
  }
  return (
    <div className="page-container guide-container">
      <Link className="back-link" href={`/tracks/${track.id}`}>
        <ArrowLeft size={14} /> {track.title}
      </Link>
      <div className="guide-heading">
        <div>
          <div
            className="eyebrow"
            style={{ color: `var(--track-${track.id}, ${track.color})` }}
          >
            LESSON {position} OF {total} / {topic.level}
          </div>
          <h1>{topic.title}</h1>
          <div className="guide-meta">
            Practice lenses: {topic.targets.join(" · ")}
          </div>
        </div>
        <button
          className="secondary-button"
          disabled={!progress.ready}
          aria-pressed={progress.saved.includes(topic.slug)}
          onClick={() => progress.toggle("saved", topic.slug)}
        >
          <Bookmark
            size={16}
            fill={progress.saved.includes(topic.slug) ? "currentColor" : "none"}
          />
          {progress.saved.includes(topic.slug) ? "Saved" : "Save guide"}
        </button>
      </div>
      <p className="lesson-intro">{topic.summary}</p>
      <nav className="section-nav" aria-label="Guide sections">
        {sections.map((s, i) => (
          <a key={s} href={`#block-${i + 1}`}>
            <span>0{i + 1}</span>
            {s}
          </a>
        ))}
      </nav>
      {topic.explanations && (
        <details className="lesson-contents">
          <summary>Detailed lesson contents</summary>
          <div>
            {["architecture", "math", "trace"]
              .flatMap((block) =>
                topic.explanations!.filter(
                  (section) => section.block === block,
                ),
              )
              .map((section) => (
                <a key={section.id} href={`#${section.id}`}>
                  {section.title}
                </a>
              ))}
          </div>
        </details>
      )}
      <section id="block-1" className="guide-section">
        <SectionTitle n={1} title="Visual architecture & mental model" />
        <SourceFigure figure={topic.figure} />
        <Explanations topic={topic} block="architecture" />
        <details className="supporting-trace">
          <summary>Inspect the tensor trace or ASCII view</summary>
          <Architecture topic={topic} />
        </details>
        {topic.lab && <Lab kind={topic.lab} />}
        <div className="variant-grid">
          {topic.variants.map((v) => (
            <article className="variant" key={v.title}>
              <h3>{v.title}</h3>
              <pre>{v.flow}</pre>
              <p>{v.detail}</p>
            </article>
          ))}
        </div>
      </section>
      <section id="block-2" className="guide-section">
        <SectionTitle n={2} title="10-second high-yield brief" />
        <div className="brief-grid">
          <article>
            <span>WHAT IT IS</span>
            <p>{topic.summary}</p>
          </article>
          <article>
            <span>WHY IT EXISTS</span>
            <p>{topic.why}</p>
          </article>
          <article>
            <span>INTERVIEW CONTEXT</span>
            <p>{topic.interview}</p>
          </article>
        </div>
      </section>
      <section id="block-3" className="guide-section">
        <SectionTitle n={3} title="Mathematical formalism" />
        <div className="equation-box">
          {topic.equations.map((eq) => (
            <div
              className="equation"
              key={eq}
              dangerouslySetInnerHTML={{
                __html: katex.renderToString(eq, {
                  displayMode: true,
                  throwOnError: false,
                  trust: false,
                  output: "htmlAndMathml",
                }),
              }}
            />
          ))}
        </div>
        <div className="derivation">
          {topic.derivation.map((p) => (
            <p key={p}>{p}</p>
          ))}
        </div>
        <Explanations topic={topic} block="math" />
      </section>
      <section id="block-4" className="guide-section">
        <SectionTitle n={4} title="Step-by-step execution trace" />
        <div className="table-scroll">
          <table className="trace-table">
            <thead>
              <tr>
                <th>Step</th>
                <th>Operation</th>
                <th>Input shape / type</th>
                <th>Transformation</th>
                <th>Output shape / type</th>
                <th>Memory / hardware implication</th>
              </tr>
            </thead>
            <tbody>
              {topic.steps.map((s, i) => (
                <tr key={s.operation}>
                  <td className="mono accent">
                    {String(i + 1).padStart(2, "0")}
                  </td>
                  <td>{s.operation}</td>
                  <td>
                    <code>{s.input}</code>
                  </td>
                  <td>{s.transformation}</td>
                  <td>
                    <code>{s.output}</code>
                  </td>
                  <td>{s.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Explanations topic={topic} block="trace" />
      </section>
      <section id="block-5" className="guide-section">
        <SectionTitle n={5} title="Staff-level traps & failure modes" />
        <div className="trap-list">
          {topic.traps.map((t, i) => (
            <article key={t}>
              <span className="mono">{String(i + 1).padStart(2, "0")}</span>
              <p>{t}</p>
            </article>
          ))}
        </div>
        <div className="tradeoff">
          <span>PRODUCTION TRADE-OFF</span>
          <p>{topic.tradeoff}</p>
        </div>
      </section>
      <section id="block-6" className="guide-section">
        <SectionTitle n={6} title="Minimal Python / PyTorch implementation" />
        <p className="implementation-note">
          Runnable core example. Install PyTorch or NumPy when imported.
          Integration concerns are described in the traps above.
        </p>
        <div className="code-block">
          <div className="code-toolbar">
            <span>
              <Code2 size={15} /> {topic.slug}.py
            </span>
            <button onClick={copy}>
              {copied ? <CheckCheck size={14} /> : <Copy size={14} />}{" "}
              {copied ? "Copied" : "Copy code"}
            </button>
          </div>
          <pre>
            <code>{topic.code}</code>
          </pre>
        </div>
        {copyError && <p role="status">{copyError}</p>}
        <div className="sources">
          <span className="eyebrow">PRIMARY SOURCES</span>
          {topic.sources.map((s) => (
            <a href={s.url} key={s.url} target="_blank" rel="noreferrer">
              {s.title}
              <ArrowUpRight size={13} />
            </a>
          ))}
        </div>
      </section>
      {suggested && topic.nextTopicReason && (
        <Link className="next-topic-callout" href={`/topics/${suggested.slug}`}>
          <span className="eyebrow">
            {suggested.slug === next?.slug ? "NEXT LESSON" : "CONNECTED LESSON"}
          </span>
          <strong>
            {suggested.title} <ArrowRight size={16} />
          </strong>
          <p>{topic.nextTopicReason}</p>
        </Link>
      )}
      {topic.relatedTopics && (
        <details className="related-topics">
          <summary>Explore related topics</summary>
          <div>
            {topic.relatedTopics.map((related) => (
              <Link href={`/topics/${related.slug}`} key={related.slug}>
                <h3>
                  {related.title} <ArrowUpRight size={16} />
                </h3>
                <p>{related.reason}</p>
              </Link>
            ))}
          </div>
        </details>
      )}
      <div className="complete-guide">
        <div>
          <h3>Can you redraw this without the guide?</h3>
          <p>
            Explain the shapes, derive the objective, and name a failure mode.
          </p>
        </div>
        <button
          className={
            progress.completed.includes(topic.slug)
              ? "secondary-button"
              : "primary-button"
          }
          disabled={!progress.ready}
          aria-pressed={progress.completed.includes(topic.slug)}
          onClick={() => progress.toggle("completed", topic.slug)}
        >
          <Check size={17} />
          {progress.completed.includes(topic.slug)
            ? "Studied"
            : "Mark as studied"}
        </button>
      </div>
      <div className="guide-pagination">
        {previous ? (
          <Link href={`/topics/${previous.slug}`}>
            <span>
              <ArrowLeft size={13} /> PREVIOUS GUIDE
            </span>
            {previous.title}
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link href={`/topics/${next.slug}`}>
            <span>
              NEXT GUIDE <ArrowRight size={13} />
            </span>
            {next.title}
          </Link>
        ) : (
          <Link href="/ai-ml">
            <span>END OF TRACK</span>Choose another AI / ML track{" "}
            <ArrowRight size={14} />
          </Link>
        )}
      </div>
    </div>
  );
}
function Explanations({
  topic,
  block,
}: {
  topic: Topic;
  block: "architecture" | "math" | "trace";
}) {
  return topic.explanations
    ?.filter((section) => section.block === block)
    .map((section) => (
      <article className="lesson-section" id={section.id} key={section.id}>
        <h3>{section.title}</h3>
        {section.figure && <SourceFigure figure={section.figure} />}
        {section.flow && <pre className="lesson-flow">{section.flow}</pre>}
        {section.paragraphs.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
        {section.equations && (
          <div className="equation-box">
            {section.equations.map((equation) => (
              <div
                className="equation"
                key={equation}
                dangerouslySetInnerHTML={{
                  __html: katex.renderToString(equation, {
                    displayMode: true,
                    throwOnError: false,
                    trust: false,
                    output: "htmlAndMathml",
                  }),
                }}
              />
            ))}
          </div>
        )}
        {section.table && (
          <div className="table-scroll">
            <table className="lesson-table">
              <thead>
                <tr>
                  {section.table.headers.map((header) => (
                    <th key={header}>{header}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {section.table.rows.map((row, i) => (
                  <tr key={i}>
                    {row.map((cell, j) => (
                      <td key={j}>{cell}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {section.bullets && (
          <ul>
            {section.bullets.map((bullet) => (
              <li key={bullet}>{bullet}</li>
            ))}
          </ul>
        )}
      </article>
    ));
}
function SectionTitle({ n, title }: { n: number; title: string }) {
  return (
    <div className="block-heading">
      <span className="mono">0{n}</span>
      <h2>{title}</h2>
    </div>
  );
}
