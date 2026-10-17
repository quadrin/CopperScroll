import * as T from 'three';
export type WalkPose={feet:[number,number,number];bearing:number;crouched:boolean;phase:number;moving:boolean};
// One original blocky right forearm, rendered in camera space. The physical
// character remains a capsule; this view model never enters the site colliders.
export function createWalkAvatar(){
 const scene=new T.Scene(),camera=new T.PerspectiveCamera(50,1,.01,10),root=new T.Group(),geometry=new T.BoxGeometry(1,1,1);
 const pixels=new Uint8Array(16*16*4);let seed=73;
 for(let i=0;i<256;i++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;const shade=((seed>>>24)%7-3)*.8;pixels.set([176+shade,124+shade,87+shade,255],i*4);}
 const texture=new T.DataTexture(pixels,16,16);texture.colorSpace=T.SRGBColorSpace;texture.magFilter=texture.minFilter=T.NearestFilter;texture.needsUpdate=true;
 const skin=new T.MeshLambertMaterial({map:texture}),sleeve=new T.MeshLambertMaterial({color:'#45594c'});
 function part(material:T.Material,y:number,height:number){const mesh=new T.Mesh(geometry,material);mesh.position.y=y;mesh.scale.set(.23,height,.23);root.add(mesh);}
 part(sleeve,-.24,1);part(skin,.50,.48);
 scene.add(root,new T.HemisphereLight('#fff3de','#6c665b',2));const light=new T.DirectionalLight('#ffffff',2);light.position.set(-2,3,4);scene.add(light);
 root.visible=false;let phase=0,moving=false,crouched=false;
 return {
  update(pose:WalkPose|null){root.visible=!!pose;if(pose){phase=pose.phase;moving=pose.moving;crouched=pose.crouched;}},
  render(renderer:T.WebGLRenderer,aspect:number){
   if(!root.visible)return;
   if(camera.aspect!==aspect){camera.aspect=aspect;camera.updateProjectionMatrix();}
   const halfHeight=2.5*Math.tan(T.MathUtils.degToRad(camera.fov/2)),phone=aspect<1,bob=moving?Math.sin(phase)*.014:0;
   root.scale.setScalar(phone?Math.max(.65,aspect):1);
   root.position.set(halfHeight*aspect*.96,halfHeight*(phone?-.70:-1.12)+bob-(crouched?.015:0),-2.5);
   root.rotation.set(-.25,-.30,.30+(moving?Math.cos(phase)*.012:0));
   renderer.clearDepth();renderer.render(scene,camera);
  },
  dispose(){geometry.dispose();skin.dispose();sleeve.dispose();texture.dispose();}
 };
}
