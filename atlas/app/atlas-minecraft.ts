import * as T from 'three';
import {siteStyle} from './atlas-site-materials';
import type {ModelGeometry} from './atlas-model-geometry';

// Site models built in a Minecraft Java Edition server and read back from its saved
// world (scripts/minecraft/build-world.mjs). The files hold block faces and the sky
// light Minecraft computed for them; nothing else from the game is used. Block
// textures below are original pixel art in each site's photo-derived colours.
type Header={version:number;id:string;size:number;half:number;origin:[number,number,number];dims:[number,number,number];materials:string[];masonry:string;features:string[];groups:{material:number;feature:number;quads:number}[]};
export type MinecraftBuild={header:Header;groups:{material:number;feature:number;quads:Uint16Array}[];edition:string;version:string|null;mismatches:number|null;rings?:MinecraftBuild[]};
type Index={minecraft:{edition:string;version:string|null};sites:Record<string,{file:string|null;terrainPlace?:string|null;readback?:{mismatches:number};surroundings?:string[]|null}>};

const base=()=>(import.meta as ImportMeta&{env?:{BASE_URL?:string}}).env?.BASE_URL??'/';
let index:Promise<Index|null>|undefined;
export function minecraftIndex(){return index??=fetch(`${base()}minecraft/index.json`).then(r=>r.ok?r.json() as Promise<Index>:null).catch(()=>null);}

// A traced plan's reconstruction layers are separate builds, keyed `<plan>@<layer>`.
export const buildKey=(planId:string,layer?:string)=>layer&&layer!=='remains'?`${planId}@${layer}`:planId;
export async function loadMinecraftBuild(planId:string,placeId:string,layer?:string):Promise<MinecraftBuild|null>{
 const list=await minecraftIndex(),site=list?.sites[buildKey(planId,layer)];if(!site?.file||(site.terrainPlace&&site.terrainPlace!==placeId))return null;
 const build=await loadBuildFile(site.file,list!,site.readback?.mismatches??null);
 // Coarser terrain rings around a plan with the wide terrain patch.
 if(build&&site.surroundings?.length)build.rings=(await Promise.all(site.surroundings.map(key=>{const ring=list!.sites[key];return ring?.file?loadBuildFile(ring.file,list!,ring.readback?.mismatches??null):null;}))).filter((b):b is MinecraftBuild=>!!b);
 return build;
}
async function loadBuildFile(file:string,list:Index,mismatches:number|null):Promise<MinecraftBuild|null>{
 const response=await fetch(`${base()}minecraft/${file}`);if(!response.ok)return null;
 let bytes=new Uint8Array(await response.arrayBuffer());
 // A host may already have removed the gzip layer through Content-Encoding.
 if(bytes[0]===0x1f&&bytes[1]===0x8b)bytes=new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
 const buffer=bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),length=new DataView(buffer).getUint32(0,true);
 const header=JSON.parse(new TextDecoder().decode(new Uint8Array(buffer,4,length))) as Header;let offset=4+length;
 const groups=header.groups.map(g=>{const quads=new Uint16Array(buffer,offset,g.quads*6);offset+=g.quads*12;return {material:g.material,feature:g.feature,quads};});
 return {header,groups,edition:list.minecraft.edition,version:list.minecraft.version,mismatches};
}

// Wider modern terrain for a place (atlas/public/terrain), decoded to the landscape patch shape.
type WideTerrain={lat:number;lon:number;extent:number;size:number;centreElevation:number;data:string};
export async function loadTerrainPatch(placeId:string){
 const response=await fetch(`${base()}terrain/${placeId}.json`);if(!response.ok)return null;
 const t=await response.json() as WideTerrain,bytes=Uint8Array.from(atob(t.data),c=>c.charCodeAt(0)),view=new DataView(bytes.buffer),elevations=new Array<number>(t.size*t.size);
 for(let i=0;i<elevations.length;i++)elevations[i]=t.centreElevation+view.getInt16(i*2,true)/10;
 return {lat:t.lat,lon:t.lon,anchorPrecision:'wide patch',extent:t.extent,size:t.size,elevations,centreElevation:t.centreElevation};
}

// Minecraft-style brightness for sky light 0–15, with a floor of 40 % so the walls of caves,
// chambers and tunnels keep their detail; the light still falls off into them.
export const skyBrightness=(level:number)=>{const f=level/15;return .4+.6*f/(4-3*f);};

function random(seed:number){let n=seed>>>0;return ()=>{n=(Math.imul(n,1664525)+1013904223)>>>0;return n/4294967296;};}
// One 16 × 16 tile per block face. The mean colour is the site's photo-derived base.
function pixelTexture(material:number,planId:string,masonry:string){
 const style=siteStyle(planId),n=16,tone=new Float32Array(n*n),rand=random(material*977+planId.length*31);
 // Codes 8–11 are the modern setting of a registered site: leaves, wood, green ground and asphalt.
 const setting:Record<number,string>={8:'#6f7a4c',9:'#6b5a43',10:'#8a8a5c',11:'#5d5b56'};
 const colour=material===7?new T.Color(style.stone).lerp(new T.Color('#f4efe3'),.62):new T.Color(setting[material]??(material===1?style.soil:material===2?style.rock:material===5?style.plaster:material===6?'#b56b42':style.stone));
 for(let i=0;i<n*n;i++)tone[i]=1+(rand()-.5)*(material===5||material===7?.05:material===3?.07:material===8?.34:material===11?.06:.16);
 const set=(x:number,y:number,f:number)=>{tone[((y+n)%n)*n+(x+n)%n]*=f;};
 if(material===1){for(let k=0;k<9;k++){const x=Math.floor(rand()*n),y=Math.floor(rand()*n),f=rand()<.5?.78:1.18;set(x,y,f);set(x+1,y,f);}}
 else if(material===9){for(let x=0;x<n;x+=3)for(let y=0;y<n;y++)set(x,y,.82);}
 else if(material===2){for(let y=0;y<n;y+=5+Math.floor(rand()*2))for(let x=0;x<n;x++)if(rand()<.8)set(x,y+Math.round(Math.sin(x*.7)*.6),.86);}
 else if(material===3){for(let k=0;k<n;k++){set(k,0,.93);set(0,k,.93);set(k,n-1,.9);set(n-1,k,.9);}}
 // Restored (drawn only by a published reconstruction): pale, with a dashed outline.
 else if(material===7){for(let k=0;k<n;k++)if(k%4<2){set(k,0,.78);set(0,k,.78);}}
 else if(material===6){for(let y=0;y<n;y++)for(let x=0;x<n;x++){const a=x%8,b=y%8;if(a===0||b===0)set(x,y,1.12);if(a===7||b===7)set(x,y,.82);}}
 else if(material===4){
  if(masonry==='rubble'){
   // Irregular fieldstones: nearest-seed cells with dark joints between them.
   const seeds=Array.from({length:7},()=>[rand()*n,rand()*n,.84+rand()*.3]);
   for(let y=0;y<n;y++)for(let x=0;x<n;x++){
    let first=99,second=99,owner=0;
    seeds.forEach(([sx,sy],i)=>{for(const [ox,oy] of [[0,0],[n,0],[-n,0],[0,n],[0,-n]]){const d=Math.hypot(x+.5-sx-ox,y+.5-sy-oy);if(d<first){second=first;first=d;owner=i;}else if(d<second)second=d;}});
    set(x,y,seeds[owner][2]*(second-first<1.1?.68:1));
   }
  }else{
   const rows=masonry==='ashlar'?1:masonry==='mudbrick'?4:2,width=masonry==='ashlar'?16:masonry==='mudbrick'?8:16,h=n/rows;
   for(let r=0;r<rows;r++){const shift=(r%2)*width/2,block=.9+rand()*.2;for(let y=r*h;y<(r+1)*h;y++)for(let x=0;x<n;x++){const joint=y===r*h||(x+shift)%width===0;set(x,y,joint?.74:block);}}
  }
 }
 const data=new Uint8Array(n*n*4);let mean=0;for(const t of tone)mean+=t/(n*n);
 const srgb=colour.clone().convertLinearToSRGB();
 for(let i=0;i<n*n;i++){const f=tone[i]/mean;data.set([Math.min(255,srgb.r*255*f),Math.min(255,srgb.g*255*f),Math.min(255,srgb.b*255*f),255],i*4);}
 const texture=new T.DataTexture(data,n,n);texture.colorSpace=T.SRGBColorSpace;texture.wrapS=texture.wrapT=T.RepeatWrapping;
 texture.magFilter=T.NearestFilter;texture.minFilter=T.NearestMipmapLinearFilter;texture.generateMipmaps=true;texture.needsUpdate=true;
 return texture;
}

export function minecraftMeshes(build:MinecraftBuild,planId:string){
 const {size:s,half:h,origin:[x0,y0,z0],dims:[nx,,nz],masonry,features}=build.header,group=new T.Group(),textures=new Map<number,T.Texture>();
 const c=[0,0,0],corner=(axis:number,plane:number,ua:number,va:number,u:number,v:number)=>{c[axis]=plane;c[ua]=u;c[va]=v;return [x0+c[0]*s,y0+c[1]*h,z0+c[2]*s,c[0],c[1],c[2]];};
 for(const g of build.groups){
  const count=g.quads.length/6,position=new Float32Array(count*12),normal=new Float32Array(count*12),uv=new Float32Array(count*8),colour=new Float32Array(count*12),index=new Uint32Array(count*6);
  for(let q=0;q<count;q++){
   const o=q*6,dir=g.quads[o]&7,light=g.quads[o]>>3,plane=g.quads[o+1],u0=g.quads[o+2],v0=g.quads[o+3],u1=g.quads[o+4],v1=g.quads[o+5];
   const axis=dir>>1,sign=dir&1?-1:1,[ua,va]=axis===0?[2,1]:axis===1?[0,2]:[0,1];
   let corners=[[u0,v0],[u1,v0],[u1,v1],[u0,v1]].map(([u,v])=>corner(axis,plane,ua,va,u,v));
   // Wind each face so that it looks outward along its direction.
   const a=corners[0],b=corners[1],d=corners[3],cross=[(b[1]-a[1])*(d[2]-a[2])-(b[2]-a[2])*(d[1]-a[1]),(b[2]-a[2])*(d[0]-a[0])-(b[0]-a[0])*(d[2]-a[2]),(b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])];
   if(cross[axis]*sign<0)corners=[corners[0],corners[3],corners[2],corners[1]];
   const shade=skyBrightness(light);
   corners.forEach((p,k)=>{
    position.set([p[0],p[1],p[2]],q*12+k*3);const nrm=[0,0,0];nrm[axis]=sign;normal.set(nrm,q*12+k*3);colour.set([shade,shade,shade],q*12+k*3);
    // Texture coordinates in blocks: one tile per block, half a tile on a slab's side.
    uv.set(axis===0?[p[5],p[4]/2]:axis===1?[p[3],p[5]]:[p[3],p[4]/2],q*8+k*2);
   });
   index.set([q*4,q*4+1,q*4+2,q*4,q*4+2,q*4+3],q*6);
  }
  const geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.BufferAttribute(position,3));geometry.setAttribute('normal',new T.BufferAttribute(normal,3));geometry.setAttribute('uv',new T.BufferAttribute(uv,2));geometry.setAttribute('color',new T.BufferAttribute(colour,3));geometry.setIndex(new T.BufferAttribute(index,1));geometry.computeBoundingSphere();
  let map=textures.get(g.material);if(!map){map=pixelTexture(g.material,planId,masonry);textures.set(g.material,map);}
  const material=new T.MeshStandardMaterial({map,vertexColors:true,roughness:1,metalness:0});material.name=`${planId}-minecraft-${build.header.materials[g.material]}`;
  const mesh=new T.Mesh(geometry,material);mesh.castShadow=mesh.receiveShadow=true;mesh.userData.walkSurface=true;mesh.userData.minecraft=true;
  if(g.feature)mesh.userData.featureId=features[g.feature-1];
  group.add(mesh);
 }
 return {group,domain:{minX:x0,maxX:x0+nx*s,minZ:z0,maxZ:z0+nz*s}};
}

const PILOT_GROUND=new Set(['qumran-ground','qumran-ridge-back','connected-limestone-bed']);
// Replace the model's architecture with the blocks. Outside the block area the smooth
// terrain and its scattered stones stay, so the view keeps its landscape context.
export function applyMinecraftBuild(model:ModelGeometry,build:MinecraftBuild,planId:string){
 const near=minecraftMeshes(build,planId),rings=(build.rings??[]).map(ring=>minecraftMeshes(ring,planId)),group=near.group;
 for(const ring of rings){ring.group.children.forEach(m=>m.userData.minecraftRing=true);group.add(...ring.group.children);}
 // The smooth terrain stays only outside the outermost block area.
 const domain=[near,...rings].reduce((a,b)=>({minX:Math.min(a.minX,b.domain.minX),maxX:Math.max(a.maxX,b.domain.maxX),minZ:Math.min(a.minZ,b.domain.minZ),maxZ:Math.max(a.maxZ,b.domain.maxZ)}),near.domain);
 const root=model.root,inside=(x:number,z:number)=>x>domain.minX&&x<domain.maxX&&z>domain.minZ&&z<domain.maxZ;
 root.updateMatrixWorld(true);const p=new T.Vector3(),m=new T.Matrix4(),hidden=new T.Matrix4().makeScale(0,0,0),remove:T.Object3D[]=[];
 for(const child of root.children){
  const ground=child.userData.siteContext==='ground'||PILOT_GROUND.has(child.name);
  if(ground&&child instanceof T.Mesh){
   const position=child.geometry.getAttribute('position'),old=child.geometry.getIndex(),kept:number[]=[];
   for(let t=0;t<(old?.count??position.count);t+=3){
    const ids=[0,1,2].map(k=>old?old.getX(t+k):t+k);let x=0,z=0;for(const id of ids){p.fromBufferAttribute(position,id).applyMatrix4(child.matrixWorld);x+=p.x/3;z+=p.z/3;}
    if(!inside(x,z))kept.push(...ids);
   }
   child.geometry.setIndex(kept);continue;
  }
  const details=child.userData.siteContext==='details'?child.children:child instanceof T.InstancedMesh&&child.userData.walkDetail?[child]:null;
  if(details){for(const mesh of details)if(mesh instanceof T.InstancedMesh){for(let i=0;i<mesh.count;i++){mesh.getMatrixAt(i,m);p.setFromMatrixPosition(m).applyMatrix4(mesh.matrixWorld);if(inside(p.x,p.z))mesh.setMatrixAt(i,hidden);}mesh.instanceMatrix.needsUpdate=true;}continue;}
  remove.push(child);
 }
 for(const child of remove){root.remove(child);child.traverse(o=>{const mesh=o as T.Mesh;mesh.geometry?.dispose();});}
 // The blocks are in the source model's world frame; the root carries the centring offset.
 group.position.copy(root.position).negate();group.name='minecraft-build';root.add(group);
 model.selectable.length=0;group.children.forEach(mesh=>{if(mesh.userData.featureId)model.selectable.push(mesh);});
 model.note=`Minecraft build · ${model.note}`;
 model.assumptions.unshift(`Minecraft build: this source model was converted to blocks of ${build.header.size} ${model.units==='metres'?'m':'model units'} (half blocks ${build.header.half}), placed by a Minecraft ${build.edition} ${build.version??''} server, saved, and read back from the world’s region files${build.mismatches===0?' with every block as placed':''}. Each face is shaded by the sky light Minecraft computed for it, so covered tunnels, cisterns and caves are darker. Rounding to the block size can move an edge or a height by up to half a block; the blocks add no detail to the source model. Block textures are original pixel art in the site’s photo-derived colours, not the game’s textures. Outside the block area the smooth terrain is shown.${build.rings?.length?` Around the site, modern terrain is built in coarser blocks (${build.rings.map(r=>`${r.header.size} m`).join(', then ')}) out to the edge of the wider elevation patch; it is today's ground, not the ancient surface.`:''}`);
 return model;
}
