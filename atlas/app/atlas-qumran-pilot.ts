import * as T from "three";
import { MercatorCoordinate } from "maplibre-gl";
import { createSiteMaterials, chippedBlock, cloneSiteMaterial } from "./atlas-site-materials";

// Display alignment only. Neither this anchor nor page-up orientation is a surveyed fit.
export const PILOT_ANCHOR = [35.45056,31.74111] as [number,number];
export const PILOT_ID = "qumran-source-pilot";
export const pilotAvailable = (id:string|null)=>id==="kh_qumran"||id==="wadi_qumran";
export const pilotStops = {
 overview:{label:"Whole site",x:0,z:0,zoom:19,pitch:65},
 intake:{label:"Intake",x:-25.6,z:-8,zoom:21,pitch:75},
 branch:{label:"Branch",x:-15.2,z:-4,zoom:21,pitch:75},
 tunnel:{label:"Tunnel mouth",x:4,z:5.6,zoom:22,pitch:83}
};
export type PilotStop = keyof typeof pilotStops;
export function pilotLocation(x:number,z:number):[number,number] {
 const m=MercatorCoordinate.fromLngLat(PILOT_ANCHOR),s=m.meterInMercatorCoordinateUnits();
 const p=new MercatorCoordinate(m.x+x*s,m.y+z*s,0).toLngLat();return [p.lng,p.lat];
}

// Manually sampled relationships from Ilan–Amit 1989 p.283 Fig.1.
// 0.2 m per redrawing unit is a display scale; cross-sections and elevations are illustrative.
const route=[[253,1200],[272,1209],[295,1212],[305,1220],[343,1230],[355,1238],[361,1245],[383,1271],[401,1268],[410,1263],[433,1263],[450,1255],[472,1271],[498,1252],[552,1215],[574,1172],[605,1147]];
const branch=[[305,1220],[318,1247],[335,1262],[350,1256],[361,1245]];
const local=([x,z]:number[])=>new T.Vector3((x-381)*.2,0,(z-1240)*.2);
function random(seed:number){let n=seed>>>0;return ()=>{n=(n*1664525+1013904223)>>>0;return n/4294967296;};}
const smooth=(a:number,b:number,v:number)=>T.MathUtils.smoothstep(v,a,b);
// An irregular, feathered apron replaces the rectangular display tile. Map
// elevation offsets the whole model consistently, preserving source-plan X/Z.
const apronRadius=(x:number,z:number)=>Math.hypot(x/118,z/94)/(1+.055*Math.sin(Math.atan2(z,x)*5)+.035*Math.cos(Math.atan2(z,x)*9));
export function fitQumranGround(root:T.Group,sample:(x:number,z:number)=>number){
 // A small elevation grid avoids thousands of map queries on phone GPUs.
 const n=8,extent=130,values:number[]=[];
 for(let j=0;j<=n;j++)for(let i=0;i<=n;i++)values.push(sample((i/n*2-1)*extent,(j/n*2-1)*extent));
 const elevation=(x:number,z:number)=>{
  const u=T.MathUtils.clamp((x/extent+1)*n/2,0,n),v=T.MathUtils.clamp((z/extent+1)*n/2,0,n),i=Math.min(n-1,Math.floor(u)),j=Math.min(n-1,Math.floor(v));
  const at=(x:number,z:number)=>values[z*(n+1)+x];
  return T.MathUtils.lerp(T.MathUtils.lerp(at(i,j),at(i+1,j),u-i),T.MathUtils.lerp(at(i,j+1),at(i+1,j+1),u-i),v-j);
 };
 root.traverse(object=>{
  if(!(object instanceof T.Mesh))return;
  if(object instanceof T.InstancedMesh){
   const source=object.userData.sourceMatrices as Float32Array;
   object.instanceMatrix.array.set(source);
   for(let i=0;i<object.count;i++){
    const k=i*16,x=source[k+12],z=source[k+14],dx=(elevation(x+.25,z)-elevation(x-.25,z))/.5,dz=(elevation(x,z+.25)-elevation(x,z-.25))/.5;
    object.instanceMatrix.array[k+13]+=elevation(x,z);
    // Tilt long channel floors with the same local slope as their ground;
    // translating only their centres would leave the ends suspended in air.
    for(const column of [0,4,8])object.instanceMatrix.array[k+column+1]+=dx*source[k+column]+dz*source[k+column+2];
   }
   object.instanceMatrix.needsUpdate=true;object.computeBoundingSphere();return;
  }
  const p=object.geometry.getAttribute('position'),base=object.geometry.getAttribute('sourceHeight');
  for(let k=0;k<p.count;k++)p.setY(k,base.getX(k)+elevation(p.getX(k)+object.position.x,p.getZ(k)+object.position.z));
  p.needsUpdate=true;object.geometry.computeVertexNormals();object.geometry.computeBoundingSphere();
 });
}

export function buildQumranPilot(){
 const root=new T.Group(),rand=random(979),surfaces=createSiteMaterials('qumran-ilan');
 const {block:stone,plaster,rock}=surfaces;
 const dirt=cloneSiteMaterial(surfaces.earth);dirt.vertexColors=true;dirt.transparent=true;dirt.depthWrite=false;
 const dark=new T.MeshStandardMaterial({color:'#191913',roughness:1,side:T.DoubleSide});
 const blockGeometry=chippedBlock(1,1,1,19);
 function mesh(g:T.BufferGeometry,m:T.Material){const o=new T.Mesh(g,m);o.castShadow=o.receiveShadow=true;root.add(o);return o;}
 function block(x:number,y:number,z:number,w:number,h:number,d:number,m:T.Material){const o=mesh(blockGeometry,m);o.scale.set(w,h,d);o.position.set(x,y+h/2,z);o.userData.siteBlock=true;return o;}
 // Display relief only. The source-plan channel route below is preserved.
 const height=(x:number,z:number)=>.3+Math.max(0,1-Math.abs(z-2)/23)*1.7+.35*Math.sin(x*.13)*Math.cos(z*.21);
 // Basin 2 (Ilan–Amit 1989 Fig. 1), sampled from the same plan as the route.
 const bend=(a:number[],c:number[],b:number[],n=6)=>Array.from({length:n},(_,i)=>{const t=(i+1)/n;return [(1-t)**2*a[0]+2*(1-t)*t*c[0]+t*t*b[0],(1-t)**2*a[1]+2*(1-t)*t*c[1]+t*t*b[1]];});
 const basinOutline=[[160,1220],...bend([160,1220],[140,1245],[169,1280]),[215,1285],[241,1258],[234,1214]].map(local);
 const inBasin=(x:number,z:number)=>{let hit=false;for(let i=0,j=basinOutline.length-1;i<basinOutline.length;j=i++){const a=basinOutline[i],b=basinOutline[j];if((a.z>z)!==(b.z>z)&&x<(b.x-a.x)*(z-a.z)/(b.z-a.z)+a.x)hit=!hit;}return hit;};
 const ground=new T.PlaneGeometry(260,220,130,110);ground.rotateX(-Math.PI/2);
 const gp=ground.getAttribute('position'),colours:number[]=[],sourceHeight:number[]=[],indices:number[]=[];
 for(let i=0;i<gp.count;i++){
  const x=gp.getX(i),z=gp.getZ(i),r=apronRadius(x,z),fade=1-smooth(.57,1,r),y=height(x,z)*(1-smooth(.55,.98,r));
  gp.setY(i,y);sourceHeight.push(y);colours.push(1,1,1,fade);
 }
 const oldIndex=ground.getIndex()!;
 for(let i=0;i<oldIndex.count;i+=3){const a=oldIndex.getX(i),b=oldIndex.getX(i+1),c=oldIndex.getX(i+2);if(colours[a*4+3]+colours[b*4+3]+colours[c*4+3]>.001&&!inBasin((gp.getX(a)+gp.getX(b)+gp.getX(c))/3,(gp.getZ(a)+gp.getZ(b)+gp.getZ(c))/3))indices.push(a,b,c);}
 ground.setIndex(indices);ground.setAttribute('color',new T.Float32BufferAttribute(colours,4));ground.setAttribute('sourceHeight',new T.Float32BufferAttribute(sourceHeight,1));ground.computeVertexNormals();
 const apron=mesh(ground,dirt);apron.name='qumran-ground';apron.userData.holes=[basinOutline.map(p=>[p.x,p.z])];apron.castShadow=false;apron.renderOrder=-3;apron.userData.walkSurface=true;
 const mouth=local([401,1268]),my=height(mouth.x,mouth.z)+.2;
 // Connected beds of fractured limestone, rather than a cloud of smooth rocks.
 // The projecting spur and every bed/joint here are illustrative scenery.
 const front=(x:number)=>-9+14*Math.exp(-(((x-mouth.x)/7)**2))+1.1*Math.sin(x*.23);
 const ridge=(x:number)=>Math.max(0,1-(Math.abs(x)/85)**4)**2*(6.8+1.3*Math.sin(x*.061)+.65*Math.sin(x*.23));
 const edge=(x:number,row:number)=>front(x)-row*.40*ridge(x)/7+.48*Math.sin(x*.63)+.28*Math.sin(x*1.7+row*1.3)+.13*Math.cos(x*4.3+row);
 const level=(x:number,row:number)=>height(x,front(x))-.22+ridge(x)*(row+.24*Math.sin(x*.11+row*2.1)*Math.sin(row*Math.PI/11))/11;
 const cliffRock=cloneSiteMaterial(rock);cliffRock.vertexColors=true;cliffRock.transparent=true;cliffRock.alphaTest=.01;
 for(let row=0;row<11;row++){
  const positions:number[]=[],uv:number[]=[],colours:number[]=[];
  function vertex(x:number,y:number,z:number){positions.push(x,y,z);uv.push(x/5,y/5);colours.push(1,1,1,smooth(.05,.9,ridge(x)));}
  function tri(a:number[],b:number[],c:number[]){vertex(a[0],a[1],a[2]);vertex(b[0],b[1],b[2]);vertex(c[0],c[1],c[2]);}
  function quad(a:number[],b:number[],c:number[],d:number[]){tri(a,b,d);tri(b,c,d);}
  for(let i=0;i<170;i++){
   const x=-85+i,x2=x+1;
   // A real opening in the display mesh leaves the tunnel recess visible.
   if(row<2&&Math.abs(x+.5-mouth.x)<1.1)continue;
   const a=[x,level(x,row),edge(x,row)],b=[x2,level(x2,row),edge(x2,row)],c=[x2,level(x2,row+1)+.08,edge(x2,row)-.12],d=[x,level(x,row+1)+.08,edge(x,row)-.12];
   quad(a,b,c,d);
   // Short weathered shelves join successive beds, rather than full-depth slabs.
   quad(d,c,[x2,level(x2,row+1),edge(x2,row+1)],[x,level(x,row+1),edge(x,row+1)]);
  }
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setAttribute('color',new T.Float32BufferAttribute(colours,4));g.computeVertexNormals();
  const face=mesh(g,cliffRock);face.name='connected-limestone-bed';face.renderOrder=-1;face.userData.stratum=row;
 }
 // The uneven crest rolls back into the apron. No rectangular lid or cut ends.
 const backPositions:number[]=[],backColours:number[]=[],backIndices:number[]=[],steps=28;
 for(let i=0;i<=170;i++)for(let j=0;j<=steps;j++){
  const x=-85+i,t=j/steps,start=edge(x,11),z=T.MathUtils.lerp(start,-64+4*Math.sin(x*.09),t),rise=ridge(x)*(1-smooth(0,1,t));
  backPositions.push(x,T.MathUtils.lerp(height(x,front(x)),height(x,z),smooth(0,1,t))+rise-.22*(1-t),z);backColours.push(1,1,1,(1-smooth(.4,1,t))*(1-smooth(48,85,Math.abs(x))));
 }
 for(let i=0;i<170;i++)for(let j=0;j<steps;j++){const a=i*(steps+1)+j,b=a+steps+1;backIndices.push(a,b,a+1,b,b+1,a+1);}
 const back=new T.BufferGeometry();back.setAttribute('position',new T.Float32BufferAttribute(backPositions,3));back.setAttribute('color',new T.Float32BufferAttribute(backColours,4));back.setIndex(backIndices);back.computeVertexNormals();
 const backSoil=cloneSiteMaterial(dirt);backSoil.vertexColors=true;backSoil.transparent=true;
 const slope=mesh(back,backSoil);slope.name='qumran-ridge-back';slope.castShadow=false;slope.renderOrder=-2;slope.userData.walkSurface=true;
 // Angular scree sits on the ground, with a few large fallen slabs at the bank.
 const rubble=new T.InstancedMesh(chippedBlock(1,.65,1,41),stone,1350),o=new T.Object3D();
 for(let i=0;i<1350;i++){
  const x=(rand()-.5)*156,z=i<160?front(x)+rand()*9:(rand()-.5)*118,r=apronRadius(x,z),s=(i<160?.25+rand()*.7:.035+rand()*.2)*(1-smooth(.55,.8,r));
  o.position.set(x,height(x,z)+s*.2,z);o.rotation.set((rand()-.5)*.5,rand()*6.28,(rand()-.5)*.4);o.scale.set(s*(1+rand()),s,s*(.6+rand()));o.updateMatrix();rubble.setMatrixAt(i,o.matrix);rubble.setColorAt(i,new T.Color().setScalar(.72+rand()*.4));
 }rubble.castShadow=rubble.receiveShadow=true;rubble.userData.walkDetail=true;root.add(rubble);
 function channel(points:number[][]){for(let i=1;i<points.length;i++){
  const a=local(points[i-1]),b=local(points[i]),length=a.distanceTo(b),yaw=-Math.atan2(b.z-a.z,b.x-a.x),group=new T.Group();group.position.set((a.x+b.x)/2,height((a.x+b.x)/2,(a.z+b.z)/2)+.15,(a.z+b.z)/2);group.rotation.y=yaw;root.add(group);
  const floor=block(0,0,0,length,.12,.65,plaster);root.remove(floor);group.add(floor);floor.position.set(0,.06,0);
  for(const side of [-1,1]){const count=Math.ceil(length/.55);for(let k=0;k<count;k++){
   const x=-length/2+(k+.5)*length/count,h=.38+rand()*.14;
   const b=block(0,0,0,length/count-.025,h,.24,stone);root.remove(b);group.add(b);b.position.set(x,.18,side*.43);b.rotation.y=(rand()-.5)*.06;
   // Pale lining and small missing patches distinguish the water face.
   if(k%4!==0){const lining=block(0,0,0,length/count-.06,h*.62,.018,plaster);root.remove(lining);group.add(lining);lining.position.set(x,.19,side*.303);}
  }}
 }}channel(route);channel(branch);
 // Basin 2 as a rock-floored hollow, and the dam proposed at point 4. Ilan–Amit 2002
 // Fig. 1 (p. 380) draws a heavy dashed line from point 3 to point 4 across the basin's
 // east side; the authors report no surviving dam. Copper marks the reconstruction.
 // The basin depth and the dam's height and width are illustrative.
 const basinFloor=Math.min(...basinOutline.map(p=>height(p.x,p.z)))-1.4,floorShape=new T.Shape();
 basinOutline.forEach((p,i)=>i?floorShape.lineTo(p.x,-p.z):floorShape.moveTo(p.x,-p.z));
 const floorGeometry=new T.ExtrudeGeometry(floorShape,{depth:.3,bevelEnabled:false});floorGeometry.rotateX(-Math.PI/2);
 const basinBed=mesh(floorGeometry,rock);basinBed.position.y=basinFloor-.3;basinBed.name='basin-2';basinBed.userData.featureId='basin2';basinBed.userData.walkSurface=true;
 for(let i=0;i<basinOutline.length;i++){
  const a=basinOutline[i],b=basinOutline[(i+1)%basinOutline.length],top=Math.max(height(a.x,a.z),height(b.x,b.z));
  const side=block((a.x+b.x)/2,basinFloor,(a.z+b.z)/2,a.distanceTo(b)+.5,top-basinFloor,.5,rock);side.rotation.y=-Math.atan2(b.z-a.z,b.x-a.x);
 }
 const copper=new T.MeshStandardMaterial({color:'#b56b42',roughness:.94,metalness:0}),d0=local([234,1214]),d1=local([250,1268]),damX=(d0.x+d1.x)/2,damZ=(d0.z+d1.z)/2;
 const dam=block(damX,basinFloor,damZ,d0.distanceTo(d1),height(damX,damZ)+.6-basinFloor,1.2,copper);dam.rotation.y=-Math.atan2(d1.z-d0.z,d1.x-d0.x);
 // A shaded, angular opening with worn jambs and a fractured lintel. Shape and
 // dimensions are interpretive, informed by the archived outlet photograph.
 for(const side of [-1,1]){
  block(mouth.x+side*.91,my-.08,mouth.z-1,.47,1.25,3.1,stone);
  block(mouth.x+side*1.34,my-.15,mouth.z-.35,.65,1.5,1.4,rock);
 }
 const lintel=block(mouth.x,my+1.16,mouth.z-.2,2.5,.42,1.4,rock);lintel.rotation.z=-.08;
 block(mouth.x,my+1.3,mouth.z-2,2.1,.55,3.1,rock);
 const recess=mesh(new T.PlaneGeometry(1.45,1.3),dark);recess.position.set(mouth.x,my+.58,mouth.z-2.6);recess.castShadow=false;
 block(mouth.x,my-.05,mouth.z-1,.9,.12,3,plaster);
 // Batch hundreds of channel stones by material. Detail remains in geometry
 // while phone GPUs submit only a handful of draws for the masonry.
 root.updateMatrixWorld(true);const batches=new Map<T.Material,T.Mesh[]>();
 root.traverse(o=>{if(o instanceof T.Mesh&&o.userData.siteBlock){const material=o.material as T.Material;const batch=batches.get(material)??[];batch.push(o);batches.set(material,batch);}});
 for(const [material,blocks] of batches){const batch=new T.InstancedMesh(blockGeometry,material,blocks.length);batch.castShadow=batch.receiveShadow=true;blocks.forEach((block,i)=>{batch.setMatrixAt(i,block.matrixWorld);batch.setColorAt(i,new T.Color().setScalar(.88+(i*17%31)/130));block.removeFromParent();});root.add(batch);}
 // Rock, scree and channels follow the same surface as the soil. Source-plan
 // horizontal relationships stay fixed; elevations and the DEM fit are illustrative.
 root.traverse(object=>{
  if(!(object instanceof T.Mesh))return;
  if(object instanceof T.InstancedMesh){object.userData.sourceMatrices=Float32Array.from(object.instanceMatrix.array);return;}
  if(object.geometry.hasAttribute('sourceHeight'))return;
  const p=object.geometry.getAttribute('position'),base:number[]=[];
  for(let i=0;i<p.count;i++)base.push(p.getY(i));
  object.geometry.setAttribute('sourceHeight',new T.Float32BufferAttribute(base,1));
 });
 return root;
}
