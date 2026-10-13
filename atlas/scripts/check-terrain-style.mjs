import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import ts from 'typescript';
const source=readFileSync(new URL('../app/atlas-terrain-style.ts',import.meta.url),'utf8');
const code=ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS}}).outputText;
const exports={};vm.runInNewContext(code,{exports,structuredClone});
const fixture={version:8,sources:{tiles:{type:'vector',url:'https://example.com/tiles.json'}},layers:[
 {id:'background',type:'background'},
 ...['building','transportation','landuse','poi','landcover','water','water_name','place'].map(name=>({id:name,type:['water_name','place','poi'].includes(name)?'symbol':'fill',source:'tiles','source-layer':name})),
 {id:'private-height-estimates',type:'fill-extrusion',source:'tiles','source-layer':'unknown'},
 {id:'detailed-place',type:'symbol',source:'tiles','source-layer':'place',minzoom:15},
]};
const before=JSON.stringify(fixture);const cleaned=exports.terrainOnlyStyle(fixture);
assert.equal(JSON.stringify(fixture),before,'The downloaded style must not be mutated');
assert.deepEqual(Array.from(cleaned.layers.map(l=>l.id)),['background','landcover','water','water_name','place']);
assert.equal(cleaned.layers.find(l=>l.id==='place').maxzoom,11.5);
assert.equal(exports.terrainFallback.layers.some(l=>l.type==='raster'),false,'Fallback must not reintroduce a modern street raster');
if(process.env.ATLAS_STYLE_FIXTURE){const live=JSON.parse(readFileSync(process.env.ATLAS_STYLE_FIXTURE,'utf8'));const actual=exports.terrainOnlyStyle(live);assert.ok(actual.layers.some(l=>l.type==='fill'&&l['source-layer']==='water'));assert.ok(actual.layers.every(l=>l.type!=='fill-extrusion'&&!/building|transportation|landuse|poi|road|rail/i.test((l['source-layer']??'')+' '+l.id)));console.log(`Live basemap checked: ${actual.layers.length} physical-geography layers retained; modern urban layers removed.`);}
console.log('Terrain style checks passed: no buildings, streets, land-use/POIs, hidden urban heights or modern-raster fallback.');
