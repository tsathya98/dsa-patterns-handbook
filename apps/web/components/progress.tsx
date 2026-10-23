"use client";
import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

type Progress = { completed: string[]; saved: string[]; last: string | null };
type Store = Progress & {
  ready: boolean;
  warning: string;
  toggle: (kind: "completed" | "saved", slug: string) => void;
  visit: (slug: string) => void;
};
const empty: Progress = { completed: [], saved: [], last: null };
const key = "interview-atlas.progress.v1";
const Context = createContext<Store>({
  ...empty,
  ready: false,
  warning: "",
  toggle: () => {},
  visit: () => {},
});
export function ProgressProvider({ children }: { children: ReactNode }) {
  const [progress, setProgress] = useState<Progress>(empty);
  const [ready, setReady] = useState(false);
  const [warning, setWarning] = useState("");
  useEffect(() => {
    try {
      const value = JSON.parse(localStorage.getItem(key) ?? "null");
      if (
        value &&
        Array.isArray(value.completed) &&
        Array.isArray(value.saved)
      ) {
        setProgress({
          completed: value.completed.filter(
            (x: unknown) => typeof x === "string",
          ),
          saved: value.saved.filter((x: unknown) => typeof x === "string"),
          last: typeof value.last === "string" ? value.last : null,
        });
      }
    } catch {
      setWarning("Saved progress could not be loaded. You can keep studying.");
    }
    setReady(true);
    function sync(event: StorageEvent) {
      if (event.key !== key) return;
      try {
        const value = JSON.parse(event.newValue ?? "null");
        if (
          value &&
          Array.isArray(value.completed) &&
          Array.isArray(value.saved)
        ) {
          setProgress({
            completed: value.completed.filter(
              (x: unknown) => typeof x === "string",
            ),
            saved: value.saved.filter((x: unknown) => typeof x === "string"),
            last: typeof value.last === "string" ? value.last : null,
          });
        }
      } catch {
        /* Keep the current session if another tab writes invalid data. */
      }
    }
    window.addEventListener("storage", sync);
    return () => window.removeEventListener("storage", sync);
  }, []);
  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem(key, JSON.stringify(progress));
    } catch {
      setWarning(
        "Browser storage is unavailable. Progress will last for this session.",
      );
    }
  }, [progress, ready]);
  function toggle(kind: "completed" | "saved", slug: string) {
    setProgress((p) => ({
      ...p,
      [kind]: p[kind].includes(slug)
        ? p[kind].filter((s) => s !== slug)
        : [...p[kind], slug],
    }));
  }
  function visit(slug: string) {
    setProgress((p) => (p.last === slug ? p : { ...p, last: slug }));
  }
  return (
    <Context.Provider value={{ ...progress, ready, warning, toggle, visit }}>
      {children}
    </Context.Provider>
  );
}
export const useProgress = () => useContext(Context);
