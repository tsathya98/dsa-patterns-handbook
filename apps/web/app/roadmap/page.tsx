import { StudyHub } from "@/components/study-hub";
import { getNoteGroups } from "@/lib/study";
export const metadata = { title: "Study plan" };
export default function Page() {
  return (
    <StudyHub
      title="Study plan"
      description="Choose a subject and a practice list. Use the detailed plans below when you want a longer schedule."
      kind="roadmap"
      groups={getNoteGroups("roadmap")}
    />
  );
}
