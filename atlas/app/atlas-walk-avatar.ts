import * as T from 'three';
export type WalkPose={feet:[number,number,number];bearing:number;crouched:boolean;phase:number;moving:boolean};
// An original block-shaped first-person body, with linen sleeves and boots.
// It is separate from the archaeological scene and never enters its colliders.
export function createWalkAvatar(){
 const root=new T.Group(),geometry=new T.BoxGeometry(1,1,1),linen=new T.MeshStandardMaterial({color:'#c8c1a5',roughness:1}),cloth=new T.MeshStandardMaterial({color:'#45594c',roughness:1}),skin=new T.MeshStandardMaterial({color:'#aa7955',roughness:1}),leather=new T.MeshStandardMaterial({color:'#4d3d2b',roughness:1});
 function part(parent:T.Group,m:T.Material,x:number,y:number,z:number,w:number,h:number,d:number){const mesh=new T.Mesh(geometry,m);mesh.position.set(x,y,z);mesh.scale.set(w,h,d);mesh.receiveShadow=true;parent.add(mesh);return mesh;}
 part(root,cloth,0,1.05,0,.40,.58,.23);
 const legs=[-1,1].map(side=>{const g=new T.Group();g.position.set(side*.11,.76,0);root.add(g);part(g,cloth,0,-.34,0,.17,.66,.19);part(g,leather,0,-.70,-.045,.19,.12,.29);return g;});
 const arms=[-1,1].map(side=>{const g=new T.Group();g.position.set(side*.23,1.4,-.08);root.add(g);part(g,linen,side*.025,-.08,-.18,.14,.19,.38);part(g,linen,0,-.10,-.46,.13,.15,.27);part(g,skin,0,-.10,-.66,.14,.14,.17);return g;});
 root.visible=false;
 return {root,update(pose:WalkPose|null){root.visible=!!pose;if(!pose)return;root.position.set(...pose.feet);root.rotation.y=-pose.bearing;root.scale.y=pose.crouched?.67:1;const swing=pose.moving?Math.sin(pose.phase)*.35:0;legs[0].rotation.x=swing;legs[1].rotation.x=-swing;arms[0].rotation.x=swing*.15;arms[1].rotation.x=-swing*.15;}};
}
