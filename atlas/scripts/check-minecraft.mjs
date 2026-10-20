// Checks the Minecraft block builds in public/minecraft/ against the source models.
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import * as Three from 'three';
import {loadModels} from './minecraft/load-models.mjs';
import {SITES} from './minecraft/build-world.mjs';

const dir=new URL('../public/minecraft/',import.meta.url),index=JSON.parse(readFileSync(new URL('index.json',dir),'utf8'));
assert.equal(index.minecraft.edition,'Java Edition');
assert.match(index.minecraft.version??'',/^\d/,'the server version must be recorded');
assert.match(index.minecraft.serverJarSha1??'',/^[0-9a-f]{40}$/,'the server jar hash must be recorded');
const models=loadModels(),mapped=new Set(models.places.filter(p=>p.lat!==null&&p.lon!==null).map(p=>p.id));
for(const spec of SITES){
 const plan=models.plans.find(p=>p.id===spec.id),site=index.sites[spec.id];
 assert.ok(plan&&plan.kind!=='survey-map',`${spec.id}: a source model plan`);
 assert.ok(site,`${spec.id}: built in the world`);
 assert.equal(site.readback.mismatches,0,`${spec.id}: every block read back as placed`);
 assert.ok(site.fills?.filled>0,`${spec.id}: the server filled blocks`);
 const onMap=plan.placeIds.some(id=>mapped.has(id));
 if(!onMap){assert.equal(site.file,null,`${spec.id}: an unplaced site gets no map file`);continue;}
 assert.ok(site.file&&existsSync(new URL(site.file,dir)),`${spec.id}: map file present`);
 const bytes=gunzipSync(readFileSync(new URL(site.file,dir))),length=bytes.readUInt32LE(0),header=JSON.parse(bytes.toString('utf8',4,4+length));
 assert.equal(header.id,spec.id);assert.equal(header.size,spec.size);assert.equal(header.half,spec.size/2);
 const features=new Set(plan.features.map(f=>f.id));for(const f of header.features)assert.ok(features.has(f),`${spec.id}: feature ${f} is a plan feature`);
 // Ilan–Amit's basin 2 and the dam proposed at point 4 (copper marks the reconstruction).
 if(spec.pilot){assert.ok(header.features.includes('basin2'),'qumran-ilan: basin 2 is built');assert.ok(Object.keys(site.counts).some(k=>k.startsWith('waxed_cut_copper')),'qumran-ilan: the reconstructed dam is built in copper');}
 const [nx,ny,nz]=header.dims;let offset=4+length,quads=0;
 for(const g of header.groups){
  assert.ok(g.material>=1&&g.material<header.materials.length,`${spec.id}: known material`);
  const q=new Uint16Array(bytes.buffer.slice(bytes.byteOffset+offset,bytes.byteOffset+offset+g.quads*12));offset+=g.quads*12;quads+=g.quads;
  for(let i=0;i<q.length;i+=6){
   const dir=q[i]&7,light=q[i]>>3,axis=dir>>1,[ua,va]=axis===0?[2,1]:axis===1?[0,2]:[0,1],dims=[nx,ny,nz];
   assert.ok(dir<6&&light<=15,`${spec.id}: face direction and sky light in range`);
   assert.ok(q[i+1]<=dims[axis]&&q[i+2]<q[i+4]&&q[i+4]<=dims[ua]&&q[i+3]<q[i+5]&&q[i+5]<=dims[va],`${spec.id}: quad inside the block grid`);
  }
 }
 assert.equal(offset,bytes.length,`${spec.id}: no trailing data`);assert.equal(quads,site.quads);
 // The block grid must sit on the source model's frame: its markers fall inside it.
 const box=new Three.Box3(new Three.Vector3(header.origin[0],header.origin[1],header.origin[2]),new Three.Vector3(header.origin[0]+nx*header.size,header.origin[1]+ny*header.half,header.origin[2]+nz*header.size));
 const markers=spec.pilot?plan.features.map(f=>new Three.Vector3((f.x+120-381)*.2,0,(f.y+1080-1240)*.2)):[...models.geometry.buildModel(plan).markers.values()];
 for(const m of markers)assert.ok(m.x>=box.min.x&&m.x<=box.max.x&&m.z>=box.min.z&&m.z<=box.max.z,`${spec.id}: marker inside the block grid`);
}
console.log(`Minecraft build checks passed: ${SITES.length} sites built in ${index.minecraft.edition} ${index.minecraft.version}, every block read back as placed, map files decode within their grids and on their source frames.`);
