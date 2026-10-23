"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { ArrowRight, ArrowLeft, Bookmark, Check, Search } from "lucide-react";
import { useProgress } from "./progress";
import type { Topic, Track } from "@/lib/content";
import type { StudyNote } from "@/lib/study";
const preparation: Record<string, string> = {
  "deep-learning":
    "Before you start: matrix multiplication, gradients, and basic neural networks. Each lesson traces the tensor shapes and operations.",
  genai:
    "Before you start: Transformer basics and embeddings. New to these? Begin with the Deep Learning & LLMs track.",
  "computer-vision":
    "Before you start: tensors, convolutions, and gradient descent. Follow the track from convolutional models to detection and generation.",
  "classical-ml":
    "Before you start: basic probability, vectors, and derivatives. Follow the objectives and assumptions through each model.",
};
export function Catalog({
  topics,
  tracks,
  initialQuery = "",
  initialTrack = "all",
  savedOnly = false,
  trackPage = false,
  fieldGuides = [],
}: {
  topics: Topic[];
  tracks: Track[];
  initialQuery?: string;
  initialTrack?: string;
  savedOnly?: boolean;
  trackPage?: boolean;
  fieldGuides?: StudyNote[];
}) {
  const [query, setQuery] = useState(initialQuery);
  const [track, setTrack] = useState(
    tracks.some((t) => t.id === initialTrack) ? initialTrack : "all",
  );
  const progress = useProgress();
  const selectedTrack = tracks.find((t) => t.id === track);
  const members = topics.filter((t) => !trackPage || t.track === track);
  const last = members.find(
    (t) => t.slug === progress.last && !progress.completed.includes(t.slug),
  );
  const next =
    last ?? members.find((t) => !progress.completed.includes(t.slug));
  const completed = members.filter((t) =>
    progress.completed.includes(t.slug),
  ).length;
  const results = useMemo(
    () =>
      topics.filter(
        (t) =>
          (track === "all" || t.track === track) &&
          (!savedOnly || progress.saved.includes(t.slug)) &&
          [
            t.title,
            t.summary,
            ...t.derivation,
            ...(t.explanations ?? []).flatMap((s) => [
              s.title,
              ...s.paragraphs,
            ]),
            ...t.traps,
          ]
            .join(" ")
            .toLowerCase()
            .includes(query.toLowerCase()),
      ),
    [topics, track, savedOnly, progress.saved, query],
  );
  const lessons = (
    <>
      <div className="catalog-toolbar">
        <label className="catalog-search">
          <Search size={17} />
          <input
            aria-label="Filter topics"
            placeholder="Find a lesson or concept..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        {!trackPage && (
          <select
            aria-label="Filter by track"
            value={track}
            onChange={(e) => setTrack(e.target.value)}
          >
            <option value="all">All tracks</option>
            {tracks.map((t) => (
              <option key={t.id} value={t.id}>
                {t.title}
              </option>
            ))}
          </select>
        )}
        <span className="muted">{results.length} lessons</span>
        {(query || (!trackPage && track !== "all")) && (
          <button
            className="text-button"
            onClick={() => {
              setQuery("");
              if (!trackPage) setTrack("all");
            }}
          >
            Clear filters
          </button>
        )}
      </div>
      <div className="topic-list">
        {results.map((topic) => (
          <article className="topic-row learner-topic-row" key={topic.slug}>
            <span className="row-index mono">
              {String(topic.order).padStart(2, "0")}
            </span>
            <div className="lesson-row-body">
              <Link href={`/topics/${topic.slug}`} className="topic-row-link">
                <h3>
                  {topic.title}
                  {progress.completed.includes(topic.slug) && (
                    <Check size={16} className="accent" aria-label="Studied" />
                  )}
                </h3>
                <p>{topic.summary}</p>
              </Link>
              {!trackPage && (
                <span className="path-count">
                  {tracks.find((t) => t.id === topic.track)?.title}
                </span>
              )}
              {!!topic.explanations?.length && (
                <details className="lesson-preview">
                  <summary>What you will learn</summary>
                  <ul>
                    {topic.explanations.map((s) => (
                      <li key={s.id}>
                        <Link href={`/topics/${topic.slug}#${s.id}`}>
                          {s.title}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </div>
            <button
              className="icon-button save-button"
              aria-label={`${progress.saved.includes(topic.slug) ? "Unsave" : "Save"} ${topic.title}`}
              aria-pressed={progress.saved.includes(topic.slug)}
              disabled={!progress.ready}
              onClick={() => progress.toggle("saved", topic.slug)}
            >
              <Bookmark
                size={17}
                fill={
                  progress.saved.includes(topic.slug) ? "currentColor" : "none"
                }
              />
            </button>
          </article>
        ))}
      </div>
      {!results.length && (
        <div className="empty-state">
          <h3>{savedOnly ? "No saved lessons match." : "No lessons match."}</h3>
          <p>
            {savedOnly
              ? "Use the bookmark beside a lesson to save it here."
              : "Try another search or clear your filters."}
          </p>
        </div>
      )}
    </>
  );
  return (
    <div className="page-container study-page learning-catalog">
      {trackPage && (
        <Link className="back-link" href="/ai-ml">
          <ArrowLeft size={14} />
          All AI / ML tracks
        </Link>
      )}
      <div className="page-heading">
        <div className="eyebrow">
          {trackPage
            ? "AI / ML LEARNING TRACK"
            : savedOnly
              ? "YOUR STUDY"
              : "LEARN AI / ML"}
        </div>
        <h1>
          {trackPage && selectedTrack
            ? selectedTrack.title
            : savedOnly
              ? "Saved AI / ML lessons"
              : "AI & ML"}
        </h1>
        <p>
          {trackPage && selectedTrack
            ? selectedTrack.description
            : savedOnly
              ? "Your bookmarked lessons, collected in one place."
              : "Choose one track and follow its lesson order. After the foundations, work through an applied system design guide."}
        </p>
      </div>
      {trackPage && selectedTrack ? (
        <>
          <section className="study-panel track-start">
            <div>
              <span className="eyebrow">
                {completed} OF {members.length} LESSONS STUDIED
              </span>
              <p>{preparation[selectedTrack.id]}</p>
              <div className="progress-bar">
                <span
                  style={{ width: `${(completed / members.length) * 100}%` }}
                />
              </div>
            </div>
            {next ? (
              <Link className="primary-button" href={`/topics/${next.slug}`}>
                {last ? "Resume" : completed ? "Continue" : "Start"}:{" "}
                {next.title}
                <ArrowRight size={16} />
              </Link>
            ) : (
              <Link className="secondary-button" href="/ai-ml">
                Explore another track <ArrowRight size={16} />
              </Link>
            )}
          </section>
          <div className="section-heading">
            <h2>Lessons in order</h2>
            <span>Open a lesson to study it in full.</span>
          </div>
          {lessons}
        </>
      ) : savedOnly ? (
        <>
          <Link className="back-link" href="/ai-ml">
            Browse all learning tracks <ArrowRight size={14} />
          </Link>
          {lessons}
        </>
      ) : (
        <>
          {last && (
            <div className="study-panel continue-panel">
              <div>
                <span className="eyebrow">LAST AI / ML LESSON</span>
                <h2>{last.title}</h2>
              </div>
              <Link className="primary-button" href={`/topics/${last.slug}`}>
                Resume lesson <ArrowRight size={16} />
              </Link>
            </div>
          )}
          <div className="section-heading">
            <h2>Learning tracks</h2>
            <span>4 tracks · 28 lessons</span>
          </div>
          <div className="track-cards learner-track-cards">
            {tracks.map((t, index) => {
              const count = topics.filter(
                (topic) => topic.track === t.id,
              ).length;
              const done = topics.filter(
                (topic) =>
                  topic.track === t.id &&
                  progress.completed.includes(topic.slug),
              ).length;
              return (
                <Link
                  href={`/tracks/${t.id}`}
                  key={t.id}
                  className="track-card"
                  style={
                    {
                      "--track-color": `var(--track-${t.id}, ${t.color})`,
                    } as React.CSSProperties
                  }
                >
                  <div>
                    <span className="mono">0{index + 1}</span>
                    <ArrowRight size={17} />
                  </div>
                  <h3>{t.title}</h3>
                  <p>{t.description}</p>
                  <div className="track-card-footer">
                    <span>{count} lessons</span>
                    <span>{done} studied</span>
                  </div>
                </Link>
              );
            })}
          </div>
          <p className="learning-advice">
            New to language models? Start with Deep Learning & LLMs, then move
            to GenAI. Choose Classical ML & Statistics for model objectives and
            statistical reasoning.
          </p>
          <details
            className="all-lessons"
            open={!!initialQuery || initialTrack !== "all"}
          >
            <summary>Find an individual lesson</summary>
            {lessons}
          </details>
          <section className="applied-guides" id="applied-systems">
            <div className="section-heading">
              <h2>Apply it in system design</h2>
              <span>{fieldGuides.length} guides</span>
            </div>
            <p>
              Use these after the relevant lessons to connect the model to a
              production system.
            </p>
            <div className="document-list">
              {fieldGuides.map((note) => (
                <Link href={`/library/${note.id}`} key={note.id}>
                  <div>
                    <h3>{note.shortTitle}</h3>
                    <p>{note.summary}</p>
                  </div>
                  <ArrowRight size={16} />
                </Link>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
