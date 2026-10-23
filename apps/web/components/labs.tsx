"use client";
import { useState } from "react";
export function Lab({ kind }: { kind: string }) {
  const [tokens, setTokens] = useState(8192);
  const [batch, setBatch] = useState(1);
  const [heads, setHeads] = useState(8);
  const [position, setPosition] = useState(3);
  const [causal, setCausal] = useState(true);
  const [stride, setStride] = useState(1);
  if (kind === "kv")
    return (
      <div className="lab">
        <div className="eyebrow">MEMORY WORKBENCH</div>
        <h3>What fits in the cache?</h3>
        <div className="lab-grid">
          <label>
            Context tokens <output>{tokens.toLocaleString()}</output>
            <input
              aria-label="Context tokens"
              type="range"
              min="1024"
              max="131072"
              step="1024"
              value={tokens}
              onChange={(e) => setTokens(+e.target.value)}
            />
          </label>
          <label>
            Active sequences <output>{batch}</output>
            <input
              aria-label="Active sequences"
              type="range"
              min="1"
              max="32"
              value={batch}
              onChange={(e) => setBatch(+e.target.value)}
            />
          </label>
          <label>
            KV heads
            <select
              aria-label="KV heads"
              value={heads}
              onChange={(e) => setHeads(+e.target.value)}
            >
              <option value="1">1: MQA</option>
              <option value="8">8: GQA</option>
              <option value="32">32: MHA</option>
            </select>
          </label>
          <div className="lab-result">
            <strong>
              {((2 * batch * tokens * 32 * heads * 128 * 2) / 2 ** 30).toFixed(
                2,
              )}
              <small>GiB</small>
            </strong>
            <span>KV tensors only</span>
          </div>
        </div>
        <p>
          Fixed: 32 layers, head dimension 128, BF16 (2 bytes). Weights,
          workspace, and paging overhead are excluded.
        </p>
      </div>
    );
  if (kind === "attention")
    return (
      <div className="lab">
        <div className="eyebrow">MASK WORKBENCH</div>
        <h3>Which tokens can see each other?</h3>
        <div className="mask-controls">
          <button aria-pressed={causal} onClick={() => setCausal(true)}>
            Causal
          </button>
          <button aria-pressed={!causal} onClick={() => setCausal(false)}>
            Bidirectional
          </button>
        </div>
        <div
          className="mask-grid"
          aria-label={`${causal ? "Causal triangular" : "Bidirectional full"} attention mask`}
        >
          {Array.from({ length: 36 }, (_, i) => {
            const row = Math.floor(i / 6),
              col = i % 6;
            return (
              <span
                key={i}
                className={!causal || col <= row ? "allowed" : "blocked"}
                title={`Query ${row + 1}, key ${col + 1}: ${!causal || col <= row ? "allowed" : "blocked"}`}
              >
                {!causal || col <= row ? "0" : "-∞"}
              </span>
            );
          })}
        </div>
        <p>
          Rows: query positions. Columns: key positions. Add 0 for allowed
          logits and negative infinity for masked logits before softmax. Padding
          still needs its own mask.
        </p>
      </div>
    );
  if (kind === "rope") {
    const angle = position * 0.35;
    return (
      <div className="lab">
        <div className="eyebrow">ROTATION WORKBENCH</div>
        <h3>One coordinate pair, rotated through position.</h3>
        <label>
          Position m <output>{position}</output>
          <input
            aria-label="Position"
            type="range"
            min="0"
            max="18"
            value={position}
            onChange={(e) => setPosition(+e.target.value)}
          />
        </label>
        <svg
          className="rotation-plane"
          viewBox="0 0 400 230"
          aria-label="Two-dimensional RoPE rotation"
        >
          <circle
            cx="200"
            cy="115"
            r="82"
            fill="none"
            stroke="var(--diagram-line)"
          />
          <path d="M80 115 H320 M200 15 V215" stroke="var(--diagram-line)" />
          <path
            d="M200 115 H282"
            stroke="var(--diagram-line)"
            strokeWidth="2"
          />
          <path
            d={`M200 115 L${200 + 82 * Math.cos(angle)} ${115 - 82 * Math.sin(angle)}`}
            stroke="var(--accent)"
            strokeWidth="3"
          />
          <circle
            cx={200 + 82 * Math.cos(angle)}
            cy={115 - 82 * Math.sin(angle)}
            r="5"
            fill="var(--accent)"
          />
          <text x="30" y="30" fill="var(--muted)">
            θ = 0.35 radians
          </text>
          <text x="30" y="220" fill="var(--accent)">
            R_m(1,0) = ({Math.cos(angle).toFixed(3)},{" "}
            {Math.sin(angle).toFixed(3)})
          </text>
        </svg>
        <p>
          Rotation preserves vector norm. For a shared frequency, the query-key
          dot product depends on the difference between their positions.
        </p>
      </div>
    );
  }
  if (kind === "convolution")
    return (
      <div className="lab">
        <div className="eyebrow">SPATIAL WORKBENCH</div>
        <h3>Trace the output resolution.</h3>
        <label>
          Stride <output>{stride}</output>
          <input
            aria-label="Stride"
            type="range"
            min="1"
            max="4"
            value={stride}
            onChange={(e) => setStride(+e.target.value)}
          />
        </label>
        <div className="dimension-flow">
          <code>[B,3,224,224]</code>
          <span>3x3 kernel, padding 1 →</span>
          <code>
            [B,64,{Math.floor(223 / stride) + 1},{Math.floor(223 / stride) + 1}]
          </code>
        </div>
        <p>
          Dilation 1. Each output axis is floor((224 + 2 - 3) / stride) + 1.
        </p>
      </div>
    );
  return null;
}
