"use client";
import {useEffect,useRef,useState} from 'react';
import {AnimatedWords} from './atlas-intro-words';

// The document's scroll position is the timeline. There is no autoplay clock:
// stopping freezes the artwork; reversing scroll reverses the same sequence.
export function useScrollScene(){
 const ref=useRef<HTMLDivElement>(null);
 const [value,setValue]=useState(0),[reduced,setReduced]=useState(false);
 useEffect(()=>{
  const query=matchMedia('(prefers-reduced-motion: reduce)');let frame=0;
  const update=()=>{frame=0;const el=ref.current;if(!el)return;const rect=el.getBoundingClientRect(),travel=Math.max(1,rect.height-innerHeight);setValue(query.matches?1:Math.max(0,Math.min(1,-rect.top/travel)));};
  const schedule=()=>{if(!frame)frame=requestAnimationFrame(update);};
  const preference=()=>{setReduced(query.matches);schedule();};
  preference();window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);query.addEventListener('change',preference);
  const observer=new ResizeObserver(schedule);if(ref.current)observer.observe(ref.current);
  return()=>{cancelAnimationFrame(frame);observer.disconnect();window.removeEventListener('scroll',schedule);window.removeEventListener('resize',schedule);query.removeEventListener('change',preference);};
 },[]);
 return {ref,value,reduced};
}
export function stepAt(value:number,count:number){return Math.min(count-1,Math.floor(value*count));}
export function Narration({lines,progress,reduced=false}:{lines:string[];progress:number;reduced?:boolean}){
 const group=stepAt(progress,lines.length),local=progress===1?1:(progress*lines.length)%1;
 const parts=lines.map(line=>line.split(/(?<=[.!?])\s+(?=[A-Z“‘])/)),fragment=stepAt(local,parts[group].length);
 return <div className="story-narration" data-static={reduced}>{parts.flatMap((sentences,i)=>sentences.map((line,j)=><p key={`${i}-${j}`} className={i===group&&j===fragment?'story-line is-current':'story-line'} aria-hidden={!reduced&&(i!==group||j!==fragment)}><AnimatedWords text={line} progress={progress===1?1:Math.max(0,Math.min(1,((local*sentences.length)%1)*2))} reduced={reduced}/></p>))}</div>;
}
