/** Protect the restored catalogs, local document links, and progress import contract. */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import assert from "node:assert/strict";
import ts from "typescript";
const root = new URL("../", import.meta.url);
const catalog = JSON.parse(
  fs.readFileSync(new URL("content/indexes/study-catalog.json", root), "utf8"),
);
assert.equal(catalog.problems.length, 237);
for (const [field, count] of [
  ["in75", 75],
  ["in150", 150],
  ["inHW", 30],
])
  assert.equal(catalog.problems.filter((p) => p[field]).length, count, field);
assert.equal(
  new Set(catalog.problems.map((p) => p.number)).size,
  catalog.problems.length,
);
assert.equal(catalog.companyProfiles.length, 62);
assert.equal(catalog.notes.filter((n) => n.docType === "company").length, 561);
assert.equal(
  catalog.notes.filter((n) => n.docType === "system_design").length,
  21,
);
for (const note of catalog.notes)
  assert.ok(
    fs.existsSync(new URL("content/" + note.id + ".md", root)),
    note.id,
  );
for (const p of catalog.problems) {
  if (p.documentId)
    assert.ok(
      fs.existsSync(new URL("content/" + p.documentId + ".md", root)),
      p.title,
    );
}
const templates = JSON.parse(
  fs.readFileSync(
    new URL("content/indexes/playground-templates.json", root),
    "utf8",
  ),
);
assert.equal(Object.keys(templates).length, 18);
const original = fs
  .readFileSync(new URL("generated/legacy/viewer.html", root), "utf8")
  .match(/const PLAYGROUND_TEMPLATES = (\{[\s\S]*?\n    \});/)[1];
assert.equal(
  JSON.stringify(templates),
  JSON.stringify(
    vm.runInNewContext("(" + original + ")", {}, { timeout: 1000 }),
  ),
);
for (const file of ["skulpt.min.js", "skulpt-stdlib.js"])
  assert.equal(
    fs.readFileSync(new URL("apps/web/public/runtime/" + file, root), "utf8"),
    fs.readFileSync(
      new URL("generated/legacy/static/vendor/" + file, root),
      "utf8",
    ),
  );
const compiled = ts.transpileModule(
  fs.readFileSync(new URL("apps/web/lib/study-progress.ts", root), "utf8"),
  {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2022,
    },
  },
).outputText;
const exports = {};
vm.runInNewContext(compiled, { exports }, { timeout: 1000 });
const { cleanStudyData, studyStorageKeys } = exports;
assert.equal(studyStorageKeys.problemStatus, "dsa_hub_prob_status_v3");
assert.equal(studyStorageKeys.documentStatus, "dsa_hub_status_v2");
assert.equal(studyStorageKeys.notes, "dsa_hub_notes_v2");
const restored = cleanStudyData({
  problemStatus: { "lc-88": "review", "lc-1": "solved", "lc-2": "invalid" },
  documentStatus: { "old/path.md": "solved" },
  notes: { "old/path.md": "remember the invariant", bad: 17 },
  customProblems: [
    {
      number: 9999,
      title: "Custom exercise",
      pattern: "Two pointers",
      difficulty: "Medium",
    },
  ],
  pomodoroHistory: [
    {
      id: "old-session",
      title: "Arrays",
      minutes: 25,
      mode: "Focus",
      time: "10:00",
    },
  ],
});
assert.equal(restored.problemStatus["lc-88"], "review");
assert.equal(restored.problemStatus["lc-1"], "solved");
assert.equal(restored.problemStatus["lc-2"], undefined);
assert.equal(restored.documentStatus["old/path.md"], "solved");
assert.equal(restored.notes["old/path.md"], "remember the invariant");
assert.equal(restored.notes.bad, undefined);
assert.equal(restored.customProblems[0].topic, "Two pointers");
assert.equal(restored.pomodoroHistory[0].minutes, 25);
for (const invalid of [
  null,
  false,
  [],
  { customProblems: [{ number: -1, title: "bad", topic: "x" }] },
  { problemStatus: "bad" },
])
  assert.ok(cleanStudyData(invalid));
console.log(
  "Validated 237 problems (75/150/30 lists), 561 banks, 62 profiles, 710 document links, 18 templates, and original progress compatibility.",
);
