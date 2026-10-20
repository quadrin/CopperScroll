// Minimal Source RCON client for a local Minecraft server: one reply per command.
import net from 'node:net';
import {once} from 'node:events';

export async function connectRcon({host='127.0.0.1',port,password}){
 const socket=net.connect(port,host);await once(socket,'connect');
 let buffer=Buffer.alloc(0),nextId=1,failure=null;const waiting=new Map();
 socket.on('data',chunk=>{
  buffer=Buffer.concat([buffer,chunk]);
  while(buffer.length>=4){
   const length=buffer.readInt32LE(0);if(buffer.length<4+length)break;
   const id=buffer.readInt32LE(4),body=buffer.toString('utf8',12,4+length-2);buffer=buffer.subarray(4+length);
   if(id===-1){failure=Error('RCON authentication failed');for(const [,w] of waiting)w.reject(failure);waiting.clear();continue;}
   const w=waiting.get(id);if(w){waiting.delete(id);w.resolve(body);}
  }
 });
 socket.on('error',e=>{failure=e;for(const [,w] of waiting)w.reject(e);waiting.clear();});
 function send(type,body){
  if(failure)return Promise.reject(failure);
  const id=nextId++,payload=Buffer.from(body,'utf8'),packet=Buffer.alloc(14+payload.length);
  packet.writeInt32LE(10+payload.length,0);packet.writeInt32LE(id,4);packet.writeInt32LE(type,8);payload.copy(packet,12);
  return new Promise((resolve,reject)=>{waiting.set(id,{resolve,reject});socket.write(packet);});
 }
 await send(3,password);
 return {command:text=>send(2,text),close:()=>socket.end()};
}
