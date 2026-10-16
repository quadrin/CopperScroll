"use client";
import {useEffect,useRef,useState} from 'react';
import * as T from 'three';
import {buildModel} from './atlas-model-geometry';
import type {SitePlan,ModelCamera} from './atlas-explorer-model';
import './atlas-perspective.css';
type Props={plan:SitePlan;featureId:string|null;camera?:ModelCamera;restoreNonce:number;onCamera:(camera:ModelCamera)=>void;onFeature:(id:string|null)=>void;onSource:()=>void};
export default function PerspectiveInspection(p:Props){
 const host=useRef<HTMLDivElement>(null),stage=useRef<HTMLDivElement>(null),keys=useRef(new Set<string>());
 const runtime=useRef<{reset:()=>void;render:()=>void}|null>(null),latest=useRef(p);latest.current=p;
 const [error,setError]=useState(false),[ready,setReady]=useState(false),[assumptions,setAssumptions]=useState<string[]>([]);
 useEffect(()=>{
  const el=host.current;if(!el)return;setError(false);setReady(false);keys.current.clear();
  let renderer:T.WebGLRenderer;try{renderer=new T.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});}catch{setError(true);return;}
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;el.appendChild(renderer.domElement);
  const scene=new T.Scene(),model=buildModel(p.plan);scene.add(model.root);setAssumptions(model.assumptions);
  const bounds=model.framing,size=bounds.getSize(new T.Vector3()),span=Math.max(size.x,size.z),step=Math.max(.05,span*.08);
  const camera=new T.PerspectiveCamera(65,1,Math.max(.005,span/20000),span*30);camera.rotation.order='YXZ';
  scene.add(new T.HemisphereLight('#fff8e9','#87745b',2));const sun=new T.DirectionalLight('#fff5df',3);sun.position.set(-span,span*2,span);scene.add(sun);
  function save(){const target=camera.position.clone().add(camera.getWorldDirection(new T.Vector3()));latest.current.onCamera({position:camera.position.toArray() as ModelCamera['position'],target:target.toArray() as ModelCamera['target'],zoom:1,projection:'perspective'});}
  function render(){renderer.render(scene,camera);if(stage.current)stage.current.dataset.camera=camera.position.toArray().map(v=>v.toFixed(3)).join(',');}
  function reset(){const point=model.markers.get(latest.current.featureId||'')??model.markers.get('north-mouth');if(point){camera.position.set(point.x,point.y+(model.units==='metres'?.8:span*.04),point.z+span*.08);camera.lookAt(point.x,point.y,point.z-span*.1);}else{camera.position.set(size.x*.2,Math.max(1.3,size.y*.4),bounds.max.z+span*.12);camera.lookAt(0,Math.max(.5,size.y*.15),0);}camera.rotation.order='YXZ';render();save();}
  function resize(){const r=el!.getBoundingClientRect();renderer.setSize(Math.max(1,r.width),Math.max(1,r.height),false);camera.aspect=Math.max(1,r.width)/Math.max(1,r.height);camera.updateProjectionMatrix();render();}
  runtime.current={reset,render};const observer=new ResizeObserver(resize);observer.observe(el);resize();
  if(p.camera?.projection==='perspective'){camera.position.fromArray(p.camera.position);camera.lookAt(new T.Vector3(...p.camera.target));camera.rotation.order='YXZ';render();}else reset();
  let drag:{x:number;y:number;id:number}|null=null,moved=false;
  const down=(e:PointerEvent)=>{el.focus();stage.current?.focus({preventScroll:true});drag={x:e.clientX,y:e.clientY,id:e.pointerId};moved=false;renderer.domElement.setPointerCapture(e.pointerId);};
  const move=(e:PointerEvent)=>{if(!drag||drag.id!==e.pointerId)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>1)moved=true;camera.rotation.y-=dx*.004;camera.rotation.x=T.MathUtils.clamp(camera.rotation.x-dy*.004,-Math.PI*.47,Math.PI*.47);drag={x:e.clientX,y:e.clientY,id:e.pointerId};render();};
  const up=(e:PointerEvent)=>{if(!drag)return;drag=null;if(renderer.domElement.hasPointerCapture(e.pointerId))renderer.domElement.releasePointerCapture(e.pointerId);if(!moved){const r=el.getBoundingClientRect(),ray=new T.Raycaster();ray.setFromCamera(new T.Vector2((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1),camera);const hit=ray.intersectObjects(model.selectable,true)[0];if(hit?.object.userData.featureId)latest.current.onFeature(hit.object.userData.featureId);}save();};
  const wheel=(e:WheelEvent)=>{e.preventDefault();camera.position.addScaledVector(camera.getWorldDirection(new T.Vector3()),(e.deltaY<0?1:-1)*step*.25);render();save();};
  const stop=()=>keys.current.clear();const release=(e:KeyboardEvent)=>keys.current.delete(e.key.toLowerCase());
  for(const [type,fn] of [['pointerdown',down],['pointermove',move],['pointerup',up],['pointercancel',up]] as const)renderer.domElement.addEventListener(type,fn);
  renderer.domElement.addEventListener('wheel',wheel,{passive:false});window.addEventListener('blur',stop);window.addEventListener('keyup',release);
  let frame=0,last=performance.now(),wasMoving=false;
  function tick(now:number){const dt=Math.min((now-last)/1000,.06);last=now;const k=keys.current;const forward=new T.Vector3(-Math.sin(camera.rotation.y),0,-Math.cos(camera.rotation.y)),right=new T.Vector3(Math.cos(camera.rotation.y),0,-Math.sin(camera.rotation.y)),direction=new T.Vector3();
   if(k.has('w')||k.has('arrowup'))direction.add(forward);if(k.has('s')||k.has('arrowdown'))direction.sub(forward);if(k.has('d')||k.has('arrowright'))direction.add(right);if(k.has('a')||k.has('arrowleft'))direction.sub(right);if(k.has('r'))direction.y+=1;if(k.has('f'))direction.y-=1;
   const moving=direction.lengthSq()>0;if(moving){camera.position.addScaledVector(direction.normalize(),step*dt*(k.has('shift')?2:1));render();}else if(wasMoving)save();wasMoving=moving;frame=requestAnimationFrame(tick);
  }frame=requestAnimationFrame(tick);setReady(true);
  return()=>{cancelAnimationFrame(frame);runtime.current=null;keys.current.clear();observer.disconnect();window.removeEventListener('blur',stop);window.removeEventListener('keyup',release);for(const [type,fn] of [['pointerdown',down],['pointermove',move],['pointerup',up],['pointercancel',up]] as const)renderer.domElement.removeEventListener(type,fn);renderer.domElement.removeEventListener('wheel',wheel);scene.traverse(o=>{const m=o as T.Mesh;m.geometry?.dispose();for(const mat of Array.isArray(m.material)?m.material:m.material?[m.material]:[]){(mat as T.MeshStandardMaterial).map?.dispose();mat.dispose();}});renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();};
 },[p.plan.id,p.restoreNonce]);
 function press(e:React.KeyboardEvent){if((e.target as HTMLElement).closest('button,summary,select,input'))return;const k=e.key.toLowerCase();if(['w','a','s','d','r','f','arrowup','arrowdown','arrowleft','arrowright','shift'].includes(k)){e.preventDefault();keys.current.add(k);}}
 return <div className="architectural-model perspective-inspection" ref={stage} tabIndex={0} role="region" aria-label={`Eye-level simulation of ${p.plan.label}`} onKeyDown={press} onBlur={e=>{if(!e.currentTarget.contains(e.relatedTarget))keys.current.clear();}} data-ready={ready}>
  <div className="perspective-webgl" ref={host}/><div className="perspective-label"><strong>Eye-level simulation</strong><span>Free camera · illustrative geometry · floors and routes are unsurveyed.</span></div>
  <div className="perspective-help">Drag to look · W A S D / arrows to move · R / F up and down · scroll to move closer</div>
  <div className="perspective-controls" aria-label="Inspection camera movement">{[['w','Forward'],['a','Left'],['s','Back'],['d','Right'],['r','Up'],['f','Down']].map(([key,label])=><button key={key} onPointerDown={e=>{e.preventDefault();e.currentTarget.setPointerCapture(e.pointerId);keys.current.add(key);}} onPointerUp={()=>keys.current.delete(key)} onPointerCancel={()=>keys.current.delete(key)} onLostPointerCapture={()=>keys.current.delete(key)}>{label}</button>)}<button onClick={()=>runtime.current?.reset()}>Reset view</button></div>
  <details className="perspective-assumptions"><summary>Model sources & assumptions</summary>{assumptions.map(a=><p key={a}>{a}</p>)}<button onClick={p.onSource}>Compare source plan</button></details>
  {(!ready||error)&&<div className="model-loading" role={error?'alert':'status'}>{error?'3D rendering is unavailable.':'Opening perspective model…'}{error&&<button onClick={p.onSource}>Open source plan</button>}</div>}
 </div>;
}
