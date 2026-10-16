"use client";
import {Layers} from 'lucide-react';
import {entryHash} from './atlas-navigation';
import './atlas-site-nav.css';
import './atlas-mobile.css';
import './atlas-clean.css';
export type AtlasSection='evidence'|'map'|'scroll';
export function sectionRoutes(entry:string){
 return {evidence:'#kb?'+new URLSearchParams({entry,view:'case',detail:'0'}).toString(),map:entryHash(entry,'2d'),scroll:entryHash(entry,'scroll')};
}
export default function AtlasSiteNav({entry,active}:{entry:string;active:AtlasSection}){
 const routes=sectionRoutes(entry);
 const links:[AtlasSection,string][]=[['evidence','Evidence'],['map','Map'],['scroll','Scroll']];
 return <header className="atlas-site-nav"><a className="atlas-site-brand" href={routes.evidence}><Layers size={24}/><span>Copper Scroll</span></a><nav aria-label="Atlas sections">{links.map(([id,label])=><a key={id} href={routes[id]} aria-current={active===id?'page':undefined}>{label}</a>)}</nav></header>;
}
