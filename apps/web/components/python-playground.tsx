"use client";
import Link from "next/link";
import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";
const PythonEditor = dynamic(
  () => import("./python-editor").then((module) => module.PythonEditor),
  {
    ssr: false,
    loading: () => (
      <div className="python-editor-loading">Loading Python editor...</div>
    ),
  },
);
export function PythonPlayground({
  templates,
  initialCode,
  sourceTitle,
  sourceHref,
}: {
  templates: Record<string, string>;
  initialCode?: string;
  sourceTitle?: string;
  sourceHref?: string;
}) {
  const [code, setCode] = useState(
    initialCode ?? templates.bubble_sort ?? 'print("Hello")',
  );
  const [template, setTemplate] = useState(
    initialCode ? "loaded" : "bubble_sort",
  );
  const [output, setOutput] = useState("Run the code to see its output.");
  const [status, setStatus] = useState("Ready");
  const [elapsed, setElapsed] = useState(0);
  const [ready, setReady] = useState(false);
  const [cursor, setCursor] = useState({ line: 1, column: 1, lines: 1 });
  const worker = useRef<Worker | null>(null);
  const timeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => {
    if (!initialCode) {
      try {
        const draft = localStorage.getItem("interview-atlas.playground.v1");
        if (draft) {
          setCode(draft);
          setTemplate("draft");
        }
      } catch {
        /* Use the selected template. */
      }
    }
    setReady(true);
    return () => {
      worker.current?.terminate();
      if (timeout.current) clearTimeout(timeout.current);
    };
  }, [initialCode]);
  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem("interview-atlas.playground.v1", code);
    } catch {
      /* Keep editing in memory. */
    }
  }, [code, ready]);
  function stop() {
    worker.current?.terminate();
    worker.current = null;
    if (timeout.current) clearTimeout(timeout.current);
    setStatus("Stopped");
    setOutput((p) => (p === "Running..." ? "Stopped by user." : p));
  }
  function run(source = code) {
    worker.current?.terminate();
    if (timeout.current) clearTimeout(timeout.current);
    setStatus("Running");
    setOutput("Running...");
    const start = performance.now();
    const current = new Worker("/python-worker.js");
    worker.current = current;
    current.onmessage = ({ data }) => {
      if (worker.current !== current) return;
      setOutput(data.output);
      setStatus(data.status);
      setElapsed(performance.now() - start);
      if (timeout.current) clearTimeout(timeout.current);
      current.terminate();
      worker.current = null;
    };
    current.onerror = () => {
      setStatus("Error");
      setOutput(
        "The Python worker could not start. Reload the page and try again.",
      );
      if (timeout.current) clearTimeout(timeout.current);
      current.terminate();
      worker.current = null;
    };
    current.postMessage({ code: source });
    timeout.current = setTimeout(() => {
      if (worker.current === current) {
        current.terminate();
        worker.current = null;
        setStatus("Stopped");
        setOutput(
          "Execution stopped after 12 seconds. Check for an infinite loop.",
        );
      }
    }, 12000);
  }
  return (
    <div className="page-container study-page">
      <div className="page-heading">
        <div className="eyebrow">ALGORITHM WORKBENCH</div>
        <h1>Python playground</h1>
        <p>
          Choose a Python template or load code from a study guide, then run it
          and inspect the output. Your draft is saved in this browser.
        </p>
      </div>
      {sourceTitle && (
        <p className="study-data-note">
          Loaded from{" "}
          {sourceHref ? (
            <Link href={sourceHref}>{sourceTitle}</Link>
          ) : (
            sourceTitle
          )}
          . Check the example inputs before running.
        </p>
      )}
      <div className="playground-toolbar">
        <label>
          Template
          <select
            aria-label="Python template"
            value={template}
            onChange={(e) => {
              const key = e.target.value;
              setTemplate(key);
              if (templates[key] !== undefined) setCode(templates[key]);
            }}
          >
            {initialCode && <option value="loaded">Loaded study guide</option>}
            <option value="draft">Your saved draft</option>
            {Object.keys(templates).map((key) => (
              <option key={key} value={key}>
                {key.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </label>
        <button
          className="primary-button"
          disabled={status === "Running"}
          onClick={() => run()}
        >
          Run Python
        </button>
        <button
          className="secondary-button"
          disabled={status !== "Running"}
          onClick={stop}
        >
          Stop
        </button>
        <span role="status">
          {status}
          {elapsed > 0 && status !== "Running"
            ? ` · ${Math.round(elapsed)} ms`
            : ""}
        </span>
      </div>
      <div className="playground-grid">
        <section>
          <h2 className="python-editor-tab">
            <span>practice.py</span>
            <small>Python</small>
          </h2>
          <PythonEditor
            value={code}
            onChange={setCode}
            onRun={(source) => {
              if (status !== "Running") run(source);
            }}
            onCursor={setCursor}
          />
          <div className="python-editor-status">
            <span>
              Ln {cursor.line}, Col {cursor.column}
            </span>
            <span>{cursor.lines} lines · Spaces: 4 · UTF-8</span>
          </div>
        </section>
        <section>
          <h2>Output</h2>
          <pre
            className="python-output"
            aria-label="Python output"
            aria-live="polite"
          >
            {output}
          </pre>
        </section>
      </div>
      <p className="study-data-note" id="python-editor-help">
        The bundled runtime supports algorithm practice and a subset of Python
        standard-library modules. NumPy, PyTorch, and filesystem-based scripts
        need your local Python environment. Code runs in this browser and is not
        sent to a server. Use Ctrl+Enter or Command+Enter to run. Tab and
        Shift+Tab indent or outdent; Escape then Tab moves focus out of the
        editor.
      </p>
    </div>
  );
}
