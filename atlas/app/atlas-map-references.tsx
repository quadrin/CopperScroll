import {lazy,Suspense,useState} from 'react';
import LibraryReferences from './atlas-library-references';
import references from './atlas-library-references.json';
import siteMedia from './atlas-site-media.json';
import type {SitePlan} from './atlas-explorer-model';
import type {Entry,Place} from './atlas-types';
const EvidenceDossier=lazy(()=>import('./atlas-dossier'));
export type MapPanel='plan'|'photos'|'sources'|'history'|null;
type SiteVideo={id:string;title:string;channel?:string;note:string};
type SiteModel={uid:string;title:string;author:string;license:string;downloadable:boolean;faces:number;note:string};
const curatedVideos=siteMedia.videos as Record<string,SiteVideo[]>;
const curatedModels=siteMedia.models as Record<string,SiteModel[]>;
export function MapVideoReferences({placeId}:{placeId:string|null}){
 const builtIn=placeId?curatedVideos[placeId]??[]:[];
 const storageKey=`atlas-site-videos:${placeId??'unplaced'}`;
 const [custom,setCustom]=useState<SiteVideo[]>(()=>{try{return JSON.parse(localStorage.getItem(storageKey)??'[]').filter((v:{id?:string})=>typeof v.id==='string'&&/^[-\w]{11}$/.test(v.id));}catch{return[];}}),[selected,setSelected]=useState<string|null>(null),[url,setUrl]=useState(''),[error,setError]=useState('');
 function add(){try{const u=new URL(url);if(!['youtube.com','www.youtube.com','m.youtube.com','youtu.be','www.youtube-nocookie.com'].includes(u.hostname))throw Error();const id=u.hostname==='youtu.be'?u.pathname.slice(1):u.searchParams.get('v')??u.pathname.match(/\/(?:embed|shorts)\/([\w-]+)/)?.[1];if(!id||!/^[-\w]{11}$/.test(id))throw Error();if(![...builtIn,...custom].some(v=>v.id===id)){const next=[...custom,{id,title:'Added site video',note:'User-supplied reference; not a surveyed camera path or verified reconstruction.'}];setCustom(next);try{localStorage.setItem(storageKey,JSON.stringify(next));}catch{}}setSelected(id);setUrl('');setError('');}catch{setError('Enter a YouTube video link.');}}
 return <><div className="map-media-references"><h3>Site videos</h3><p>Watch references beside the map. Videos are embedded from YouTube and remain their makers’ work. A video does not register the model’s position, date a feature or create a 360° capture.</p>{[...builtIn,...custom].map(video=><button key={video.id} aria-pressed={selected===video.id} onClick={()=>setSelected(video.id)}><strong>{video.title}</strong>{video.channel&&<small className="map-media-channel">{video.channel}</small>}<small>{video.note}</small></button>)}
 {selected&&<><iframe title="Site reference video" src={`https://www.youtube-nocookie.com/embed/${selected}`} allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowFullScreen referrerPolicy="strict-origin-when-cross-origin"/><p className="map-media-limit">If playback is unavailable, check the network connection or the video’s embedding permissions. <a href={`https://www.youtube.com/watch?v=${selected}`} target="_blank" rel="noreferrer">Open on YouTube</a></p></>}
 <label>Add a walkthrough reference<input aria-label="YouTube site video URL" value={url} onChange={e=>setUrl(e.target.value)} placeholder="https://www.youtube.com/watch?v=…" type="url"/></label><button onClick={add}>Show video here</button>{error&&<p role="alert">{error}</p>}{!builtIn.length&&!custom.length&&<p>No curated walkthrough video is attached to this site yet.</p>}</div>
 <MapModelReferences placeId={placeId}/></>;
}
export function MapModelReferences({placeId}:{placeId:string|null}){
 const models=placeId?curatedModels[placeId]??[]:[];
 const [selected,setSelected]=useState<string|null>(null);
 if(!models.length)return null;
 const active=models.find(m=>m.uid===selected);
 return <div className="map-media-references map-model-references"><h3>3D models</h3><p>Third-party photogrammetry and scans, shown in Sketchfab’s viewer. They are not georeferenced, not surveyed plans and not the atlas’s source-based models. Each stays under its maker’s licence.</p>
 {models.map(m=><button key={m.uid} aria-pressed={selected===m.uid} onClick={()=>setSelected(m.uid)}><strong>{m.title}</strong><small className="map-media-channel">{m.author} · {m.license}{m.downloadable?' · downloadable':''}</small>{m.note&&<small>{m.note}</small>}</button>)}
 {active&&<><iframe className="map-model-embed" title={`3D model: ${active.title}`} src={`https://sketchfab.com/models/${active.uid}/embed?autostart=1&ui_infos=0&ui_watermark_link=1`} allow="autoplay; fullscreen; xr-spatial-tracking" allowFullScreen referrerPolicy="strict-origin-when-cross-origin"/><p className="map-media-limit">Model: <a href={`https://sketchfab.com/3d-models/${active.uid}`} target="_blank" rel="noreferrer">{active.title}</a> by {active.author} on Sketchfab · {active.license}. Loading needs an internet connection.</p></>}
 </div>;
}
export function MapSourceReferences({plan,placeId,assumptions,entry,place,onEntry,onHistory,onRead}:{plan?:SitePlan;placeId:string|null;assumptions:string[];entry:Entry;place:Place|null;onEntry:(id:string)=>void;onHistory:()=>void;onRead:()=>void}){
 const [scan,setScan]=useState<string|null>(null);
 const planRefs:Record<string,{sourceId:string;locator:string}[]>=references.planReferences;
 const files:Record<string,{driveId:string;title:string}>=references.sources;
 return <div className="map-media-references"><LibraryReferences planIds={plan?[plan.id]:[]} placeId={placeId}/>{plan&&<><h3>{plan.source}</h3><p>{plan.credit}</p><p>{plan.limit}</p>{(planRefs[plan.id]??[]).map(ref=><button key={ref.sourceId} onClick={()=>setScan(files[ref.sourceId].driveId)}>View library scan here</button>)}</>}{scan&&<><iframe title="Google Drive source scan" className="map-drive-scan" src={`https://drive.google.com/file/d/${scan}/preview`} allowFullScreen/><p>Drive access follows your account’s permissions.</p></>}{assumptions.length>0&&<details><summary>Model sources and assumptions</summary>{assumptions.map(a=><p key={a}>{a}</p>)}</details>}<details className="map-evidence-accordion"><summary>Site evidence and interpretations</summary><div className="map-evidence-body"><Suspense fallback={<p>Opening the evidence record…</p>}><EvidenceDossier entry={entry} place={place} onEntry={onEntry} onLandscape={onHistory} onRead={onRead}/></Suspense></div></details></div>;
}
