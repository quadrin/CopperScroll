import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import ts from "typescript";
import * as Three from 'three';
import * as maplibre from 'maplibre-gl';
// Compile in memory so this geometry check needs neither a GPU nor a preview server.
async function module(path,deps){const exports={};const code=ts.transpileModule(await readFile(new URL(path,import.meta.url),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText;new Function('exports','require',code)(exports,name=>{assert(name in deps,`Missing test dependency: ${name}`);return deps[name]});return exports;}
const siteSurfaces=JSON.parse((await import('node:fs')).readFileSync(new URL('../app/atlas-site-surfaces.json',import.meta.url),'utf8'));
const surfaces=await module('../app/atlas-site-materials.ts',{'three':Three,'./atlas-site-surfaces.json':{__esModule:true,default:siteSurfaces,...siteSurfaces}});
const pilot=await module('../app/atlas-qumran-pilot.ts',{'three':Three,'maplibre-gl':maplibre,'./atlas-site-materials':surfaces});
assert(pilot.pilotAvailable("kh_qumran"));assert(pilot.pilotAvailable("wadi_qumran"));assert(!pilot.pilotAvailable("abu_saraj"));
assert.deepEqual(pilot.pilotLocation(0,0).map(n=>+n.toFixed(5)),pilot.PILOT_ANCHOR);
assert(pilot.pilotLocation(10,0)[0]>pilot.PILOT_ANCHOR[0]);assert(pilot.pilotLocation(0,10)[1]<pilot.PILOT_ANCHOR[1]);
const model=pilot.buildQumranPilot();let vertices=0,instances=0,meshes=0,cliffs=0;
model.traverse(o=>{if(!o.isMesh)return;meshes++;if(o.isInstancedMesh)instances+=o.count;const p=o.geometry.getAttribute("position");vertices+=p.count;for(const x of p.array)assert(Number.isFinite(x));if(o.name==='connected-limestone-bed'){cliffs++;const normals=o.geometry.getAttribute('normal');assert(Array.from(normals.array).some(n=>n>.5),'Cliff faces must have outward normals');}});
assert(meshes>10);assert(instances>500);assert(vertices>10000);assert(cliffs>0,'The limestone bank must have continuous rock geometry');
const ground=model.getObjectByName('qumran-ground'),p=ground.geometry.getAttribute('position'),colour=ground.geometry.getAttribute('color');
assert(ground.material.transparent,'The ground apron must blend into the geographic map');
assert.equal(ground.material.depthWrite,false,'Invisible apron pixels must not hide the landscape behind them');
assert.equal(model.getObjectByName('qumran-ridge-back').material.depthWrite,false,'The feathered ridge must not punch holes through the ground or sky');
assert(Array.from({length:colour.count},(_,i)=>colour.getW(i)).some(a=>a>0&&a<1),'The apron needs a gradual alpha transition');
for(let i=0;i<p.count;i++)if(Math.abs(p.getX(i))>125||Math.abs(p.getZ(i))>105)assert.equal(colour.getW(i),0,'No opaque rectangular perimeter');
const original=Float32Array.from(p.array);let samples=0;
pilot.fitQumranGround(model,(x,z)=>{samples++;return x*.12+z*.08;});
assert(samples<100,'Terrain adaptation must use a bounded elevation grid');
for(let i=0;i<p.count;i++){
 assert(Math.abs(p.getY(i)-(original[i*3+1]+p.getX(i)*.12+p.getZ(i)*.08))<.0001,'The whole ground must follow a sloped DEM without a raised bench');
 assert.equal(p.getX(i),original[i*3]);assert.equal(p.getZ(i),original[i*3+2]);
}
model.traverse(o=>{if(!o.isInstancedMesh)return;const source=o.userData.sourceMatrices,m=o.instanceMatrix.array;for(let i=0;i<o.count;i++){const k=i*16;assert(Math.abs(m[k+13]-(source[k+13]+source[k+12]*.12+source[k+14]*.08))<.0001,'Stones must follow their ground');for(const c of [0,4,8])assert(Math.abs(m[k+c+1]-(source[k+c+1]+source[k+c]*.12+source[k+c+2]*.08))<.0001,'Long channel floors must follow the local slope');}});
pilot.fitQumranGround(model,()=>0);assert(p.array.every((v,i)=>v===original[i]),'Returning to flat Map mode must remove terrain offsets');
const crest=model.getObjectByName('qumran-ridge-back').geometry.getAttribute('position');
assert(Math.abs(crest.getY(85*29)-crest.getY(60*29))>1,'The ridge must have an uneven crest');
assert(crest.getY(0)<2.5&&crest.getY(170*29)<2.5&&crest.getY(85*29)>5,'The cliff ends must taper into the ground');
const ridgeNormals=model.getObjectByName('qumran-ridge-back').geometry.getAttribute('normal');
assert(ridgeNormals.getY(85*29+15)>.5,'The ridge must face upward and receive sunlight');
// All camera stops remain close to the same model, with the low-view pitch supported by map config.
for(const s of Object.values(pilot.pilotStops)){assert(Math.abs(s.x)<64&&Math.abs(s.z)<39);assert(s.zoom<=22&&s.pitch<=85);}
const mapSource=await readFile(new URL("../app/atlas-map.tsx",import.meta.url),"utf8");
assert(mapSource.includes("maxPitch:85"));
const integratedSource=await readFile(new URL("../app/atlas-map-site-layer.ts",import.meta.url),"utf8");
assert(integratedSource.includes("approximate display alignment"));assert(integratedSource.includes("does not reconstruct the whole Qumran settlement"));
surfaces.disposeSiteScene(model);
console.log(`Qumran pilot checks passed: ${meshes} meshes, ${instances} instanced stones, finite coordinates and map camera stops.`);
