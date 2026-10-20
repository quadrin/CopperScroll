import * as T from "three";
import { landscapeGround, type LandscapeGround } from "./atlas-model-landscape";
import { SVGLoader } from "three/addons/loaders/SVGLoader.js";
import type { SitePlan } from "./atlas-explorer-model";
import { createSiteMaterials, cloneSiteMaterial, chippedBlock } from './atlas-site-materials';

export type { ModelCamera } from "./atlas-explorer-model";
export type ModelGeometry = { root: T.Group; markers: Map<string, T.Vector3>; selectable: T.Object3D[]; roof: T.Group; note: string; assumptions: string[]; units: "metres" | "relative"; framing:T.Box3; landscape:{context:string;credit:string;mapped:boolean};walkStart?:{position:[number,number];bearing:number;pitch:number} };
type Point = [number, number];

function polygon(points:Point[]) {const s=new T.Shape();points.forEach(([x,z],i)=>i?s.lineTo(x,-z):s.moveTo(x,-z));s.closePath();return s;}
function material(color:string,map?:T.Texture){return new T.MeshStandardMaterial({color,map:map??null,roughness:.94,metalness:0});}
export function buildModel(plan:SitePlan):ModelGeometry {
 const root=new T.Group(), roof=new T.Group(),markers=new Map<string,T.Vector3>(),selectable:T.Object3D[]=[];
 const surfaces=createSiteMaterials(plan.id),{stone,rock,earth,plaster}=surfaces,copper=material("#b56b42");
 const wellHoles:Point[][]=[],courtFloors:{x:number;z:number;w:number;d:number;mesh:T.Mesh}[]=[];let ground:LandscapeGround={w:40,d:40,holes:[],pads:[]};
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
  for(const side of [-1,1]){const count=Math.ceil(length/.65),blocks=new T.InstancedMesh(chippedBlock(1,1,1,23),cloneSiteMaterial(surfaces.block),count),o=new T.Object3D();
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
  slab(points,.3,-depth-.3,plaster,id);walls(points,depth,.35,-depth,id,true,lining);
  points.forEach((a,i)=>{const b=points[(i+1)%points.length],cap=box((a[0]+b[0])/2,(a[1]+b[1])/2,Math.hypot(b[0]-a[0],b[1]-a[1]),.39,.12,.015,id,surfaces.block);cap.rotation.y=-Math.atan2(b[1]-a[1],b[0]-a[0]);});
 }
 function shaft(x:number,z:number,r:number,depth:number,id:string){
  wellHoles.push(circlePoints(x,z,r+.02));
  const g=new T.CylinderGeometry(r,r*.78,depth,32,1,true);const m=mesh(g,stone,id);m.position.set(x,-depth/2,z);(m.material as T.MeshStandardMaterial).side=T.DoubleSide;
  const rim=mesh(new T.TorusGeometry(r,.17,6,48),stone,id);rim.rotation.x=Math.PI/2;rim.position.set(x,.12,z);
  const floor=mesh(new T.CircleGeometry(r*.8,32),plaster,id);floor.rotation.x=-Math.PI/2;floor.position.set(x,-depth+.02,z);
 }
 function steps(x:number,z:number,width:number,run:number,rise:number,count:number,id:string){const g=new T.Group();root.add(g);g.position.set(x,0,z);for(let i=0;i<count;i++)box(-run/2+(i+.5)*run/count,0,run/count+.01,width,(i+1)*rise/count,0,id,stone,g);return g;}
 function marker(id:string,x:number,z:number,y=1){markers.set(id,new T.Vector3(x,y,z));}
 function plinth(w:number,d:number,_depth=1.2,holes:Point[][]=[]){ground={w,d,holes:[...holes,...wellHoles],pads:ground.pads};}

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
  units="metres";note="Double pool · published depths 5 m and 2.6 m";
  const n:Point[]=[[-19,-27],[-.8,-27],[0,-11],[-19,-12]],s:Point[]=[[-19,-6.9],[-1,-6.9],[-1,7.5],[-19,7.5]];
  basin(n,5,"north-pool",plaster);basin(s,2.6,"south-member",plaster);marker("north-pool",-10,-19,.55);marker("south-member",-10,.1,.55);
  slab([[-23,-30],[4,-30],[4,11],[-23,11]],.8,-5.8,rock,undefined,root,[n,s]);
  const bridge=box(-9,17,32,2.4,3.1,-3.2,"bridge");bridge.rotation.y=.35;
  for(let i=0;i<8;i++)box(-24+i*4,17,1,2.5,2.6,-3.2,"bridge",rock);
  trough([new T.Vector3(-30,.2,4),new T.Vector3(-14,.2,18),new T.Vector3(4,.2,24)],.52,"bridge");marker("bridge",-9,17,1);
  basin([[-27,20],[-15,20],[-15,31],[-27,31]],1.8,"separate-pool");marker("separate-pool",-21,25,.6);
  court(20,12,28,37,2.1);court(20,12,11,15,1.9);box(32,-3,6,7,3.2);
  for(const [x,z] of [[16,35],[24,38],[39,4],[42,-7]])shaft(x,z,2,3,"cisterns");marker("cisterns",20,36,.7);
  plinth(88,86,6.3,[n,s,[[-27,20],[-15,20],[-15,31],[-27,31]]]);
  assumptions.push("Northern pool sides approximate the published 19 / 15 / 18.2 / 16 m quadrilateral. Published maximum depths are shown: about 5 m north, 2.6 m south.","Rock separation uses 5.1 m, the midpoint of the reported 4.8–5.4 m range. Southern outline, bridge dimensions in this view, summit walls, other cistern depths and surrounding relief are illustrative.","The double pool is drawn rock-cut with plastered faces (Patrich 1989 p. 255, \"rock-cut double pool\"; reference photograph hyrcania-c-hurkania-5011 shows plastered rock walls), not as laid masonry; the coping course is illustrative.","No north bearing is assigned to the source frame. Floors are tinted to distinguish basins; the tint is not a reconstructed water level. Centre/rim origins and construction phases remain unresolved.");
 } else if(plan.id==="gerizim-precinct"){
  units="metres";note="Hellenistic precinct · selected architectural relationships";
  const start=root.children.length;
  court(0,0,136,212,3.2);court(0,-30,98,96,1.8);court(43,66,25,24,3.8,"citadel");
  // The platform expresses the published stair's relative rise, not an independently surveyed terrain model.
  court(-38,102,13,12,1.2,"west-entrance");
  for(const z of [-75,66]){court(-40,z,22,16,2.2);court(-9,z,22,16,2.2);}
  root.children.slice(start).forEach(m=>m.position.y+=15.5);
  ground.pads.push({x:0,z:0,w:136,d:212,height:15.5,feather:12});marker("citadel",43,66,20);marker("west-entrance",-38,102,17);
  const mansionStart=root.children.length,cisternHole=circlePoints(-103,28,1.65);
  court(-94,28,40,40,2.8,"mansion",[cisternHole]);court(-103,28,20,14,2.1,"mansion",[cisternHole]);
  for(let i=0;i<3;i++)court(-83,16+i*12,10,9,2.2,"mansion");shaft(-103,28,1.6,2.6,"mansion");
  root.children.slice(mansionStart).forEach(m=>m.position.y+=8);
  ground.pads.push({x:-94,z:28,w:42,d:42,height:8,feather:10});marker("mansion",-94,28,11.6);
  const stair=steps(84,-13,23,34,15.5,57,"east-stair");stair.rotation.y=Math.PI;
  court(107,-13,9,13,2.8,"east-stair");marker("east-stair",84,-13,11);
  plinth(255,290,7);
  assumptions.push("Reported envelopes are used for the 212 × 136 m Hellenistic enclosure, 40 × 40 m mansion, 20 × 14 m building IV and 25 × 24 m citadel.","The eastern stair uses the reported maximum 23 m width, 34 m run, 15.5 m rise and approximately 57 steps. The western entrance is shown as a separate schematic landing; it is not equated with the southern seven-step flight or the 15-step flight at E1.","Most wall heights, room divisions, the mansion’s 8 m display level and the cistern’s display location/depth are illustrative. The precinct platform expresses the east stair’s relative rise; its block shape is not surveyed terrain. Relative building placement is simplified; no temple superstructure, P5178 coordinate or contemporary use horizon is asserted.");
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
  units="metres";note="Two pools and dam · published dimensions; eastern complex schematic";
  // Plan metres: x east, z south, origin at the southern pool's north-west corner. Shifted to centre the scene.
  const c=([x,z]:Point):Point=>[x-54,z],r=(x0:number,z0:number,x1:number,z1:number):Point[]=>[[x0,z0],[x1,z0],[x1,z1],[x0,z1]].map(p=>c(p as Point));
  const north=r(0,-46.5,53,-6.5),south=([[0,0],[45,0],[64.99,45.83],[0,47]] as Point[]).map(c);
  basin(north,10,"north-pool");basin(south,14,"south-pool");
  const [cx,cz]=c([26.5,-5.6]);shaft(cx,cz,.55,15,"dam");
  // Steps down the whole western side, south of the settling basin; count and run are illustrative.
  const [sx,sz]=c([7,27]);const flight=steps(sx,sz,40,14,14,40,"south-pool");flight.position.y=-14;flight.rotation.y=Math.PI;
  walls(r(1,1,6,6),2.6,.5,-14,"settling-basin");
  const [kx,kz]=c([95,20]);shaft(kx,kz,3,8.5,"cistern-1");
  const grottoes:[number,number,number,number,number,string][]=[[93.5,10,96.5,13,2.5,"first-installation"],[101,11,104,14,2.2,"first-installation"],[100.5,19,102.5,21,.3,"first-installation"],[93.5,27,96.5,30,1.5,"first-installation"],[106,19,107.5,21,1.5,"grotto-5"],[100,26,103.5,29.5,3,"grotto-6"]];
  for(const [x0,z0,x1,z1,depth,id] of grottoes)basin(r(x0,z0,x1,z1),depth,id,rock);
  const [gx,gz]=c([106.3,20]);const g5=steps(gx,gz,1.5,.6,1.5,4,"grotto-5");g5.position.y=-1.5;g5.rotation.y=Math.PI;
  const [tx,tz]=c([98.8,24.9]);const sill=box(tx,tz,1.3,.55,.16,0,"threshold");sill.rotation.y=-.46;box(tx-.75,tz-.3,.4,.4,1.2,0,"threshold");
  for(const [id,x,z,y] of [["north-pool",26.5,-26.5,.6],["dam",26.5,-3.25,1],["south-pool",20,22,.6],["settling-basin",3.5,3.5,-12.8],["cistern-1",95,20,.6],["threshold",98.8,24.9,.6],["grotto-6",101.75,27.75,.6],["grotto-5",106.75,20,.6],["first-installation",95,11.5,.6]] as [string,number,number,number][]){const [x2,z2]=c([x,z]);marker(id,x2,z2,y);}
  plinth(128,108,14,[north,south,...grottoes.map(([x0,z0,x1,z1])=>r(x0,z0,x1,z1))]);
  assumptions.push("Northern pool 53 × 40 m (Gibson). Its depth is not given in the sources read; 10 m is about 21,200 m³ divided by its area, an inference. The 53 m side is drawn east–west.","Southern pool sides about 45 m north, 50 m east, 65 m south and 47 m west, up to 14 m deep (Duprez); the outline assumes a straight east–west north side and a north–south west side. The dam is 6.5 m wide (Duprez 6.50 m at the top; Gibson 6–6.5 m) and drawn as long as the northern pool.","The chimney is drawn round, 1.1 m across and 15 m deep after Duprez; von Wahlde gives 12 m. Its small openings to the northern pool are not drawn.","The western steps follow Gibson's report of steps along the whole western side; their count, run, width and the absence of landings are illustrative. The settling basin's 2.6 m east wall is Duprez's; its size and place in the corner are illustrative.","Pool and dam faces are drawn as laid ashlar in courses of about 60 cm (Duprez p. 34); Duprez reports rock in the lower parts, which the model does not separate.","Eastern complex: cistern 1 (about 8.5 m deep, 6 m across), grotto 5 (1.5 × 2 × 1.5 m, four steps) and basin 4 (about 30 cm deep) use Duprez's dimensions. Other sizes and all positions follow the arrangement of Duprez Pl. II, whose scale is not recorded; the distance and bearing from the pools are schematic. The grottoes are roofed caves, drawn open.","Byzantine and Crusader churches and later structures are omitted. The model makes no claim about a deposit point.");
 } else if(plan.id==="east-gate-warren"){
  units="metres";note="Golden Gate · Warren’s levels and gallery, Plate VI frame";
  // Plate VI frame in metres: origin at the gate outline's centre, x to plate right (≈ east), z to plate down.
  // Levels: y = 0 at the Haram surface by cistern XV (2,408 ft); Warren's feet × 0.3048 below it.
  const ft=(level:number)=>(level-2408)*.3048,wallX=11.5,outside=ft(2389),shaftTop=ft(2333.5),gz=9.1,sx=53.48;
  ground.pads.push({x:wallX+150,z:0,w:300,d:600,height:shaftTop,feather:.5},{x:wallX+.5,z:0,w:1,d:600,height:outside,feather:42},{x:wallX-150,z:0,w:300,d:600,height:0,feather:.5});
  const surface=(x:number,z:number)=>{let y=-.28;for(const p of ground.pads){const d=Math.max(Math.abs(x-p.x)-p.w/2,Math.abs(z-p.z)-p.d/2,0),t=T.MathUtils.clamp(d/p.feather,0,1);y=T.MathUtils.lerp(y,p.height,1-t*t*(3-2*t));}return y;};
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
 } else if(plan.id==="jericho-early"||plan.id==="jericho-late"){
  units="metres";note=plan.id==="jericho-early"?"Early paired pools · published approximate dimensions":"Joined basin · a separate architectural state";
  if(plan.id==="jericho-early"){
   const a:Point[]=[[-16,-9],[2,-9],[2,4],[-16,4]],b:Point[]=[[-16,9],[2,9],[2,22],[-16,22]];basin(a,2.5,"complex");basin(b,2.5,"complex");plinth(43,47,3.5,[a,b]);
  }else{const a:Point[]=[[-16,-9],[16,-9],[16,9],[-16,9]];basin(a,2.5,"complex");plinth(48,34,3.5,[a]);}
  for(let i=0;i<6;i++){box(7,-12+i*6,.5,.5,2.8,0,"complex");}
  marker("complex",-7,0,1);
  assumptions.push("The early state uses the reported approximate 18 × 13 m pool envelopes; the joined state uses approximately 32 × 18 m. They remain separate selectable models.","Depth 2.5 m, surrounding platform, columns and wall heights are illustrative. The reconstructed source figures do not establish a conduit origin, floor datum or deposit point.");
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
 roof.visible=false;
 const bounds=new T.Box3().setFromObject(root);bounds.expandByPoint(new T.Vector3(-ground.w/2,-1,-ground.d/2));bounds.expandByPoint(new T.Vector3(ground.w/2,1,ground.d/2));const center=bounds.getCenter(new T.Vector3());
 root.position.set(-center.x,0,-center.z);markers.forEach(p=>{p.x-=center.x;p.z-=center.z});
 const context=landscapeGround(ground,plan.placeIds[0],[center.x,center.z],earth,surfaces.block);context.mesh.position.set(center.x,0,center.z);context.mesh.userData.walkSurface=true;context.mesh.userData.siteContext='ground';root.add(context.mesh);context.details.position.set(center.x,0,center.z);context.details.userData.siteContext='details';root.add(context.details);
 assumptions.push(surfaces.style.photos.length?`Base colours and the ${surfaces.style.masonry} masonry pattern are taken from reference photographs (${surfaces.style.photos.join(', ')}): sunlit-face medians of sample boxes, recorded in research/assets/plans/atlas-explorer/surface-samples-2026-10-17. ${surfaces.style.masonryNote??''} Individual stones, joints, chipped edges, plaster wear and soil relief remain illustrative, not recorded stones or weathering; photographs vary in exposure and white balance.`:`Surface art uses a ${surfaces.style.id} material palette, metre-scaled stone joints, chipped edges, plaster wear and soil relief. These are illustrative visual treatments, not recorded individual stones or weathering.`);
 assumptions.push(context.patch?"Surrounding relief is sampled from Mapterhorn’s modern elevation tiles around the existing site anchor. The local bench is feathered to expose the model. Architectural position and bearing are schematic, not surveyed or registered; the terrain is not ancient ground level.":"The rock setting is illustrative because this cave has no established geographic coordinates.");
 const starts:Record<string,[string,number,number,number,number]>={'gerizim-precinct':['east-stair',28,22,308,100],'hyrcania-waterworks':['north-pool',0,-12,180,76],'jericho-early':['complex',0,6,0,76],'jericho-late':['complex',0,12,0,76],'siloam-receiver':['L103',0,6,0,80],'doq-waterworks':['intake',4,5,-35,83],'jericho-ac':['AC94',0,7,0,80],'bethesda-pools':['dam',-12,0,160,84],'east-gate-warren':['massive-wall',8,-12,270,90]};
 const start=starts[plan.id],point=start?markers.get(start[0]):undefined;
 const walkStart=point&&start?{position:[point.x+start[1],point.z+start[2]] as Point,bearing:start[3],pitch:start[4]}:undefined;
 return {root,roof,markers,selectable,note,assumptions,units,walkStart,framing:bounds.translate(new T.Vector3(-center.x,0,-center.z)),landscape:{context:context.context,credit:context.credit,mapped:!!context.patch}};
}
