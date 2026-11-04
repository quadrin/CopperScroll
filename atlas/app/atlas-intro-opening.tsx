"use client";
import {useEffect,useRef,useState} from 'react';
import * as T from 'three';
import {Narration,useScrollScene} from './atlas-intro-motion';
import {AnimatedWords} from './atlas-intro-words';
import {sheetPoint,SHEET_LENGTH_M} from './atlas-scroll-3d-model';

type Grid={extent:number;size:number;elevations:number[];centreElevation:number};
type Terrain={anchor:{lat:number;lon:number};verticalExaggeration:number;regional:Grid;middle:Grid;local:Grid};
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const smooth=(v:number)=>{const t=clamp(v);return t*t*(3-2*t);};
const base=import.meta.env?.BASE_URL??'/';
export default function DesertOpening(){
 const timeline=useScrollScene(),host=useRef<HTMLDivElement>(null),qumran=useRef<HTMLSpanElement>(null),caveLabel=useRef<HTMLSpanElement>(null);
 const runtime=useRef<{update:(value:number)=>void}|null>(null),current=useRef(0);
 const [failed,setFailed]=useState(false),[ready,setReady]=useState(false);
 const value=timeline.reduced?0:timeline.value;current.current=value;
 useEffect(()=>{
  const element=host.current;if(!element)return;const el:HTMLDivElement=element;let disposed=false,renderer:T.WebGLRenderer|undefined,observer:ResizeObserver|undefined,disposeScene:(()=>void)|undefined;
  const controller=new AbortController();
  async function mount(){
   try{
    const response=await fetch(`${base}introduction/opening-terrain.json`,{signal:controller.signal});if(!response.ok)throw Error('Terrain unavailable');const data=await response.json() as Terrain;if(disposed)return;
    renderer=new T.WebGLRenderer({antialias:true,logarithmicDepthBuffer:true,powerPreference:'low-power'});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;el.appendChild(renderer.domElement);
    const scene=new T.Scene(),camera=new T.PerspectiveCamera(43,1,.015,120000);
    const background=new T.Color('#d9d6cd'),night=new T.Color('#181b15'),paper=new T.Color('#f7f5ef');scene.background=background;
    const fill=new T.DirectionalLight('#fffaf2',1.4);scene.add(fill);scene.add(fill.target);
    const ambient=new T.HemisphereLight('#fffdf7','#77776c',1.8);scene.add(ambient);
    const sun=new T.DirectionalLight('#fffaf3',3);sun.position.set(-13000,22000,17000);scene.add(sun);
    const terrainMat=new T.MeshStandardMaterial({vertexColors:true,roughness:1,flatShading:false,transparent:true});
    // World-space limestone grain; illustrative microdetail, not additional DEM data.
    terrainMat.onBeforeCompile=shader=>{
     shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 rockPosition;').replace('#include <begin_vertex>','#include <begin_vertex>\nrockPosition=position;');
     shader.fragmentShader=shader.fragmentShader.replace('#include <common>',`#include <common>
      varying vec3 rockPosition;
      float rockHash(vec3 p){return fract(sin(dot(p,vec3(127.1,311.7,74.7)))*43758.5453);}
      float rockNoise(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(rockHash(i),rockHash(i+vec3(1,0,0)),f.x),mix(rockHash(i+vec3(0,1,0)),rockHash(i+vec3(1,1,0)),f.x),f.y),mix(mix(rockHash(i+vec3(0,0,1)),rockHash(i+vec3(1,0,1)),f.x),mix(rockHash(i+vec3(0,1,1)),rockHash(i+vec3(1,1,1)),f.x),f.y),f.z);}
     `).replace('#include <color_fragment>',`#include <color_fragment>
      float grain=rockNoise(rockPosition*.16)*.5+rockNoise(rockPosition*.63)*.3+rockNoise(rockPosition*2.4)*.2;
      float strata=sin(rockPosition.y*.8+rockNoise(rockPosition*.07)*3.);
      diffuseColor.rgb*=.79+grain*.28+strata*.035;
     `);
    };
    const origin=data.local.centreElevation,exaggeration=data.verticalExaggeration;
    function sample(grid:Grid,x:number,z:number){
     const fx=clamp(x/grid.extent+.5)*(grid.size-1),fz=clamp(z/grid.extent+.5)*(grid.size-1),ix=Math.min(grid.size-2,Math.floor(fx)),iz=Math.min(grid.size-2,Math.floor(fz)),tx=fx-ix,tz=fz-iz;
     const at=(a:number,b:number)=>grid.elevations[b*grid.size+a];
     return T.MathUtils.lerp(T.MathUtils.lerp(at(ix,iz),at(ix+1,iz),tx),T.MathUtils.lerp(at(ix,iz+1),at(ix+1,iz+1),tx),tz);
    }
    // One nonuniform mesh, with denser vertices near the approach. Source DEM
    // resolutions blend in height, never as overlapping transparent surfaces.
    const n=innerWidth<760?385:513,terrainGeo=new T.PlaneGeometry(data.regional.extent,data.regional.extent,n-1,n-1);terrainGeo.rotateX(-Math.PI/2);
    const pos=terrainGeo.getAttribute('position') as T.BufferAttribute,colors=new Float32Array(n*n*3);
    const low=new T.Color('#c9c4b8'),high=new T.Color('#a5a18f'),lake=new T.Color('#728e8b'),color=new T.Color();
    for(let j=0;j<n;j++)for(let i=0;i<n;i++){
     const index=j*n+i,tx=i/(n-1)*2-1,tz=j/(n-1)*2-1,x=Math.sign(tx)*tx*tx*data.regional.extent/2,z=Math.sign(tz)*tz*tz*data.regional.extent/2,r=Math.max(Math.abs(x),Math.abs(z));
     let h=sample(data.regional,x,z);h=T.MathUtils.lerp(h,sample(data.middle,x,z),1-smooth((r-4500)/1200));h=T.MathUtils.lerp(h,sample(data.local,x,z),1-smooth((r-850)/350));
     pos.setXYZ(index,x,(h-origin)*exaggeration,z);color.copy(low).lerp(high,clamp((h+250)/1100)).lerp(lake,smooth((-h-390)/30)*.76);colors.set([color.r,color.g,color.b],index*3);
    }
    terrainGeo.setAttribute('color',new T.BufferAttribute(colors,3));pos.needsUpdate=true;terrainGeo.computeVertexNormals();const terrainMesh=new T.Mesh(terrainGeo,terrainMat);scene.add(terrainMesh);
    // Local architecture is illustrative. The DEM supplies geographical context,
    // not a surveyed cave mouth or the lost ancient cliff/chamber surfaces.
    const chamber=new T.Group();chamber.rotation.y=Math.PI/2;scene.add(chamber);
    const rockMaterials=['#a9a393','#bcb4a2','#858478','#c7c0af'].map(color=>new T.MeshStandardMaterial({color,roughness:1,flatShading:false,transparent:true}));
    rockMaterials.forEach(material=>{material.onBeforeCompile=terrainMat.onBeforeCompile;});
    // A contiguous, stratified rock surface around the opening avoids a box
    // or a ring of decorative boulders. All chamber detail remains illustrative.
    const rings=160,around=256,cliffPositions:number[]=[],cliffColors:number[]=[],cliffIndices:number[]=[];
    const cliffColor=new T.Color();
    for(let r=0;r<=rings;r++)for(let i=0;i<=around;i++){
     const angle=i/around*Math.PI*2,t=(r/rings)**2,ca=Math.cos(angle),sa=Math.sin(angle);
     const innerX=2.6*ca*(1+.05*Math.sin(angle*7)),innerY=1.85*sa*(1+.09*Math.sin(angle*5));
     const outerX=120*ca*(1+.08*Math.sin(angle*9)),outerY=70*sa*(1+.09*Math.sin(angle*6))+2;
     const x=T.MathUtils.lerp(innerX,outerX,t),y=T.MathUtils.lerp(innerY,outerY,t);
     const fine=1-smooth((Math.hypot(x,y)-5)/18);
     const strata=fine*(.018*Math.sin(y*8+x*.4)+.035*Math.sin(y*3-x*.27));
     const relief=fine*(.20*Math.sin(x*1.5+y*.7)+.10*Math.sin(x*4-y*2.8));
     const z=.8+.25*Math.sin(x*.14)+.18*Math.sin(y*.2)+relief+strata;
     cliffPositions.push(x,y,z);
     cliffColor.set('#b1aa99').multiplyScalar(.88+.06*Math.sin(y*1.3)+fine*.08*Math.sin(y*9));cliffColors.push(cliffColor.r,cliffColor.g,cliffColor.b);
     if(r<rings&&i<around){const a=r*(around+1)+i,c=a+around+1;cliffIndices.push(a,c,a+1,a+1,c,c+1);}
    }
    const cliffGeo=new T.BufferGeometry();cliffGeo.setAttribute('position',new T.Float32BufferAttribute(cliffPositions,3));cliffGeo.setAttribute('color',new T.Float32BufferAttribute(cliffColors,3));cliffGeo.setIndex(cliffIndices);cliffGeo.computeVertexNormals();
    rockMaterials[0].vertexColors=true;rockMaterials[0].color.set('#ffffff');rockMaterials[0].side=T.DoubleSide;
    const facade=new T.Mesh(cliffGeo,rockMaterials[0]);chamber.add(facade);
    const floorMat=new T.MeshStandardMaterial({color:'#827357',roughness:1,transparent:true,vertexColors:true});
    const floorGeo=new T.PlaneGeometry(48,28,60,40);floorGeo.rotateX(-Math.PI/2);const floorVertices=floorGeo.getAttribute('position') as T.BufferAttribute;
    const floorColors=new Float32Array(floorVertices.count*4);for(let i=0;i<floorVertices.count;i++){const x=floorVertices.getX(i),z=floorVertices.getZ(i);floorVertices.setY(i,.016*Math.sin(x*6+z*2)+.012*Math.sin(z*9));const shade=.53+.47*smooth((z+3)/7),alpha=1-smooth((Math.max(Math.abs(x)/24,Math.abs(z)/14)-.6)/.4);floorColors.set([shade,shade,shade,alpha],i*4);}floorGeo.setAttribute('color',new T.BufferAttribute(floorColors,4));floorGeo.computeVertexNormals();
    const floor=new T.Mesh(floorGeo,floorMat);floor.position.set(0,-1.59,-2);chamber.add(floor);
    const interiorMat=new T.MeshStandardMaterial({color:'#524c3b',roughness:1,flatShading:false,transparent:true,side:T.DoubleSide});
    const tunnel=new T.BufferGeometry(),tunnelPoints:number[]=[],tunnelIndices:number[]=[];
    for(let j=0;j<=45;j++)for(let i=0;i<=80;i++){
     const a=i/80*Math.PI*2,z=1-j/45*7.7,rough=1+.035*Math.sin(a*13+z*4)+.025*Math.sin(a*7-z*9);
     tunnelPoints.push(3.05*Math.cos(a)*rough,1.95*Math.sin(a)*rough,z);
     if(j<45&&i<80){const b=j*81+i,c=b+81;tunnelIndices.push(b,c,b+1,b+1,c,c+1);}
    }
    tunnel.setAttribute('position',new T.Float32BufferAttribute(tunnelPoints,3));tunnel.setIndex(tunnelIndices);tunnel.computeVertexNormals();chamber.add(new T.Mesh(tunnel,interiorMat));
    const rearGeo=new T.CircleGeometry(3.2,80);rearGeo.scale(1,.7,1);const rear=new T.Mesh(rearGeo,interiorMat);rear.position.z=-6.7;chamber.add(rear);
    const light=new T.PointLight('#ffe2b2',10,12,2);light.position.set(-.7,.4,-2.8);chamber.add(light);
    // Photographic inscription detail, reused as an illustrative repeating surface.
    // This preserves real Hebrew grooves; it is not a reconstruction of the columns.
    const manuscript=await new T.TextureLoader().loadAsync(`${base}scroll/strip13.webp`);
    if(disposed){manuscript.dispose();return;}
    const writingCanvas=document.createElement('canvas');writingCanvas.width=3072;writingCanvas.height=1024;
    const ink=writingCanvas.getContext('2d')!,image=manuscript.image as HTMLImageElement;
    for(let col=0;col<12;col++)ink.drawImage(image,image.width*.23,image.height*.045,image.width*.61,image.height*.76,col*256,0,256,1024);
    const writingTexture=new T.CanvasTexture(writingCanvas);writingTexture.colorSpace=T.SRGBColorSpace;writingTexture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
    const copper=new T.MeshStandardMaterial({map:writingTexture,bumpMap:writingTexture,bumpScale:.0008,metalness:.18,roughness:.88,color:'#b9b09f',side:T.DoubleSide});
    const roll=new T.Group(),stripGeometries:T.BufferGeometry[]=[];const segments=42;
    for(let strip=0;strip<23;strip++){
     const geometry=new T.BufferGeometry(),positions=new Float32Array((segments+1)*6),uvs=new Float32Array((segments+1)*4),indices:number[]=[];
     for(let i=0;i<=segments;i++){const u=(strip+i/segments)/23;uvs.set([u,0,u,1],i*4);if(i<segments){const a=i*2;indices.push(a,a+1,a+2,a+1,a+3,a+2);}}
     geometry.setAttribute('position',new T.BufferAttribute(positions,3));geometry.setAttribute('uv',new T.BufferAttribute(uvs,2));geometry.setIndex(indices);stripGeometries.push(geometry);roll.add(new T.Mesh(geometry,copper));
    }
    let previousShape=-1;
    function shapeRoll(unroll:number,gap:number){
     const shape=unroll+gap;if(shape===previousShape)return;previousShape=shape;
     for(let strip=0;strip<23;strip++){
      const geometry=stripGeometries[strip],positions=geometry.getAttribute('position') as T.BufferAttribute;
      for(let i=0;i<=segments;i++){const u=(strip+i/segments)/23*SHEET_LENGTH_M,[x,z]=sheetPoint(u,unroll,SHEET_LENGTH_M),cx=x-SHEET_LENGTH_M/2*(1-unroll)+(11-strip)*.018*gap;positions.setXYZ(i*2,cx,-.15,z);positions.setXYZ(i*2+1,cx,.15,z);}
      positions.needsUpdate=true;geometry.computeVertexNormals();geometry.computeBoundingSphere();
     }
    }
    shapeRoll(0,0);roll.position.set(0,-1.49,-4);roll.rotation.z=Math.PI/2;chamber.add(roll);
    const secondCopper=copper.clone();secondCopper.transparent=true;const second=roll.clone(true);second.traverse(child=>{if(child instanceof T.Mesh)child.material=secondCopper;});second.position.set(-.02,-1.49,-4.24);second.rotation.z=Math.PI/2+.08;chamber.add(second);
    const render=()=>{if(!disposed)renderer!.render(scene,camera);};
    const q=new T.Vector3((35.45941-data.anchor.lon)*111320*Math.cos(data.anchor.lat*Math.PI/180),15,(data.anchor.lat-31.74183)*111320);
    function label(node:HTMLSpanElement|null,position:T.Vector3,opacity:number){
     if(!node)return;const projected=position.clone().project(camera),visible=Math.abs(projected.x)<.88&&Math.abs(projected.y)<.88&&projected.z<1;
     node.style.opacity=String(visible?opacity:0);node.style.left=`${(projected.x+1)*50}%`;node.style.top=`${(1-projected.y)*50}%`;
    }
    function update(value:number){
     const p=Math.min(1,value/.62),story=clamp((value-.70)/.30),unroll=smooth((story-.625)/.22),gap=smooth((story-.845)/.155);
     const inside=smooth((p-.54)/.22),handoff=smooth((p-.945)/.055);
     if(p<=.54){
      const u=p/.54,d=44000*Math.pow(180/44000,u),angle=.85*(1-smooth(u));
      camera.position.set(d*Math.cos(angle),d*(.62-.12*u),d*Math.sin(angle));camera.lookAt(-4200*(1-smooth(u)),0,-1600*(1-smooth(u)));
     }else if(p<=.76){
      const u=(p-.54)/.22,d=180*Math.pow(1.8/180,u);camera.position.set(d,90*Math.pow(1-u,3)-.6*u,.2*Math.sin(Math.PI*u));camera.lookAt(-4*smooth(u),-1.42*smooth(u),0);
     }else{
      const u=smooth((p-.76)/.19),closeDistance=Math.max(.7,.5/camera.aspect);camera.position.set(T.MathUtils.lerp(1.8,-4+closeDistance,u),T.MathUtils.lerp(-.6,-1.42+.24*(closeDistance/.7),u),T.MathUtils.lerp(0,.1,u));camera.lookAt(-4,-1.42,0);
     }
     if(value>.62){
      const shrink=smooth((value-.62)/.08),closeDistance=Math.max(.7,.5/camera.aspect),framedDistance=Math.max(1.2,.65/camera.aspect),openDistance=Math.max(framedDistance,2.9/(2*Math.tan(43*Math.PI/360)*camera.aspect));
      const distance=T.MathUtils.lerp(T.MathUtils.lerp(closeDistance,framedDistance,shrink),openDistance,unroll);
      camera.position.set(-4+distance,-1.42+.25*distance,.1);camera.lookAt(-4,-1.42-.10*distance*shrink,0);
     }
     shapeRoll(unroll,gap);terrainMat.opacity=1-smooth((p-.46)/.08);terrainMat.depthWrite=terrainMat.opacity>.98;terrainMesh.visible=terrainMat.opacity>.001;
     const rockOpacity=smooth((p-.43)/.11)*(1-handoff);rockMaterials.forEach(m=>{m.opacity=rockOpacity;m.depthWrite=rockOpacity>.98;});floorMat.opacity=rockOpacity*smooth((p-.64)/.08);interiorMat.opacity=rockOpacity;floorMat.depthWrite=floorMat.opacity>.98;interiorMat.depthWrite=rockOpacity>.98;
     facade.visible=rockOpacity>.001;chamber.children.forEach(child=>{if(child instanceof T.Mesh)child.visible=rockOpacity>.001;});floor.visible=floorMat.opacity>.001;
     secondCopper.opacity=1-handoff;roll.rotation.z=(1-handoff)*Math.PI/2;roll.position.y=T.MathUtils.lerp(-1.49,-1.42,handoff);
     ambient.intensity=T.MathUtils.lerp(1.8,.4,inside)+handoff*1.3;sun.intensity=T.MathUtils.lerp(3,.12,inside)+handoff*2.7;light.intensity=10*(1-handoff);
     fill.position.copy(camera.position);fill.target.position.set(-4,-1.42,0);fill.intensity=handoff*1.8;
     background.set('#d9d6cd').lerp(night,inside).lerp(paper,handoff);camera.updateMatrixWorld();
     label(qumran.current,q,1-smooth((p-.25)/.12));label(caveLabel.current,new T.Vector3(0,3.7,0),smooth((p-.4)/.08)*(1-smooth((p-.58)/.08)));
     render();
    }
    runtime.current={update};observer=new ResizeObserver(()=>{if(!renderer)return;const w=el.clientWidth,h=el.clientHeight;renderer.setSize(w,h);camera.aspect=w/Math.max(1,h);camera.updateProjectionMatrix();update(current.current);});observer.observe(el);
    const contextLost=(event:Event)=>{event.preventDefault();setFailed(true);};renderer.domElement.addEventListener('webglcontextlost',contextLost);
    disposeScene=()=>{renderer?.domElement.removeEventListener('webglcontextlost',contextLost);terrainGeo.dispose();facade.geometry.dispose();floor.geometry.dispose();chamber.traverse(child=>{if(child instanceof T.Mesh&&!stripGeometries.includes(child.geometry)&&child!==facade&&child!==floor)child.geometry.dispose();});stripGeometries.forEach(g=>g.dispose());manuscript.dispose();writingTexture.dispose();[terrainMat,...rockMaterials,floorMat,interiorMat,copper,secondCopper].forEach(m=>m.dispose());};
    update(current.current);setReady(true);
   }catch(error){if(!disposed&&!controller.signal.aborted)setFailed(true);}
  }
  void mount();return()=>{disposed=true;controller.abort();observer?.disconnect();disposeScene?.();renderer?.dispose();el.replaceChildren();runtime.current=null;};
 },[]);
 useEffect(()=>runtime.current?.update(value),[value,ready]);
 const flight=Math.min(1,value/.62),story=clamp((value-.70)/.30),phase=flight<.36?'desert':flight<.6?'approach':flight<.82?'cave':story<.625?'scroll':story<.845?'unroll':'strips';
 const discoveryLines=['In 1952, excavators entered Qumran Cave 3.','Inside lay two rolls of copper.','A document was engraved into the metal.','It became known as the Copper Scroll.','Corrosion had made it too brittle to unwind.','In Manchester in 1955–56, Baker cut it into 23 strips.','The writing filled twelve columns.','It listed hidden valuables—and directions to them.'];
 return <div className="story-opening" ref={timeline.ref} data-progress={value.toFixed(3)} data-phase={phase} data-ready={ready} data-object="continuous-scroll" data-surface="photographic-hebrew" data-reduced={timeline.reduced}>
  <div className="story-opening-sticky">
   <div className="story-opening-canvas" ref={host} role="img" aria-label="Scroll-driven journey across relief terrain of the Judean Desert to Qumran Cave 3, then inside an illustrative cave to the rolled Copper Scroll."/>
   {failed&&<div className="story-opening-fallback"><svg viewBox="0 0 1000 650" role="img" aria-label="Illustrative relief of desert ridges descending towards Qumran and the Dead Sea"><rect width="1000" height="650" fill="#ded6c5"/>{Array.from({length:18},(_,i)=><path key={i} d={`M-80 ${80+i*31}L210 ${-50+i*29} 400 ${100+i*24} 570 ${130+i*22} 680 ${270+i*15} 1080 ${340+i*15}`} fill="none" stroke={i%3?'#b9a888':'#8e866b'} strokeWidth={i%3?12:22}/>)}<path d="M800 280Q730 400 860 650H1000V250Z" fill="#718b89"/></svg></div>}
   <div className="story-opening-wash" style={{opacity:1-smooth(flight/.23)}}/>
   <h1 aria-label="What is the Copper Scroll?" style={{opacity:1-smooth((flight-.03)/.18),transform:`translateY(${-flight*80}px)`}}>What is the <br/><AnimatedWords text="Copper Scroll?" progress={smooth(flight/.12)} reduced={timeline.reduced}/></h1>
   <span className="story-opening-place" ref={qumran}>Qumran</span><span className="story-opening-place" ref={caveLabel}>Cave 3 · 3Q</span>
   {!timeline.reduced&&<div className="story-opening-copy" style={{opacity:smooth((value-.70)/.02)}} aria-hidden={value<.70}><Narration lines={discoveryLines} progress={story} /></div>}
   <span className="story-opening-down" style={{opacity:1-smooth(flight/.12)}} aria-hidden="true">↓</span>
  </div>
  {timeline.reduced&&<div className="story-opening-static-copy"><Narration lines={discoveryLines} progress={1} reduced/></div>}
 </div>;
}
