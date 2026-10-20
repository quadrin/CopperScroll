// Greedy quads over the half-height cell grid read back from the Minecraft world.
// Faces carry Minecraft's saved sky light (0–15) of the open block in front of them.
import {gzipSync} from 'node:zlib';

// The grid's sides and floor are closed too. Outside the block area the smooth terrain
// covers them; without them a walker who leaves the area could see or walk into its
// hollow inside.
export function greedyQuads({nx,ny,nz,cells,feature,light}){
 const at=(i,j,k)=>(i*nz+k)*ny+j,outside=(i,j,k)=>i<0||k<0||j<0||i>=nx||k>=nz||j>=ny;
 const solid=(i,j,k)=>!outside(i,j,k)&&cells[at(i,j,k)]!==0;
 const lightAt=(i,j,k)=>outside(i,j,k)?15:light[at(i,j,k)];
 const dims=[nx,ny,nz],groups=new Map();
 for(let dir=0;dir<6;dir++){
  const axis=dir>>1,sign=dir&1?-1:1,[ua,va]=axis===0?[2,1]:axis===1?[0,2]:[0,1],nu=dims[ua],nv=dims[va],mask=new Int32Array(nu*nv);
  for(let t=0;t<dims[axis];t++){
   mask.fill(0);
   for(let u=0;u<nu;u++)for(let v=0;v<nv;v++){
    const c=[0,0,0];c[axis]=t;c[ua]=u;c[va]=v;const n=at(c[0],c[1],c[2]),code=cells[n];if(!code)continue;
    const o=[...c];o[axis]+=sign;if(solid(o[0],o[1],o[2]))continue;
    mask[u*nv+v]=1+code+(feature[n]<<3)+(lightAt(o[0],o[1],o[2])<<11);
   }
   for(let u=0;u<nu;u++)for(let v=0;v<nv;){
    const key=mask[u*nv+v];if(!key){v++;continue;}
    let v1=v+1;while(v1<nv&&mask[u*nv+v1]===key)v1++;
    let u1=u+1;grow:while(u1<nu){for(let w=v;w<v1;w++)if(mask[u1*nv+w]!==key)break grow;u1++;}
    for(let uu=u;uu<u1;uu++)mask.fill(0,uu*nv+v,uu*nv+v1);
    const value=key-1,code=value&7,feat=(value>>3)&255,lit=value>>11,group=`${code}:${feat}`;
    let list=groups.get(group);if(!list)groups.set(group,list=[]);
    list.push(dir|lit<<3,sign>0?t+1:t,u,v,u1,v1);
    v=v1;
   }
  }
 }
 return groups;
}

// File: [u32 header length][header JSON][pad to 4][Uint16 quads per group], gzipped.
// Each quad: dir|light<<3, plane, u0, v0, u1, v1 in grid units.
export function encodeBuild(header,groups){
 const list=[...groups].map(([key,quads])=>{const [material,feature]=key.split(':').map(Number);return {material,feature,quads:quads.length/6,data:Uint16Array.from(quads)};});
 const json=Buffer.from(JSON.stringify({...header,groups:list.map(({material,feature,quads})=>({material,feature,quads}))}),'utf8');
 const pad=(4-(4+json.length)%4)%4,head=Buffer.alloc(4);head.writeUInt32LE(json.length+pad,0);
 for(const g of list)if(g.data.some(v=>v>65535))throw Error('Grid too large for 16-bit quads');
 return gzipSync(Buffer.concat([head,json,Buffer.from(' '.repeat(pad)),...list.map(g=>Buffer.from(g.data.buffer))]),{level:9});
}
