import type {KBData,KBRecord} from './atlas-kb-model';
type Catalogue={entries:{id:string;title:string;hebrew:string;description:string;landmark:string;region:string;candidates:{placeId:string}[]}[];places:{id:string;name:string;shortName:string}[]};
export type EntryFilters={text:string;region:string;feature:string;coverage:string};
export const emptyEntryFilters:EntryFilters={text:'',region:'',feature:'',coverage:''};
export const featureMentions=[
 {id:'cave',label:'Cave',pattern:/cave|cavern|cavity/i},
 {id:'pool',label:'Pool / basin',pattern:/pool|basin|reservoir/i},
 {id:'cistern',label:'Cistern',pattern:/cistern/i},
 {id:'pit',label:'Pit / shaft',pattern:/\bpit\b|shaft/i},
 {id:'grave',label:'Grave / tomb',pattern:/grave|tomb|burial/i},
 {id:'channel',label:'Channel / conduit',pattern:/channel|conduit|aqueduct|drain|pipe/i},
 {id:'steps',label:'Steps / stairs',pattern:/step|stair/i},
 {id:'wall',label:'Wall / gate',pattern:/wall|gate/i},
 {id:'spring',label:'Spring / well',pattern:/spring|\bwell\b/i},
 {id:'building',label:'Building / courtyard / ruin',pattern:/building|house|courtyard|court|ruin/i},
];
export const regionNames:Record<string,string>={jericho:'Jericho & Qumran',jerusalem:'Jerusalem',region:'Judean hills & north',unplaced:'Unplaced'};
export const searchForm=(v:string)=>v.normalize('NFD').replace(/\p{M}/gu,'').toLocaleLowerCase();
export function entryFilterRows(catalogue:Catalogue,kb:KBData){
 const places=new Map(catalogue.places.map(p=>[p.id,p]));
 return catalogue.entries.map(e=>{
  const sites=e.candidates.map(c=>places.get(c.placeId)).filter(Boolean).map(p=>p!.name+' '+p!.shortName).join(' ');
  const features=featureMentions.filter(f=>f.pattern.test(e.landmark+' '+e.description)).map(f=>f.id);
  return {...e,features,sites,hasComparison:(kb.entries[e.id]||[]).some(k=>k.startsWith('evaluation/')),search:searchForm([e.id,e.title,e.hebrew,e.description,e.landmark,sites].join(' '))};
 });
}
export function filterEntries(rows:ReturnType<typeof entryFilterRows>,f:EntryFilters){
 const terms=searchForm(f.text.trim()).split(/\s+/).filter(Boolean);
 return rows.filter(r=>terms.every(t=>r.search.includes(t))&&(!f.region||r.region===f.region)&&(!f.feature||r.features.includes(f.feature))&&(!f.coverage||(f.coverage==='comparisons'?r.hasComparison:!r.hasComparison)));
}
export type CandidateFilter='all'|'conflict'|'unknown'|'fits'|'review';
export function filterCandidateRows<T extends {candidate:KBRecord;result?:KBRecord}>(rows:T[],text:string,status:CandidateFilter):T[]{
 const terms=searchForm(text.trim()).split(/\s+/).filter(Boolean);
 return rows.filter(({candidate,result})=>{
  const searchable=searchForm(candidate.id+' '+candidate.label),checks=result?.payload.checks||[];
  if(!terms.every(t=>searchable.includes(t)))return false;
  if(status==='conflict')return checks.some((c:any)=>c.status==='contradicted');
  if(status==='unknown')return !result||!checks.length||checks.some((c:any)=>!['compatible','contradicted'].includes(c.status));
  if(status==='fits')return checks.length>0&&checks.every((c:any)=>c.status==='compatible');
  if(status==='review')return result?.payload.reassessment?.required===true;
  return true;
 });
}
