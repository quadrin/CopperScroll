import * as T from 'three';
export type WalkPose={feet:[number,number,number];bearing:number;crouched:boolean;phase:number;moving:boolean;swings?:number};
// One blocky right arm in camera space, placed the way Minecraft Java Edition places the
// empty first-person hand: the same box (4 × 12 × 4 pixels on a shoulder pivot), the same
// sequence of fixed offsets and turns, a 70° view, entity-style face lighting, and the
// game's view-bob, swing and raise curves. Skin and sleeve are original pixel art; no
// game code or assets are used. The physical character remains a capsule; this view
// model never enters the site colliders.
const PX=1/16,SKIN=['#b58565','#a97a5b','#be9070','#9c6f51'],SLEEVE=['#2f9a9e','#288a8e','#38a6aa','#217578'];
function hash(i:number){let s=Math.imul(i+1,2654435761)>>>0;s^=s>>>15;s=Math.imul(s,2246822519)>>>0;return (s>>>8)%997/997;}
// A face of w × h pixels. Image row 0 is the hand end; the last `sleeveRows` rows are the sleeve.
function face(w:number,h:number,seed:number,sleeveRows:number){
 const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;const g=canvas.getContext('2d')!;
 for(let row=0;row<h;row++)for(let x=0;x<w;x++){
  const sleeve=row>=h-sleeveRows,palette=sleeve?SLEEVE:SKIN,r=hash(seed*131+row*17+x);
  // Mostly the base tone with sparse darker and lighter pixels; a darker hem where the sleeve starts.
  let tone=r<.66?0:r<.82?1:r<.94?2:3;if(sleeve&&row===h-sleeveRows)tone=r<.6?1:3;
  g.fillStyle=palette[tone];g.fillRect(x,row,1,1);
 }
 const texture=new T.CanvasTexture(canvas);texture.colorSpace=T.SRGBColorSpace;texture.magFilter=texture.minFilter=T.NearestFilter;texture.generateMipmaps=false;return texture;
}
const deg=T.MathUtils.degToRad;
// Entity face lighting: two fixed lights and 40 % ambient, one value per face.
const LIGHTS=[new T.Vector3(.2,1,-.7).normalize(),new T.Vector3(-.2,1,.7).normalize()];
export function createWalkAvatar(){
 const scene=new T.Scene(),camera=new T.PerspectiveCamera(70,1,.05,10);
 // Model space has y down, as in the game's entity models: the box runs from the shoulder
 // (y = -2) to the hand (y = 10) around a pivot 5 pixels right of the body's centre line.
 const geometry=new T.BoxGeometry(4*PX,12*PX,4*PX).translate(-1*PX,4*PX,0);
 // Box faces: +x, -x, +y (hand end), -y (shoulder end), +z, -z. Sides 4 × 12, ends 4 × 4.
 const textures=[face(4,12,1,4),face(4,12,2,4),face(4,4,3,0),face(4,4,4,4),face(4,12,5,4),face(4,12,6,4)];
 const materials=textures.map(map=>new T.MeshBasicMaterial({map,side:T.DoubleSide}));
 const mesh=new T.Mesh(geometry,materials);mesh.matrixAutoUpdate=false;scene.add(mesh);
 const normals=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]].map(([x,y,z])=>new T.Vector3(x,y,z)),n=new T.Vector3(),normalMatrix=new T.Matrix3();
 const m=new T.Matrix4(),step=new T.Matrix4(),apply=(op:T.Matrix4)=>m.multiply(op);
 const move=(x:number,y:number,z:number)=>apply(step.makeTranslation(x,y,z)),turnX=(a:number)=>apply(step.makeRotationX(a)),turnY=(a:number)=>apply(step.makeRotationY(a)),turnZ=(a:number)=>apply(step.makeRotationZ(a));
 mesh.visible=false;let phase=0,moving=false,swings=0,swingStart=-1,shownAt=0,bob=0,last=performance.now();
 const reduced=typeof window!=='undefined'&&window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
 return {
  update(pose:WalkPose|null){
   if(pose&&!mesh.visible)shownAt=performance.now();
   mesh.visible=!!pose;
   if(pose){phase=pose.phase;moving=pose.moving;if((pose.swings??0)>swings&&swings>=0)swingStart=performance.now();swings=pose.swings??0;}
  },
  render(renderer:T.WebGLRenderer,aspect:number){
   if(!mesh.visible)return;
   const now=performance.now(),dt=Math.min(.1,(now-last)/1000);last=now;
   if(camera.aspect!==aspect){camera.aspect=aspect;camera.updateProjectionMatrix();}
   // The bob eases toward 0.1 while walking, as the game's does.
   bob+=((moving?.1:0)-bob)*Math.min(1,dt*10);
   // Swing over 0.3 s (six game ticks); raise from 0.6 below over about 0.2 s on entry.
   const p=swingStart<0?0:Math.min(1,(now-swingStart)/300);if(p>=1)swingStart=-1;
   const lowered=reduced?0:Math.max(0,1-(now-shownAt)/200),root=Math.sqrt(p);
   m.identity();
   // A screen narrower than 16:10 would cut the arm off: draw it nearer the centre there.
   if(aspect<1.6)move((.347*aspect-.555)*1.4,0,0);
   // View bobbing, applied to the hand as in the game.
   move(Math.sin(phase)*bob*.5,-Math.abs(Math.cos(phase)*bob),0);turnZ(deg(Math.sin(phase)*bob*3));turnX(deg(Math.abs(Math.cos(phase-.2)*bob)*5));
   // The empty right hand: offsets, swing and fixed turns, in the game's order.
   move(-.3*Math.sin(root*Math.PI)+.64,.4*Math.sin(root*Math.PI*2)-.6-lowered*.6,-.4*Math.sin(p*Math.PI)-.72);
   turnY(deg(45));turnY(deg(Math.sin(root*Math.PI)*70));turnZ(deg(Math.sin(p*p*Math.PI)*-20));
   move(-1,3.6,3.5);turnZ(deg(120));turnX(deg(200));turnY(deg(-135));move(5.6,0,0);
   // The arm part: shoulder pivot, then its slight outward tilt.
   move(-5*PX,2*PX,0);turnZ(.1);
   mesh.matrix.copy(m);mesh.matrixWorldNeedsUpdate=true;
   normalMatrix.getNormalMatrix(m);
   normals.forEach((normal,i)=>{n.copy(normal).applyMatrix3(normalMatrix).normalize();
    materials[i].color.setScalar(Math.min(1,.4+.6*(Math.max(0,n.dot(LIGHTS[0]))+Math.max(0,n.dot(LIGHTS[1])))));});
   renderer.clearDepth();renderer.render(scene,camera);
  },
  dispose(){geometry.dispose();materials.forEach(material=>material.dispose());textures.forEach(texture=>texture.dispose());}
 };
}
