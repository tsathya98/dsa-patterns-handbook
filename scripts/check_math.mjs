import fs from "node:fs";
import katex from "katex";
const root = new URL("../content/curriculum/", import.meta.url);
let count = 0;
for (const track of fs
  .readdirSync(root, { withFileTypes: true })
  .filter((x) => x.isDirectory())) {
  const folder = new URL(`${track.name}/`, root);
  for (const name of fs
    .readdirSync(folder)
    .filter((x) => x.endsWith(".json"))) {
    const topic = JSON.parse(fs.readFileSync(new URL(name, folder), "utf8"));
    const equations = [
      ...topic.equations,
      ...(topic.explanations ?? []).flatMap(
        (section) => section.equations ?? [],
      ),
    ];
    for (const equation of equations) {
      katex.renderToString(equation, {
        displayMode: true,
        throwOnError: true,
        trust: false,
      });
      count++;
    }
  }
}
console.log(`Rendered ${count} curriculum equations without errors.`);
