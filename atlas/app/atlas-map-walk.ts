import {LngLat,type Map} from 'maplibre-gl';
import {Vector3} from 'three';
import {WalkCharacter,WalkInput} from './atlas-walk-physics';
import type {MapSiteRuntime} from './atlas-map-site-layer';
export type WalkController={keys:Set<string>;press:(key:string)=>void;release:(key:string)=>void;toggleSprint:()=>void;toggleCrouch:()=>void;reset:()=>void;stop:()=>void;position:()=>[number,number,number];stance:()=>{sprinting:boolean;sprintEnabled:boolean;crouched:boolean;grounded:boolean}};
export function startMapWalk(map:Map,site:MapSiteRuntime,onChange:(position:[number,number,number])=>void,start?:[number,number]):WalkController {
 const before={center:map.getCenter(),zoom:map.getZoom(),pitch:map.getPitch(),bearing:map.getBearing(),padding:map.getPadding(),elevation:map.getCenterElevation()};
 const maxZoom=map.getMaxZoom(),maxPitch=map.getMaxPitch(),fov=map.getVerticalFieldOfView(),clamped=map.getCenterClampedToGround(),canvas=map.getCanvas();
 const input=new WalkInput();let bearing=0,pitch=86,phase=0,frame=0,previous=performance.now(),drag:{x:number;y:number;id:number}|null=null,blockedFrames=0,lastReport=0;
 function initial(){
  bearing=0;pitch=86;
  if(start){bearing=before.bearing;return site.local(...start);}
  if(site.model.walkStart){bearing=site.model.walkStart.bearing;pitch=site.model.walkStart.pitch;return site.model.walkStart.position;}
  const entrance=site.model.markers.get('D')??site.model.markers.get('north-mouth');return [entrance?.x??0,entrance?entrance.z+10:site.span*.35];
 }
 const at=initial(),body=new WalkCharacter(()=>site.collisionWorld(),new Vector3(at[0],0,at[1]));
 // Only enter the walking state after a full body fits on modeled ground.
 canvas.dataset.walkPosition=body.eye.toArray().join(',');
 const regionalLayers=map.getStyle().layers.filter(layer=>'source' in layer).map(layer=>({id:layer.id,visibility:map.getLayoutProperty(layer.id,'visibility')??'visible'}));
 for(const layer of regionalLayers)map.setLayoutProperty(layer.id,'visibility','none');
 const handlers=[map.dragPan,map.dragRotate,map.scrollZoom,map.doubleClickZoom,map.touchZoomRotate,map.keyboard],enabled=handlers.map(h=>h.isEnabled());handlers.forEach(h=>h.disable());
 map.stop();map.setMaxZoom(25);map.setMaxPitch(145);map.setCenterClampedToGround(false);map.setVerticalFieldOfView(65);
 function apply(force=false){
  const eye=body.eye,foot=body.feet,from=site.location(eye.x,eye.z),angle=bearing*Math.PI/180,ahead=site.location(eye.x+Math.sin(angle)*20,eye.z-Math.cos(angle)*20),altitude=site.baseElevation()+.2+eye.y;
  const options=map.calculateCameraOptionsFromTo(new LngLat(...from),altitude,new LngLat(...ahead),altitude-Math.tan((90-pitch)*Math.PI/180)*20);
  canvas.dataset.walkPosition=eye.toArray().map(n=>n.toFixed(3)).join(',');canvas.dataset.walkFeet=foot.toArray().map(n=>n.toFixed(3)).join(',');
  canvas.dataset.walkGrounded=String(body.grounded);canvas.dataset.walkSprint=String(body.sprinting);canvas.dataset.walkCrouch=String(body.crouched);canvas.dataset.walkBlocked=String(body.blocked);canvas.dataset.walkBlockedFrames=String(blockedFrames);canvas.dataset.walkSpeed=Math.hypot(body.velocity.x,body.velocity.z).toFixed(3);canvas.dataset.walkTriangles=String(site.collisionWorld().triangles);
  map.jumpTo({...options,padding:{top:0,bottom:0,left:0,right:0}});canvas.dataset.walkPitch=map.getPitch().toFixed(2);
  site.setWalker({feet:foot.toArray() as [number,number,number],bearing:angle,crouched:body.crouched,phase,moving:Math.hypot(body.velocity.x,body.velocity.z)>.1});
  if(force||performance.now()-lastReport>100){onChange(eye.toArray() as [number,number,number]);lastReport=performance.now();}
 }
 function reset(){input.clear();const at=initial();body.spawn(new Vector3(at[0],0,at[1]));phase=0;apply(true);}
 const look=(dx:number,dy:number)=>{bearing+=dx*.23;pitch=Math.max(25,Math.min(145,pitch+dy*.16));apply(true);};
 const down=(e:PointerEvent)=>{if(e.button!==0||document.pointerLockElement===canvas)return;canvas.focus();canvas.setPointerCapture(e.pointerId);drag={x:e.clientX,y:e.clientY,id:e.pointerId};};
 const move=(e:PointerEvent)=>{if(!drag||drag.id!==e.pointerId)return;look(e.clientX-drag.x,e.clientY-drag.y);drag={x:e.clientX,y:e.clientY,id:e.pointerId};};
 const up=(e:PointerEvent)=>{drag=null;if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);};
 const lockedLook=(e:MouseEvent)=>{if(document.pointerLockElement===canvas)look(e.movementX,e.movementY);};
 const lock=(e:MouseEvent)=>{if(!window.matchMedia('(hover: hover)').matches||!canvas.requestPointerLock)return;e.preventDefault();void Promise.resolve(canvas.requestPointerLock()).catch(()=>{});};
 const controls=['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','shift','control',' '];
 const keydown=(e:KeyboardEvent)=>{
  if(e.key==='Escape'&&document.pointerLockElement===canvas){e.stopPropagation();document.exitPointerLock();return;}
  if((e.target as HTMLElement).closest('input,select,textarea,button'))return;
  const key=e.key.toLowerCase();if(controls.includes(key)){e.preventDefault();if(!e.repeat)input.press(key);}else if(key==='r'){e.preventDefault();reset();}
 };
 const keyup=(e:KeyboardEvent)=>input.release(e.key.toLowerCase()),blur=()=>{input.clear();body.velocity.set(0,0,0);apply(true);};
 canvas.addEventListener('pointerdown',down);canvas.addEventListener('pointermove',move);canvas.addEventListener('pointerup',up);canvas.addEventListener('pointercancel',up);canvas.addEventListener('dblclick',lock);document.addEventListener('mousemove',lockedLook);document.addEventListener('keydown',keydown);window.addEventListener('keyup',keyup);window.addEventListener('blur',blur);
 function tick(now:number){
  const dt=Math.min((now-previous)/1000,.1);previous=now;const old=body.eye,oldStance=`${body.grounded}/${body.crouched}/${body.sprinting}`,intent=input.read(bearing*Math.PI/180);
  body.advance(dt,intent);if(body.blocked)blockedFrames++;phase+=Math.hypot(body.velocity.x,body.velocity.z)*dt*3;
  const stanceChanged=oldStance!==`${body.grounded}/${body.crouched}/${body.sprinting}`;
  if(body.eye.distanceToSquared(old)>1e-10||stanceChanged||intent.forward||intent.right||intent.jump)apply(stanceChanged);
  frame=requestAnimationFrame(tick);
 }
 apply(true);frame=requestAnimationFrame(tick);canvas.focus();
 return {keys:input.keys,press:key=>input.press(key),release:key=>input.release(key),toggleSprint:()=>{input.toggleSprint();apply(true);},toggleCrouch:()=>input.toggleCrouch(),reset,position:()=>body.eye.toArray() as [number,number,number],stance:()=>({sprinting:body.sprinting,sprintEnabled:input.sprintEnabled,crouched:body.crouched,grounded:body.grounded}),stop(){
  cancelAnimationFrame(frame);input.clear();if(document.pointerLockElement===canvas)document.exitPointerLock();site.setWalker(null);
  canvas.removeEventListener('pointerdown',down);canvas.removeEventListener('pointermove',move);canvas.removeEventListener('pointerup',up);canvas.removeEventListener('pointercancel',up);canvas.removeEventListener('dblclick',lock);document.removeEventListener('mousemove',lockedLook);document.removeEventListener('keydown',keydown);window.removeEventListener('keyup',keyup);window.removeEventListener('blur',blur);
  handlers.forEach((h,i)=>{if(enabled[i])h.enable();});map.setCenterClampedToGround(clamped);map.setMaxZoom(maxZoom);map.setMaxPitch(maxPitch);map.setVerticalFieldOfView(fov);map.jumpTo(before);
  for(const layer of regionalLayers)if(map.getLayer(layer.id))map.setLayoutProperty(layer.id,'visibility',layer.visibility);
  for(const key of Object.keys(canvas.dataset))if(key.startsWith('walk'))delete canvas.dataset[key];
 }};
}
