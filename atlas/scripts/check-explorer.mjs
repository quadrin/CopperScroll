import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import ts from 'typescript';
function module(path, deps={}) { const exports={};const code=ts.transpileModule(readFileSync(new URL(path,import.meta.url),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText;vm.runInNewContext(code,{exports,URLSearchParams,require:n=>deps[n]});return exports; }
const nav=module('../app/atlas-navigation.ts');
const contextRoutes=module('../app/atlas-context-routes.ts');
const plans=JSON.parse(readFileSync(new URL('../app/atlas-site-plans.json',import.meta.url),'utf8'));
const {entries,places}=JSON.parse(readFileSync(new URL('../app/atlas-data.json',import.meta.url),'utf8'));
const model=module('../app/atlas-explorer-model.ts',{'./atlas-navigation':nav,'./atlas-site-plans.json':plans,'./atlas-data.json':{entries,places},'./atlas-context-routes':contextRoutes});
const primary=id=>entries.find(e=>e.id===id)?.candidates[0]?.placeId??null;
assert.equal(new Set(plans.map(p=>p.id)).size,plans.length);
let roundtrips=0;
for(const p of plans){
 assert.ok(p.width>0&&p.height>0&&p.features.length>0);
 assert.match(p.limit,/registr|register|image-coordinate/i,`${p.id}: disclose registration or source frame`);
 for(const id of p.placeIds)assert.ok(places.some(place=>place.id===id),id);
 assert.equal(new Set(p.features.map(f=>f.id)).size,p.features.length);
 for(const f of p.features){
  assert.ok(f.x>=0&&f.x<=p.width&&f.y>=0&&f.y<=p.height,`${p.id}/${f.id} must stay in its source frame`);
  assert.ok(f.description&&f.limit&&f.sources.length&&f.sourceUrl);
  for(const id of f.entryIds)assert.ok(entries.some(e=>e.id===id));
  for(const view of ['plan','photo']){
   const state={...model.initialExplorer,mode:'site',entryId:f.entryIds[0]??entries.find(e=>e.candidates.some(c=>p.placeIds.includes(c.placeId)))?.id??'25',placeId:p.placeIds[0],planId:p.id,featureId:f.id,siteView:view};
   const hash=model.explorerHash(state);const restored=model.explorerFromHash(hash,primary);
   assert.ok(restored,hash);assert.equal(restored.entryId,state.entryId);assert.equal(restored.placeId,state.placeId);assert.equal(restored.featureId,state.featureId);assert.equal(restored.siteView,view);roundtrips++;
  }
 }
 const overview={...model.initialExplorer,mode:'site',planId:p.id,featureId:null,siteView:'photo'};
 assert.equal(model.explorerFromHash(model.explorerHash(overview),primary)?.siteView,'photo');
}
for(const hash of ['#entry-61/site/qumran-ilan','#entry-21/site/unknown','#entry-21/site/qumran-ilan/unknown','#entry-21/site/qumran-ilan/D/photo/extra','#entry-21/site/qumran-ilan//photo'])assert.equal(model.explorerFromHash(hash,primary),null,hash);
assert.equal(model.initialExplorer.mode,'site');
assert.equal(model.initialExplorer.planId,'qumran-ilan');
const generic=model.explorerFromHash('#entry-27/site',primary);
assert.equal(generic?.mode,'site');assert.equal(generic?.placeId,'jericho_area');assert.equal(generic?.planId,null);
assert.equal(model.explorerFromHash('#entry-27',primary)?.mode,'site');
assert.equal(model.explorerHash(generic),'#entry-27/site');
console.log(`Explorer data and routes passed: ${plans.length} source plans, ${roundtrips} feature/view roundtrips, bounded source coordinates, provenance and invalid routes.`);

for(const {id} of entries){
 assert.equal(model.explorerFromHash(nav.entryHash(id,'2d'),primary)?.mode,'2d');
 for(const tool of ['relationships','inventory','states','coverage','decisions']){
  const state={...model.initialExplorer,entryId:id,workbench:tool};
  const restored=model.explorerFromHash(model.explorerHash(state),primary);
  assert.equal(restored.entryId,id);assert.equal(restored.workbench,tool);
 }
}
for(const plan of plans)for(const representation of ['source','model','walk']){
 const state={...model.initialExplorer,entryId:plan.features[0].entryIds[0]??entries.find(e=>e.candidates.some(c=>plan.placeIds.includes(c.placeId)))?.id??'25',mode:'site',planId:plan.id,featureId:plan.features[0].id,representation};
 const restored=model.explorerFromHash(model.explorerHash(state),primary);assert.equal(restored.representation,representation);assert.equal(restored.featureId,state.featureId);
}
for(const hash of ['#workbench/relationships?entry=61','#entry-25/site/abu-saraj-iv17/source/photo'])assert.equal(model.explorerFromHash(hash,primary),null);
console.log('Map, source/model and entry-specific workbench deep links pass.');

// Evidence links retain chosen localities even without a source-plan route.
for(const place of places)for(const mode of ['2d','3d','landscape','dossier','ground','scroll']){
 const state={...model.initialExplorer,entryId:'25',placeId:place.id,mode,planId:null,explicitPlace:true};
 const hash=model.explorerHash(state);const restored=model.explorerFromHash(hash,primary);
 assert.equal(restored?.placeId,place.id,hash);assert.equal(restored?.mode,mode,hash);
 assert.equal(model.explorerHash(restored),hash);
}
for(const hash of ['#entry-25/2d?place=unknown','#entry-25/2d?place=','#entry-25/2d?place=kh_qumran&place=wadi_qumran','#entry-25/2d?place=kh_qumran&extra=1','#entry-25/2d?place=kh_qumran?extra','#entry-25/site/qumran-ilan/source?place=kh_qumran'])assert.equal(model.explorerFromHash(hash,primary),null,hash);
console.log('Evidence/map locality queries: all known localities (including unplaced ones) round-trip; unknown, repeated, malformed and unsupported parameters are rejected.');

for(const view of contextRoutes.inspectionViews)for(const mode of ['2d','scroll']){
 const state={...model.initialExplorer,entryId:'25',mode,planId:null,inspection:view,recordId:'source/inventory-sion-iv17',explicitPlace:true};
 const hash=model.explorerHash(state),restored=model.explorerFromHash(hash,primary);
 assert.equal(restored?.inspection,view);assert.equal(restored?.recordId,state.recordId);assert.equal(restored?.placeId,state.placeId);assert.equal(model.explorerHash(restored),hash);
}
for(const hash of ['#entry-25/2d?inspect=unknown','#entry-25/2d?inspect=record&record=','#entry-25/2d?record=source/test','#entry-25/scroll?inspect=names&inspect=sources'])assert.equal(model.explorerFromHash(hash,primary),null,hash);
assert.equal(contextRoutes.legacyEvidenceTarget('#kb?entry=25&view=case'),'#entry-25/2d?inspect=compare');
assert.equal(contextRoutes.legacyEvidenceTarget('#kb?entry=18&view=names'),'#entry-18/scroll?inspect=names');
const legacy=contextRoutes.legacyEvidenceTarget('#kb?entry=25&record=source/inventory-sion-iv17&detail=1');
assert.equal(model.explorerFromHash(legacy,primary)?.recordId,'source/inventory-sion-iv17');
console.log('Contextual views and canonical record IDs round-trip in Map/Scroll; old Evidence bookmarks redirect without losing records.');
