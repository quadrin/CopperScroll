import {LngLat,type Map} from 'maplibre-gl';
import type {MapSiteRuntime} from './atlas-map-site-layer';
export type WalkController={keys:Set<string>;reset:()=>void;stop:()=>void;position:()=>[number,number,number]};
export function startMapWalk(map:Map,site:MapSiteRuntime,onChange:(position:[number,number,number])=>void,start?:[number,number]):WalkController {
 const before={center:map.getCenter(),zoom:map.getZoom(),pitch:map.getPitch(),bearing:map.getBearing(),padding:map.getPadding(),elevation:map.getCenterElevation()};
 const maxZoom=map.getMaxZoom(),maxPitch=map.getMaxPitch(),clamped=map.getCenterClampedToGround();
 // At eye level the site ground and sky fill this same canvas. Suspend regional
 // tiles: looking above the horizon can otherwise ask the geographic tile
 // cover for unsupported zoom levels. Restore each layer's own visibility.
 const regionalLayers=map.getStyle().layers.filter(layer=>'source' in layer).map(layer=>({id:layer.id,visibility:map.getLayoutProperty(layer.id,'visibility')??'visible'}));
 for(const layer of regionalLayers)map.setLayoutProperty(layer.id,'visibility','none');
 const handlers=[map.dragPan,map.dragRotate,map.scrollZoom,map.doubleClickZoom,map.touchZoomRotate,map.keyboard];const enabled=handlers.map(h=>h.isEnabled());handlers.forEach(h=>h.disable());
 map.stop();map.setMaxZoom(25);map.setMaxPitch(145);map.setCenterClampedToGround(false);
 const keys=new Set<string>(),canvas=map.getCanvas();let x=0,z=site.span*.58,height=1.7,bearing=0,pitch=86,drag:{x:number;y:number;id:number}|null=null,frame=0,previous=performance.now();
 function apply(){const from=site.location(x,z),ahead=site.location(x+Math.sin(bearing*Math.PI/180)*20,z-Math.cos(bearing*Math.PI/180)*20);const base=site.baseElevation()+.2+site.groundHeight(x,z);
  const options=map.calculateCameraOptionsFromTo(new LngLat(...from),base+height,new LngLat(...ahead),base+height-Math.tan((90-pitch)*Math.PI/180)*20);
  canvas.dataset.walkPosition=[x,height,z].map(n=>n.toFixed(3)).join(',');map.jumpTo({...options,padding:{top:0,bottom:0,left:0,right:0}});canvas.dataset.walkPitch=map.getPitch().toFixed(2);onChange([x,height,z]);
 }
 function reset(){height=1.7;bearing=0;pitch=86;
  if(start){[x,z]=site.local(...start);bearing=before.bearing;}
  else if(site.model.walkStart){[x,z]=site.model.walkStart.position;bearing=site.model.walkStart.bearing;pitch=site.model.walkStart.pitch;}
  else{const entrance=site.model.markers.get('D')??site.model.markers.get('north-mouth');x=entrance?.x??0;z=entrance?entrance.z+10:site.span*.35;}apply();}
 const down=(e:PointerEvent)=>{if(e.button!==0)return;canvas.focus();canvas.setPointerCapture(e.pointerId);drag={x:e.clientX,y:e.clientY,id:e.pointerId};};
 const move=(e:PointerEvent)=>{if(!drag||drag.id!==e.pointerId)return;bearing+=(e.clientX-drag.x)*.23;pitch=Math.max(25,Math.min(145,pitch+(e.clientY-drag.y)*.16));drag={x:e.clientX,y:e.clientY,id:e.pointerId};apply();};
 const up=(e:PointerEvent)=>{drag=null;if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);};
 const keydown=(e:KeyboardEvent)=>{if((e.target as HTMLElement).closest('input,select,textarea,button'))return;if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','shift'].includes(e.key.toLowerCase())){e.preventDefault();keys.add(e.key.toLowerCase());}};
 const keyup=(e:KeyboardEvent)=>keys.delete(e.key.toLowerCase()),blur=()=>keys.clear();
 canvas.addEventListener('pointerdown',down);canvas.addEventListener('pointermove',move);canvas.addEventListener('pointerup',up);canvas.addEventListener('pointercancel',up);canvas.addEventListener('keydown',keydown);window.addEventListener('keyup',keyup);window.addEventListener('blur',blur);
 function tick(now:number){const dt=Math.min((now-previous)/1000,.05);previous=now;let forward=0,right=0;if(keys.has('w')||keys.has('arrowup'))forward++;if(keys.has('s')||keys.has('arrowdown'))forward--;if(keys.has('d')||keys.has('arrowright'))right++;if(keys.has('a')||keys.has('arrowleft'))right--;if(forward||right){const b=bearing*Math.PI/180,speed=(keys.has('shift')?4:1.6)*dt/Math.max(1,Math.hypot(forward,right));x+=(Math.sin(b)*forward+Math.cos(b)*right)*speed;z+=(-Math.cos(b)*forward+Math.sin(b)*right)*speed;const limit=Math.max(site.span*1.5,30);x=Math.max(-limit,Math.min(limit,x));z=Math.max(-limit,Math.min(limit,z));apply();}frame=requestAnimationFrame(tick);}
 reset();frame=requestAnimationFrame(tick);canvas.focus();
 return {keys,reset,position:()=>[x,height,z],stop(){cancelAnimationFrame(frame);keys.clear();canvas.removeEventListener('pointerdown',down);canvas.removeEventListener('pointermove',move);canvas.removeEventListener('pointerup',up);canvas.removeEventListener('pointercancel',up);canvas.removeEventListener('keydown',keydown);window.removeEventListener('keyup',keyup);window.removeEventListener('blur',blur);handlers.forEach((h,i)=>{if(enabled[i])h.enable();});map.setCenterClampedToGround(clamped);map.setMaxZoom(maxZoom);map.setMaxPitch(maxPitch);map.jumpTo(before);for(const layer of regionalLayers)if(map.getLayer(layer.id))map.setLayoutProperty(layer.id,'visibility',layer.visibility);delete canvas.dataset.walkPosition;delete canvas.dataset.walkPitch;}};
}
