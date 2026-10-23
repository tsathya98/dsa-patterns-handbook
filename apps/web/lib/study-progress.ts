import type { Problem, StudyStatus } from "./study";
export type FocusLog = {
  id: string;
  title: string;
  minutes: number;
  mode: string;
  time: string;
};
export type StudyData = {
  problemStatus: Record<string, StudyStatus>;
  documentStatus: Record<string, StudyStatus>;
  notes: Record<string, string>;
  customProblems: Problem[];
  pomodoroHistory: FocusLog[];
};
export const studyStorageKeys = {
  problemStatus: "dsa_hub_prob_status_v3",
  documentStatus: "dsa_hub_status_v2",
  notes: "dsa_hub_notes_v2",
  customProblems: "dsa_hub_custom_probs_v2",
  pomodoroHistory: "dsa_hub_pomo_log_v1",
};
export const emptyStudyData: StudyData = {
  problemStatus: {},
  documentStatus: {},
  notes: {},
  customProblems: [],
  pomodoroHistory: [],
};
function statusMap(value: unknown): Record<string, StudyStatus> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return Object.fromEntries(
    Object.entries(value).filter(([, s]) =>
      ["todo", "solved", "review"].includes(s),
    ),
  );
}
export function cleanStudyData(value: unknown): StudyData {
  const v =
    value && typeof value === "object" ? (value as Partial<StudyData>) : {};
  return {
    problemStatus: statusMap(v.problemStatus),
    documentStatus: statusMap(v.documentStatus),
    notes: Object.fromEntries(
      Object.entries(
        v.notes && typeof v.notes === "object" && !Array.isArray(v.notes)
          ? v.notes
          : {},
      ).filter(([, s]) => typeof s === "string"),
    ),
    customProblems: Array.isArray(v.customProblems)
      ? v.customProblems
          .filter(
            (p) =>
              p &&
              Number.isSafeInteger(p.number) &&
              p.number > 0 &&
              typeof p.title === "string" &&
              (typeof p.topic === "string" || typeof p.pattern === "string"),
          )
          .map((p) => ({
            ...p,
            displayNum: `#${p.number}`,
            difficulty: ["Easy", "Medium", "Hard"].includes(p.difficulty)
              ? p.difficulty
              : "Medium",
            topic: p.topic || p.pattern,
            pattern: p.pattern || p.topic,
            url: `https://leetcode.com/problemset/?search=${p.number}`,
            docPath: "",
            documentId: null,
            summary: "",
            in150: false,
            in75: false,
            inHW: false,
            companies: [],
            companyFreq: {},
          }))
      : [],
    pomodoroHistory: Array.isArray(v.pomodoroHistory)
      ? v.pomodoroHistory
          .filter(
            (p) =>
              p &&
              typeof p.id === "string" &&
              typeof p.title === "string" &&
              Number.isFinite(p.minutes) &&
              p.minutes >= 0 &&
              p.minutes <= 180,
          )
          .map((p) => ({
            id: p.id,
            title: p.title,
            minutes: p.minutes,
            mode: typeof p.mode === "string" ? p.mode : "Focus",
            time: typeof p.time === "string" ? p.time : "Saved session",
          }))
      : [],
  };
}
