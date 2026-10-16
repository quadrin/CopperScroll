import * as T from "three";
import { MercatorCoordinate } from "maplibre-gl";
import { createSiteMaterials, chippedBlock } from "./atlas-site-materials";

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

export function buildQumranPilot(){
 const root=new T.Group(),rand=random(979),surfaces=createSiteMaterials('qumran-ilan');
 const {block:stone,plaster,rock}=surfaces;
 const dirt=surfaces.earth;
 const dark=new T.MeshStandardMaterial({color:'#191913',roughness:1,side:T.DoubleSide});
 const blockGeometry=chippedBlock(1,1,1,19);
 function mesh(g:T.BufferGeometry,m:T.Material){const o=new T.Mesh(g,m);o.castShadow=o.receiveShadow=true;root.add(o);return o;}
 function block(x:number,y:number,z:number,w:number,h:number,d:number,m:T.Material){const o=mesh(blockGeometry,m);o.scale.set(w,h,d);o.position.set(x,y+h/2,z);o.userData.siteBlock=true;return o;}
 // Display relief only. The source-plan channel route below is preserved.
 const height=(x:number,z:number)=>.3+Math.max(0,1-Math.abs(z-2)/23)*1.7+.35*Math.sin(x*.13)*Math.cos(z*.21);
 const ground=new T.PlaneGeometry(180,140,180,140);ground.rotateX(-Math.PI/2);
 const gp=ground.getAttribute('position');for(let i=0;i<gp.count;i++){const x=gp.getX(i),z=gp.getZ(i),edge=Math.min((90-Math.abs(x))/15,(70-Math.abs(z))/15,1);gp.setY(i,Math.max(0,edge)*height(x,z));}ground.computeVertexNormals();mesh(ground,dirt).userData.walkSurface=true;
 const mouth=local([401,1268]),my=height(mouth.x,mouth.z)+.2;
 // Connected beds of fractured limestone, rather than a cloud of smooth rocks.
 // The projecting spur and every bed/joint here are illustrative scenery.
 const front=(x:number)=>-9+14*Math.exp(-(((x-mouth.x)/7)**2))+1.1*Math.sin(x*.23);
 for(let row=0;row<11;row++){
  const positions:number[]=[],uv:number[]=[];const base=row*.72;
  function vertex(x:number,y:number,z:number){positions.push(x,y,z);uv.push(x/5,y/5);}
  function tri(a:number[],b:number[],c:number[]){vertex(a[0],a[1],a[2]);vertex(b[0],b[1],b[2]);vertex(c[0],c[1],c[2]);}
  function quad(a:number[],b:number[],c:number[],d:number[]){tri(a,b,d);tri(b,c,d);}
  for(let i=0;i<120;i++){
   const x=-60+i,x2=x+1;
   // A real opening in the display mesh leaves the tunnel recess visible.
   if(row<2&&Math.abs(x+.5-mouth.x)<1.1)continue;
   const edge=(t:number)=>front(t)-row*.62+.20*Math.sin(t*2.7+row*1.3)+.12*Math.cos(t*5.3+row);
   const y=(t:number)=>height(t,front(t))+base-.35+.06*Math.sin(t*.8+row*.9);
   const a=[x,y(x),edge(x)],b=[x2,y(x2),edge(x2)],c=[x2,y(x2)+.90,edge(x2)-.12],d=[x,y(x)+.90,edge(x)-.12];
   quad(a,b,c,d);quad(d,c,[x2,c[1]-.03,-31],[x,d[1]-.03,-31]);
   // Darker undersides between strata create coherent, grounded ledges.
   quad(a,[x,a[1],-31],[x2,b[1],-31],b);
  }
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.computeVertexNormals();
  const face=mesh(g,rock);face.name='connected-limestone-bed';face.userData.stratum=row;
 }
 // Angular scree sits on the ground, with a few large fallen slabs at the bank.
 const rubble=new T.InstancedMesh(chippedBlock(1,.65,1,41),stone,1350),o=new T.Object3D();
 for(let i=0;i<1350;i++){
  const x=(rand()-.5)*145,z=(rand()-.5)*105,s=i<160?.25+rand()*.7:.035+rand()*.2;
  o.position.set(x,height(x,z)+s*.2,z);o.rotation.set((rand()-.5)*.5,rand()*6.28,(rand()-.5)*.4);o.scale.set(s*(1+rand()),s,s*(.6+rand()));o.updateMatrix();rubble.setMatrixAt(i,o.matrix);rubble.setColorAt(i,new T.Color().setScalar(.72+rand()*.4));
 }rubble.castShadow=rubble.receiveShadow=true;root.add(rubble);
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
 return root;
}
