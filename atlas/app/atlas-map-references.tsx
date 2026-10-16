import {lazy,Suspense,useState} from 'react';
import LibraryReferences from './atlas-library-references';
import references from './atlas-library-references.json';
import type {SitePlan} from './atlas-explorer-model';
import type {Entry,Place} from './atlas-types';
const EvidenceDossier=lazy(()=>import('./atlas-dossier'));
export type MapPanel='plan'|'photos'|'sources'|'history'|null;
const qumranVideos=[{id:'muN-EJR631Y',title:'Qumran aqueduct · Mattiolli',note:'Existing creator-linked reference; footage has not been visually reviewed.'},{id:'vLn1ltBqeSI',title:'Qumran · Sergio & Rhoda',note:'Existing video lead; footage has not been visually reviewed.'}];
export function MapVideoReferences({placeId}:{placeId:string|null}){
 const builtIn=placeId==='kh_qumran'||placeId==='wadi_qumran'?qumranVideos:[];
 const storageKey=`atlas-site-videos:${placeId??'unplaced'}`;
 const [custom,setCustom]=useState<{id:string;title:string;note:string}[]>(()=>{try{return JSON.parse(localStorage.getItem(storageKey)??'[]').filter((v:{id?:string})=>typeof v.id==='string'&&/^[-\w]{11}$/.test(v.id));}catch{return[];}}),[selected,setSelected]=useState<string|null>(null),[url,setUrl]=useState(''),[error,setError]=useState('');
 function add(){try{const u=new URL(url);if(!['youtube.com','www.youtube.com','m.youtube.com','youtu.be','www.youtube-nocookie.com'].includes(u.hostname))throw Error();const id=u.hostname==='youtu.be'?u.pathname.slice(1):u.searchParams.get('v')??u.pathname.match(/\/(?:embed|shorts)\/([\w-]+)/)?.[1];if(!id||!/^[-\w]{11}$/.test(id))throw Error();if(![...builtIn,...custom].some(v=>v.id===id)){const next=[...custom,{id,title:'Added site video',note:'User-supplied reference; not a surveyed camera path or verified reconstruction.'}];setCustom(next);try{localStorage.setItem(storageKey,JSON.stringify(next));}catch{}}setSelected(id);setUrl('');setError('');}catch{setError('Enter a YouTube video link.');}}
 return <div className="map-media-references"><h3>Site videos</h3><p>Watch references beside the map. A video does not register the model’s position or create a 360° capture.</p>{[...builtIn,...custom].map(video=><button key={video.id} aria-pressed={selected===video.id} onClick={()=>setSelected(video.id)}><strong>{video.title}</strong><small>{video.note}</small></button>)}
 {selected&&<><iframe title="Site reference video" src={`https://www.youtube-nocookie.com/embed/${selected}`} allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowFullScreen referrerPolicy="strict-origin-when-cross-origin"/><p className="map-media-limit">If playback is unavailable, check the network connection or the video’s embedding permissions.</p></>}
 <label>Add a walkthrough reference<input aria-label="YouTube site video URL" value={url} onChange={e=>setUrl(e.target.value)} placeholder="https://www.youtube.com/watch?v=…" type="url"/></label><button onClick={add}>Show video here</button>{error&&<p role="alert">{error}</p>}{!builtIn.length&&!custom.length&&<p>No curated walkthrough video is attached to this site yet.</p>}</div>;
}
export function MapSourceReferences({plan,placeId,assumptions,entry,place,onEntry,onHistory,onRead}:{plan?:SitePlan;placeId:string|null;assumptions:string[];entry:Entry;place:Place|null;onEntry:(id:string)=>void;onHistory:()=>void;onRead:()=>void}){
 const [scan,setScan]=useState<string|null>(null);
 const planRefs:Record<string,{sourceId:string;locator:string}[]>=references.planReferences;
 const files:Record<string,{driveId:string;title:string}>=references.sources;
 return <div className="map-media-references"><LibraryReferences planIds={plan?[plan.id]:[]} placeId={placeId}/>{plan&&<><h3>{plan.source}</h3><p>{plan.credit}</p><p>{plan.limit}</p>{(planRefs[plan.id]??[]).map(ref=><button key={ref.sourceId} onClick={()=>setScan(files[ref.sourceId].driveId)}>View library scan here</button>)}</>}{scan&&<><iframe title="Google Drive source scan" className="map-drive-scan" src={`https://drive.google.com/file/d/${scan}/preview`} allowFullScreen/><p>Drive access follows your account’s permissions.</p></>}{assumptions.length>0&&<details><summary>Model sources and assumptions</summary>{assumptions.map(a=><p key={a}>{a}</p>)}</details>}<details className="map-evidence-accordion"><summary>Site evidence and interpretations</summary><div className="map-evidence-body"><Suspense fallback={<p>Opening the evidence record…</p>}><EvidenceDossier entry={entry} place={place} onEntry={onEntry} onLandscape={onHistory} onRead={onRead}/></Suspense></div></details></div>;
}
