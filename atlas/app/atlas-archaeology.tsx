"use client";
import { BookOpen, ChevronRight, Mountain } from "lucide-react";
import { sitePlans, type SitePlan } from "./atlas-explorer-model";
import { placeDossiers } from "./atlas-dossiers-data";
import type { Entry, Place } from "./atlas-types";
import "./atlas-archaeology.css";
const base=import.meta.env?.BASE_URL??"/";
function PlanPreview({plan}:{plan:SitePlan}){
 if(plan.image)return <img src={`${base}${plan.image}`} alt={plan.label} loading="lazy"/>;
 return <svg viewBox={`0 0 ${plan.width} ${plan.height}`} role="img" aria-label={plan.label}><rect width={plan.width} height={plan.height} fill="#e8dec2"/><g transform={plan.transform}>{plan.shapes?.map((shape,i)=><path key={i} d={shape.d} className={`site-shape site-shape-${shape.kind}`} vectorEffect="non-scaling-stroke"/>)}</g></svg>;
}
export default function ArchaeologyCatalog({entry,place,places,onPlan,onRead,onDossier,onTerrain}:{entry:Entry;place:Place|null;places:Place[];onPlan:(plan:SitePlan)=>void;onRead:()=>void;onDossier:()=>void;onTerrain:()=>void}){
 const dossier=placeDossiers.find(d=>d.id===place?.id);
 const groups=Array.from(new Set(sitePlans.map(p=>p.placeIds[0]))).map(id=>({place:places.find(p=>p.id===id)!,plans:sitePlans.filter(p=>p.placeIds[0]===id)}));
 const nearby=place?groups.filter(g=>g.place.region===place.region):groups;
 const shown=nearby.length?nearby:groups;
 return <section className="archaeology-catalog" aria-label="Archaeological candidate overview">
  <header><div><span className="small-caps">Entry {entry.id} · archaeological evidence</span><h2>{place?.shortName??entry.title}</h2><p>{entry.description}</p></div><button className="archaeology-terrain" onClick={onTerrain}><Mountain size={15}/>Regional terrain</button></header>
  <div className="archaeology-question"><div><span className="site-kind">Structure remains unresolved</span><h3>{entry.title}</h3><p>{entry.caution||"A specific excavated structure has not been assigned to this entry."}</p><p>The plans below show documented archaeological sites. They provide regional context; their buildings are not identified as this entry’s location.</p></div><div className="archaeology-question-actions"><button onClick={onRead}><BookOpen size={15}/>Read entry {entry.id}</button><button onClick={onDossier}>Candidate evidence <ChevronRight size={15}/></button></div></div>
  {dossier&&<details className="archaeology-local-records"><summary>Recorded structures at {dossier.name}</summary>{dossier.features.map(f=><article key={f.name}><span className="site-kind">{f.kind}</span><h3>{f.name}</h3><p>{f.observation}</p><p>{f.limit}</p></article>)}</details>}
  <h3 className="archaeology-section-title">{nearby.length?"Excavations in this region":"Available excavation plans"}</h3>
  <div className="archaeology-plan-grid">{shown.map(g=><article key={g.place.id}><div className="archaeology-preview"><PlanPreview plan={g.plans[0]}/></div><div className="archaeology-plan-copy"><span className="site-kind">Source-backed site plans</span><h3>{g.place.shortName}</h3><p>{g.plans[0].source}</p><small className="archaeology-credit">{g.plans[0].credit} {g.plans[0].licenseUrl&&<a href={g.plans[0].licenseUrl} target="_blank" rel="noreferrer">Licence</a>}</small><div>{g.plans.map(p=><button key={p.id} onClick={()=>onPlan(p)}>{p.label}<ChevronRight size={14}/></button>)}</div></div></article>)}</div>
 </section>;
}
