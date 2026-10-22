// Turns a built atlas site model (a three.js scene) into Minecraft blocks.
// Cells are half a block high, so a lone lower or upper half becomes a slab.
// The geometry, positions and heights stay those of the source model; only
// their resolution changes. The material decides the Minecraft block.
import * as T from 'three';

// Codes 8–11 are the modern setting around a registered site: tree crowns and trunks, green
// ground and roads.
export const MATERIALS=['air','soil','rock','limestone','masonry','plaster','copper','restored','leaves','wood','grass','asphalt'];
const CODE={soil:1,bedrock:2,limestone:3,masonry:4,plaster:5,copper:6,restored:7,leaves:8,wood:9,grass:10,asphalt:11};
// Where two solids share a cell the higher priority wins; a restored part never hides an
// observed one. Ground fill always yields to architecture, and the setting to the site.
const PRIORITY=[0,1,2,3,4,5,6,.5,.3,.4,1.1,1.2];
const MASONRY={rubble:['cobblestone','cobblestone_slab'],coursed:['stone_bricks','stone_brick_slab'],ashlar:['cut_sandstone','cut_sandstone_slab'],mudbrick:['mud_bricks','mud_brick_slab']};
export function blockTable(masonry){
 return {1:['coarse_dirt',null],2:['stone','stone_slab'],3:['smooth_stone','smooth_stone_slab'],4:MASONRY[masonry]??MASONRY.coursed,5:['smooth_quartz','smooth_quartz_slab'],6:['waxed_cut_copper','waxed_cut_copper_slab'],7:['smooth_sandstone','smooth_sandstone_slab'],
  8:['oak_leaves[persistent=true]',null],9:['oak_log',null],10:['moss_block',null],11:['gray_concrete',null]};
}

export function materialCode(material){
 const kind=material?.userData?.siteSurface;
 if(kind)return CODE[kind]??0;
 // The copper lining marks a proposed course or reconstruction in the source.
 if(material?.color&&material.color.getHexString()==='b56b42')return CODE.copper;
 return 0;
}

export function createGrid({minX,maxX,minZ,maxZ,minY,maxY,size}){
 const s=size,h=s/2,x0=Math.floor(minX/s)*s,z0=Math.floor(minZ/s)*s,y0=Math.floor(minY/s)*s;
 const nx=Math.ceil((maxX-x0)/s),nz=Math.ceil((maxZ-z0)/s),ny=2*Math.ceil((maxY-y0)/s),count=nx*ny*nz;
 return {s,h,x0,y0,z0,nx,ny,nz,cells:new Uint8Array(count),solid:new Uint8Array(count),feature:new Uint8Array(count),features:[]};
}
// Cells are stored column by column: index = (i*nz+k)*ny+j.
const cellIndex=(g,i,j,k)=>(i*g.nz+k)*g.ny+j;
function featureIndex(g,id){if(!id)return 0;let n=g.features.indexOf(id);if(n<0){g.features.push(id);n=g.features.length-1;}return n+1;}
function setCell(g,i,j,k,code,feature){
 if(i<0||j<0||k<0||i>=g.nx||j>=g.ny||k>=g.nz)return;
 const n=cellIndex(g,i,j,k);
 if(g.solid[n]&&PRIORITY[g.cells[n]]>PRIORITY[code])return;
 g.cells[n]=code;g.solid[n]=1;if(feature||!g.feature[n])g.feature[n]=feature;
}

const triangles=(mesh,fn)=>{
 const p=mesh.geometry.getAttribute('position'),index=mesh.geometry.getIndex(),colour=mesh.geometry.getAttribute('color'),a=new T.Vector3(),b=new T.Vector3(),c=new T.Vector3();
 for(let t=0;t<(index?.count??p.count);t+=3){
  const ia=index?index.getX(t):t,ib=index?index.getX(t+1):t+1,ic=index?index.getX(t+2):t+2;
  // Faded display edges are not ground, the same rule as the walk colliders.
  if(colour?.itemSize===4&&Math.max(colour.getW(ia),colour.getW(ib),colour.getW(ic))<.03)continue;
  fn(a.fromBufferAttribute(p,ia).applyMatrix4(mesh.matrixWorld),b.fromBufferAttribute(p,ib).applyMatrix4(mesh.matrixWorld),c.fromBufferAttribute(p,ic).applyMatrix4(mesh.matrixWorld));
 }
};
// Column centres inside the triangle's ground projection, with the triangle's height there.
function columns(g,a,b,c,fn){
 const minX=Math.min(a.x,b.x,c.x),maxX=Math.max(a.x,b.x,c.x),minZ=Math.min(a.z,b.z,c.z),maxZ=Math.max(a.z,b.z,c.z);
 const i0=Math.max(0,Math.ceil((minX-g.x0)/g.s-.5)),i1=Math.min(g.nx-1,Math.floor((maxX-g.x0)/g.s-.5)),k0=Math.max(0,Math.ceil((minZ-g.z0)/g.s-.5)),k1=Math.min(g.nz-1,Math.floor((maxZ-g.z0)/g.s-.5));
 const d=(b.z-c.z)*(a.x-c.x)+(c.x-b.x)*(a.z-c.z);if(Math.abs(d)<1e-12)return;
 for(let i=i0;i<=i1;i++)for(let k=k0;k<=k1;k++){
  const x=g.x0+(i+.5)*g.s,z=g.z0+(k+.5)*g.s,u=((b.z-c.z)*(x-c.x)+(c.x-b.x)*(z-c.z))/d,v=((c.z-a.z)*(x-c.x)+(a.x-c.x)*(z-c.z))/d,w=1-u-v;
  if(u<-1e-9||v<-1e-9||w<-1e-9)continue;
  fn(i,k,u*a.y+v*b.y+w*c.y);
 }
}

function insidePolygon(x,z,points){let hit=false;for(let i=0,j=points.length-1;i<points.length;j=i++){const [a,b]=points[i],[c,d]=points[j];if((b>z)!==(d>z)&&x<(c-a)*(z-b)/(d-b)+a)hit=!hit;}return hit;}
// Ground: the top surface of each column, filled down to the grid floor. Columns inside
// the ground's holes (pools, shafts) stay open: the display mesh drops only triangles whose
// centre is inside a hole, and filling the rest would wall in the pool edges. Under a mapped
// path or stair (the mesh's pavedAt) the top half metre takes that block.
export function rasterGround(g,meshes,{soilDepth=2,exclude=null}={}){
 const n=g.nx*g.nz,top=new Float64Array(n).fill(-Infinity),kind=new Uint8Array(n),pave=new Uint8Array(n);
 const excluded=(i,k)=>{if(!exclude)return false;const x=g.x0+(i+.5)*g.s,z=g.z0+(k+.5)*g.s;return x>exclude.minX&&x<exclude.maxX&&z>exclude.minZ&&z<exclude.maxZ;};
 for(const mesh of meshes){
  const code=materialCode(mesh.material)||CODE.soil,holes=mesh.userData.holes??[],inverse=mesh.matrixWorld.clone().invert(),p=new T.Vector3();
  const open=(x,z)=>{p.set(x,0,z).applyMatrix4(inverse);return holes.some(h=>insidePolygon(p.x,p.z,h));};
  if(mesh.userData.heightAt){
   const lift=new T.Vector3().setFromMatrixPosition(mesh.matrixWorld).y,paved=mesh.userData.pavedAt;
   for(let i=0;i<g.nx;i++)for(let k=0;k<g.nz;k++){
    const x=g.x0+(i+.5)*g.s,z=g.z0+(k+.5)*g.s;if(excluded(i,k)||open(x,z))continue;
    p.set(x,0,z).applyMatrix4(inverse);if(Math.hypot(p.x,p.z)>mesh.userData.radius)continue;
    const y=mesh.userData.heightAt(p.x,p.z)+lift,col=i*g.nz+k;if(y>top[col]){top[col]=y;kind[col]=code;pave[col]=paved?CODE[paved(p.x,p.z)]??0:0;}
   }
   continue;
  }
  triangles(mesh,(a,b,c)=>columns(g,a,b,c,(i,k,y)=>{const col=i*g.nz+k;if(y>top[col]&&!excluded(i,k)&&!open(g.x0+(i+.5)*g.s,g.z0+(k+.5)*g.s)){top[col]=y;kind[col]=code;}}));
 }
 for(let i=0;i<g.nx;i++)for(let k=0;k<g.nz;k++){
  const col=i*g.nz+k;if(top[col]===-Infinity)continue;
  for(let j=0;j<g.ny;j++){const y=g.y0+(j+.5)*g.h;if(y>=top[col])break;const n=cellIndex(g,i,j,k);g.cells[n]=pave[col]&&top[col]-y<=.5?pave[col]:kind[col]===CODE.soil&&top[col]-y>soilDepth?CODE.bedrock:kind[col];}
 }
 return top;
}

// An oriented box; dimensions thinner than a cell are widened to one cell so
// thin walls and linings stay continuous instead of breaking into gaps.
function orientedBox(g,matrix,box,code,feature){
 const centre=box.getCenter(new T.Vector3()),half=box.getSize(new T.Vector3()).multiplyScalar(.5),m=matrix.clone().multiply(new T.Matrix4().makeTranslation(centre.x,centre.y,centre.z));
 const origin=new T.Vector3().setFromMatrixPosition(m),axes=[0,1,2].map(i=>new T.Vector3().setFromMatrixColumn(m,i)),ext=[];
 for(let i=0;i<3;i++){
  const length=axes[i].length();if(length<1e-9)return;axes[i].divideScalar(length);const d=axes[i];
  // One direction per axis line, so ties below always fall to the same side.
  const major=Math.abs(d.x)>=Math.abs(d.y)&&Math.abs(d.x)>=Math.abs(d.z)?d.x:Math.abs(d.y)>=Math.abs(d.z)?d.y:d.z;if(major<0)d.negate();
  // The 2 cm allowance closes the drawn joints between stones (1.4–3.5 cm); otherwise a
  // joint on a cell centre leaves a hole through the wall.
  ext.push(Math.max(half.getComponent(i)*length+Math.min(.02,.1*g.h),.5*Math.max(g.s*Math.abs(d.x),g.h*Math.abs(d.y),g.s*Math.abs(d.z))));
 }
 const reach=[0,1,2].map(c=>axes.reduce((sum,d,i)=>sum+ext[i]*Math.abs(d.getComponent(c)),0));
 const i0=Math.max(0,Math.ceil((origin.x-reach[0]-g.x0)/g.s-.5)),i1=Math.min(g.nx-1,Math.floor((origin.x+reach[0]-g.x0)/g.s-.5));
 const j0=Math.max(0,Math.ceil((origin.y-reach[1]-g.y0)/g.h-.5)),j1=Math.min(g.ny-1,Math.floor((origin.y+reach[1]-g.y0)/g.h-.5));
 const k0=Math.max(0,Math.ceil((origin.z-reach[2]-g.z0)/g.s-.5)),k1=Math.min(g.nz-1,Math.floor((origin.z+reach[2]-g.z0)/g.s-.5));
 const q=new T.Vector3();
 for(let i=i0;i<=i1;i++)for(let k=k0;k<=k1;k++)for(let j=j0;j<=j1;j++){
  q.set(g.x0+(i+.5)*g.s-origin.x,g.y0+(j+.5)*g.h-origin.y,g.z0+(k+.5)*g.s-origin.z);
  // Half-open: a cell centre exactly on a face counts on one side only. A closed
  // test lets rounding noise put a wall on alternate sides of a cell boundary.
  let inside=true;for(let a=0;a<3&&inside;a++){const t=q.dot(axes[a]);inside=t>-ext[a]+1e-6&&t<=ext[a]+1e-6;}
  if(inside)setCell(g,i,j,k,code,feature);
 }
}

// Closed meshes: cells whose centre lies between paired crossings of a vertical line.
function parityFill(g,mesh,code,feature){
 const hits=new Map();
 triangles(mesh,(a,b,c)=>columns(g,a,b,c,(i,k,y)=>{const col=i*g.nz+k;let list=hits.get(col);if(!list)hits.set(col,list=[]);list.push(y);}));
 for(const [col,list] of hits){
  list.sort((p,q)=>p-q);const ys=list.filter((y,n)=>n===0||y-list[n-1]>1e-7);
  const i=Math.floor(col/g.nz),k=col%g.nz;
  if(ys.length%2){for(const y of ys)setCell(g,i,Math.floor((y-g.y0)/g.h),k,code,feature);continue;}
  for(let p=0;p<ys.length;p+=2){const j0=Math.floor((ys[p]-g.y0)/g.h-.5+1e-6)+1,j1=Math.floor((ys[p+1]-g.y0)/g.h-.5+1e-6);for(let j=j0;j<=j1;j++)setCell(g,i,j,k,code,feature);}
 }
}

// Open or thin surfaces: cells containing points sampled just inside the surface.
function surfaceSample(g,mesh,code,feature){
 const step=.45*Math.min(g.s,g.h),e=.01*g.h,ab=new T.Vector3(),ac=new T.Vector3(),n=new T.Vector3(),p=new T.Vector3();
 triangles(mesh,(a,b,c)=>{
  ab.subVectors(b,a);ac.subVectors(c,a);n.crossVectors(ab,ac);if(n.lengthSq()<1e-14)return;n.normalize();
  const steps=Math.max(1,Math.ceil(Math.max(ab.length(),ac.length(),b.distanceTo(c))/step));
  for(let u=0;u<=steps;u++)for(let v=0;v<=steps-u;v++){
   p.copy(a).addScaledVector(ab,u/steps).addScaledVector(ac,v/steps).addScaledVector(n,-e);
   setCell(g,Math.floor((p.x-g.x0)/g.s),Math.floor((p.y-g.y0)/g.h),Math.floor((p.z-g.z0)/g.s),code,feature);
  }
 });
}

const isBlock=geometry=>geometry.type==='ExtrudeGeometry'&&geometry.parameters?.options?.bevelEnabled;
const isClosed=geometry=>geometry.type==='ExtrudeGeometry'||geometry.type==='BoxGeometry'||geometry.type==='TorusGeometry'||(geometry.type==='CylinderGeometry'&&!geometry.parameters.openEnded);

export function rasterSolids(g,objects,{minDetail=0}={}){
 const local=new T.Matrix4(),world=new T.Matrix4(),size=new T.Vector3();
 for(const mesh of objects){
  const code=materialCode(mesh.material);if(!code)continue;
  const feature=featureIndex(g,mesh.userData.featureId);
  mesh.geometry.computeBoundingBox();const box=mesh.geometry.boundingBox;
  if(mesh.isInstancedMesh){
   for(let n=0;n<mesh.count;n++){
    mesh.getMatrixAt(n,local);world.multiplyMatrices(mesh.matrixWorld,local);
    // Small scattered pebbles are scenery below block size; larger fallen stones stay.
    if(mesh.userData.walkDetail){box.getSize(size);const scale=new T.Vector3().setFromMatrixScale(world);if(Math.max(size.x*scale.x,size.z*scale.z)<minDetail)continue;}
    if(Math.abs(world.determinant())>1e-12)orientedBox(g,world,box,code,feature);
   }
   continue;
  }
  if(isBlock(mesh.geometry)){orientedBox(g,mesh.matrixWorld,box,code,feature);continue;}
  const scale=new T.Vector3().setFromMatrixScale(mesh.matrixWorld),dims=box.getSize(size).multiply(scale);
  if(isClosed(mesh.geometry)){parityFill(g,mesh,code,feature);if(Math.min(dims.x,dims.z)<g.s||dims.y<g.h)surfaceSample(g,mesh,code,feature);}
  else surfaceSample(g,mesh,code,feature);
 }
}

export function carve(g,{minX,maxX,minY,maxY,minZ,maxZ}){
 for(let i=0;i<g.nx;i++)for(let k=0;k<g.nz;k++)for(let j=0;j<g.ny;j++){
  const x=g.x0+(i+.5)*g.s,y=g.y0+(j+.5)*g.h,z=g.z0+(k+.5)*g.s;
  if(x>minX&&x<maxX&&y>minY&&y<maxY&&z>minZ&&z<maxZ){const n=cellIndex(g,i,j,k);g.cells[n]=0;g.solid[n]=0;g.feature[n]=0;}
 }
}

// Rock below the lowest occupied cell: no hollow void under pool floors and shafts.
export function underfill(g){
 for(let i=0;i<g.nx;i++)for(let k=0;k<g.nz;k++){
  const base=cellIndex(g,i,0,k);let lowest=-1;for(let j=0;j<g.ny;j++)if(g.cells[base+j]){lowest=j;break;}
  for(let j=0;j<lowest;j++)g.cells[base+j]=CODE.bedrock;
 }
}

// Blocks: [i][Y][k] → palette index of a block state string.
export function toBlocks(g,masonry){
 const table=blockTable(masonry),ny=g.ny/2,blocks=new Uint16Array(g.nx*ny*g.nz),palette=['air'],lookup=new Map([['air',0]]),feature=new Uint8Array(g.nx*ny*g.nz);
 const id=state=>{let n=lookup.get(state);if(n===undefined){n=palette.length;palette.push(state);lookup.set(state,n);}return n;};
 for(let i=0;i<g.nx;i++)for(let k=0;k<g.nz;k++)for(let Y=0;Y<ny;Y++){
  const lo=cellIndex(g,i,2*Y,k),up=lo+1,a=g.cells[lo],b=g.cells[up],out=(i*g.nz+k)*ny+Y;if(!a&&!b)continue;
  let state;
  if(a&&b)state=table[PRIORITY[a]>=PRIORITY[b]?a:b][0];
  else{const code=a||b,[full,slab]=table[code];state=slab?`${slab}[type=${a?'bottom':'top'}]`:full;}
  const first=PRIORITY[a]>=PRIORITY[b];blocks[out]=id(state);feature[out]=g.feature[first?lo:up]||g.feature[first?up:lo];
 }
 return {nx:g.nx,ny,nz:g.nz,blocks,palette,feature};
}

// Greedy boxes of identical blocks, each within /fill's default 32,768-block limit.
export function fillBoxes(b){
 const seen=new Uint8Array(b.blocks.length),at=(i,Y,k)=>(i*b.nz+k)*b.ny+Y,boxes=[];
 for(let i=0;i<b.nx;i++)for(let k=0;k<b.nz;k++)for(let Y=0;Y<b.ny;Y++){
  const n=at(i,Y,k),state=b.blocks[n];if(!state||seen[n])continue;
  let y1=Y;while(y1+1<b.ny&&y1-Y<63&&b.blocks[at(i,y1+1,k)]===state&&!seen[at(i,y1+1,k)])y1++;
  const free=(ii,kk)=>{for(let y=Y;y<=y1;y++){const m=at(ii,y,kk);if(b.blocks[m]!==state||seen[m])return false;}return true;};
  let k1=k;while(k1+1<b.nz&&(k1+2-k)*(y1-Y+1)<=512&&free(i,k1+1))k1++;
  let i1=i;grow:while(i1+1<b.nx&&(i1+2-i)*(k1-k+1)*(y1-Y+1)<=32768){for(let kk=k;kk<=k1;kk++)if(!free(i1+1,kk))break grow;i1++;}
  for(let ii=i;ii<=i1;ii++)for(let kk=k;kk<=k1;kk++)for(let y=Y;y<=y1;y++)seen[at(ii,y,kk)]=1;
  boxes.push([i,Y,k,i1,y1,k1,state]);
 }
 return boxes;
}
