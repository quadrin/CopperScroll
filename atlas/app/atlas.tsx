"use client";
import { lazy, Suspense, useCallback, useEffect, useRef, useState } from "react";
import { ArrowLeft, BookOpen, ChevronDown, ExternalLink, FlaskConical, Layers, Map, Search, ScrollText, X } from "lucide-react";
import AtlasMap from "./atlas-map";
import EntryText from "./atlas-text";
import EvidenceReview from "./atlas-evidence";
import { EvidenceChips, EvidenceComponents, EvidenceLegend, strongestCandidate } from "./atlas-components";
import SiteExplorer, { FeatureNote } from "./atlas-site-explorer";
import data from "./atlas-data.json";
import ArchaeologyCatalog from "./atlas-archaeology";
import { explorerFromHash, explorerHash, initialExplorer, archaeologyForPlace, plansForPlace, sitePlans, type ExplorerState, type Camera, type Viewport } from "./atlas-explorer-model";
import type { Entry, Place } from "./atlas-types";
import "./atlas-revamp.css";
import "./atlas-unified.css";
const entries = data.entries as Entry[];
const places = data.places as Place[];
const byPlace = Object.fromEntries(places.map(p=>[p.id,p]));
const primaryPlace = (id:string)=>entries.find(e=>e.id===id)?.candidates[0]?.placeId??null;
const Workbench = lazy(()=>import("./atlas-workbench"));
const Dossier = lazy(()=>import("./atlas-dossier"));
const repo = "https://github.com/quadrin/CopperScroll/blob/main";
type HistoryState = ExplorerState & { enlarged?: boolean };

export default function Atlas(){
 const [state,setState] = useState<HistoryState>(()=>{if(typeof window==="undefined")return initialExplorer;const saved=window.history.state?.atlas;if(saved&&window.history.state.atlasVersion!==2&&["2d","3d"].includes(saved.mode))return archaeologyForPlace(saved.entryId,saved.placeId);return saved&&explorerHash(saved)===location.hash?saved:explorerFromHash(location.hash,primaryPlace)??initialExplorer});
 const current=useRef(state);
 const [depth,setDepth]=useState(0);
 const [restoreNonce,setRestoreNonce]=useState(0);
 const [mapRestore,setMapRestore]=useState<{camera?:Camera;nonce:number}>({nonce:0});
 const [focusNonce,setFocusNonce]=useState(0);
 const [browse,setBrowse]=useState(false);
 const [query,setQuery]=useState("");
 const [region,setRegion]=useState("all");
 const [notes,setNotes]=useState(false);
 const [more,setMore]=useState(false);
 const [layers,setLayers]=useState(false);
 const [about,setAbout]=useState(false);
 useEffect(()=>{function escape(event:KeyboardEvent){if(event.key!=="Escape")return;setBrowse(false);setNotes(false);setMore(false);setLayers(false);setAbout(false);}window.addEventListener("keydown",escape);return()=>window.removeEventListener("keydown",escape)},[]);
 const entry=entries.find(e=>e.id===state.entryId)??entries[0];
 const place=state.placeId?byPlace[state.placeId]??null:null;
 const plan=sitePlans.find(p=>p.id===state.planId)??plansForPlace(state.placeId)[0];
 const feature=plan?.features.find(f=>f.id===state.featureId);

 const matches=entries.filter(e=>(region==="all"||e.region===region)&&(!query||[e.id,e.title,e.hebrew,e.description,...e.candidates.map(c=>byPlace[c.placeId].name)].join(" ").toLowerCase().includes(query.toLowerCase())));
 const visibleIds=Array.from(new Set((query||region!=="all"?matches:entries).flatMap(e=>e.candidates.map(c=>c.placeId))));
 const saveSnapshot=useCallback((patch:Partial<HistoryState>)=>{
  current.current={...current.current,...patch};
  const h=window.history.state;
  if(h?.atlas)window.history.replaceState({...h,atlas:current.current,atlasVersion:2},"",location.href);
 },[]);
 const navigate=useCallback((patch:Partial<HistoryState>,replace=false)=>{
  const prev=current.current;
  const next={...prev,...patch};
  if(explorerHash(next)===explorerHash(prev)&&JSON.stringify(next)===JSON.stringify(prev))return;
  const h=window.history.state;
  window.history.replaceState({...h,atlas:prev,atlasDepth:h?.atlasDepth??0,atlasVersion:2},"",location.href);
  const nextDepth=replace?h?.atlasDepth??0:(h?.atlasDepth??0)+1;
  window.history[replace?"replaceState":"pushState"]({atlas:next,atlasDepth:nextDepth,atlasVersion:2},"",explorerHash(next));
  current.current=next;setState(next);setDepth(nextDepth);setBrowse(false);setMore(false);setLayers(false);
  if(next.entryId!==prev.entryId||next.placeId!==prev.placeId)setFocusNonce(n=>n+1);
  if(next.mode!==prev.mode||next.scrollPhoto!==prev.scrollPhoto)window.dispatchEvent(new Event("atlas:modechange"));
 },[]);
 useEffect(()=>{
  const existing=window.history.state;
  if(existing?.atlas&&existing.atlasVersion===2&&explorerHash(existing.atlas)===location.hash){current.current=existing.atlas;setState(existing.atlas);setDepth(existing.atlasDepth??0);setMapRestore({camera:existing.atlas.camera,nonce:1});}
  else window.history.replaceState({atlas:current.current,atlasDepth:0,atlasVersion:2},"",explorerHash(current.current));
  function restore(){
   const h=window.history.state;
   const restored=h?.atlas??explorerFromHash(location.hash,primaryPlace);
   if(!restored)return;
   if(!h?.atlas)window.history.replaceState({atlas:restored,atlasDepth:0,atlasVersion:2},"",location.href);
   current.current=restored;setState(restored);setDepth(h?.atlasDepth??0);setRestoreNonce(n=>n+1);setMapRestore(old=>({camera:restored.camera,nonce:old.nonce+1}));setBrowse(false);setNotes(false);setMore(false);setLayers(false);
  }
  window.addEventListener("popstate",restore);window.addEventListener("hashchange",restore);
  return()=>{window.removeEventListener("popstate",restore);window.removeEventListener("hashchange",restore)};
 },[]);
 function back(){
  if((window.history.state?.atlasDepth??0)>0)window.history.back();
  else if(state.enlarged)navigate({enlarged:false},true);
  else if(state.siteView==="photo")navigate({siteView:"plan",highlightId:null},true);
  else if(state.featureId)navigate({featureId:null},true);
  else if(state.workbench||state.mode!=="site")navigate({...archaeologyForPlace(entry.id,state.placeId),camera:state.camera},true);
 }
 function changeMode(mode:string){navigate({mode,workbench:null,scrollPhoto:false,recordId:null,enlarged:false});setNotes(false)}
 function chooseEntry(id:string,placeId?:string){
  const e=entries.find(e=>e.id===id);if(!e)return;
  const focused=placeId??e.candidates[0]?.placeId??null;
  navigate({entryId:id,placeId:focused,mode:state.mode==="scroll"?"scroll":"site",workbench:null,planId:state.mode==="scroll"?null:plansForPlace(focused)[0]?.id??null,featureId:null,highlightId:null,recordId:null,viewport:undefined,photoViewport:undefined,modelCamera:undefined,representation:"model",enlarged:false});setNotes(false);
 }
 function choosePlace(id:string){const linked=entry.candidates.some(c=>c.placeId===id)?entry:entries.find(e=>e.candidates.some(c=>c.placeId===id&&c.status==="preferred"))??entries.find(e=>e.candidates.some(c=>c.placeId===id));if(linked)chooseEntry(linked.id,id);}
 function exploreCandidate(id=state.placeId){const p=plansForPlace(id)[0];navigate({placeId:id,mode:"site",planId:p?.id??null,featureId:null,highlightId:null,recordId:null,viewport:undefined,photoViewport:undefined,modelCamera:undefined,representation:"model",siteView:"plan",workbench:null,enlarged:false});setNotes(false)}
 function selectScrollEntry(id:string){const e=entries.find(e=>e.id===id);if(!e)return;const same=e.candidates.some(c=>c.placeId===state.placeId);navigate({entryId:id,scrollColumn:undefined,...(same?{}:{placeId:primaryPlace(id),planId:null,featureId:null,highlightId:null})});}
 function read(id=entry.id){navigate({entryId:id,mode:"scroll",workbench:null,scrollPhoto:false,scrollColumn:undefined,enlarged:false});setNotes(false)}
 useEffect(()=>{
  const context=(document as Document & {modelContext?:{registerTool:(t:unknown,o:{signal:AbortSignal})=>void|Promise<void>}}).modelContext;
  if(!context?.registerTool)return;const controller=new AbortController();
  try{void Promise.resolve(context.registerTool({name:"navigate_scroll_entry",title:"Explore a Copper Scroll entry",description:"Select an entry and its candidate sites.",inputSchema:{type:"object",properties:{entryId:{type:"string",enum:entries.map(e=>e.id)}},required:["entryId"],additionalProperties:false},execute:async(input:{entryId:string})=>{const e=entries.find(e=>e.id===input.entryId);if(!e)throw Error("Unknown entry");navigate({entryId:e.id,placeId:primaryPlace(e.id),mode:"site",workbench:null,planId:plansForPlace(primaryPlace(e.id))[0]?.id??null,featureId:null});return {entryId:e.id,title:e.title};}},{signal:controller.signal})).catch(()=>{});}catch{}return()=>controller.abort();
 },[navigate]);
 const canBack=depth>0||state.mode!=="site"||!!state.featureId||state.siteView==="photo"||!!state.workbench;
 return <main className="atlas-shell unified-atlas" data-mode={state.mode}>
  <a className="skip-link" href="#explore-surface">Skip to exploration</a>
  <header className="unified-header">
   <button className="atlas-back" aria-label="Back" disabled={!canBack} onClick={back}><ArrowLeft size={18}/><span>Back</span></button>
   <div className="unified-brand"><ScrollText size={21}/><span>Copper Scroll <small>Atlas · 3Q15</small></span></div>
   <nav aria-label="Main views"><a href="#kb" className="atlas-kb-return">Knowledge base</a><button aria-current={state.mode!=="scroll"&&!state.workbench?"page":undefined} onClick={()=>exploreCandidate()}><Map size={16}/>Explore</button><button aria-current={state.mode==="scroll"&&!state.workbench?"page":undefined} onClick={()=>read()}><BookOpen size={16}/>Read the scroll</button></nav>
   <div className="unified-header-actions"><button aria-label="Find an entry or place" aria-expanded={browse} onClick={()=>{setBrowse(v=>!v);setMore(false)}}><Search size={17}/><span>Find a place or entry</span></button><div className="unified-menu-wrap"><button aria-label="More atlas options" aria-expanded={more} onClick={()=>setMore(v=>!v)}>More<ChevronDown size={13}/></button>{more&&<div className="unified-menu"><button onClick={()=>{navigate({workbench:"relationships"});setNotes(false)}}><FlaskConical size={15}/>Research tools</button><button onClick={()=>{setAbout(true);setMore(false)}}>About &amp; sources</button><a href={`${repo}/research/README.md`} target="_blank" rel="noreferrer">Research notes<ExternalLink size={13}/></a></div>}</div></div>
  </header>
  <div id="explore-surface" className="unified-surface">
   {state.workbench?<Suspense fallback={<p>Opening research tools…</p>}><Workbench moduleId={state.workbench} onModule={id=>navigate({workbench:id})} onClose={back}/></Suspense>:<>
    <AtlasMap entry={entry} places={places} entries={entries} focusId={state.placeId} focusNonce={focusNonce} visibleIds={visibleIds} mode={state.mode} onMode={changeMode} onPlace={choosePlace} onEntry={selectScrollEntry} mobileView="map" onText={()=>read()}
     onExploreSite={()=>exploreCandidate()} onCamera={camera=>saveSnapshot({camera})} restoreCamera={mapRestore.camera} restoreNonce={mapRestore.nonce}
     onRecord={id=>navigate({recordId:id})} recordId={state.recordId}
     scrollPhoto={state.scrollPhoto} scrollColumn={state.scrollColumn} onScrollColumn={column=>navigate({scrollColumn:column})} onScrollPhoto={(show,id)=>navigate({scrollPhoto:show,entryId:id??entry.id})}/>
    {state.mode==="site"&&!plan&&<ArchaeologyCatalog entry={entry} place={place} places={places} onPlan={selected=>{const id=selected.placeIds[0];const linked=entries.find(e=>e.candidates.some(c=>c.placeId===id))!;navigate({...archaeologyForPlace(linked.id,id),planId:selected.id});}} onRead={()=>read()} onDossier={()=>changeMode("dossier")} onTerrain={()=>{changeMode("3d");setFocusNonce(n=>n+1)}}/>}
    {state.mode==="site"&&plan&&<SiteExplorer entry={entry} place={place} plan={plan} featureId={state.featureId} highlightId={state.highlightId} onHighlight={id=>navigate({highlightId:id})} view={state.siteView} representation={state.representation} modelCamera={state.modelCamera} onModelCamera={modelCamera=>saveSnapshot({modelCamera})} onRepresentation={representation=>navigate({representation,siteView:"plan"})} viewport={state.viewport} photoViewport={state.photoViewport} restoreNonce={restoreNonce} onViewport={(v:Viewport,photo:boolean)=>saveSnapshot(photo?{photoViewport:v}:{viewport:v})} onFeature={id=>navigate({featureId:id,enlarged:false})} onPlan={id=>navigate({planId:id,featureId:null,highlightId:null,viewport:undefined,modelCamera:undefined,representation:"model",siteView:"plan"})} onView={view=>navigate({siteView:view,enlarged:false})} onTerrain={()=>{changeMode("3d");setFocusNonce(n=>n+1)}} onRead={read} enlarged={!!state.enlarged} onEnlarge={()=>navigate({enlarged:true})} onCloseEnlarged={back}/>}
    {state.mode==="dossier"&&<div className="unified-dossier"><Suspense fallback={<p>Opening evidence…</p>}><Dossier entry={entry} place={place} onEntry={selectScrollEntry} onRead={()=>read()}/></Suspense></div>}
    {["2d","3d"].includes(state.mode)&&<>
     <div className="explore-context"><span>Entry {entry.id} · {entry.title}</span><button onClick={()=>setNotes(v=>!v)} aria-expanded={notes}>{notes?"Close details":"Entry details"}</button><div className="unified-menu-wrap"><button onClick={()=>setLayers(v=>!v)} aria-expanded={layers}><Layers size={14}/>Map layers</button>{layers&&<div className="unified-menu"><p>Historical context for this place</p><button onClick={()=>changeMode("landscape")}>Historical maps &amp; archive</button><small>Source dates and alignment limits accompany each layer.</small></div>}</div></div>
     {feature&&state.planId&&!notes&&<aside className="terrain-feature-note"><button onClick={()=>navigate({mode:"site",siteView:"plan"})}>View selected structure in plan</button><FeatureNote feature={feature} onRead={read}/><p className="terrain-registration-note">This feature has source-plan coordinates; its exact terrain position is unresolved.</p></aside>}

    </>}
   </>}
   {browse&&<aside className="unified-browser" aria-label="Find entries"><header><h2>Find an entry or place</h2><button aria-label="Close search" onClick={()=>setBrowse(false)}><X size={18}/></button></header><input autoFocus aria-label="Search entries and places" placeholder="Qumran, Siloam, 29…" value={query} onChange={e=>setQuery(e.target.value)}/><select aria-label="Filter region" value={region} onChange={e=>setRegion(e.target.value)}><option value="all">All regions</option><option value="jericho">Jericho &amp; Qumran</option><option value="jerusalem">Jerusalem</option><option value="region">Judean hills &amp; north</option><option value="unplaced">Unplaced</option></select><nav aria-label="Entry results">{matches.map(e=><button key={e.id} aria-current={e.id===entry.id?"true":undefined} onClick={()=>chooseEntry(e.id)}><span>{e.id}</span><div><strong>{e.title}</strong><small>{e.candidates[0]?byPlace[e.candidates[0].placeId].shortName:"Location unresolved"}</small></div></button>)}{matches.length===0&&<p>No matching entry. Try another place name.</p>}</nav></aside>}
   {notes&&<aside className="unified-entry-note" aria-label="Entry details"><header><span>Entry {entry.id} · {entry.lines}</span><button aria-label="Close entry details" onClick={()=>setNotes(false)}><X size={18}/></button></header><h2>{entry.title}</h2><p>{entry.description}</p><h3>Candidate sites</h3>{entry.candidates.length>0&&<EvidenceLegend/>}{entry.candidates.map(c=><div className="unified-candidate" key={c.placeId}><strong>{byPlace[c.placeId].shortName}</strong><EvidenceChips entryId={entry.id} placeId={c.placeId}/><small className="ec-status">{c.status}</small><button onClick={()=>{exploreCandidate(c.placeId);setNotes(false)}}>Explore candidate</button></div>)}{!entry.candidates.length&&<p>No mapped candidate.</p>}<button className="unified-read-link" onClick={()=>read()}><BookOpen size={16}/>Read this passage</button><details><summary>Evidence &amp; interpretation</summary><EvidenceComponents entryId={entry.id} placeId={state.placeId&&entry.candidates.some(c=>c.placeId===state.placeId)?state.placeId:strongestCandidate(entry)?.placeId}/><EvidenceReview entryId={entry.id} placeId={state.placeId}/><p>{entry.evidence}</p><p>{entry.caution}</p><button onClick={()=>{changeMode("dossier");setNotes(false)}}>Full source dossier</button></details><details><summary>Passage translation</summary><EntryText entryId={entry.id} onOpenScroll={()=>read()}/></details></aside>}
  </div>
  {about&&<div className="unified-modal" role="dialog" aria-modal="true" aria-label="About the atlas"><div><button aria-label="Close about" onClick={()=>setAbout(false)}><X/></button><h2>Places, structures &amp; the scroll</h2><p>Select a candidate, explore its source plan, and inspect a feature’s evidence. Regional relief provides geographical context. Excavated structures are explored through their source plans. Source-relative plans retain their own coordinates until registration is established.</p><p>All current site identifications remain conditional. A feature comparison identifies neither a deposit nor surviving treasure.</p><p>Hebrew: Abegg’s transcription, ETCBC CC BY-NC 4.0. Translation: this project. Plans and photographs retain their source credits and licences.</p><a href={`${repo}/atlas/README.md`} target="_blank" rel="noreferrer">Atlas guide &amp; sources</a></div></div>}
 </main>;
}
