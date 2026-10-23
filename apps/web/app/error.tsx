"use client";
export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <div className="page-container empty-state">
      <h1>The page could not load.</h1>
      <p>Your study progress is stored separately in this browser.</p>
      <button className="primary-button" onClick={reset}>
        Try again
      </button>
    </div>
  );
}
