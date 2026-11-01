import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';

const require=createRequire(import.meta.url);
const survey=JSON.parse(readFileSync(new URL('../app/atlas-landscape-cave-survey.json',import.meta.url),'utf8'));
const source=readFileSync(new URL('../app/atlas-landscape.tsx',import.meta.url),'utf8').replace('import.meta.env?.BASE_URL','undefined');
const exports={};
const code=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX,esModuleInterop:true}}).outputText;
vm.runInNewContext(code,{exports,require:name=>{
 if(name.endsWith('.css'))return {};
 if(name==='./atlas-landscape-data')return {};
 if(name.startsWith('./')&&name.endsWith('.json'))return JSON.parse(readFileSync(new URL(`../app/${name.slice(2)}`,import.meta.url),'utf8'));
 return require(name);
}});
for(const comparison of survey.comparisons){
 const record=survey.features.find(f=>f.properties.point===comparison.point).properties;
 const html=renderToStaticMarkup(React.createElement(exports.SurveyPointCard,{record,onClose:()=>{}}));
 assert(html.includes(`Two source positions for ${comparison.siglum}`));
 for(const value of [...comparison.coordinates,comparison.itm_e,comparison.itm_n])assert(html.includes(String(value)));
 assert(html.includes(`<strong>${comparison.offset_m} m</strong>`));
 assert(html.includes('positional accuracy unspecified'));
 assert(html.includes('discrepancy remains unresolved'));
 assert(html.includes('Candidate anchors and confidence are unchanged'));
 assert(html.includes('/research/sources/iaa_gis_2026-10-30/spatial/README.md'));
}
const unmatched=survey.features.find(f=>f.properties.point===19).properties;
const html=renderToStaticMarkup(React.createElement(exports.SurveyPointCard,{record:unmatched,onClose:()=>{}}));
assert(!html.includes('Cave coordinate comparison'),'no inferred alternate point for an unchecked crosswalk');
assert(html.includes('These estimates do not resolve disagreement with another source'));
console.log('Cave coordinates: separate 3Q/1Q source positions, discrepancy distances, original CRS, unknown IAA accuracy and unmatched-point behavior passed.');
