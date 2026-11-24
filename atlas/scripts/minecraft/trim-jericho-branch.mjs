// Reproduce the display cut on the archived 20–22 October Minecraft face exports.
// This preserves the server readback record. The next server build uses the shorter
// centreline directly. Supply the original atlas/public/minecraft directory as argv[2].
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {gunzipSync} from 'node:zlib';
import {loadModels} from './load-models.mjs';
import {encodeBuild} from './mesh.mjs';

const dir=fileURLToPath(new URL('../../public/minecraft/',import.meta.url));
const original=resolve(process.argv[2]??dir);
const index=JSON.parse(readFileSync(join(dir,'index.json'),'utf8'));
const models=loadModels(), feature='A(B)99-ch-N';
for(const id of ['jericho-early','jericho-late','jericho-late@stage6']){
 const plan=models.plans.find(p=>p.id===id.split('@')[0]);
 const model=models.geometry.buildModel(plan,{layer:id.split('@')[1]??'remains'});
 model.root.updateMatrixWorld(true);
 const branch=new models.Three.Box3();
 for(const part of model.selectable)if(part.userData.featureId===feature)branch.expandByObject(part);
 assert.ok(!branch.isEmpty());
 const endX=branch.max.x-model.root.position.x;
 for(const suffix of ['', '.bare']){
  const site=index.sites[id+suffix],input=readFileSync(join(original,site.file));
  const sha=createHash('sha256').update(input).digest('hex');
  if(site.displayCut&&original===dir)continue;
  if(site.displayCut)assert.equal(sha,site.displayCut.sourceSha256);
  const data=gunzipSync(input),length=data.readUInt32LE(0),header=JSON.parse(data.toString('utf8',4,4+length));
  const cut=Math.round((endX-header.origin[0])/header.size);
  let offset=4+length,trimmed=false;
  const groups=new Map();
  for(const group of header.groups){
   const quads=new Uint16Array(data.buffer,data.byteOffset+offset,group.quads*6);
   offset+=group.quads*12;
   const key=group.material+':'+group.feature;
   if(header.features[group.feature-1]!==feature){groups.set(key,quads);continue;}
   const faces=[],cap=new Map();
   for(let n=0;n<quads.length;n+=6){
    const [code,plane,u0,v0,u1,v1]=quads.subarray(n,n+6),axis=(code&7)>>1;
    if(axis===0){
     if(plane<cut||(plane===cut&&(code&1)===0))faces.push(code,plane,u0,v0,u1,v1);
     if(plane>=cut){
      // First x-facing skin east of the cut on each half-cell row. An outward
      // face closes a cut solid; an inward face begins a separate solid.
      for(let z=u0;z<u1;z++)for(let y=v0;y<v1;y++){
       const cell=z*header.dims[1]+y,hit=cap.get(cell);
       if(!hit||plane<hit.plane)cap.set(cell,{plane,code,z,y});
      }
     }
     trimmed||=plane>cut;
    }else if(u0<cut){faces.push(code,plane,u0,v0,Math.min(cut,u1),v1);trimmed||=u1>cut;}
    else trimmed=true;
   }
   for(const {plane,code,z,y} of cap.values()){
    if(plane>cut&&(code&1)===0)faces.push(code,cut,z,y,z+1,y+1);
   }
   groups.set(key,faces);
  }
  assert.equal(offset,data.length);assert.ok(trimmed);
  const output=encodeBuild(header,groups);
  writeFileSync(join(dir,site.file),output);site.bytes=output.length;
  site.quads=[...groups.values()].reduce((sum,q)=>sum+q.length/6,0);
  site.displayCut={feature,sourceSha256:sha,eastGridPlane:cut,
   note:'Plan 15 comparison. Terminal block faces trimmed at display export. The exposed end takes its material and light from the saved faces of the cut branch.'};
 }
}
writeFileSync(join(dir,'index.json'),JSON.stringify(index,null,1)+'\n');
