import fs from "node:fs";
import { decodeRouteId } from "./route-id";
import path from "node:path";
import { cache } from "react";

export type Step = {
  operation: string;
  transformation: string;
  input: string;
  output: string;
  note: string;
};
export type Topic = {
  order: number;
  slug: string;
  track: string;
  title: string;
  summary: string;
  why: string;
  interview: string;
  level: string;
  targets: string[];
  equations: string[];
  derivation: string[];
  steps: Step[];
  traps: string[];
  tradeoff: string;
  code: string;
  variants: { title: string; flow: string; detail: string }[];
  sources: { title: string; url: string }[];
  figure: { url: string; source: string; title: string; caption: string };
  lab: string | null;
  explanations?: {
    id: string;
    block: "architecture" | "math" | "trace";
    title: string;
    paragraphs: string[];
    flow?: string;
    equations?: string[];
    bullets?: string[];
    table?: { headers: string[]; rows: string[][] };
    figure?: Topic["figure"];
  }[];
  nextTopicReason?: string;
  nextTopic?: string;
  relatedTopics?: { slug: string; title: string; reason: string }[];
};
export type Track = {
  id: string;
  title: string;
  description: string;
  color: string;
};
export type Document = {
  id: string;
  title: string;
  bucket: string;
  path: string;
};
const root = path.resolve(process.cwd(), "../../content");
const curriculum = path.join(root, "curriculum");
export const getTracks = cache((): Track[] =>
  JSON.parse(fs.readFileSync(path.join(curriculum, "tracks.json"), "utf8")),
);
export const getTopics = cache((): Topic[] =>
  getTracks().flatMap((track) =>
    fs
      .readdirSync(path.join(curriculum, track.id))
      .filter((f) => f.endsWith(".json"))
      .map(
        (file) =>
          JSON.parse(
            fs.readFileSync(path.join(curriculum, track.id, file), "utf8"),
          ) as Topic,
      )
      .sort((a, b) => a.order - b.order),
  ),
);
const buckets: Record<string, string> = {
  dsa: "DSA",
  "system-design": "System design",
  "ai-ml": "AI field notes",
  "cheat-sheets": "Cheat sheets",
  companies: "Companies",
  plans: "Study plans",
};
export const getDocuments = cache((): Document[] => {
  const result: Document[] = [];
  function walk(folder: string) {
    for (const item of fs.readdirSync(folder, { withFileTypes: true })) {
      const full = path.join(folder, item.name);
      if (item.isDirectory()) walk(full);
      else if (item.name.endsWith(".md")) {
        const relative = path.relative(root, full).split(path.sep).join("/");
        const text = fs.readFileSync(full, "utf8");
        const title =
          text.match(/^#\s+(.+)$/m)?.[1]?.replace(/[*`]/g, "") ??
          item.name.replace(/\.md$/, "").replace(/[_-]/g, " ");
        result.push({
          id: relative.replace(/\.md$/, ""),
          title,
          bucket: buckets[relative.split("/")[0]],
          path: relative,
        });
      }
    }
  }
  for (const bucket of Object.keys(buckets)) walk(path.join(root, bucket));
  return result.sort((a, b) => a.title.localeCompare(b.title));
});
export function getDocument(id: string) {
  id = decodeRouteId(id);
  const doc = getDocuments().find((d) => d.id === id);
  if (!doc) return null;
  // Resolve only allowlisted repository documents; route input never becomes a raw filesystem path.
  return {
    ...doc,
    content: fs.readFileSync(path.join(root, doc.path), "utf8"),
  };
}
export function resolveDocumentLink(current: string, href: string): string {
  if (/^(?:https?:|mailto:|#)/.test(href)) return href;
  const [file, hash] = href.split("#");
  const resolved = path.posix.normalize(
    path.posix.join(path.posix.dirname(current), file),
  );
  const doc = getDocuments().find((d) => d.path === resolved);
  if (doc) return `/library/${doc.id}${hash ? `#${hash}` : ""}`;
  if (resolved.endsWith(".py") && getSource(resolved))
    return `/source/${resolved}`;
  return href;
}

export function getSource(relative: string) {
  relative = decodeRouteId(relative);
  const doc = getDocuments().find(
    (d) => d.path.replace(/\.md$/, ".py") === relative,
  );
  if (!doc || !fs.existsSync(path.join(root, relative))) return null;
  return {
    title: doc.title,
    documentId: doc.id,
    path: relative,
    code: fs.readFileSync(path.join(root, relative), "utf8"),
  };
}
