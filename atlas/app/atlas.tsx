"use client";
import { lazy, Suspense, useCallback, useEffect, useRef, useState } from "react";
import { ArrowLeft, BookOpen, ChevronDown, Search, X } from "lucide-react";
import AtlasMap from "./atlas-map";
import AtlasSiteNav from "./atlas-site-nav";
import EntryText from "./atlas-text";
import EvidenceReview from "./atlas-evidence";
import { EvidenceChips, EvidenceComponents, EvidenceLegend, strongestCandidate } from "./atlas-components";
import data from "./atlas-data.json";
import { explorerFromHash, explorerHash, initialExplorer, archaeologyForPlace, plansForPlace, sitePlans, type ExplorerState, type Camera } from "./atlas-explorer-model";
import type { Entry, Place } from "./atlas-types";
import "./atlas-revamp.css";
import "./atlas-unified.css";
import "./atlas-clean.css";
const entries = data.entries as Entry[];
const places = data.places as Place[];
const byPlace = Object.fromEntries(places.map(p=>[p.id,p]));
const primaryPlace = (id:string)=>entries.find(e=>e.id===id)?.candidates[0]?.placeId??null;
const Workbench = lazy(()=>import("./atlas-workbench"));
type HistoryState = ExplorerState & { enlarged?: boolean };

export default function Atlas(){
 const [state,setState] = useState<HistoryState>(()=>{if(typeof window==="undefined")return initialExplorer;const saved=window.history.state?.atlas;if(saved&&window.history.state.atlasVersion!==2&&["2d","3d"].includes(saved.mode))return archaeologyForPlace(saved.entryId,saved.placeId);return saved&&explorerHash(saved)===location.hash?saved:explorerFromHash(location.hash,primaryPlace)??initialExplorer});
 const current=useRef(state);
 const [depth,setDepth]=useState(0);
 const [mapRestore,setMapRestore]=useState<{camera?:Camera;nonce:number}>({nonce:0});
 const [focusNonce,setFocusNonce]=useState(0);
 const [browse,setBrowse]=useState(false);
 const [contextOpen,setContextOpen]=useState(false);
 const contextToggle=useRef<HTMLButtonElement>(null);
 useEffect(()=>{if(!contextOpen)return;const close=(e:PointerEvent)=>{if(!contextToggle.current?.closest(".atlas-explorer-bar")?.contains(e.target as Node))setContextOpen(false)};document.addEventListener("pointerdown",close);return()=>document.removeEventListener("pointerdown",close)},[contextOpen]);
 const [query,setQuery]=useState("");
 const [region,setRegion]=useState("all");
 const [notes,setNotes]=useState(false);
 useEffect(()=>{function escape(event:KeyboardEvent){if(event.key!=="Escape")return;setBrowse(false);setNotes(false);setContextOpen(false);}window.addEventListener("keydown",escape);return()=>window.removeEventListener("keydown",escape)},[]);
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
  current.current=next;setState(next);setDepth(nextDepth);setBrowse(false);setContextOpen(false);
  if(next.entryId!==prev.entryId||next.placeId!==prev.placeId)setFocusNonce(n=>n+1);
  if(next.mode!==prev.mode||next.scrollPhoto!==prev.scrollPhoto||next.scroll3d!==prev.scroll3d)window.dispatchEvent(new Event("atlas:modechange"));
 },[]);
 useEffect(()=>{
  const existing=window.history.state;
  if(existing?.atlas&&existing.atlasVersion===2&&explorerHash(existing.atlas)===location.hash){current.current=existing.atlas;setState(existing.atlas);setDepth(existing.atlasDepth??0);setMapRestore({camera:existing.atlas.camera,nonce:1});}
  else window.history.replaceState({atlas:current.current,atlasDepth:0,atlasVersion:2},"",explorerHash(current.current));
  function restore(){
   const h=window.history.state;
   const restored=h?.atlas&&explorerHash(h.atlas)===location.hash?h.atlas:explorerFromHash(location.hash,primaryPlace);
   if(!restored)return;
   if(!h?.atlas)window.history.replaceState({atlas:restored,atlasDepth:0,atlasVersion:2},"",location.href);
   current.current=restored;setState(restored);setDepth(h?.atlasDepth??0);setMapRestore(old=>({camera:restored.camera,nonce:old.nonce+1}));setBrowse(false);setNotes(false);setContextOpen(false);
  }
  window.addEventListener("popstate",restore);window.addEventListener("hashchange",restore);
  return()=>{window.removeEventListener("popstate",restore);window.removeEventListener("hashchange",restore)};
 },[]);
 function back(){
  if((window.history.state?.atlasDepth??0)>0)window.history.back();
  else if(state.enlarged)navigate({enlarged:false},true);
  else if(state.siteView==="photo")navigate({siteView:"plan",highlightId:null},true);
  else if(state.featureId)navigate({featureId:null},true);
  else {navigate({mode:"2d",workbench:null,featureId:null},true);window.dispatchEvent(new Event("atlas:overview"));}
 }
 function changeMode(mode:string){navigate({mode,workbench:null,scrollPhoto:false,scroll3d:false,recordId:null,enlarged:false});setNotes(false)}
 function chooseEntry(id:string,placeId?:string){
  const e=entries.find(e=>e.id===id);if(!e)return;
  const focused=placeId??e.candidates[0]?.placeId??null;
  navigate({entryId:id,placeId:focused,mode:["2d","3d","scroll","landscape","dossier","ground","scene"].includes(state.mode)?state.mode:"site",workbench:null,planId:state.mode==="scroll"?null:plansForPlace(focused)[0]?.id??null,featureId:null,highlightId:null,recordId:null,viewport:undefined,photoViewport:undefined,modelCamera:undefined,representation:"model",enlarged:false});setNotes(false);
 }
 function choosePlace(id:string){const linked=entry.candidates.some(c=>c.placeId===id)?entry:entries.find(e=>e.candidates.some(c=>c.placeId===id&&c.status==="preferred"))??entries.find(e=>e.candidates.some(c=>c.placeId===id));if(linked)chooseEntry(linked.id,id);}
 function exploreCandidate(id=state.placeId){const p=plansForPlace(id)[0];navigate({placeId:id,mode:"2d",planId:p?.id??null,featureId:null,highlightId:null,recordId:null,viewport:undefined,photoViewport:undefined,modelCamera:undefined,representation:"model",siteView:"plan",workbench:null,enlarged:false});setFocusNonce(n=>n+1);setNotes(false)}
 function selectScrollEntry(id:string){const e=entries.find(e=>e.id===id);if(!e)return;const same=e.candidates.some(c=>c.placeId===state.placeId);navigate({entryId:id,scrollColumn:undefined,...(same?{}:{placeId:primaryPlace(id),planId:null,featureId:null,highlightId:null})});}
 function read(id=entry.id){navigate({entryId:id,mode:"scroll",workbench:null,scrollPhoto:false,scroll3d:false,scrollColumn:undefined,enlarged:false});setNotes(false)}
 useEffect(()=>{
  const context=(document as Document & {modelContext?:{registerTool:(t:unknown,o:{signal:AbortSignal})=>void|Promise<void>}}).modelContext;
  if(!context?.registerTool)return;const controller=new AbortController();
  try{void Promise.resolve(context.registerTool({name:"navigate_scroll_entry",title:"Explore a Copper Scroll entry",description:"Select an entry and its candidate sites.",inputSchema:{type:"object",properties:{entryId:{type:"string",enum:entries.map(e=>e.id)}},required:["entryId"],additionalProperties:false},execute:async(input:{entryId:string})=>{const e=entries.find(e=>e.id===input.entryId);if(!e)throw Error("Unknown entry");navigate({entryId:e.id,placeId:primaryPlace(e.id),mode:"site",workbench:null,planId:plansForPlace(primaryPlace(e.id))[0]?.id??null,featureId:null});return {entryId:e.id,title:e.title};}},{signal:controller.signal})).catch(()=>{});}catch{}return()=>controller.abort();
 },[navigate]);
 const canBack=depth>0||!["2d","3d"].includes(state.mode)||!!state.featureId||!!state.workbench;
 return <main className="atlas-shell unified-atlas" data-mode={state.mode}>
  <a className="skip-link" href="#explore-surface">Skip to exploration</a>
  <AtlasSiteNav entry={entry.id} active={state.workbench?'evidence':['scroll','scene'].includes(state.mode)?'scroll':'map'}/>
  <div className="atlas-explorer-bar" aria-label="Current passage and place">
   <button className="atlas-back" aria-label="Back within atlas" disabled={!canBack} onClick={back}><ArrowLeft size={16}/><span>Back</span></button>
   <button ref={contextToggle} className="atlas-context-toggle" aria-label="Change passage, candidate or site plan" aria-expanded={contextOpen} aria-controls="atlas-context-panel" onClick={()=>setContextOpen(v=>!v)}><span><strong>{entry.id} · {entry.title}</strong><small>{plan?.label??place?.shortName??'Location unresolved'}</small></span><ChevronDown size={18}/></button>
   <button className="atlas-mobile-find" aria-label="Find an entry or place" aria-expanded={browse} onClick={()=>{setContextOpen(false);setBrowse(v=>!v)}}><Search size={18}/></button>
   <div id="atlas-context-panel" className="atlas-context-panel" data-expanded={contextOpen}>
    <div className="atlas-context-panel-head"><strong>Passage and place</strong><button aria-label="Close passage and place" onClick={()=>{setContextOpen(false);contextToggle.current?.focus()}}><X size={18}/></button></div>
   <label className="atlas-entry-picker">Passage<select aria-label="Selected passage" value={entry.id} onChange={e=>chooseEntry(e.target.value)}>{entries.map(e=><option key={e.id} value={e.id}>{e.id} · {e.title}</option>)}</select></label>
   <label>Candidate<select aria-label="Selected candidate" value={state.placeId??''} disabled={!entry.candidates.length} onChange={e=>chooseEntry(entry.id,e.target.value)}>{!entry.candidates.length&&<option value="">Location unresolved</option>}{place&&!entry.candidates.some(c=>c.placeId===place.id)&&<option value={place.id}>Context · {place.shortName}</option>}{entry.candidates.map(c=><option key={c.placeId} value={c.placeId}>{byPlace[c.placeId].shortName}</option>)}</select></label>
   <label className="atlas-plan-picker">Site plans<select aria-label="Browse all site plans" value={plan?.id??''} onChange={e=>{const chosen=sitePlans.find(p=>p.id===e.target.value);if(!chosen)return;const id=chosen.placeIds[0],linked=entry.candidates.some(c=>c.placeId===id)?entry:entries.find(e=>e.candidates.some(c=>c.placeId===id));if(linked)navigate({...archaeologyForPlace(linked.id,id),planId:chosen.id,representation:'model',modelCamera:undefined,viewport:undefined,photoViewport:undefined});}}><option value="">Choose a source plan…</option>{sitePlans.map(p=><option key={p.id} value={p.id}>{p.label}</option>)}</select></label>

   </div>
  </div>
  <div id="explore-surface" className="unified-surface">
   {state.workbench?<Suspense fallback={<p>Opening research tools…</p>}><Workbench moduleId={state.workbench} onModule={id=>navigate({workbench:id})} onClose={back}/></Suspense>:<>
    <AtlasMap representation={state.representation} planId={plan?.id} featureId={state.featureId} onFeature={id=>navigate({featureId:id})} onPlan={id=>navigate({planId:id,featureId:null})} entry={entry} places={places} entries={entries} focusId={state.placeId} focusNonce={focusNonce} visibleIds={visibleIds} mode={state.mode} onMode={changeMode} onPlace={choosePlace} onEntry={selectScrollEntry} mobileView="map" onText={()=>read()}
     onExploreSite={()=>exploreCandidate()} onDetails={()=>setNotes(true)} onCamera={camera=>saveSnapshot({camera})} restoreCamera={mapRestore.camera} restoreNonce={mapRestore.nonce}
     onRecord={id=>navigate({recordId:id})} recordId={state.recordId}
     scrollPhoto={state.scrollPhoto} scrollColumn={state.scrollColumn} onScrollColumn={column=>navigate({scrollColumn:column})} onScrollPhoto={(show,id)=>navigate({scrollPhoto:show,scroll3d:false,entryId:id??entry.id})} scroll3d={state.scroll3d} onScroll3d={show=>navigate({scroll3d:show,scrollPhoto:false})}/>


   </>}
   {browse&&<aside className="unified-browser" aria-label="Find entries"><header><h2>Find an entry or place</h2><button aria-label="Close search" onClick={()=>setBrowse(false)}><X size={18}/></button></header><input autoFocus aria-label="Search entries and places" placeholder="Qumran, Siloam, 29…" value={query} onChange={e=>setQuery(e.target.value)}/><select aria-label="Filter region" value={region} onChange={e=>setRegion(e.target.value)}><option value="all">All regions</option><option value="jericho">Jericho &amp; Qumran</option><option value="jerusalem">Jerusalem</option><option value="region">Judean hills &amp; north</option><option value="unplaced">Unplaced</option></select><nav aria-label="Entry results">{matches.map(e=><button key={e.id} aria-current={e.id===entry.id?"true":undefined} onClick={()=>chooseEntry(e.id)}><span>{e.id}</span><div><strong>{e.title}</strong><small>{e.candidates[0]?byPlace[e.candidates[0].placeId].shortName:"Location unresolved"}</small></div></button>)}{matches.length===0&&<p>No matching entry. Try another place name.</p>}</nav></aside>}
   {notes&&<aside className="unified-entry-note" aria-label="Entry details"><header><span>Entry {entry.id} · {entry.lines}</span><button aria-label="Close entry details" onClick={()=>setNotes(false)}><X size={18}/></button></header><h2>{entry.title}</h2><p>{entry.description}</p><h3>Candidate sites</h3>{entry.candidates.length>0&&<EvidenceLegend/>}{entry.candidates.map(c=><div className="unified-candidate" key={c.placeId}><strong>{byPlace[c.placeId].shortName}</strong><EvidenceChips entryId={entry.id} placeId={c.placeId}/><small className="ec-status">{c.status}</small><button onClick={()=>{exploreCandidate(c.placeId);setNotes(false)}}>Explore candidate</button></div>)}{!entry.candidates.length&&<p>No mapped candidate.</p>}<button className="unified-read-link" onClick={()=>read()}><BookOpen size={16}/>Read this passage</button><details><summary>Evidence &amp; interpretation</summary><EvidenceComponents entryId={entry.id} placeId={state.placeId&&entry.candidates.some(c=>c.placeId===state.placeId)?state.placeId:strongestCandidate(entry)?.placeId}/><EvidenceReview entryId={entry.id} placeId={state.placeId}/><p>{entry.evidence}</p><p>{entry.caution}</p><button onClick={()=>{changeMode("dossier");setNotes(false)}}>Full source dossier</button></details><details><summary>Passage translation</summary><EntryText entryId={entry.id} onOpenScroll={()=>read()}/></details></aside>}
  </div>
 </main>;
}
