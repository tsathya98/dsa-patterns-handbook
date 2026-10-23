import { notFound } from "next/navigation";
import { getTopics, getTracks } from "@/lib/content";
import { TopicGuide } from "@/components/topic-guide";
export const dynamicParams = false;
export function generateStaticParams() {
  return getTopics().map((t) => ({ slug: t.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const topic = getTopics().find((t) => t.slug === slug);
  return {
    title: topic?.title ?? "Guide not found",
    description: topic?.summary,
  };
}
export default async function TopicPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const topics = getTopics();
  const index = topics.findIndex((t) => t.slug === slug);
  if (index < 0) notFound();
  const topic = topics[index];
  const summarize = (t: typeof topic | undefined) =>
    t ? { slug: t.slug, title: t.title } : undefined;
  return (
    <TopicGuide
      key={slug}
      topic={topic}
      track={getTracks().find((t) => t.id === topic.track)!}
      previous={summarize(
        topics
          .filter((t) => t.track === topic.track)
          .find((t) => t.order === topic.order - 1),
      )}
      next={summarize(
        topics.find(
          (t) => t.track === topic.track && t.order === topic.order + 1,
        ),
      )}
      suggested={summarize(topics.find((t) => t.slug === topic.nextTopic))}
      position={
        topics
          .filter((t) => t.track === topic.track)
          .findIndex((t) => t.slug === slug) + 1
      }
      total={topics.filter((t) => t.track === topic.track).length}
    />
  );
}
