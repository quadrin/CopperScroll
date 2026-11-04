"use client";
import {useEffect,useRef,useState} from 'react';
import * as T from 'three';
const base=import.meta.env?.BASE_URL??'/';
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const candidates=[{name:'Twin Cave',area:'near Qumran',lat:31.74183,lon:35.45941,dx:0,dy:0},{name:'IV/17',area:'near Jericho',lat:31.85611,lon:35.46306,dx:-60,dy:-8},{name:'IV/11',area:'near Jericho',lat:31.85611,lon:35.46306,dx:64,dy:28}];
type Position={x:number;y:number};
export default function CandidateMap({progress,reduced=false}:{progress:number;reduced?:boolean}){
 const host=useRef<HTMLDivElement>(null),update=useRef<((p:number)=>void)|null>(null),current=useRef(progress),[positions,setPositions]=useState<Position[]>([]),[failed,setFailed]=useState(false);current.current=progress;
 useEffect(()=>{
  let stopped=false,renderer:T.WebGLRenderer|undefined,geometry:T.PlaneGeometry|undefined,material:T.MeshStandardMaterial|undefined,observer:ResizeObserver|undefined;const controller=new AbortController();
  async function mount(){try{
   const response=await fetch(`${base}introduction/opening-terrain.json`,{signal:controller.signal});if(!response.ok)throw Error('Terrain unavailable');const data=await response.json() as {anchor:{lat:number;lon:number};regional:{size:number;extent:number;centreElevation:number;elevations:number[]}};if(stopped||!host.current)return;
   renderer=new T.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=T.SRGBColorSpace;renderer.setClearColor('#f7f5ef',0);host.current.appendChild(renderer.domElement);
   const scene=new T.Scene(),camera=new T.PerspectiveCamera(38,1,10,150000);scene.add(new T.HemisphereLight('#fffdf5','#77776c',2));const sun=new T.DirectionalLight('#fffaf3',2.3);sun.position.set(-18000,25000,13000);scene.add(sun);
   const grid=data.regional,step=2,n=(grid.size-1)/step+1;geometry=new T.PlaneGeometry(grid.extent,grid.extent,n-1,n-1);geometry.rotateX(-Math.PI/2);const vertices=geometry.getAttribute('position') as T.BufferAttribute,colors=new Float32Array(n*n*3),chalk=new T.Color('#c9c4b8'),high=new T.Color('#aaa692'),lake=new T.Color('#809c9b'),color=new T.Color();
   for(let j=0;j<n;j++)for(let i=0;i<n;i++){const k=j*n+i,h=grid.elevations[j*step*grid.size+i*step];vertices.setY(k,(h-grid.centreElevation)*1.65);color.copy(chalk).lerp(high,clamp((h+250)/1200)).lerp(lake,clamp((-h-390)/30)*.8);colors.set([color.r,color.g,color.b],k*3);}
   geometry.setAttribute('color',new T.BufferAttribute(colors,3));geometry.computeVertexNormals();material=new T.MeshStandardMaterial({vertexColors:true,roughness:1});scene.add(new T.Mesh(geometry,material));
   const world=(lat:number,lon:number)=>new T.Vector3((lon-data.anchor.lon)*111320*Math.cos(data.anchor.lat*Math.PI/180),150,(data.anchor.lat-lat)*111320);
   update.current=(p:number)=>{if(!renderer||!host.current)return;const w=host.current.clientWidth,h=host.current.clientHeight;if(w<1||h<1)return;renderer.setSize(w,h,false);camera.aspect=w/Math.max(1,h);camera.updateProjectionMatrix();const pan=reduced?1:clamp(p/.16),distance=(w<650?49000:37000)-pan*3500;camera.position.set(distance*.57,distance*.76,distance*.70-5000);camera.lookAt(0,0,-4400);camera.updateMatrixWorld();setPositions(candidates.map(c=>{const point=world(c.lat,c.lon).project(camera);return {x:(point.x+1)*w/2,y:(1-point.y)*h/2};}));renderer.render(scene,camera);};
   observer=new ResizeObserver(()=>update.current?.(current.current));observer.observe(host.current);update.current(current.current);
  }catch(error){if(!stopped&&!controller.signal.aborted)setFailed(true);}}
  void mount();return()=>{stopped=true;controller.abort();observer?.disconnect();renderer?.dispose();geometry?.dispose();material?.dispose();host.current?.replaceChildren();update.current=null;};
 },[reduced]);
 useEffect(()=>update.current?.(progress),[progress]);
 return <div className="story-regional-map" data-ready={positions.length===3} data-precision="regional" role="img" aria-label="Judean Desert relief map. Twin Cave is proposed near Qumran; IV/17 and IV/11 near Jericho. Pins indicate regions, not registered cave mouths.">
  <div className="story-regional-canvas" ref={host}/>
  {failed&&<svg className="story-regional-fallback" viewBox="0 0 1000 500"><path d="M100 75L390 20L570 110L680 285L900 410L650 470L370 350L160 290Z" fill="#d9d3c5"/>{Array.from({length:18},(_,i)=><path key={i} d={`M120 ${90+i*12}Q420 ${10+i*14} 620 ${230+i*10}T900 ${420+i*3}`} fill="none" stroke="#a7a18e" opacity=".45"/>)}<path d="M670 260L900 410L770 460L640 330Z" fill="#91aaa6"/></svg>}
  {candidates.map((candidate,i)=>{const position=positions[i]??{x:(i?48:63)*((host.current?.clientWidth??700)/100),y:(i?30:67)*((host.current?.clientHeight??450)/100)},offset=(host.current?.clientWidth??700)<360?.72:1,amount=reduced?1:clamp((progress-(.25+i*.05))/.04),drop=(1-amount)**2*75;return <div key={candidate.name} className="story-regional-pin" data-site={candidate.name} data-dropped={amount===1} style={{left:position.x,top:position.y,opacity:amount}}>
   <span className="story-regional-area"/>
   <svg className="story-pin-leader" width="180" height="130" viewBox="-90 -70 180 130"><path d={`M0 0L${candidate.dx*offset} ${candidate.dy}`} fill="none" stroke="#93613f" strokeDasharray="3 4"/></svg>
   <div className="story-pin-content" style={{transform:`translate(${candidate.dx*offset}px,${candidate.dy-drop}px)`}}><svg viewBox="0 0 30 42" width="25" height="35" aria-hidden="true"><path d="M15 40C12 31 2 23 2 15a13 13 0 1 1 26 0c0 8-10 16-13 25Z" fill="#9b613c" stroke="#f7f5ef" strokeWidth="1.5"/><circle cx="15" cy="15" r="4" fill="#f2e5c9"/></svg><span className="story-pin-name">{candidate.name}</span><span className="story-pin-area">{candidate.area}</span></div>
  </div>;})}

 </div>;
}
