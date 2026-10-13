import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import ts from 'typescript';
function module(path, deps={}) { const exports={};const code=ts.transpileModule(readFileSync(new URL(path,import.meta.url),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText;vm.runInNewContext(code,{exports,require:n=>deps[n]});return exports; }
const nav=module('../app/atlas-navigation.ts');
const plans=JSON.parse(readFileSync(new URL('../app/atlas-site-plans.json',import.meta.url),'utf8'));
const {entries,places}=JSON.parse(readFileSync(new URL('../app/atlas-data.json',import.meta.url),'utf8'));
const model=module('../app/atlas-explorer-model.ts',{'./atlas-navigation':nav,'./atlas-site-plans.json':plans});
const primary=id=>entries.find(e=>e.id===id)?.candidates[0]?.placeId??null;
assert.equal(new Set(plans.map(p=>p.id)).size,plans.length);
let roundtrips=0;
for(const p of plans){
 assert.ok(p.width>0&&p.height>0&&p.features.length>0);
 assert.ok(p.limit.includes('registration')||p.limit.includes('unregistered')||p.limit.includes('image-coordinate'));
 for(const id of p.placeIds)assert.ok(places.some(place=>place.id===id),id);
 assert.equal(new Set(p.features.map(f=>f.id)).size,p.features.length);
 for(const f of p.features){
  assert.ok(f.x>=0&&f.x<=p.width&&f.y>=0&&f.y<=p.height,`${p.id}/${f.id} must stay in its source frame`);
  assert.ok(f.description&&f.limit&&f.sources.length&&f.sourceUrl);
  for(const id of f.entryIds)assert.ok(entries.some(e=>e.id===id));
  for(const view of ['plan','photo']){
   const state={...model.initialExplorer,mode:'site',entryId:f.entryIds[0],placeId:p.placeIds[0],planId:p.id,featureId:f.id,siteView:view};
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
