"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, type ReactNode } from "react";
import {
  ArrowUpRight,
  BookOpen,
  Bookmark,
  ChevronRight,
  Command,
  Home,
  Code2,
  Network,
  Brain,
  Building2,
  Layers3,
  ListChecks,
  Map,
  Timer,
  Menu,
  Search,
  X,
} from "lucide-react";
import { useProgress } from "./progress";
import { FocusMini } from "./focus-timer";
import { ThemeToggle } from "./theme-toggle";
import type { Track } from "@/lib/content";
export function Shell({
  children,
  tracks,
  topics,
  documents,
}: {
  children: ReactNode;
  documents: { id: string; title: string; section: string }[];
  tracks: Track[];
  topics: { slug: string; title: string; track: string }[];
}) {
  const pathname = usePathname();
  const router = useRouter();
  const [menu, setMenu] = useState(false);
  const [query, setQuery] = useState("");
  const progress = useProgress();
  const currentTopic = topics.find(
    (topic) => pathname === `/topics/${topic.slug}`,
  );
  const currentTrack = tracks.find(
    (track) =>
      pathname === `/tracks/${track.id}` || currentTopic?.track === track.id,
  );
  const currentDocument = documents.find(
    (document) =>
      pathname === `/library/${document.id}` ||
      pathname === `/source/${document.id}.py`,
  );
  return (
    <div className="workspace">
      <a href="#main" className="skip-link">
        Skip to content
      </a>
      <aside
        className={`sidebar ${menu ? "is-open" : ""}`}
        aria-label="Main navigation"
      >
        <Link href="/" className="brand" onClick={() => setMenu(false)}>
          <span className="brand-icon">
            <Command size={23} />
          </span>
          <span>
            interview<span className="brand-light">atlas</span>
          </span>
        </Link>
        <div className="sidebar-label">LEARN</div>
        <nav aria-label="Study subjects">
          {[
            { href: "/", label: "Overview", icon: Home },
            { href: "/concepts", label: "DSA concepts", icon: BookOpen },
            { href: "/problems", label: "Coding practice", icon: Code2 },
            { href: "/system-design", label: "System design", icon: Network },
            { href: "/ai-ml", label: "AI & ML", icon: Brain },
            { href: "/companies", label: "Company prep", icon: Building2 },
          ].map((item) => {
            const active =
              item.href === "/"
                ? pathname === "/"
                : pathname.startsWith(item.href) ||
                  currentDocument?.section === item.href ||
                  (item.href === "/ai-ml" && !!currentTrack);
            return (
              <Link
                key={item.href}
                className={`nav-item ${active ? "active" : ""}`}
                aria-current={active ? "page" : undefined}
                href={item.href}
                onClick={() => setMenu(false)}
              >
                <item.icon size={17} />
                {item.label}
              </Link>
            );
          })}
        </nav>
        {currentTrack && (
          <details className="current-track-nav" key={currentTrack.id}>
            <summary>In this track</summary>
            <nav className="track-nav" aria-label={currentTrack.title}>
              <Link
                href={`/tracks/${currentTrack.id}`}
                onClick={() => setMenu(false)}
              >
                Track overview
              </Link>
              {topics
                .filter((topic) => topic.track === currentTrack.id)
                .map((topic) => (
                  <Link
                    key={topic.slug}
                    href={`/topics/${topic.slug}`}
                    aria-current={
                      currentTopic?.slug === topic.slug ? "page" : undefined
                    }
                    onClick={() => setMenu(false)}
                  >
                    {topic.title}
                  </Link>
                ))}
            </nav>
          </details>
        )}
        <div className="sidebar-label nav-group-label">YOUR STUDY</div>
        <nav aria-label="Your study">
          <Link
            className={`nav-item ${pathname === "/tracker" ? "active" : ""}`}
            href="/tracker"
            onClick={() => setMenu(false)}
          >
            <ListChecks size={17} />
            Review queue
          </Link>
          <Link
            className="nav-item"
            href="/ai-ml?saved=1"
            onClick={() => setMenu(false)}
          >
            <Bookmark size={17} />
            Saved AI / ML lessons
            <span className="nav-count">{progress.saved.length}</span>
          </Link>
          <Link
            className={`nav-item ${pathname === "/roadmap" || currentDocument?.section === "/roadmap" ? "active" : ""}`}
            href="/roadmap"
            onClick={() => setMenu(false)}
          >
            <Map size={17} />
            Study plan
          </Link>
        </nav>
        <details
          className="nav-utilities"
          key={pathname}
          open={
            [
              "/playground",
              "/focus",
              "/cheat-sheets",
              "/library",
              "/source",
            ].some((path) => pathname.startsWith(path)) &&
            (!currentDocument || currentDocument.section === "/cheat-sheets")
          }
        >
          <summary>Tools & reference</summary>
          <nav aria-label="Tools and reference">
            {[
              { href: "/playground", label: "Python playground", icon: Code2 },
              { href: "/focus", label: "Focus sessions", icon: Timer },
              { href: "/cheat-sheets", label: "Cheat sheets", icon: Layers3 },
              {
                href: "/library",
                label: "All reference material",
                icon: BookOpen,
              },
            ].map((item) => (
              <Link
                className={`nav-item ${(pathname.startsWith(item.href) && !currentDocument) || currentDocument?.section === item.href ? "active" : ""}`}
                key={item.href}
                href={item.href}
                onClick={() => setMenu(false)}
              >
                <item.icon size={17} />
                {item.label}
              </Link>
            ))}
            <Link
              className="nav-item"
              href="/legacy/viewer.html"
              target="_blank"
            >
              Original study hub
              <ArrowUpRight size={13} />
            </Link>
          </nav>
        </details>
        <div className="sidebar-bottom">
          <p>Progress and notes are saved in this browser.</p>
        </div>
      </aside>
      {menu && (
        <button
          className="menu-backdrop"
          onClick={() => setMenu(false)}
          aria-label="Close navigation"
        />
      )}
      <div className="main-shell">
        <header className="topbar">
          <button
            className="icon-button mobile-menu"
            onClick={() => setMenu(!menu)}
            aria-label={menu ? "Close navigation" : "Open navigation"}
          >
            {menu ? <X size={20} /> : <Menu size={20} />}
          </button>
          <div className="breadcrumbs">
            Workspace <ChevronRight size={13} />
            <span>
              {currentDocument
                ? currentDocument.title
                : currentTopic
                  ? currentTopic.title
                  : currentTrack
                    ? currentTrack.title
                    : pathname.startsWith("/library")
                      ? "Study library"
                      : ((
                          {
                            "/": "Overview",
                            "/problems": "Coding problems",
                            "/concepts": "DSA concepts",
                            "/system-design": "System design",
                            "/ai-ml": "AI & ML",
                            "/companies": "Companies, pay & roles",
                            "/cheat-sheets": "Cheat sheets",
                            "/roadmap": "Study plan",
                            "/tracker": "Review queue",
                            "/playground": "Python playground",
                            "/focus": "Focus sessions",
                            "/search": "Search",
                          } as Record<string, string>
                        )["/" + pathname.split("/")[1]] ?? "Study material")}
            </span>
          </div>
          <form
            className="global-search"
            action="/search"
            onSubmit={(e) => {
              e.preventDefault();
              router.push(`/search?q=${encodeURIComponent(query)}`);
            }}
          >
            <Search size={15} />
            <input
              name="q"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search the workspace..."
              aria-label="Search all study material"
            />
            <kbd>Enter</kbd>
          </form>
          <ThemeToggle />
          <span className="edition">
            <span className="online-dot" /> LOCAL EDITION
          </span>
          <FocusMini />
        </header>
        {progress.warning && (
          <div className="storage-warning" role="status">
            {progress.warning}
          </div>
        )}
        <main id="main">{children}</main>
        <footer className="footer">
          <span>INTERVIEW ATLAS</span>
          <span>Diagrams first. Details when you need them.</span>
          <span>Built for the whiteboard ↗</span>
        </footer>
      </div>
    </div>
  );
}
