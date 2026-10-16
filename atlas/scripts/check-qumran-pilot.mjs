import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import ts from "typescript";
import * as Three from 'three';
import * as maplibre from 'maplibre-gl';
// Compile in memory so this geometry check needs neither a GPU nor a preview server.
async function module(path,deps){const exports={};const code=ts.transpileModule(await readFile(new URL(path,import.meta.url),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText;new Function('exports','require',code)(exports,name=>{assert(name in deps,`Missing test dependency: ${name}`);return deps[name]});return exports;}
const surfaces=await module('../app/atlas-site-materials.ts',{'three':Three});
const pilot=await module('../app/atlas-qumran-pilot.ts',{'three':Three,'maplibre-gl':maplibre,'./atlas-site-materials':surfaces});
assert(pilot.pilotAvailable("kh_qumran"));assert(pilot.pilotAvailable("wadi_qumran"));assert(!pilot.pilotAvailable("abu_saraj"));
assert.deepEqual(pilot.pilotLocation(0,0).map(n=>+n.toFixed(5)),pilot.PILOT_ANCHOR);
assert(pilot.pilotLocation(10,0)[0]>pilot.PILOT_ANCHOR[0]);assert(pilot.pilotLocation(0,10)[1]<pilot.PILOT_ANCHOR[1]);
const model=pilot.buildQumranPilot();let vertices=0,instances=0,meshes=0,cliffs=0;
model.traverse(o=>{if(!o.isMesh)return;meshes++;if(o.isInstancedMesh)instances+=o.count;const p=o.geometry.getAttribute("position");vertices+=p.count;for(const x of p.array)assert(Number.isFinite(x));if(o.name==='connected-limestone-bed'){cliffs++;const normals=o.geometry.getAttribute('normal');assert(Array.from(normals.array).some(n=>n>.5),'Cliff faces must have outward normals');}});
assert(meshes>10);assert(instances>500);assert(vertices>10000);assert(cliffs>0,'The limestone bank must have continuous rock geometry');
// All camera stops remain close to the same model, with the low-view pitch supported by map config.
for(const s of Object.values(pilot.pilotStops)){assert(Math.abs(s.x)<64&&Math.abs(s.z)<39);assert(s.zoom<=22&&s.pitch<=85);}
const mapSource=await readFile(new URL("../app/atlas-map.tsx",import.meta.url),"utf8");
assert(mapSource.includes("maxPitch:85"));
const integratedSource=await readFile(new URL("../app/atlas-map-site-layer.ts",import.meta.url),"utf8");
assert(integratedSource.includes("approximate display alignment"));assert(integratedSource.includes("does not reconstruct the whole Qumran settlement"));
surfaces.disposeSiteScene(model);
console.log(`Qumran pilot checks passed: ${meshes} meshes, ${instances} instanced stones, finite coordinates and map camera stops.`);
