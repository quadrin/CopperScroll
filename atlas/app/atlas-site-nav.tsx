"use client";
import {Layers,ChevronDown} from 'lucide-react';
import {entryHash} from './atlas-navigation';
import './atlas-site-nav.css';
export type AtlasSection='evidence'|'map'|'sites'|'scroll'|'sources'|'tools';
export function sectionRoutes(entry:string,planId?:string|null){
 const kb=(view:string)=>'#kb?'+new URLSearchParams({entry,view,detail:'0'}).toString();
 return {evidence:kb('case'),map:entryHash(entry,'2d'),sites:`#entry-${entry}/site${planId?'/'+planId:''}`,scroll:entryHash(entry,'scroll'),sources:kb('sources'),tools:`#workbench/relationships?entry=${entry}`};
}
export default function AtlasSiteNav({entry,active,planId}:{entry:string;active:AtlasSection;planId?:string|null}){
 const routes=sectionRoutes(entry,planId);
 const links:[AtlasSection,string][]=[['evidence','Evidence'],['map','Map'],['sites','Sites & 3D'],['scroll','Scroll'],['sources','Sources'],['tools','Tools']];
 return <header className="atlas-site-nav"><a className="atlas-site-brand" href={routes.evidence}><Layers size={24}/><span>Copper Scroll<small>RESEARCH ATLAS · 3Q15</small></span></a><nav aria-label="Atlas sections">{links.map(([id,label])=><a key={id} href={routes[id]} aria-current={active===id?'page':undefined}>{label}</a>)}</nav><details className="atlas-section-directory"><summary>All sections<ChevronDown size={14}/></summary><div onClick={e=>{if((e.target as Element).closest('a'))e.currentTarget.closest('details')?.removeAttribute('open');}}><span>Entry {entry} · direct routes</span>{links.map(([id,label])=><a key={id} href={routes[id]}>{label}</a>)}<a href={entryHash(entry,'3d')}>Regional terrain</a><a href={entryHash(entry,'ground')}>Site photographs</a><a href={entryHash(entry,'dossier')}>Candidate dossier</a><a href={entryHash(entry,'landscape')}>Historical maps & imagery</a><a href={entryHash(entry,'scene')}>Passage schematic</a>{planId&&<a href={`#entry-${entry}/site/${planId}/walk`}>Eye-level simulation</a>}<span>Research tools</span>{['relationships','inventory','states','coverage','decisions'].map(id=><a key={id} href={`#workbench/${id}?entry=${entry}`}>{({relationships:'Pool & pit relationships',inventory:'Cave comparisons',states:'Historical states',coverage:'Evidence coverage',decisions:'Deciding observations'} as Record<string,string>)[id]}</a>)}<a href="https://github.com/quadrin/CopperScroll" target="_blank" rel="noreferrer">Project repository</a></div></details></header>;
}
