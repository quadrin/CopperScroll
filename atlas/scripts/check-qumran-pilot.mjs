import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import ts from "typescript";
// Compile in memory so this geometry check needs neither a GPU nor a preview server.
const source=await readFile(new URL("../app/atlas-qumran-pilot.ts",import.meta.url),"utf8");
const compiled=ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ESNext}}).outputText
 .replace('from "three"',`from ${JSON.stringify(import.meta.resolve("three"))}`)
 .replace('from "maplibre-gl"',`from ${JSON.stringify(import.meta.resolve("maplibre-gl"))}`);
const pilot=await import(`data:text/javascript;base64,${Buffer.from(compiled).toString("base64")}`);
assert(pilot.pilotAvailable("kh_qumran"));assert(pilot.pilotAvailable("wadi_qumran"));assert(!pilot.pilotAvailable("abu_saraj"));
assert.deepEqual(pilot.pilotLocation(0,0).map(n=>+n.toFixed(5)),pilot.PILOT_ANCHOR);
assert(pilot.pilotLocation(10,0)[0]>pilot.PILOT_ANCHOR[0]);assert(pilot.pilotLocation(0,10)[1]<pilot.PILOT_ANCHOR[1]);
const model=pilot.buildQumranPilot();let vertices=0,instances=0,meshes=0;
model.traverse(o=>{if(!o.isMesh)return;meshes++;if(o.isInstancedMesh)instances+=o.count;const p=o.geometry.getAttribute("position");vertices+=p.count;for(const x of p.array)assert(Number.isFinite(x));});
assert(meshes>100);assert.equal(instances,2100);assert(vertices>10000);
// All camera stops remain close to the same model, with the low-view pitch supported by map config.
for(const s of Object.values(pilot.pilotStops)){assert(Math.abs(s.x)<64&&Math.abs(s.z)<39);assert(s.zoom<=22&&s.pitch<=85);}
const mapSource=await readFile(new URL("../app/atlas-map.tsx",import.meta.url),"utf8");
assert(mapSource.includes("maxPitch:85"));assert(mapSource.includes("Approximate placement"));assert(mapSource.includes("not a photogrammetric reconstruction"));
model.traverse(o=>{if(o.isMesh){o.geometry.dispose();(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>m.dispose());}});
console.log(`Qumran pilot checks passed: ${meshes} meshes, ${instances} instanced rocks, finite coordinates and map camera stops.`);
