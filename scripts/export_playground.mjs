/** Export the existing repository templates for the Next.js playground. */
import fs from "node:fs";
import vm from "node:vm";
const html = fs.readFileSync(
  new URL("../generated/legacy/viewer.html", import.meta.url),
  "utf8",
);
const match = html.match(/const PLAYGROUND_TEMPLATES = (\{[\s\S]*?\n    \});/);
if (!match) throw new Error("Original playground templates were not found");
const templates = vm.runInNewContext(`(${match[1]})`, Object.create(null), {
  timeout: 1000,
});
fs.writeFileSync(
  new URL("../content/indexes/playground-templates.json", import.meta.url),
  JSON.stringify(templates, null, 2) + "\n",
);
for (const file of ["skulpt.min.js", "skulpt-stdlib.js"]) {
  fs.copyFileSync(
    new URL(`../generated/legacy/static/vendor/${file}`, import.meta.url),
    new URL(`../apps/web/public/runtime/${file}`, import.meta.url),
  );
}
console.log(
  `Exported ${Object.keys(templates).length} original Python templates and bundled runtime.`,
);
