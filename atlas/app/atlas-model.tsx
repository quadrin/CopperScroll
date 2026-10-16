"use client";
import { useEffect, useRef, useState } from "react";
import * as T from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { Maximize2, Minus, Plus, RotateCcw, Scan, Layers, Move, Orbit } from "lucide-react";
import { buildModel, type ModelCamera, type ModelGeometry } from "./atlas-model-geometry";
import type { SitePlan } from "./atlas-explorer-model";
import "./atlas-model.css";

type Props={plan:SitePlan;featureId:string|null;onFeature:(id:string|null)=>void;camera?:ModelCamera;onCamera:(camera:ModelCamera)=>void;restoreNonce:number;onSource:()=>void};
type Runtime={render:()=>void;fit:()=>void;top:()=>void;zoom:(amount:number)=>void;controls:OrbitControls;camera:T.OrthographicCamera;model:ModelGeometry;renderer:T.WebGLRenderer};
export default function ArchitecturalModel(p:Props){
 const host=useRef<HTMLDivElement>(null),stage=useRef<HTMLDivElement>(null),runtime=useRef<Runtime|null>(null);
 const pins=useRef(new Map<string,HTMLButtonElement>()), callbacks=useRef(p);callbacks.current=p;
 const focused=useRef<string|null|undefined>(undefined),restoreSeen=useRef(p.restoreNonce);
 const [error,setError]=useState(false),[ready,setReady]=useState(false),[cutaway,setCutaway]=useState(true),[top,setTop]=useState(false),[navigation,setNavigation]=useState<"pan"|"orbit">(p.camera?.navigation??"pan");
 const [info,setInfo]=useState<{note:string;assumptions:string[];context?:string;credit?:string;mapped?:boolean}>({note:"Opening the architectural model…",assumptions:[]});
 useEffect(()=>{
  const el=host.current;if(!el)return;setReady(false);setError(false);setCutaway(true);setTop(false);setNavigation(p.camera?.navigation??"pan");
  let renderer:T.WebGLRenderer;
  try{renderer=new T.WebGLRenderer({antialias:true,alpha:true,powerPreference:"low-power"});}catch{setError(true);return;}
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;el.appendChild(renderer.domElement);
  const scene=new T.Scene(),model=buildModel(p.plan);scene.add(model.root);
  setInfo({note:model.note,assumptions:model.assumptions,...model.landscape});
  const box=model.framing,size=box.getSize(new T.Vector3()),span=Math.max(size.x,size.z),target=new T.Vector3(0,Math.max(0,size.y*.2),0);
  const camera=new T.OrthographicCamera(-span,span,span,-span,.01,span*16);camera.position.set(span*.95,span*.9,span*1.05);camera.lookAt(target);camera.zoom=1.3;
  focused.current=p.camera?p.featureId:undefined;restoreSeen.current=p.restoreNonce;
  const controls=new OrbitControls(camera,renderer.domElement);controls.target.copy(target);controls.enableDamping=false;controls.rotateSpeed=.45;controls.minPolarAngle=.025;controls.maxPolarAngle=Math.PI*.48;controls.minZoom=.45;controls.maxZoom=32;controls.screenSpacePanning=true;controls.enablePan=true;controls.zoomToCursor=true;
  const hemi=new T.HemisphereLight("#fff8e7","#89765b",1.35);scene.add(hemi);
  const sun=new T.DirectionalLight("#fff5dc",3.4);sun.position.set(-span*.4,span*1.8,span*.9);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-span;sun.shadow.camera.right=span;sun.shadow.camera.top=span;sun.shadow.camera.bottom=-span;sun.shadow.camera.near=.1;sun.shadow.camera.far=span*5;sun.shadow.normalBias=.08;sun.shadow.bias=-.0002;sun.shadow.radius=3;scene.add(sun);
  const fill=new T.DirectionalLight("#d8e4de",.85);fill.position.set(span,span*.6,-span);scene.add(fill);
  const shadow=new T.Mesh(new T.PlaneGeometry(span*5,span*5),new T.ShadowMaterial({color:"#514634",opacity:.14}));shadow.rotation.x=-Math.PI/2;shadow.position.y=box.min.y-.02;shadow.receiveShadow=true;scene.add(shadow);
  let width=1,height=1,fitZoom=1.3,firstSize=true;
  const save=()=>callbacks.current.onCamera({position:camera.position.toArray() as ModelCamera["position"],target:controls.target.toArray() as ModelCamera["target"],zoom:camera.zoom,up:camera.up.toArray() as ModelCamera["up"],navigation:controls.mouseButtons.LEFT===T.MOUSE.PAN?"pan":"orbit"});
  function render(){
   model.root.updateMatrixWorld(true);renderer.render(scene,camera);setTop(Math.hypot(camera.position.x-controls.target.x,camera.position.z-controls.target.z)/Math.max(.001,Math.abs(camera.position.y-controls.target.y))<.06);
   model.markers.forEach((position,id)=>{const pin=pins.current.get(id);if(!pin)return;const v=position.clone().project(camera);const x=(v.x*.5+.5)*width,y=(-v.y*.5+.5)*height;pin.style.transform=`translate(${x}px,${y}px) translate(-15px,-15px)`;pin.hidden=v.z>1||v.z< -1||x<8||x>width-8||y<8||y>height-8;});
   if(stage.current)stage.current.dataset.camera=`${camera.position.toArray().map(v=>v.toFixed(3)).join(",")}/${camera.zoom.toFixed(3)}`;
  }
  function fit(){camera.zoom=fitZoom;controls.target.copy(target);camera.position.set(span*.95,span*.9,span*1.05);camera.up.set(0,1,0);camera.updateProjectionMatrix();controls.update();setTop(false);render();save();}
  function resize(){const r=el!.getBoundingClientRect();width=Math.max(1,r.width);height=Math.max(1,r.height);const aspect=width/height,half=span*.63;camera.left=-half*Math.max(1,aspect);camera.right=half*Math.max(1,aspect);camera.top=half*Math.max(1,1/aspect);camera.bottom=-half*Math.max(1,1/aspect);camera.updateProjectionMatrix();const reference=camera.clone();reference.zoom=1;reference.position.set(span*.95,span*.9,span*1.05);reference.lookAt(target);reference.updateProjectionMatrix();reference.updateMatrixWorld();let reach=0;for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){const point=new T.Vector3(x,y,z).project(reference);reach=Math.max(reach,Math.abs(point.x),Math.abs(point.y));}fitZoom=Math.min(1.3,.9/Math.max(.01,reach));if(firstSize&&!p.camera){camera.zoom=fitZoom;camera.updateProjectionMatrix();}firstSize=false;renderer.setSize(width,height,false);render();}
  const rt:Runtime={model,camera,controls,renderer,render,fit,top:()=>{camera.position.set(controls.target.x,controls.target.y+span*2,controls.target.z+span*.05);camera.updateProjectionMatrix();controls.update();setTop(true);render();save();},zoom:amount=>{camera.zoom=T.MathUtils.clamp(camera.zoom*amount,.45,32);camera.updateProjectionMatrix();render();save();}};runtime.current=rt;
  controls.addEventListener("change",render);controls.addEventListener("end",save);
  const observer=new ResizeObserver(resize);observer.observe(el);resize();
  if(p.camera){camera.position.fromArray(p.camera.position);camera.up.set(0,1,0);camera.zoom=p.camera.zoom;controls.target.fromArray(p.camera.target);camera.updateProjectionMatrix();controls.update();render();}
  let pointer:{x:number;y:number}|null=null;
  const down=(e:PointerEvent)=>{pointer={x:e.clientX,y:e.clientY}};
  const up=(e:PointerEvent)=>{if(!pointer||Math.hypot(e.clientX-pointer.x,e.clientY-pointer.y)>5)return;pointer=null;const r=el.getBoundingClientRect(),ray=new T.Raycaster();ray.setFromCamera(new T.Vector2((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1),camera);const hit=ray.intersectObjects(model.selectable,true)[0];if(hit?.object.userData.featureId)callbacks.current.onFeature(hit.object.userData.featureId);};
  renderer.domElement.addEventListener("pointerdown",down);renderer.domElement.addEventListener("pointerup",up);
  setReady(true);
  return()=>{runtime.current=null;observer.disconnect();controls.dispose();renderer.domElement.removeEventListener("pointerdown",down);renderer.domElement.removeEventListener("pointerup",up);const textures=new Set<T.Texture>();scene.traverse(object=>{const mesh=object as T.Mesh;if(mesh.geometry)mesh.geometry.dispose();for(const mat of Array.isArray(mesh.material)?mesh.material:mesh.material?[mesh.material]:[]){const m=mat as T.MeshStandardMaterial;if(m.map)textures.add(m.map);mat.dispose();}});textures.forEach(t=>t.dispose());renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();};
 },[p.plan.id]);
 useEffect(()=>{const r=runtime.current;if(!r)return;r.controls.mouseButtons.LEFT=navigation==="pan"?T.MOUSE.PAN:T.MOUSE.ROTATE;r.controls.mouseButtons.RIGHT=navigation==="pan"?T.MOUSE.ROTATE:T.MOUSE.PAN;r.controls.touches.ONE=navigation==="pan"?T.TOUCH.PAN:T.TOUCH.ROTATE;r.controls.touches.TWO=T.TOUCH.DOLLY_PAN;},[navigation,ready]);
 useEffect(()=>{const r=runtime.current;if(!r)return;r.model.roof.visible=!cutaway;r.render();},[cutaway]);
 useEffect(()=>{const r=runtime.current;if(!r)return;const ids=new Set<T.Material>();r.model.root.traverse(o=>{const m=o as T.Mesh;if(!m.material)return;for(const mat of Array.isArray(m.material)?m.material:[m.material]){if(ids.has(mat))continue;ids.add(mat);const s=mat as T.MeshStandardMaterial;if(!s.emissive)continue;s.emissive.set(m.userData.featureId===p.featureId?"#815129":"#000000");s.emissiveIntensity=m.userData.featureId===p.featureId ? .17 : 0;}});if(restoreSeen.current!==p.restoreNonce){restoreSeen.current=p.restoreNonce;focused.current=p.featureId;}
  else if(p.featureId&&focused.current!==p.featureId&&ready){const point=r.model.markers.get(p.featureId);if(point){const offset=r.camera.position.clone().sub(r.controls.target);r.controls.target.copy(point);r.camera.position.copy(point.clone().add(offset));r.camera.zoom=Math.max(r.camera.zoom,2.1);r.camera.updateProjectionMatrix();r.controls.update();callbacks.current.onCamera({position:r.camera.position.toArray() as ModelCamera["position"],target:r.controls.target.toArray() as ModelCamera["target"],zoom:r.camera.zoom,up:r.camera.up.toArray() as ModelCamera["up"],navigation});}focused.current=p.featureId;}
  else if(ready)focused.current=p.featureId;
  r.render();},[p.featureId,ready,p.restoreNonce]);
 useEffect(()=>{const r=runtime.current;if(!r||!p.camera)return;r.camera.position.fromArray(p.camera.position);r.camera.up.set(0,1,0);r.camera.zoom=p.camera.zoom;setNavigation(p.camera.navigation??"pan");r.controls.target.fromArray(p.camera.target);r.camera.updateProjectionMatrix();r.controls.update();r.render();},[p.restoreNonce]);
 function key(e:React.KeyboardEvent){
  const r=runtime.current;if(!r||e.target!==e.currentTarget)return;
  const dirs:Record<string,[number,number]>={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,1],ArrowDown:[0,-1]};
  if(dirs[e.key]){e.preventDefault();const [x,y]=dirs[e.key];
   if(e.shiftKey){const offset=r.camera.position.clone().sub(r.controls.target);offset.applyAxisAngle(new T.Vector3(0,1,0),x*.12);r.camera.position.copy(offset.add(r.controls.target));}
   else{const right=new T.Vector3().setFromMatrixColumn(r.camera.matrix,0),up=new T.Vector3().setFromMatrixColumn(r.camera.matrix,1);const distance=(r.camera.top-r.camera.bottom)/r.camera.zoom*.07,move=right.multiplyScalar(x*distance).add(up.multiplyScalar(y*distance));r.camera.position.add(move);r.controls.target.add(move);}
   r.controls.update();r.render();callbacks.current.onCamera({position:r.camera.position.toArray() as ModelCamera["position"],target:r.controls.target.toArray() as ModelCamera["target"],zoom:r.camera.zoom,up:r.camera.up.toArray() as ModelCamera["up"],navigation});
  }else if(["+","="].includes(e.key)){e.preventDefault();r.zoom(1.2)}else if(e.key==="-"){e.preventDefault();r.zoom(1/1.2)}
 }

 return <div className="architectural-model" ref={stage} tabIndex={0} onKeyDown={key} role="region" aria-label={`Interactive 3D schematic of ${p.plan.label}`} data-ready={ready}>
  <div className="model-webgl" ref={host}/>
  <div className="model-kicker"><span>3D schematic</span><p>{info.note}</p></div>
  <div className="model-pins" aria-label="Model features">{p.plan.features.map((f,i)=><button key={f.id} ref={el=>{if(el)pins.current.set(f.id,el);else pins.current.delete(f.id)}} className={f.id===p.featureId?"active":""} aria-label={`Inspect ${f.label} in 3D`} aria-pressed={f.id===p.featureId} onClick={()=>p.onFeature(f.id)}><span>{i+1}</span>{f.id===p.featureId&&<strong>{f.label}</strong>}</button>)}</div>
  <div className="model-landscape-credit"><span>{info.context}</span>{info.mapped?<a href="https://mapterhorn.com/attribution/" target="_blank" rel="noreferrer">{info.credit}</a>:<small>{info.credit}</small>}</div>
  <div className="model-help">{navigation==="pan"?"Drag to pan · scroll or pinch to zoom · right-drag to rotate":"Drag to rotate · scroll or pinch to zoom · right-drag to pan"}</div>
  <div className="model-tools" aria-label="3D model controls">
   <button aria-label={navigation==="pan"?"Switch to rotate navigation":"Switch to map navigation"} aria-pressed={navigation==="orbit"} onClick={()=>{const next=navigation==="pan"?"orbit":"pan";setNavigation(next);const r=runtime.current;if(r)callbacks.current.onCamera({position:r.camera.position.toArray() as ModelCamera["position"],target:r.controls.target.toArray() as ModelCamera["target"],zoom:r.camera.zoom,up:r.camera.up.toArray() as ModelCamera["up"],navigation:next});}}>{navigation==="pan"?<Move size={16}/>:<Orbit size={16}/>}<span>{navigation==="pan"?"Pan":"Rotate"}</span></button>
   {p.plan.id==="abu-saraj-iv17"&&<button aria-pressed={cutaway} onClick={()=>setCutaway(v=>!v)}><Layers size={16}/>{cutaway?"Cutaway":"Roof"}</button>}
   <button aria-pressed={top} aria-label="Look down on model" onClick={()=>top?runtime.current?.fit():runtime.current?.top()}><Scan size={16}/><span>Top</span></button>
   <button aria-label="Zoom in 3D model" onClick={()=>runtime.current?.zoom(1.25)}><Plus size={17}/></button>
   <button aria-label="Zoom out 3D model" onClick={()=>runtime.current?.zoom(.8)}><Minus size={17}/></button>
   <button aria-label="Show whole site" onClick={()=>runtime.current?.fit()}><RotateCcw size={17}/></button>
  </div>
  <details className="model-assumptions"><summary>Model assumptions</summary>{info.assumptions.map(a=><p key={a}>{a}</p>)}<button onClick={p.onSource}><Maximize2 size={13}/>Compare source plan</button></details>
  {!ready&&!error&&<div className="model-loading" role="status">Opening 3D schematic…</div>}
  {error&&<div className="model-loading" role="alert"><p>3D rendering is unavailable in this browser.</p><button onClick={p.onSource}>Open source plan</button></div>}
 </div>;
}
