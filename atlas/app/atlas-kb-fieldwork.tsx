"use client";
import {useState} from 'react';
import {ArrowUpRight} from 'lucide-react';
import {Segments,useScrollText} from './atlas-text';
import {sitePlans} from './atlas-explorer-model';
import type {KBRecord} from './atlas-kb-model';

const base=import.meta.env?.BASE_URL??'/';
const iv17=sitePlans.find(p=>p.id==='abu-saraj-iv17')!;

// Display adapters only: the reader, plan catalogue and KB remain authoritative.
export function PassageEdition({entry,onSelect}:{entry:KBRecord;onSelect:(key:string)=>void}){
 const {data,failed}=useScrollText();
 const lines=data?.entries[entry.id];
 const concordance=entry.payload.edition_concordance;
 return <div className="kb-edition">
  <header><span>3Q15 · {entry.payload.canonical_lines}</span><span>Edition-based text</span></header>
  <div className="kb-edition-labels"><span>Line</span><span>Project translation</span><span lang="he" dir="rtl">עברית</span></div>
  {entry.payload.translation_context?.map((line:{line:string;text:string})=>{
   const original=lines?.find(l=>l.ref===line.line);
   return <div className="kb-edition-line" key={line.line}><span className="kb-line-ref">{line.line}</span><p>{line.text.replace(/\{\{([^|}]+)\|[^}]+\}\}/g,'$1')}</p><p className="kb-edition-hebrew" lang="he" dir="rtl">{original?original.w.map((w,n)=><span key={n}><Segments w={w}/>{w.n!=null&&<bdi className="kb-ancient-number">{w.n}</bdi>}{' '}</span>):<span className="kb-hebrew-pending">{failed?'Text unavailable':'Loading…'}</span>}</p></div>;
  })}
  <footer><p className="kb-edition-numbering">Entry numbering · Puech {concordance?.entry_puech??entry.id} / Lefkovits {concordance?.item_lefkovits??'—'} / Milik {concordance?.item_milik??'—'} / Allegro {concordance?.item_allegro??'—'}</p><details><summary>Editorial signs & text source</summary><p>[ ] restored letters · ⟨ ⟩ supplied correction · {'{ }'} editorial deletion · {'{{ }}'} ancient cancellation · dotted letters: uncertain · raised letters: above the line. Numerals appear as modern numbers.</p><p>Hebrew: Abegg, Bowley & Cook, ETCBC dss 2.0.1, <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noreferrer">CC BY-NC 4.0</a>. Modern typesetting; manuscript-image verification has its own record. English: project translation. Alternative readings remain below.</p></details><button className="kb-inline-link" onClick={()=>onSelect(entry.key)}>Passage record, boundaries & sources <ArrowUpRight size={14}/></button></footer>
 </div>;
}

export function SourcePlate({compact=false,onSelect}:{compact?:boolean;onSelect:(key:string)=>void}){
 const [failed,setFailed]=useState(false);
 return <figure className={'kb-source-plate'+(compact?' compact':'')}>
  <div className="kb-plate-heading"><span>PL. 01 · IV/17</span><span>Published excavation plan</span></div>
  <a className="kb-plate-image" href={`${base}${iv17.image}`} target="_blank" rel="noreferrer" aria-label="Open complete IV/17 source plan">{failed?<span>Plan image unavailable. Open the published source below.</span>:<img src={`${base}${iv17.image}`} alt="Sion’s complete Plan 5 of IV/17, including the original caption, scale and north arrow. No project overlays." onError={()=>setFailed(true)} loading={compact?'lazy':'eager'}/>}</a>
  <figcaption><strong>{iv17.source}</strong><p>{iv17.credit}</p><p className="kb-plate-limit">{iv17.limit}</p><div><button className="kb-inline-link" onClick={()=>onSelect('source/inventory-sion-iv17')}>Evidence record <ArrowUpRight size={14}/></button><a href={iv17.sourceUrl} target="_blank" rel="noreferrer">Publication <ArrowUpRight size={14}/></a><a href={iv17.licenseUrl} target="_blank" rel="noreferrer">Licence</a><a href="#entry-25/site/abu-saraj-iv17/source">Inspect plan in atlas <ArrowUpRight size={14}/></a></div></figcaption>
 </figure>;
}

export function CandidateFieldRecord({candidate,onSelect}:{candidate:KBRecord;onSelect:(key:string)=>void}){
 return <div className="kb-field-record"><div><span className="kb-field-label">Catalogue / hypothesis</span><code>{candidate.id}</code><h4>{candidate.label}</h4><button className="kb-inline-link" onClick={()=>onSelect(candidate.key)}>Feature identities, phases & source records <ArrowUpRight size={14}/></button></div>{candidate.key==='hypothesis/iv17'?<SourcePlate compact onSelect={onSelect}/>:<p className="kb-plan-gap"><span>Figure coverage</span>No source plan is linked to this candidate in this view. Its observations, historical states and uncertainties remain in the evidence record.</p>}</div>;
}
