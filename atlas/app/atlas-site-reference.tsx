"use client";
import {useEffect,useRef,useState} from 'react';
import {ExternalLink,Minus,Plus,RotateCcw,X} from 'lucide-react';
import LibraryReferences from './atlas-library-references';
import {plansForPlace,type SiteFeature,type SitePlan,type Viewport} from './atlas-explorer-model';
import type {Place} from './atlas-types';
import EntryText from './atlas-text';
import './atlas-site-reference.css';

const base=import.meta.env?.BASE_URL??'/';
const fit:Viewport={x:0,y:0,zoom:1};
const clamp=(n:number)=>Math.max(1,Math.min(32,n));
type Props={plan:SitePlan;place:Place|null;featureId:string|null;viewport:Viewport;restoreNonce:number;onViewport:(v:Viewport)=>void;onFeature:(id:string|null)=>void;onPlan:(id:string)=>void;onRead:(id:string)=>void};

function Passage({entryId,onRead}:{entryId:string;onRead:(id:string)=>void}){
 const [open,setOpen]=useState(false);
 return <details className="reference-passage" onToggle={event=>setOpen(event.currentTarget.open)}><summary>Scroll passage · Entry {entryId}</summary>{open&&<EntryText entryId={entryId} onOpenScroll={()=>onRead(entryId)}/>}</details>;
}
function FeatureNote({feature,onRead}:{feature:SiteFeature;onRead:(id:string)=>void}){
 return <article className="reference-feature-note" aria-label={`Details: ${feature.label}`}><span className="reference-kind">{feature.kind}</span><h3>{feature.label}</h3><p>{feature.description}</p><details><summary>Interpretation &amp; sources</summary><p>{feature.limit}</p><ul>{feature.sources.map(source=><li key={source}>{source}</li>)}</ul><a href={feature.sourceUrl} target="_blank" rel="noreferrer">Original evidence record <ExternalLink size={12}/></a></details>{feature.entryIds.map(entryId=><Passage key={entryId} entryId={entryId} onRead={onRead}/>)}</article>;
}

// Source information belongs to the atlas panel. This component has no route,
// viewer switch, independent model canvas or mobile inspector drawer.
export default function SiteReference(p:Props){
 const {plan,place,featureId}=p,feature=plan.features.find(f=>f.id===featureId);
 const stage=useRef<HTMLDivElement>(null),svg=useRef<SVGSVGElement>(null),note=useRef<HTMLDivElement>(null);
 const [camera,setCamera]=useState(p.viewport),[imageError,setImageError]=useState(false),[size,setSize]=useState({width:500,height:320});
 const current=useRef(camera);current.current=camera;
 const drag=useRef<{pointers:Map<number,{x:number;y:number}>;origin:Viewport;start:{x:number;y:number};distance:number}|null>(null);
 const lastFeature=useRef<string|null>(null);
 const {width,height}=plan,alternatives=plansForPlace(place?.id??null),fitScale=Math.max(.01,Math.min(size.width/width,size.height/height));
 function update(value:Viewport){const next={...value,zoom:clamp(value.zoom)};current.current=next;setCamera(next);p.onViewport(next);}
 useEffect(()=>{const element=stage.current;if(!element)return;const observer=new ResizeObserver(([r])=>setSize({width:r.contentRect.width,height:r.contentRect.height}));observer.observe(element);return()=>observer.disconnect();},[]);
 useEffect(()=>{current.current=p.viewport;setCamera(p.viewport);},[p.viewport,p.restoreNonce]);
 useEffect(()=>{setImageError(false);lastFeature.current=null;},[plan.id]);
 useEffect(()=>{if(!feature||feature.id===lastFeature.current)return;lastFeature.current=feature.id;update({zoom:Math.max(current.current.zoom,2.4),x:width/2-feature.x,y:height/2-feature.y});note.current?.scrollIntoView({block:'nearest',behavior:'instant'});},[featureId,plan.id,p.restoreNonce]);
 useEffect(()=>{const element=stage.current;if(!element)return;const stop=(event:WheelEvent)=>event.preventDefault();element.addEventListener('wheel',stop,{passive:false});return()=>element.removeEventListener('wheel',stop);},[]);
 function zoom(factor:number){update({...current.current,zoom:current.current.zoom*factor});}
 function local(clientX:number,clientY:number){const rect=svg.current?.getBoundingClientRect();if(!rect)return{x:0,y:0};const scale=Math.min(rect.width/width,rect.height/height);return{x:(clientX-rect.left)/scale,y:(clientY-rect.top)/scale};}
 function release(event:React.PointerEvent<HTMLDivElement>){const d=drag.current;if(!d)return;d.pointers.delete(event.pointerId);if(!d.pointers.size)drag.current=null;else{const point=[...d.pointers.values()][0];drag.current={...d,origin:current.current,start:point,distance:0};}}
 return <section className="site-reference" aria-label={`${place?.shortName??plan.label} plan and features`}>
  {alternatives.length>1&&<div className="reference-plan-heading"><label>Source plan<select aria-label="Source plan" value={plan.id} onChange={event=>p.onPlan(event.target.value)}>{alternatives.map(item=><option key={item.id} value={item.id}>{item.label}</option>)}</select></label></div>}
  {place?.lat==null&&<p className="reference-location-note">Location not established. Explore the published plan here; no map position is assigned.</p>}
  <div ref={stage} className="site-stage" tabIndex={0} role="region" aria-label="Interactive site plan: drag to pan, plus or minus to zoom" data-zoom={camera.zoom.toFixed(3)} data-pan={`${camera.x.toFixed(2)},${camera.y.toFixed(2)}`}
   onKeyDown={event=>{if(event.target!==event.currentTarget)return;const moves:Record<string,[number,number]>={ArrowLeft:[30,0],ArrowRight:[-30,0],ArrowUp:[0,30],ArrowDown:[0,-30]};if(moves[event.key]){event.preventDefault();update({...camera,x:camera.x+moves[event.key][0]/camera.zoom,y:camera.y+moves[event.key][1]/camera.zoom});}else if(['+','='].includes(event.key)){event.preventDefault();zoom(1.25);}else if(event.key==='-'){event.preventDefault();zoom(.8);}}}
   onWheel={event=>zoom(event.deltaY<0?1.1:.9)}
   onPointerDown={event=>{if((event.target as Element).closest('button,[role=button]'))return;event.currentTarget.setPointerCapture(event.pointerId);const point=local(event.clientX,event.clientY);if(!drag.current)drag.current={pointers:new Map(),origin:current.current,start:point,distance:0};drag.current.pointers.set(event.pointerId,point);if(drag.current.pointers.size===2){const[a,b]=[...drag.current.pointers.values()];drag.current.distance=Math.hypot(a.x-b.x,a.y-b.y);drag.current.origin=current.current;}}}
   onPointerMove={event=>{const d=drag.current;if(!d?.pointers.has(event.pointerId))return;const point=local(event.clientX,event.clientY);d.pointers.set(event.pointerId,point);if(d.pointers.size===2){const[a,b]=[...d.pointers.values()];update({...d.origin,zoom:d.origin.zoom*Math.hypot(a.x-b.x,a.y-b.y)/Math.max(1,d.distance)});}else update({...d.origin,x:d.origin.x+(point.x-d.start.x)/d.origin.zoom,y:d.origin.y+(point.y-d.start.y)/d.origin.zoom});}}
   onPointerUp={release} onPointerCancel={release}>
   <svg ref={svg} viewBox={`0 0 ${width} ${height}`} aria-label={plan.label}>
    <defs><marker id="source-north" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="#526349"/></marker><pattern id="site-grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#b6b697" strokeOpacity=".18"/></pattern></defs>
    <rect width={width} height={height} fill={plan.image?'#fff':'#e8dec2'}/>
    <g transform={`translate(${width/2} ${height/2}) scale(${camera.zoom}) translate(${-width/2+camera.x} ${-height/2+camera.y})`}>
     {plan.image?<image href={`${base}${plan.image}`} width={width} height={height} onError={()=>setImageError(true)}/>:<><rect width={width} height={height} fill="url(#site-grid)"/><g transform={plan.transform}>{plan.shapes?.map((shape,i)=><path key={i} d={shape.d} className={`site-shape site-shape-${shape.kind}`} vectorEffect="non-scaling-stroke"/>)}</g></>}
     <g className="site-plan-annotations" aria-hidden="true">{plan.annotations?.map((a,i)=><text key={i} x={a.x} y={a.y}>{a.text}</text>)}{plan.north&&<g><path d={`M${plan.north.x} ${plan.north.y} l${plan.north.dx} ${plan.north.dy}`} markerEnd="url(#source-north)"/><text x={plan.north.x+plan.north.dx+8} y={plan.north.y+plan.north.dy}>N</text></g>}{plan.scale&&<g><path d={`M${plan.scale.x} ${plan.scale.y-5} v10 m0 -5 h${plan.scale.length} m0 -5 v10`}/><text x={plan.scale.x} y={plan.scale.y+25}>{plan.scale.label}</text></g>}</g>
     {plan.features.map((f,i)=><g key={f.id} role="button" tabIndex={0} aria-label={`Inspect ${f.label}`} aria-pressed={f.id===featureId} className={`site-object ${f.id===featureId?'active':''}`} onClick={()=>p.onFeature(f.id)} onKeyDown={event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();p.onFeature(f.id);}}}>
      <title>{f.label}</title><circle className="site-touch-target" cx={f.x} cy={f.y} r={22/(camera.zoom*fitScale)}/>{f.path&&<path d={f.path} className="site-feature-outline" vectorEffect="non-scaling-stroke"/>}
      <circle cx={f.x} cy={f.y} r={15/(camera.zoom*fitScale)} className="site-object-halo"/><circle cx={f.x} cy={f.y} r={9/(camera.zoom*fitScale)} className="site-object-dot"/><text x={f.x} y={f.y+3.5/(camera.zoom*fitScale)} fontSize={10/(camera.zoom*fitScale)} textAnchor="middle">{i+1}</text>{(f.id===featureId||camera.zoom>3.5)&&<text className="site-object-label" x={f.x+16/(camera.zoom*fitScale)} y={f.y+4/(camera.zoom*fitScale)} fontSize={11/(camera.zoom*fitScale)}>{size.width<500?f.label.slice(0,24)+(f.label.length>24?'…':''):f.label}</text>}
     </g>)}
    </g>
   </svg>
   {imageError&&<p className="reference-image-error">The source image could not load. <a href={`${base}${plan.image}`} target="_blank" rel="noreferrer">Open the original figure</a></p>}
   <div className="site-zoom-controls"><button aria-label="Zoom in site view" onClick={()=>zoom(1.3)} disabled={camera.zoom>=32}><Plus size={18}/></button><button aria-label="Zoom out site view" onClick={()=>zoom(1/1.3)} disabled={camera.zoom<=1}><Minus size={18}/></button><button aria-label="Fit site view" onClick={()=>update(fit)}><RotateCcw size={16}/></button></div>
  </div>
  <footer className="reference-plan-source"><strong>{plan.source}</strong><p>{plan.credit} {plan.sourceUrl&&<a href={plan.sourceUrl} target="_blank" rel="noreferrer">Original source</a>} {plan.licenseUrl&&<a href={plan.licenseUrl} target="_blank" rel="noreferrer">Licence</a>}</p><LibraryReferences planIds={[plan.id]} compact/><details><summary>Alignment &amp; scale</summary><p>{plan.limit}</p></details></footer>
  <div className="reference-features" aria-label="Structure details"><h3>Site features</h3><div className="site-feature-list" aria-label="Site structures">{plan.features.map((f,i)=><button key={f.id} aria-pressed={featureId===f.id} onClick={()=>p.onFeature(f.id)}><span>{i+1}</span><div><strong>{f.label}</strong><small>{f.kind}</small></div></button>)}</div>
   {feature&&<div ref={note}><button className="reference-clear-feature" onClick={()=>{lastFeature.current=null;p.onFeature(null);}}><X size={13}/>All features</button><FeatureNote key={feature.id} feature={feature} onRead={p.onRead}/></div>}
  </div>
 </section>;
}
