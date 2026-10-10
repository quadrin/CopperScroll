import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import ts from "typescript";

// Exercise the actual model against the published text/photo registration.
const source = fs.readFileSync(new URL("./atlas-reader-model.ts", import.meta.url), "utf8");
const photo = JSON.parse(fs.readFileSync(new URL("./atlas-photo-data.json", import.meta.url), "utf8"));
const text = JSON.parse(fs.readFileSync(new URL("./atlas-text.json", import.meta.url), "utf8"));
const output = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, esModuleInterop: true } }).outputText;
const sandboxModule = { exports: {} };
vm.runInNewContext(output, { module: sandboxModule, exports: sandboxModule.exports, require: path => {
  assert.equal(path, "./atlas-photo-data.json");
  return photo;
} });
const { photoTarget, mappedWordsForEntry, wordOwner, isPhotographHash } = sandboxModule.exports;

assert.equal(isPhotographHash("#entry-31/scroll/photo"), true);
assert.equal(isPhotographHash("#scroll/photo"), true);
assert.equal(isPhotographHash("#entry-31/scroll"), false);
assert.equal(isPhotographHash("#entry-31/photo"), false, "Place photographs are a different atlas view");
assert.equal(isPhotographHash("#entry-31/history/photo"), false);

assert.equal(photoTarget(text, "21").entryId, "30", "Column V must not remain selected over column VII imagery");
assert.equal(photoTarget(text, "21").line, "VII 8");
assert.equal(photoTarget(text, "31").entryId, "31");
assert.equal(photoTarget(text, "31").line, "VII 11");
assert.equal(mappedWordsForEntry(text, "29").length, 1);
assert.equal(mappedWordsForEntry(text, "30").length, 5);
assert.equal(mappedWordsForEntry(text, "31").length, 2);
for (const entryId of Object.keys(text.entries)) {
  const target = photoTarget(text, entryId);
  const word = photo.words[target.index];
  assert.equal(wordOwner(text, word.line, word.word), target.entryId, `Photograph target must belong to its selected entry (${entryId})`);
  if (!mappedWordsForEntry(text, entryId).length) assert.equal(target.entryId, "30");
}
const shared = { entries: { a: [{ ref: "I 1", from: 0, to: 2 }], b: [{ ref: "I 1", from: 2, to: 4 }] } };
assert.equal(wordOwner(shared, "I 1", 1), "a");
assert.equal(wordOwner(shared, "I 1", 2), "b", "Shared-line ownership respects entry boundaries");
assert.equal(wordOwner(shared, "I 1", 4), undefined);
console.log("Reader context checks passed: all entries resolve to a registered photograph word and owner.");
