"use client";
import {useMemo,useState} from 'react';
import {ChevronDown,SlidersHorizontal,ArrowRight} from 'lucide-react';
import catalogue from './atlas-data.json';
import type {KBData} from './atlas-kb-model';
import {entryFilterRows,filterEntries,emptyEntryFilters,featureMentions,regionNames} from './atlas-kb-filters-model';
import './atlas-kb-filters.css';

export default function EntryFinder({data,current,onChoose}:{data:KBData|null;current:string;onChoose:(id:string)=>void}){
 const [open,setOpen]=useState(false),[filters,setFilters]=useState({...emptyEntryFilters});
 const rows=useMemo(()=>data?entryFilterRows(catalogue,data):[],[data]);
 const matches=useMemo(()=>filterEntries(rows,filters),[rows,filters]);
 const active=Object.values(filters).filter(Boolean).length;
 const regions=[...new Set(rows.map(r=>r.region))];
 const set=(key:keyof typeof filters,value:string)=>setFilters(f=>({...f,[key]:value}));
 return <section className="kb-entry-finder" aria-label="Filter atlas entries">
  <button className="kb-filter-disclosure" aria-expanded={open} aria-controls="kb-entry-filters" onClick={()=>setOpen(v=>!v)}><SlidersHorizontal size={17}/><span>Filter entries</span>{active>0&&<strong>{matches.length} / {rows.length}</strong>}<ChevronDown size={16}/></button>
  {active>0&&!open&&<p className="kb-filter-summary">{matches.length} entries match your filters. <button onClick={()=>setFilters({...emptyEntryFilters})}>Clear filters</button></p>}
  {open&&<div id="kb-entry-filters" className="kb-filter-panel">
   <div className="kb-entry-filter-controls"><label>Entry, place or landmark<input type="search" aria-label="Filter entries by text" placeholder="e.g. Koḥlit, Qumran, IV/17…" value={filters.text} onChange={e=>set('text',e.target.value)}/></label><label>Region<select aria-label="Filter entries by region" value={filters.region} onChange={e=>set('region',e.target.value)}><option value="">All regions</option>{regions.map(r=><option key={r} value={r}>{regionNames[r]||r}</option>)}</select></label><label>Feature mentioned<select aria-label="Filter entries by feature" value={filters.feature} onChange={e=>set('feature',e.target.value)}><option value="">All features</option>{featureMentions.map(f=><option key={f.id} value={f.id}>{f.label}</option>)}</select></label><label>KB coverage<select aria-label="Filter entries by coverage" value={filters.coverage} onChange={e=>set('coverage',e.target.value)}><option value="">All entries</option><option value="comparisons">Saved candidate comparisons</option><option value="passage">No saved candidate comparison</option></select></label></div>
   <div className="kb-filter-results-heading"><p role="status">{data?`${matches.length} of ${rows.length} entries`:'Loading entry register…'}</p><button disabled={!active} onClick={()=>setFilters({...emptyEntryFilters})}>Clear filters</button></div>
   <p className="kb-filter-explanation">Feature filters search the passage descriptions. Choose a result to open it; the current passage stays open until then.</p>
   <div className="kb-entry-filter-results" aria-label="Matching entries">{matches.map(r=><button key={r.id} aria-current={r.id===current?'page':undefined} onClick={()=>onChoose(r.id)}><span>{r.id}</span><span><strong>{r.title}</strong><small>{regionNames[r.region]||r.region} · {r.hasComparison?'Saved comparisons':'Passage register'}</small></span><ArrowRight size={15}/></button>)}{data&&!matches.length&&<p>No entries match these filters. Clear a filter to broaden the results.</p>}</div>
  </div>}
 </section>;
}
