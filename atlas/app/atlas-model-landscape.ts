import * as T from "three";
import patches from "./atlas-model-terrain.json";
import { cloneSiteMaterial, chippedBlock } from './atlas-site-materials';
type Point=[number,number];
export type LandscapePad={x:number;z:number;w:number;d:number;height:number;feather:number};
export type LandscapeGround={w:number;d:number;holes:Point[][];pads:LandscapePad[]};
type Patch={lat:number;lon:number;anchorPrecision:string;extent:number;size:number;elevations:number[];centreElevation:number};
export type TerrainPatch=Patch;
const terrain=patches as Record<string,Patch>;
const smooth=(t:number)=>{const v=T.MathUtils.clamp(t,0,1);return v*v*(3-2*v)};
function inside(x:number,z:number,points:Point[]){let hit=false;for(let i=0,j=points.length-1;i<points.length;j=i++){const [a,b]=points[i],[c,d]=points[j];if((b>z)!==(d>z)&&x<(c-a)*(z-b)/(d-b)+a)hit=!hit;}return hit;}
export function elevationAt(patch:Patch,x:number,z:number){
 const u=T.MathUtils.clamp((x/patch.extent+.5)*(patch.size-1),0,patch.size-1),v=T.MathUtils.clamp((z/patch.extent+.5)*(patch.size-1),0,patch.size-1),i=Math.floor(u),j=Math.floor(v),a=u-i,b=v-j;
 const value=(x:number,y:number)=>patch.elevations[Math.min(y,patch.size-1)*patch.size+Math.min(x,patch.size-1)];
 return T.MathUtils.lerp(T.MathUtils.lerp(value(i,j),value(i+1,j),a),T.MathUtils.lerp(value(i,j+1),value(i+1,j+1),a),b)-patch.centreElevation;
}
// A wider terrain patch, when one is loaded for the place, replaces the 800 m default.
export function landscapeGround(ground:LandscapeGround,placeId:string,offset:Point,surface?:T.MeshStandardMaterial,stone?:T.MeshStandardMaterial,wide?:Patch){
 const patch=wide??terrain[placeId],radius=wide?wide.extent/2*.96:Math.min(380,Math.max(ground.w,ground.d)*1.7),n=128,positions:number[]=[],colours:number[]=[],indices:number[]=[],holes=ground.holes.map(h=>h.map(([x,z]):Point=>[x-offset[0],z-offset[1]]));
 const coordinate=(i:number)=>{const t=i/n*2-1;return Math.sign(t)*Math.pow(Math.abs(t),1.6)*radius};
 const height=(x:number,z:number)=>{
  const source=patch?elevationAt(patch,x,z):Math.max(0,-z*.48)+1.5*Math.sin(x*.25)*Math.sin(z*.18);
  const bench=1-smooth((Math.max(Math.abs(x)/(ground.w*.5),Math.abs(z)/(ground.d*.5))-1)/.6);
  let y=T.MathUtils.lerp(source,-.28,bench);
  for(const p of ground.pads){const distance=Math.max(Math.abs(x-(p.x-offset[0]))-p.w/2,Math.abs(z-(p.z-offset[1]))-p.d/2,0);y=T.MathUtils.lerp(y,p.height,1-smooth(distance/p.feather));}
  return y;
 };
 for(let j=0;j<=n;j++)for(let i=0;i<=n;i++){
  const x=coordinate(i),z=coordinate(j),y=height(x,z);positions.push(x,y,z);
  const ripple=Math.sin(x*.11)*Math.cos(z*.08)*.05,tone=T.MathUtils.clamp(.83+y/(radius*3)+ripple,.65,1.05);colours.push(tone,tone,tone,1-smooth((Math.hypot(x,z)/radius-.72)/.27));
 }
 function triangle(a:number,b:number,c:number){const x=(positions[a*3]+positions[b*3]+positions[c*3])/3,z=(positions[a*3+2]+positions[b*3+2]+positions[c*3+2])/3;if((x/radius)**2+(z/radius)**2>1||holes.some(h=>inside(x,z,h)))return;indices.push(a,b,c);}
 for(let j=0;j<n;j++)for(let i=0;i<n;i++){const a=j*(n+1)+i,b=a+1,c=a+n+1,d=c+1;triangle(a,c,b);triangle(b,c,d);}
 const geometry=new T.BufferGeometry();geometry.setAttribute("position",new T.Float32BufferAttribute(positions,3));geometry.setAttribute("color",new T.Float32BufferAttribute(colours,4));geometry.setIndex(indices);geometry.computeVertexNormals();
 const mat=surface?cloneSiteMaterial(surface):new T.MeshStandardMaterial({color:'#b5a384',roughness:1});mat.vertexColors=true;mat.side=T.DoubleSide;mat.transparent=true;mat.depthWrite=false;
 const mesh=new T.Mesh(geometry,mat);mesh.receiveShadow=true;mesh.castShadow=false;mesh.renderOrder=-3;
 // The block export fills the ground column by column from these, not from triangles that cross a pool edge.
 mesh.userData.heightAt=height;mesh.userData.holes=holes;mesh.userData.radius=radius;
 const details=new T.Group();let seed=7841;const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
 const rubble=new T.InstancedMesh(chippedBlock(1,.65,1,61),stone??new T.MeshStandardMaterial({color:'#a6997d',roughness:1}),650),o=new T.Object3D();
 for(let i=0;i<650;i++){
  let x=0,z=0;for(let attempt=0;attempt<12;attempt++){x=(random()-.5)*radius*1.3;z=(random()-.5)*radius*1.3;if(!holes.some(h=>inside(x,z,h)))break;}
  const size=.06+random()*.31;o.position.set(x,height(x,z)+size*.2,z);o.scale.set(size*(1+random()),size,size);o.rotation.set((random()-.5)*.4,random()*6.28,(random()-.5)*.4);o.updateMatrix();rubble.setMatrixAt(i,o.matrix);rubble.setColorAt(i,new T.Color().setScalar(.78+random()*.35));
 }rubble.castShadow=rubble.receiveShadow=true;rubble.userData.walkDetail=true;details.add(rubble);
 // Sparse dry plants are scenery, with no surveyed vegetation distribution.
 const blades:number[]=[];for(let k=0;k<7;k++){const a=k*2.399,h=.22+(k%3)*.06,r=.12;blades.push(0,0,0,Math.cos(a)*r,h,Math.sin(a)*r,Math.cos(a+.3)*.025,0,Math.sin(a+.3)*.025);}
 const tuft=new T.BufferGeometry();tuft.setAttribute('position',new T.Float32BufferAttribute(blades,3));tuft.computeVertexNormals();const plants=new T.InstancedMesh(tuft,new T.MeshStandardMaterial({color:placeId.includes('gerizim')?'#737756':'#93815a',roughness:1,side:T.DoubleSide}),placeId.includes('gerizim')?100:35);
 for(let i=0;i<plants.count;i++){const x=(random()-.5)*radius*1.4,z=(random()-.5)*radius*1.4;o.position.set(x,height(x,z),z);o.rotation.set(0,random()*6.28,0);o.scale.setScalar(.7+random()*1.2);o.updateMatrix();plants.setMatrixAt(i,o.matrix);}plants.userData.walkCollision=false;details.add(plants);
 return {mesh,details,context:patch?`Terrain around the site anchor · ${patch.anchorPrecision}`:"Unlocated cave · illustrative rock setting",credit:patch?"Mapterhorn elevation · local bench and model placement illustrative":"Cave landscape illustrative · location unassigned",patch};
}
