"use client";
import {useEffect,useRef} from 'react';
import {ArrowUpRight} from 'lucide-react';
import {mountCopperPlate} from './atlas-landing-plate';
import {sectionRoutes} from './atlas-site-nav';
import translation from '../../text/translation_en.json';
import './atlas-landing.css';

const base=import.meta.env?.BASE_URL??'/';
const passageLines=['VI 1','VI 2','VI 3','VI 4','VI 5','VI 6'] as const;

function CopperPlate(){
 const canvas=useRef<HTMLCanvasElement>(null);
 useEffect(()=>{if(canvas.current)return mountCopperPlate(canvas.current);},[]);
 return <canvas ref={canvas} width="900" height="408" role="img" aria-label="Illustration of the opening four lines of the Copper Scroll engraved in copper, with changing light. This is a simulation, not a manuscript photograph."/>;
}
export default function AtlasLanding({entry='21'}:{entry?:string}){
 const routes=sectionRoutes(entry);
 const exampleRoutes=sectionRoutes('25');
 return <div className="atlas-landing">
  <a className="landing-skip" href="#landing-introduction" onClick={event=>{event.preventDefault();const introduction=document.getElementById('landing-introduction');introduction?.focus();introduction?.scrollIntoView();}}>Skip to introduction</a>
  <header className="landing-header">
   <a className="landing-brand" href="#home" aria-label="Copper Scroll Atlas home">Copper Scroll</a>
   <nav aria-label="Atlas sections"><a className="atlas-intro-link" href={routes.introduction}>What is the Copper Scroll?</a><a href={routes.map}>Map</a><a href={routes.scroll}>Scroll</a></nav>
  </header>
  <main>
   <section className="landing-hero" aria-labelledby="landing-title">
    <div className="landing-plate"><CopperPlate/></div>
    <div className="landing-shade"/>
    <div className="landing-hero-text">
     <p className="landing-object-id">3Q15</p>
     <h1 id="landing-title">The Copper Scroll</h1>
     <p>Text, sites, and archaeological evidence.</p>
     <a className="landing-primary" href={routes.map}>Open atlas <ArrowUpRight size={18} aria-hidden="true"/></a>
    </div>
    <span className="landing-art-label">Copper illustration · move the light</span>
   </section>
   <section id="landing-introduction" tabIndex={-1} className="landing-introduction" aria-labelledby="landing-intro-title">
    <div className="landing-passage">
     <p className="landing-source-label">Entry 25 · Column VI, lines 1–6</p>
     <h2 id="landing-intro-title">The cave of the pillar</h2>
     <blockquote>{passageLines.map(ref=><p key={ref}><span>{ref}</span>{translation[ref]}</p>)}</blockquote>
     <p className="landing-caption">Project translation. Brackets mark restored letters. <a href={exampleRoutes.scroll}>Read in context</a></p>
     <p className="landing-comparison">Cave IV/17 is one proposed match. The ancient entrances, thresholds and construction phases remain unresolved. <a href={exampleRoutes.compare}>Compare the candidates <ArrowUpRight size={14} aria-hidden="true"/></a></p>
    </div>
    <figure className="landing-source-plan">
     <a href={`${base}dossiers/sion2002-plan5-iv17.webp`} aria-label="Open the published IV/17 excavation plan"><img src={`${base}dossiers/sion2002-plan5-iv17.webp`} alt="Complete published plan of cave IV/17, with its original caption, scale and north arrow." loading="lazy"/></a>
     <figcaption><p>IV/17 · Sion 2002, <cite>ʿAtiqot</cite> 41, Plan 5, p. 63.</p><p>Ofer Sion / Israel Antiquities Authority · <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>. Original figure caption, scale and north arrow retained. Geographic registration is unresolved. <a href="https://publications.iaa.org.il/atiqot/vol41/iss1/6/">Publication</a></p></figcaption>
    </figure>
   </section>
  </main>
  <footer className="landing-footer"><p>Candidate locations are hypotheses. A landmark match does not establish a surviving deposit.</p><p>Copper illustration adapted from <cite>Copper Scroll Experimental Approaches</cite>; simulated surface. Hebrew: M. G. Abegg Jr.’s transcription, <a href="https://github.com/ETCBC/dss">ETCBC</a>, <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>.</p></footer>
 </div>;
}
