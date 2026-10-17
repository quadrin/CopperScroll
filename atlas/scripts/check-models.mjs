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
const exports=module('../app/atlas-model-geometry.ts',{'three':Three,'three/addons/loaders/SVGLoader.js':{SVGLoader},'./atlas-model-landscape':landscape,'./atlas-site-materials':surfaces});
for(const patch of Object.values(terrain)){assert.equal(patch.elevations.length,patch.size**2);assert.ok(patch.elevations.every(Number.isFinite));assert.ok(Math.abs(landscape.elevationAt(patch,0,0))<.02);}
const plans=JSON.parse(readFileSync(new URL('../app/atlas-site-plans.json',import.meta.url),'utf8'));
const models=new Map();
for(const id of ['abu-saraj-iv17','hyrcania-waterworks','gerizim-precinct','doq-waterworks','jericho-early','jericho-late']){
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
console.log('3D model checks passed: complete feature coverage, finite geometry, disclosed assumptions, separate published pool depths, bounded cave height and Gerizim stair distinction.');
