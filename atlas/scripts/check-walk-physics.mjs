import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import ts from 'typescript';
import * as T from 'three';
import * as maplibre from 'maplibre-gl';
import {Octree} from 'three/addons/math/Octree.js';
import {Capsule} from 'three/addons/math/Capsule.js';
const exports={};const source=await readFile(new URL('../app/atlas-walk-physics.ts',import.meta.url),'utf8');
new Function('exports','require',ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS}}).outputText)(exports,name=>({'three':T,'three/addons/math/Octree.js':{Octree},'three/addons/math/Capsule.js':{Capsule}}[name]));
const {createWalkWorld,WalkCharacter,WalkInput}=exports;
const material=new T.MeshBasicMaterial();
function scene(){const root=new T.Group();const floor=new T.Mesh(new T.BoxGeometry(40,.2,40),material);floor.position.y=-.1;root.add(floor);return root;}
function block(root,x,y,z,w,h,d){const m=new T.Mesh(new T.BoxGeometry(w,h,d),material);m.position.set(x,y+h/2,z);root.add(m);return m;}
const input={forward:1,right:0,bearing:0,sprint:false,crouch:false,jump:false};
function run(body,seconds,value=input){for(let i=0;i<Math.round(seconds*120);i++)body.advance(1/120,value);}
let root=scene();block(root,0,0,-2,12,4,.08);let world=createWalkWorld(root),body=new WalkCharacter(()=>world,new T.Vector3(0,0,2));
run(body,3,{...input,sprint:true});assert(body.feet.z>-1.69,'Sprint cannot tunnel through a thin wall');assert(body.feet.z<-1,'The character must actually reach the wall');assert(body.grounded,'The body must stay grounded at the wall');
run(body,1,{...input,right:1});assert(body.feet.x>1,'Diagonal movement must slide along the wall');assert(body.feet.z>-1.69);
root=scene();block(root,0,0,-1,4,.28,2);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,2));run(body,.8);assert(body.feet.y>.27,'The body must step onto a low ledge');
root=scene();block(root,0,0,-1,4,1,2);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,2));run(body,2);assert(body.feet.z>.27,'A high ledge must block walking');assert(body.feet.y<.1,'The body cannot climb a vertical wall');
root=scene();world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3());body.advance(1/60,{...input,forward:0,jump:true});run(body,.2,{...input,forward:0});assert(body.feet.y>.5,'Jump must lift the physical body');run(body,1,{...input,forward:0});assert(body.feet.y<.02&&body.grounded,'Gravity must return the body to the floor');
root=scene();block(root,0,1.6,0,6,.3,6);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,5));run(body,2,{...input,crouch:true});assert(body.feet.z<3,'Crouching must enter a low passage');run(body,.2,{...input,forward:0});assert(body.crouched,'Releasing crouch must not put the head through a ceiling');assert(body.eye.y<1.6);
body.advance(1/60,{...input,forward:0,jump:true});for(let i=0;i<60;i++){body.advance(1/120,{...input,forward:0});assert(body.feet.y+1.5<1.61,'Jumping must not pass through a low ceiling');}
root=scene();const instances=new T.InstancedMesh(new T.BoxGeometry(12,3,.1),material,1);instances.setMatrixAt(0,new T.Matrix4().makeRotationY(.35).setPosition(0,1.5,-2));root.add(instances);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,2));run(body,2,{...input,sprint:true});const wallLocal=body.feet.clone().sub(new T.Vector3(0,0,-2)).applyAxisAngle(new T.Vector3(0,1,0),-.35);assert(wallLocal.z>.32,`Transformed masonry must keep the body in front of its rotated face: ${wallLocal.toArray()}`);
root=new T.Group();const slope=new T.Mesh(new T.PlaneGeometry(30,30,1,1),material);slope.rotation.x=-Math.PI/2+.35;root.add(slope);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,3));const startY=body.feet.y;run(body,1);assert(body.feet.y>startY+.6&&body.grounded,`Walking must follow a climbable slope: ${body.feet.toArray()}, grounded ${body.grounded}, startY ${startY}`);
root=scene();const steep=new T.BufferGeometry();steep.setAttribute('position',new T.Float32BufferAttribute([-5,0,0,5,0,0,-5,8,-4,5,0,0,5,8,-4,-5,8,-4],3));steep.computeVertexNormals();root.add(new T.Mesh(steep,material));world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,3));run(body,3,{...input,sprint:true});assert(body.feet.z>-.3&&body.feet.y<.5,'A steep cliff must block uphill movement instead of lifting the body through it');
const controls=new WalkInput();controls.press('s',100);controls.release('s');controls.press('s',280);assert(controls.read(0).sprint,'Double-tap S must sprint');controls.release('s');assert(!controls.read(0).sprint,'Releasing S must end its sprint');controls.press('w',1000);controls.press('w',1100);assert(!controls.read(0).sprint,'Key repeat must not count as double tap');controls.release('w');controls.press('w',1200);assert(controls.read(0).sprint,'Double-tap W must also sprint');controls.clear();assert(!controls.read(0).sprint&&controls.keys.size===0,'Blur must clear held movement and sprint');
controls.press(' ');assert(controls.read(0).jumpHeld&&controls.read(0).jumpHeld,'Holding Space must persist across rendered frames');controls.release(' ');assert(!controls.read(0).jumpHeld);
// Numerical targets are independent Minecraft-style outcomes, measured from
// distance and flight time rather than comparing constants to themselves.
root=scene();world=createWalkWorld(root);
const measurements={};
for(const [name,intent,target] of [['walk',input,4.317],['sprint',{...input,sprint:true},5.612],['crouch',{...input,crouch:true},1.295],['diagonal',{...input,right:1},4.317]]){
 body=new WalkCharacter(()=>world,new T.Vector3());run(body,1,intent);const at=body.feet;run(body,1,intent);const distance=body.feet.distanceTo(at);assert(Math.abs(distance-target)<.03,`${name}: expected ${target} metres in one second, got ${distance}`);measurements[name]=+distance.toFixed(3);
}
body=new WalkCharacter(()=>world,new T.Vector3());const floorY=body.feet.y;let apex=0,flight=0;
body.advance(1/120,{...input,forward:0,jump:true});
for(let i=1;i<120;i++){apex=Math.max(apex,body.feet.y-floorY);if(body.grounded){flight=i/120;break;}body.advance(1/120,{...input,forward:0});}
assert(apex>1.23&&apex<1.27,`Jump must reach about 1.25 m, got ${apex}`);assert(flight>=11/20&&flight<=12/20,`Jump must land during the twelfth game tick (~0.6 s), got ${flight}`);measurements.jumpHeight=+apex.toFixed(3);measurements.flight=flight;
const jumpRanges=[];
for(const sprint of [false,true]){body=new WalkCharacter(()=>world,new T.Vector3(0,0,8));run(body,1,{...input,sprint});const at=body.feet;body.advance(1/120,{...input,sprint,jump:true});for(let i=0;i<120&&!body.grounded;i++)body.advance(1/120,{...input,sprint});jumpRanges.push(at.z-body.feet.z);}
assert(jumpRanges[1]>jumpRanges[0]+1,'Sprinting into a jump must carry the character farther');measurements.jumpRanges=jumpRanges.map(n=>+n.toFixed(3));
body=new WalkCharacter(()=>world,new T.Vector3());let hops=0,wasGrounded=true;
for(let i=0;i<240;i++){body.advance(1/120,{...input,forward:0,jumpHeld:true});if(wasGrounded&&!body.grounded)hops++;wasGrounded=body.grounded;}assert(hops>=3,'Held Space must jump again after landing');
body=new WalkCharacter(()=>world,new T.Vector3());run(body,1);body.advance(1/120,{...input,jump:true});run(body,.1,{...input,forward:0,right:-1});assert(body.velocity.z<-.5&&body.velocity.x<0&&Math.abs(body.velocity.x)<2,'Air steering must preserve forward momentum instead of snapping to the new direction');
body=new WalkCharacter(()=>world,new T.Vector3());run(body,1);const stopAt=body.feet;run(body,.4,{...input,forward:0});assert(Math.hypot(body.velocity.x,body.velocity.z)<.1&&body.feet.distanceTo(stopAt)<.28,'Ground friction must stop the character within about a quarter block after release');
root=scene();block(root,0,0,-1,4,.5,2);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,2));run(body,.7);assert(body.feet.y>.49,'A half-metre slab must be stepped over');
root=new T.Group();block(root,0,0,0,8,1,4);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(0,0,1));run(body,4,{...input,crouch:true});assert(body.feet.z>-2&&body.grounded,'Sneaking must stop at an unsupported ledge');
root=scene();block(root,0,30,0,4,.2,4);world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3());run(body,1);run(body,3,{...input,forward:0});assert(body.feet.y<.03&&body.grounded,'A long fall must land on the ground rather than phase through it or reset above it');
// Rendering at 30/60/144 Hz must not change jump height or travelled distance.
for(const hz of [30,60,144]){
 root=scene();world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3());for(let i=0;i<hz*2;i++)body.advance(1/hz,input);assert(Math.abs(body.feet.z+8.374)<.04,`${hz} Hz must preserve the same movement distance`);
 body=new WalkCharacter(()=>world,new T.Vector3());const y=body.feet.y;let height=0;for(let i=0;i<hz;i++){body.advance(1/hz,{...input,forward:0,jump:i===0});height=Math.max(height,body.feet.y-y);}assert(height>1.23&&height<1.27,`${hz} Hz must preserve jump height and queued input`);
}
// Exercise the same irregular rock and instanced masonry used by the atlas,
// both on flat Map ground and after the DEM fit moves and tilts the geometry.
async function module(file,deps){const value={};new Function('exports','require',ts.transpileModule(await readFile(new URL(file,import.meta.url),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS}}).outputText)(value,name=>{assert(name in deps,`Missing dependency ${name}`);return deps[name];});return value;}
const siteSurfaces=JSON.parse((await import('node:fs')).readFileSync(new URL('../app/atlas-site-surfaces.json',import.meta.url),'utf8'));
const surfaces=await module('../app/atlas-site-materials.ts',{'three':T,'./atlas-site-surfaces.json':{__esModule:true,default:siteSurfaces,...siteSurfaces}});
const pilot=await module('../app/atlas-qumran-pilot.ts',{'three':T,'maplibre-gl':maplibre,'./atlas-site-materials':surfaces});
root=pilot.buildQumranPilot();
for(const sloped of [false,true]){
 if(sloped)pilot.fitQumranGround(root,(x,z)=>x*.12+z*.08);
 world=createWalkWorld(root);body=new WalkCharacter(()=>world,new T.Vector3(4,0,15.6));const start=body.feet;let blocked=0;
 for(let i=0;i<600;i++){body.advance(1/120,{...input,sprint:true});if(body.blocked)blocked++;assert(body.feet.y<start.y+2,'A source-model wall must not teleport the body onto the cliff crest');}
 assert(blocked>10,'The real Qumran architecture must stop sprinting');assert(body.feet.z>6&&body.feet.z<8,'The body must reach and remain outside the modeled tunnel masonry');
}
surfaces.disposeSiteScene(root);
console.log('Minecraft-style movement measurements:',JSON.stringify(measurements));
console.log('Character physics passed: speeds, jump arc/range, held jumps, air momentum, friction, half-metre steps, sneak ledges, long falls, frame rates, thin walls, ceilings, slopes, W/S gestures and real Qumran terrain/architecture.');
