import type {KBRecord} from './atlas-kb-model';
export const searchForm=(value:string)=>value.normalize('NFD').replace(/\p{M}/gu,'').toLocaleLowerCase();
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
