// Render every saved selector choice without starting a browser or preview server.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import ts from "typescript";

const file = new URL("../app/atlas-workbench.tsx", import.meta.url);
const requireFromApp = createRequire(file);
const source = readFileSync(file, "utf8") + "\nexport { Relationships, Inventory, HistoricalStates, Coverage, Decisions };\n";
const compiled = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, esModuleInterop: true } }).outputText;
const module = { exports: {} };
const localRequire = id => id.endsWith(".css") ? {} : requireFromApp(id);
new Function("require", "module", "exports", compiled)(localRequire, module, module.exports);
const components = module.exports;
const snapshot = JSON.parse(readFileSync(new URL("../app/atlas-workbench.json", import.meta.url), "utf8"));
const escaped = value => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#x27;");
const first = (records, id) => [records.find(record => record.id === id), ...records.filter(record => record.id !== id)];
const render = (component, props) => renderToStaticMarkup(createElement(component, props));
let choices = 0;

for (const item of snapshot.modules) {
  const html = render(components.default, { moduleId: item.id, onModule() {}, onClose() {} });
  assert.ok(html.includes(escaped(item.title)), `${item.id}: module heading did not render`);
  assert.ok(html.includes('id="research-workbench"'));
  if (item.id === "relationships") {
    for (const branch of item.data.branches) {
      const candidate = { ...item, data: { ...item.data, readings: first(item.data.readings, branch.reading_id), windows: first(item.data.windows, branch.window_id), assignments: first(item.data.assignments, branch.assignment_id) } };
      const html = render(components.Relationships, { module: candidate });
      const result = item.results.find(result => result.id === branch.result_id);
      assert.ok(html.includes(escaped(result.title)), `${branch.id}: selected branch result did not render`);
      for (const check of result.checks) assert.ok(html.includes(escaped(check.label)));
      choices++;
    }
  }
  if (item.id === "inventory") {
    for (const query of item.data.queries) for (const branch of query.branches) {
      const saved = { ...query, branches: first(query.branches, branch.id) };
      const candidate = { ...item, data: { ...item.data, queries: [saved, ...item.data.queries.filter(record => record.id !== query.id)] } };
      const html = render(components.Inventory, { module: candidate });
      for (const cave of item.data.catalog) assert.ok(html.includes(escaped(cave.name)), `${branch.id}: missing control ${cave.id}`);
      for (const control of query.candidate_results) for (const check of control.branches.find(result => result.branch_id === branch.id).checks) assert.ok(html.includes(escaped(check.detail)), `${branch.id}: selected check detail missing`);
      assert.ok(html.includes("true/grid/magnetic convention unspecified"));
      if (branch.depth_metres !== undefined) assert.ok(html.includes(" m. Ancient origin and datum"));
      choices++;
    }
  }
  if (item.id === "states") for (const view of item.data.views) {
    const candidate = { ...item, data: { ...item.data, views: first(item.data.views, view.id) } };
    const html = render(components.HistoricalStates, { module: candidate });
    for (const resultId of view.query_ids) assert.ok(html.includes(escaped(item.results.find(result => result.id === resultId).title)));
    if (view.native_shapes.length) assert.ok(html.includes("source-crop pixels"));
    choices++;
  }
  if (item.id === "coverage") for (const target of item.data.targets) {
    const candidate = { ...item, data: { ...item.data, targets: first(item.data.targets, target.id) } };
    const html = render(components.Coverage, { module: candidate });
    assert.ok(html.includes(escaped(target.label)));
    for (const gate of target.gates) assert.ok(html.includes(escaped(gate.detail)));
    choices++;
  }
  if (item.id === "decisions") for (const task of item.data.tasks) {
    const candidate = { ...item, data: { ...item.data, tasks: first(item.data.tasks, task.id) } };
    const html = render(components.Decisions, { module: candidate });
    assert.ok(html.includes(escaped(task.current_evidence.detail)));
    for (const outcome of task.outcomes) assert.ok(html.includes(escaped(outcome.label)));
    assert.ok(html.includes("Choose a hypothetical outcome"));
    choices++;
  }
}
console.log(`Rendered five modules and ${choices} saved selector choices; controls, provenance qualifiers and planning labels passed.`);
