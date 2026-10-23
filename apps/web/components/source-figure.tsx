"use client";
import { useState } from "react";
import { ArrowUpRight, ExternalLink } from "lucide-react";
import type { Topic } from "@/lib/content";
export function SourceFigure({
  figure,
  compact = false,
}: {
  figure: Topic["figure"];
  compact?: boolean;
}) {
  const [failed, setFailed] = useState(false);
  return (
    <figure className={`source-figure ${compact ? "compact-figure" : ""}`}>
      <div className="figure-toolbar">
        <span>ARTICLE FIGURE</span>
        <a href={figure.url} target="_blank" rel="noreferrer">
          Open full size <ExternalLink size={12} />
        </a>
      </div>
      <div className="figure-image">
        {failed ? (
          <div className="figure-unavailable">
            <p>The source image could not load.</p>
            <a href={figure.source} target="_blank" rel="noreferrer">
              View it in the original article <ArrowUpRight size={14} />
            </a>
          </div>
        ) : (
          <a
            href={figure.url}
            target="_blank"
            rel="noreferrer"
            aria-label={`Open full-size figure: ${figure.caption}`}
          >
            <img
              src={figure.url}
              alt={figure.caption}
              onError={() => setFailed(true)}
              referrerPolicy="no-referrer"
            />
          </a>
        )}
      </div>
      <figcaption>
        <p>{figure.caption}</p>
        <a href={figure.source} target="_blank" rel="noreferrer">
          Source: {figure.title}
          <ArrowUpRight size={12} />
        </a>
      </figcaption>
    </figure>
  );
}
