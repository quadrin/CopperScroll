// Reads blocks and sky light back from a Minecraft Java world's region files
// (Anvil format, 1.18+ chunk layout). Only the parts this pipeline needs.
import {readFileSync,existsSync} from 'node:fs';
import {inflateSync,gunzipSync} from 'node:zlib';

export function readNbt(buffer){
 let at=0;
 const u8=()=>buffer[at++],i16=()=>{const v=buffer.readInt16BE(at);at+=2;return v;},i32=()=>{const v=buffer.readInt32BE(at);at+=4;return v;};
 const str=()=>{const n=buffer.readUInt16BE(at);at+=2;const v=buffer.toString('utf8',at,at+n);at+=n;return v;};
 function payload(type){
  switch(type){
   case 1:{const v=buffer.readInt8(at);at+=1;return v;}
   case 2:return i16();
   case 3:return i32();
   case 4:{const v=buffer.readBigInt64BE(at);at+=8;return v;}
   case 5:{const v=buffer.readFloatBE(at);at+=4;return v;}
   case 6:{const v=buffer.readDoubleBE(at);at+=8;return v;}
   case 7:{const n=i32(),v=buffer.subarray(at,at+n);at+=n;return v;}
   case 8:return str();
   case 9:{const t=u8(),n=i32(),list=[];for(let i=0;i<n;i++)list.push(payload(t));return list;}
   case 10:{const o={};for(;;){const t=u8();if(t===0)return o;const name=str();o[name]=payload(t);}}
   case 11:{const n=i32(),v=new Int32Array(n);for(let i=0;i<n;i++)v[i]=i32();return v;}
   case 12:{const n=i32(),v=new BigInt64Array(n);for(let i=0;i<n;i++){v[i]=buffer.readBigInt64BE(at);at+=8;}return v;}
   default:throw Error(`Unknown NBT tag ${type}`);
  }
 }
 const type=u8();str();return payload(type);
}

// Block state as "name[key=value,...]" with sorted properties, the form used for comparison.
// Palettes come as {Name, Properties} (1.18–1.21) or, since 26.x, as a bare string,
// a compound with one empty-named string, or {id, properties}.
export function stateKey(entry){
 const raw=typeof entry==='string'?entry:entry.Name??entry.id??entry[''],properties=typeof entry==='string'?null:entry.Properties??entry.properties;
 if(typeof raw!=='string')throw Error(`Unknown palette entry ${JSON.stringify(entry)}`);
 const name=raw.replace(/^minecraft:/,''),props=properties?Object.entries(properties).sort(([a],[b])=>a.localeCompare(b)):[];
 return props.length?`${name}[${props.map(([k,v])=>`${k}=${v}`).join(',')}]`:name;
}

export class World{
 constructor(regionDir){this.regionDir=regionDir;this.regions=new Map();this.chunks=new Map();}
 region(rx,rz){
  const key=`${rx},${rz}`;if(this.regions.has(key))return this.regions.get(key);
  const path=`${this.regionDir}/r.${rx}.${rz}.mca`,data=existsSync(path)?readFileSync(path):null;this.regions.set(key,data);return data;
 }
 chunk(cx,cz){
  const key=`${cx},${cz}`;if(this.chunks.has(key))return this.chunks.get(key);
  let chunk=null;const region=this.region(Math.floor(cx/32),Math.floor(cz/32));
  if(region&&region.length>=8192){
   const slot=((cz&31)*32+(cx&31))*4,offset=(region[slot]<<16|region[slot+1]<<8|region[slot+2])*4096;
   if(offset){
    const length=region.readUInt32BE(offset),kind=region[offset+4],body=region.subarray(offset+5,offset+4+length);
    if(kind!==2&&kind!==1&&kind!==3)throw Error(`Chunk ${key}: compression type ${kind} is not supported`);
    const nbt=readNbt(kind===2?inflateSync(body):kind===1?gunzipSync(body):body);
    const sections=new Map();
    for(const s of nbt.sections??[]){
     const palette=s.block_states?.palette?.map(stateKey)??['air'],data=s.block_states?.data,bits=Math.max(4,Math.ceil(Math.log2(palette.length)));
     sections.set(s.Y,{palette,data,bits,perLong:Math.floor(64/bits),sky:s.SkyLight??null});
    }
    chunk={status:nbt.Status,light:nbt.isLightOn,sections,dataVersion:nbt.DataVersion};
   }
  }
  this.chunks.set(key,chunk);return chunk;
 }
 section(x,y,z){const c=this.chunk(Math.floor(x/16),Math.floor(z/16));return c?.sections.get(Math.floor(y/16))??null;}
 block(x,y,z){
  const s=this.section(x,y,z);if(!s)return 'air';if(!s.data)return s.palette[0];
  const i=((y&15)*16+(z&15))*16+(x&15),long=s.data[Math.floor(i/s.perLong)],shift=BigInt((i%s.perLong)*s.bits);
  return s.palette[Number((BigInt.asUintN(64,long)>>shift)&((1n<<BigInt(s.bits))-1n))];
 }
 // Sky light 0–15, or null where the save holds no light for that section.
 skyLight(x,y,z){
  const s=this.section(x,y,z);if(!s?.sky)return null;
  const i=((y&15)*16+(z&15))*16+(x&15),byte=s.sky[i>>1]&255;return i&1?byte>>4:byte&15;
 }
}
