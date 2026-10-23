import Link from "next/link";
export default function NotFound() {
  return (
    <div className="page-container empty-state">
      <div className="eyebrow">404 / UNCHARTED</div>
      <h1>This guide is not here.</h1>
      <p>The topic or document could not be found.</p>
      <Link href="/" className="primary-button">
        Back to overview
      </Link>
    </div>
  );
}
