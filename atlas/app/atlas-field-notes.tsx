"use client";
import {useEffect,useState} from 'react';
import AtlasSiteNav from './atlas-site-nav';
import {CHAPTERS,OTHER,PLACES,UNITS,REPO,FIGS,type Entry,type Status} from './atlas-field-notes-data';
import './atlas-field-notes.css';

const base=import.meta.env?.BASE_URL??'/';
// The access-controlled build (Cloudflare Pages behind Cloudflare Access) carries media/field-notes/; the public build does not.
const PHOTO_SITE=((import.meta.env as unknown as Record<string,string|undefined>|undefined)?.VITE_WSRP_PHOTO_SITE)??'https://copper-scroll-photos.pages.dev/';
type Lib={files:string[]}|null;
const ROMAN=['i','ii','iii','iv','v','vi'];
const tone=(s:Status)=>({'Checked':'good','Holds':'good','Probable':'mid','Seen':'mid','Possible':'weak','Not decided':'weak','Not testable':'weak','Not confirmed':'bad','Fails':'bad','No link':'plain','Chance level':'plain'} as Record<Status,string>)[s];

export function useFieldMedia(){
 const [lib,setLib]=useState<Lib>(null);
 useEffect(()=>{fetch(base+'media/field-notes/index.json',{cache:'no-store'}).then(r=>r.ok?r.json() as Promise<{files?:unknown}>:null).then(j=>setLib(j&&Array.isArray(j.files)?{files:j.files as string[]}:null)).catch(()=>setLib(null));},[]);
 return lib;
}

function Figure({id,lib,open}:{id:string;lib:Lib;open:(id:string)=>void}){
 const f=FIGS[id];
 if(lib===null||!lib.files.includes(id+'.webp'))return null;
 return <figure className="fa-fig"><button type="button" onClick={()=>open(id)} aria-label={'Enlarge: '+f.caption}><img src={base+'media/field-notes/'+id+'.webp'} alt={f.caption} loading="lazy"/></button><figcaption>{f.caption} <i>{f.credit}.</i></figcaption></figure>;
}

function Record({e,lib,open}:{e:Entry;lib:Lib;open:(id:string)=>void}){
 const n=e.figs?.length??0;
 return <article className="fa-entry" id={'fa-'+e.id}>
  <div className="fa-margin">
   {e.sit&&<span className="fa-sc">{e.sit.toLowerCase()}</span>}
   <span className={'fa-status fa-'+tone(e.status)}>{e.status.toLowerCase()}</span>
   <span className="fa-sc fa-date">{e.date}</span>
  </div>
  <div className="fa-main">
   <h3>{e.name}</h3>
   {e.sub&&<p className="fa-sub">{e.sub}</p>}
   {e.body.map((p,i)=><p key={i}>{p}</p>)}
   {e.tasks&&<ul className="fa-tasks">{e.tasks.map(t=><li key={t}>{t}</li>)}</ul>}
   {n>0&&(lib===null
    ?<p className="fa-private">{n===1?'One figure':n+' figures'} in the access-controlled version{PHOTO_SITE&&<> · <a href={PHOTO_SITE+'#field-notes'} target="_blank" rel="noreferrer">open</a></>}.</p>
    :e.figs!.map(id=><Figure key={id} id={id} lib={lib} open={open}/>))}
   {e.sources&&<p className="fa-src"><span className="fa-sc">source</span> {e.sources.map(([l,h],i)=><span key={h}>{i>0&&' · '}<a href={REPO+h} target="_blank" rel="noreferrer">{l}</a></span>)}</p>}
  </div>
 </article>;
}

export function AtlasPage({children,title}:{children:React.ReactNode;title:string}){
 useEffect(()=>{document.title=title+' · Copper Scroll Atlas';window.scrollTo(0,0);return()=>{document.title='The Copper Scroll Atlas';};},[title]);
 return <div className="field-atlas"><AtlasSiteNav entry="21" active="notes"/><main>{children}</main></div>;
}

const jump=(id:string)=>(ev:React.MouseEvent)=>{ev.preventDefault();document.getElementById(id)?.scrollIntoView({behavior:'smooth'});};

export default function AtlasFieldNotes(){
 const lib=useFieldMedia(),[big,setBig]=useState<string|null>(null);
 useEffect(()=>{if(!big)return;const k=(e:KeyboardEvent)=>{if(e.key==='Escape')setBig(null);};document.addEventListener('keydown',k);return()=>document.removeEventListener('keydown',k);},[big]);
 return <AtlasPage title="Field notes">
  <header className="fa-title">
   <p className="fa-sc fa-spaced">The Copper Scroll</p>
   <span className="fa-rule"/>
   <h1>Field notes</h1>
   <p className="fa-subtitle">places checked on air photographs of 1918, satellite images of 1974–1978 and in the survey books</p>
   <p className="fa-edition"><span className="fa-sc">copper scroll project</span><br/>Notes of 13–14 November 2026<br/><i>{lib===null?'Figures are in the access-controlled version only.':'Access-controlled version: the figures are private study copies.'}</i></p>
   <nav className="fa-contents" aria-label="Chapters">
    {CHAPTERS.map((c,i)=><a key={c.id} href="#field-notes" onClick={jump('fa-ch-'+c.id)}><span className="fa-sc">{ROMAN[i]}</span> {c.title}</a>)}
    <a href="#field-notes" onClick={jump('fa-ch-other')}><span className="fa-sc">{ROMAN[CHAPTERS.length]}</span> Other work without a place</a>
    <a href="#field-notes" onClick={jump('fa-register')}><span className="fa-sc">reg.</span> Register of places and units</a>
    <a href="#changelog"><span className="fa-sc">log</span> Changelog</a>
   </nav>
  </header>

  {CHAPTERS.map((c,i)=><section key={c.id} id={'fa-ch-'+c.id} className="fa-chapter" aria-labelledby={'fa-h-'+c.id}>
   <h2 id={'fa-h-'+c.id}><span>{ROMAN[i]}</span>{c.title}</h2>
   {c.entries.map(e=><Record key={e.id} e={e} lib={lib} open={setBig}/>)}
  </section>)}

  <section id="fa-ch-other" className="fa-chapter" aria-labelledby="fa-h-other">
   <h2 id="fa-h-other"><span>{ROMAN[CHAPTERS.length]}</span>Other work without a place</h2>
   {OTHER.map(e=><Record key={e.id} e={e} lib={lib} open={setBig}/>)}
  </section>

  <section id="fa-register" className="fa-chapter" aria-labelledby="fa-h-reg">
   <h2 id="fa-h-reg"><span>reg.</span>Register</h2>
   <p className="fa-note">Status words: Checked, Probable, Possible, Seen, Not confirmed. PG = Palestine Grid (km). Positions from the height models of the images.</p>
   <table className="fa-reg"><thead><tr><th>Place</th><th>Status</th><th>Position</th><th>Images</th></tr></thead>
    <tbody>{PLACES.map(r=><tr key={r.place}><td>{r.place}</td><td><i className={'fa-'+tone(r.status)}>{r.status}</i></td><td className="fa-num">{r.position}</td><td>{r.source}</td></tr>)}</tbody></table>
   <h3 className="fa-reg-h">Koḥlit units checked by hand</h3>
   <p className="fa-note">Beside the registered count, which is not changed. Sectors: east 45–135°, north 315–45°; limit 1000 m. The other 14 units with two of three conditions hold with margins of 130 m or more.</p>
   <table className="fa-reg"><thead><tr><th>Unit</th><th>Name</th><th>Result</th><th>Reason</th></tr></thead>
    <tbody>{UNITS.map(r=><tr key={r.unit}><td className="fa-sc">{r.unit.toLowerCase()}</td><td>{r.name}</td><td><i className={'fa-'+tone(r.result)}>{r.result}</i></td><td>{r.why}</td></tr>)}</tbody></table>
   <p className="fa-end">What changed in these days, with the earlier values and the corrections, is in the <a href="#changelog">changelog</a>. No rating, candidate or strength of a match was changed.</p>
  </section>

  {big&&<div className="fa-lightbox" role="dialog" aria-modal="true" aria-label={FIGS[big].caption} onClick={()=>setBig(null)}><figure onClick={e=>e.stopPropagation()}><img src={base+'media/field-notes/'+big+'.webp'} alt={FIGS[big].caption}/><figcaption>{FIGS[big].caption} <i>{FIGS[big].credit}.</i></figcaption><button type="button" onClick={()=>setBig(null)}>Close</button></figure></div>}
 </AtlasPage>;
}
