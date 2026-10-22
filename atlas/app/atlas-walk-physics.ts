import * as T from 'three';
import {Octree} from 'three/addons/math/Octree.js';
import {Capsule} from 'three/addons/math/Capsule.js';

export const WALK_BODY={radius:.30,height:1.8,eye:1.62,crouchHeight:1.5,crouchEye:1.27,step:.6,slope:Math.cos(50*Math.PI/180),speed:4.317,sprintSpeed:5.612};
// Minecraft Java-style ground motion: 20 Hz impulses/drag, with collision and
// camera positions advanced at 120 Hz so movement stays smooth on the map.
// Coefficient reference: PrismarineJS/prismarine-physics (normal movement).
const GAME_TICK=1/20,SUBSTEP=1/120,GROUND_DRAG=.6*.91,AIR_DRAG=.91,VERTICAL_DRAG=.98;
export type WalkIntent={forward:number;right:number;bearing:number;sprint:boolean;crouch:boolean;jump:boolean;jumpHeld?:boolean;fly?:boolean;descend?:boolean};
// Creative-mode flight, as Minecraft Java: abilities.flySpeed 0.05 blocks/tick (doubled when
// sprinting), air drag 0.91; Space/Shift add ±3 × flySpeed per tick and vertical speed keeps 0.6
// of itself each tick, so climbing and descending settle at 7.5 m/s. One block is one metre here.
const FLY_SPEED=.05,FLY_CEILING=400;
const UP=new T.Vector3(0,1,0),DOWN=new T.Vector3(0,-1,0),SKIN=.004;
type Contact={normal:T.Vector3;depth:number};
export type WalkWorld={tree:Octree;triangles:number;floor:(x:number,z:number,top:number,bottom:number)=>{height:number;normal:T.Vector3}|null;resolve:(body:Capsule,steep?:boolean)=>Contact[];clear:(body:Capsule)=>boolean};

// Use the displayed terrain/architecture. Repeated chipped blocks get oriented
// box colliders; their bevels and small pebbles do not need thousands of extra faces.
export function createWalkWorld(root:T.Object3D):WalkWorld {
 const tree=new Octree(),a=new T.Vector3(),b=new T.Vector3(),c=new T.Vector3(),matrix=new T.Matrix4();let triangles=0;
 const add=(p:T.BufferAttribute|T.InterleavedBufferAttribute,i:number,j:number,k:number,m:T.Matrix4)=>{
  a.fromBufferAttribute(p,i).applyMatrix4(m);b.fromBufferAttribute(p,j).applyMatrix4(m);c.fromBufferAttribute(p,k).applyMatrix4(m);
  if(new T.Vector3().subVectors(b,a).cross(new T.Vector3().subVectors(c,a)).lengthSq()<1e-12)return;
  tree.addTriangle(new T.Triangle(a.clone(),b.clone(),c.clone()));triangles++;
 };
 const cube=new T.BoxGeometry(1,1,1),cubeP=cube.getAttribute('position'),cubeI=cube.getIndex()!,local=new T.Matrix4(),boxMatrix=new T.Matrix4(),size=new T.Vector3(),centre=new T.Vector3();
 root.updateWorldMatrix(true,true);
 root.traverseVisible(object=>{
  if(!(object instanceof T.Mesh)||object.userData.walkCollision===false)return;
  const geometry=object.geometry,p=geometry.getAttribute('position'),index=geometry.getIndex(),colour=geometry.getAttribute('color');
  if(object instanceof T.InstancedMesh){
   geometry.computeBoundingBox();geometry.boundingBox!.getSize(size);geometry.boundingBox!.getCenter(centre);
   const shape=new T.Matrix4().makeTranslation(centre.x,centre.y,centre.z).scale(size);
   for(let i=0;i<object.count;i++){
    object.getMatrixAt(i,local);matrix.multiplyMatrices(object.matrixWorld,local);
    const height=new T.Vector3(matrix.elements[4],matrix.elements[5],matrix.elements[6]).length()*size.y;
    if((object.userData.walkDetail&&height<.12)||Math.abs(matrix.determinant())<1e-10)continue;
    boxMatrix.multiplyMatrices(matrix,shape);
    for(let j=0;j<cubeI.count;j+=3)add(cubeP,cubeI.getX(j),cubeI.getX(j+1),cubeI.getX(j+2),boxMatrix);
   }
  }else for(let i=0;i<(index?.count??p.count);i+=3){
   const ia=index?index.getX(i):i,ib=index?index.getX(i+1):i+1,ic=index?index.getX(i+2):i+2;
   if(colour?.itemSize===4&&Math.max(colour.getW(ia),colour.getW(ib),colour.getW(ic))<.03)continue;
   add(p,ia,ib,ic,object.matrixWorld);
   const materials=Array.isArray(object.material)?object.material:[object.material];
   if(!object.userData.walkSurface||materials.some(m=>m.side===T.DoubleSide))add(p,ic,ib,ia,object.matrixWorld);
  }
 });cube.dispose();tree.build();
 const world:WalkWorld={tree,triangles,
  floor(x,z,top,bottom){const hit=tree.rayIntersect(new T.Ray(new T.Vector3(x,top,z),DOWN));if(!hit||hit.position.y<bottom)return null;const normal=hit.triangle.getNormal(new T.Vector3());return normal.y>=WALK_BODY.slope?{height:hit.position.y,normal}:null;},
  clear(body){const hit=tree.capsuleIntersect(body);return !hit||hit.depth<SKIN*2;},
  resolve(body,steep=false){
   const contacts:Contact[]=[];
   for(let pass=0;pass<4;pass++){
    const candidates:T.Triangle[]=[];tree.getCapsuleTriangles(body,candidates);let moved=false;
    for(const triangle of candidates){const hit=tree.triangleCapsuleIntersect(body,triangle);if(!hit||hit.depth<1e-6)continue;
     const normal=hit.normal.clone();contacts.push({normal,depth:hit.depth});
     if(steep&&normal.y>0&&normal.y<WALK_BODY.slope){const horizontal=normal.clone().setY(0),length=horizontal.length();if(length>.01)body.translate(horizontal.multiplyScalar((hit.depth+SKIN)/(length*length)));}
     else body.translate(normal.clone().multiplyScalar(hit.depth+SKIN));moved=true;
    }if(!moved)break;
   }return contacts;
  }
 };return world;
}

// MapLibre's near plane is height/50 pixels, about half a metre at eye level. It would
// cut away a wall or overhang beside the walker; a block build, which has faces only on
// its outside, would then look hollow (Minecraft's "x-ray"). The site scene clears and
// uses its own depth, so it can draw with a nearer plane without changing the map.
export function pullNearPlane(projection:T.Matrix4,factor:number){
 const e=projection.elements,z=[e[2],e[6],e[10],e[14]],w=[e[3],e[7],e[11],e[15]];
 // With a standard perspective, row z = -A·(row w) + B·(0,0,0,1); recover A and B.
 const k=[0,1,2].reduce((a,b)=>Math.abs(w[b])>Math.abs(w[a])?b:a,0);if(Math.abs(w[k])<1e-12)return;
 const A=-z[k]/w[k],B=z[3]+A*w[3],near=B/(A-1),far=B/(A+1);if(!(near>0&&far>near))return;
 const n=near/factor,A2=-(far+n)/(far-n),B2=-2*far*n/(far-n);
 for(let c=0;c<4;c++)e[c*4+2]=-A2*w[c]+(c===3?B2:0);
}

export class WalkCharacter {
 readonly capsule=new Capsule();readonly velocity=new T.Vector3();grounded=false;blocked=false;crouched=false;sprinting=false;flying=false;
 private safe=new T.Vector3();private accumulator=0;private jumpBuffer=0;private jumpCooldown=0;private substep=0;private horizontalDrag=GROUND_DRAG;
 constructor(private world:()=>WalkWorld,start:T.Vector3){this.spawn(start);}
 get feet(){return this.capsule.start.clone().addScaledVector(UP,-WALK_BODY.radius);}
 get eye(){return this.feet.addScaledVector(UP,this.crouched?WALK_BODY.crouchEye:WALK_BODY.eye);}
 private shape(feet:T.Vector3,crouch=this.crouched){return new Capsule(feet.clone().addScaledVector(UP,WALK_BODY.radius),feet.clone().addScaledVector(UP,(crouch?WALK_BODY.crouchHeight:WALK_BODY.height)-WALK_BODY.radius),WALK_BODY.radius);}
 spawn(at:T.Vector3){
  const world=this.world();
  for(let ring=0;ring<=16;ring++)for(let i=0;i<(ring?16:1);i++){
   const x=at.x+Math.cos(i*Math.PI/8)*ring*.4,z=at.z+Math.sin(i*Math.PI/8)*ring*.4,floor=world.floor(x,z,1000,-1000);if(!floor)continue;
   const foot=new T.Vector3(x,floor.height+SKIN,z),body=this.shape(foot,false);world.resolve(body);
   if(body.start.distanceTo(foot.clone().addScaledVector(UP,WALK_BODY.radius))>.15||!world.clear(body))continue;
   this.capsule.copy(body);this.velocity.set(0,0,0);this.grounded=true;this.crouched=false;this.sprinting=false;this.blocked=false;this.flying=false;this.jumpBuffer=0;this.jumpCooldown=0;this.substep=0;this.horizontalDrag=GROUND_DRAG;this.safe.copy(this.feet);return;
  }throw Error('There is no clear standing space here. Drop the person on open ground.');
 }
 advance(elapsed:number,input:WalkIntent){
  // A double tap of Space starts or ends flight; it never queues a jump of its own.
  if(input.fly){this.flying=!this.flying;this.jumpBuffer=0;if(this.flying){this.grounded=false;this.velocity.y=Math.max(this.velocity.y,0);}}
  this.accumulator+=Math.min(elapsed,.1);if(input.jump&&!input.fly)this.jumpBuffer=.1;
  while(this.accumulator>=SUBSTEP){this.step(SUBSTEP,input);this.accumulator-=SUBSTEP;}
 }
 private step(dt:number,input:WalkIntent){
  // While flying, Shift descends instead of crouching.
  const world=this.world(),old=this.feet,crouch=input.crouch&&!this.flying,height=crouch?WALK_BODY.crouchHeight:WALK_BODY.height;
  if(crouch||!this.crouched||world.clear(this.shape(old,false))){this.crouched=crouch;this.capsule.end.y=this.capsule.start.y+height-2*WALK_BODY.radius;}
  const direction=new T.Vector3(Math.sin(input.bearing)*input.forward+Math.cos(input.bearing)*input.right,0,-Math.cos(input.bearing)*input.forward+Math.sin(input.bearing)*input.right);if(direction.lengthSq()>1)direction.normalize();
  this.sprinting=input.sprint&&!this.crouched&&direction.lengthSq()>0;
  if(this.substep===0){
   this.velocity.x*=this.horizontalDrag;this.velocity.z*=this.horizontalDrag;
   for(const axis of ['x','z'] as const)if(Math.abs(this.velocity[axis])<.06)this.velocity[axis]=0;
   this.horizontalDrag=this.grounded&&!this.flying?GROUND_DRAG:AIR_DRAG;
   const acceleration=this.flying?FLY_SPEED*.98/GAME_TICK*(this.sprinting?2:1):(this.grounded?.1:.02)*.98/GAME_TICK*(this.sprinting?1.3:1)*(this.crouched?.3:1);
   this.velocity.addScaledVector(direction,acceleration);
   if(this.flying){const lift=Number(!!input.jumpHeld||this.jumpBuffer>0)-Number(input.descend??input.crouch);this.velocity.y+=lift*FLY_SPEED*3/GAME_TICK;this.jumpBuffer=0;}
   const wantsJump=this.jumpBuffer>0||input.jumpHeld;
   if(!wantsJump)this.jumpCooldown=0;else this.jumpCooldown=Math.max(0,this.jumpCooldown-GAME_TICK);
   if(wantsJump&&this.grounded&&!this.flying&&this.jumpCooldown<=1e-6){this.velocity.y=.42/GAME_TICK;if(this.sprinting)this.velocity.addScaledVector(direction.clone().normalize(),.2/GAME_TICK);this.grounded=false;this.jumpBuffer=0;this.jumpCooldown=.5;}
  }
  this.jumpBuffer=Math.max(0,this.jumpBuffer-dt);
  const horizontal=new T.Vector3(this.velocity.x*dt,0,this.velocity.z*dt),before=this.capsule.clone();
  if(this.grounded&&this.crouched){
   const support=(x:number,z:number)=>!!world.floor(x,z,old.y+.05,old.y-WALK_BODY.step);
   if(!support(old.x+horizontal.x,old.z+horizontal.z)){
    const xSafe=support(old.x+horizontal.x,old.z),zSafe=support(old.x,old.z+horizontal.z);
    if(!xSafe||zSafe){horizontal.x=0;this.velocity.x=0;}
    if(!zSafe||xSafe){horizontal.z=0;this.velocity.z=0;}
   }
  }
  // Probe just ahead of the feet for small steps. A tall wall cannot be selected
  // because this ray starts only one step above the current floor, not overhead.
  if(this.grounded&&horizontal.lengthSq()>1e-10){
   const ahead=old.clone().add(horizontal).addScaledVector(direction.clone().normalize(),WALK_BODY.radius+.025),floor=world.floor(ahead.x,ahead.z,old.y+WALK_BODY.step,old.y-.08);
   if(floor&&floor.normal.y>.98&&floor.height>old.y+.01){const raised=this.shape(new T.Vector3(old.x+horizontal.x,floor.height+SKIN,old.z+horizontal.z));const contacts=world.resolve(raised,true);if(!contacts.some(c=>c.normal.y<-.5)&&raised.start.y-before.start.y<=WALK_BODY.step+.02&&Math.hypot(raised.start.x-before.start.x,raised.start.z-before.start.z)>.3*horizontal.length())this.capsule.copy(raised);else this.capsule.translate(horizontal);}
   else this.capsule.translate(horizontal);
  }else this.capsule.translate(horizontal);
  const wallContacts=world.resolve(this.capsule,true);
  this.blocked=wallContacts.some(c=>Math.abs(c.normal.y)<WALK_BODY.slope&&horizontal.dot(c.normal)<-1e-7);
  for(const {normal} of wallContacts)if(Math.abs(normal.y)<WALK_BODY.slope){const n=normal.clone().setY(0).normalize(),inward=this.velocity.dot(n);if(inward<0)this.velocity.addScaledVector(n,-inward);}
  this.capsule.translate(new T.Vector3(0,this.velocity.y*dt,0));
  const falling=this.velocity.y<0,contacts=world.resolve(this.capsule);this.grounded=contacts.some(c=>c.normal.y>=WALK_BODY.slope&&this.velocity.y<=0)&&(!this.flying||falling);
  // As in Minecraft, flying down onto the ground ends the flight.
  if(this.flying&&this.grounded)this.flying=false;
  for(const {normal} of contacts){
   // A supporting slope absorbs gravity without turning it into downhill
   // horizontal velocity. Air/ceiling/wall contacts still clip their normal.
   if(normal.y>=WALK_BODY.slope&&this.velocity.y<=0){this.velocity.y=0;continue;}
   const inward=this.velocity.dot(normal);if(inward<0)this.velocity.addScaledVector(normal,-inward);
  }
  const foot=this.feet,floor=world.floor(foot.x,foot.z,foot.y+.025,foot.y-.10);
  if(!this.flying&&this.velocity.y<=.1&&floor&&foot.y-floor.height<=.08){this.capsule.translate(new T.Vector3(0,floor.height+SKIN-foot.y,0));world.resolve(this.capsule);this.velocity.y=0;this.grounded=true;}
  if(this.grounded)this.safe.copy(this.feet);
  this.substep=(this.substep+1)%6;
  if(this.substep===0)this.velocity.y=this.flying?this.velocity.y*.6:(this.velocity.y-.08/GAME_TICK)*VERTICAL_DRAG;
  // Flight has a ceiling well above the site so that the map camera stays meaningful.
  const ceiling=(world.tree.box?.max.y??0)+FLY_CEILING;if(this.flying&&this.feet.y>ceiling){this.capsule.translate(new T.Vector3(0,ceiling-this.feet.y,0));this.velocity.y=Math.min(0,this.velocity.y);}
  if(this.feet.y<(world.tree.box?.min.y??-1000)-8||this.feet.y<-1000)this.spawn(this.safe);
 }
}

export class WalkInput {
 readonly keys=new Set<string>();private taps=new Map<string,number>();private sprintKey='';private sprintToggle=false;private crouchToggle=false;jump=false;fly=false;
 press(key:string,now=performance.now()){
  if(this.keys.has(key))return;
  if(key==='w'||key==='s'){if(now-(this.taps.get(key)??-Infinity)<300)this.sprintKey=key;this.taps.set(key,now);}
  // Two presses of Space within 7 game ticks (0.35 s) toggle flight, as in Minecraft.
  if(key===' '){this.jump=true;if(now-(this.taps.get(key)??-Infinity)<350){this.fly=true;this.taps.delete(key);}else this.taps.set(key,now);}
  this.keys.add(key);
 }
 release(key:string){this.keys.delete(key);if(key===this.sprintKey)this.sprintKey='';}
 get sprintEnabled(){return this.sprintToggle;}
 toggleSprint(){this.sprintToggle=!this.sprintToggle;}toggleCrouch(){this.crouchToggle=!this.crouchToggle;}toggleFly(){this.fly=true;}
 clear(){this.keys.clear();this.taps.clear();this.sprintKey='';this.sprintToggle=false;this.crouchToggle=false;this.jump=false;this.fly=false;}
 read(bearing:number){const down=(...keys:string[])=>keys.some(k=>this.keys.has(k));const value={forward:Number(down('w','arrowup'))-Number(down('s','arrowdown')),right:Number(down('d','arrowright'))-Number(down('a','arrowleft')),bearing,sprint:!!this.sprintKey||this.sprintToggle||down('control'),crouch:this.crouchToggle||down('shift'),jump:this.jump,jumpHeld:down(' '),fly:this.fly,descend:down('shift')};this.jump=false;this.fly=false;return value;}
}
