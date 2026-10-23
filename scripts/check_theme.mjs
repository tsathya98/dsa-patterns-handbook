import assert from "node:assert/strict";
import fs from "node:fs";
const css = fs.readFileSync(
  new URL("../apps/web/styles/tokens.css", import.meta.url),
  "utf8",
);
const themes = { light: {}, dark: {} };
for (const [, mode, body] of css.matchAll(
  /:root(?:\[data-theme="(dark)"\])?\s*\{([^}]+)\}/g,
)) {
  for (const [, key, value] of body.matchAll(/--([\w-]+):\s*([^;]+);/g))
    themes[mode || "light"][key] = value.trim();
}
function luminance(hex) {
  assert.match(hex, /^#[a-f\d]{6}$/i);
  const [r, g, b] = hex
    .slice(1)
    .match(/../g)
    .map((v) => parseInt(v, 16) / 255)
    .map((v) => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function contrast(foreground, background) {
  const a = luminance(foreground),
    b = luminance(background);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}
const report = {};
for (const [name, colors] of Object.entries(themes)) {
  const textMinimum = name === "dark" ? 7 : 4.5;
  const ratios = [];
  for (const background of [
    "bg",
    "surface",
    "panel",
    "accent-soft",
    "control-bg",
  ]) {
    for (const foreground of ["text", "muted", "accent"]) {
      const ratio = contrast(colors[foreground], colors[background]);
      assert.ok(
        ratio >= textMinimum,
        `${name} ${foreground}/${background}: ${ratio.toFixed(2)}`,
      );
      ratios.push(ratio);
    }
  }
  assert.ok(
    contrast(colors["on-accent"], colors.accent) >= 4.5,
    `${name} button text`,
  );
  for (const background of ["bg", "surface", "panel", "control-bg"])
    assert.ok(
      contrast(colors["control-line"], colors[background]) >= 3,
      `${name} control border/${background}`,
    );
  for (const [foreground, background] of [
    ["easy-text", "easy-bg"],
    ["warning-text", "warning-bg"],
    ["hard-text", "hard-bg"],
  ])
    assert.ok(
      contrast(colors[foreground], colors[background]) >= 4.5,
      `${name} ${foreground}`,
    );
  report[name] = Math.min(...ratios).toFixed(2);
}
for (const [name, size] of [
  ["font-xs", ".75"],
  ["font-sm", ".875"],
  ["font-base", "1"],
])
  assert.equal(
    Number(themes.light[name].replace("rem", "")),
    Number(size),
    name,
  );
assert.ok(
  luminance(themes.dark.bg) <= 0.005,
  "Dark canvas should remain near black",
);
console.log(
  `Validated theme text, button, status, and control-border contrast. Lowest main text pair: light ${report.light}:1, dark ${report.dark}:1. Shared type scale: 12/14/16 px at the default root size.`,
);
