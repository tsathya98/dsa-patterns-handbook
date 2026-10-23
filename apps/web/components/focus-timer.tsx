"use client";
import Link from "next/link";
import {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { useStudy } from "./study-state";
type TimerState = {
  id: string;
  title: string;
  minutes: number;
  remaining: number;
  endsAt: number | null;
};
const initial: TimerState = {
  id: "",
  title: "",
  minutes: 25,
  remaining: 1500,
  endsAt: null,
};
const Context = createContext<{
  timer: TimerState;
  seconds: number;
  ready: boolean;
  choose: (minutes: number) => void;
  toggle: () => void;
  reset: () => void;
  setTitle: (title: string) => void;
} | null>(null);
const key = "interview-atlas.focus.v1";
export function FocusProvider({ children }: { children: ReactNode }) {
  const [timer, setTimer] = useState(initial);
  const [ready, setReady] = useState(false);
  const [clock, setClock] = useState(0);
  const study = useStudy();
  const latest = useRef(study);
  latest.current = study;
  useEffect(() => {
    try {
      const value = JSON.parse(localStorage.getItem(key) ?? "null");
      if (
        value &&
        typeof value.title === "string" &&
        Number.isFinite(value.minutes) &&
        value.minutes >= 1 &&
        value.minutes <= 180 &&
        Number.isFinite(value.remaining) &&
        (value.endsAt === null || Number.isFinite(value.endsAt))
      )
        setTimer(value);
    } catch {
      /* Start with a 25 minute focus block. */
    }
    setClock(Date.now());
    setReady(true);
    const interval = setInterval(() => setClock(Date.now()), 500);
    return () => clearInterval(interval);
  }, []);
  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem(key, JSON.stringify(timer));
    } catch {
      /* The active session still works in memory. */
    }
  }, [timer, ready]);
  const seconds =
    timer.endsAt === null
      ? timer.remaining
      : Math.max(0, Math.ceil((timer.endsAt - clock) / 1000));
  useEffect(() => {
    if (!ready || !study.ready || !timer.endsAt || seconds > 0) return;
    latest.current.addFocus({
      id: timer.id,
      title: timer.title.trim() || "Focus session",
      minutes: timer.minutes,
      mode: `${timer.minutes}m focus`,
      time: new Date().toLocaleString(),
    });
    setTimer((p) => ({ ...p, endsAt: null, remaining: 0 }));
  }, [ready, study.ready, timer, seconds]);
  return (
    <Context.Provider
      value={{
        timer,
        seconds,
        ready,
        choose: (minutes) =>
          setTimer((p) => ({
            ...p,
            id: "",
            minutes,
            remaining: minutes * 60,
            endsAt: null,
          })),
        setTitle: (title) => setTimer((p) => ({ ...p, title })),
        reset: () =>
          setTimer((p) => ({
            ...p,
            id: "",
            remaining: p.minutes * 60,
            endsAt: null,
          })),
        toggle: () =>
          setTimer((p) =>
            p.endsAt
              ? {
                  ...p,
                  remaining: Math.max(
                    0,
                    Math.ceil((p.endsAt - Date.now()) / 1000),
                  ),
                  endsAt: null,
                }
              : {
                  ...p,
                  id: p.remaining > 0 && p.id ? p.id : `pomo-${Date.now()}`,
                  remaining: p.remaining || p.minutes * 60,
                  endsAt: Date.now() + (p.remaining || p.minutes * 60) * 1000,
                },
          ),
      }}
    >
      {children}
    </Context.Provider>
  );
}
function useFocus() {
  const value = useContext(Context);
  if (!value) throw new Error("FocusProvider is required");
  return value;
}
export function FocusMini() {
  const { timer, seconds } = useFocus();
  if (!timer.endsAt) return null;
  return (
    <Link
      className="focus-mini"
      href="/focus"
      aria-label="Open active focus session"
    >
      Focus {Math.floor(seconds / 60)}:{String(seconds % 60).padStart(2, "0")}
    </Link>
  );
}
export function FocusSessions() {
  const { timer, seconds, ready, choose, toggle, reset, setTitle } = useFocus();
  const study = useStudy();
  const [custom, setCustom] = useState(25);
  return (
    <div className="page-container study-page">
      <div className="page-heading">
        <div className="eyebrow">DELIBERATE PRACTICE</div>
        <h1>Focus sessions</h1>
        <p>
          Choose one task, start a focus block, and keep a record of completed
          sessions. The active timer continues across pages and reloads.
        </p>
      </div>
      <div className="focus-layout">
        <section className="study-panel focus-panel">
          <label>
            Your task
            <input
              aria-label="Focus task"
              value={timer.title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Derive attention, solve LC 88, design a queue..."
            />
          </label>
          <div className="study-tabs" aria-label="Focus presets">
            {[25, 50, 90, 5, 15].map((m) => (
              <button
                key={m}
                aria-pressed={timer.minutes === m}
                onClick={() => choose(m)}
              >
                {m} min
              </button>
            ))}
          </div>
          <div className="focus-clock" role="timer" aria-label="Time remaining">
            {Math.floor(seconds / 60)}:{String(seconds % 60).padStart(2, "0")}
          </div>
          <p>
            {timer.endsAt
              ? "Session running"
              : seconds === 0
                ? "Session complete"
                : "Ready or paused"}
          </p>
          <div className="focus-actions">
            <button
              className="primary-button"
              disabled={!ready}
              onClick={toggle}
            >
              {timer.endsAt
                ? "Pause"
                : seconds === 0
                  ? "Start again"
                  : "Start / resume"}
            </button>
            <button className="secondary-button" onClick={reset}>
              Reset
            </button>
          </div>
          <form
            className="focus-custom"
            onSubmit={(e) => {
              e.preventDefault();
              choose(Math.max(1, Math.min(180, custom)));
            }}
          >
            <label>
              Custom minutes
              <input
                type="number"
                aria-label="Custom focus minutes"
                min="1"
                max="180"
                value={custom}
                onChange={(e) => setCustom(Number(e.target.value))}
              />
            </label>
            <button className="secondary-button">Set duration</button>
          </form>
        </section>
        <section className="study-panel focus-history">
          <h2>Completed sessions</h2>
          <p>
            {study.pomodoroHistory.length} sessions ·{" "}
            {study.pomodoroHistory.reduce((sum, p) => sum + p.minutes, 0)} total
            minutes
          </p>
          {study.pomodoroHistory.length ? (
            study.pomodoroHistory.slice(0, 30).map((p) => (
              <article key={p.id}>
                <strong>{p.title}</strong>
                <span>
                  {p.minutes} min · {p.time}
                </span>
              </article>
            ))
          ) : (
            <div className="empty-state">
              <h3>No completed sessions yet.</h3>
              <p>
                Completed blocks appear here and are included in progress
                exports.
              </p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
