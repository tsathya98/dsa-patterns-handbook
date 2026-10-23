/** Run every original template through the same worker entry point as the browser. */
import fs from "node:fs";
import vm from "node:vm";
import assert from "node:assert/strict";
const root = new URL("../", import.meta.url);
const templates = JSON.parse(
  fs.readFileSync(
    new URL("content/indexes/playground-templates.json", root),
    "utf8",
  ),
);
for (const [name, code] of Object.entries(templates)) {
  let result;
  const scope = { setTimeout, clearTimeout, console, TextDecoder, TextEncoder };
  const context = vm.createContext(scope);
  scope.self = scope;
  scope.postMessage = (message) => {
    result = message;
  };
  scope.importScripts = (...files) =>
    files.forEach((file) =>
      vm.runInContext(
        fs.readFileSync(new URL("apps/web/public" + file, root), "utf8"),
        context,
      ),
    );
  vm.runInContext(
    fs.readFileSync(new URL("apps/web/public/python-worker.js", root), "utf8"),
    context,
  );
  await scope.onmessage({ data: { code } });
  assert.equal(result?.status, "Completed", `${name}: ${result?.output}`);
}
console.log(
  `Executed ${Object.keys(templates).length} original Python templates through the playground worker.`,
);
