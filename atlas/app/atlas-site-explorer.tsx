"use client";
import { useEffect, useRef, useState } from "react";
import { ArrowLeft, BookOpen, Box, Camera, Footprints, ExternalLink, Map, Minus, Plus, RotateCcw, X } from "lucide-react";
import scenes from "./atlas-scenes.json";
import type { Entry, Place } from "./atlas-types";
import { plansForPlace, type SiteFeature, type SitePlan, type Viewport, type ModelCamera } from "./atlas-explorer-model";
import "./atlas-site-explorer.css";
import PerspectiveInspection from "./atlas-perspective";
import ArchitecturalModel from "./atlas-model";

const clamp = (n: number, low: number, high: number) => Math.min(high, Math.max(low, n));
const base = import.meta.env?.BASE_URL ?? "/";
type Props = { entry: Entry; place: Place | null; plan: SitePlan; featureId: string | null; highlightId?: string | null; onHighlight: (id: string) => void; view: "plan" | "photo"; representation?: "model" | "source" | "walk"; modelCamera?: ModelCamera; onModelCamera: (v: ModelCamera) => void; onRepresentation: (v: "model" | "source" | "walk") => void; viewport?: Viewport; photoViewport?: Viewport; restoreNonce: number; onViewport: (v: Viewport, photo: boolean) => void; onFeature: (id: string | null) => void; onPlan: (id: string) => void; onView: (view: "plan" | "photo") => void; onTerrain: () => void; onRead: (id: string) => void; onEnlarge: () => void; enlarged: boolean; onCloseEnlarged: () => void };
export function FeatureNote({ feature, onRead }: { feature: SiteFeature; onRead: (id: string) => void }) {
 return <div className="feature-note"><span className="site-kind">{feature.kind}</span><h3>{feature.label}</h3><p>{feature.description}</p><details><summary>Interpretation &amp; sources</summary><p>{feature.limit}</p><ul>{feature.sources.map(s => <li key={s}>{s}</li>)}</ul><a href={feature.sourceUrl} target="_blank" rel="noreferrer">Open evidence record <ExternalLink size={12}/></a></details><div className="feature-entry-links">{feature.entryIds.map(id => <button key={id} onClick={() => onRead(id)}><BookOpen size={14}/>Read entry {id}</button>)}</div></div>;
}
export default function SiteExplorer(p: Props) {
 const {plan, place, featureId, view} = p;
 const scene = scenes.find(s => s.placeId === place?.id);
 const feature = plan.features.find(f => f.id === featureId);
 const highlight = scene?.highlights.find(h=>h.id===p.highlightId);
 const photo = view === "photo";
 const walking=p.representation==="walk";
 const model = !photo && plan.kind !== "survey-map" && (p.representation ?? "model") !== "source";
 const stage = useRef<HTMLDivElement>(null);
 const svg = useRef<SVGSVGElement>(null);
 const drag = useRef<{ pointers: globalThis.Map<number,{x:number;y:number}>; origin: Viewport; start: {x:number;y:number}; distance: number } | null>(null);
 const fit = {x:0,y:0,zoom:1};
 const [camera, setCamera] = useState<Viewport>(photo ? p.photoViewport ?? fit : p.viewport ?? fit);
 const [imageError, setImageError] = useState(false);
 const [inspectorOpen,setInspectorOpen]=useState(!!feature);
 const sheetDrag=useRef<{y:number;moved:boolean}|null>(null);
 const ignoreSheetClick=useRef(false);
 const [size,setSize]=useState({width:650,height:300});
 const width = photo ? scene?.width ?? 1000 : plan.width;
 const height = photo ? scene?.height ?? 700 : plan.height;
 const fitScale=Math.max(.01,Math.min(size.width/width,size.height/height));
 useEffect(()=>{const el=stage.current;if(!el)return;const observer=new ResizeObserver(([r])=>setSize({width:r.contentRect.width,height:r.contentRect.height}));observer.observe(el);return()=>observer.disconnect()},[]);
 useEffect(()=>{setInspectorOpen(!!featureId||!!p.highlightId)},[featureId,p.highlightId]);
 const current = useRef(camera); current.current = camera;
 const lastFeature = useRef(featureId);
 const lastHighlight = useRef(p.highlightId);
 function update(v: Viewport) { const next = {...v,zoom:clamp(v.zoom,1,32)}; current.current=next;setCamera(next);p.onViewport(next,photo); }
 useEffect(() => { const next = (photo ? p.photoViewport : p.viewport) ?? fit;current.current=next;setCamera(next);lastFeature.current=featureId;setImageError(false); }, [plan.id,view,p.restoreNonce]); // History owns restored camera; drag changes only this surface.
 useEffect(() => {
  if(featureId === lastFeature.current) return; lastFeature.current=featureId;
  if(feature && !photo){const zoom=Math.max(current.current.zoom,2.4);update({zoom,x:width/2-feature.x,y:height/2-feature.y});}
 },[featureId,photo]);
 useEffect(()=>{if(p.highlightId===lastHighlight.current)return;lastHighlight.current=p.highlightId;if(photo&&highlight)update({zoom:Math.max(current.current.zoom,1.8),x:width/2-highlight.x*width/100,y:height/2-highlight.y*height/100})},[p.highlightId]);
 useEffect(()=>{const el=stage.current;if(!el)return;const stop=(event:WheelEvent)=>event.preventDefault();el.addEventListener("wheel",stop,{passive:false});return()=>el.removeEventListener("wheel",stop)},[]);
 function zoom(factor:number){update({...current.current,zoom:current.current.zoom*factor})}
 function local(clientX:number,clientY:number){const rect=svg.current?.getBoundingClientRect();if(!rect)return {x:0,y:0};const scale=Math.min(rect.width/width,rect.height/height);return {x:clientX/scale,y:clientY/scale};}
 function release(event: React.PointerEvent<HTMLDivElement>){drag.current?.pointers.delete(event.pointerId); if(drag.current?.pointers.size===0)drag.current=null;else if(drag.current){const point=[...drag.current.pointers.values()][0];drag.current={...drag.current,origin:current.current,start:point,distance:0};}}
 return <section className={`site-explorer ${p.enlarged?"site-media-enlarged":""}`} aria-label={`Explore ${place?.shortName ?? "candidate"} structures`}>
  <header className="site-explorer-head"><div><span className="small-caps">Explore candidate · entry {p.entry.id}</span><h2>{place?.shortName}</h2></div><div className="site-view-switch" role="group" aria-label="Site view">{plan.kind!=="survey-map"&&<button className="model-view-button" aria-pressed={model&&!walking} onClick={()=>{p.onRepresentation("model")}}><Box size={14}/>3D model</button>}{plan.kind!=="survey-map"&&<button aria-pressed={walking&&!photo} onClick={()=>p.onRepresentation("walk")}><Footprints size={14}/>Eye level</button>}<button aria-pressed={!photo&&!model} onClick={()=>{p.onRepresentation("source")}}><Map size={14}/>Source plan</button><button aria-pressed={photo} onClick={()=>p.onView("photo")}><Camera size={14}/>Photos</button><button onClick={p.onTerrain}>Regional terrain</button></div></header>
  <div className="site-explorer-body">
   <div className="site-canvas-column">
    {!photo && <div className="site-plan-selector"><label>Source plan <select aria-label="Source plan" value={plan.id} onChange={e=>p.onPlan(e.target.value)}>{plansForPlace(place?.id??null).map(item=><option key={item.id} value={item.id}>{item.label}</option>)}</select></label><span>{model?"Local model · up to 32× zoom · display assumptions below":"Drag to pan · up to 32× zoom · source resolution limits detail"}</span></div>}
    {model ? walking ? <PerspectiveInspection restoreNonce={p.restoreNonce} plan={plan} featureId={featureId} camera={p.modelCamera?.projection==="perspective"?p.modelCamera:undefined} onCamera={p.onModelCamera} onFeature={p.onFeature} onSource={()=>p.onRepresentation("source")}/> : <ArchitecturalModel plan={plan} featureId={featureId} onFeature={p.onFeature} camera={p.modelCamera?.projection==="perspective"?undefined:p.modelCamera} onCamera={p.onModelCamera} restoreNonce={p.restoreNonce} onSource={()=>p.onRepresentation("source")}/> : <div ref={stage} className="site-stage" tabIndex={0} role="region" aria-label={`${photo ? "Photograph" : "Interactive site plan"}: drag to pan, plus or minus to zoom`} data-zoom={camera.zoom.toFixed(3)} data-pan={`${camera.x.toFixed(2)},${camera.y.toFixed(2)}`}
     onKeyDown={e=>{if(e.target!==e.currentTarget)return;const moves:Record<string,[number,number]>={ArrowLeft:[30,0],ArrowRight:[-30,0],ArrowUp:[0,30],ArrowDown:[0,-30]};if(moves[e.key]){e.preventDefault();update({...camera,x:camera.x+moves[e.key][0]/camera.zoom,y:camera.y+moves[e.key][1]/camera.zoom})}else if(["+","="].includes(e.key)){e.preventDefault();zoom(1.25)}else if(e.key==="-"){e.preventDefault();zoom(.8)}}}
     onWheel={e=>zoom(e.deltaY<0?1.1:.9)}
     onPointerDown={e=>{if((e.target as Element).closest("button,[role=button]"))return;e.currentTarget.setPointerCapture(e.pointerId);const pt=local(e.clientX,e.clientY);if(!drag.current)drag.current={pointers:new globalThis.Map(),origin:camera,start:pt,distance:0};drag.current.pointers.set(e.pointerId,pt);if(drag.current.pointers.size===2){const [a,b]=[...drag.current.pointers.values()];drag.current.distance=Math.hypot(a.x-b.x,a.y-b.y);drag.current.origin=camera;}}}
     onPointerMove={e=>{const d=drag.current;if(!d?.pointers.has(e.pointerId))return;const pt=local(e.clientX,e.clientY);d.pointers.set(e.pointerId,pt);if(d.pointers.size===2){const[a,b]=[...d.pointers.values()];update({...d.origin,zoom:d.origin.zoom*Math.hypot(a.x-b.x,a.y-b.y)/Math.max(1,d.distance)})}else update({...d.origin,x:d.origin.x+(pt.x-d.start.x)/d.origin.zoom,y:d.origin.y+(pt.y-d.start.y)/d.origin.zoom});}}
     onPointerUp={release} onPointerCancel={release}>
     <svg ref={svg} viewBox={`0 0 ${width} ${height}`} aria-label={photo ? scene?.alt : plan.label}>
      <defs><marker id="source-north" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="#526349"/></marker><pattern id="site-grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#b6b697" strokeOpacity=".18"/></pattern></defs>
      <rect width={width} height={height} fill={photo?"#172b25":plan.image?"#fff":"#e8dec2"}/>
      <g transform={`translate(${width/2} ${height/2}) scale(${camera.zoom}) translate(${-width/2+camera.x} ${-height/2+camera.y})`}>
       {photo ? scene && <image href={scene.src} width={width} height={height} onError={()=>setImageError(true)}/> : plan.image ? <image href={`${base}${plan.image}`} width={width} height={height} onError={()=>setImageError(true)}/> : <><rect width={width} height={height} fill="url(#site-grid)"/><g transform={plan.transform}>{plan.shapes?.map((shape,i)=><path key={i} d={shape.d} className={`site-shape site-shape-${shape.kind}`} vectorEffect="non-scaling-stroke"/>)}</g></>}
       {!photo && <g className="site-plan-annotations" aria-hidden="true">
        {plan.annotations?.map((a,i)=><text key={i} x={a.x} y={a.y}>{a.text}</text>)}
        {plan.north&&<g><path d={`M${plan.north.x} ${plan.north.y} l${plan.north.dx} ${plan.north.dy}`} markerEnd="url(#source-north)"/><text x={plan.north.x+plan.north.dx+8} y={plan.north.y+plan.north.dy}>N</text></g>}
        {plan.scale&&<g><path d={`M${plan.scale.x} ${plan.scale.y-5} v10 m0 -5 h${plan.scale.length} m0 -5 v10`}/><text x={plan.scale.x} y={plan.scale.y+25}>{plan.scale.label}</text></g>}
       </g>}
       {!photo && plan.features.map((f,i)=><g key={f.id} role="button" tabIndex={0} aria-label={`Inspect ${f.label}`} aria-pressed={f.id===featureId} className={`site-object ${f.id===featureId?"active":""}`} onClick={()=>p.onFeature(f.id)} onKeyDown={e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();p.onFeature(f.id)}}}>
        <title>{f.label}</title><circle className="site-touch-target" cx={f.x} cy={f.y} r={22/(camera.zoom*fitScale)}/>
        {f.path&&<path d={f.path} className="site-feature-outline" vectorEffect="non-scaling-stroke"/>}
        <circle cx={f.x} cy={f.y} r={15/(camera.zoom*fitScale)} className="site-object-halo"/><circle cx={f.x} cy={f.y} r={9/(camera.zoom*fitScale)} className="site-object-dot"/><text x={f.x} y={f.y+3.5/(camera.zoom*fitScale)} fontSize={10/(camera.zoom*fitScale)} textAnchor="middle">{i+1}</text>{(f.id===featureId||camera.zoom>3.5)&&<text className="site-object-label" x={f.x+16/(camera.zoom*fitScale)} y={f.y+4/(camera.zoom*fitScale)} fontSize={11/(camera.zoom*fitScale)}>{size.width<600?f.label.slice(0,24)+(f.label.length>24?"…":""):f.label}</text>}
       </g>)}
       {photo && scene?.highlights.map((h,i)=><g className={`site-photo-region ${h.id===p.highlightId?"active":""}`} key={h.id} role="button" tabIndex={0} aria-label={`Inspect photo detail: ${h.label}`} aria-pressed={h.id===p.highlightId} onClick={()=>p.onHighlight(h.id)} onKeyDown={e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();p.onHighlight(h.id)}}}><polygon points={h.points.split(" ").map(pair=>{const[x,y]=pair.split(",").map(Number);return `${x*width/100},${y*height/100}`}).join(" ")} vectorEffect="non-scaling-stroke"/><text x={h.x*width/100} y={h.y*height/100} fontSize={Math.max(width/75,12)/camera.zoom}>{i+1} · {h.label}</text></g>)}
      </g>
     </svg>
     {photo&&!scene&&<div className="site-image-message"><Camera/><h3>No photograph for this candidate yet</h3><p>Its source plan and feature evidence remain available.</p><button onClick={()=>p.onView("plan")}>Return to site plan</button></div>}
     {imageError&&<div className="site-image-message"><p>The source image could not load.</p><a href={scene?.sourceUrl ?? `${base}${plan.image}`} target="_blank" rel="noreferrer">Open image source</a></div>}
     <div className="site-zoom-controls"><button aria-label="Zoom in site view" onClick={()=>zoom(1.3)} disabled={camera.zoom>=12}><Plus size={18}/></button><button aria-label="Zoom out site view" onClick={()=>zoom(1/1.3)} disabled={camera.zoom<=1}><Minus size={18}/></button><button aria-label="Fit site view" onClick={()=>update(fit)}><RotateCcw size={16}/></button>{photo&&scene&&<button aria-label="Enlarge photograph" onClick={p.onEnlarge}><ExternalLink size={16}/></button>}</div>
     {p.enlarged&&<button className="site-enlarged-close" onClick={p.onCloseEnlarged}><ArrowLeft size={16}/>Back to details</button>}
    </div>}
    <footer className="site-source-caption"><strong>{photo ? scene?.title ?? "Photographic coverage" : plan.source}</strong><span>{photo&&scene ? <>{scene.author} · <a href={scene.sourceUrl} target="_blank" rel="noreferrer">Source</a> · <a href={scene.licenseUrl} target="_blank" rel="noreferrer">{scene.license}</a>. {scene.caption}</> : <>{model?"Interactive schematic derived from the cited plan; display heights and simplified geometry are listed under Model assumptions.":plan.credit} {plan.sourceUrl&&<a href={plan.sourceUrl} target="_blank" rel="noreferrer">Original source</a>} {plan.licenseUrl&&<a href={plan.licenseUrl} target="_blank" rel="noreferrer">Licence</a>}</>}</span>{!photo&&<details><summary>Alignment &amp; scale</summary><p>{plan.limit}</p></details>}</footer>
   </div>
   <aside className="site-inspector" data-expanded={inspectorOpen} aria-label="Structure details"><button className="site-sheet-handle" aria-expanded={inspectorOpen} onPointerDown={e=>{e.currentTarget.setPointerCapture(e.pointerId);sheetDrag.current={y:e.clientY,moved:false}}} onPointerMove={e=>{if(!sheetDrag.current)return;const delta=e.clientY-sheetDrag.current.y;if(Math.abs(delta)>24){sheetDrag.current.moved=true;setInspectorOpen(delta<0)}}} onPointerUp={()=>{ignoreSheetClick.current=!!sheetDrag.current?.moved;sheetDrag.current=null}} onPointerCancel={()=>{sheetDrag.current=null}} onClick={()=>{if(ignoreSheetClick.current){ignoreSheetClick.current=false;return;}setInspectorOpen(v=>!v)}}>{inspectorOpen?"Minimize details":"Open structure details"}<span/></button>
    {photo&&highlight&&<div className="photo-selected-detail" aria-live="polite"><span className="site-kind">Visible photographic feature</span><h3>{highlight.label}</h3><p>{highlight.note}</p>{highlight.entryIds.map(id=><button key={id} onClick={()=>p.onRead(id)}>Read entry {id}</button>)}</div>}
    {feature ? <><button className="site-clear-feature" onClick={()=>p.onFeature(null)}><X size={13}/>All structures</button><FeatureNote feature={feature} onRead={p.onRead}/>{!photo&&<button className="site-photo-link" onClick={()=>p.onView("photo")}><Camera size={16}/>Inspect photographic context</button>}{photo&&scene&&<p className="site-photo-limit">This photograph shows {scene.title.toLowerCase()}. Its highlights describe visible context; the selected plan feature is not automatically registered to this image.</p>}</> : <><span className="site-kind">Explore the structures</span><h3>{photo?"Photographic context":"Select a feature"}</h3><p>{photo?scene?.caption??"Photographic coverage is pending.":`Select a numbered feature on the ${model?"model":"plan"}, or choose one below. The view focuses on it and opens its evidence and scroll passage here.`}</p></>}
    <div className="site-feature-list" aria-label="Site structures">{plan.features.map((f,i)=><button key={f.id} aria-pressed={featureId===f.id} onClick={()=>p.onFeature(f.id)}><span>{i+1}</span><div><strong>{f.label}</strong><small>{f.kind}</small></div></button>)}</div>
    {photo&&scene&&<details><summary>Visible photo details</summary>{scene.highlights.map(h=><div key={h.id}><h4>{h.label}</h4><p>{h.note}</p></div>)}</details>}
   </aside>
  </div>
 </section>;
}
