import type { Metadata } from "next";
import { ProgressProvider } from "@/components/progress";
import { Shell } from "@/components/shell";
import { getTopics, getTracks } from "@/lib/content";
import { getStudyCatalog } from "@/lib/study";
import { StudyProvider } from "@/components/study-state";
import { FocusProvider } from "@/components/focus-timer";
import { themeInitScript } from "@/lib/theme";
import "katex/dist/katex.min.css";
import "@/styles/tokens.css";
import "./globals.css";
import "@/styles/controls.css";
export const metadata: Metadata = {
  title: {
    default: "Interview Atlas | Interview Preparation",
    template: "%s | Interview Atlas",
  },
  description:
    "Coding, system design, AI and ML learning tracks, and company interview preparation.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-scroll-behavior="smooth" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body>
        <ProgressProvider>
          <StudyProvider
            defaults={getStudyCatalog().problems.map(
              ({ number, docPath, defaultSolved }) => ({
                number,
                docPath,
                defaultSolved,
              }),
            )}
          >
            <FocusProvider>
              <Shell
                documents={getStudyCatalog()
                  .notes.filter((note) => note.docType !== "company")
                  .map((note) => ({
                    id: note.id,
                    title: note.shortTitle,
                    section: note.id.startsWith("plans/")
                      ? "/roadmap"
                      : ((
                          {
                            concept: "/concepts",
                            problem: "/problems",
                            system_design: "/system-design",
                            ai: "/ai-ml",
                            cheat_sheet: "/cheat-sheets",
                          } as Record<string, string>
                        )[note.docType] ?? "/library"),
                  }))}
                tracks={getTracks()}
                topics={getTopics().map(({ slug, title, track }) => ({
                  slug,
                  title,
                  track,
                }))}
              >
                {children}
              </Shell>
            </FocusProvider>
          </StudyProvider>
        </ProgressProvider>
      </body>
    </html>
  );
}
