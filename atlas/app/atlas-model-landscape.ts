import * as T from "three";
import patches from "./atlas-model-terrain.json";
type Point=[number,number];
export type LandscapePad={x:number;z:number;w:number;d:number;height:number;feather:number};
export type LandscapeGround={w:number;d:number;holes:Point[][];pads:LandscapePad[]};
type Patch={lat:number;lon:number;anchorPrecision:string;extent:number;size:number;elevations:number[];centreElevation:number};
const terrain=patches as Record<string,Patch>;
const smooth=(t:number)=>{const v=T.MathUtils.clamp(t,0,1);return v*v*(3-2*v)};
function inside(x:number,z:number,points:Point[]){let hit=false;for(let i=0,j=points.length-1;i<points.length;j=i++){const [a,b]=points[i],[c,d]=points[j];if((b>z)!==(d>z)&&x<(c-a)*(z-b)/(d-b)+a)hit=!hit;}return hit;}
export function elevationAt(patch:Patch,x:number,z:number){
 const u=T.MathUtils.clamp((x/patch.extent+.5)*(patch.size-1),0,patch.size-1),v=T.MathUtils.clamp((z/patch.extent+.5)*(patch.size-1),0,patch.size-1),i=Math.floor(u),j=Math.floor(v),a=u-i,b=v-j;
 const value=(x:number,y:number)=>patch.elevations[Math.min(y,patch.size-1)*patch.size+Math.min(x,patch.size-1)];
 return T.MathUtils.lerp(T.MathUtils.lerp(value(i,j),value(i+1,j),a),T.MathUtils.lerp(value(i,j+1),value(i+1,j+1),a),b)-patch.centreElevation;
}
export function landscapeGround(ground:LandscapeGround,placeId:string,offset:Point){
 const patch=terrain[placeId],radius=Math.min(380,Math.max(ground.w,ground.d)*1.7),n=128,positions:number[]=[],colours:number[]=[],indices:number[]=[],holes=ground.holes.map(h=>h.map(([x,z]):Point=>[x-offset[0],z-offset[1]]));
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
  const ripple=Math.sin(x*.11)*Math.cos(z*.08)*.03,tone=T.MathUtils.clamp(.45+y/(radius*.6)+ripple,0,1),color=new T.Color().lerpColors(new T.Color("#c6b98e"),new T.Color("#dfd1b1"),tone);colours.push(color.r,color.g,color.b,1-smooth((Math.hypot(x,z)/radius-.72)/.27));
 }
 function triangle(a:number,b:number,c:number){const x=(positions[a*3]+positions[b*3]+positions[c*3])/3,z=(positions[a*3+2]+positions[b*3+2]+positions[c*3+2])/3;if((x/radius)**2+(z/radius)**2>1||holes.some(h=>inside(x,z,h)))return;indices.push(a,b,c);}
 for(let j=0;j<n;j++)for(let i=0;i<n;i++){const a=j*(n+1)+i,b=a+1,c=a+n+1,d=c+1;triangle(a,c,b);triangle(b,c,d);}
 const geometry=new T.BufferGeometry();geometry.setAttribute("position",new T.Float32BufferAttribute(positions,3));geometry.setAttribute("color",new T.Float32BufferAttribute(colours,4));geometry.setIndex(indices);geometry.computeVertexNormals();
 const mesh=new T.Mesh(geometry,new T.MeshStandardMaterial({vertexColors:true,roughness:1,side:T.DoubleSide,transparent:true,depthWrite:false}));mesh.receiveShadow=true;mesh.castShadow=true;
 return {mesh,context:patch?`Terrain around the site anchor · ${patch.anchorPrecision}`:"Unlocated cave · illustrative rock setting",credit:patch?"Mapterhorn elevation · local bench and model placement illustrative":"Cave landscape illustrative · location unassigned",patch};
}
