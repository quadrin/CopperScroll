import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import ts from 'typescript';
import * as React from 'react';
import * as jsx from 'react/jsx-runtime';
import { renderToStaticMarkup } from 'react-dom/server';

async function module(path, deps) {
  const exports = {};
  const code = ts.transpileModule(await readFile(new URL(path, import.meta.url), 'utf8'), {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX },
  }).outputText;
  new Function('exports', 'require', code)(exports, name => {
    assert(name in deps, `Missing test dependency: ${name}`);
    return deps[name];
  });
  return exports;
}

const measure = await module('../app/atlas-walk-measure.ts', {});
const { default: Card } = await module('../app/atlas-walk-measure-card.tsx', {
  react: React, 'react/jsx-runtime': jsx, './atlas-walk-measure': measure, './atlas-walk-tools.css': {},
});
const props = { points: [[0, 0, 0], [3, 12, 4]], style: 'smooth', onClear() {} };
const physical = renderToStaticMarkup(React.createElement(Card, { ...props, units: 'metres' }));
assert(physical.includes('5.00 m'));
assert(physical.includes('13.00 m'));
assert(physical.includes('10.0 cubits'));
assert(physical.includes('26.0 cubits'));
assert(!physical.includes('disabled=""'));
for (const units of ['relative', null]) {
  const unscaled = renderToStaticMarkup(React.createElement(Card, { ...props, units }));
  assert(unscaled.includes('5.00 model units'));
  assert(unscaled.includes('13.00 model units'));
  assert(!/\d\.\d cubits/.test(unscaled), 'Unscaled model cannot produce numeric cubit conversions');
  assert(!unscaled.includes('5.00 m</span>'));
  assert(unscaled.includes('disabled=""'), 'Keep the cubit selector visible but unavailable');
  assert(unscaled.includes('aria-describedby="measure-scale-limit"'));
}
const map = await readFile(new URL('../app/atlas-map.tsx', import.meta.url), 'utf8');
assert(map.includes('setSiteUnits(runtime.model.units)'));
assert(map.includes('units={siteUnits}'));
console.log('Measurement unit checks passed: calibrated lengths convert to cubits; relative and unknown scales stay in model units.');
