// Pure evidence traversal shared by the landing page and its semantic checks.
export type KBRecord = {key:string; id:string; kind:string; label:string; payload:Record<string,any>; locators:Record<string,any>[]; exposure:string; review_status:string; visibility:string};
export type KBEdge = {subject:string; relation:string; object:string};
export type KBData = {version:string; records:KBRecord[]; edges:KBEdge[]; entries:Record<string,string[]>; dependency_relations:string[]};
export type KBIndex = {data:KBData; by:Map<string,KBRecord>; out:Map<string,KBEdge[]>; incoming:Map<string,KBEdge[]>};
export const stages = ['Text & readings','Requirements','Candidates & features','Claims & observations','Sources'] as const;
export function stage(r:KBRecord){
 if(['entry','reading_set','reading','interpretation','translation','restoration','locus','witness','segment','image','name','occurrence','entity'].includes(r.kind))return 0;
 if(['requirement','branch'].includes(r.kind))return 1;
 if(['hypothesis','feature','state','event','frame','identity'].includes(r.kind))return 2;
 if(['claim','observation','gap','acquisition','evaluation','test','coverage','search'].includes(r.kind))return 3;
 return 4;
}
export function index(data:KBData):KBIndex {
 const by=new Map(data.records.map(r=>[r.key,r]));const out=new Map<string,KBEdge[]>(),incoming=new Map<string,KBEdge[]>();
 for(const e of data.edges){out.set(e.subject,[...(out.get(e.subject)||[]),e]);incoming.set(e.object,[...(incoming.get(e.object)||[]),e]);}
 return {data,by,out,incoming};
}
export function entryContext(i:KBIndex,id:string){
 const keys=new Set(i.data.entries[id]||['entry/'+id]);
 // Individually addressed edition readings and interpretations inherit their
 // parent reading-set's entry, without merging alternative branches.
 for(let pass=0;pass<3;pass++)for(const e of i.data.edges){
  const subject=i.by.get(e.subject);if(!subject)continue;
  if(keys.has(e.object)&&['reading','interpretation','restoration','translation'].includes(subject.kind))keys.add(e.subject);
 }
 for(const k of [...keys])for(const e of i.out.get(k)||[])if(['cites','derived_from','requires','assigns','prerequisite','uses_frame'].includes(e.relation))keys.add(e.object);
 return [...keys].map(k=>i.by.get(k)).filter(Boolean) as KBRecord[];
}
export function impact(i:KBIndex,key:string){
 const paths=new Map<string,KBEdge[]>([[key,[]]]),queue=[key];const permitted=new Set(i.data.dependency_relations);
 while(queue.length){const current=queue.shift()!;for(const e of i.incoming.get(current)||[]){
  if(!permitted.has(e.relation))continue;
  if(e.relation==='under_branch'&&i.by.get(e.subject)?.kind==='requirement'&&'required_for' in i.by.get(e.subject)!.payload)continue;
  if(!paths.has(e.subject)){paths.set(e.subject,[...paths.get(current)!,e]);queue.push(e.subject);}
 }}
 return [...paths].filter(([k])=>k!==key).map(([key,path])=>({record:i.by.get(key)!,path}));
}
export function evidence(i:KBIndex,key:string){
 const seen=new Set<string>(),queue=[key];while(queue.length){const k=queue.shift()!;if(seen.has(k))continue;seen.add(k);for(const e of i.out.get(k)||[])queue.push(e.object);}
 return [...seen].map(k=>i.by.get(k)!).filter(Boolean);
}
export function displayValue(value:any):string {
 if(value===null||value===undefined)return 'Unestablished';
 if(typeof value==='boolean')return value?'Yes':'No';
 if(typeof value==='object')return JSON.stringify(value,null,2);
 return String(value);
}
export function brief(r:KBRecord){const p=r.payload;return p.meaning||p.detail||p.citation||p.summary||p.record_needed||p.uncertainty||p.target_prerequisites||(typeof p.value==='string'?p.value:'')||p.note||p.context||r.label;}
export function locatorLabel(l:Record<string,any>){return [l.printed_page!=null?'p. '+l.printed_page:null,l.pdf_page!=null?'PDF '+l.pdf_page:null,l.figure,l.archival_identifier,l.image_region].filter(Boolean).join(' · ');}
export function recordUrl(r:KBRecord){const l=r.locators[0];return 'https://github.com/quadrin/CopperScroll/blob/main/'+l.repo_path;}
export function graphRecords(i:KBIndex,id:string,selected:string,focus=false){
 const context=entryContext(i,id);let pool=context;
 if(focus){const keys=new Set([selected]);for(const e of [...i.out.get(selected)||[],...i.incoming.get(selected)||[]]){keys.add(e.subject);keys.add(e.object);}pool=[...keys].map(k=>i.by.get(k)!).filter(Boolean);}
 const allowed=new Set(['entry','reading_set','reading','interpretation','requirement','hypothesis','feature','state','claim','observation','source','gap','branch','evaluation']);
 const neighbors=new Set([...(i.out.get(selected)||[]).map(e=>e.object),...(i.incoming.get(selected)||[]).map(e=>e.subject)]);
 const score=(r:KBRecord)=>r.key===selected?-100:neighbors.has(r.key)?-80:r.kind==='reading_set'?-30:r.kind==='hypothesis'?-20:r.kind==='requirement'?-15:r.kind==='claim'?-8:0;
 const chosen:KBRecord[]=[];
 for(let s=0;s<5;s++)chosen.push(...pool.filter(r=>stage(r)===s&&allowed.has(r.kind)).sort((a,b)=>score(a)-score(b)||a.key.localeCompare(b.key)).slice(0,6));
 if(!chosen.some(r=>r.key===selected)&&i.by.has(selected))chosen.push(i.by.get(selected)!);
 const keys=new Set(chosen.map(r=>r.key));
 return {records:chosen,edges:i.data.edges.filter(e=>keys.has(e.subject)&&keys.has(e.object)&&e.relation!=='in_entry'),total:pool.length};
}
export const isKBRoute=(hash:string)=>!hash||hash==='#'||hash==='#kb'||hash.startsWith('#kb?');

// A comparison never substitutes a candidate's best result from another branch
// or period. Missing cells remain missing, including for controls.
export function comparisonKey(r:KBRecord){return JSON.stringify([r.payload.branch_key,r.payload.window_id||'']);}
export function comparisonChoices(i:KBIndex,candidates:KBRecord[]){
 const keys=new Set(candidates.map(r=>r.key)),seen=new Set<string>();
 return i.data.records.filter(r=>r.kind==='evaluation'&&keys.has(r.payload.hypothesis_key)).filter(r=>{const key=comparisonKey(r);if(seen.has(key))return false;seen.add(key);return true;}).map(r=>({key:comparisonKey(r),branch:r.payload.branch_key as string,window:r.payload.window_id||''}));
}
export function comparisonRows(i:KBIndex,candidates:KBRecord[],choice:string){
 return candidates.map(candidate=>{const matches=i.data.records.filter(r=>r.kind==='evaluation'&&r.payload.hypothesis_key===candidate.key&&comparisonKey(r)===choice);if(matches.length>1)throw new Error('Ambiguous saved comparison: '+candidate.key);return {candidate,result:matches[0]};});
}
export function branchLabel(r:KBRecord|undefined){
 if(!r)return 'Unestablished branch';const p=r.payload.choices||r.payload;
 if(!p.reading)return r.label;
 const reading=String(p.reading).replace('B-PILLAR','Pillar').replace('B-TERRACE','Terrace');
 return [reading,p.orientation==='both-mouths'?'both mouths face east':p.orientation==='cave'?'cave faces east':p.orientation,p.unit?`${p.unit} m cubit`:null,p.direction,p.phase,p.deposit?.replaceAll('-',' '),p.ruleset==='primary'?'primary rule':p.ruleset].filter(Boolean).join(' · ');
}
