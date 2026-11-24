import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
import {createRequire} from 'node:module';
import vm from 'node:vm';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';

const app = new URL('../app/',import.meta.url);
const base = '/CopperScroll/atlas-site/';
const require = createRequire(import.meta.url);
function load(file,dependencies={}) {
  const source=readFileSync(new URL(file,app),'utf8');
  const code=ts.transpileModule(source,{compilerOptions:{esModuleInterop:true,jsx:ts.JsxEmit.ReactJSX,module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText;
  const exports={};
  const localRequire=name=>{
    if (name.endsWith('.css')) return {};
    if (name.endsWith('.json')) return JSON.parse(readFileSync(new URL(name,app),'utf8'));
    return dependencies[name]??require(name);
  };
  vm.runInNewContext(code.replaceAll('import.meta', '({env:{BASE_URL:'+JSON.stringify(base)+'}})'),{exports,require:localRequire});
  return exports;
}
const plans=load('atlas-geographic-plans.ts');
const imagery=load('atlas-archive-imagery.ts');
const ui=load('atlas-research-layers.tsx',{'./atlas-geographic-plans':plans,'./atlas-archive-imagery':imagery});
const {geographicPlans,geographicResearchFeatures}=plans;
const ids=new Set();
function checkId(id){assert(!ids.has(id),id);ids.add(id);}
function checkPoint([x,y]){assert(Number.isFinite(x)&&x>30&&x<40&&Number.isFinite(y)&&y>28&&y<35);}
function checkImage(path){
  const url=new URL('../public/'+path,import.meta.url);
  assert(existsSync(url),'Missing image '+path);
  assert(readFileSync(url).length>128,'Empty image '+path);
}
for(const sheet of geographicPlans){
  checkId(sheet.id);checkImage(sheet.image);assert.equal(sheet.corners.length,4);sheet.corners.forEach(checkPoint);
  assert(sheet.credit&&sheet.sourceUrl&&sheet.detail);
}
for(const layer of imagery.archiveImagery){
  checkId(layer.id);assert(layer.credit&&layer.date&&layer.note);
  if(layer.source.type==='image'){assert(layer.source.url.startsWith(base));checkImage(layer.source.url.slice(base.length));layer.source.coordinates.forEach(checkPoint);}
  else assert(layer.source.tiles[0].startsWith('https://'));
}
for(const feature of geographicResearchFeatures.features){
  checkId(feature.properties.id);assert(feature.properties.status&&feature.properties.detail&&feature.properties.sourceUrl);
  const g=feature.geometry;
  (g.type==='Point'?[g.coordinates]:g.type==='Polygon'?g.coordinates.flat():g.coordinates).forEach(checkPoint);
}
const html=renderToStaticMarkup(React.createElement(ui.default,{map:null,visible:true,site:'jericho_palaces',plan:'jericho-stage-6',setPlan(){},open(){},close(){},onSummary(){}}));
for(const label of ['Selected site','Stage 6','Imagery','Plan opacity','Fit plan','CORONA','HEXAGON','RAF','GeoMOLG','Mapped research observations'])
  assert(html.toLowerCase().includes(label.toLowerCase()),label);
console.log(geographicPlans.length+' plan overlays, '+imagery.archiveImagery.length+' imagery layers and '+geographicResearchFeatures.features.length+' research geometries passed.');
