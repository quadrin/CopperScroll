"use client";
import {lazy,Suspense,useEffect,useLayoutEffect,useRef} from 'react';
import {X} from 'lucide-react';
import {inspectionLabels,type InspectionView} from './atlas-context-routes';
import './atlas-context-sheet.css';
const Content=lazy(()=>import('./atlas-context-evidence'));
type Props={entryId:string;entryTitle:string;placeId?:string|null;placeName?:string;view:InspectionView;record?:string|null;onView:(view:InspectionView)=>void;onRecord:(key:string)=>void;onClose:()=>void};
export default function ContextSheet({entryId,entryTitle,placeId,placeName,view,record,onView,onRecord,onClose}:Props){
 const close=useRef<HTMLButtonElement>(null);const lastClose=useRef(onClose);lastClose.current=onClose;
 const body=useRef<HTMLDivElement>(null),positions=useRef(new Map<string,number>());
 useLayoutEffect(()=>{
  const element=body.current,key=entryId+'|'+view+'|'+(record??'');
  if(element)element.scrollTop=positions.current.get(key)??0;
  return()=>{if(element)positions.current.set(key,element.scrollTop);};
 },[entryId,view,record]);
 useEffect(()=>{
  const previous=document.activeElement as HTMLElement|null;close.current?.focus();
  const escape=(event:KeyboardEvent)=>{if(event.key==='Escape'&&!event.defaultPrevented){event.preventDefault();lastClose.current();}};
  document.addEventListener('keydown',escape);
  return()=>{document.removeEventListener('keydown',escape);if(previous?.isConnected)previous.focus({preventScroll:true});else document.querySelector<HTMLElement>('.atlas-site-nav a[aria-current="page"]')?.focus({preventScroll:true});};
 },[]);
 const wide=['compare','graph','tests'].includes(view);
 return <aside className={'atlas-context-sheet'+(wide?' context-sheet-wide':'')} role="dialog" aria-modal="false" aria-labelledby="context-sheet-title" data-evidence-view={view}>
  <header><div><h2 id="context-sheet-title">{inspectionLabels[view]}</h2><p>{entryId} · {entryTitle}{view==='assessment'&&placeName?' / '+placeName:''}</p></div><button ref={close} type="button" onClick={onClose} aria-label="Close contextual evidence"><X size={20}/></button></header>
  <div ref={body} className="context-sheet-body"><Suspense fallback={<p role="status">Opening records…</p>}><Content key={entryId} entryId={entryId} view={view} record={record??undefined} placeId={placeId??undefined} onView={onView} onRecord={onRecord}/></Suspense></div>
 </aside>;
}
