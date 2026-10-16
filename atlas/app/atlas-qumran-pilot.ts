import * as T from "three";
import { MercatorCoordinate, type Map, type CustomLayerInterface } from "maplibre-gl";

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
 const root=new T.Group(),rand=random(979);
 const stone=new T.MeshStandardMaterial({color:"#c9b797",roughness:1,vertexColors:true});
 const plaster=new T.MeshStandardMaterial({color:"#c7bfa5",roughness:1});
 const dark=new T.MeshStandardMaterial({color:"#514b3f",roughness:1,side:T.DoubleSide});
 const dirt=new T.MeshStandardMaterial({color:"#b6a383",roughness:1,vertexColors:true});
 // Weathering is deterministic rendering detail, never a record of individual stones.
 function weather(g:T.BufferGeometry,base:T.Color,amount=.12){const p=g.getAttribute("position"),c=[];
  for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i);const n=Math.sin(x*7.3+y*13.7+z*9.1)*Math.sin(z*16.1+x*3.7);const band=Math.sin(y*15+Math.sin(x*.7)*.5);const b=1+amount*n+band*.035;c.push(base.r*b,base.g*b,base.b*b);}
  g.setAttribute("color",new T.Float32BufferAttribute(c,3));return g;}
 function mesh(g:T.BufferGeometry,m:T.Material){const o=new T.Mesh(g,m);root.add(o);return o;}
 function block(x:number,y:number,z:number,w:number,h:number,d:number,m:T.Material){const g=new T.BoxGeometry(w,h,d,2,2,2);if(m===stone)weather(g,new T.Color("#ffffff"));const o=mesh(g,m);o.position.set(x,y+h/2,z);return o;}
 // A raised, source-relative rock outcrop keeps the open channel visible above contextual DEM.
 const height=(x:number,z:number)=>.3+Math.max(0,1-Math.abs(z-2)/23)*1.7+.35*Math.sin(x*.13)*Math.cos(z*.21);
 const ground=new T.PlaneGeometry(128,78,128,78);ground.rotateX(-Math.PI/2);
 const gp=ground.getAttribute("position");for(let i=0;i<gp.count;i++){const x=gp.getX(i),z=gp.getZ(i),edge=Math.min((64-Math.abs(x))/10,(39-Math.abs(z))/10,1);gp.setY(i,Math.max(0,edge)*height(x,z));}ground.computeVertexNormals();mesh(weather(ground,new T.Color("#ffffff")),dirt);
 // Layered limestone bank. Interior mouth is left open at the long-tunnel position.
 const rocks=new T.InstancedMesh(weather(new T.IcosahedronGeometry(1,1),new T.Color("#ffffff")),stone,1250);
 const transform=new T.Object3D(),tint=new T.Color();
 for(let i=0;i<1250;i++){const x=(rand()-.5)*116,z=-10-rand()*14,y=height(x,z)+rand()*7.5;
  transform.position.set(x,y,z);transform.rotation.set(rand()*.5,rand()*6.28,rand()*.4);transform.scale.set(.5+rand()*2.5,.25+rand()*.65,.45+rand()*1.4);transform.updateMatrix();rocks.setMatrixAt(i,transform.matrix);tint.setRGB(.82+rand()*.15,.81+rand()*.14,.76+rand()*.13);rocks.setColorAt(i,tint);}
 root.add(rocks);
 const rubble=new T.InstancedMesh(weather(new T.DodecahedronGeometry(1,0),new T.Color("#ffffff")),stone,850);
 for(let i=0;i<850;i++){const x=(rand()-.5)*119,z=(rand()-.5)*70;transform.position.set(x,height(x,z)+.04,z);transform.rotation.set(rand()*3,rand()*6,rand()*3);const s=.025+rand()*.21;transform.scale.set(s*1.7,s,s);transform.updateMatrix();rubble.setMatrixAt(i,transform.matrix);}root.add(rubble);
 function channel(points:number[][]){for(let i=1;i<points.length;i++){const a=local(points[i-1]),b=local(points[i]),length=a.distanceTo(b),yaw=-Math.atan2(b.z-a.z,b.x-a.x),group=new T.Group();group.position.set((a.x+b.x)/2,height((a.x+b.x)/2,(a.z+b.z)/2)+.15,(a.z+b.z)/2);group.rotation.y=yaw;root.add(group);
   const floor=block(0,0,0,length,.12,.65,plaster);root.remove(floor);group.add(floor);floor.position.set(0,.06,0);
   for(const side of [-1,1]){const count=Math.ceil(length/.55);for(let k=0;k<count;k++){const x=-length/2+(k+.5)*length/count;const o=block(0,0,0,length/count-.025,.38+rand()*.14,.24,stone);root.remove(o);group.add(o);o.position.set(x,.18,side*.43);o.rotation.y=(rand()-.5)*.06;}}
  }}channel(route);channel(branch);
 // Photo-referenced mouth form, with an actual dark interior and irregular stone surround.
 const mouth=local([401,1268]),my=height(mouth.x,mouth.z)+.2;
 const shell=new T.CylinderGeometry(1.15,1.2,5.8,24,1,true,0,Math.PI);shell.rotateZ(Math.PI/2);shell.rotateY(Math.PI/2);
 const cover=mesh(weather(shell,new T.Color("#ffffff")),stone);cover.position.set(mouth.x,my+.3,mouth.z-1.8);cover.material=stone.clone();(cover.material as T.Material).side=T.DoubleSide;
 const recess=mesh(new T.PlaneGeometry(1.6,1.45),dark);recess.position.set(mouth.x,my+.7,mouth.z-2.2);
 for(let i=0;i<11;i++){const angle=i*Math.PI/10;const b=block(mouth.x+Math.cos(angle)*1.1,my+Math.sin(angle)*1.1,mouth.z,.4,.3,.65,stone);b.rotation.z=angle-.5*Math.PI;}
 block(mouth.x,my-.05,mouth.z-1,.9,.12,2.4,plaster);
 return root;
}

export function createQumranLayer(map:Map,onFailure:(message:string)=>void):CustomLayerInterface {
 let renderer:T.WebGLRenderer|undefined,root:T.Group|undefined;
 const scene=new T.Scene(),camera=new T.Camera();
 return {id:PILOT_ID,type:"custom",renderingMode:"3d",
  onAdd(_map,gl){try{root=buildQumranPilot();scene.add(root);scene.add(new T.HemisphereLight(0xfff5df,0x736955,2.4));const sun=new T.DirectionalLight(0xffedd2,2.5);sun.position.set(-50,90,35);scene.add(sun);renderer=new T.WebGLRenderer({canvas:map.getCanvas(),context:gl});renderer.autoClear=false;}catch{onFailure("Site detail could not load. Source plans and photographs remain available.");}},
  render(_gl,args){if(!renderer||!root||map.getZoom()<16)return;
   const elevation=map.queryTerrainElevation(PILOT_ANCHOR);if(elevation===null)return;
   const origin=MercatorCoordinate.fromLngLat(PILOT_ANCHOR,elevation+.15),s=origin.meterInMercatorCoordinateUnits();
   const localMatrix=new T.Matrix4().makeTranslation(origin.x,origin.y,origin.z).scale(new T.Vector3(s,-s,s)).multiply(new T.Matrix4().makeRotationX(Math.PI/2));
   camera.projectionMatrix.fromArray(args.defaultProjectionData.mainMatrix).multiply(localMatrix);
   renderer.resetState();renderer.render(scene,camera);renderer.resetState();
  },
  onRemove(){scene.traverse(o=>{if(o instanceof T.Mesh){o.geometry.dispose();const mats=Array.isArray(o.material)?o.material:[o.material];mats.forEach(m=>m.dispose());if(o instanceof T.InstancedMesh)o.dispose();}});renderer?.dispose();}
 };
}
