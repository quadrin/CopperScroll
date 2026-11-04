"use client";
import {useEffect,useRef,useState,type RefObject} from 'react';

/** Read only while the sticky stage is in view and the tab is visible. */
export function useReadingStage(ref:RefObject<HTMLDivElement|null>){
 const [visible,setVisible]=useState(false);
 useEffect(()=>{const node=ref.current?.querySelector(':scope > .story-sticky');if(!node)return;const observer=new IntersectionObserver(([entry])=>setVisible(entry.intersectionRatio>.85),{threshold:[0,.85,1]});observer.observe(node);return()=>observer.disconnect();},[ref]);
 return visible;
}
export function useReadingTime(active:boolean,reduced:boolean,resetKey:string|number){
 const elapsed=useRef(0),[frame,setFrame]=useState({key:resetKey,time:0});
 useEffect(()=>{elapsed.current=0;setFrame({key:resetKey,time:0});},[resetKey,reduced]);
 useEffect(()=>{
  if(!active||reduced)return;let last=performance.now();
  const tick=()=>{const now=performance.now();if(!document.hidden){elapsed.current+=Math.min(250,now-last);setFrame({key:resetKey,time:elapsed.current});}last=now;};
  const visibility=()=>{last=performance.now();};document.addEventListener('visibilitychange',visibility);
  const timer=window.setInterval(tick,80);return()=>{window.clearInterval(timer);document.removeEventListener('visibilitychange',visibility);};
 },[active,reduced,resetKey]);
 return frame.key===resetKey?frame.time:0;
}
export function PassageLines({lines,language,active,reduced}:{lines:string[];language:'he'|'en';active:boolean;reduced:boolean}){
 const time=useReadingTime(active,reduced,language),lead=1800,hold=language==='he'?2400:3400,exit=700,cycle=hold+exit;
 const complete=!reduced&&time>=lead+cycle*lines.length;
 return <div className={`story-passage-lines${complete?' is-complete':''}`} data-language={language} data-complete={complete} data-running={active&&!reduced}>
  {lines.map((line,i)=>{const local=time-lead-i*cycle,state=reduced||complete?'overview':local<0?'queued':local<hold?'reading':local<cycle?'leaving':'gone';return <p key={`${complete}-${i}`} className="story-passage-line" data-line={i} data-state={state}>{line}</p>;})}
 </div>;
}
