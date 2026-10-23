"use client";
import { useId, useState } from "react";
import { ChevronRight, Play, RotateCcw } from "lucide-react";
import type { Topic } from "@/lib/content";

export function Architecture({
  topic,
  compact = false,
}: {
  topic: Topic;
  compact?: boolean;
}) {
  const [selected, setSelected] = useState(0);
  const [ascii, setAscii] = useState(false);
  const id = useId().replaceAll(":", "");
  const steps = topic.steps;
  const svgHeight = 90 + steps.length * 95;
  return (
    <div className={`architecture ${compact ? "compact" : ""}`}>
      <div className="diagram-toolbar">
        <span>
          <span className="online-dot" /> EXECUTION GRAPH
        </span>
        <div>
          <button aria-pressed={!ascii} onClick={() => setAscii(false)}>
            Visual
          </button>
          <button aria-pressed={ascii} onClick={() => setAscii(true)}>
            ASCII
          </button>
        </div>
        <span className="diagram-hint">Select a stage to inspect</span>
      </div>
      <div className="diagram-mobile-hint">
        Scroll the diagram horizontally to inspect the shapes.
      </div>
      {ascii ? (
        <pre className="ascii-diagram">
          {steps
            .map(
              (s, i) =>
                `${i ? "          |\n          v\n" : ""}[${String(i + 1).padStart(2, "0")}] ${s.operation}\n     ${s.input}\n     -> ${s.output}`,
            )
            .join("\n")}
        </pre>
      ) : (
        <div className="diagram-canvas">
          {topic.slug === "transformer-architectures" && !topic.explanations ? (
            <svg
              viewBox="0 0 850 330"
              role="img"
              aria-label="Attention tensor flow with parallel query, key, and value projections"
            >
              <defs>
                <marker
                  id={id}
                  markerWidth="8"
                  markerHeight="8"
                  refX="6"
                  refY="3"
                  orient="auto"
                >
                  <path d="M0,0 L6,3 L0,6" fill="var(--diagram-line)" />
                </marker>
              </defs>
              <g
                stroke="var(--diagram-line)"
                fill="none"
                markerEnd={`url(#${id})`}
              >
                <path d="M95 160 H155 V65 H211" />
                <path d="M95 160 H211" />
                <path d="M95 160 H155 V255 H211" />
                <path d="M331 65 H370 V132 H403" />
                <path d="M331 160 H403" />
                <path d="M331 255 H604 V204 H645" />
                <path d="M547 147 H580 V147 H645" />
              </g>
              <rect
                className="svg-input"
                x="15"
                y="126"
                width="100"
                height="68"
                rx="8"
              />
              <text x="65" y="151">
                Input X
              </text>
              <text className="tensor-label" x="65" y="176">
                [B,S,D]
              </text>
              {[
                ["Query / Wq", "Q [B,H,S,dh]", 35],
                ["Key / Wk", "K [B,H,S,dh]", 130],
                ["Value / Wv", "V [B,H,S,dh]", 225],
              ].map(([title, shape, y]) => (
                <g
                  key={title}
                  className={`svg-node ${selected === 0 ? "selected" : ""}`}
                >
                  <rect x="211" y={Number(y)} width="130" height="60" rx="8" />
                  <text x="276" y={Number(y) + 24}>
                    {title}
                  </text>
                  <text className="tensor-label" x="276" y={Number(y) + 45}>
                    {shape}
                  </text>
                </g>
              ))}
              <g className={`svg-node ${selected === 2 ? "selected" : ""}`}>
                <rect x="403" y="112" width="145" height="72" rx="8" />
                <text x="475" y="137">
                  QKᵀ / √dh + mask
                </text>
                <text className="tensor-label" x="475" y="162">
                  [B,H,S,S]
                </text>
              </g>
              <g className={`svg-node ${selected === 3 ? "selected" : ""}`}>
                <rect x="645" y="112" width="178" height="118" rx="8" />
                <text x="734" y="139">
                  Softmax → multiply V
                </text>
                <text className="tensor-label" x="734" y="163">
                  [B,H,S,dh]
                </text>
                <line
                  x1="664"
                  x2="804"
                  y1="176"
                  y2="176"
                  stroke="var(--diagram-line)"
                />
                <text x="734" y="196">
                  Merge heads + Wo
                </text>
                <text className="tensor-label" x="734" y="216">
                  Output [B,S,D]
                </text>
              </g>
              <text className="svg-caption" x="425" y="315">
                SELF-ATTENTION · D = H × dh · residual + FFN preserve [B,S,D]
              </text>
            </svg>
          ) : (
            <svg
              viewBox={`0 0 800 ${svgHeight}`}
              role="img"
              aria-label={`${topic.title}: inputs, operations, and output shapes`}
            >
              <defs>
                <marker
                  id={id}
                  markerWidth="8"
                  markerHeight="8"
                  refX="6"
                  refY="3"
                  orient="auto"
                >
                  <path d="M0,0 L6,3 L0,6" fill="var(--diagram-line)" />
                </marker>
              </defs>
              {steps.map((s, i) => (
                <g key={s.operation}>
                  {i > 0 && (
                    <path
                      d={`M400 ${i * 95 - 3} V${i * 95 + 17}`}
                      stroke="var(--diagram-line)"
                      markerEnd={`url(#${id})`}
                    />
                  )}
                  <text className="svg-step-number" x="88" y={i * 95 + 60}>
                    {String(i + 1).padStart(2, "0")}
                  </text>
                  <g className={`svg-node ${selected === i ? "selected" : ""}`}>
                    <rect
                      x="145"
                      y={i * 95 + 20}
                      width="510"
                      height="70"
                      rx="9"
                    />
                    <text x="400" y={i * 95 + 47}>
                      {s.operation}
                    </text>
                    <text className="tensor-label" x="400" y={i * 95 + 71}>
                      {s.output}
                    </text>
                  </g>
                </g>
              ))}
              <text className="svg-caption" x="400" y={svgHeight - 28}>
                INPUT: {steps[0].input}
              </text>
            </svg>
          )}
        </div>
      )}
      <div className="stage-tabs" aria-label="Execution stages">
        {steps.map((s, i) => (
          <button
            key={s.operation}
            aria-pressed={selected === i}
            onClick={() => setSelected(i)}
          >
            <span>{String(i + 1).padStart(2, "0")}</span>
            {s.operation}
            <ChevronRight size={13} />
          </button>
        ))}
      </div>
      <div className="stage-inspector" aria-live="polite">
        <span className="mono accent">
          STAGE {String(selected + 1).padStart(2, "0")}
        </span>
        <strong>{steps[selected].operation}</strong>
        <code>
          {steps[selected].input} → {steps[selected].output}
        </code>
        <p>{steps[selected].note}</p>
      </div>
      {!compact && (
        <div className="trace-controls">
          <button onClick={() => setSelected((selected + 1) % steps.length)}>
            <Play size={13} /> Next stage
          </button>
          <button onClick={() => setSelected(0)}>
            <RotateCcw size={13} /> Reset
          </button>
          <span>
            Operations are illustrative; code runs in your Python environment.
          </span>
        </div>
      )}
    </div>
  );
}
