import * as T from 'three';
import {Octree} from 'three/addons/math/Octree.js';
import {Capsule} from 'three/addons/math/Capsule.js';

export const WALK_BODY={radius:.28,height:1.8,eye:1.65,crouchHeight:1.2,crouchEye:1.05,step:.35,slope:Math.cos(50*Math.PI/180),speed:3.4,sprintSpeed:5.6};
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

export class WalkCharacter {
 readonly capsule=new Capsule();readonly velocity=new T.Vector3();grounded=false;blocked=false;crouched=false;sprinting=false;
 private safe=new T.Vector3();private accumulator=0;private jumpQueued=false;
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
   this.capsule.copy(body);this.velocity.set(0,0,0);this.grounded=true;this.crouched=false;this.safe.copy(this.feet);return;
  }throw Error('There is no clear standing space here. Drop the person on open ground.');
 }
 advance(elapsed:number,input:{forward:number;right:number;bearing:number;sprint:boolean;crouch:boolean;jump:boolean}){
  this.accumulator+=Math.min(elapsed,.1);this.jumpQueued||=input.jump;
  while(this.accumulator>=1/120){this.step(1/120,{...input,jump:this.jumpQueued});this.jumpQueued=false;this.accumulator-=1/120;}
 }
 private step(dt:number,input:{forward:number;right:number;bearing:number;sprint:boolean;crouch:boolean;jump:boolean}){
  const world=this.world(),old=this.feet,height=input.crouch?WALK_BODY.crouchHeight:WALK_BODY.height;
  if(input.crouch||!this.crouched||world.clear(this.shape(old,false))){this.crouched=input.crouch;this.capsule.end.y=this.capsule.start.y+height-2*WALK_BODY.radius;}
  const direction=new T.Vector3(Math.sin(input.bearing)*input.forward+Math.cos(input.bearing)*input.right,0,-Math.cos(input.bearing)*input.forward+Math.sin(input.bearing)*input.right);if(direction.lengthSq()>1)direction.normalize();
  this.sprinting=input.sprint&&!this.crouched&&direction.lengthSq()>0;
  const speed=this.crouched?1.5:this.sprinting?WALK_BODY.sprintSpeed:WALK_BODY.speed,acceleration=(this.grounded?32:9)*dt;
  for(const axis of ['x','z'] as const)this.velocity[axis]+=T.MathUtils.clamp(direction[axis]*speed-this.velocity[axis],-acceleration,acceleration);
  if(input.jump&&this.grounded){this.velocity.y=6.2;this.grounded=false;}
  const horizontal=new T.Vector3(this.velocity.x*dt,0,this.velocity.z*dt),before=this.capsule.clone();
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
  this.velocity.y=Math.max(-25,this.velocity.y-20*dt);this.capsule.translate(new T.Vector3(0,this.velocity.y*dt,0));
  const contacts=world.resolve(this.capsule);this.grounded=contacts.some(c=>c.normal.y>=WALK_BODY.slope&&this.velocity.y<=0);
  for(const {normal} of contacts){const inward=this.velocity.dot(normal);if(inward<0)this.velocity.addScaledVector(normal,-inward);}
  const foot=this.feet,floor=world.floor(foot.x,foot.z,foot.y+.025,foot.y-.10);
  if(this.velocity.y<=.1&&floor&&foot.y-floor.height<=.08){this.capsule.translate(new T.Vector3(0,floor.height+SKIN-foot.y,0));world.resolve(this.capsule);this.velocity.y=0;this.grounded=true;}
  if(this.grounded)this.safe.copy(this.feet);
  if(this.feet.y<this.safe.y-25||this.feet.y<-1000)this.spawn(this.safe);
 }
}

export class WalkInput {
 readonly keys=new Set<string>();private taps=new Map<string,number>();private sprintKey='';private sprintToggle=false;private crouchToggle=false;jump=false;
 press(key:string,now=performance.now()){
  if(this.keys.has(key))return;
  if(key==='w'||key==='s'){if(now-(this.taps.get(key)??-Infinity)<300)this.sprintKey=key;this.taps.set(key,now);}
  if(key===' ')this.jump=true;this.keys.add(key);
 }
 release(key:string){this.keys.delete(key);if(key===this.sprintKey)this.sprintKey='';}
 get sprintEnabled(){return this.sprintToggle;}
 toggleSprint(){this.sprintToggle=!this.sprintToggle;}toggleCrouch(){this.crouchToggle=!this.crouchToggle;}
 clear(){this.keys.clear();this.taps.clear();this.sprintKey='';this.sprintToggle=false;this.crouchToggle=false;this.jump=false;}
 read(bearing:number){const down=(...keys:string[])=>keys.some(k=>this.keys.has(k));const value={forward:Number(down('w','arrowup'))-Number(down('s','arrowdown')),right:Number(down('d','arrowright'))-Number(down('a','arrowleft')),bearing,sprint:!!this.sprintKey||this.sprintToggle||down('control'),crouch:this.crouchToggle||down('shift'),jump:this.jump};this.jump=false;return value;}
}
