"use client";
import {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
import type { Problem, StudyStatus } from "@/lib/study";
import {
  cleanStudyData,
  emptyStudyData,
  studyStorageKeys,
  type FocusLog,
  type StudyData,
} from "@/lib/study-progress";
const keys = studyStorageKeys;
type Store = StudyData & {
  ready: boolean;
  warning: string;
  setStatus: (problem: Problem, status: StudyStatus) => void;
  setDocStatus: (path: string, status: StudyStatus) => void;
  setNote: (id: string, text: string) => void;
  addProblem: (problem: Problem) => void;
  importData: (value: unknown) => void;
  addFocus: (log: FocusLog) => void;
};
const Context = createContext<Store | null>(null);
export function StudyProvider({
  children,
  defaults,
}: {
  children: ReactNode;
  defaults: { number: number; docPath: string; defaultSolved: boolean }[];
}) {
  const [data, setData] = useState<StudyData>(emptyStudyData);
  const [ready, setReady] = useState(false);
  const [warning, setWarning] = useState("");
  const initial = useRef(defaults);
  useEffect(() => {
    try {
      const loaded: Record<string, unknown> = {};
      for (const [name, key] of Object.entries(keys)) {
        try {
          loaded[name] = JSON.parse(localStorage.getItem(key) ?? "null");
        } catch {
          setWarning(
            "Some saved study data could not be read. Valid records were retained; import a backup for missing records.",
          );
        }
      }
      const cleaned = cleanStudyData(loaded);
      if (!localStorage.getItem(keys.problemStatus)) {
        for (const p of initial.current) {
          const inherited = cleaned.documentStatus[p.docPath];
          if (inherited || p.defaultSolved)
            cleaned.problemStatus[`lc-${p.number}`] = inherited ?? "solved";
        }
      }
      setData(cleaned);
    } catch {
      setWarning(
        "Some saved study data could not be read. Import a backup to restore it.",
      );
    }
    setReady(true);
    function sync(event: StorageEvent) {
      const entry = Object.entries(keys).find(([, key]) => key === event.key);
      if (!entry) return;
      try {
        const value = cleanStudyData({
          [entry[0]]: JSON.parse(event.newValue ?? "null"),
        });
        setData((p) => ({
          ...p,
          [entry[0]]: value[entry[0] as keyof StudyData],
        }));
      } catch {
        /* Retain valid in-memory data. */
      }
    }
    window.addEventListener("storage", sync);
    return () => window.removeEventListener("storage", sync);
  }, []);
  useEffect(() => {
    if (!ready) return;
    try {
      for (const [name, key] of Object.entries(keys))
        localStorage.setItem(
          key,
          JSON.stringify(data[name as keyof StudyData]),
        );
    } catch {
      setWarning(
        "Browser storage is unavailable. Export progress before leaving this session.",
      );
    }
  }, [data, ready]);
  return (
    <Context.Provider
      value={{
        ...data,
        ready,
        warning,
        setStatus: (problem, status) =>
          setData((p) => ({
            ...p,
            problemStatus: {
              ...p.problemStatus,
              [`lc-${problem.number}`]: status,
            },
            documentStatus: problem.docPath
              ? { ...p.documentStatus, [problem.docPath]: status }
              : p.documentStatus,
          })),
        setDocStatus: (path, status) =>
          setData((p) => ({
            ...p,
            documentStatus: { ...p.documentStatus, [path]: status },
          })),
        setNote: (id, text) =>
          setData((p) => ({ ...p, notes: { ...p.notes, [id]: text } })),
        addProblem: (problem) =>
          setData((p) => ({
            ...p,
            customProblems: [
              ...p.customProblems.filter((x) => x.number !== problem.number),
              problem,
            ],
          })),
        addFocus: (log) =>
          setData((p) => ({
            ...p,
            pomodoroHistory: [
              log,
              ...p.pomodoroHistory.filter((entry) => entry.id !== log.id),
            ],
          })),
        importData: (value) => {
          const incoming = cleanStudyData(value);
          setData((p) => ({
            problemStatus: { ...p.problemStatus, ...incoming.problemStatus },
            documentStatus: { ...p.documentStatus, ...incoming.documentStatus },
            notes: { ...p.notes, ...incoming.notes },
            customProblems: [
              ...new Map(
                [...p.customProblems, ...incoming.customProblems].map((x) => [
                  x.number,
                  x,
                ]),
              ).values(),
            ],
            pomodoroHistory: [
              ...new Map(
                [...p.pomodoroHistory, ...incoming.pomodoroHistory].map((x) => [
                  x.id,
                  x,
                ]),
              ).values(),
            ],
          }));
        },
      }}
    >
      {children}
    </Context.Provider>
  );
}
export function useStudy() {
  const store = useContext(Context);
  if (!store) throw new Error("StudyProvider is required");
  return store;
}
export function StudyBackup() {
  const store = useStudy();
  const [message, setMessage] = useState("");
  function download() {
    const blob = new Blob(
      [
        JSON.stringify(
          {
            version: 1,
            problemStatus: store.problemStatus,
            documentStatus: store.documentStatus,
            notes: store.notes,
            customProblems: store.customProblems,
            pomodoroHistory: store.pomodoroHistory,
          },
          null,
          2,
        ),
      ],
      { type: "application/json" },
    );
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "interview-atlas-study-progress.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  return (
    <div className="study-backup">
      <button
        className="secondary-button"
        onClick={download}
        disabled={!store.ready}
      >
        Export progress
      </button>
      <label className="secondary-button">
        Import progress
        <input
          type="file"
          accept="application/json"
          onChange={async (e) => {
            try {
              const file = e.target.files?.[0];
              if (!file) return;
              const value = JSON.parse(await file.text());
              if (value.version !== 1 || !value.problemStatus)
                throw new Error("Choose a study progress export.");
              store.importData(value);
              setMessage("Progress merged. Existing entries were retained.");
            } catch {
              setMessage(
                "Could not import this file. Choose a valid study progress export.",
              );
            }
            e.target.value = "";
          }}
        />
      </label>
      <span role="status">{message}</span>
      {store.warning && <p role="status">{store.warning}</p>}
    </div>
  );
}
