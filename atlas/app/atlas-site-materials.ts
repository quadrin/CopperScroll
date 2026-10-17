import * as T from 'three';

// Original procedural surface art. Base colours and masonry types come from
// reference photographs (atlas-site-surfaces.json, built by
// tools/build_site_surfaces.py); the photos guide the material character, not
// a claim about individual blocks, cracks, weathering or ancient surface colours.
import surfaceData from './atlas-site-surfaces.json';
type Surface = 'masonry' | 'limestone' | 'bedrock' | 'soil' | 'plaster';
export type Masonry = 'rubble' | 'coursed' | 'ashlar' | 'mudbrick';
type Style = {id:string;stone:string;rock:string;soil:string;plaster:string;lichen:number;courses:number;masonry:Masonry;photos:string[];masonryNote?:string};
type PhotoSurface = {stone?:string;rock?:string;soil?:string;plaster?:string;masonry:Masonry;masonryNote:string;photos:string[];lichen?:number};
const photoSurfaces = surfaceData.sites as Record<string,PhotoSurface>;
const fallback = (id:string) => {
 if(id.includes('gerizim'))return {id:'gerizim',stone:'#aaa99b',rock:'#97978a',soil:'#827a61',plaster:'#c3ba9f',lichen:.28,courses:.38};
 if(id.includes('siloam'))return {id:'siloam',stone:'#b7ad92',rock:'#a9a087',soil:'#8f8269',plaster:'#b1b09c',lichen:.23,courses:.33};
 if(id.includes('jericho'))return {id:'jericho',stone:'#ceb998',rock:'#b7a387',soil:'#ae8d67',plaster:'#dbbba0',lichen:.015,courses:.31};
 if(id.includes('doq'))return {id:'doq',stone:'#baab8a',rock:'#ac926e',soil:'#9e825f',plaster:'#c2b79b',lichen:.035,courses:.33};
 if(id.includes('hyrcania'))return {id:'hyrcania',stone:'#c9bea1',rock:'#b8ab8d',soil:'#a39170',plaster:'#b4b5a0',lichen:.045,courses:.35};
 return {id:'qumran',stone:'#c6b896',rock:'#b7a47e',soil:'#b29a72',plaster:'#d1c5a6',lichen:.015,courses:.29};
};
export const siteStyle = (id:string):Style => {
 const base=fallback(id),photo=photoSurfaces[base.id];
 if(!photo)return {...base,masonry:'coursed',photos:[]};
 return {...base,stone:photo.stone??base.stone,rock:photo.rock??base.rock,soil:photo.soil??base.soil,plaster:photo.plaster??base.plaster,lichen:photo.lichen??base.lichen,masonry:photo.masonry,photos:photo.photos,masonryNote:photo.masonryNote};
};
const fract=(v:number)=>v-Math.floor(v);
const hash=(x:number,y:number,seed:number)=>fract(Math.sin(x*127.1+y*311.7+seed*74.7)*43758.5453);
function noise(x:number,y:number,seed:number,periodX=256,periodY=256){const i=Math.floor(x)%periodX,j=Math.floor(y)%periodY,a=fract(x),b=fract(y),u=a*a*(3-2*a),v=b*b*(3-2*b),nextX=(i+1)%periodX,nextY=(j+1)%periodY;return T.MathUtils.lerp(T.MathUtils.lerp(hash(i,j,seed),hash(nextX,j,seed),u),T.MathUtils.lerp(hash(i,nextY,seed),hash(nextX,nextY,seed),u),v);}
function surfaces(kind:Surface,style:Style){
 const n=512,colour=new Uint8Array(n*n*4),relief=new Uint8Array(n*n*4);
 const fractures=Array.from({length:72},(_,i)=>[.15+hash(i,0,31)*.7,.15+hash(i,0,32)*.7]);
 const base=new T.Color(kind==='soil'?style.soil:kind==='plaster'?style.plaster:kind==='bedrock'?style.rock:style.stone).convertLinearToSRGB();
 const metres=kind==='masonry'?style.courses*(style.masonry==='rubble'?12:8):kind==='soil'?3:kind==='bedrock'?5:2;
 const clamp=(v:number)=>T.MathUtils.clamp(v,0,1);
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  const u=x/n,v=y/n,coarse=noise(u*16,v*16,5,16,16),medium=noise(u*57,v*57,12,57,57),fine=hash(x,y,7),micro=noise(u*145,v*145,9,145,145);
  let tone=.80+coarse*.25+(medium-.5)*.12+(fine-.5)*.12,h=.4+medium*.09+(micro-.5)*.04,r=.9,moss=0;
  if(kind==='masonry'&&style.masonry==='rubble'){
   // Irregular fieldstones: nearest jittered seed defines a stone, the gap to
   // the second-nearest seed defines a wide, uneven mortar joint.
   const gx=u*9,gy=v*12,ix=Math.floor(gx),iy=Math.floor(gy);let first=10,second=10,owner=0;
   for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const cx=(ix+dx+9)%9,cy=(iy+dy+12)%12,sx=ix+dx+.15+hash(cx,cy,41)*.7,sy=iy+dy+.15+hash(cx,cy,42)*.7,d=Math.hypot((gx-sx)*1.25,gy-sy);if(d<first){second=first;first=d;owner=cx*31+cy;}else if(d<second)second=d;}
   const gap=second-first,bevel=clamp((gap-.06-noise(u*90,v*90,3,90,90)*.07)*7),block=hash(owner,1,23);
   tone*=.72+block*.52;tone*=.42+.58*bevel;h=.08+bevel*.62+coarse*.12;
  }else if(kind==='masonry'){
   const rows=style.masonry==='ashlar'?6:style.masonry==='mudbrick'?11:8,per=style.masonry==='ashlar'?2:style.masonry==='mudbrick'?3:4;
   const row=Math.floor(v*rows),yy=fract(v*rows),shift=hash(row,0,10),px=u*per+shift,cell=Math.floor(px),xx=fract(px);
   const joint=style.masonry==='ashlar'?.45:style.masonry==='mudbrick'?.8:.55,broken=(style.masonry==='ashlar'?.004:.008)+noise(u*180,v*180,3,180,180)*(style.masonry==='ashlar'?.006:.012);
   const edge=Math.min(xx,1-xx,yy*joint,(1-yy)*joint);
   const bevel=clamp((edge-broken)*(style.masonry==='ashlar'?40:25)),block=hash(cell,row,22);
   tone*=(style.masonry==='ashlar'?.86:.74)+block*(style.masonry==='ashlar'?.24:.46);tone*=.51+.49*bevel;h=.12+bevel*.55+coarse*.10;
   // Recessed, irregular joints and granular chisel marks survive close zoom.
   tone-=Math.max(0,.12-micro)*.45;moss=style.lichen*noise(u*12,v*12,87,12,12)*(1-bevel*.6);
  }else if(kind==='bedrock'){
   const line=fract(v*13+noise(u*6,v*3,14,6,3)*1.1+noise(u*28,v*11,15,28,11)*.35),joint=Math.min(line,1-line);
   const strata=clamp(joint*29),gx=u*9,gy=v*8,ix=Math.floor(gx),iy=Math.floor(gy);let first=10,second=10;
   // Angular fracture boundaries avoid a regular masonry grid or looping lines.
   for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){
    const [a,b]=fractures[((iy+dy+8)%8)*9+(ix+dx+9)%9],distance=(ix+dx+a-gx)**2+(iy+dy+b-gy)**2;
    if(distance<first){second=first;first=distance;}else if(distance<second)second=distance;
   }
   const crack=second-first;
   tone*=.73+strata*.28+noise(u*9,v*21,4,9,21)*.12;tone*=crack<.018?.80:1;
   h=.2+strata*.38+coarse*.25;r=.97;
  }else if(kind==='limestone'){
   const vein=Math.abs(noise(u*20,v*20,6,20,20)-.5),pit=medium<.22?.88:1;
   tone*=pit*(vein<.012?.91:1);h=.35+coarse*.20+medium*.09;
  }else if(kind==='soil'){
   const gx=u*72,gy=v*72,ix=Math.floor(gx),iy=Math.floor(gy),dx=fract(gx)-.5,dy=fract(gy)-.5;
   const pebble=Math.hypot(dx,dy)<.14+hash(ix,iy,3)*.2&&hash(ix,iy,2)>.45;
   if(pebble){tone*=1.12+(dx-dy)*.45;h+=.28;r=.98;}else{tone*=.86+micro*.2;h+=fine*.06;}
   tone*=.90+noise(u*7,v*7,13,7,7)*.18;
  }else{
   const patch=noise(u*8,v*8,16,8,8),edge=Math.abs(noise(u*37,v*37,4,37,37)-.5);
   tone*=.83+patch*.26;if(edge<.012){tone*=.72;h-=.1;}
   h=.48+medium*.05+fine*.025;moss=style.lichen*noise(u*11,v*11,88,11,11);r=.87;
  }
  const i=(y*n+x)*4;colour[i]=255*clamp(base.r*tone-moss*.15);colour[i+1]=255*clamp(base.g*tone-moss*.09);colour[i+2]=255*clamp(base.b*tone-moss*.17);colour[i+3]=255;
  relief[i]=255*clamp(h);relief[i+1]=255*clamp(r+(fine-.5)*.08);relief[i+2]=0;relief[i+3]=255;
 }
 // Renormalise so the texture's mean colour equals the photo-derived base;
 // joints and tone variation then add contrast without darkening the surface.
 {let sr=0,sg=0,sb=0;const count=n*n;for(let i=0;i<count*4;i+=4){sr+=colour[i];sg+=colour[i+1];sb+=colour[i+2];}
  const fr=base.r*255*count/Math.max(1,sr),fg=base.g*255*count/Math.max(1,sg),fb=base.b*255*count/Math.max(1,sb);
  for(let i=0;i<count*4;i+=4){colour[i]=Math.min(255,colour[i]*fr);colour[i+1]=Math.min(255,colour[i+1]*fg);colour[i+2]=Math.min(255,colour[i+2]*fb);}}
 const texture=(data:Uint8Array,srgb=false)=>{const t=new T.DataTexture(data,n,n);t.wrapS=t.wrapT=T.RepeatWrapping;t.magFilter=T.LinearFilter;t.minFilter=T.LinearMipmapLinearFilter;t.generateMipmaps=true;t.anisotropy=8;if(srgb)t.colorSpace=T.SRGBColorSpace;t.needsUpdate=true;return t;};
 return {map:texture(colour,true),relief:texture(relief),metres};
}

// World-space projection keeps a stone the same size on a 200 m enclosure,
// a short wall, an instanced block and an irregular cliff. No stretched box UVs.
function projectedSurface(material:T.MeshStandardMaterial,metres:number,organic=false){
 material.onBeforeCompile=shader=>{
  shader.uniforms.siteMetres={value:metres};
  shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 vSitePosition; varying vec3 vSiteNormal;');
  shader.vertexShader=shader.vertexShader.replace('#include <worldpos_vertex>',`#include <worldpos_vertex>
   vec4 sitePosition=vec4(transformed,1.0); vec3 siteNormal=objectNormal;
   #ifdef USE_INSTANCING
    sitePosition=instanceMatrix*sitePosition; siteNormal=mat3(instanceMatrix)*siteNormal;
   #endif
   vSitePosition=(modelMatrix*sitePosition).xyz; vSiteNormal=normalize(mat3(modelMatrix)*siteNormal);`);
  shader.fragmentShader=shader.fragmentShader.replace('#include <common>',`#include <common>
   varying vec3 vSitePosition; varying vec3 vSiteNormal; uniform float siteMetres;
   vec4 siteSample(sampler2D surfaceMap){
    vec3 n=abs(normalize(vSiteNormal)),p=vSitePosition/siteMetres;
    vec2 uv=n.y>max(n.x,n.z)?p.xz:(n.x>n.z?p.zy:p.xy);
    return ${organic?'texture2D(surfaceMap,uv)*.62+texture2D(surfaceMap,mat2(.74,-.67,.67,.74)*uv*1.71+vec2(.31,.73))*.38':'texture2D(surfaceMap,uv)'};
   }`);
  shader.fragmentShader=shader.fragmentShader.replace('#include <map_fragment>','diffuseColor *= siteSample(map);');
  shader.fragmentShader=shader.fragmentShader.replace('#include <roughnessmap_fragment>','float roughnessFactor = roughness * siteSample(roughnessMap).g;');
  shader.fragmentShader=shader.fragmentShader.replace('#include <normal_fragment_maps>',`float siteRelief=siteSample(bumpMap).r;
   normal=perturbNormalArb(-vViewPosition,normal,vec2(dFdx(siteRelief),dFdy(siteRelief))*bumpScale,faceDirection);`);
 };
 material.customProgramCacheKey=()=>`site-surface-v3-${metres}-${organic}`;
 return material;
}
export function cloneSiteMaterial<M extends T.Material>(material:M):M {const clone=material.clone();clone.onBeforeCompile=material.onBeforeCompile;clone.customProgramCacheKey=material.customProgramCacheKey;return clone;}
export function createSiteMaterials(id:string){
 const style=siteStyle(id);
 const make=(kind:Surface)=>{const t=surfaces(kind,style),m=new T.MeshStandardMaterial({map:t.map,bumpMap:t.relief,roughnessMap:t.relief,bumpScale:kind==='bedrock'?.07:kind==='soil'?.025:kind==='plaster'?.012:.032,roughness:1});m.name=`${style.id}-${kind}`;m.userData.siteSurface=kind;m.userData.siteStyle=style.id;return projectedSurface(m,t.metres,kind==='soil');};
 return {style,stone:make('masonry'),block:make('limestone'),rock:make('bedrock'),earth:make('soil'),plaster:make('plaster')};
}

export function chippedBlock(w:number,h:number,d:number,seed=1){
 const b=Math.min(w,h,d,.4)*.065,s=new T.Shape();s.moveTo(-w/2+b,-h/2+b);s.lineTo(w/2-b,-h/2+b);s.lineTo(w/2-b,h/2-b);s.lineTo(-w/2+b,h/2-b);s.closePath();
 const g=new T.ExtrudeGeometry(s,{depth:Math.max(.001,d-2*b),bevelEnabled:true,bevelSegments:1,steps:1,bevelSize:b,bevelThickness:b});g.translate(0,0,-d/2+b);
 // One shared low-poly form gives chipped edges without rounded potato rocks.
 const p=g.getAttribute('position');for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i);const edge=hash(Math.round(x*100),Math.round(y*100+z*31),seed);p.setXYZ(i,x+(edge-.5)*b*.4,y+(edge-.5)*b*.3,z+(edge-.5)*b*.4);}g.computeVertexNormals();return g;
}

export function disposeSiteScene(root:T.Object3D){
 const textures=new Set<T.Texture>(),materials=new Set<T.Material>(),geometries=new Set<T.BufferGeometry>();
 root.traverse(o=>{const mesh=o as T.Mesh;if(mesh.geometry)geometries.add(mesh.geometry);for(const m of Array.isArray(mesh.material)?mesh.material:mesh.material?[mesh.material]:[]){materials.add(m);for(const v of Object.values(m))if(v instanceof T.Texture)textures.add(v);}});
 textures.forEach(t=>t.dispose());materials.forEach(m=>m.dispose());geometries.forEach(g=>g.dispose());
}
