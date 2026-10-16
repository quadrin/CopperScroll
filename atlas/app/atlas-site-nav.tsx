"use client";
import {useEffect,useRef} from 'react';
import {Layers,ChevronDown} from 'lucide-react';
import {entryHash} from './atlas-navigation';
import './atlas-site-nav.css';
import './atlas-mobile.css';
import './atlas-clean.css';
export type AtlasSection='evidence'|'map'|'sites'|'scroll'|'sources'|'tools';
export function sectionRoutes(entry:string,planId?:string|null){
 const kb=(view:string)=>'#kb?'+new URLSearchParams({entry,view,detail:'0'}).toString();
 return {evidence:kb('case'),map:entryHash(entry,'2d'),sites:`#entry-${entry}/site${planId?'/'+planId+'/source':''}`,scroll:entryHash(entry,'scroll'),sources:kb('sources'),tools:`#workbench/relationships?entry=${entry}`};
}
export default function AtlasSiteNav({entry,active,planId}:{entry:string;active:AtlasSection;planId?:string|null}){
 const routes=sectionRoutes(entry,planId);
 const directory=useRef<HTMLDetailsElement>(null);
 useEffect(()=>{const close=()=>directory.current?.removeAttribute("open");const outside=(e:PointerEvent)=>{if(!directory.current?.contains(e.target as Node))close()};const escape=(e:KeyboardEvent)=>{if(e.key==="Escape"&&directory.current?.open){close();directory.current.querySelector("summary")?.focus()}};document.addEventListener("pointerdown",outside);document.addEventListener("keydown",escape);window.addEventListener("hashchange",close);return()=>{document.removeEventListener("pointerdown",outside);document.removeEventListener("keydown",escape);window.removeEventListener("hashchange",close)}},[]);
 const links:[AtlasSection,string][]=[['evidence','Evidence'],['map','Map'],['sites','Sites & 3D'],['scroll','Scroll'],['sources','Sources'],['tools','Tools']];
 return <header className="atlas-site-nav"><a className="atlas-site-brand" href={routes.evidence}><Layers size={24}/><span>Copper Scroll</span></a><nav aria-label="Atlas sections">{links.filter(([id])=>['evidence','map','sources'].includes(id)).map(([id,label])=><a key={id} href={id==='sources'&&active==='map'?entryHash(entry,'dossier'):routes[id]} aria-current={active===id?'page':undefined}>{label}</a>)}</nav><details ref={directory} className="atlas-section-directory"><summary aria-label="More sections" aria-current={['sites','scroll','tools'].includes(active)?'page':undefined}>More<ChevronDown size={14}/></summary><div onClick={e=>{if((e.target as Element).closest('a'))e.currentTarget.closest('details')?.removeAttribute('open');}}>{links.filter(([id])=>['scroll','tools'].includes(id)).map(([id,label])=><a key={id} href={routes[id]}>{label}</a>)}<details><summary>Research views</summary><a href={entryHash(entry,'scene')}>Passage schematic</a>{['relationships','inventory','states','coverage','decisions'].map(id=><a key={id} href={`#workbench/${id}?entry=${entry}`}>{({relationships:'Pool & pit relationships',inventory:'Cave comparisons',states:'Historical states',coverage:'Evidence coverage',decisions:'Deciding observations'} as Record<string,string>)[id]}</a>)}<a href="https://github.com/quadrin/CopperScroll" target="_blank" rel="noreferrer">Project repository</a></details></div></details></header>;
}
