import { StudyHub } from "@/components/study-hub";
import { getNoteGroups } from "@/lib/study";
export const metadata = { title: "System design" };
export default function Page() {
  return (
    <StudyHub
      title="System design"
      description="Frameworks, distributed systems pillars, canonical HLD cases, Python LLD, and whiteboard practice."
      kind="system-design"
      groups={getNoteGroups("system-design")}
    />
  );
}
