// Checks the Minecraft block builds in public/minecraft/ against the source models.
//   node scripts/check-minecraft.mjs [--require-bare]
// A bare build (the Ancient ground view, `<build>.bare`) that is not built yet is listed; the atlas
// draws that view smooth. --require-bare makes a missing bare build a failure.
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import * as Three from 'three';
import {loadModels} from './minecraft/load-models.mjs';
import {buildSpecs,ringsFor,wideTerrain,bareKey} from './minecraft/build-world.mjs';
import {materialCode} from './minecraft/voxelize.mjs';

const requireBare=process.argv.includes('--require-bare');
const dir=new URL('../public/minecraft/',import.meta.url),index=JSON.parse(readFileSync(new URL('index.json',dir),'utf8'));
assert.equal(index.minecraft.edition,'Java Edition');
assert.match(index.minecraft.version??'',/^\d/,'the server version must be recorded');
assert.match(index.minecraft.serverJarSha1??'',/^[0-9a-f]{40}$/,'the server jar hash must be recorded');
const models=loadModels(),mapped=new Set(models.places.filter(p=>p.lat!==null&&p.lon!==null).map(p=>p.id)),specs=buildSpecs(models);
// Codes 8–11 (leaves, wood, green ground, asphalt) are today's setting only; soil and rock are the ground.
const SETTING_STATES=/^(oak_leaves|oak_log|moss_block|gray_concrete)\b/,GROUND=new Set([1,2]);
const files=new Map(),missing=[];
for(const spec of specs){
 const plan=models.plans.find(p=>p.id===spec.plan),site=index.sites[spec.id];
 assert.ok(plan&&plan.kind!=='survey-map',`${spec.id}: a source model plan`);
 if(!site&&spec.bare&&!requireBare){missing.push(spec.id);continue;}
 assert.ok(site,`${spec.id}: built in the world`);
 assert.equal(site.readback.mismatches,0,`${spec.id}: every block read back as placed`);
 assert.ok(site.fills?.filled>0,`${spec.id}: the server filled blocks`);
 if(spec.bare){
  // A bare build stands for one normal build and was made with the Ancient ground view's current pads.
  assert.equal(site.bare,true,`${spec.id}: marked bare`);assert.equal(site.normalBuild,spec.normal,`${spec.id}: names the build it stands for`);
  assert.equal(JSON.stringify(site.pads??null),JSON.stringify(spec.pads??null),`${spec.id}: built with the Ancient ground view's current pads (rebuild with --sites ${spec.plan} --bare-only)`);
  assert.ok(!Object.keys(site.counts).some(k=>SETTING_STATES.test(k)),`${spec.id}: no block of today's setting (leaves, wood, green ground, asphalt)`);
 }else assert.equal(site.bare,undefined,`${spec.id}: not marked bare`);
 const onMap=plan.placeIds.some(id=>mapped.has(id));
 if(!onMap){assert.equal(site.file,null,`${spec.id}: an unplaced site gets no map file`);continue;}
 assert.ok(site.file&&existsSync(new URL(site.file,dir)),`${spec.id}: map file present`);
 const bytes=gunzipSync(readFileSync(new URL(site.file,dir))),length=bytes.readUInt32LE(0),header=JSON.parse(bytes.toString('utf8',4,4+length));
 assert.equal(header.id,spec.id);assert.equal(header.size,spec.size);assert.equal(header.half,spec.size/2);assert.equal(!!header.bare,!!spec.bare,`${spec.id}: header marks a bare build`);
 if(spec.bare)assert.ok(header.materials.length<=8,`${spec.id}: lists no material of today's setting`);
 const [nx,ny,nz]=header.dims;let offset=4+length,quads=0;const groups=[];
 for(const g of header.groups){
  assert.ok(g.material>=1&&g.material<header.materials.length,`${spec.id}: known material`);
  const q=new Uint16Array(bytes.buffer.slice(bytes.byteOffset+offset,bytes.byteOffset+offset+g.quads*12));offset+=g.quads*12;quads+=g.quads;groups.push({material:g.material,quads:q});
  for(let i=0;i<q.length;i+=6){
   const dir=q[i]&7,light=q[i]>>3,axis=dir>>1,[ua,va]=axis===0?[2,1]:axis===1?[0,2]:[0,1],dims=[nx,ny,nz];
   assert.ok(dir<6&&light<=15,`${spec.id}: face direction and sky light in range`);
   assert.ok(q[i+1]<=dims[axis]&&q[i+2]<q[i+4]&&q[i+4]<=dims[ua]&&q[i+3]<q[i+5]&&q[i+5]<=dims[va],`${spec.id}: quad inside the block grid`);
  }
 }
 assert.equal(offset,bytes.length,`${spec.id}: no trailing data`);assert.equal(quads,site.quads);
 files.set(spec.id,{header,groups});
 if(spec.ring!==undefined){
  // A ring spans its square and leaves out exactly the build inside it (checked below).
  assert.deepEqual([header.origin[0],header.origin[2],header.dims[0]*spec.size,header.dims[2]*spec.size],[-spec.half,-spec.half,2*spec.half,2*spec.half],`${spec.id}: ring extent`);
  continue;
 }
 if(plan.terrain==='wide'){
  const rings=specs.filter(s=>s.plan===plan.id&&s.ring!==undefined&&!s.bare===!spec.bare).map(s=>s.id);
  assert.ok(site.surroundings?.length===ringsFor(plan.id).length,`${spec.id}: lists its terrain rings`);assert.deepEqual(site.surroundings,rings,`${spec.id}: lists its own ${spec.bare?'bare ':''}rings`);
 }
 // Blocks carry plan feature ids; a traced plan's blocks may also carry its element ids.
 const features=new Set([...plan.features.map(f=>f.id),...(models.tracedPlans[plan.traced]?.elements.map(e=>e.id)??[])]);for(const f of header.features)assert.ok(features.has(f),`${spec.id}: feature ${f} is a plan feature or traced element`);
 // Ilan–Amit's basin 2 and the dam proposed at point 4 (copper marks the reconstruction).
 if(spec.pilot){assert.ok(header.features.includes('basin2'),'qumran-ilan: basin 2 is built');assert.ok(Object.keys(site.counts).some(k=>k.startsWith('waxed_cut_copper')),'qumran-ilan: the reconstructed dam is built in copper');}
 // The block grid must sit on the source model's frame: its markers fall inside it.
 const box=new Three.Box3(new Three.Vector3(header.origin[0],header.origin[1],header.origin[2]),new Three.Vector3(header.origin[0]+nx*header.size,header.origin[1]+ny*header.half,header.origin[2]+nz*header.size));
 const markers=spec.pilot?plan.features.map(f=>new Three.Vector3((f.x+120-381)*.2,0,(f.y+1080-1240)*.2)):[...models.geometry.buildModel(plan,{layer:spec.layer}).markers.values()];
 if(!spec.layer||spec.layer==='remains')for(const m of markers)assert.ok(m.x>=box.min.x&&m.x<=box.max.x&&m.z>=box.min.z&&m.z<=box.max.z,`${spec.id}: marker inside the block grid`);
}

// Each face as the column (i, k) of the solid cell behind it, with the face's height in cells.
function forColumns({header,groups},fn){
 for(const {material,quads:q} of groups)for(let n=0;n<q.length;n+=6){
  const dir=q[n]&7,axis=dir>>1,inner=dir&1?q[n+1]:q[n+1]-1,u0=q[n+2],v0=q[n+3],u1=q[n+4],v1=q[n+5];
  if(axis===1){for(let i=u0;i<u1;i++)for(let k=v0;k<v1;k++)fn(i,k,material,1,dir);}
  else for(let u=u0;u<u1;u++)fn(axis===0?inner:u,axis===0?u:inner,material,v1-v0,dir);
 }
 return header;
}
// The model's own parts, as the voxelizer takes them: every visible solid except the ground and
// anything mapped. Their silhouettes on the ground (points sampled every half block over each
// triangle; small instances by their boxes), widened by one block, form the model's footprint.
function ownFootprint(model,header,minDetail){
 const [x0,,z0]=header.origin,[nx,,nz]=header.dims,s=header.size,seen=new Uint8Array(nx*nz),local=new Three.Matrix4(),world=new Three.Matrix4(),size=new Three.Vector3();
 const at=(x,z)=>{const i=Math.floor((x-x0)/s),k=Math.floor((z-z0)/s);if(i>=0&&k>=0&&i<nx&&k<nz)seen[i*nz+k]=1;};
 const a=new Three.Vector3(),b=new Three.Vector3(),c=new Three.Vector3(),ab=new Three.Vector3(),ac=new Three.Vector3(),p=new Three.Vector3();
 const sample=(geometry,matrix)=>{
  const pos=geometry.getAttribute('position'),index=geometry.getIndex();
  for(let t=0;t<(index?.count??pos.count);t+=3){
   a.fromBufferAttribute(pos,index?index.getX(t):t).applyMatrix4(matrix);b.fromBufferAttribute(pos,index?index.getX(t+1):t+1).applyMatrix4(matrix);c.fromBufferAttribute(pos,index?index.getX(t+2):t+2).applyMatrix4(matrix);
   ab.subVectors(b,a);ac.subVectors(c,a);const steps=Math.max(1,Math.ceil(Math.max(ab.length(),ac.length(),b.distanceTo(c))/(s/2)));
   for(let u=0;u<=steps;u++)for(let v=0;v<=steps-u;v++){p.copy(a).addScaledVector(ab,u/steps).addScaledVector(ac,v/steps);at(p.x,p.z);}
  }
 };
 const mapped=new Set();model.root.traverse(o=>{if(o.userData.siteContext==='osm')o.traverse(m=>mapped.add(m));});
 model.root.updateMatrixWorld(true);
 model.root.traverseVisible(o=>{
  if(!o.isMesh||mapped.has(o)||o.userData.siteContext==='ground'||(o.userData.walkCollision===false&&!o.userData.blockSolid)||!materialCode(o.material))return;
  if(!o.isInstancedMesh){sample(o.geometry,o.matrixWorld);return;}
  o.geometry.computeBoundingBox();const box=o.geometry.boundingBox;
  for(let n=0;n<o.count;n++){
   o.getMatrixAt(n,local);world.multiplyMatrices(o.matrixWorld,local);
   if(o.userData.walkDetail){box.getSize(size);const scale=new Three.Vector3().setFromMatrixScale(world);if(Math.max(size.x*scale.x,size.z*scale.z)<minDetail)continue;}
   const w=box.clone().applyMatrix4(world);for(let x=w.min.x;x<w.max.x+s/2;x+=s/2)for(let z=w.min.z;z<w.max.z+s/2;z+=s/2)at(Math.min(x,w.max.x),Math.min(z,w.max.z));
  }
 });
 // One block wider: thin parts are widened to a block and rounding moves an edge by up to half a block.
 const mask=new Uint8Array(nx*nz);
 for(let i=0;i<nx;i++)for(let k=0;k<nz;k++)if(seen[i*nz+k])for(let di=-1;di<=1;di++)for(let dk=-1;dk<=1;dk++){const ii=i+di,kk=k+dk;if(ii>=0&&kk>=0&&ii<nx&&kk<nz)mask[ii*nz+kk]=1;}
 return mask;
}
// Bare near builds: outside the model's own footprint only ground (soil, rock) may show a face. Faces
// of any other material there are today's graves, walls, buildings or paving; the normal build has them.
const report=[];
for(const spec of specs.filter(s=>s.bare&&s.ring===undefined&&files.has(s.id))){
 const bare=files.get(spec.id),normal=files.get(spec.normal),plan=models.plans.find(p=>p.id===spec.plan),{header}=bare;
 assert.ok(normal,`${spec.id}: its normal build ${spec.normal} is present`);
 assert.deepEqual([header.size,header.origin[0],header.origin[2],header.dims[0],header.dims[2]],[normal.header.size,normal.header.origin[0],normal.header.origin[2],normal.header.dims[0],normal.header.dims[2]],`${spec.id}: same block grid across the ground as ${spec.normal}`);
 // The model is built here without mapped surroundings, independently of the build script's options.
 const own=models.geometry.buildModel(plan,{layer:spec.layer,terrain:plan.terrain==='wide'?wideTerrain(plan.placeIds[0]):undefined,pads:spec.pads??undefined});
 const mask=ownFootprint(own,header,spec.size*.8),nz=header.dims[2];
 const outside=file=>{let faces=0;const by={};forColumns(file,(i,k,material,n)=>{if(mask[i*nz+k]||GROUND.has(material))return;faces+=n;by[file.header.materials[material]]=(by[file.header.materials[material]]??0)+n;});return {faces,by};};
 const b=outside(bare),t=outside(normal),share=mask.reduce((a,v)=>a+(v?0:1),0)/mask.length;
 assert.equal(b.faces,0,`${spec.id}: no face of a mapped feature or paving outside the model's own footprint (${JSON.stringify(b.by)})`);
 report.push(`${spec.id}: ${(100*share).toFixed(0)} % of columns outside the footprint; there ${spec.normal} has ${t.faces} faces of today's features (${Object.entries(t.by).map(([k,v])=>`${k} ${v}`).join(', ')}), the bare build none`);
}
// Rings: the hole is exactly the build inside (the plan's default view, or the ring inside); every
// column inside it is empty and every column on its rim is ground. A bare ring is cut for the bare build.
let holes=0;
for(const spec of specs.filter(s=>s.ring!==undefined&&files.has(s.id))){
 const ring=files.get(spec.id),[x0,,z0]=ring.header.origin,[nx,,nz]=ring.header.dims,s=ring.header.size,plan=models.plans.find(p=>p.id===spec.plan);
 let hole;
 if(spec.ring===0){const key=spec.bare?bareKey(plan.id):plan.id,inner=files.get(key)?.header;assert.ok(inner,`${spec.id}: the build inside it (${key}) is present`);hole=[inner.origin[0],inner.origin[0]+inner.dims[0]*inner.size,inner.origin[2],inner.origin[2]+inner.dims[2]*inner.size];}
 else{const h=ringsFor(plan.id)[spec.ring-1].half;hole=[-h,h,-h,h];}
 if(spec.bare&&files.has(spec.normal)){const t=files.get(spec.normal).header;assert.deepEqual([t.origin,t.dims].flat().filter((_,n)=>n!==1&&n!==4),[ring.header.origin,ring.header.dims].flat().filter((_,n)=>n!==1&&n!==4),`${spec.id}: same square as ${spec.normal}`);}
 const solid=new Uint8Array(nx*nz);forColumns(ring,(i,k,material,n,dir)=>{if(dir===2)solid[i*nz+k]=1;});
 let inside=0,rim=0,rimSolid=0;
 for(let i=0;i<nx;i++)for(let k=0;k<nz;k++){
  const cx=x0+(i+.5)*s,cz=z0+(k+.5)*s,within=cx>hole[0]&&cx<hole[1]&&cz>hole[2]&&cz<hole[3],near=cx>hole[0]-s&&cx<hole[1]+s&&cz>hole[2]-s&&cz<hole[3]+s;
  if(within){inside++;assert.equal(solid[i*nz+k],0,`${spec.id}: column (${cx}, ${cz}) inside the hole is empty`);}
  else if(near){rim++;rimSolid+=solid[i*nz+k];}
 }
 assert.ok(inside>0&&rim>0&&rimSolid===rim,`${spec.id}: the hole is exactly the build inside it (${rimSolid} of ${rim} rim columns are ground)`);
 holes++;
}
console.log(`Minecraft build checks passed: ${specs.length-missing.length} builds in ${index.minecraft.edition} ${index.minecraft.version}, every block read back as placed, map files decode within their grids and on their source frames, ${holes} ring holes match the builds inside them.`);
const bareBuilt=specs.filter(s=>s.bare&&files.has(s.id)).length;
console.log(`Bare builds (Ancient ground): ${bareBuilt} built, no block of today's setting, no mapped feature outside the models' own footprints${report.length?':':'.'}${report.map(r=>`\n  ${r}`).join('')}`);
if(missing.length)console.log(`Not built yet (the atlas draws these Ancient ground views smooth): ${missing.join(', ')}`);
