import { StudyHub } from "@/components/study-hub";
import { getNoteGroups } from "@/lib/study";
export const metadata = { title: "Cheat sheets" };
export default function Page() {
  return (
    <StudyHub
      title="Cheat sheets"
      description="Compact references for patterns, complexity, Python, and system design revision."
      kind="cheat-sheets"
      groups={getNoteGroups("cheat-sheets")}
    />
  );
}
