import * as T from "three";
import { landscapeGround, elevationAt, placeTerrain, type LandscapeGround } from "./atlas-model-landscape";
import { siteContext, pavedIndex, greenIndex, buildSiteContext, CONTEXT_LICENCE, type ContextFeature } from "./atlas-model-context";
import { SVGLoader } from "three/addons/loaders/SVGLoader.js";
import type { SitePlan } from "./atlas-explorer-model";
import { createSiteMaterials, cloneSiteMaterial, chippedBlock } from './atlas-site-materials';
import { decodeRaster, elementPoints, rasterRectangles, type TracedElement, type TracedPlan } from './atlas-traced';
import tracedData from './atlas-traced-plans.json';
import type { TerrainPatch, LandscapePad } from './atlas-model-landscape';

const traced=tracedData as unknown as Record<string,TracedPlan>;
// Illustrative heights for traced plans, used only where no height is published.
export const TRACED_HEIGHTS={ruin:.9,wall:3.2,column:3.6,columnBase:.4,depth:2,dashed:.12,podium:1};
// `context`: the mapped surroundings of a plan placed in its setting (atlas/public/context), when loaded.
// `pads`: extra ground pads in the model's frame for one view only (the Ancient ground view's published levels, atlas-ancient-ground.ts).
export type BuildOptions={layer?:string;terrain?:TerrainPatch;context?:ContextFeature[];pads?:LandscapePad[]};
// How a plan that has no registration of its own meets its mapped setting: the model point (or marker)
// that goes onto the mapped target or the place anchor, the model point (or marker) where model height
// `datumY` meets the modern terrain, and whether its display bench is kept around it.
// `centre` is the model point that the model's ground (and its block build) is centred on, if not its origin.
// `level` (metres above sea level) puts model height 0 at a published level instead of on the modern terrain.
const SETTINGS:Record<string,{point?:Point|string;datum?:Point|string;datumY?:number;bench?:boolean;centre?:Point;level?:number;levelNote?:string}>={
 // The traced frame's origin (the centre of cistern L110) is the registered point.
 // Its ground is the median of the 31 published room and court levels on Magen & Peleg Fig. 57 (−324.54 m),
 // 0.28 m below the model's floors as on every bench.
 'qumran-settlement':{point:'traced-origin',level:-324.26,levelNote:'Heights: the model’s ground is set to −324.54 m, the median of the 31 room and court spot levels printed on Magen & Peleg 2018 Fig. 57 (−323.41 to −326.02 m; pools and channels left out), not to the modern terrain. Single rooms differ from it by up to 1.5 m; the traced walls keep one ground.'},
 'bethesda-pools':{point:'dam'},
 // The gatehouse is the frame's origin; y = 0 is the Haram surface at cistern XV.
 'east-gate-warren':{datum:'cistern-xv'},
 // The traced frame's origin (the outer north-west corner of the northern pool) is the registered point.
 'jericho-early':{point:'traced-origin'},'jericho-late':{point:'traced-origin'},
 // The precinct stands on the summit platform, 15.5 m above the model's base.
 'gerizim-precinct':{datum:'persian-precinct',datumY:15.5,bench:false},
 // The parts spread round the hill on their own ground: no display bench.
 'hyrcania-waterworks':{bench:false,centre:[-92,-5]},
};
// Hyrcania, metres from the place anchor (x east, z south), from Patrich 1989 Fig. 22 registered to imagery
// (research/assets/plans/imagery-registration-2026-10-22/hyrcania.json).
const HYRCANIA={doublePool:[-106.6,-69.75] as Point,separatePool:[-158.4,1.9] as Point,pit:[-72.1,-82] as Point,summit:[-37.7,7.7] as Point,tunnel:[-104,65.2] as Point,
 bridge:[[-87.2,-14.2],[-172,-87.4]] as [Point,Point],cisterns:[[-31.2,50.1],[-24.7,62.7],[-24.2,77],[-12,69.5]] as Point[],
 arc:[[-39.8,-30.7],[-50.8,-19.4],[-60.7,-7.7],[-72.7,4.1],[-84.7,15.9],[-92.4,27.4],[-96.9,38.6],[-98,44.1]] as Point[],east:[[-39.5,-31.1],[-33.9,-30.1],[-18.9,-5.8],[-24.1,46.6]] as Point[]};
// Gerizim, metres from the place anchor (x east, z south), from Magen 2008's plans registered to imagery
// (research/assets/plans/imagery-registration-2026-10-22/gerizim.json).
const GERIZIM={core:[[-20.2,-88.3],[60.2,-71],[49.8,-1.6],[-38.9,-7.3]] as Point[],centre:[12.7,-42] as Point,northGate:[20,-79.7] as Point,eastGate:[57,-38] as Point,southGate:[5.4,-4.5] as Point,
 stair:[78,-42] as Point,lowerGate:[100,-25] as Point,citadel:[41.5,28.5] as Point,fortified:{c:[-29,14.5] as Point,sw:[-51,33.6] as Point},westEntrance:[-12.5,43.5] as Point,mansion:[-73.3,1.9] as Point,platform:[17,9] as Point};

export type { ModelCamera } from "./atlas-explorer-model";
export type ModelGeometry = { root: T.Group; markers: Map<string, T.Vector3>; selectable: T.Object3D[]; roof: T.Group; note: string; assumptions: string[]; units: "metres" | "relative"; framing:T.Box3; landscape:{context:string;credit:string;mapped:boolean;registered?:boolean;registeredBy?:'outlines'|'imagery'};walkStart?:{position:[number,number];bearing:number;pitch:number} };
type Point = [number, number];
type Space = [number, number, number, number, number, number];

function polygon(points:Point[]) {const s=new T.Shape();points.forEach(([x,z],i)=>i?s.lineTo(x,-z):s.moveTo(x,-z));s.closePath();return s;}
function material(color:string,map?:T.Texture){return new T.MeshStandardMaterial({color,map:map??null,roughness:.94,metalness:0});}
export function buildModel(plan:SitePlan,options:BuildOptions={}):ModelGeometry {
 const root=new T.Group(), roof=new T.Group(),markers=new Map<string,T.Vector3>(),selectable:T.Object3D[]=[];
 const surfaces=createSiteMaterials(plan.id),{stone,rock,earth,plaster,restored}=surfaces,copper=material("#b56b42");let tracedStart:ModelGeometry["walkStart"],tracedOrigin:Point|undefined;
 const wellHoles:Point[][]=[],courtFloors:{x:number;z:number;w:number;d:number;mesh:T.Mesh}[]=[];let ground:LandscapeGround={w:40,d:40,holes:[],pads:[]};
 // A model registered to the place frame keeps it: no recentring, and its ground rectangle sits here.
 let placeFrame:Point|null=null;
 const circlePoints=(x:number,z:number,r:number):Point[]=>Array.from({length:36},(_,i)=>[x+Math.cos(i*Math.PI/18)*r,z+Math.sin(i*Math.PI/18)*r]);
 const assumptions:string[]=[];let note="Plan relations in 3D · heights illustrative",units:ModelGeometry["units"]="relative";
 const tag=(mesh:T.Object3D,id?:string)=>{if(id){mesh.userData.featureId=id;selectable.push(mesh)}return mesh};
 function mesh(geometry:T.BufferGeometry,mat:T.Material,id?:string,parent=root){const m=new T.Mesh(geometry,cloneSiteMaterial(mat));m.castShadow=mat!==earth;m.receiveShadow=true;parent.add(tag(m,id));return m;}
 function box(x:number,z:number,w:number,d:number,h:number,y=0,id?:string,mat:T.Material=stone,parent=root){const m=mesh(chippedBlock(w,h,d),mat,id,parent);m.position.set(x,y+h/2,z);return m;}
 function slab(points:Point[],depth:number,y=0,mat:T.Material=stone,id?:string,parent=root,holes:Point[][]=[]){const s=polygon(points);for(const hole of holes)s.holes.push(polygon(hole));const g=new T.ExtrudeGeometry(s,{depth,bevelEnabled:false,curveSegments:12});g.rotateX(-Math.PI/2);const m=mesh(g,mat,id,parent);m.position.y=y;m.userData.walkSurface=true;return m;}
 function trough(points:T.Vector3[],width:number,id?:string,lining:T.Material=plaster){for(let i=1;i<points.length;i++){
  const a=points[i-1],b=points[i],length=Math.hypot(b.x-a.x,b.z-a.z);if(length<.01)continue;
  const yaw=-Math.atan2(b.z-a.z,b.x-a.x),g=new T.Group();g.position.copy(a.clone().add(b).multiplyScalar(.5));g.rotation.y=yaw;root.add(g);
  box(0,0,length,width,.09,0,id,lining,g);
  for(const side of [-1,1]){const count=Math.ceil(length/.65),blocks=new T.InstancedMesh(chippedBlock(1,1,1,23),cloneSiteMaterial(lining===restored?restored:surfaces.block),count),o=new T.Object3D();
   for(let k=0;k<count;k++){o.position.set(-length/2+(k+.5)*length/count,.23,side*(width/2+.065));o.scale.set(length/count-.015,.38,.14);o.rotation.set(0,0,Math.sin(k*7)*.009);o.updateMatrix();blocks.setMatrixAt(k,o.matrix);}blocks.castShadow=blocks.receiveShadow=true;g.add(tag(blocks,id));}
 }}
 function coveredPassage(points:T.Vector3[],id?:string){for(let i=1;i<points.length;i++){
  const a=points[i-1],b=points[i],length=Math.hypot(b.x-a.x,b.z-a.z);if(length<.01)continue;
  const g=new T.Group();g.position.copy(a.clone().add(b).multiplyScalar(.5));g.rotation.y=-Math.atan2(b.z-a.z,b.x-a.x);root.add(g);
  box(0,0,length+.02,.95,.09,0,id,plaster,g);
  for(const side of [-1,1])box(0,side*.64,length+.02,.34,1.35,0,id,rock,g);
  box(0,0,length+.12,1.66,.38,1.35,id,rock,g);
 }}
 function walls(points:Point[],height:number,thickness:number,y=0,id?:string,closed=true,mat:T.Material=stone){
  for(let i=0;i<points.length-(closed?0:1);i++){
   const a=points[i],b=points[(i+1)%points.length],length=Math.hypot(b[0]-a[0],b[1]-a[1]);
   const yaw=-Math.atan2(b[1]-a[1],b[0]-a[0]);
   if(mat===stone&&length>.8){
    const kind=surfaces.style.masonry,rubble=kind==='rubble',unit=kind==='ashlar'?1.05:rubble?.46:.68;
    const rows=Math.max(1,Math.ceil(height/surfaces.style.courses)),columns=Math.max(1,Math.ceil(length/unit)),h=height/rows;
    const blocks=new T.InstancedMesh(chippedBlock(1,1,1,17),cloneSiteMaterial(surfaces.block),rows*(columns*2+2)),o=new T.Object3D();let index=0;
    const jitter=(k:number,seed:number)=>Math.sin(k*12.9898+seed*78.233)*.5;
    for(let row=0;row<rows;row++){
     // Rubble (Qumran, Hyrcania, from their reference photos) uses unequal
     // stone lengths, heights and set-backs; coursed and ashlar keep regular joints.
     const cuts=[0];if(rubble){let x=0,k=0;while(x<length){x=Math.min(length,x+unit*(.62+(jitter(row*41+k++,i+3)+.5)*.85));cuts.push(x);}}
     else{const step=length/columns,offset=(row%2)*step*.5;for(let col=0;col<=columns;col++)cuts.push(Math.min(length,Math.max(0,(col+1)*step-offset)));}
     for(let c=1;c<cuts.length;c++){
      const left=cuts[c-1],right=cuts[c];if(right-left<.025)continue;
      const t=(left+right)/(2*length),tone=rubble?.72+(jitter(row*7+c,11)+.5)*.42:.81+((c*11+row*7)%23)/80;
      const hh=rubble?h*(.78+(jitter(row*5+c,7)+.5)*.2):h,dz=rubble?jitter(row*3+c,5)*.07:0;
      o.position.set(a[0]+(b[0]-a[0])*t+Math.sin(yaw)*dz,y+(row+.5)*h+(rubble?jitter(c,row)*.03:0),a[1]+(b[1]-a[1])*t+Math.cos(yaw)*dz);
      o.rotation.set(rubble?jitter(c,row+2)*.05:0,yaw+(rubble?jitter(c+row,4)*.06:0),rubble?jitter(c*13,row)*.08:Math.sin(c*13+row*7)*.004);
      o.scale.set(right-left-(rubble?.035:.014),hh-.012,thickness*(rubble?.92+(jitter(c,row+9)+.5)*.12:1));o.updateMatrix();blocks.setMatrixAt(index,o.matrix);blocks.setColorAt(index++,new T.Color().setScalar(tone));
     }}blocks.count=index;blocks.castShadow=blocks.receiveShadow=true;root.add(tag(blocks,id));
   }else {const m=box((a[0]+b[0])/2,(a[1]+b[1])/2,length,thickness,height,y,id,mat);m.rotation.y=yaw;}
   // Individually chipped coping stones give the ruin a broken silhouette.
   // Their positions and wear are surface art, not a stone-by-stone survey.
   if(mat===stone&&length>.8){const count=Math.ceil(length/.72),caps=new T.InstancedMesh(chippedBlock(1,.20,1),cloneSiteMaterial(surfaces.block),count),o=new T.Object3D();caps.castShadow=caps.receiveShadow=true;
    for(let k=0;k<count;k++){const t=(k+.5)/count,w=length/count-.025;o.position.set(a[0]+(b[0]-a[0])*t,y+height-.04+Math.sin(k*7.1)*.035,a[1]+(b[1]-a[1])*t);o.rotation.y=yaw;o.scale.set(w,1,thickness+.04);o.updateMatrix();caps.setMatrixAt(k,o.matrix);caps.setColorAt(k,new T.Color().setScalar(.82+((k*13)%17)/65));}root.add(tag(caps,id));}
  }
 }
 function court(x:number,z:number,w:number,d:number,h:number,id?:string,holes:Point[][]=[]){const p:Point[]=[[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]];
  // Nested rooms share their courtyard floor. Coplanar duplicate floors flicker
  // and cast false shadows when the camera reaches eye level.
  if(!courtFloors.some(f=>Math.abs(f.mesh.position.y)<.001&&Math.abs(x-f.x)+w/2<=f.w/2&&Math.abs(z-f.z)+d/2<=f.d/2))courtFloors.push({x,z,w,d,mesh:slab(p,.25,0,earth,id,root,holes)});
  walls(p,h,Math.max(.28,w*.025),0,id);}
 function basin(points:Point[],depth:number,id:string,lining:T.Material=stone){
  // A basin drawn only by a reconstruction is restored throughout, floor and coping included.
  const whole=lining===restored;
  slab(points,.3,-depth-.3,whole?restored:plaster,id);walls(points,depth,.35,-depth,id,true,lining);
  points.forEach((a,i)=>{const b=points[(i+1)%points.length],cap=box((a[0]+b[0])/2,(a[1]+b[1])/2,Math.hypot(b[0]-a[0],b[1]-a[1]),.39,.12,.015,id,whole?restored:surfaces.block);cap.rotation.y=-Math.atan2(b[1]-a[1],b[0]-a[0]);});
 }
 function shaft(x:number,z:number,r:number,depth:number,id:string,mat:T.Material=stone){
  wellHoles.push(circlePoints(x,z,r+.02));
  const g=new T.CylinderGeometry(r,r*.78,depth,32,1,true);const m=mesh(g,mat,id);m.position.set(x,-depth/2,z);(m.material as T.MeshStandardMaterial).side=T.DoubleSide;
  const rim=mesh(new T.TorusGeometry(r,.17,6,48),mat,id);rim.rotation.x=Math.PI/2;rim.position.set(x,.12,z);
  const floor=mesh(new T.CircleGeometry(r*.8,32),mat===restored?restored:plaster,id);floor.rotation.x=-Math.PI/2;floor.position.set(x,-depth+.02,z);
 }
 function steps(x:number,z:number,width:number,run:number,rise:number,count:number,id:string,mat:T.Material=stone){const g=new T.Group();root.add(g);g.position.set(x,0,z);for(let i=0;i<count;i++)box(-run/2+(i+.5)*run/count,0,run/count+.01,width,(i+1)*rise/count,0,id,mat,g);return g;}
 function marker(id:string,x:number,z:number,y=1){markers.set(id,new T.Vector3(x,y,z));}
 function plinth(w:number,d:number,_depth=1.2,holes:Point[][]=[]){ground={w,d,holes:[...holes,...wellHoles],pads:ground.pads};}
 // Rock with rock-cut spaces: the rock is drawn as boxes, band by band between the spaces'
 // floor and ceiling levels, so chambers, doorways and stairs stay open in the smooth model
 // and in the block build. A space is [x0, x1, z0, z1, y0, y1] in the parent's frame.
 function rockMass(bounds:Space,spaces:Space[],parent:T.Group=root,id?:string,mat:T.Material=rock){
  const cuts=(lo:number,hi:number,a:number,b:number)=>[...new Set([lo,hi,...spaces.flatMap(s=>[s[a],s[b]]).filter(v=>v>lo&&v<hi)])].sort((p,q)=>p-q);
  const xs=cuts(bounds[0],bounds[1],0,1),zs=cuts(bounds[2],bounds[3],2,3),ys=cuts(bounds[4],bounds[5],4,5),nx=xs.length-1,nz=zs.length-1;
  const emit=(key:string,y0:number,y1:number)=>{const [i0,i1,k0,k1]=key.split(',').map(Number),w=xs[i1+1]-xs[i0],d=zs[k1+1]-zs[k0],m=mesh(new T.BoxGeometry(w,y1-y0,d),mat,id,parent);m.position.set(xs[i0]+w/2,(y0+y1)/2,zs[k0]+d/2);};
  let open=new Map<string,number>();
  for(let j=0;j<ys.length-1;j++){
   const yc=(ys[j]+ys[j+1])/2,solid=(i:number,k:number)=>{const xc=(xs[i]+xs[i+1])/2,zc=(zs[k]+zs[k+1])/2;return !spaces.some(s=>xc>s[0]&&xc<s[1]&&zc>s[2]&&zc<s[3]&&yc>s[4]&&yc<s[5]);};
   const used=new Uint8Array(nx*nz),next=new Map<string,number>();
   for(let k=0;k<nz;k++)for(let i=0;i<nx;i++){
    if(used[k*nx+i]||!solid(i,k))continue;
    let i1=i;while(i1+1<nx&&!used[k*nx+i1+1]&&solid(i1+1,k))i1++;
    let k1=k;grow:while(k1+1<nz){for(let ii=i;ii<=i1;ii++)if(used[(k1+1)*nx+ii]||!solid(ii,k1+1))break grow;k1++;}
    for(let kk=k;kk<=k1;kk++)for(let ii=i;ii<=i1;ii++)used[kk*nx+ii]=1;
    const key=`${i},${i1},${k},${k1}`;next.set(key,open.get(key)??ys[j]);
   }
   for(const [key,y0] of open)if(!next.has(key))emit(key,y0,ys[j]);
   open=next;
  }
  for(const [key,y0] of open)emit(key,y0,ys[ys.length-1]);
 }
 // A square-based pyramid (closed, so the block export fills it), its base edges on the frame's axes.
 function pyramid(x:number,z:number,side:number,height:number,y:number,mat:T.Material,id?:string,parent:T.Group=root){const m=mesh(new T.CylinderGeometry(.02,side/Math.SQRT2,height,4),mat,id,parent);m.rotation.y=Math.PI/4;m.position.set(x,y+height/2,z);return m;}
 // The part of a polygon on the far side of x = c (Sutherland–Hodgman against one line).
 const clipX=(poly:Point[],c:number,keepAbove=true)=>{const out:Point[]=[],inside=(p:Point)=>keepAbove?p[0]>=c:p[0]<=c;poly.forEach((p,i)=>{const q=poly[(i+1)%poly.length];if(inside(p))out.push(p);if(inside(p)!==inside(q)){const t=(c-p[0])/(q[0]-p[0]);out.push([c,p[1]+t*(q[1]-p[1])]);}});return out;};

 if(plan.id==="abu-saraj-iv17"){
  units="metres";note="Cave cutaway · published 1.4–1.7 m height range";
  const s=3/178, convert=([x,z]:Point):Point=>[(x-330)*s,(z-290)*s];
  const outer:Point[]=[[35,433],[103,392],[165,335],[197,295],[159,248],[158,180],[225,145],[258,103],[291,83],[338,111],[361,141],[414,122],[470,118],[545,139],[579,163],[591,230],[591,337],[576,384],[594,410],[614,425]];
  const pillar:Point[]=[[333,406],[338,367],[350,341],[341,312],[346,290],[371,277],[398,294],[411,316],[388,343],[409,367],[434,383],[490,377],[500,391],[488,404],[497,417],[521,420],[524,440],[491,447],[452,443],[414,430],[373,408]];
  slab(outer.map(convert),.28,-.28,earth,undefined,root,[pillar.map(convert)]);
  walls(outer.map(convert),1.55,.38,0,undefined,false,rock);slab(pillar.map(convert),1.55,0,rock,"pillar");
  const [bx,bz]=convert([231,442]);box(bx,bz,.4,2.4,.72,0,"south-mouth");
  // The cap is a presentation volume only; the plan gives no surveyed roof shape.
  slab(outer.map(convert),.45,1.55,rock,undefined,roof);root.add(roof);
  for(const f of plan.features){const [x,z]=convert([f.x,f.y]);marker(f.id,x,z,f.id==="pillar"?1.75:.4);}
  plinth(12,9,.55);
  assumptions.push("Outline sampled from Sion’s Plan 5. Scale follows its 3 m bar; sampling and scanned line widths limit precision.","Wall height 1.55 m is the midpoint of the published 1.4–1.7 m range, applied uniformly for display. Roof thickness and shape, wall thickness and masonry height are illustrative.","The two present openings, pillar and southern blocking wall remain distinct. No threshold elevation, ancient roof profile or deposit point is inferred.");
 } else if(plan.id==="hyrcania-waterworks"){
  units="metres";const herodian=options.layer==="herodian",H=HYRCANIA;
  note=herodian?"Herodian east bridge raised to its channel · Patrich 2002 (reconstruction)":"Double pool and east bridge · Patrich 1989 Fig. 22 registered to imagery";
  // Positions are metres from the place anchor (x east, z south): Patrich 1989 Fig. 22 (p. 256), registered to
  // satellite imagery (research/assets/plans/imagery-registration-2026-10-22/hyrcania.json). The parts spread
  // round the hill, so each stands on the modern terrain at its own place; y = 0 is the terrain at the anchor.
  const patch=placeTerrain(plan.placeIds[0],options.terrain),g0=patch?elevationAt(patch,0,0):0,groundAt=(x:number,z:number)=>(patch?elevationAt(patch,x,z):0)-g0;
  // A turn on the map, clockwise by deg about the old frame's point c0, then a move to C.
  const turn=(p:Point,c0:Point,C:Point,deg:number):Point=>{const t=T.MathUtils.degToRad(deg),x=p[0]-c0[0],z=p[1]-c0[1];return [C[0]+x*Math.cos(t)-z*Math.sin(t),C[1]+x*Math.sin(t)+z*Math.cos(t)];};
  const lift=(y:number,build:()=>void)=>{const start=root.children.length;build();root.children.slice(start).forEach(o=>o.position.y+=y);};
  // Double pool: the published sizes (old frame below), turned 35° clockwise so that its members lie as
  // Fig. 22 draws them (north-east and south-west, long sides on 122°), centred where the figure puts them.
  const dp=(p:Point)=>turn(p,[-10,-9.45],H.doublePool,35);
  const n=([[-19,-27],[-.8,-27],[0,-11],[-19,-12]] as Point[]).map(dp),s=([[-19,-6.9],[-1,-6.9],[-1,7.5],[-19,7.5]] as Point[]).map(dp);
  const sp=(p:Point)=>turn(p,[-21,25.5],H.separatePool,-4.75),south=([[-27,20],[-15,20],[-15,31],[-27,31]] as Point[]).map(sp);
  const yPool=groundAt(...H.doublePool),ySouth=groundAt(...H.separatePool);
  lift(yPool,()=>{basin(n,5,"north-pool",plaster);basin(s,2.6,"south-member",plaster);slab(([[-23,-30],[4,-30],[4,11],[-23,11]] as Point[]).map(dp),.8,-5.8,rock,undefined,root,[n,s]);});
  const mid=(ps:Point[]):Point=>[ps.reduce((a,p)=>a+p[0],0)/ps.length,ps.reduce((a,p)=>a+p[1],0)/ps.length];
  {const [x,z]=mid(n);marker("north-pool",x,z,yPool+.55);}{const [x,z]=mid(s);marker("south-member",x,z,yPool+.55);}
  ground.pads.push({x:H.doublePool[0],z:H.doublePool[1],w:34,d:34,height:yPool,feather:8,angle:-T.MathUtils.degToRad(35)});
  // East bridge, no. 48 (Patrich 2002): 112 m long (p. 346); preserved up to about 6 m high, 2.5 m wide at the
  // base and 1.45 m at the top (p. 348). Fig. 22 draws it across the saddle north-west of the summit (גשר),
  // from the summit track north-westwards; it is drawn along that line. Its foot follows the modern terrain;
  // its top is level, 6 m above the saddle's lowest point.
  const [ex,ez]=H.bridge[0],[wx,wz]=H.bridge[1],length=Math.hypot(wx-ex,wz-ez),yaw=-Math.atan2(wz-ez,wx-ex);
  const along=(f:number):Point=>[ex+(wx-ex)*f,ez+(wz-ez)*f],samples=Array.from({length:15},(_,k)=>groundAt(...along(k/14))),low=Math.min(...samples);
  const bridge=new T.Group();bridge.position.set(ex,0,ez);bridge.rotation.y=yaw;root.add(bridge);
  for(let k=0;k<14;k++){const f=(k+.5)/14,foot=Math.min(samples[k],samples[k+1])-.4,top=Math.max(low+6,foot+.5);
   const section=new T.Shape([new T.Vector2(-1.25,0),new T.Vector2(1.25,0),new T.Vector2(.725,top-foot),new T.Vector2(-.725,top-foot)]);
   const g=new T.ExtrudeGeometry(section,{depth:length/14+.02,bevelEnabled:false});g.rotateY(Math.PI/2);const m=mesh(g,stone,"bridge",bridge);m.position.set(f*length-length/28,foot,0);}
  if(herodian){
   // The Herodian channel ran about 12.5 m above the saddle (p. 348): the upper part and the
   // channel are drawn only by this reconstruction.
   box(length/2,0,length,1.45,6.5,low+6,"bridge",restored,bridge);
   const ch=mesh(new T.BoxGeometry(length,.5,.5),restored,"bridge",bridge);ch.position.set(length/2,low+12.75,0);
  }
  {const [x,z]=along(.5);marker("bridge",x,z,(herodian?low+13.5:low+7));}
  // Southern pool ("the southern pool" on Fig. 22): a quarried depression with a vertical rock-cut west side and
  // no visible plaster (pp. 348, 351); its size is illustrative.
  lift(ySouth,()=>basin(south,1.8,"separate-pool",rock));marker("separate-pool",H.separatePool[0],H.separatePool[1],ySouth+.6);
  ground.pads.push({x:H.separatePool[0],z:H.separatePool[1],w:18,d:17,height:ySouth,feather:6});
  // Round pit north-east of the north pool: 3.05 m across, 4.3 m deep (p. 348, Fig. 23), at the round
  // cistern Fig. 22 draws there.
  {const y=groundAt(...H.pit);lift(y,()=>shaft(H.pit[0],H.pit[1],1.525,4.3,"pit",rock));marker("pit",H.pit[0],H.pit[1],y+.6);}
  // The summit fortress wall where Fig. 22 draws it (the north-west arc and the east side; the south is open
  // on the figure), and the summit buildings as one court. Wall heights are illustrative.
  for(const line of [H.arc,H.east])for(let k=0;k+1<line.length;k++){const seg=[line[k],line[k+1]],y=Math.min(...seg.map(p=>groundAt(...p)));lift(y-.3,()=>walls(seg,2.7,1.6,0,undefined,false));}
  {const y=groundAt(...H.summit);lift(y,()=>{court(H.summit[0],H.summit[1],22,28,2.1);court(H.summit[0],H.summit[1],9,12,1.9);});ground.pads.push({x:H.summit[0],z:H.summit[1],w:26,d:32,height:y,feather:6});}
  // Southern cisterns D, E, F and G where Fig. 22 draws them; their sizes and depths are illustrative.
  for(const c of H.cisterns){const y=groundAt(...c);lift(y,()=>shaft(c[0],c[1],2,3,"cisterns"));}
  {const [x,z]=mid(H.cisterns.slice(0,2));marker("cisterns",x,z,groundAt(x,z)+.7);}
  // Point 49: a built, barrel-vaulted tunnel between cisterns A and N; free part 11.5 m long, 1.25 m high and
  // 0.75 m wide, with a square opening at the north end and débris at the south (p. 351). It is set at the
  // figure's (49), running north–south on the figure; its exact course is not drawn there.
  {const [tx,tz]=H.tunnel,y=groundAt(tx,tz),g=new T.Group();g.position.set(tx,y,tz);g.rotation.y=T.MathUtils.degToRad(4.75);root.add(g);
   const r=.575,len=11.5;box(0,0,.75,len,.08,0,"tunnel-49",plaster,g);
   for(const side of [-1,1])box(side*r,0,.4,len,.875,0,"tunnel-49",stone,g);
   const vault=new T.CylinderGeometry(r,r,len,16,1,true,-Math.PI/2,Math.PI);vault.rotateX(-Math.PI/2);const v=mesh(vault,stone,"tunnel-49",g);v.position.set(0,.875,0);(v.material as T.MeshStandardMaterial).side=T.DoubleSide;
   box(0,len/2-.6,1.55,1.2,1.25,0,"tunnel-49",earth,g);marker("tunnel-49",tx,tz-len/2+3,y+1.6);}
  plinth(190,190,6.3,[n,s,south]);ground.focus=H.doublePool;
  assumptions.push("Positions come from Patrich 1989 Fig. 22 (p. 256; 0–50 m bar in five segments, 4.61 px/m on the scan), registered to Vantor WorldView-2 imagery of 21 October 2023 (Esri World Imagery, 0.5 m pixels, stated accuracy 5 m) by matching its walls to the imagery: the figure's page-up lies 4.75° ± 0.6° west of north, at 4.633 px/m (0.5 % from the bar). The figure's contours then follow the 10 m elevation model's contours round the hill, and its bridge, double pool, round cistern and southern cisterns fall on the features visible in the imagery. Record: research/assets/plans/imagery-registration-2026-10-22/hyrcania.json.","Northern pool sides approximate the published 19 / 15 / 18.2 / 16 m quadrilateral. Published maximum depths are shown: about 5 m north, 2.6 m south (Patrich 1989 p. 255; repeated in Patrich 2002 p. 348). Patrich's compass words for the sides are rounded: on the registered figure the pools' long sides run at about 122°.","Rock separation uses 5.1 m, the midpoint of the reported 4.8–5.4 m range. The southern pool's outline, the summit walls and buildings, the cisterns' sizes and depths and the tunnel's course are illustrative; each part stands on the 10 m modern elevation model at its own place, which is not the ancient ground.","The double pool is drawn rock-cut with plastered faces (Patrich 1989 p. 255, \"rock-cut double pool\"; reference photograph hyrcania-c-hurkania-5011 shows plastered rock walls), not as laid masonry; the coping course is illustrative.","East bridge (no. 48): 112 m long, 2.5 m wide at the base and 1.45 m at the top, about 6 m high at most today (Patrich 2002 pp. 346–348). Fig. 22 draws it across the saddle north-west of the summit; it is drawn along that line, from the summit track. Its foot follows the modern terrain and its top is level, 6 m above the saddle's lowest point; its varying preserved height and its Hasmonean lower courses are not drawn. Feldman (1973 or later, p. 334) gives the eastern saddle wall as 170 m long and 16.78 m high.","The round pit (3.05 m across, 4.3 m deep) and the point 49 tunnel (11.5 × 1.25 × 0.75 m, barrel-vaulted) use Patrich 2002's dimensions. The pit is set at the round cistern that Fig. 22 draws north-east of the double pool; the tunnel at the figure's (49). The tunnel's vault is drawn as a half-cylinder; its south end is drawn blocked by débris.","Floors are tinted to distinguish basins; the tint is not a reconstructed water level. Centre/rim origins and construction phases remain unresolved. The placement is for display: it changes no reading, test or rating.");
  if(herodian)assumptions.push("Herodian view: Patrich 2002 p. 348 puts the Herodian channel about 12.5 m above the bridge's base, 1.20 m above its present west end. The pale upper wall (1.45 m wide, from 6 to 12.5 m) and the 0.5 m channel on it are drawn only by this reconstruction; Patrich also offers upper arches or a siphon, and Ritmeyer's drawing (Fig. 17) was not traced. The channel's onward course to the upper cisterns on the south and east slopes is not drawn.");
 } else if(plan.id==="gerizim-precinct"){
  units="metres";const persian=options.layer==="persian",G=GERIZIM;
  note=persian?"Persian-period precinct · Magen, Misgav & Tsfania 2004 (reconstruction)":"Hellenistic precinct · Magen's plans registered to imagery";
  // Positions are metres from the place anchor (x east, z south), read from Magen 2008's site plan (p. 1743)
  // and precinct plan (p. 1746), each registered to satellite imagery (record:
  // research/assets/plans/imagery-registration-2026-10-22/gerizim.json). The precinct core keeps the
  // drawn outline of its walls; the other parts are the reported envelopes at their drawn places.
  const start=root.children.length,[nw,ne,se,sw]=G.core;
  // Each wall of the core, broken at its gates (3 m openings).
  const runs=(gates:Point[]):Point[][]=>{const out:Point[][]=[];for(const [a,b] of [[nw,ne],[ne,se],[se,sw],[sw,nw]] as [Point,Point][]){
   const len=Math.hypot(b[0]-a[0],b[1]-a[1]),ux=(b[0]-a[0])/len,uz=(b[1]-a[1])/len,at=(t:number):Point=>[a[0]+ux*t,a[1]+uz*t];
   const cuts=gates.filter(g=>Math.abs((g[0]-a[0])*uz-(g[1]-a[1])*ux)<4).map(g=>(g[0]-a[0])*ux+(g[1]-a[1])*uz).filter(t=>t>0&&t<len).sort((x,y)=>x-y);
   let from=0;for(const t of cuts){out.push([at(from),at(t-1.5)]);from=t+1.5;}out.push([at(from),at(len)]);}return out;};
  if(persian){
   // Magen et al. 2004 p. 3*: the Persian precinct measured 96 × 98 m including its gates; three gates,
   // north (six-chambered, fully exposed), south and east; no west gate. The Hellenistic core kept its size
   // (Magen 2008 p. 1746), so the core outline stands for it; the gates are set at the middles of the
   // north and south walls and at the later east gate, over the Persian altar (precinct plan no. 23).
   slab(G.core,.25,-.25,earth,"persian-precinct");
   for(const run of runs([G.northGate,G.eastGate,G.southGate]))walls(run,3.2,1.3,0,"persian-precinct",false);
   // North gate: three chambers each side of a central passage, along the north wall. The layout follows
   // the type; its sizes are illustrative.
   const gate=new T.Group();gate.position.set(G.northGate[0],0,G.northGate[1]);gate.rotation.y=-Math.atan2(ne[1]-nw[1],ne[0]-nw[0]);root.add(gate);
   for(const side of [-1,1]){for(let k=0;k<4;k++)box(side*4.5,k*4,5,1,3.2,0,"persian-precinct",stone,gate);box(side*6.75,6,.5,13,3.2,0,"persian-precinct",stone,gate);}
   // South and east gates: their Persian-period form is not described; the gatehouses are drawn only by this view.
   for(const [x,z] of [G.southGate,G.eastGate]){const g=root.children.length;court(x,z,9,7,3.4,"persian-precinct");root.children.slice(g).forEach(m=>{if(m instanceof T.Mesh){(m.material as T.Material).dispose();m.material=cloneSiteMaterial(restored);}});}
   root.children.slice(start).forEach(m=>m.position.y+=15.5);
  }else{
   // The summit platform stands for the reported 212 × 136 m enclosure (Magen 2008 p. 1746) round the core,
   // the courtyards, the citadel and the fortified enclosure; its walls are not drawn.
   const [px,pz]=G.platform;slab([[px-68,pz-106],[px+68,pz-106],[px+68,pz+106],[px-68,pz+106]],.25,-.25,earth);
   for(const run of runs([G.northGate,G.eastGate]))walls(run,2.2,1.3,0,"persian-precinct",false);
   walls([sw,G.fortified.sw],2.2,1.3,0,undefined,false);
   court(G.citadel[0],G.citadel[1],25,24,3.8,"citadel");court(G.fortified.c[0],G.fortified.c[1],39,38,3);
   court(G.westEntrance[0],G.westEntrance[1],13,12,1.2,"west-entrance");
   root.children.slice(start).forEach(m=>m.position.y+=15.5);
   const [mx,mz]=G.mansion,mansionStart=root.children.length,cisternHole=circlePoints(mx-9,mz,1.65);
   court(mx,mz,40,40,2.8,"mansion",[cisternHole]);court(mx-9,mz,20,14,2.1,"mansion",[cisternHole]);
   for(let i=0;i<3;i++)court(mx+11,mz-12+i*12,10,9,2.2,"mansion");shaft(mx-9,mz,1.6,2.6,"mansion");
   root.children.slice(mansionStart).forEach(m=>m.position.y+=8);
   ground.pads.push({x:mx,z:mz,w:42,d:42,height:8,feather:10});
   const stair=steps(G.stair[0],G.stair[1],23,34,15.5,57,"east-stair");stair.rotation.y=Math.PI;
   court(G.lowerGate[0],G.lowerGate[1],9,13,2.8,"east-stair");
  }
  ground.pads.push({x:G.platform[0],z:G.platform[1],w:136,d:212,height:15.5,feather:12});
  for(const [id,[x,z],y] of [["persian-precinct",G.centre,18],["citadel",G.citadel,persian?17:20],["west-entrance",G.westEntrance,17],["mansion",G.mansion,persian?9:11.6],["east-stair",G.stair,11]] as [string,Point,number][])marker(id,x,z,y);
  plinth(255,290,7);
  assumptions.push("Positions come from Magen 2008's site plan (p. 1743, 0–50 m bar) and plan of the sacred precinct (p. 1746, 0–25 m bar). Each plan was registered to Vantor WorldView-2 imagery of 21 October 2023 (Esri World Imagery, 0.5 m pixels, stated accuracy 5 m) by matching its walls to the imagery: the site plan is turned 4.35° and the precinct plan 92.85° from their drawn north arrows, at their bar scales within 1.5 %. The two plans then agree within 1–2 m. Record: research/assets/plans/imagery-registration-2026-10-22/gerizim.json.");
  if(persian)assumptions.push("Persian view: the precinct is the drawn outline of the core walls (west wall 83 m on the plan; Magen 2008 p. 1746: 84 m), which kept the Persian compound's size (96 × 98 m including the gates, Magen et al. 2004 p. 3*; about 200 × 200 cubits). Gates stand on the north, south and east and none on the west. The north gate is drawn as a six-chambered gate (fully exposed, p. 3*); its pier and chamber sizes are illustrative. The pale south and east gatehouses are drawn only by this view: their Persian-period form and size are not described in the pages read.","The Hellenistic enclosure, citadel, western entrance, Area P mansion and eastern stair are not drawn; their markers stay for comparison with the Hellenistic view. Remains of a Persian stair to the east gate lie under the later stair (p. 3*); they are not drawn. Wall heights and the platform level are illustrative.");
  else assumptions.push("The core walls follow the precinct plan's outline, with the north and east gates as openings; their 2.2 m height follows the west wall's preserved 2 m (Magen 2008 p. 1746). The outer west wall runs on to the fortified enclosure. Reported envelopes are drawn at their places on the plans: the 212 × 136 m enclosure (as the summit platform, without walls), the 39 × 38 m fortified enclosure, the 40 × 40 m mansion with its 20 × 14 m building IV, and the 25 × 24 m citadel.","The eastern stair uses the reported maximum 23 m width, 34 m run, 15.5 m rise and approximately 57 steps, centred where both plans draw it. The western entrance is shown as a separate schematic landing; it is not equated with the southern seven-step flight or the 15-step flight at E1.","Most wall heights, room divisions, the mansion’s 8 m display level and the cistern’s display location/depth are illustrative. The precinct platform expresses the east stair’s relative rise; its block shape is not surveyed terrain. No temple superstructure, P5178 coordinate or contemporary use horizon is asserted.");
 } else if(plan.id==="doq-waterworks"){
  note="Aqueduct, cisterns and ridge · source-relative model";
  const conv=([x,z]:Point):Point=>[(x-270)*.09,(z-300)*.09];
  const pts:Point[]=[[347,222],[311,248],[285,262],[317,277],[323,323],[327,380],[351,431],[302,452],[228,438]];
  trough(pts.map(p=>{const [x,z]=conv(p);return new T.Vector3(x,.35,z)}),.64,"intake");
  for(const p of [[145,357],[155,365],[168,373],[178,381],[191,388],[202,398],[215,408],[246,421],[289,424],[306,375]] as Point[]){const [x,z]=conv(p);shaft(x,z,1.15,3.2,"cisterns");}
  court(-2,6,8,4,1.1);box(-2,6,2,1.6,.4,0,undefined,rock);
  trough([[119,285],[195,264],[266,279]].map(p=>{const [x,z]=conv(p as Point);return new T.Vector3(x,-.04,z)}),1.2,"ditch",rock);
  for(const f of plan.features){const [x,z]=conv([f.x,f.y]);marker(f.id,x,z,1.5)}
  plinth(39,38,3.8);
  assumptions.push("The aqueduct and ten cistern positions follow selected relationships in Amit Fig. 2. The frame is normalized for display, without geographic registration.","Cistern diameters/depths, channel cross-section, defensive wall heights and ridge relief are illustrative. The source does not identify a guard-post or drying-room corner.");
 } else if(plan.id==="bethesda-pools"){
  units="metres";const royal=options.layer==="royal";
  note=royal?"Royal-period dam, upper pool and open canal · Pierre & Rousée 1981 (reconstruction)":"Two pools and dam · published dimensions on Pierre & Rousée’s plan; eastern complex schematic";
  // Plan metres: x east, z south, origin at the southern pool's north-west corner. Shifted to centre the scene.
  const c=([x,z]:Point):Point=>[x-54,z],r=(x0:number,z0:number,x1:number,z1:number):Point[]=>[[x0,z0],[x1,z0],[x1,z1],[x0,z1]].map(p=>c(p as Point));
  const D=(x0:number,x1:number,z0:number,z1:number,y0:number,y1:number):Space=>{const [a,b]=c([x0,z0]),[e,f]=c([x1,z1]);return [a,e,b,f,y0,y1];};
  // The dam is about 40 m long (Pierre & Rousée 1981 p. 24) and forms the north pool's south side, so the
  // pool's 40 m side is drawn east–west and Gibson's 53 m north–south (inference).
  const north=r(0,-59.5,40,-6.5),south=([[0,0],[45,0],[64.99,45.83],[0,47]] as Point[]).map(c),canal=r(19.625,0,20.375,46);
  basin(north,10,"north-pool");
  // The eastern complex keeps Duprez Pl. II's arrangement (its numbers below; scale not recorded). E moves it as
  // one block to the 'Grottes' area of Pierre & Rousée 1981 Fig. 2, 2–18 m east of the dam's east end across its
  // line, 3 m east of that area's centre to clear the south pool's drawn corner
  // (research/assets/plans/imagery-registration-2026-10-22/bethesda.json).
  const E=(x:number,z:number):Point=>[x-46,z-25],eastern=new Set(["cistern-1","threshold","grotto-6","grotto-5","first-installation"]);
  const grottoes=([[93.5,10,96.5,13,2.5,"first-installation"],[101,11,104,14,2.2,"first-installation"],[100.5,19,102.5,21,.3,"first-installation"],[93.5,27,96.5,30,1.5,"first-installation"],[106,19,107.5,21,1.5,"grotto-5"],[100,26,103.5,29.5,3,"grotto-6"]] as [number,number,number,number,number,string][]).map(([x0,z0,x1,z1,depth,id])=>[...E(x0,z0),...E(x1,z1),depth,id] as [number,number,number,number,number,string]);
  if(royal){
   // Pierre & Rousée 1981 pp. 24–25, Fig. 3: before the south basin, a slab-covered corridor about 2 m high
   // ran south from the foot of the dam's square shaft, and the water fell about 3 m into an open rock-cut
   // canal about 1 m deep and 0.75 m wide, known for about 50 m. The dam: a rock base and 20 courses of about 50 cm.
   rockMass(D(0,40,-6.5,0,-12,-10),[],root,"dam",rock);
   rockMass(D(0,40,-6.5,0,-10,0),[D(19.5,20.5,-6,-5,-10,.5),D(19.6,20.4,-5,.01,-10,-8)],root,"dam",stone);
   // The valley in front of the dam, drawn inside the later south basin's outline: drawn only by this view.
   walls(([[40,0],[45,0],[64.99,45.83],[0,47],[0,0]] as Point[]).map(c),12,.35,-12,"south-pool",false,restored);
   slab(south,.3,-12.3,restored,"south-pool",root,[canal]);
   const [ax,az]=c([20,23]);slab(canal,.3,-13.3,rock,"canal");for(const side of [-1,1])box(ax+side*.525,az,.3,46,1,-13,"canal",rock);
   plinth(128,128,14,[north,south,r(0,-6.5,40,0),canal]);
  }else{
   basin(south,14,"south-pool");
   // Square shaft about 1 × 1 m behind the dam's north face (Duprez; Pierre & Rousée p. 24), 15 m deep after Duprez.
   const [cx,cz]=c([20,-5.5]),sq:Point[]=[[cx-.6,cz-.6],[cx+.6,cz-.6],[cx+.6,cz+.6],[cx-.6,cz+.6]];wellHoles.push(sq);walls(sq,15,.2,-15,"dam",true,stone);slab(sq,.2,-15.2,plaster,"dam");
   // Steps down the whole western side, south of the settling basin; count and run are illustrative.
   const [sx,sz]=c([7,27]);const flight=steps(sx,sz,40,14,14,40,"south-pool");flight.position.y=-14;flight.rotation.y=Math.PI;
   walls(r(1,1,6,6),2.6,.5,-14,"settling-basin");
   const [kx,kz]=c(E(95,20));shaft(kx,kz,3,8.5,"cistern-1");
   for(const [x0,z0,x1,z1,depth,id] of grottoes)basin(r(x0,z0,x1,z1),depth,id,rock);
   const [gx,gz]=c(E(106.3,20));const g5=steps(gx,gz,1.5,.6,1.5,4,"grotto-5");g5.position.y=-1.5;g5.rotation.y=Math.PI;
   const [tx,tz]=c(E(98.8,24.9));const sill=box(tx,tz,1.3,.55,.16,0,"threshold");sill.rotation.y=-.46;box(tx-.75,tz-.3,.4,.4,1.2,0,"threshold");
   plinth(128,128,14,[north,south,...grottoes.map(([x0,z0,x1,z1])=>r(x0,z0,x1,z1))]);
  }
  for(const [id,x,z,y] of [["north-pool",20,-33,.6],["dam",20,-3.25,1],["canal",20,10,royal?-11:.6],["south-pool",20,22,.6],["settling-basin",3.5,3.5,-12.8],["cistern-1",95,20,.6],["threshold",98.8,24.9,.6],["grotto-6",101.75,27.75,.6],["grotto-5",106.75,20,.6],["first-installation",95,11.5,.6]] as [string,number,number,number][]){const [x2,z2]=c(eastern.has(id)?E(x,z):[x,z]);marker(id,x2,z2,y);}
  assumptions.push("Northern pool 53 × 40 m (Gibson). Pierre & Rousée 1981 (p. 24) give the dam as about 40 m long; because the dam forms the pool's south side, the 40 m side is drawn east–west and the 53 m side north–south (inference). The north pool's extent is otherwise unknown: only its south-east corner is assured (p. 25). Its depth is not given in the sources read; 10 m is about 21,200 m³ divided by its area, an inference.","Southern pool sides about 45 m north, 50 m east, 65 m south and 47 m west, up to 14 m deep (Duprez); the outline assumes a straight east–west north side and a north–south west side. The dam is 6.5 m wide (Duprez 6.50 m at the top; Gibson 6–6.5 m; Pierre & Rousée 6 m at the top and more than 7 m at the base).","The shaft is drawn square, about 1 × 1 m (Duprez; Pierre & Rousée p. 24), 15 m deep after Duprez; von Wahlde gives 12 m. Its small openings to the northern pool (20 × 15 cm every 2 m) are not drawn.","Pool and dam faces are drawn as laid ashlar in courses of about 60 cm (Duprez p. 34); Pierre & Rousée give about 50 cm. The dam's rock base is drawn separately only in the royal-period view.","Byzantine and Crusader churches and later structures are omitted. The model makes no claim about a deposit point.","Placement in the mapped setting: Pierre & Rousée 1981 Fig. 2 (detail plan, without a scale bar) is registered to satellite imagery (Vantor Legion, 3 January 2025; Esri World Imagery, 0.34 m, stated accuracy 8.5 m) by matching its drawn structures to the imagery's edges. The dam's centre stands about 21 m west and 4 m north of the centroid of the mapped site outline used before, and its axis runs 10.4° north of east (about ±4°: the imagery fixes the turn only between about 5° and 12°; the mapped ruins run 13–16°). A second fit, through Schick's 1888 plan registered to St Anne's church, the city wall and Lions' Gate, puts the dam's centre within 0.7 m of this one, with a turn of 5.3°. At either fit's scale the drawn dam is 6.3–6.6 m wide and 38–42 m long, as published. Schick's two pools are Fig. 2's medieval cistern and the cistern under the Moustier, against the dam's north face (inference). Record: research/assets/plans/imagery-registration-2026-10-22/bethesda.json.");
  if(royal)assumptions.push("Royal-period view after Pierre & Rousée 1981 (pp. 24–25, Fig. 3, Pl. 1): they date the dam, the north pool and the open canal to the Judahite monarchy and the south basin to the Hellenistic period (Simon II, 220–195 BCE). The south basin, its steps and settling basin and the eastern complex are left out. The valley in front of the dam is drawn only by this view (pale), inside the later basin's outline: its natural shape is not known.","Levels are relative and partly inferred: dam top 0; the corridor (2 m high, 0.8 m wide drawn) leaves the shaft foot at the north pool's floor (10 m down); the canal floor is 3 m below the corridor (\"drops about 3 m\"), so the valley floor is drawn 12 m below the dam top, within the dam's reported maximum height of 13 m. The rock base is drawn 2 m high and the 20 courses as one 10 m mass; the courses' set-backs are not drawn. The canal is drawn straight south from the corridor for 46 m, to the later basin's edge (about 50 m known).");
  else assumptions.push("The western steps follow Gibson's report of steps along the whole western side; their count, run, width and the absence of landings are illustrative. The settling basin's 2.6 m east wall is Duprez's; its size and place in the corner are illustrative.","Eastern complex: cistern 1 (about 8.5 m deep, 6 m across), grotto 5 (1.5 × 2 × 1.5 m, four steps) and basin 4 (about 30 cm deep) use Duprez's dimensions. Other sizes and the positions inside the complex follow the arrangement of Duprez Pl. II, whose scale is not recorded. The complex is drawn as one block in the 'Grottes' area that Pierre & Rousée 1981 Fig. 2 draws 2–18 m east of the dam's east end, across the dam's line; that these are Duprez's grottoes is an inference, and the block's place inside that area is schematic. The grottoes are roofed caves, drawn open.","Pierre & Rousée 1981 describe the Hellenistic rebuilding: the corridor at the shaft foot was deepened about 2 m so that the water passed under the dam, and the canal was vaulted (three voussoirs) under the south basin with about 2 m of fill over the vault (p. 25). These are not drawn: with Duprez's 14 m basin depth the canal's level cannot be placed from the reported figures.");
 } else if(plan.id==="east-gate-warren"){
  units="metres";note="Golden Gate · Warren’s levels and gallery, Plate VI frame";
  // Plate VI frame in metres: origin at the gate outline's centre, x to plate right (≈ east), z to plate down.
  // Levels: y = 0 at the Haram surface by cistern XV (2,408 ft); Warren's feet × 0.3048 below it.
  const ft=(level:number)=>(level-2408)*.3048,wallX=11.5,outside=ft(2389),shaftTop=ft(2333.5),gz=9.1,sx=53.48;
  // Warren's levels as a stylised step: the outside ground at the gallery shaft, the ground at the wall's
  // foot, and the Haram surface. The model's parts are placed on it. In the mapped setting the same pads
  // are confined to the model's neighbourhood and feathered into the modern terrain.
  const warrenPads=[{x:wallX+150,z:0,w:300,d:600,height:shaftTop,feather:.5},{x:wallX+.5,z:0,w:1,d:600,height:outside,feather:42},{x:wallX-150,z:0,w:300,d:600,height:0,feather:.5}];
  if(siteContext(plan.id))ground.pads.push({x:wallX+35,z:0,w:70,d:140,height:shaftTop,feather:12},{x:wallX+.5,z:0,w:1,d:140,height:outside,feather:42},{x:wallX-80,z:0,w:160,d:180,height:0,feather:4});
  else ground.pads.push(...warrenPads);
  const surface=(x:number,z:number)=>{let y=-.28;for(const p of warrenPads){const d=Math.max(Math.abs(x-p.x)-p.w/2,Math.abs(z-p.z)-p.d/2,0),t=T.MathUtils.clamp(d/p.feather,0,1);y=T.MathUtils.lerp(y,p.height,1-t*t*(3-2*t));}return y;};
  const gate:Point[]=[[-12.39,-8.65],[12.39,-8.65],[12.39,8.65],[-12.39,8.65]],sill=ft(2396);
  slab(gate,.3,sill-.3,stone,"gatehouse");walls(gate,12,2.2,sill,"gatehouse");slab(gate,.6,sill+12,stone,"gatehouse");
  // Haram wall from just below the outside ground to an illustrative parapet. Its buried
  // foundation (Warren: 30–40 ft below the outside surface) is not drawn.
  for(const [a,b] of [[-45,-8.65],[8.65,45]])walls([[wallX-1.25,a],[wallX-1.25,b]],2.5-(outside-.6),2.5,outside-.6,"east-wall",false);
  // Cistern XV: rock-roofed chamber with one square shaft entrance (entrance size illustrative).
  const xv=[-42.4,-12.44] as Point;shaft(xv[0],xv[1],2.75,10.67,"cistern-xv");
  slab(circlePoints(xv[0],xv[1],2.95),.45,-.45,rock,"cistern-xv",root,[[[xv[0]-.5,xv[1]-.5],[xv[0]+.5,xv[1]-.5],[xv[0]+.5,xv[1]+.5],[xv[0]-.5,xv[1]+.5]]]);
  const warren=root.children.length;shaft(sx,gz,.8,7.77,"gallery");root.children.slice(warren).forEach(m=>m.position.y+=shaftTop);
  // Gallery floor rise reported by Warren: 8 ft at 37 ft and 25 ft 6 in at 85 ft from the shaft.
  const rise=(d:number)=>d<10.25?0:d<37?(d-10.25)/(37-10.25)*8:d<85?8+(d-37)/48*17.5:25.5+(d-85)*.365;
  const floor=(x:number)=>ft(2308)+rise((sx-x)/.3048)*.3048;
  for(let x=sx-.6;x>27.4;x-=1.5){const x1=Math.max(27.4,x-1.5),y=floor((x+x1)/2);coveredPassage([new T.Vector3(x,y,gz),new T.Vector3(x1,y,gz)],"gallery");}
  // Display cutaway along the gallery; it is not an excavation.
  const cut:Point[]=[[25.2,gz-2.6],[56,gz-2.6],[56,gz+2.6],[25.2,gz+2.6]],base=ft(2308)-1;
  slab(cut,.4,base-.4,rock);
  // Each side is one profile (base to the interpolated surface), so the walk octree gets no stacked coplanar faces.
  for(const side of [-1,1]){const zEdge=gz+side*2.6,profile=new T.Shape();profile.moveTo(25.2,base);profile.lineTo(56,base);
   for(let x=56;x>=25.2;x-=.7)profile.lineTo(x,surface(x,zEdge)+.08);profile.lineTo(25.2,surface(25.2,zEdge)+.08);profile.closePath();
   const g=new T.ExtrudeGeometry(profile,{depth:1.2,bevelEnabled:false});const m=mesh(g,rock);m.position.z=side>0?zEdge:zEdge-1.2;}
  for(const x of [24.6,56.6])box(x,gz,1.2,7.6,surface(x,gz)+.2-base,base,undefined,rock);
  const mw:Point[]=[[21.75,-7.67],[23.96,-5.33],[25.78,-2.47],[26.69,.78],[26.95,4.03],[27.4,9.1],[27.7,13.4]];
  for(let i=1;i<mw.length;i++){const a=mw[i-1],b=mw[i],top=surface((a[0]+b[0])/2,(a[1]+b[1])/2);walls([a,b],top-(ft(2338.5)-1.5),2,ft(2338.5)-1.5,"massive-wall",false);}
  const col=mesh(new T.CylinderGeometry(.46,.46,1.6,24),stone,"column");col.position.set(32.75,floor(32.75)+.91+.8,gz-1.6);
  for(const [id,x,z,y] of [["gatehouse",0,0,sill+13],["east-wall",wallX,-25,3],["cistern-xv",xv[0],xv[1],.6],["massive-wall",25.8,-2.5,surface(25.8,-2.5)+1],["gallery",40,gz,floor(40)+1],["tank-tomb",47.84,gz,floor(47.84)+1],["column",32.75,gz-1.6,floor(32.75)+2.6]] as [string,number,number,number][])marker(id,x,z,y);
  plinth(130,100,2,[gate,cut]);
  assumptions.push("Plan positions are measured on Warren's Plate VI with its own scale bar (2.344 px per ft); the outline of the Golden Gate (24.8 × 17.3 m), cistern XV (18 ft across, 30.0 m west of the gatehouse) and the massive wall follow the plate. The frame is the plate's, about 9° from north, without geographic registration. Archive: research/assets/plans/warren1884-plate-vi.","Levels follow Warren's feet: Haram surface 2,408 at cistern XV (rock 2,393 plus 15 ft), sill 2,396, ground outside the gate about 2,389, shaft top about 2,333.5 and bottom 2,308. The level 2,389 and the shaft's identification with the plate's 2308 square are inferences. The ground between these levels is a smooth interpolation, not surveyed relief.","The gatehouse's height, roof, wall thickness and twin passages are illustrative; it is drawn as a closed block. The Haram wall is drawn straight, 2.5 m thick, from the outside ground to an illustrative parapet; its foundation, which Warren found to extend 30–40 ft below the outside surface, is not drawn.","Warren's gallery is drawn in a display cutaway trench. Its section, the shaft's round form and the steps of its floor are illustrative; the floor rise follows the reported 8 ft at 37 ft and 25 ft 6 in at 85 ft. The tank or tomb is marked only. The column is drawn beside the gallery so that it can be seen.","The massive wall is drawn 2 m thick from about 5 ft below its plate level of 2,338.5 up to the present surface, as SWP thinks probable; its base and thickness are unknown, and the plate places it about 8 ft further from the Haram wall than the text's 46 ft.");
 } else if(plan.id==="kidron-bene-hezir"){
  units="metres";const original=options.layer==="avigad";
  note=original?"Bene Ḥezir before its later breaches, with Avigad’s nefesh pyramid (reconstruction)":"Bene Ḥezir and Zechariah · Avigad 1954 measurements";
  // Avigad's frame: x his east, z his south, origin at the centre of the Doric façade. He states only
  // main directions. The frame is placed and turned by the OpenStreetMap outlines of the three
  // monuments (tools/build_osm_context.py): his porch centre (2.1, 0) on the mapped porch, his 'west'
  // along the mapped façade normal. y = 0 in the frame is the rock path at the foot of the cliff, set to
  // the modern ground at Absalom's mapped centre; the tomb floor F is 8.50 m above it (p. 42).
  const reg=siteContext(plan.id)!.registration as {porchCentre:Point;frameRotationDeg:number;facadeNormalBearing:number;absalomCentre:Point;absalomSideBearing:number;zechariahCentre:Point};
  const patch=placeTerrain(plan.placeIds[0],options.terrain),base=patch?elevationAt(patch,...reg.absalomCentre):0,turn=T.MathUtils.degToRad(reg.frameRotationDeg);
  const porchOffset=new T.Vector3(2.1,0,0).applyAxisAngle(new T.Vector3(0,1,0),turn);
  const tomb=new T.Group();tomb.rotation.y=turn;tomb.position.set(reg.porchCentre[0]-porchOffset.x,base,reg.porchCentre[1]-porchOffset.z);root.add(tomb);tomb.updateMatrix();
  const F=8.5,TOP=F+7,CW=F+8.4,at=(x:number,y:number,z:number)=>new T.Vector3(x,y,z).applyMatrix4(tomb.matrix);
  const S=(x0:number,x1:number,z0:number,z1:number,y0:number,y1:number):Space=>[x0,x1,z0,z1,y0,y1];
  // A rock-cut cube of side `side` from y0, `h` high, with corner pilasters and `n` engaged Ionic columns
  // (base, shaft and a cushion capital) on each face.
  function classicalCube(parent:T.Group,side:number,y0:number,h:number,n:number,r:number,id:string,mat:T.Material){
   box(0,0,side,side,h,y0,id,mat,parent);
   for(const sx of [-1,1])for(const sz of [-1,1])box(sx*(side/2-.27),sz*(side/2-.27),.7,.7,h,y0,id,mat,parent);
   const gap=(side-1.1)/(n+1),half=side/2;
   for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]])for(let k=1;k<=n;k++){
    const t=-side/2+.55+k*gap,x=dx*(half+r*.4)+dz*t,z=dz*(half+r*.4)+dx*t;
    const foot=mesh(new T.CylinderGeometry(r*1.3,r*1.35,.22,20),mat,id,parent);foot.position.set(x,y0+.11,z);
    const shaft=mesh(new T.CylinderGeometry(r*.9,r,h-.62,20),mat,id,parent);shaft.position.set(x,y0+.22+(h-.62)/2,z);
    box(x,z,dx?r*2:r*3.2,dx?r*3.2:r*2,.4,y0+h-.4,id,mat,parent);
   }
  }
  // An Egyptian (cavetto) cornice: a square band flaring from `bottom` to `top` wide over height h.
  function cavetto(parent:T.Group,bottom:number,top:number,y:number,h:number,id:string,mat:T.Material){
   const m=mesh(new T.CylinderGeometry(top/Math.SQRT2,bottom/Math.SQRT2,h,4,1),mat,id,parent);m.rotation.y=Math.PI/4;m.position.set(0,y+h/2,0);
  }
  const kokh=(axis:'x'|'z',from:number,dir:1|-1,centre:number,mouth:number,width:number,length:number):Space[]=>{
   const m=Math.min(.3,length*.15),a=[from,from+dir*m].sort((p,q)=>p-q),b=[from+dir*m,from+dir*length].sort((p,q)=>p-q);
   return axis==='x'?[S(a[0],a[1],centre-mouth/2,centre+mouth/2,F,F+.9),S(b[0],b[1],centre-width/2,centre+width/2,F,F+.9)]:[S(centre-mouth/2,centre+mouth/2,a[0],a[1],F,F+.9),S(centre-width/2,centre+width/2,b[0],b[1],F,F+.9)];
  };
  const spaces:Space[]=[
   S(-1.6,0,-7.005,2.875,F,TOP+1),                  // platform in front of both façades (0.90–2.09 m deep)
   S(-1.5,-.7,-5.6,-4.8,F-3.6,F-2.4),S(-1.5,-.7,1.2,2,F-3.6,F-2.4),  // two openings in the scarp below the façade (Fig. 25)
   S(0,.55,-2.575,2.575,F,F+3),                     // between the antae, under the architrave
   S(.55,3.7,-2.85,2.85,F,F+3.35),                  // porch, 5.55–5.83 × 3.04–3.23 m, 3.20–3.50 m high
   S(3.7,4.5,-1.2,1.2,F,F+2.2),                     // the present wide opening into A (not original)
   S(4.5,8,-2.4,2.4,F,F+2.2),                       // chamber A, 4.20–5.40 × 3.17–3.85 m, 2.20 m high
   S(5.2,7.3,-3.2,-2.4,F,F+1.5),                    // later breach that took the north doorway
   S(4.575,7.925,-6.7,-3.2,F,F+1.5),S(5.4,7.1,-5.74,-3.2,F-.5,F),   // B, 3.35 × 3.50 × 1.50 m, pit 1.70 × 2.54 m
   ...kokh('z',-6.7,-1,5.3,.55,1.25,2.1),...kokh('z',-6.7,-1,7.15,.6,1.2,2.1),...kokh('x',7.925,1,-6.2,.5,.8,2.2),
   S(5.915,6.585,2.4,3.2,F,F+1.56),                 // doorway to C, 0.67 × 1.56 m
   S(4.45,8.05,3.2,7.2,F,F+1.1),S(5.5,7,3.2,6,F-.86,F),           // C, 4.00 × 3.60 m, pit 1.50 × 2.80 m
   ...[3.85,5.2,6.55].flatMap(z=>kokh('x',8.05,1,z,.58,1.1,2.1)),...kokh('z',7.2,1,6.25,.58,1.1,2.1),
   S(8,8.85,-.335,.335,F,F+1.5),                    // doorway to D
   S(8.85,12.37,-1.9,1.9,F,F+1.95),S(9.585,11.635,-1.025,1.025,F-.77,F),  // D, pit 2.05 m square, 77 cm deep
   S(10.3,11,1.9,2.6,F,F+.9),                       // unfinished kokh, south wall
   S(10.335,10.885,-2.2,-1.9,F,F+.85),S(9.935,11.285,-4.2,-2.2,F,F+1),   // north-wall cell, opening 0.55 × 0.85 m
   ...kokh('x',12.37,1,-1.285,.5,1.23,2.34),        // east-wall cell 1.23 × 2.34 m
   S(12.37,13.17,1.3,1.91,F,F+1.2),                 // opening 0.61 × 1.20 m into E
   S(13.17,15.37,.6,2.63,F,F+1.75),                 // E, 2.03 × 2.20 m, 1.75 m high
   S(13.3,15.25,0,.6,F+.65,F+1.72),S(15.37,15.97,.64,2.59,F+.65,F+1.72),S(13.3,15.25,2.63,3.23,F+.65,F+1.72),  // arcosolia
   S(0,.25,-5.905,-3.975,F,F+3.6),S(.25,1.55,-5.33,-4.55,F+.6,F+2.25),     // nefesh: recess 1.93 m, niche 0.78 × 1.65 × 1.30 m
   S(.85,1.2,-5.115,-4.765,F-.2,F+.6),S(.4,2.4,-5.44,-4.44,F-1.4,F-.2),    // hole in the niche floor; cell 1.00 × 2.00 m below
   S(1.3,2.9,-2.85,-1.85,F+3.35,TOP+1),             // the stair shaft breaks into the porch ceiling
   ...Array.from({length:22},(_,k)=>S(1.3,2.9,-3.13-k*.28,-2.85-k*.28,F+1.78+k*.2417,TOP+1)),  // north stair, 1.60 m wide
   S(1.545,2.705,2.85,3.35,F,F+3),                  // south corridor: jamb opening 1.16 m
   ...([[3.35,4.85,.21],[4.85,5.15,.42],[5.15,9.85,.63],[9.85,10.15,.84],[10.15,10.45,1.05],[10.45,10.75,1.26],[10.75,11.05,1.51],[11.05,11.15,1.75]] as [number,number,number][]).map(([z0,z1,d])=>S(.975,3.275,z0,z1,F-d,F-d+3.5)),
   S(1.45,2.8,11.15,11.48,F-2,F+.5),                // opening into the Zechariah court, 1.35 m wide
   S(-1.6,10.625,11.48,22.46,F-2.6,TOP+1),          // Zechariah court, open to the west
  ];
  if(original)spaces.push(S(0,4.13,-7.005,-2.875,F+4,TOP+1));  // rock cleared above the nefesh façade for the pyramid
  rockMass(S(-1.5,20,-13,26,-1,TOP),spaces,tomb);
  // The court walls are "as high as the monument" (p. 79): on Fig. 25 they rise to about 16–17.5 m above
  // the path, so the rock round the court is carried up to CW.
  rockMass(S(-1.5,20,9.5,26,TOP,CW),[S(-1.6,10.625,11.48,22.46,TOP-1,CW+1)],tomb);
  box(-3.09,10.98,3.17,1,CW+1,-1,"zechariah",rock,tomb);  // the court's north rock wall runs on to 15.30 m
  // Doric columns in antis: lower diameter 0.53–0.55 m, upper 0.48 m, shaft 2.82 m, capital 0.18 m, abacus about 0.90 m.
  for(const z of [1.03,-.86]){const c=mesh(new T.CylinderGeometry(.24,.27,2.82,20),rock,"porch",tomb);c.position.set(.275,F+1.41,z);box(.275,z,.9,.9,.18,F+2.82,"porch",rock,tomb);}
  // Doric entablature over the columns (p. 44): architrave 0.39 m, frieze 0.23 m with triglyphs, cornice
  // 0.335 m, to 3.95 m above the floor. How far each band stands proud of the rock is illustrative.
  box(-.04,0,.08,5.75,.39,F+3,"bene-hezir-facade",rock,tomb);box(-.02,0,.04,5.75,.23,F+3.39,"bene-hezir-facade",rock,tomb);
  for(let k=0;k<7;k++)box(-.06,-2.55+k*.85,.12,.3,.23,F+3.39,"bene-hezir-facade",rock,tomb);
  box(-.17,0,.34,6.1,.335,F+3.62,"bene-hezir-facade",rock,tomb);
  // Present fill in the court (modern graves). On Fig. 25 the graves reach Zechariah's visible foot about
  // 7.7 m above the path (F − 0.8); the fill is drawn in terraces from the court mouth up to that level.
  for(const [x0,x1,top] of [[-1.6,-.3,F-2.5],[-.3,1,F-1.65],[1,10.625,F-.8]])box((x0+x1)/2,16.97,x1-x0,10.98,top-(F-2.6),F-2.6,undefined,earth,tomb);
  // Zechariah: a monolith 5.50–5.60 m square; 2.75–3.08 m from the north rock wall, 2.95 m from the east, 2.68 m from the south (p. 79).
  // Its parts as seen today (owner's photographs): a stepped base, two engaged Ionic columns between corner
  // pilasters on each face, an architrave, an Egyptian (cavetto) cornice and the pyramid. Heights follow
  // Fig. 25 above its visible foot (F − 0.8): capitals to 3.6 m, architrave to 4.3 m, cornice to 5.05 m,
  // pyramid 4.05 m high on a 5.1 m base. The buried base steps and the cornice's projection are illustrative.
  {const zc=new T.Group();zc.position.set(4.9,0,17.005);tomb.add(zc);
   box(0,0,5.55,5.55,5.79,F-3,"zechariah",rock,zc);box(0,0,6.25,6.25,.3,F-1.6,"zechariah",rock,zc);box(0,0,5.9,5.9,.3,F-1.3,"zechariah",rock,zc);
   classicalCube(zc,5.55,F-1,3.79,2,.27,"zechariah",rock);
   box(0,0,5.7,5.7,.72,F+2.79,"zechariah",rock,zc);
   cavetto(zc,5.7,6.1,F+3.51,.5,"zechariah",rock);box(0,0,6.1,6.1,.25,F+4.01,"zechariah",rock,zc);pyramid(0,0,5.1,4.05,F+4.26,rock,"zechariah",zc);}
  if(original){
   // Avigad's original state: the porch doorway about 0.80 m wide on the column axis (p. 38); the north
   // doorway of A (lost in a breach); the pit in D 50 cm deep before it was deepened (p. 41); the corridor
   // cleared to the steps that Slouschz saw; and the nefesh completed by a pyramid (Fig. 42, 1; pp. 73–78).
   for(const [x0,x1,z0,z1,y0,y1] of [[3.7,4.5,-1.2,-.4,F,F+2.2],[3.7,4.5,.4,1.2,F,F+2.2],[3.7,4.5,-.4,.4,F+1.7,F+2.2],[5.2,5.925,-3.2,-2.4,F,F+1.5],[6.575,7.3,-3.2,-2.4,F,F+1.5],[5.925,6.575,-3.2,-2.4,F+1.4,F+1.5],[9.585,11.635,-1.025,1.025,F-.77,F-.5]] as Space[])box((x0+x1)/2,(z0+z1)/2,x1-x0,z1-z0,y1-y0,y0,"chambers",restored,tomb);
   pyramid(2.065,-4.94,4.13,5,F+4,restored,"nefesh",tomb);
  }else{
   // The last corridor steps lie under earth (p. 39).
   for(const [x0,x1,z0,z1,y0] of [[.975,3.275,10.75,11.05,F-1.51],[.975,3.275,11.05,11.15,F-1.75],[1.45,2.8,11.15,11.48,F-2]] as [number,number,number,number,number][])box((x0+x1)/2,(z0+z1)/2,x1-x0,z1-z0,F-1.26-y0,y0,"corridor",earth,tomb);
  }
  // Absalom, about 50 m from Bene Ḥezir (p. 37), north of it on Fig. 25, stands at its mapped centre with its
  // sides on the mapped outline. Avigad's summary gives its 20 m height and its parts: a rock-cut square
  // substructure, a course of dressed stone, a round drum and a concave cone. The heights of the parts are
  // read from the Fig. 25 elevation, scaled to the 20 m (the record has the measurements); the members'
  // detail follows the owner's photographs.
  const absalom=new T.Group();absalom.position.set(reg.absalomCentre[0],base,reg.absalomCentre[1]);absalom.rotation.y=-T.MathUtils.degToRad(reg.absalomSideBearing);root.add(absalom);absalom.updateMatrix();
  {// Rock-cut: a podium from the path to 2.1 m with a base moulding to 2.4 m, the cube with two engaged
   // Ionic columns between corner pilasters on each face (to 7.0 m), architrave, Doric frieze with
   // triglyphs (7.3–7.9 m) and an Egyptian cornice to 8.8 m.
   box(0,0,7,7,2.4,-.3,"absalom",rock,absalom);box(0,0,7.2,7.2,.32,2.07,"absalom",rock,absalom);
   classicalCube(absalom,6.8,2.39,4.6,2,.3,"absalom",rock);
   box(0,0,7.05,7.05,.3,6.99,"absalom",rock,absalom);box(0,0,6.95,6.95,.62,7.29,"absalom",rock,absalom);
   for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]])for(let k=-4;k<=4;k++)box(dx*3.5+dz*k*.75,dz*3.5+dx*k*.75,dx?.1:.32,dx?.32:.1,.62,7.29,"absalom",rock,absalom);
   cavetto(absalom,6.95,7.5,7.91,.71,"absalom",rock);box(0,0,7.5,7.5,.18,8.62,"absalom",rock,absalom);
   // Built: the square course of dressed stone (8.8–10.2 m) with its crowning moulding (to 10.9 m), the
   // round drum with a band and a rope moulding (to 13.3 m), and the concave cone with its finial (to 20 m).
   box(0,0,6.25,6.25,1.42,8.8,"absalom",stone,absalom);box(0,0,6.35,6.35,.38,10.22,"absalom",stone,absalom);box(0,0,6.45,6.45,.32,10.6,"absalom",stone,absalom);
   const drum=mesh(new T.CylinderGeometry(3.05,3.05,2.03,32),stone,"absalom",absalom);drum.position.set(0,11.935,0);
   const band=mesh(new T.CylinderGeometry(3.12,3.12,.31,32),stone,"absalom",absalom);band.position.set(0,12.345,0);
   const rope=mesh(new T.TorusGeometry(3.05,.18,8,40),stone,"absalom",absalom);rope.rotation.x=Math.PI/2;rope.position.set(0,13.12,0);
   const profile=Array.from({length:17},(_,k)=>{const t=k/16;return new T.Vector2(.42+2.67*(1-t)**2.1,13.3+5.75*t);});
   mesh(new T.LatheGeometry(profile,32),stone,"absalom",absalom);
   mesh(new T.LatheGeometry([[.45,19.05],[.5,19.1],[.5,19.3],[.3,19.36],[.38,19.6],[.36,19.85],[.18,19.98],[0,20]].map(([r,y])=>new T.Vector2(r,y)),20),stone,"absalom",absalom);}
  {// The rock-cut court around Absalom, open to the west, with a passage 2.4 m wide on three sides; its
   // walls are drawn to 9 m (on Fig. 25 the rock and the walls on it rise to 8–10.5 m). In the east
   // wall, north of the axis, the pedimented entrance of the Jehoshaphat tomb (summary: "a large entrance
   // carrying a pediment", reached by "a flight of steps touching 'Absalom's Tomb'"). On Fig. 25 its sill
   // is level with Absalom's base moulding (1.9 m), its opening about 2.5 m wide and 3 m high, its
   // pediment to 5.9 m; the steps rise east beside the podium. The cave behind is not drawn.
   rockMass([-4.6,14,-12,12,-4,9],[[-4.6,7,-7,7,0,9.1],[7,8.6,-5.9,-3.6,1.9,4.9],[8.6,12,-6.6,-2.9,1.9,4.6]],absalom,"absalom");
   box(1.2,0,11.6,14,.25,-.23,undefined,earth,absalom);
   for(let k=0;k<9;k++)box(4.28+k*.32,-5.15,.32,2.9,.211*(k+1),0,"absalom",rock,absalom);
   for(const z of [-6.05,-3.45])box(6.92,z,.16,.3,3,1.9,"absalom",rock,absalom);
   box(6.9,-4.75,.2,3.1,.3,4.9,"absalom",rock,absalom);
   const pediment=new T.Shape();pediment.moveTo(-1.55,0);pediment.lineTo(1.55,0);pediment.lineTo(0,.65);pediment.closePath();
   const tympanum=mesh(new T.ExtrudeGeometry(pediment,{depth:.25,bevelEnabled:false}),rock,"absalom",absalom);tympanum.rotation.y=Math.PI/2;tympanum.position.set(6.8,5.2,-4.75);}
  const put=(id:string,v:T.Vector3)=>marker(id,v.x,v.z,v.y);
  put("bene-hezir-facade",at(-.4,F+4.4,0));put("porch",at(2.1,F+1.6,0));put("chambers",at(6.25,F+1.2,0));put("corridor",at(2.1,F+.8,7));put("nefesh",at(.2,F+(original?6.5:2.4),-4.94));put("zechariah",at(4.9,F+5.5,17));marker("absalom",reg.absalomCentre[0],reg.absalomCentre[1],base+21);
  // Ground: the terrain is hidden under the rock mass. Pads, applied in order, level the valley floor
  // in front (from Zechariah's court to Absalom), raise the slope behind the scarp to the rock surface,
  // and meet the rock mass itself. The modern terrain model is too coarse to show the scarp, so the
  // pads are illustrative.
  const flat=(x:number,z:number):Point=>{const v=at(x,0,z);return [v.x,v.z];};
  // The terrain holes stop 0.8 m inside the rock's sides and back, where the ground stands at the rock top:
  // the cut follows whole terrain cells, and a cut outside the rock would open a gap beside it.
  const rockHole=[flat(-1.5,-12.2),flat(19.2,-12.2),flat(19.2,25.2),flat(-1.5,25.2)];
  const front=flat(-2,17),foot:Point=[reg.absalomCentre[0]-4,reg.absalomCentre[1]],along=new T.Vector2(foot[0]-front[0],foot[1]-front[1]),length=along.length();along.normalize();
  const west=along.y<0?new T.Vector2(along.y,-along.x):new T.Vector2(-along.y,along.x),valley=[(front[0]+foot[0])/2+west.x*11,(front[1]+foot[1])/2+west.y*11];
  ground.pads.push({x:valley[0],z:valley[1],w:26,d:length+20,height:base,feather:18,angle:Math.atan2(along.x,along.y)});
  // "Here the path climbs to the southern entrance of the Bene Ḥezir cave and the Zechariah court" (p. 42),
  // over a slope built up by modern graves. On Fig. 25 the ground in front of the scarp leaves the path
  // about 5 m north of the façade's north end and is 4.6 m up at the end of the court's north wall; it rises on to
  // about 6.7 m at the court's south wall, and the graves in the court reach Zechariah's foot (F − 0.8).
  // The ramps follow those levels; their width is illustrative.
  const ramp=flat(-6.8,-.35),approach=flat(-6.8,17),terrace=flat(-6.8,28);
  ground.pads.push({x:ramp[0],z:ramp[1],w:10.4,d:22.7,height:base,rise:4.6,feather:5,angle:turn},{x:approach[0],z:approach[1],w:10.4,d:12,height:base+4.6,rise:2.1,feather:6,angle:turn},{x:terrace[0],z:terrace[1],w:10.4,d:10,height:base+6.7,feather:10,angle:turn});
  // The rock pad starts 4.5 m behind the façade line: the terrain cells (about 4 m) would otherwise
  // slope up across the façade. It runs on 14 m south of the rock mass, past Zechariah, as the scarp
  // does. To the north the scarp bends east towards Absalom (the mapped path at its foot runs there),
  // so a shoulder further back covers the north side. The rock mass is then no free block.
  const behind=flat(28,5),shoulder=flat(15,-17),scarp=flat(11.5,14);
  ground.pads.push({x:behind[0],z:behind[1],w:24,d:58,height:base+TOP-.3,feather:20,angle:turn},{x:shoulder[0],z:shoulder[1],w:12,d:14,height:base+TOP-.3,feather:4,angle:turn},{x:scarp[0],z:scarp[1],w:17,d:52,height:base+TOP-.3,feather:2.5,angle:turn});
  // The higher rock round Zechariah's court. The pad stays 5.5 m behind the court mouth, and 3 m south of
  // the step from the lower rock, so no ground rises above the rock top at a hole edge.
  const courtTop=flat(17.5,20.75);
  ground.pads.push({x:courtTop[0],z:courtTop[1],w:27,d:16.5,height:base+CW-.3,feather:3,angle:turn});
  // Absalom: level ground (the path) in front, no terrain inside its rock-cut court, and the ground
  // behind the court at the rock top.
  const local=(x:number,z:number):Point=>{const v=new T.Vector3(x,0,z).applyMatrix4(absalom.matrix);return [v.x,v.z];},spin=absalom.rotation.y;
  const absalomHole=[local(-4.6,-11.2),local(13.2,-11.2),local(13.2,11.2),local(-4.6,11.2)],aroundAbsalom=local(11.7,0),plaza=local(-11.3,0);
  ground.pads.push({x:aroundAbsalom[0],z:aroundAbsalom[1],w:32.6,d:36,height:base+8.7,feather:8,angle:spin},{x:plaza[0],z:plaza[1],w:13.4,d:26,height:base,feather:4,angle:spin});
  plinth(70,110,2,[rockHole,absalomHole]);ground.bench=false;
  placeFrame=[(reg.absalomCentre[0]+reg.zechariahCentre[0])/2,(reg.absalomCentre[1]+reg.zechariahCentre[1])/2];ground.focus=flat(0,8);
  // Start on the valley floor, far enough out to see the façade 8.5 m up.
  {const [x,z]=flat(-20,1);tracedStart={position:[x,z],bearing:(reg.facadeNormalBearing+180)%360,pitch:94};}
  assumptions.push("Plan, chamber and façade sizes are Avigad's (1954 pp. 37–49, 79): façade 5.75 + 4.13 = 9.88 m, porch 5.7 × 3.15 m and 3.35 m high, columns 3.00 m with 0.53 m lower diameter, entablature 0.95 m; chambers A–E, their pits, kokhim and arcosolia, the 1.60 m north stair (13 steps from 1.78 to 4.68 m above the floor) and the south corridor (8.30 m, 2.30 m wide, steps of 20–22 cm). Ranges are drawn at their means; trapezoidal chambers are drawn as rectangles.","Avigad gives no wall thicknesses, chamber floor levels or kokh heights: walls between chambers are drawn 0.8 m, all chamber floors at the porch floor with benches at that level, kokhim 0.9 m high, and the stair continued above its visible top to the rock surface. Which side of each chamber carries which dimension is inferred from the kokhim on each wall.","The façade's two parts meet at an obtuse angle (p. 37); they are drawn in one plane. The frame is Avigad's (his directions are rounded, p. 39), placed and turned by the OpenStreetMap outlines of the three monuments: his 'west' faces the mapped façade normal (about 245°, his 'south-west', p. 37), from the mapped outline and from the bearing that puts Zechariah where his plan does (the two agree within 1°). The rock path (y = 0 of the frame) is set to the modern terrain at Absalom's mapped centre. Levels: tomb floor 8.50 m above the rock path (p. 42; the Fig. 25 elevation, measured on the owner's photograph, gives 8.5 m); rock surface drawn 7 m above the floor (up to 8.00 m at the stair, p. 39; a wall 'about 15 m high', p. 42). The other levels are read from the Fig. 25 west elevation, whose ground line is that rock path: Zechariah's court walls to about 16.9 m, the ground climbing in front of the scarp to 4.6 m at the court's north wall and 6.7 m at its south wall, the court fill at Zechariah's foot 7.7 m. The two openings drawn in the scarp below the façade (4.9–6.1 m up; the burial cells of p. 38 n. 1 and Fig. 48) are cut 0.8 m deep; their depth is illustrative.","Zechariah: the 5.55 m square monolith and its passages (2.9 m north, 2.95 m east, 2.68 m south; court 11.45 × 10.98 m drawn, 11.20 × 11.45 m published) follow p. 79; the corridor opening is set 3.08 m from its north-west corner. Its parts follow the owner's photographs (a stepped base, two engaged Ionic columns between corner pilasters on each face, an architrave, an Egyptian cornice, the pyramid). Their heights are read from Fig. 25 (about ±0.3 m): visible from 7.7 m above the path, capitals to 3.6 m above that, architrave to 4.3 m, cornice to 5.05 m, pyramid 4.05 m high on a 5.1 m base, apex about 16.8 m above the path. Its base is buried (p. 79): the base steps under the fill and the cornice's projection are illustrative. The court walls are 'as high as the monument' (p. 79) and are drawn to 16.9 m. The fill in the court is drawn in terraces from the court mouth to Zechariah's foot; the ramps in front follow Fig. 25's ground line, and their width is illustrative.","Absalom stands at the centre of its mapped outline, 52 m from the mapped Bene Ḥezir porch (Avigad: about 50 m), its sides turned with the outline, on the path level. Its 20 m height and its parts are published in the pages read (a rock-cut substructure with Ionic columns, a Doric frieze and an Egyptian cornice, a course of dressed stone, a round drum and a concave cone). The heights of the parts and the widths of drum and cone are read from the Fig. 25 elevation, scaled to the 20 m: a podium to 2.1 m and a base moulding to 2.4 m, columns and capitals to 7.0 m, architrave and frieze to 7.9 m, cornice to 8.8 m, the stone course to 10.2 m with its moulding to 10.9 m, the drum (6.1 m across) to 13.0 m, the rope moulding to 13.3 m, the cone to 19.05 m and the finial to 20 m. The members' detail follows the owner's photographs and is illustrative. Its rock-cut court (a 2.4 m passage on three sides, open to the west) is illustrative in plan; its walls are drawn to 9 m (Fig. 25: 8–10.5 m with walls on top). The Jehoshaphat entrance in its east wall follows Fig. 25 in height: sill 1.9 m, level with Absalom's base moulding, opening about 2.3 m wide and 3 m high, pediment to 5.85 m, and nine steps beside the podium. The Jehoshaphat cave behind its entrance is not drawn.");
  if(original)assumptions.push("Original-state view (pale parts are drawn only by it): the porch doorway narrowed to Avigad's original 0.80 m (p. 38), the north doorway of A restored in its breach, the pit in D at its original 50 cm (p. 41), and the corridor cleared of earth. The nefesh pyramid follows Avigad's reconstruction (Fig. 42, 1; pp. 73–78), which publishes no dimensions: its 4.13 m base (the added façade's width) and 5 m height are illustrative. Avigad notes that the rock leaves no room for a square base without reaching over the steps behind the nefesh (p. 76); the model shows that overlap with the north stair rather than resolving it.");
 } else if(plan.id==="temple-great-sea"){
  units="metres";note="The Great Sea (cistern VIII) · Warren Pl. VII outline, published depths";
  // Warren 1884 Pl. VII traced at its own scale bar and turned by its north arrow (8.8°): x east, z south,
  // origin at the outline's vertex mean (research/assets/plans/warren1884-plate-vii). y = 0 is the Haram surface.
  const outline:Point[]=[[-2.11,-25.89],[-2.92,-22.6],[-9.36,-20.03],[-9.15,-15.32],[-19.96,-12.07],[-18.76,-4.36],[-16.23,-1.6],[-15.13,2.97],[-13.86,4.35],[-14.79,7.65],[-12.94,13.68],[-11.54,15.04],[-12.49,19.92],[-14.45,23.38],[-12.93,24.73],[-1.76,22.99],[15.73,18.69],[21.78,16.18],[22.31,14.51],[20,3.83],[18.62,.88],[16.2,-.32],[14.69,-3.24],[18.1,-10.09],[15.56,-12.85],[15.34,-15.97],[5.89,-19.24],[4.16,-25.28]];
  const floor=-14,ceiling=-4,surface=-.28,cut=-4;
  // Floor 14 m and rock roof about 2.5 m thick (Schick); rock 1.5 m below the surface (Warren); rock-cut and plastered.
  slab(outline,.3,floor-.3,plaster,"great-sea");
  // The walls run up to the surface, with a gap where the stair enters on the south.
  const g0:Point=[13.3,19.29],g1:Point=[14.7,18.94],i=outline.findIndex(p=>p[0]===15.73);
  walls([g1,...outline.slice(i),...outline.slice(0,i-1),outline[i-1],g0],surface-floor,.35,floor,"great-sea",false,plaster);
  // Five free-standing rock piers (Schick); Warren draws none, so their places and size are illustrative.
  for(const [x,z] of [[-3,-14],[8,-8],[-6,2],[8,8],[0,15]])box(x,z,3,3,ceiling-floor,floor,"piers",rock);
  // Shaft mouths: the one Warren draws, and two more of the three Wilson found in use (places illustrative).
  const mouths=[[2.37,13.14],[8,-15],[13,3]].map(([x,z]):Point[]=>[[x-.5,z-.5],[x+.5,z-.5],[x+.5,z+.5],[x-.5,z+.5]]);
  // Display cutaway: the roof is drawn only east of x = -4 m, so the chamber can be seen from above.
  const roofed=clipX(outline,cut);slab(roofed,2.5,ceiling,rock,"great-sea",root,mouths);slab(roofed,surface-(-1.5),-1.5,earth,"great-sea",root,mouths);
  // Stair from the south: 44 steps (Barclay) or 50 (Schick), narrow, entered from a well-like opening (Whitty).
  const N=50,rise=(surface-floor)/N,run=.28,top=19.1+N*run,stairs:Space[]=[[12.6,15.4,18,19.3,floor,ceiling]];
  for(let k=0;k<N;k++){const z1=top-k*run,y=surface-(k+1)*rise;stairs.push([13.4,14.6,z1-run,z1,y,k<6?1:y+2.2]);}
  rockMass([12.6,15.4,18,top+.5,floor-.3,surface],stairs,root,"stair");
  const stairHole:Point[]=[[12.6,18],[15.4,18],[15.4,top+.5],[12.6,top+.5]];
  for(const [id,x,z,y] of [["great-sea",2,0,-6],["mouth",2.37,13.14,.6],["piers",-6,2,-9],["stair",14,26,-5]] as [string,number,number,number][])marker(id,x,z,y);
  plinth(70,84,2,[outline,stairHole]);
  // Registered by the Haram's south corners (tools/build_osm_context.py): the plate frame is turned and moved
  // so that Warren's south wall lies on the mapped one. y = 0, the Haram surface, is the modern terrain there.
  const reg=siteContext(plan.id)?.registration as {origin:Point;rotationDeg:number;residuals_m:number[]}|undefined;
  if(reg){
   const patch=placeTerrain(plan.placeIds[0],options.terrain),base=patch?elevationAt(patch,...reg.origin):0,frame=new T.Group();
   frame.position.set(reg.origin[0],base,reg.origin[1]);frame.rotation.y=T.MathUtils.degToRad(reg.rotationDeg);frame.updateMatrix();
   for(const child of [...root.children])frame.add(child);root.add(frame);
   const move=(p:Point):Point=>{const v=new T.Vector3(p[0],0,p[1]).applyMatrix4(frame.matrix);return [v.x,v.z];};
   markers.forEach(v=>v.applyMatrix4(frame.matrix));ground.holes=ground.holes.map(h=>h.map(move));
   ground.pads.push({x:reg.origin[0],z:reg.origin[1],w:ground.w,d:ground.d,height:base-.28,feather:12,angle:frame.rotation.y});
   ground.bench=false;placeFrame=reg.origin;ground.focus=reg.origin;
   assumptions.push(`Position: Warren's plate is registered to the Haram's south-west and south-east corners as mapped by OpenStreetMap (residual ${reg.residuals_m[0].toFixed(1)} m at each corner; the plate's frame is turned ${reg.rotationDeg.toFixed(2)}°). The cistern's place under the court north of al-Aqsa follows from the plate; its outline keeps its own uncertainty of about ±2 m. The Haram surface over it is levelled to the modern terrain at the outline's centre.`);
  }
  assumptions.push("Outline: the hatched extent of cistern VIII on Warren 1884 Pl. VII, traced at the plate's own scale (0.130 m per pixel) and turned by its north arrow; 37.7 × 48.4 m and about 1,360 m² on the plate's axes, uncertain by about ±2 m. Gibson & Jacobson 1996 (p. 33) tabulate about 40 × 30 m (Schick) and 44 × 45 m (Pierotti). The plate draws no piers, stair or roof openings other than one mouth; its hatching may include the small chamber to the north-east.","Levels: floor 14 m below the Haram surface and a rock roof about 2.5 m thick (Schick), rock 1.5 m below the surface (Warren), so 10 m from floor to roof (Pierotti 10 m; Schick also gives 11.5 m). Wilson and Warren give the floor 12.85–13.3 m down. Walls and floor are drawn plastered (\"entirely rock-cut and plastered\").","The five piers follow Schick's count (Wilson's plan has four piers and two rock partitions); their places and 3 × 3 m size are illustrative. Of the shaft mouths, only the one Warren draws is placed from the plate; two more stand for the three Wilson found in use, at illustrative places, 1 m square.","The stair is drawn with Schick's 50 steps from the south, 1.2 m wide, with a well-like opening at the top (Whitty, via G&J p. 33); its line, width and the opening's depth are illustrative. The roof is cut away west of x = −4 m for display only: the cistern is roofed throughout, partly in rock and partly with flat stones (W&C p. 220). The small circular chamber, the conduits and Pierotti's passages east and south are not drawn.","Cistern VIII lies south of the inner platform in front of the Aqṣā; its position comes from the plate's registration to the mapped Haram corners (below). No date is given for the cutting of the cistern in the pages read.");
 } else if(plan.traced&&traced[plan.traced]){
  const source=traced[plan.traced],view=source.layers.find(l=>l.id===options.layer)??source.layers.find(l=>l.id==='remains')??source.layers[0],rebuilt=view.kind!=='observed';
  units="metres";note=`${view.label} · ${rebuilt?'published reconstruction':'traced plan'}`;
  // Escarpment lines are left to the terrain; they do not size the display bench.
  const shown=source.elements.filter(e=>e.layers.includes(view.id)),datum=source.frame.ground??0,all=shown.filter(e=>e.kind!=='cliff-edge').flatMap(elementPoints);
  // Centre the traced frame so the display bench, markers and camera sit on the drawn site.
  // A traced plan may name a focus; the extent is then widened so that the focus is its centre.
  if(source.focus){const xs=all.map(p=>p[0]),zs=all.map(p=>p[1]),[fx,fz]=source.focus;all.push([2*fx-Math.min(...xs),2*fz-Math.min(...zs)],[2*fx-Math.max(...xs),2*fz-Math.max(...zs)]);}
  const minX=Math.min(...all.map(p=>p[0])),maxX=Math.max(...all.map(p=>p[0])),minZ=Math.min(...all.map(p=>p[1])),maxZ=Math.max(...all.map(p=>p[1])),cx=(minX+maxX)/2,cz=(minZ+maxZ)/2;
  // The traced frame's origin in model coordinates: a placement ties this point, not the view's centre,
  // so every view of the plan lands in the same place.
  tracedOrigin=[-cx,-cz];
  const c=([x,z]:Point):Point=>[x-cx,z-cz],level=(v:number|null|undefined,fallback=0)=>v==null?fallback:v-datum;
  // In a reconstruction view, parts drawn only by the reconstruction use the pale restored surface.
  const rebuiltPart=(e:TracedElement)=>rebuilt&&e.status!=='observed',pick=(e:TracedElement,base:T.MeshStandardMaterial)=>rebuiltPart(e)?restored:base;
  const wallHeight=(e:TracedElement)=>e.height?.value??(rebuilt?TRACED_HEIGHTS.wall:TRACED_HEIGHTS.ruin);
  // A wall's base and height: from its published top and bottom levels where given, else from the ground.
  const wallSpan=(e:TracedElement):[number,number]=>{const t=e.levels?.top,b=e.levels?.bottom,h=e.lineStyle==='dashed'&&e.height?.value==null?TRACED_HEIGHTS.dashed:wallHeight(e);return t!=null&&b!=null?[level(b),t-b]:t!=null?[level(t)-h,h]:[level(b),h];};
  const lifted=(y:number,build:()=>void)=>{const start=root.children.length;build();root.children.slice(start).forEach(o=>o.position.y+=y);};
  const holes:Point[][]=[];let guessedDepth=false;
  // A pool's depth: its published floor level, else its published depth, else illustrative.
  const poolDepth=(e:TracedElement)=>{const floor=e.levels?.floor??e.levels?.bottom;return floor!=null?level(e.levels?.rim??e.levels?.top)-level(floor):e.height?.value??TRACED_HEIGHTS.depth;};
  const inside=([x,z]:Point,poly:Point[])=>poly.reduce((hit,a,i)=>{const b=poly[(i+1)%poly.length];return (a[1]>z)!==(b[1]>z)&&x<a[0]+(z-a[1])*(b[0]-a[0])/(b[1]-a[1])?!hit:hit;},false);
  const pools=shown.filter(e=>(e.kind==='pool'||e.kind==='cistern')&&e.geometry.type==='polygon'),inPool:string[]=[];
  const centroid=(pts:Point[]):Point=>[pts.reduce((a,p)=>a+p[0],0)/pts.length,pts.reduce((a,p)=>a+p[1],0)/pts.length];
  for(const e of shown){
   const g=e.geometry;
   if(g.type==='raster'){
    const rects=rasterRectangles(decodeRaster(g),g.cols,g.rows),h=wallHeight(e),blocks=new T.InstancedMesh(chippedBlock(1,1,1,29),cloneSiteMaterial(pick(e,stone)),rects.length),o=new T.Object3D();
    rects.forEach(([col,row,w,d],i)=>{const [x,z]=c([g.origin[0]+(col+w/2)*g.cell,g.origin[1]+(row+d/2)*g.cell]);o.position.set(x,level(e.levels?.bottom)+h/2,z);o.scale.set(w*g.cell,h,d*g.cell);o.updateMatrix();blocks.setMatrixAt(i,o.matrix);blocks.setColorAt(i,new T.Color().setScalar(.86+((i*37)%23)/120));});
    blocks.castShadow=blocks.receiveShadow=true;root.add(tag(blocks,e.id));continue;
   }
   const pts=g.type==='point'?[c(g.at)]:g.points.map(c);
   // A wall the figure draws dashed (meaning not stated) is a low strip on the ground, not a standing wall.
   if(e.kind==='wall'){const [base,h]=wallSpan(e);walls(pts,h,g.type==='polyline'?g.width??.6:.6,base,e.id,g.type==='polygon'||!!(g.type==='polyline'&&g.closed),pick(e,stone));}
   else if(e.kind==='pool'||e.kind==='cistern'){
    const rim=level(e.levels?.rim??e.levels?.top),depth=poolDepth(e);guessedDepth||=(e.levels?.floor??e.levels?.bottom)==null&&e.height?.value==null;
    if(g.type==='point')lifted(rim,()=>shaft(pts[0][0],pts[0][1],g.radius??1,depth,e.id,pick(e,stone)));
    else{lifted(rim,()=>basin(pts,depth,e.id,pick(e,plaster)));holes.push(pts);}
   }
   else if(e.kind==='steps'&&g.type==='polygon'){
    const xs=pts.map(p=>p[0]),zs=pts.map(p=>p[1]),x0=Math.min(...xs),x1=Math.max(...xs),z0=Math.min(...zs),z1=Math.max(...zs),down=e.steps?.down??'n',alongX=down==='e'||down==='w';
    // Steps drawn inside a pool, or naming one, go down from its rim to its floor.
    const pool=pools.find(p=>p.id===e.steps?.pool)??pools.find(p=>inside([(x0+x1)/2,(z0+z1)/2],(p.geometry as {points:Point[]}).points.map(c))),poolTop=pool&&level(pool.levels?.rim??pool.levels?.top);
    const top=pool?poolTop!:level(e.levels?.top??e.levels?.rim),bottom=pool?poolTop!-poolDepth(pool):level(e.levels?.bottom??e.levels?.floor,top-1),count=e.steps?.count??Math.max(2,Math.round((top-bottom)/.25));
    // steps() rises toward its local +x; turn it so that it goes down toward `down`.
    const flight=steps((x0+x1)/2,(z0+z1)/2,alongX?z1-z0:x1-x0,alongX?x1-x0:z1-z0,top-bottom,count,e.id,pick(e,stone));flight.position.y=bottom;flight.rotation.y={e:Math.PI,w:0,s:Math.PI/2,n:-Math.PI/2}[down];
   }
   else if(e.kind==='column'&&g.type==='point'){const r=g.radius??.3,h=e.height?.value??(rebuilt?TRACED_HEIGHTS.column:TRACED_HEIGHTS.columnBase),m=mesh(new T.CylinderGeometry(r,r*1.04,h,16),pick(e,surfaces.block),e.id);m.position.set(pts[0][0],level(e.levels?.floor)+h/2,pts[0][1]);}
   else if(e.kind==='channel'&&g.type==='polyline')trough(pts.map(([x,z])=>new T.Vector3(x,level(e.levels?.top)+.12,z)),g.width??.4,e.id,rebuiltPart(e)?restored:plaster);
   else if((e.kind==='room'||e.kind==='platform'||e.kind==='garden'||e.kind==='path')&&g.type==='polygon'){
    // A platform with no level drawn inside a pool stands on the pool's floor (illustrative height).
    const pool=e.kind==='platform'&&e.levels?.floor==null?pools.find(p=>inside(centroid(pts),(p.geometry as {points:Point[]}).points.map(c))):undefined;
    if(pool){const floor=level(pool.levels?.rim??pool.levels?.top)-poolDepth(pool),h=e.height?.value??TRACED_HEIGHTS.podium;slab(pts,h,floor,pick(e,stone),e.id);inPool.push(e.label??e.id);}
    else slab(pts,.2,level(e.levels?.floor)-.2,pick(e,e.kind==='garden'?earth:plaster),e.id);
   }
  }
  for(const f of plan.features){const e=source.elements.find(e=>e.id===f.id),at=source.features?.find(x=>x.id===f.id)?.at,[x,z]=e?centroid(elementPoints(e).map(c)):at?c(at):[0,0];marker(f.id,x,z,1.2);}
  plinth(maxX-minX+24,maxZ-minZ+24,2,holes);
  tracedStart=source.walkStart?{position:c(source.walkStart.at),bearing:source.walkStart.bearing,pitch:84}:{position:[0,(maxZ-minZ)/2+4],bearing:0,pitch:84};
  assumptions.push(`Traced from ${source.sources.map(s=>s.citation).join('; ')} at each figure's own scale bar; north from ${source.frame.north}. ${(siteContext(plan.id)?.registration as {placement?:string}|undefined)?.placement==='imagery'?'The frame is registered to satellite imagery, as the placement note states.':'The frame is not registered to geographic coordinates: the model sits at the site anchor.'} Record: research/models/traced_plans/${source.id}.md.`);
  assumptions.push(rebuilt?`${view.label} is a published reconstruction. Pale parts with a dashed grid are drawn only by that reconstruction; parts also recorded as found keep their normal surfaces. The plans give no heights: walls (${TRACED_HEIGHTS.wall} m) and columns (${TRACED_HEIGHTS.column} m) are illustrative.`:`Only elements recorded as found are shown. Walls are drawn ${TRACED_HEIGHTS.ruin} m high: preserved heights are not traced.`);
  if(inPool.length)assumptions.push(`${inPool.join(', ')}: drawn on the pool floor, ${TRACED_HEIGHTS.podium} m high (illustrative); no level is published.`);
  if(shown.some(e=>e.kind==='wall'&&e.lineStyle==='dashed'))assumptions.push(`Lines that the figure draws dashed, without a stated meaning, are low strips (${TRACED_HEIGHTS.dashed} m), not walls.`);
  const guessed=guessedDepth?` Where neither is published, the depth is an illustrative ${TRACED_HEIGHTS.depth} m.`:'';
  assumptions.push(source.frame.datum?`Pool rims and floors and room floors follow the published spot levels (${source.frame.datum}); the general ground is level ${datum}.${guessed}`:`No levels are used: the site is drawn on one level surface. Pool depths are the published depths.${guessed}`);
 } else {
  const scale=36/Math.max(plan.width,plan.height),conv=(x:number,z:number):Point=>[(x-plan.width/2)*scale,(z-plan.height/2)*scale];
  const loader=new SVGLoader(),basinHoles:Point[][]=[];
  const pieces=plan.shapes?.length?plan.shapes:plan.features.filter(f=>f.path).map(f=>({d:f.path!,kind:/basin|pool/i.test(f.label)?"basin":/wall|dam/i.test(f.label)?"wall":"channel",id:f.id}));
  for(const piece of pieces??[]){
   const svg=`<svg xmlns="http://www.w3.org/2000/svg"><g transform="${plan.transform??""}"><path d="${piece.d}"/></g></svg>`;
   const parsed=loader.parse(svg);const id="id" in piece?String(piece.id):undefined;
   for(const path of parsed.paths)for(const sub of path.subPaths){const pts=sub.getPoints(36).map(p=>conv(p.x,p.y));if(pts.length<2)continue;
    if(piece.kind==="basin"){basinHoles.push(pts);slab(pts,.2,-1.1,plaster,id);walls(pts,1.1,.25,-1.1,id);}
    else if(piece.kind==="wall"||piece.kind==="rock"){walls(pts,piece.kind==="rock"?2.8:1.7,.55,0,id,sub.autoClose);}
    else if(piece.kind==='tunnel')coveredPassage(pts.map(([x,z])=>new T.Vector3(x,.12,z)),id);
    // A reconstructed dam line: copper marks the source's proposal, not surviving masonry.
    else if(piece.kind==='dam')walls(pts,1.2,.9,0,id,false,copper);
    else trough(pts.map(([x,z])=>new T.Vector3(x,.12,z)),.4,id,piece.kind==='reconstruction'?copper:plaster);
   }
  }
  for(const f of plan.features){const [x,z]=conv(f.x,f.y);marker(f.id,x,z,1.2);}
  if(!pieces?.length)for(const f of plan.features){const [x,z]=conv(f.x,f.y);court(x,z,5,4,1.7,f.id);}
  plinth(40*plan.width/Math.max(plan.width,plan.height)+7,40*plan.height/Math.max(plan.width,plan.height)+7,2,basinHoles);
  assumptions.push("Selected source-plan outlines and feature envelopes are normalized into a relative scene. They are not new measured footprints.","Wall heights, pool depths, terrain/platform relief and conduit cross-sections are illustrative. Source phasing, restorations and feature interpretations remain those of the accompanying record.");
  if(pieces?.some(piece=>piece.kind==='dam'))assumptions.push('The copper-coloured wall marks a dam that the source draws as a reconstruction. Its height and width are illustrative; no surviving remains are reported.');
  if(pieces?.some(piece=>piece.kind==='reconstruction'))assumptions.push('Copper-coloured channel lining marks the proposed course shown in the source. Its display does not establish surviving masonry. Covered passages have illustrative rectangular sections; the source plan does not measure their roof form.');
 }
 // A plan placed in its mapped setting by the OpenStreetMap tool (tools/build_osm_context.py) moves from its
 // own frame into the place frame: the chosen model point onto the mapped target (the place anchor when the
 // plan is not registered), turned as registered, with model height datumY on the modern terrain.
 const setting=placeFrame?undefined:siteContext(plan.id),fit=SETTINGS[plan.id];let anchored=false,byImagery=false;
 if(setting&&fit){
  const reg=(setting.registration??{}) as {target?:Point;rotationDeg?:number;placement?:string};anchored=reg.placement==='anchor';byImagery=reg.placement==='imagery';
  const pick=(p:Point|string|undefined,fallback:Point):Point=>{if(typeof p!=='string')return p??fallback;if(p==='traced-origin')return tracedOrigin??fallback;const m=markers.get(p);return m?[m.x,m.z]:fallback;};
  const from=pick(fit.point,[0,0]),datum=pick(fit.datum,from),to=reg.target??[0,0],turn=T.MathUtils.degToRad(reg.rotationDeg??0);
  const frame=new T.Group(),f=new T.Vector3(from[0],0,from[1]).applyAxisAngle(new T.Vector3(0,1,0),turn);frame.rotation.y=turn;frame.position.set(to[0]-f.x,0,to[1]-f.z);frame.updateMatrix();
  const move=(p:Point):Point=>{const v=new T.Vector3(p[0],0,p[1]).applyMatrix4(frame.matrix);return [v.x,v.z];};
  const patch=placeTerrain(plan.placeIds[0],options.terrain),at=move(datum),base=fit.level!==undefined&&patch?fit.level-patch.centreElevation:(patch?elevationAt(patch,at[0],at[1]):0)-(fit.datumY??0);
  frame.position.y=base;frame.updateMatrix();if(fit.levelNote)assumptions.push(fit.levelNote);
  for(const child of [...root.children])frame.add(child);root.add(frame);
  markers.forEach(v=>v.applyMatrix4(frame.matrix));
  const centre=move(fit.centre??[0,0]);
  ground.holes=ground.holes.map(h=>h.map(move));
  ground.pads=ground.pads.map(p=>{const [x,z]=move([p.x,p.z]);return {...p,x,z,height:p.height+base,angle:(p.angle??0)+turn};});
  // The display bench becomes a pad around the model, at its own ground.
  if(fit.bench!==false&&ground.bench!==false)ground.pads.unshift({x:centre[0],z:centre[1],w:ground.w,d:ground.d,height:base-.28,feather:Math.max(ground.w,ground.d)*.3,angle:turn});
  ground.bench=false;placeFrame=centre;ground.focus=ground.focus?move(ground.focus):centre;
  if(tracedStart)tracedStart={...tracedStart,position:move(tracedStart.position)};
 }
 roof.visible=false;
 const [gx,gz]=placeFrame??[0,0],bounds=new T.Box3().setFromObject(root);bounds.expandByPoint(new T.Vector3(gx-ground.w/2,-1,gz-ground.d/2));bounds.expandByPoint(new T.Vector3(gx+ground.w/2,1,gz+ground.d/2));const center=placeFrame?new T.Vector3():bounds.getCenter(new T.Vector3());
 root.position.set(-center.x,0,-center.z);markers.forEach(p=>{p.x-=center.x;p.z-=center.z});
 if(options.pads)ground.pads.push(...options.pads);
 const osm=placeFrame?siteContext(plan.id):undefined,features=osm?options.context:undefined;if(features){ground.paved=pavedIndex(features);ground.green=greenIndex(features);}
 const context=landscapeGround(ground,plan.placeIds[0],[center.x,center.z],earth,surfaces.block,options.terrain);context.mesh.position.set(center.x,0,center.z);context.mesh.userData.walkSurface=true;context.mesh.userData.siteContext='ground';root.add(context.mesh);context.details.position.set(center.x,0,center.z);context.details.userData.siteContext='details';root.add(context.details);
 if(osm&&features){
  // Mapped surroundings, added after the framing box so that they do not widen the model's own build.
  // Around a plan that is not registered, none are drawn inside its own ground.
  const surface=context.mesh.userData.surfaceAt as (x:number,z:number)=>number,holes=ground.holes,reach=context.mesh.userData.radius*.4;
  const open=(x:number,z:number)=>holes.some(h=>{let hit=false;for(let i=0,j=h.length-1;i<h.length;j=i++){const [a,b]=h[i],[c,d]=h[j];if((b>z)!==(d>z)&&x<(c-a)*(z-b)/(d-b)+a)hit=!hit;}return hit;});
  const turn=(siteContext(plan.id)?.registration as {rotationDeg?:number}|null)?.rotationDeg??0,c=Math.cos(T.MathUtils.degToRad(turn)),s=Math.sin(T.MathUtils.degToRad(turn));
  const ownGround=(x:number,z:number)=>{const dx=x-gx,dz=z-gz;return Math.abs(dx*c-dz*s)<ground.w/2&&Math.abs(dx*s+dz*c)<ground.d/2;};
  const keepOut=(x:number,z:number)=>open(x,z)||[...markers.values()].some(m=>Math.hypot(m.x-x,m.z-z)<6)||(anchored&&ownGround(x,z));
  const group=buildSiteContext(features,surface,{paving:stone,stair:surfaces.block,wall:stone,grave:surfaces.block},{keepOut,open,within:(x,z)=>Math.hypot(x-gx,z-gz)<reach});
  root.add(group);
  if(anchored)assumptions.push(`The model is not registered to these surroundings: it stays at the site anchor (${plan.placeIds[0]}), so where it sits among them is uncertain by the anchor's precision. No mapped feature is drawn inside the model's own ground.`);
  assumptions.push(`Surroundings are today's, from OpenStreetMap (${CONTEXT_LICENCE}; retrieved ${osm.retrieved}; record ${osm.record}): ${group.userData.counts.graves.toLocaleString('en')} graves set in rows inside the mapped cemetery areas (about 1 × 2 m, 1.45 m apart; long axes east–west, or across the qibla in the Muslim cemetery; illustrative, not mapped graves), mapped footpaths (2.4 m where no width is mapped), roads (3.5–8 m by class) and stairs (0.4 m treads on the terrain), ${group.userData.counts.trees.toLocaleString('en')} trees (mapped single trees, and trees about 7 m apart in mapped woods and orchards; sizes illustrative), green ground in mapped woods, orchards and grass, city walls (2.6 m thick, 12 m above the lower ground where no height is mapped), retaining walls, gate buildings (9 m above the ground where no height is mapped) and ${group.userData.counts.buildings} buildings (mapped heights, else 6.5 m; flat roofs, with domes and pyramids where mapped). They show the modern setting and are not evidence for the ancient one.`);
 }
 assumptions.push(surfaces.style.photos.length?`Base colours and the ${surfaces.style.masonry} masonry pattern are taken from reference photographs (${surfaces.style.photos.join(', ')}): sunlit-face medians of sample boxes, recorded in research/assets/plans/atlas-explorer/surface-samples-2026-10-17. ${surfaces.style.masonryNote??''} Individual stones, joints, chipped edges, plaster wear and soil relief remain illustrative, not recorded stones or weathering; photographs vary in exposure and white balance.`:`Surface art uses a ${surfaces.style.id} material palette, metre-scaled stone joints, chipped edges, plaster wear and soil relief. These are illustrative visual treatments, not recorded individual stones or weathering.`);
 assumptions.push(context.patch&&osm&&!anchored?`Surrounding relief is sampled from Mapterhorn’s modern elevation tiles in the place’s own frame; the model is placed and turned by ${byImagery?'satellite imagery':'mapped outlines'}, as stated above. The terrain is not ancient ground level.`:context.patch&&osm?"Surrounding relief is sampled from Mapterhorn’s modern elevation tiles in the place’s own frame, with the model’s ground levelled into it at the site anchor. Its position and bearing are schematic, not surveyed or registered; the terrain is not ancient ground level.":context.patch?"Surrounding relief is sampled from Mapterhorn’s modern elevation tiles around the existing site anchor. The local bench is feathered to expose the model. Architectural position and bearing are schematic, not surveyed or registered; the terrain is not ancient ground level.":"The rock setting is illustrative because this cave has no established geographic coordinates.");
 const starts:Record<string,[string,number,number,number,number]>={'temple-great-sea':['great-sea',0,-34,180,84],'gerizim-precinct':['east-stair',28,22,308,100],'hyrcania-waterworks':['north-pool',0,-12,180,76],'jericho-early':['complex',-14.5,0,90,80],'jericho-late':['complex',-14.5,0,90,80],'siloam-receiver':['L103',0,6,0,80],'doq-waterworks':['intake',4,5,-35,83],'jericho-ac':['AC94',0,7,0,80],'bethesda-pools':['dam',-12,0,160,84],'east-gate-warren':['massive-wall',8,-12,270,90]};
 const start=starts[plan.id],point=start?markers.get(start[0]):undefined;
 const walkStart=point&&start?{position:[point.x+start[1],point.z+start[2]] as Point,bearing:start[3],pitch:start[4]}:tracedStart&&{...tracedStart,position:[tracedStart.position[0]-center.x,tracedStart.position[1]-center.z] as Point};
 return {root,roof,markers,selectable,note,assumptions,units,walkStart,framing:bounds.translate(new T.Vector3(-center.x,0,-center.z)),landscape:{context:osm?(anchored?'Terrain and mapped surroundings · model at the site anchor, not registered':(byImagery?'Terrain and mapped surroundings · model registered to satellite imagery':'Terrain and mapped surroundings · model registered to OpenStreetMap outlines')):context.context,credit:osm?`${context.credit} · surroundings © OpenStreetMap contributors (ODbL)`:context.credit,mapped:!!context.patch,registered:!!osm&&!anchored,registeredBy:osm&&!anchored?(byImagery?'imagery':'outlines'):undefined}};
}
