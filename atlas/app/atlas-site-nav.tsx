"use client";
import {useEffect,useRef} from 'react';
import {entryHash} from './atlas-navigation';
import {contextHash,type InspectionView} from './atlas-context-routes';
import './atlas-site-nav.css';
import './atlas-mobile.css';
import './atlas-clean.css';
export type AtlasSection='map'|'scroll'|'introduction';
export function sectionRoutes(entry:string,place?:string|null){const query=place?'?'+new URLSearchParams({place}).toString():'';return {introduction:'#what-is-the-copper-scroll',map:entryHash(entry,'2d')+query,scroll:entryHash(entry,'scroll')+query,compare:contextHash(entry,'compare',place)};}
export default function AtlasSiteNav({entry,active,record,place}:{entry:string;active:AtlasSection;record?:string|null;place?:string|null}){
 const routes=sectionRoutes(entry,place),menu=useRef<HTMLDetailsElement>(null);
 useEffect(()=>{
  const close=(event:PointerEvent)=>{if(menu.current&&!menu.current.contains(event.target as Node))menu.current.open=false;};
  const escape=(event:KeyboardEvent)=>{if(event.key==='Escape'&&menu.current?.open){event.preventDefault();menu.current.open=false;menu.current.querySelector('summary')?.focus();}};
  document.addEventListener('pointerdown',close);document.addEventListener('keydown',escape);
  return()=>{document.removeEventListener('pointerdown',close);document.removeEventListener('keydown',escape);};
 },[]);
 const tools:[InspectionView,string][]=[['graph','Connection graph'],['tests','Saved tests'],['impact','Change impact'],['sources','Source catalogue'],['names','Names & attestations']];
 return <header className="atlas-site-nav"><a className="atlas-site-brand" href="#home" aria-label="Copper Scroll home">Copper Scroll</a><nav aria-label="Atlas sections"><a className="atlas-intro-link" href={routes.introduction} aria-current={active==='introduction'?'page':undefined}>What is the Copper Scroll?</a>{(['map','scroll'] as const).map(id=><a key={id} href={routes[id]} aria-current={active===id?'page':undefined}>{id==='map'?'Map':'Scroll'}</a>)}</nav><details ref={menu} className="atlas-research-menu"><summary>Research tools</summary><div>{tools.map(([view,label])=><a key={view} href={contextHash(entry,view,place,view==='impact'?record:null,view==='names'?'scroll':active==='scroll'?'scroll':'2d')} onClick={()=>{if(menu.current)menu.current.open=false;}}>{label}</a>)}<a href={'#workbench/relationships?entry='+entry} onClick={()=>{if(menu.current)menu.current.open=false;}}>Feature workbench</a></div></details></header>;
}
