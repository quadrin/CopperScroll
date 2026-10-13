import * as T from "three";
import { landscapeGround, type LandscapeGround } from "./atlas-model-landscape";
import { SVGLoader } from "three/addons/loaders/SVGLoader.js";
import type { SitePlan } from "./atlas-explorer-model";

export type { ModelCamera } from "./atlas-explorer-model";
export type ModelGeometry = { root: T.Group; markers: Map<string, T.Vector3>; selectable: T.Object3D[]; roof: T.Group; note: string; assumptions: string[]; units: "metres" | "relative"; framing:T.Box3; landscape:{context:string;credit:string;mapped:boolean} };
type Point = [number, number];

function texture() {
 const n=128, data=new Uint8Array(n*n*4);let seed=1457;
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  seed=(seed*1664525+1013904223)>>>0;const noise=(seed/4294967296-.5)*18;
  const mortar=y%32<2||(x+(Math.floor(y/32)%2)*32)%64<2;
  const c=(mortar?202:238)+noise,i=(y*n+x)*4;
  data[i]=c;data[i+1]=c-8;data[i+2]=c-23;data[i+3]=255;
 }
 const tex=new T.DataTexture(data,n,n);tex.wrapS=tex.wrapT=T.RepeatWrapping;tex.colorSpace=T.SRGBColorSpace;tex.needsUpdate=true;return tex;
}
function polygon(points:Point[]) {const s=new T.Shape();points.forEach(([x,z],i)=>i?s.lineTo(x,-z):s.moveTo(x,-z));s.closePath();return s;}
function material(color:string,map?:T.Texture){return new T.MeshStandardMaterial({color,map:map??null,roughness:.94,metalness:0});}
export function buildModel(plan:SitePlan):ModelGeometry {
 const root=new T.Group(), roof=new T.Group(),markers=new Map<string,T.Vector3>(),selectable:T.Object3D[]=[];
 const stone=material("#ede2cc",texture()),rock=material("#b5a283"),earth=material("#c5b89b"),plaster=material("#b8c9bf"),copper=material("#b56b42");
 const wellHoles:Point[][]=[];let ground:LandscapeGround={w:40,d:40,holes:[],pads:[]};
 const circlePoints=(x:number,z:number,r:number):Point[]=>Array.from({length:36},(_,i)=>[x+Math.cos(i*Math.PI/18)*r,z+Math.sin(i*Math.PI/18)*r]);
 const assumptions:string[]=[];let note="Plan relations in 3D · heights illustrative",units:ModelGeometry["units"]="relative";
 const tag=(mesh:T.Object3D,id?:string)=>{if(id){mesh.userData.featureId=id;selectable.push(mesh)}return mesh};
 function mesh(geometry:T.BufferGeometry,mat:T.Material,id?:string,parent=root){const m=new T.Mesh(geometry,mat.clone());m.castShadow=true;m.receiveShadow=true;parent.add(tag(m,id));return m;}
 function box(x:number,z:number,w:number,d:number,h:number,y=0,id?:string,mat:T.Material=stone,parent=root){const m=mesh(new T.BoxGeometry(w,h,d),mat,id,parent);m.position.set(x,y+h/2,z);return m;}
 function slab(points:Point[],depth:number,y=0,mat:T.Material=stone,id?:string,parent=root,holes:Point[][]=[]){const s=polygon(points);for(const hole of holes)s.holes.push(polygon(hole));const g=new T.ExtrudeGeometry(s,{depth,bevelEnabled:false,curveSegments:12});g.rotateX(-Math.PI/2);const m=mesh(g,mat,id,parent);m.position.y=y;return m;}
 function tube(points:T.Vector3[],radius:number,mat:T.Material=stone,id?:string,parent=root){const curve=new T.CatmullRomCurve3(points,false,"centripetal");return mesh(new T.TubeGeometry(curve,Math.max(16,points.length*6),radius,8,false),mat,id,parent);}
 function walls(points:Point[],height:number,thickness:number,y=0,id?:string,closed=true,mat:T.Material=stone){
  for(let i=0;i<points.length-(closed?0:1);i++){
   const a=points[i],b=points[(i+1)%points.length],length=Math.hypot(b[0]-a[0],b[1]-a[1]);
   const m=box((a[0]+b[0])/2,(a[1]+b[1])/2,length,thickness,height,y,id,mat);m.rotation.y=-Math.atan2(b[1]-a[1],b[0]-a[0]);
   // Horizontal courses make the volumes legible at a distance; no masonry survey is implied.
   for(let k=1;mat===stone&&k<Math.min(5,height/.45);k++){const seam=box((a[0]+b[0])/2,(a[1]+b[1])/2,length+.01,thickness+.014,.024,y+height*k/Math.ceil(Math.min(5,height/.45)),id,rock);seam.rotation.y=m.rotation.y;}
  }
 }
 function court(x:number,z:number,w:number,d:number,h:number,id?:string,holes:Point[][]=[]){const p:Point[]=[[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]];slab(p,.25,0,earth,id,root,holes);walls(p,h,Math.max(.28,w*.025),0,id);}
 function basin(points:Point[],depth:number,id:string){
  slab(points,.3,-depth-.3,plaster,id);walls(points,depth,.35,-depth,id);
  points.forEach((a,i)=>{const b=points[(i+1)%points.length];tube([new T.Vector3(a[0],.035,a[1]),new T.Vector3(b[0],.035,b[1])],.10,stone,id)});
 }
 function shaft(x:number,z:number,r:number,depth:number,id:string){
  wellHoles.push(circlePoints(x,z,r+.02));
  const g=new T.CylinderGeometry(r,r*.78,depth,32,1,true);const m=mesh(g,stone,id);m.position.set(x,-depth/2,z);m.material=(stone.clone());(m.material as T.MeshStandardMaterial).side=T.DoubleSide;
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
  basin(n,5,"north-pool");basin(s,2.6,"south-member");marker("north-pool",-10,-19,.55);marker("south-member",-10,.1,.55);
  slab([[-23,-30],[4,-30],[4,11],[-23,11]],.8,-5.8,rock,undefined,root,[n,s]);
  const bridge=box(-9,17,32,2.4,3.1,-3.2,"bridge");bridge.rotation.y=.35;
  for(let i=0;i<8;i++)box(-24+i*4,17,1,2.5,2.6,-3.2,"bridge",rock);
  tube([new T.Vector3(-30,.2,4),new T.Vector3(-14,.2,18),new T.Vector3(4,.2,24)],.26,stone,"bridge");marker("bridge",-9,17,1);
  basin([[-27,20],[-15,20],[-15,31],[-27,31]],1.8,"separate-pool");marker("separate-pool",-21,25,.6);
  court(20,12,28,37,2.1);court(20,12,11,15,1.9);box(32,-3,6,7,3.2);
  for(const [x,z] of [[16,35],[24,38],[39,4],[42,-7]])shaft(x,z,2,3,"cisterns");marker("cisterns",20,36,.7);
  plinth(88,86,6.3,[n,s,[[-27,20],[-15,20],[-15,31],[-27,31]]]);
  assumptions.push("Northern pool sides approximate the published 19 / 15 / 18.2 / 16 m quadrilateral. Published maximum depths are shown: about 5 m north, 2.6 m south.","Rock separation uses 5.1 m, the midpoint of the reported 4.8–5.4 m range. Southern outline, bridge dimensions in this view, summit walls, other cistern depths and surrounding relief are illustrative.","No north bearing is assigned to the source frame. Floors are tinted to distinguish basins; the tint is not a reconstructed water level. Centre/rim origins and construction phases remain unresolved.");
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
  tube(pts.map(p=>{const [x,z]=conv(p);return new T.Vector3(x,.65,z)}),.32,stone,"intake");
  for(const p of [[145,357],[155,365],[168,373],[178,381],[191,388],[202,398],[215,408],[246,421],[289,424],[306,375]] as Point[]){const [x,z]=conv(p);shaft(x,z,1.15,3.2,"cisterns");}
  court(-2,6,8,4,1.1);box(-2,6,2,1.6,.4,0,undefined,rock);
  tube([[119,285],[195,264],[266,279]].map(p=>{const [x,z]=conv(p as Point);return new T.Vector3(x,.2,z)}),.6,rock,"ditch");
  for(const f of plan.features){const [x,z]=conv([f.x,f.y]);marker(f.id,x,z,1.5)}
  plinth(39,38,3.8);
  assumptions.push("The aqueduct and ten cistern positions follow selected relationships in Amit Fig. 2. The frame is normalized for display, without geographic registration.","Cistern diameters/depths, channel cross-section, defensive wall heights and ridge relief are illustrative. The source does not identify a guard-post or drying-room corner.");
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
    else tube(pts.map(([x,z])=>new T.Vector3(x,piece.kind==="tunnel"?.55:.18,z)),piece.kind==="tunnel"?.6:.2,piece.kind==="reconstruction"?copper:stone,id);
   }
  }
  for(const f of plan.features){const [x,z]=conv(f.x,f.y);marker(f.id,x,z,1.2);}
  if(!pieces?.length)for(const f of plan.features){const [x,z]=conv(f.x,f.y);court(x,z,5,4,1.7,f.id);}
  plinth(40*plan.width/Math.max(plan.width,plan.height)+7,40*plan.height/Math.max(plan.width,plan.height)+7,2,basinHoles);
  assumptions.push("Selected source-plan outlines and feature envelopes are normalized into a relative scene. They are not new measured footprints.","Wall heights, pool depths, terrain/platform relief and conduit cross-sections are illustrative. Source phasing, restorations and feature interpretations remain those of the accompanying record.");
 }
 roof.visible=false;
 const bounds=new T.Box3().setFromObject(root);bounds.expandByPoint(new T.Vector3(-ground.w/2,-1,-ground.d/2));bounds.expandByPoint(new T.Vector3(ground.w/2,1,ground.d/2));const center=bounds.getCenter(new T.Vector3());
 root.position.set(-center.x,0,-center.z);markers.forEach(p=>{p.x-=center.x;p.z-=center.z});
 const context=landscapeGround(ground,plan.placeIds[0],[center.x,center.z]);context.mesh.position.set(center.x,0,center.z);root.add(context.mesh);
 assumptions.push(context.patch?"Surrounding relief is sampled from Mapterhorn’s modern elevation tiles around the existing site anchor. The local bench is feathered to expose the model. Architectural position and bearing are schematic, not surveyed or registered; the terrain is not ancient ground level.":"The rock setting is illustrative because this cave has no established geographic coordinates.");
 return {root,roof,markers,selectable,note,assumptions,units,framing:bounds.translate(new T.Vector3(-center.x,0,-center.z)),landscape:{context:context.context,credit:context.credit,mapped:!!context.patch}};
}
