import fs from "node:fs";
import path from "node:path";
import { cache } from "react";
import { getDocuments } from "./content";

export type StudyStatus = "todo" | "solved" | "review";
export type Problem = {
  number: number;
  displayNum: string;
  title: string;
  difficulty: string;
  topic: string;
  pattern: string;
  url: string;
  docPath: string;
  documentId: string | null;
  summary: string;
  in150: boolean;
  in75: boolean;
  inHW: boolean;
  defaultSolved: boolean;
  companies: string[];
  companyFreq: Record<string, number>;
};
export type StudyNote = {
  id: string;
  path: string;
  title: string;
  shortTitle: string;
  category: string;
  categoryLabel: string;
  summary: string;
  docType: string;
  pattern: string;
  lcNumber: number | null;
  difficulty: string;
};
export type CompanyProfile = {
  name: string;
  slug: string;
  tier: string;
  location: string;
  seniorLvl: string;
  seniorBase: string;
  seniorTC: string;
  staffTC: string;
  equityType: string;
  wlb: string;
  wlbNote: string;
  interviewFocus: string;
  aiDomain: string;
  aiFocus: string;
  aiRoles: string;
  tags: string[];
};
export type CompanyQuestion = {
  title: string;
  difficulty: string;
  frequency: number;
  period: string;
  url: string;
  documentId: string | null;
  number: number | null;
};
export type Company = {
  slug: string;
  name: string;
  questions: number;
  profiles: CompanyProfile[];
};
const root = path.resolve(process.cwd(), "../../content");
export const getStudyCatalog = cache(
  (): {
    problems: Problem[];
    notes: StudyNote[];
    companyProfiles: CompanyProfile[];
  } =>
    JSON.parse(
      fs.readFileSync(path.join(root, "indexes/study-catalog.json"), "utf8"),
    ),
);
export const getCompanyQuestions = cache((slug: string): CompanyQuestion[] => {
  // Only IDs from the repository index are allowed to reach a file read.
  const doc = getDocuments().find((d) => d.id === `companies/${slug}`);
  if (!doc) return [];
  const problems = getStudyCatalog().problems;
  const bySlug = new Map(
    problems.map((p) => [p.url.match(/problems\/([^/]+)/)?.[1], p]),
  );
  return fs
    .readFileSync(path.join(root, doc.path), "utf8")
    .split("\n")
    .flatMap((line) => {
      const parts = line.split("|").map((x) => x.trim());
      if (
        parts.length < 8 ||
        !/^https:\/\/leetcode\.com\/problems\//.test(parts[6])
      )
        return [];
      const linked = bySlug.get(parts[6].match(/problems\/([^/]+)/)?.[1]);
      return [
        {
          title: parts[2],
          difficulty: parts[3],
          frequency: Number(parts[4]) || 0,
          period: parts[5],
          url: parts[6],
          documentId: linked?.documentId ?? null,
          number: linked?.number ?? null,
        },
      ];
    });
});
export const getCompanies = cache((): Company[] => {
  const profiles = getStudyCatalog().companyProfiles;
  const banks = getDocuments().filter((d) => d.bucket === "Companies");
  const slugs = new Set([
    ...banks.map((d) => d.id.split("/")[1]),
    ...profiles.map((p) => p.slug),
  ]);
  return [...slugs]
    .map((slug) => {
      const companyProfiles = profiles.filter((p) => p.slug === slug);
      const bank = banks.find((d) => d.id === `companies/${slug}`);
      const text = bank
        ? fs.readFileSync(path.join(root, bank.path), "utf8")
        : "";
      const rows = text
        .split("\n")
        .filter((line) => line.includes("https://leetcode.com/problems/"));
      return {
        slug,
        name:
          rows[0]?.split("|")[1]?.trim() ||
          companyProfiles[0]?.name ||
          slug.replaceAll("-", " "),
        questions: rows.length,
        profiles: companyProfiles,
      };
    })
    .sort((a, b) => a.name.localeCompare(b.name));
});
export function getNoteGroups(
  kind: string,
): { title: string; notes: StudyNote[] }[] {
  const notes = getStudyCatalog()
    .notes.filter((note) => {
      if (kind === "concepts")
        return note.docType === "concept" && note.id.startsWith("dsa/");
      if (kind === "system-design") return note.docType === "system_design";
      if (kind === "ai-ml") return note.docType === "ai";
      if (kind === "cheat-sheets") return note.docType === "cheat_sheet";
      return note.id.startsWith("plans/");
    })
    .map((note) =>
      note.id.includes("company_tiers_and_compensation")
        ? { ...note, categoryLabel: "Career reference" }
        : note.id.includes("excalidraw_practice")
          ? { ...note, categoryLabel: "Whiteboard practice" }
          : note,
    );
  const titles = [...new Set(notes.map((note) => note.categoryLabel))];
  const rank = (title: string) =>
    title === "Career reference" ? 2 : title === "Whiteboard practice" ? 1 : 0;
  return titles
    .sort((a, b) => rank(a) - rank(b))
    .map((title) => ({
      title,
      notes: notes.filter((note) => note.categoryLabel === title),
    }));
}
