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
  const update=()=>{frame=0;const el=ref.current;if(!el)return;const rect=el.getBoundingClientRect(),sticky=el.querySelector(':scope > .story-sticky, :scope > .story-opening-sticky') as HTMLElement|null,viewport=sticky?.offsetHeight||document.documentElement.clientHeight,travel=Math.max(1,rect.height-viewport);setValue(query.matches?1:Math.max(0,Math.min(1,-rect.top/travel)));};
  const schedule=()=>{if(!frame)frame=requestAnimationFrame(update);};
  const preference=()=>{setReduced(query.matches);schedule();};
  preference();window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);query.addEventListener('change',preference);
  const observer=new ResizeObserver(schedule);if(ref.current)observer.observe(ref.current);
  return()=>{cancelAnimationFrame(frame);observer.disconnect();window.removeEventListener('scroll',schedule);window.removeEventListener('resize',schedule);query.removeEventListener('change',preference);};
 },[]);
 return {ref,value,reduced};
}
export function stepAt(value:number,count:number){return Math.min(count-1,Math.floor(value*count));}
// Each beat reserves its last third for reading the completed visual.
export function beatTiming(progress:number,count:number){
 const index=stepAt(progress,count),local=progress===1?1:(progress*count)%1;
 return {index,local,animation:Math.min(1,local/.65)};
}
export function Narration({lines,progress,reduced=false}:{lines:string[];progress:number;reduced?:boolean}){
 const beat=beatTiming(progress,lines.length);
 const [shown,setShown]=useState(beat.index),[transition,setTransition]=useState<'steady'|'out'|'in'>('steady');
 const shownRef=useRef(beat.index);
 useEffect(()=>{
  if(reduced||beat.index===shownRef.current){setShown(beat.index);shownRef.current=beat.index;setTransition('steady');return;}
  // Finish the outgoing fade before replacing the sentence. A new target cancels
  // the pending swap, so fast scrolling and reversal always resolve to this beat.
  setTransition('out');
  const timer=window.setTimeout(()=>{shownRef.current=beat.index;setShown(beat.index);setTransition('in');},170);
  return()=>window.clearTimeout(timer);
 },[beat.index,reduced]);
 const display=reduced?beat.index:shown;
 return <div className="story-narration" data-static={reduced} data-beat={beat.index} data-displayed-beat={display} data-transition={reduced?'steady':transition} data-word-animation-complete={reduced||beat.animation===1}>{lines.map((line,i)=><p key={i} className={i===display?'story-line is-current':'story-line'} aria-hidden={!reduced&&i!==display}><AnimatedWords text={line} progress={display===beat.index?beat.animation:1} reduced={reduced}/></p>)}</div>;
}
