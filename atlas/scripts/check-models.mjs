import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import ts from 'typescript';
import * as Three from 'three';
import {SVGLoader} from 'three/addons/loaders/SVGLoader.js';

const terrain=JSON.parse(readFileSync(new URL('../app/atlas-model-terrain.json',import.meta.url),'utf8'));
function module(path,deps){const exports={};const code=ts.transpileModule(readFileSync(new URL(path,import.meta.url),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText;new Function('exports','require',code)(exports,name=>{assert(name in deps,`Missing test dependency: ${name}`);return deps[name]});return exports;}
const siteSurfaces=JSON.parse(readFileSync(new URL('../app/atlas-site-surfaces.json',import.meta.url),'utf8'));
const surfaces=module('../app/atlas-site-materials.ts',{'three':Three,'./atlas-site-surfaces.json':{__esModule:true,default:siteSurfaces,...siteSurfaces}});
const landscape=module('../app/atlas-model-landscape.ts',{'three':Three,'./atlas-model-terrain.json':terrain,'./atlas-site-materials':surfaces});
const tracedPlans=JSON.parse(readFileSync(new URL('../app/atlas-traced-plans.json',import.meta.url),'utf8'));
const contextData=JSON.parse(readFileSync(new URL('../app/atlas-site-context.json',import.meta.url),'utf8'));
const context=module('../app/atlas-model-context.ts',{'three':Three,'./atlas-site-context.json':{__esModule:true,default:contextData,...contextData},'./atlas-site-materials':surfaces});
const exports=module('../app/atlas-model-geometry.ts',{'three':Three,'three/addons/loaders/SVGLoader.js':{SVGLoader},'./atlas-model-landscape':landscape,'./atlas-model-context':context,'./atlas-site-materials':surfaces,'./atlas-traced':module('../app/atlas-traced.ts',{}),'./atlas-traced-plans.json':{__esModule:true,default:tracedPlans,...tracedPlans}});
for(const patch of Object.values(terrain)){assert.equal(patch.elevations.length,patch.size**2);assert.ok(patch.elevations.every(Number.isFinite));assert.ok(Math.abs(landscape.elevationAt(patch,0,0))<.02);}
const plans=JSON.parse(readFileSync(new URL('../app/atlas-site-plans.json',import.meta.url),'utf8'));
const models=new Map();
for(const id of ['abu-saraj-iv17','hyrcania-waterworks','gerizim-precinct','doq-waterworks','jericho-early','jericho-late','bethesda-pools','east-gate-warren','kidron-bene-hezir','temple-great-sea']){
 const plan=plans.find(p=>p.id===id),model=exports.buildModel(plan);
 assert.deepEqual([...model.markers.keys()].sort(),plan.features.map(f=>f.id).sort(),`${id}: all source features must remain selectable`);
 for(const marker of model.markers.values())assert.ok(marker.toArray().every(Number.isFinite));
 const box=new Three.Box3().setFromObject(model.root);
 assert.ok(box.min.toArray().concat(box.max.toArray()).every(Number.isFinite));
 assert.equal(model.roof.visible,false);
 assert.ok(model.assumptions.some(text=>/illustrative/.test(text)),`${id}: display assumptions must be disclosed`);
 models.set(id,model);
}
const hyrcania=models.get('hyrcania-waterworks');
for(const [id,depth] of [['north-pool',5],['south-member',2.6]]){
 const floor=hyrcania.selectable.find(o=>o.userData.featureId===id&&o.geometry.type==='ExtrudeGeometry');
 const box=new Three.Box3().setFromObject(floor);
 assert.ok(Math.abs(box.max.y+depth)<1e-6,`${id}: basin floor must follow its own published depth`);
}
const cave=models.get('abu-saraj-iv17');
const pillar=cave.selectable.find(o=>o.userData.featureId==='pillar');
const height=new Three.Box3().setFromObject(pillar).getSize(new Three.Vector3()).y;
assert.ok(height>=1.4&&height<=1.7,'cave height must remain within the reported range');
assert.equal(cave.units,'metres');
assert.equal(cave.landscape.mapped,false,'unlocated cave must not acquire geographic terrain');
assert.equal(models.get('gerizim-precinct').landscape.mapped,true);
assert.ok(models.get('gerizim-precinct').assumptions.some(s=>s.includes('not surveyed or registered')));
assert.equal(models.get('doq-waterworks').units,'relative');
assert.ok(models.get('gerizim-precinct').assumptions.some(s=>s.includes('not equated with the southern seven-step')));
// Traced plans: each view builds; the remains view shows only what was found, and a
// reconstruction view draws exactly its reconstruction-only parts in the restored surface.
const surfaceOf=o=>[o.material].flat().map(m=>m?.userData?.siteSurface);
let tracedViews=0;
for(const plan of plans.filter(p=>p.traced)){
 const source=tracedPlans[plan.traced];assert.ok(source,`${plan.id}: traced plan ${plan.traced} missing (run node scripts/build-traced-plans.mjs)`);
 for(const layer of plan.layers??[{id:'remains',kind:'observed'}]){
  const model=exports.buildModel(plan,{layer:layer.id}),shown=source.elements.filter(e=>e.layers.includes(layer.id));
  assert.deepEqual([...model.markers.keys()].sort(),plan.features.map(f=>f.id).sort(),`${plan.id}@${layer.id}: all source features must remain selectable`);
  assert.ok(new Three.Box3().setFromObject(model.root).min.toArray().every(Number.isFinite),`${plan.id}@${layer.id}: finite geometry`);
  assert.ok(model.assumptions.some(t=>/illustrative|preserved heights are not traced/.test(t)),`${plan.id}@${layer.id}: heights must be disclosed`);
  for(const e of shown){
   if(e.kind==='cliff-edge')continue;
   const parts=model.selectable.filter(o=>o.userData.featureId===e.id);
   assert.ok(parts.length,`${plan.id}@${layer.id}: element ${e.id} is drawn`);
   const pale=parts.flatMap(surfaceOf).map(s=>s==='restored'),rebuilt=layer.kind!=='observed'&&e.status!=='observed';
   assert.ok(rebuilt?pale.every(Boolean):!pale.some(Boolean),`${plan.id}@${layer.id}: ${e.id} must ${rebuilt?'':'not '}use the restored surface`);
  }
  if(layer.kind==='observed')assert.ok(shown.every(e=>e.status==='observed'),`${plan.id}: the remains view holds only observed elements`);
  tracedViews++;
 }
}
// Hand-built plans with views: the remains view uses no restored surface; each reconstruction
// view draws its reconstruction-only parts in the restored surface and says so.
let builtViews=0;
for(const plan of plans.filter(p=>!p.traced&&p.layers?.length)){
 for(const layer of plan.layers){
  const model=exports.buildModel(plan,{layer:layer.id}),pale=[];model.root.traverse(o=>{if(o.isMesh)pale.push(...surfaceOf(o).map(s=>s==='restored'));});
  assert.deepEqual([...model.markers.keys()].sort(),plan.features.map(f=>f.id).sort(),`${plan.id}@${layer.id}: all source features must remain selectable`);
  assert.ok(new Three.Box3().setFromObject(model.root).min.toArray().every(Number.isFinite),`${plan.id}@${layer.id}: finite geometry`);
  if(layer.kind==='observed')assert.ok(!pale.some(Boolean),`${plan.id}: the remains view uses no restored surface`);
  else{assert.ok(pale.some(Boolean),`${plan.id}@${layer.id}: reconstruction-only parts use the restored surface`);assert.ok(model.assumptions.some(t=>/drawn only by/.test(t)),`${plan.id}@${layer.id}: the reconstruction is disclosed`);}
  builtViews++;
 }
}
const kidron=models.get('kidron-bene-hezir');
assert.ok(kidron.assumptions.some(t=>t.includes('south-west')),'Bene Ḥezir: the façade faces south-west (Avigad p. 37)');
const sea=models.get('temple-great-sea');
assert.ok(sea.assumptions.some(t=>t.includes('Pl. VII')),'Great Sea: the plate outline is disclosed');
// Registered models keep the place frame: their mapped monuments and corners stay where OpenStreetMap puts them,
// and the mapped surroundings are drawn and credited.
const placed=JSON.parse(readFileSync(new URL('../app/atlas-site-context.json',import.meta.url),'utf8')).plans;
{const r=placed['kidron-bene-hezir'].registration,a=kidron.markers.get('absalom'),p=kidron.markers.get('porch');
 assert.ok(Math.hypot(a.x-r.absalomCentre[0],a.z-r.absalomCentre[1])<.01,'Absalom stands at its mapped centre');
 assert.ok(Math.hypot(p.x-r.porchCentre[0],p.z-r.porchCentre[1])<.01,'the Bene Ḥezir porch sits on the mapped porch');
 assert.ok(Math.abs(Math.hypot(a.x-p.x,a.z-p.z)-50)<5,'Absalom is about 50 m from Bene Ḥezir (Avigad p. 37)');
 assert.ok(Math.abs(r.facadeNormalBearing-225)<45,'the mapped façade faces Avigad’s south-west');}
{const r=placed['temple-great-sea'].registration,c=sea.markers.get('great-sea');
 assert.ok(r.residuals_m.every(v=>v<2),'Pl. VII fits the mapped Haram corners within 2 m');
 assert.ok(Math.hypot(c.x-r.origin[0],c.z-r.origin[1])<3,'the cistern sits at its registered place');}
for(const model of [kidron,sea]){
 const group=model.root.children.find(c=>c.userData.siteContext==='osm');
 assert.ok(group&&model.landscape.credit.includes('OpenStreetMap')&&model.assumptions.some(t=>t.includes('Open Database License')),'mapped surroundings are drawn and credited');
}
assert.ok(kidron.root.children.find(c=>c.userData.siteContext==='osm').userData.counts.graves>1000,'Kidron: the Mount of Olives graves are drawn');
console.log(`3D model checks passed: complete feature coverage, finite geometry, disclosed assumptions, separate published pool depths, bounded cave height, Gerizim stair distinction, two models registered to mapped outlines with their surroundings, ${tracedViews} traced-plan views and ${builtViews} views of hand-built plans.`);
