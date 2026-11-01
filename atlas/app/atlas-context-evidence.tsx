"use client";

import {lazy,Suspense,useEffect,useRef,useState} from 'react';
import {ArrowLeft} from 'lucide-react';
import {index,entryContext,type KBData,type KBIndex} from './atlas-kb-model';
import {Comparison,Graph,Inspector,Requirements,Names,Impact,Sources,ReadingAlternatives,Targets,RecordSearch} from './atlas-kb';
import {EvidenceComponents} from './atlas-components';
import catalogue from './atlas-data.json';
import type {Entry} from './atlas-types';
import './atlas-context-evidence.css';

const SiteDossier=lazy(()=>import('./atlas-evidence-dossier'));
export type ContextEvidenceView='compare'|'assessment'|'record'|'readings'|'names'|'sources'|'dossier'|'graph'|'tests'|'impact';
export const viewLabels:Record<ContextEvidenceView,string>={compare:'Compare candidates',assessment:'Candidate assessment',record:'Evidence record',readings:'Reading alternatives',names:'Names & dates',sources:'Sources & gaps',dossier:'Site dossier',graph:'Connections',tests:'Saved tests',impact:'Change impact'};
export type ContextEvidenceProps={entryId:string;view:ContextEvidenceView;record?:string;placeId?:string;onView:(view:ContextEvidenceView)=>void;onRecord:(key:string)=>void;onClose?:()=>void};

let cachedIndex:KBIndex|null=null;
let pendingIndex:Promise<KBIndex>|null=null;
// Map and reader panels share the same immutable snapshot and index.
export function loadContextEvidence():Promise<KBIndex>{
 if(cachedIndex)return Promise.resolve(cachedIndex);
 if(!pendingIndex)pendingIndex=import('./atlas-kb.json').then(module=>{cachedIndex=index(module.default as unknown as KBData);return cachedIndex;}).catch(error=>{pendingIndex=null;throw error;});
 return pendingIndex;
}

export default function ContextEvidence({entryId,view,record,placeId,onView,onRecord,onClose}:ContextEvidenceProps){
 const [i,setIndex]=useState<KBIndex|null>(cachedIndex),[error,setError]=useState(''),[attempt,setAttempt]=useState(0),[trail,setTrail]=useState<string[]>([]);
 const previousView=useRef<ContextEvidenceView>('compare'),pendingRecord=useRef<string|undefined>(undefined);
 useEffect(()=>{let active=true;setError('');loadContextEvidence().then(value=>{if(active)setIndex(value);}).catch(()=>{if(active)setError('The evidence snapshot could not load.');});return()=>{active=false;};},[attempt]);
 useEffect(()=>{if(view!=='record')previousView.current=view;},[view]);
 useEffect(()=>{setTrail([]);previousView.current=view==='record'?'compare':view;},[entryId]);
 useEffect(()=>{if(record!==pendingRecord.current)setTrail([]);pendingRecord.current=undefined;},[record]);
 function select(key:string){if(view==='record'&&record&&key!==record)setTrail(items=>[...items,record]);else if(view!=='record')setTrail([]);pendingRecord.current=key;onRecord(key);}
 function back(){if(trail.length){const key=trail[trail.length-1];setTrail(items=>items.slice(0,-1));pendingRecord.current=key;onRecord(key);}else onView(previousView.current);}
 if(error)return <div className="kb-context-evidence"><p role="alert">{error}</p><button className="kb-inline-link" onClick={()=>setAttempt(value=>value+1)}>Retry loading evidence</button>{onClose&&<button className="kb-inline-link" onClick={onClose}>Return to the atlas</button>}</div>;
 if(!i)return <div className="kb-context-evidence"><p className="kb-loading" role="status">Loading evidence…</p></div>;
 const entry=i.by.get('entry/'+entryId),context=entryContext(i,entryId),candidates=context.filter(item=>item.kind==='hypothesis');
 if(!entry)return <div className="kb-context-evidence"><p role="status">This passage is unavailable in the evidence register.</p></div>;
 const selected=record?i.by.get(record):undefined;
 const assessment=(catalogue.entries as Entry[]).find(item=>item.id===entryId);
 const assessedPlace=placeId||assessment?.candidates[0]?.placeId;
 // Keep the originating view mounted while inspecting records, preserving its
 // chosen comparison branch, expanded candidate and source scope for Back.
 const contentView=view==='record'?previousView.current:view;
 return <div className="kb-context-evidence" data-evidence-view={view}>
  <div hidden={view==='record'}>
  {contentView==='compare'&&<><Comparison key={entryId} i={i} candidates={candidates} onSelect={select}/><Targets i={i} context={context} onSelect={select}/></>}
  {contentView==='assessment'&&<><section className="kb-context-assessment">{assessment?<><p>{assessment.description}</p>{assessedPlace&&<EvidenceComponents entryId={entryId} placeId={assessedPlace}/>}<p>{assessment.evidence}</p><p>{assessment.caution}</p></>:<p>No candidate assessment is recorded for this passage.</p>}</section><Targets i={i} context={context} onSelect={select}/></>}
  {contentView==='readings'&&<ReadingAlternatives i={i} context={context} onSelect={select}/>}
  {contentView==='names'&&<Names i={i} onSelect={select}/>}
  {contentView==='sources'&&<Sources key={entryId} i={i} context={context} onSelect={select}/>}
  {contentView==='dossier'&&<Suspense fallback={<p role="status">Loading the site dossier…</p>}><SiteDossier entryId={entryId} placeId={placeId||''}/></Suspense>}
  {contentView==='graph'&&<><RecordSearch i={i} onSelect={select}/><p className="kb-view-help">Select a connected record to inspect its evidence and assumptions.</p><Graph i={i} entry={entryId} selected={selected?.key||entry.key} onSelect={select}/></>}
  {contentView==='tests'&&<Requirements key={entryId} i={i} candidates={candidates} onSelect={select}/>}
  {contentView==='impact'&&(selected?<Impact i={i} selected={selected} onSelect={select}/>:<><p role="status">Select a source below, then choose “What depends on this?” in its record.</p><Sources key={entryId} i={i} context={context} onSelect={select}/></>)}
  </div>
  {view==='record'&&<><div className="kb-context-record-back"><button onClick={back}><ArrowLeft size={16}/>{trail.length?'Back to previous record':'Back to '+viewLabels[previousView.current].toLowerCase()}</button></div>{selected?<Inspector key={selected.key} i={i} record={selected} onSelect={select} onImpact={()=>onView('impact')}/>:<p role="status">This evidence record is unavailable. Its identifier has not been replaced with another record.</p>}</>}
 </div>;
}
