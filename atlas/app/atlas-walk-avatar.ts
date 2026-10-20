import * as T from 'three';
export type WalkPose={feet:[number,number,number];bearing:number;crouched:boolean;phase:number;moving:boolean;swings?:number};
// One original blocky right arm in the Minecraft manner, rendered in camera space:
// a 4 × 12 × 4 pixel box with original pixel-art skin and sleeve, unlit faces at
// fixed brightness steps, a walking bob, a swing on click and a short raise on entry.
// The physical character remains a capsule; this view model never enters the site colliders.
const PX=.0625,SKIN=['#c08e66','#b5845d','#ca9a72','#a97a55'],SLEEVE=['#3c8a92','#347a82','#4598a0','#2c6970'];
// Brightness of a face by the direction it faces on screen, as in Minecraft's block shading.
const SHADE={up:1,down:.5,front:.8,side:.6};
function hash(i:number){let s=Math.imul(i+1,2654435761)>>>0;s^=s>>>15;s=Math.imul(s,2246822519)>>>0;return (s>>>8)%997/997;}
// One face as a w × h pixel canvas; rows from the hand end (y = 0) to the shoulder (y = h - 1).
function face(w:number,h:number,seed:number,sleeveRows:number){
 const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;const g=canvas.getContext('2d')!;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const sleeve=y>=h-sleeveRows,palette=sleeve?SLEEVE:SKIN,r=hash(seed*131+y*17+x);
  // Mostly the base tone, with sparse darker and lighter pixels; a darker hem row at the sleeve edge.
  let tone=r<.62?0:r<.8?1:r<.93?2:3;if(sleeve&&y===h-sleeveRows)tone=r<.5?1:3;if(!sleeve&&y===0)tone=r<.5?1:0;
  g.fillStyle=palette[tone];g.fillRect(x,h-1-y,1,1);
 }
 const texture=new T.CanvasTexture(canvas);texture.colorSpace=T.SRGBColorSpace;texture.magFilter=texture.minFilter=T.NearestFilter;texture.generateMipmaps=false;return texture;
}
export function createWalkAvatar(){
 const scene=new T.Scene(),camera=new T.PerspectiveCamera(70,1,.01,10),root=new T.Group(),arm=new T.Group();root.add(arm);
 // Box faces: +x, -x, +y (shoulder end), -y (hand end), +z, -z. Sides are 4 × 12 pixels, ends 4 × 4.
 const textures=[face(4,12,1,4),face(4,12,2,4),face(4,4,3,4),face(4,4,4,0),face(4,12,5,4),face(4,12,6,4)];
 const materials=textures.map(map=>new T.MeshBasicMaterial({map}));
 const geometry=new T.BoxGeometry(4*PX,12*PX,4*PX),mesh=new T.Mesh(geometry,materials);
 // The arm hangs from its shoulder end, so rotations swing it like a limb.
 mesh.position.y=-6*PX;arm.add(mesh);scene.add(root);
 const normals=[new T.Vector3(1,0,0),new T.Vector3(-1,0,0),new T.Vector3(0,1,0),new T.Vector3(0,-1,0),new T.Vector3(0,0,1),new T.Vector3(0,0,-1)],n=new T.Vector3(),q=new T.Quaternion();
 root.visible=false;let phase=0,moving=false,crouched=false,swings=0,swingStart=-1,shownAt=0,bobWeight=0,last=performance.now();
 const reduced=typeof window!=='undefined'&&window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
 return {
  update(pose:WalkPose|null){
   if(pose&&!root.visible)shownAt=performance.now();
   root.visible=!!pose;
   if(pose){phase=pose.phase;moving=pose.moving;crouched=pose.crouched;if((pose.swings??0)>swings&&swings>=0)swingStart=performance.now();swings=pose.swings??0;}
  },
  render(renderer:T.WebGLRenderer,aspect:number){
   if(!root.visible)return;
   const now=performance.now(),dt=Math.min(.1,(now-last)/1000);last=now;
   if(camera.aspect!==aspect){camera.aspect=aspect;camera.updateProjectionMatrix();}
   const phone=aspect<1;bobWeight+=((moving?1:0)-bobWeight)*Math.min(1,dt*8);
   // Walking bob: a sideways sway with a double-rate dip, like the game's view bobbing.
   const bx=Math.sin(phase)*.035*bobWeight,by=-Math.abs(Math.cos(phase))*.045*bobWeight;
   // Swing: about 0.3 s, forward and toward the centre, then back.
   const p=swingStart<0?1:Math.min(1,(now-swingStart)/300),s1=Math.sin(Math.sqrt(p)*Math.PI),s2=Math.sin(p*p*Math.PI);if(p>=1)swingStart=-1;
   // Raise from below the screen when the walk view opens.
   const equip=reduced?1:Math.min(1,(now-shownAt)/220),rise=(1-equip)*(1-equip)*.55;
   // The shoulder sits just off the bottom-right corner, measured in the visible half-width at its depth.
   const depth=.55,halfHeight=depth*Math.tan(T.MathUtils.degToRad(camera.fov/2)),halfWidth=halfHeight*aspect;
   root.scale.setScalar(phone?.62:1);
   root.position.set(halfWidth*(phone?1.3:1)+bx-s1*.16,-halfHeight*1.6+by-rise-(crouched?.03:0)+Math.sin(Math.sqrt(p)*Math.PI*2)*.06,-depth-s2*.12);
   // Pitch forward, yaw toward the centre, and roll about the arm's length to show its top and inner faces.
   arm.rotation.set(2.05-s2*.7,.45+s1*.4,bx*.6-s2*.2,'YXZ');mesh.rotation.y=-.95;
   // Flat Minecraft shading: each face takes the step for the way it faces on screen.
   arm.updateMatrixWorld(true);mesh.getWorldQuaternion(q);
   normals.forEach((normal,i)=>{n.copy(normal).applyQuaternion(q);const ax=Math.abs(n.x),ay=Math.abs(n.y),az=Math.abs(n.z);
    const shade=ay>=ax&&ay>=az?(n.y>0?SHADE.up:SHADE.down):az>=ax?SHADE.front:SHADE.side;materials[i].color.setScalar(shade);});
   renderer.clearDepth();renderer.render(scene,camera);
  },
  dispose(){geometry.dispose();materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());}
 };
}
