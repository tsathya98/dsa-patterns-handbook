import { ReviewQueue } from "@/components/review-queue";
import { getStudyCatalog } from "@/lib/study";
export const metadata = { title: "Review queue" };
export default function TrackerPage() {
  const catalog = getStudyCatalog();
  return <ReviewQueue problems={catalog.problems} notes={catalog.notes} />;
}
