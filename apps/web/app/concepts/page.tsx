import { StudyHub } from "@/components/study-hub";
import { getNoteGroups } from "@/lib/study";
export const metadata = { title: "DSA concepts" };
export default function Page() {
  return (
    <StudyHub
      title="DSA concepts"
      description="Build the mental models behind the problem lists. Read the original concept notes, then apply the pattern in practice."
      kind="concepts"
      groups={getNoteGroups("concepts")}
    />
  );
}
