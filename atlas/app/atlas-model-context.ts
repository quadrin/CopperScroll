import * as T from "three";
import contextData from "./atlas-site-context.json";
import { cloneSiteMaterial } from './atlas-site-materials';

// Modern surroundings of a site from OpenStreetMap (tools/build_osm_context.py): today's paths,
// stairs, roads, cemeteries, walls, buildings, trees and green ground, projected to the place frame
// (metres, x east, z south). They give the model its setting and are never archaeological evidence.
type Point=[number,number];
export type ContextFeature={id:string;kind:'steps'|'path'|'road'|'wall'|'retaining-wall'|'cemetery'|'gate'|'building'|'green'|'tree';pts:Point[];road?:string;cover?:'wood'|'orchard'|'grass';leafType?:string;name?:string;width?:number;height?:number;incline?:string;religion?:string;area?:boolean;minHeight?:number;roofShape?:'dome'|'pyramidal';roofHeight?:number;roofColour?:string;part?:boolean};
export type SiteContext={place:string;retrieved:string;record:string;registration:Record<string,unknown>|null;features:ContextFeature[]};
const data=contextData as unknown as {licence:string;plans:Record<string,SiteContext>};
export const siteContext=(planId:string):SiteContext|undefined=>data.plans[planId];
export const CONTEXT_LICENCE=data.licence;

// Illustrative sizes where OSM gives none.
const WIDTH={path:2.4,steps:2.2},ROAD_WIDTH:Record<string,number>={motorway:12,trunk:10,primary:9,secondary:8,tertiary:7,unclassified:5.5,residential:5.5,living_street:4.5,service:3.5},WALL={wall:{thickness:2.6,height:12},'retaining-wall':{thickness:.8,height:1.2}},GATE_HEIGHT=9,BUILDING_HEIGHT=6.5;
// Plain surfaces for the setting; `siteSurface` names the block each becomes in the block export.
const plain=(colour:string,surface:string)=>{const m=new T.MeshStandardMaterial({color:colour,roughness:.95,metalness:0});m.userData.siteSurface=surface;return m;};
// Graves: about 1 × 2 m, in rows 1.45 m apart and 2.9 m from head to head. Long axes run
// east–west, or across the qibla (157°) in a Muslim cemetery. Illustrative, not mapped graves.
// No grave is set where the ground under it falls more than 1.2 m (a slope of about 30°).
const GRAVE={across:1.45,along:2.9,width:1,length:2.05,height:.45,steepest:1.2,bearing:{muslim:67,other:90}};
// Trees: mapped single trees, and trees set about 7 m apart in mapped woods (pines) and orchards
// (olives). Sizes are illustrative: olives with a 1.6 m trunk and a crown about 5 m across, pines
// with a 5 m trunk and a crown 4.5 m high.
const TREE={olive:{trunk:1.6,crown:[2.6,2.4],colour:'#8a9068'},pine:{trunk:5,crown:[2.3,4.5],colour:'#56613f'}},PLANTED={wood:{spacing:7,fill:.8},orchard:{spacing:7,fill:.9}};
// How strongly green ground tints the terrain.
const GREEN={wood:.9,orchard:.75,grass:.6};

function segmentDistance(x:number,z:number,a:Point,b:Point){
 const dx=b[0]-a[0],dz=b[1]-a[1],t=T.MathUtils.clamp(((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz||1),0,1);
 return Math.hypot(x-a[0]-t*dx,z-a[1]-t*dz);
}
function inside(x:number,z:number,points:Point[]){let hit=false;for(let i=0,j=points.length-1;i<points.length;j=i++){const [a,b]=points[i],[c,d]=points[j];if((b>z)!==(d>z)&&x<(c-a)*(z-b)/(d-b)+a)hit=!hit;}return hit;}

// Line features in 16 m buckets: which one, if any, covers a point (with an extra margin).
function lineIndex(features:ContextFeature[],kinds:ContextFeature['kind'][],halfWidth:(f:ContextFeature)=>number){
 const size=16,buckets=new Map<number,{a:Point;b:Point;r:number;kind:ContextFeature['kind']}[]>(),key=(i:number,k:number)=>(i+4096)*8192+k+4096;
 for(const f of features){
  if(!kinds.includes(f.kind))continue;const r=halfWidth(f);
  for(let n=0;n+1<f.pts.length;n++){
   const a=f.pts[n],b=f.pts[n+1],segment={a,b,r,kind:f.kind};
   for(let i=Math.floor((Math.min(a[0],b[0])-r-4)/size);i<=Math.floor((Math.max(a[0],b[0])+r+4)/size);i++)
    for(let k=Math.floor((Math.min(a[1],b[1])-r-4)/size);k<=Math.floor((Math.max(a[1],b[1])+r+4)/size);k++){const list=buckets.get(key(i,k));if(list)list.push(segment);else buckets.set(key(i,k),[segment]);}
  }
 }
 return (x:number,z:number,margin=0)=>{for(const s of buckets.get(key(Math.floor(x/size),Math.floor(z/size)))??[])if(segmentDistance(x,z,s.a,s.b)<=s.r+margin)return s.kind;return null;};
}
const lineWidth=(f:ContextFeature)=>(f.width??(f.kind==='road'?ROAD_WIDTH[f.road??'']??5.5:WIDTH[f.kind as 'path'|'steps'])??2)/2;
const greens=(features:ContextFeature[])=>features.filter(f=>f.kind==='green'&&f.cover&&f.pts.length>3).map(f=>({cover:f.cover!,pts:ring(f.pts)}));

// The block a column's top takes under a mapped path (paving), stair, road (asphalt) or green
// ground (grass), for the block export.
export function pavedIndex(features:ContextFeature[]){
 const at=lineIndex(features.filter(f=>!f.area),['path','steps','road'],lineWidth),green=polygonIndex(greens(features).map(g=>g.pts));
 return (x:number,z:number)=>{const kind=at(x,z);return kind==='steps'?'limestone':kind==='road'?'asphalt':kind?'masonry':green(x,z)?'grass':null;};
}
// How strongly the terrain at a point is tinted green (0 to 1).
export function greenIndex(features:ContextFeature[]){
 const at=bucketed(greens(features));
 return (x:number,z:number)=>{let best=0;for(const a of at(x,z))if(GREEN[a.cover]>best&&inside(x,z,a.pts))best=GREEN[a.cover];return best;};
}

function resample(points:Point[],step:number){
 const out:Point[]=[];
 for(let i=0;i+1<points.length;i++){const a=points[i],b=points[i+1],n=Math.max(1,Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/step));for(let k=0;k<n;k++)out.push([a[0]+(b[0]-a[0])*k/n,a[1]+(b[1]-a[1])*k/n]);}
 out.push(points[points.length-1]);return out;
}
function sideways(samples:Point[],k:number,half:number):Point{
 const a=samples[Math.max(0,k-1)],b=samples[Math.min(samples.length-1,k+1)],dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz)||1;
 return [-dz/l*half,dx/l*half];
}
const ring=(pts:Point[])=>pts.length>1&&pts[0][0]===pts[pts.length-1][0]&&pts[0][1]===pts[pts.length-1][1]?pts.slice(0,-1):pts;
// Areas in 16 m buckets: the areas whose bounding boxes reach a point's bucket.
function bucketed<A extends {pts:Point[]}>(areas:A[]){
 const size=16,buckets=new Map<number,A[]>(),key=(i:number,k:number)=>(i+4096)*8192+k+4096;
 for(const a of areas){const xs=a.pts.map(q=>q[0]),zs=a.pts.map(q=>q[1]);for(let i=Math.floor(Math.min(...xs)/size);i<=Math.floor(Math.max(...xs)/size);i++)for(let k=Math.floor(Math.min(...zs)/size);k<=Math.floor(Math.max(...zs)/size);k++){const list=buckets.get(key(i,k));if(list)list.push(a);else buckets.set(key(i,k),[a]);}}
 return (x:number,z:number)=>buckets.get(key(Math.floor(x/size),Math.floor(z/size)))??[];
}
// Whether a point is inside any of the polygons (building footprints, green areas).
function polygonIndex(polygons:Point[][]){const at=bucketed(polygons.map(pts=>({pts})));return (x:number,z:number)=>at(x,z).some(a=>inside(x,z,a.pts));}
function geometry(positions:number[],indices:number[]){const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();return g;}

export type ContextMaterials={paving:T.MeshStandardMaterial;stair:T.MeshStandardMaterial;wall:T.MeshStandardMaterial;grave:T.MeshStandardMaterial};
// `surface` is the drawn terrain's height; `keepOut` marks ground the model itself occupies and `open`
// the terrain's holes (pools, shafts, the model's rock), where no path, stair or wall is draped.
export type ContextArea={keepOut:(x:number,z:number)=>boolean;open:(x:number,z:number)=>boolean;within:(x:number,z:number)=>boolean};
export function buildSiteContext(features:ContextFeature[],surface:(x:number,z:number)=>number,materials:ContextMaterials,{keepOut,open,within}:ContextArea){
 const group=new T.Group();group.name='site-context';group.userData.siteContext='osm';
 const lift=.05,offset=(m:T.MeshStandardMaterial,units=-2)=>{const c=m.userData.siteStyle?cloneSiteMaterial(m):m;c.polygonOffset=true;c.polygonOffsetFactor=units;c.polygonOffsetUnits=units;return c;};
 // Paths and roads: ribbons draped on the terrain. They are walked on through the terrain under them;
 // paths draw over roads where they meet.
 const ribbon=(kind:'path'|'road',material:T.MeshStandardMaterial,units:number)=>{
  const positions:number[]=[],indices:number[]=[];
  for(const f of features){
   if(f.kind!==kind||f.area||!f.pts.some(([x,z])=>within(x,z)))continue;
   const samples=resample(f.pts,2),half=lineWidth(f),start=positions.length/3;
   samples.forEach((p,k)=>{const [sx,sz]=sideways(samples,k,half);for(const s of [-1,1]){const x=p[0]+s*sx,z=p[1]+s*sz;positions.push(x,surface(x,z)+lift,z);}});
   // A span is left out over a hole, or where the ground under it is steeper than 45° (a cliff that
   // the terrain model smooths, not a slope a path climbs).
   const y=(n:number)=>positions[n*3+1],steep=(a:number,b:number)=>Math.abs(y(a)-y(b))>Math.hypot(positions[a*3]-positions[b*3],positions[a*3+2]-positions[b*3+2]);
   for(let k=0;k+1<samples.length;k++){const a=start+2*k;if(open(...samples[k])||open(...samples[k+1])||steep(a,a+2)||steep(a+1,a+3)||steep(a,a+1))continue;indices.push(a,a+1,a+2,a+1,a+3,a+2);}
  }
  const mesh=new T.Mesh(geometry(positions,indices),offset(material,units));mesh.material.side=T.DoubleSide;mesh.receiveShadow=true;mesh.userData.walkCollision=false;mesh.name=`context-${kind}s`;group.add(mesh);
 };
 ribbon('road',plain('#5d5b56','asphalt'),-1);ribbon('path',materials.paving,-2);
 // Stairs: 0.4 m treads, each level with the higher end of the ground under it, and risers between.
 {const positions:number[]=[],indices:number[]=[];
  const quad=(a:T.Vector3,b:T.Vector3,c:T.Vector3,d:T.Vector3)=>{const n=positions.length/3;positions.push(a.x,a.y,a.z,b.x,b.y,b.z,c.x,c.y,c.z,d.x,d.y,d.z);indices.push(n,n+1,n+2,n,n+2,n+3);};
  for(const f of features){
   if(f.kind!=='steps'||!f.pts.some(([x,z])=>within(x,z)))continue;
   const samples=resample(f.pts,.4),half=lineWidth(f);
   const level=samples.map((p,k)=>{const [sx,sz]=sideways(samples,k,half);return Math.max(surface(p[0]+sx,p[1]+sz),surface(p[0]-sx,p[1]-sz),surface(p[0],p[1]));});
   for(let k=0;k+1<samples.length;k++){
    if(open(...samples[k])||open(...samples[k+1]))continue;
    const y=Math.max(level[k],level[k+1])+lift,[ax,az]=sideways(samples,k,half),[bx,bz]=sideways(samples,k+1,half),p=samples[k],q=samples[k+1];
    const a=new T.Vector3(p[0]-ax,y,p[1]-az),b=new T.Vector3(p[0]+ax,y,p[1]+az),c=new T.Vector3(q[0]+bx,y,q[1]+bz),d=new T.Vector3(q[0]-bx,y,q[1]-bz);
    quad(a,b,c,d);
    // Riser at the lower end of the tread, down to the ground.
    const low=Math.min(level[k],level[k+1])-.1,end=level[k]<level[k+1]?[a,b]:[d,c];
    quad(end[0],end[1],new T.Vector3(end[1].x,low,end[1].z),new T.Vector3(end[0].x,low,end[0].z));
   }
  }
  const stairs=new T.Mesh(geometry(positions,indices),offset(materials.stair));stairs.material.side=T.DoubleSide;stairs.castShadow=stairs.receiveShadow=true;stairs.userData.contextFine=true;stairs.name='context-stairs';group.add(stairs);}
 // Walls: one box per stretch of up to 6 m, so the base follows the ground.
 const wallBoxes:{x:number;z:number;angle:number;length:number;thickness:number;y0:number;y1:number}[]=[];
 for(const f of features){
  if(f.kind!=='wall'&&f.kind!=='retaining-wall')continue;const spec=WALL[f.kind];
  const samples=resample(f.pts,6);
  for(let k=0;k+1<samples.length;k++){
   const a=samples[k],b=samples[k+1],x=(a[0]+b[0])/2,z=(a[1]+b[1])/2,dx=b[0]-a[0],dz=b[1]-a[1],length=Math.hypot(dx,dz);if(length<.05||!within(x,z)||open(x,z))continue;
   const nx=-dz/length,nz=dx/length,side=spec.thickness/2+3,heights=[surface(a[0],a[1]),surface(b[0],b[1]),surface(x+nx*side,z+nz*side),surface(x-nx*side,z-nz*side)],lo=Math.min(...heights),hi=Math.max(...heights);
   // A city wall stands its height above the lower ground; a retaining wall rises just above the higher.
   const y1=f.kind==='wall'?Math.max(lo+(f.height??spec.height),hi+1.5):Math.max(hi+.6,lo+(f.height??spec.height));
   wallBoxes.push({x,z,angle:Math.atan2(-dz,dx),length:length+spec.thickness*.5,thickness:spec.thickness,y0:lo-1,y1});
  }
 }
 if(wallBoxes.length){
  const walls=new T.InstancedMesh(new T.BoxGeometry(1,1,1),cloneSiteMaterial(materials.wall),wallBoxes.length),o=new T.Object3D();
  wallBoxes.forEach((w,i)=>{o.position.set(w.x,(w.y0+w.y1)/2,w.z);o.rotation.set(0,w.angle,0);o.scale.set(w.length,w.y1-w.y0,w.thickness);o.updateMatrix();walls.setMatrixAt(i,o.matrix);});
  walls.castShadow=walls.receiveShadow=true;walls.name='context-walls';group.add(walls);
 }
 // Gate buildings: their mapped footprints, raised above the highest ground under them.
 const gates=features.filter(f=>f.kind==='gate'&&f.pts.length>3&&f.pts.some(([x,z])=>within(x,z)));
 for(const f of gates){
  const pts=f.pts[0][0]===f.pts[f.pts.length-1][0]&&f.pts[0][1]===f.pts[f.pts.length-1][1]?f.pts.slice(0,-1):f.pts;
  const heights=pts.map(([x,z])=>surface(x,z)),lo=Math.min(...heights)-1,hi=Math.max(...heights)+(f.height??GATE_HEIGHT);
  const shape=new T.Shape();pts.forEach(([x,z],i)=>i?shape.lineTo(x,-z):shape.moveTo(x,-z));shape.closePath();
  const g=new T.ExtrudeGeometry(shape,{depth:hi-lo,bevelEnabled:false});g.rotateX(-Math.PI/2);g.translate(0,lo,0);
  const m=new T.Mesh(g,cloneSiteMaterial(materials.wall));m.castShadow=m.receiveShadow=true;m.name=`context-gate-${f.id}`;group.add(m);
 }
 // Buildings: walls from the lowest ground under them to the mapped height (or 6.5 m), a flat roof,
 // and a dome or pyramid where OSM maps one. Footprints on the model itself are left out.
 const buildings=features.filter(f=>f.kind==='building'&&f.pts.length>3).map(f=>({f,pts:ring(f.pts)})).filter(({pts})=>{const cx=pts.reduce((a,p)=>a+p[0],0)/pts.length,cz=pts.reduce((a,p)=>a+p[1],0)/pts.length;return within(cx,cz)&&!keepOut(cx,cz);});
 {const positions:number[]=[],indices:number[]=[],v=(x:number,y:number,z:number)=>{positions.push(x,y,z);return positions.length/3-1;};
  for(const {f,pts} of buildings){
   const ground=pts.map(([x,z])=>surface(x,z)),lo=Math.min(...ground),top=lo+(f.height??BUILDING_HEIGHT),roof=f.roofShape?Math.min(f.roofHeight??0,top-lo-1):0,eaves=top-roof,bottom=f.minHeight?lo+f.minHeight:lo-1;
   if(eaves<=bottom+.5)continue;
   for(let i=0;i<pts.length;i++){const a=pts[i],b=pts[(i+1)%pts.length],n=[v(a[0],bottom,a[1]),v(b[0],bottom,b[1]),v(b[0],eaves,b[1]),v(a[0],eaves,a[1])];indices.push(n[0],n[1],n[2],n[0],n[2],n[3]);}
   const cap=pts.map(([x,z])=>v(x,eaves,z));for(const [a,b,c] of T.ShapeUtils.triangulateShape(pts.map(([x,z])=>new T.Vector2(x,z)),[]))indices.push(cap[a],cap[c],cap[b]);
   if(roof>0){
    const cx=pts.reduce((a,p)=>a+p[0],0)/pts.length,cz=pts.reduce((a,p)=>a+p[1],0)/pts.length,r=pts.reduce((a,p)=>a+Math.hypot(p[0]-cx,p[1]-cz),0)/pts.length;
    const g=f.roofShape==='dome'?new T.SphereGeometry(r,28,10,0,Math.PI*2,0,Math.PI/2).scale(1,roof/r,1):new T.CylinderGeometry(.02,r,roof,Math.max(4,pts.length),1).translate(0,roof/2,0);
    const m=new T.Mesh(g,cloneSiteMaterial(materials.wall));if(f.roofColour)m.material.color.set(f.roofColour);m.position.set(cx,eaves,cz);m.castShadow=m.receiveShadow=true;m.name=`context-roof-${f.id}`;group.add(m);
   }
  }
  if(indices.length){const mesh=new T.Mesh(geometry(positions,indices),cloneSiteMaterial(materials.wall));mesh.material.side=T.DoubleSide;mesh.castShadow=mesh.receiveShadow=true;mesh.name='context-buildings';group.add(mesh);}
 }
 const built=polygonIndex(buildings.map(b=>b.pts));
 // Graves on one lattice per orientation, so overlapping cemetery plots do not double them.
 const clear=lineIndex(features.filter(f=>!f.area),['path','steps','road','wall','retaining-wall'],f=>f.kind==='wall'||f.kind==='retaining-wall'?WALL[f.kind].thickness/2:lineWidth(f));
 const placed=new Set<string>(),graves:{x:number;z:number;angle:number;w:number;l:number;y0:number;y1:number}[]=[];
 let seed=90173;const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
 for(const f of features){
  if(f.kind!=='cemetery'||f.pts.length<4)continue;
  const bearing=f.religion==='muslim'?GRAVE.bearing.muslim:GRAVE.bearing.other,th=T.MathUtils.degToRad(bearing),u:Point=[Math.sin(th),-Math.cos(th)],v:Point=[-u[1],u[0]];
  const xs=f.pts.map(p=>p[0]),zs=f.pts.map(p=>p[1]),corners:Point[]=[[Math.min(...xs),Math.min(...zs)],[Math.max(...xs),Math.min(...zs)],[Math.min(...xs),Math.max(...zs)],[Math.max(...xs),Math.max(...zs)]];
  const along=corners.map(([x,z])=>(x*u[0]+z*u[1])/GRAVE.along),across=corners.map(([x,z])=>(x*v[0]+z*v[1])/GRAVE.across);
  for(let i=Math.floor(Math.min(...along));i<=Math.ceil(Math.max(...along));i++)for(let j=Math.floor(Math.min(...across));j<=Math.ceil(Math.max(...across));j++){
   const key=`${bearing}:${i}:${j}`;if(placed.has(key))continue;
   const x=i*GRAVE.along*u[0]+j*GRAVE.across*v[0],z=i*GRAVE.along*u[1]+j*GRAVE.across*v[1];
   if(!within(x,z)||!inside(x,z,f.pts))continue;placed.add(key);
   const r=random();if(r<.12||keepOut(x,z)||clear(x,z,1.6)||built(x,z))continue;
   const angle=Math.PI/2-th+(random()-.5)*.08,w=GRAVE.width*(.9+random()*.2),l=GRAVE.length*(.92+random()*.14),jx=(random()-.5)*.3,jz=(random()-.5)*.3;
   const ends=[-1,1].flatMap(s=>[-1,1].map(t=>surface(x+jx+s*u[0]*l/2+t*v[0]*w/2,z+jz+s*u[1]*l/2+t*v[1]*w/2))),lo=Math.min(...ends),hi=Math.max(...ends);
   if(hi-lo>GRAVE.steepest)continue;
   graves.push({x:x+jx,z:z+jz,angle,w,l,y0:lo-.15,y1:hi+GRAVE.height*(.8+random()*.5)});
  }
 }
 if(graves.length){
  const mesh=new T.InstancedMesh(new T.BoxGeometry(1,1,1),cloneSiteMaterial(materials.grave),graves.length),o=new T.Object3D();
  graves.forEach((g,i)=>{o.position.set(g.x,(g.y0+g.y1)/2,g.z);o.rotation.set(0,g.angle,0);o.scale.set(g.l,g.y1-g.y0,g.w);o.updateMatrix();mesh.setMatrixAt(i,o.matrix);mesh.setColorAt(i,new T.Color().setScalar(.9+random()*.16));});
  mesh.receiveShadow=true;mesh.castShadow=false;mesh.name='context-graves';group.add(mesh);
 }
 // Trees: mapped single trees, and planted trees on a jittered 7 m grid in woods and orchards.
 const trees:{x:number;z:number;kind:'olive'|'pine';size:number}[]=[],graveyard=polygonIndex(features.filter(f=>f.kind==='cemetery').map(f=>ring(f.pts)));
 const free=(x:number,z:number)=>within(x,z)&&!keepOut(x,z)&&!clear(x,z,1.2)&&!built(x,z);
 for(const f of features)if(f.kind==='tree'){const [x,z]=f.pts[0];if(free(x,z))trees.push({x,z,kind:f.leafType==='needleleaved'?'pine':'olive',size:.8+random()*.4});}
 for(const g of greens(features)){
  if(g.cover==='grass')continue;const plan=PLANTED[g.cover],xs=g.pts.map(p=>p[0]),zs=g.pts.map(p=>p[1]);
  for(let x=Math.ceil(Math.min(...xs)/plan.spacing)*plan.spacing;x<=Math.max(...xs);x+=plan.spacing)for(let z=Math.ceil(Math.min(...zs)/plan.spacing)*plan.spacing;z<=Math.max(...zs);z+=plan.spacing){
   const tx=x+(random()-.5)*plan.spacing*.5,tz=z+(random()-.5)*plan.spacing*.5;
   if(random()<plan.fill&&inside(tx,tz,g.pts)&&free(tx,tz)&&!graveyard(tx,tz))trees.push({x:tx,z:tz,kind:g.cover==='wood'?'pine':'olive',size:.75+random()*.5});
  }
 }
 if(trees.length){
  const trunks=new T.InstancedMesh(new T.CylinderGeometry(.16,.24,1,6),plain('#6b5a43','wood'),trees.length),crowns=new T.InstancedMesh(new T.IcosahedronGeometry(1,1),plain('#ffffff','leaves'),trees.length),o=new T.Object3D();
  trees.forEach((t,i)=>{
   const spec=TREE[t.kind],y=surface(t.x,t.z),h=spec.trunk*t.size,r=spec.crown[0]*t.size,c=spec.crown[1]*t.size;
   o.position.set(t.x,y+h/2-.15,t.z);o.rotation.set(0,0,0);o.scale.set(1,h+.3,1);o.updateMatrix();trunks.setMatrixAt(i,o.matrix);
   o.position.set(t.x,y+h+c/2-.3,t.z);o.rotation.set(0,random()*6.28,0);o.scale.set(r,c/2,r*(.85+random()*.3));o.updateMatrix();crowns.setMatrixAt(i,o.matrix);
   crowns.setColorAt(i,new T.Color(spec.colour).multiplyScalar(.88+random()*.24));
  });
  trunks.castShadow=crowns.castShadow=true;trunks.receiveShadow=crowns.receiveShadow=true;trunks.name='context-trunks';crowns.name='context-crowns';
  // Crowns do not stop a walker in the smooth model; in the block build they are leaves.
  crowns.userData.walkCollision=false;crowns.userData.blockSolid=true;group.add(trunks,crowns);
 }
 group.userData.counts={graves:graves.length,wallStretches:wallBoxes.length,gates:gates.length,buildings:buildings.length,trees:trees.length};
 return group;
}
