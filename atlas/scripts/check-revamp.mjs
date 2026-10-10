import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";
import ts from "typescript";

const source = readFileSync(new URL("../app/atlas-navigation.ts", import.meta.url), "utf8");
const compiled = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS } }).outputText;
const exports = {};
vm.runInNewContext(compiled, { exports });
const { atlasModes, entryHash, parseAtlasHash } = exports;
const { entries } = JSON.parse(readFileSync(new URL("../app/atlas-data.json", import.meta.url), "utf8"));
assert.equal(entries.length, 61);
assert.equal(atlasModes.length, 8);

let roundtrips = 0;
for (const { id } of entries) for (const mode of atlasModes) {
  const hash = entryHash(id, mode);
  const route = parseAtlasHash(hash);
  assert.ok(route, `${hash} must parse`);
  assert.equal(route.entryId, id, `${hash} must retain its entry`);
  assert.equal(route.mode, mode, `${hash} must retain its mode`);
  assert.equal(route.workbench, null);
  roundtrips++;
}

for (const { id } of entries) {
  const route = parseAtlasHash(`#entry-${id}/scroll/photo`);
  assert.equal(route?.entryId, id);
  assert.equal(route?.mode, "scroll", "The manuscript photograph stays in the reader, not place photos");
}
assert.equal(parseAtlasHash("#scroll/photo")?.mode, "scroll");
for (const [alias, mode] of Object.entries({ "2d": "2d", "3d": "3d", scroll: "scroll", photo: "ground", ground: "ground", scene: "scene", landscape: "landscape", dossier: "dossier", history: "history" })) {
  const route = parseAtlasHash(`#${alias}`);
  assert.equal(route?.entryId, null, `Bare #${alias} keeps the selected entry`);
  assert.equal(route?.mode, mode);
  assert.equal(parseAtlasHash(`#entry-12a/${alias}`)?.mode, mode);
}
assert.equal(parseAtlasHash("#workbench")?.workbench, "relationships");
for (const id of ["relationships", "inventory", "states", "coverage", "decisions"]) {
  const route = parseAtlasHash(`#workbench/${id}`);
  assert.equal(route?.workbench, id);
  assert.equal(route?.entryId, null);
  assert.equal(route?.mode, null);
}

const invalid = [
  "", "#", "entry-31/scroll", "##scroll", "#unknown", "#__proto__", "#constructor", "#toString", "#entry-", "#entry-0", "#entry-61", "#entry-00", "#entry-03", "#entry-1a", "#entry-12A", "#entry-a",
  "#entry-31scroll", "#entry-31/", "#entry-31/unknown", "#entry-31//scroll", "#entry-31/scroll/", "#entry-31/scroll/photo/extra",
  "#entry-31/history/photo", "#entry-31/dossier/photo", "#entry-31/photo/photo", "#entry-31/scene/photo", "#entry-31/scroll/scene",
  "#history/photo", "#photo/photo", "#scroll/photo/photo", "#scroll?entry=31", "#workbench/unknown", "#workbench/coverage/extra", "#entry-31/workbench",
];
for (const hash of invalid) assert.equal(parseAtlasHash(hash), null, `Malformed route ${JSON.stringify(hash)} must not change entry or view`);

console.log(`Navigation checks passed: ${roundtrips} entry/mode roundtrips, 61 manuscript-photo routes, legacy aliases, five workbench views and ${invalid.length} invalid routes.`);
