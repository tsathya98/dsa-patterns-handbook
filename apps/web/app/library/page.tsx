import { Library } from "@/components/library";
import { getDocuments } from "@/lib/content";
export const metadata = { title: "Study library" };
export default function LibraryPage() {
  return <Library documents={getDocuments()} />;
}
