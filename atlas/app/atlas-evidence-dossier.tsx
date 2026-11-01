"use client";

import AtlasDossier from './atlas-dossier';
import EntryText from './atlas-text';
import EvidenceReview from './atlas-evidence';
import {EvidenceChips,EvidenceLegend} from './atlas-components';
import data from './atlas-data.json';
import type {Entry,Place} from './atlas-types';
import './atlas-evidence-dossier.css';
import {contextHash} from './atlas-context-routes';

const entries=data.entries as Entry[];
const places=data.places as Place[];
const dossierHash=(entry:string,place:string)=>contextHash(entry,'dossier',place);

// The complete dossier keeps its original source records, figures, phases,
// alternative localities and interpretations. Only its destination changes.
export default function EvidenceSiteDossier({entryId,placeId}:{entryId:string;placeId:string}){
 const entry=entries.find(item=>item.id===entryId);
 const selectedPlaceId=placeId||entry?.candidates[0]?.placeId||'';
 const place=places.find(item=>item.id===selectedPlaceId)??null;
 if(!entry)return <section className="evidence-site-dossier"><p>This passage is unavailable.</p><a href="#entry-21/2d">Open map</a></section>;
 function linkedEntry(id:string){
  const next=entries.find(item=>item.id===id);
  const target=next?.candidates.some(candidate=>candidate.placeId===selectedPlaceId)?selectedPlaceId:next?.candidates[0]?.placeId??'';
  location.hash=dossierHash(id,target);
 }
 return <section className="evidence-site-dossier" aria-label="Complete site evidence">
  <div className="evidence-dossier-tools">
   {!!entry.candidates.length&&<label>Candidate site<select aria-label="Evidence candidate site" value={place?.id??''} onChange={event=>{location.hash=dossierHash(entry.id,event.target.value)}}>{!place&&<option value="">Location unresolved</option>}{place&&!entry.candidates.some(candidate=>candidate.placeId===place.id)&&<option value={place.id}>Context · {place.shortName}</option>}{entry.candidates.map(candidate=><option key={candidate.placeId} value={candidate.placeId}>{places.find(item=>item.id===candidate.placeId)?.shortName??candidate.placeId}</option>)}</select></label>}
   {place&&<a href={`#entry-${entry.id}/2d?place=${encodeURIComponent(place.id)}`}>View this site on the map</a>}
  </div>
  {placeId&&!place&&<p role="status">This site ID is unavailable. Choose a listed candidate to inspect its evidence.</p>}
  <AtlasDossier entry={entry} place={place} onEntry={linkedEntry} onRead={()=>{location.hash=`#entry-${entry.id}/scroll${place?'?'+new URLSearchParams({place:place.id}):''}`}} onLandscape={()=>{location.hash=`#entry-${entry.id}/landscape${place?'?'+new URLSearchParams({place:place.id}):''}`}}/>
  <details className="evidence-entry-assessment"><summary>Passage and candidate assessments</summary><p>{entry.description}</p><p>{entry.evidence}</p><p>{entry.caution}</p>{!!entry.candidates.length&&<><EvidenceLegend/>{entry.candidates.map(candidate=><article key={candidate.placeId}><h3>{places.find(item=>item.id===candidate.placeId)?.shortName??candidate.placeId}</h3><EvidenceChips entryId={entry.id} placeId={candidate.placeId}/><p>{candidate.status}</p><a href={dossierHash(entry.id,candidate.placeId)}>Inspect this candidate’s evidence</a></article>)}</>}<EvidenceReview entryId={entry.id} placeId={place?.id??null}/><EntryText entryId={entry.id} onOpenScroll={()=>{location.hash=`#entry-${entry.id}/scroll${place?'?'+new URLSearchParams({place:place.id}):''}`}}/></details>
 </section>;
}
