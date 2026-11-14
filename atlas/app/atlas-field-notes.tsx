"use client";
import {useEffect,useState} from 'react';
import {ArrowUpRight} from 'lucide-react';
import AtlasSiteNav from './atlas-site-nav';
import {SECTIONS,PLACES,UNITS,CORRECTIONS,SUMMARY,REPO,FIGS,type Status} from './atlas-field-notes-data';
const base=import.meta.env?.BASE_URL??'/';
// The access-controlled build (Cloudflare Pages behind Cloudflare Access) carries media/field-notes/; the public build does not.
const PHOTO_SITE=((import.meta.env as unknown as Record<string,string|undefined>|undefined)?.VITE_WSRP_PHOTO_SITE)??'https://copper-scroll-photos.pages.dev/';
type Lib={files:string[]}|null;
import './atlas-field-notes.css';

const tone=(s:Status)=>({'Checked':'good','Holds':'good','Probable':'mid','Seen':'mid','Changed':'info','Corrected':'info','Possible':'weak','Not decided':'weak','Not testable':'weak','Not confirmed':'bad','Fails':'bad','No link':'neutral','Chance level':'neutral'} as Record<Status,string>)[s];
function Chip({s}:{s:Status}){return <span className={'fn-chip fn-'+tone(s)}>{s}</span>;}
function Figures({ids,lib,open}:{ids:string[];lib:Lib;open:(id:string)=>void}){
 if(lib===null)return <p className="fn-private">{ids.length} {ids.length===1?'figure':'figures'} in the access-controlled version{PHOTO_SITE?<> · <a href={PHOTO_SITE+'#field-notes'} target="_blank" rel="noreferrer">open</a></>:null}</p>;
 const have=ids.filter(id=>lib.files.includes(id+'.webp'));
 return <div className="fn-figs">{have.map(id=><button key={id} type="button" className="fn-fig" onClick={()=>open(id)} aria-label={'Enlarge: '+FIGS[id].caption}><img src={base+'media/field-notes/'+id+'.webp'} alt={FIGS[id].caption} loading="lazy"/></button>)}</div>;
}
function Ext({href,children}:{href:string;children:React.ReactNode}){return <a href={REPO+href} target="_blank" rel="noreferrer">{children}<ArrowUpRight size={13} aria-hidden="true"/></a>;}

export default function AtlasFieldNotes(){
 const [lib,setLib]=useState<Lib>(null),[big,setBig]=useState<string|null>(null);
 useEffect(()=>{fetch(base+'media/field-notes/index.json',{cache:'no-store'}).then(r=>r.ok?r.json():null).then(j=>setLib(j&&Array.isArray(j.files)?j:null)).catch(()=>setLib(null));},[]);
 useEffect(()=>{if(!big)return;const k=(e:KeyboardEvent)=>{if(e.key==='Escape')setBig(null);};document.addEventListener('keydown',k);return()=>document.removeEventListener('keydown',k);},[big]);
 useEffect(()=>{document.title='Field notes · Copper Scroll Atlas';window.scrollTo(0,0);return()=>{document.title='The Copper Scroll Atlas';};},[]);
 return <div className="atlas-field-notes">
  <AtlasSiteNav entry="21" active="notes"/>
  <main>
   <header className="fn-head">
    <p className="fn-kicker">Field notes · 13–14 November 2026</p>
    <h1>Latest checks</h1>
    <p className="fn-lede">Results of the work with other methods: air photographs of 1918, satellite images of 1974–1978, survey books, and an audit of the Koḥlit count. Each item links to its note in the repository.</p>
    <ul className="fn-summary">{SUMMARY.filter((_,i)=>lib===null||i<2).map(s=><li key={s}>{s}</li>)}{lib!==null&&<li>This is the access-controlled version: the figures are private study copies. Do not share them.</li>}</ul>
    <nav className="fn-toc" aria-label="On this page">{[...SECTIONS.map(s=>[s.id,s.title]),['places','Places table'],['units','Koḥlit units'],['corrections','Corrections']].map(([id,t])=><a key={id} href={'#field-notes'} onClick={e=>{e.preventDefault();document.getElementById('fn-'+id)?.scrollIntoView({behavior:'smooth'});}}>{t}</a>)}</nav>
   </header>

   {SECTIONS.map(sec=><section key={sec.id} id={'fn-'+sec.id} className="fn-section" aria-labelledby={'fn-h-'+sec.id}>
    <h2 id={'fn-h-'+sec.id}>{sec.title}</h2>
    {sec.intro&&<p className="fn-intro">{sec.intro}</p>}
    <div className="fn-cards">{sec.notes.map(n=><article key={n.title} className="fn-card">
     <div className="fn-card-top"><span className="fn-date">{n.date}</span>{n.status&&<Chip s={n.status}/>}</div>
     <h3>{n.title}</h3>
     <p>{n.text}</p>
     {n.figs&&<Figures ids={n.figs} lib={lib} open={setBig}/>}
     {n.links&&<p className="fn-links">{n.links.map(([l,h])=><Ext key={h} href={h}>{l}</Ext>)}</p>}
    </article>)}</div>
   </section>)}

   <section id="fn-places" className="fn-section" aria-labelledby="fn-h-places">
    <h2 id="fn-h-places">Places table</h2>
    <p className="fn-intro">Status words: Checked, Probable, Possible, Seen, Not confirmed. PG = Palestine Grid (km).</p>
    <div className="fn-table-wrap"><table className="fn-table"><thead><tr><th>Place</th><th>Status</th><th>Position</th><th>Basis</th></tr></thead>
     <tbody>{PLACES.map(r=><tr key={r.place}><td>{r.place}</td><td><Chip s={r.status}/></td><td className="fn-num">{r.position}</td><td>{r.source}</td></tr>)}</tbody></table></div>
   </section>

   <section id="fn-units" className="fn-section" aria-labelledby="fn-h-units">
    <h2 id="fn-h-units">Koḥlit units checked by hand</h2>
    <p className="fn-intro">Sectors: east 45–135°, north 315–45°; limit 1000 m. The registered count is not changed.</p>
    <div className="fn-table-wrap"><table className="fn-table"><thead><tr><th>Unit</th><th>Name</th><th>Before</th><th>Now</th><th>Why</th></tr></thead>
     <tbody>{UNITS.map(r=><tr key={r.unit}><td className="fn-num">{r.unit}</td><td>{r.name}</td><td>{r.before}</td><td><Chip s={r.now}/></td><td>{r.why}</td></tr>)}</tbody></table></div>
   </section>

   <section id="fn-corrections" className="fn-section" aria-labelledby="fn-h-corrections">
    <h2 id="fn-h-corrections">Corrections of earlier statements</h2>
    <p className="fn-intro">From the edit log, which keeps each earlier value and the reason for the change.</p>
    <ul className="fn-corr">{CORRECTIONS.map(([id,t])=><li key={id+t}><span className="fn-num">{id}</span>{t}</li>)}</ul>
    <p className="fn-links"><Ext href="research/sources/hexagon_registration_2026-11-11/edit_log_location_grades_and_image_statuses.md">Full edit log</Ext></p>
   </section>
  </main>
  {big&&<div className="fn-lightbox" role="dialog" aria-modal="true" aria-label={FIGS[big].caption} onClick={()=>setBig(null)}><figure onClick={e=>e.stopPropagation()}><img src={base+'media/field-notes/'+big+'.webp'} alt={FIGS[big].caption}/><figcaption>{FIGS[big].caption}<span>{FIGS[big].credit}</span></figcaption><button type="button" onClick={()=>setBig(null)}>Close</button></figure></div>}
 </div>;
}
