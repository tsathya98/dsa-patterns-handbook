import fs from "node:fs";
import path from "node:path";
import { getDocument, getSource, getTopics } from "@/lib/content";
import { PythonPlayground } from "@/components/python-playground";
export const metadata = { title: "Python playground" };
export default async function PlaygroundPage({
  searchParams,
}: {
  searchParams: Promise<{ document?: string; topic?: string }>;
}) {
  const params = await searchParams;
  const doc = params.document ? getDocument(params.document) : null;
  const topic = params.topic
    ? getTopics().find((t) => t.slug === params.topic)
    : null;
  const blocks = doc
    ? [...doc.content.matchAll(/```(?:python|py)\s*\n([\s\S]*?)```/g)].map(
        (m) => m[1].trim(),
      )
    : [];
  const source = doc ? getSource(doc.path.replace(/\.md$/, ".py")) : null;
  const initialCode = source?.code ?? blocks[0] ?? topic?.code;
  const templates = JSON.parse(
    fs.readFileSync(
      path.resolve(
        process.cwd(),
        "../../content/indexes/playground-templates.json",
      ),
      "utf8",
    ),
  );
  return (
    <PythonPlayground
      key={params.document ?? params.topic ?? "default"}
      templates={templates}
      initialCode={initialCode}
      sourceTitle={doc?.title ?? topic?.title}
      sourceHref={
        doc ? `/library/${doc.id}` : topic ? `/topics/${topic.slug}` : undefined
      }
    />
  );
}
