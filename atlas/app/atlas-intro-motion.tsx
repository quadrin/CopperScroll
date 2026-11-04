"use client";
import {useEffect,useRef,useState,type ReactNode} from 'react';
import {AnimatedWords} from './atlas-intro-words';

// The opening and inventory follow document scroll. Entry 25 has its own
// unified finite action/caption controller in atlas-entry-investigation.tsx.
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
export function VisualBeat({progress,count,reduced=false,children}:{progress:number;count:number;reduced?:boolean;children:ReactNode}){
 const beat=beatTiming(progress,count),t=reduced?1:beat.animation;
 return <div className="story-visual-beat" data-visual-beat={beat.index} data-visual-complete={reduced||t===1} style={{opacity:t*t*(3-2*t)}}>{children}</div>;
}
export function Narration({lines,progress,reduced=false,readyAt=.65,visualReady}:{lines:string[];progress:number;reduced?:boolean;readyAt?:number;visualReady?:boolean}){
 const beat=beatTiming(progress,lines.length),ready=reduced||(visualReady??beat.local>=readyAt);
 const initial=ready?beat.index:-1;
 const [shown,setShown]=useState(initial),[transition,setTransition]=useState<'steady'|'out'|'in'>('steady');
 const shownRef=useRef(initial);
 useEffect(()=>{
  if(!ready){shownRef.current=-1;setShown(-1);setTransition('steady');return;}
  if(reduced||beat.index===shownRef.current){setShown(beat.index);shownRef.current=beat.index;setTransition('steady');return;}
  // Clear the preceding sentence during the next visual; reveal only the matching
  // sentence once that visual has settled. A new target cancels stale swaps.
  setShown(-1);setTransition('out');
  const timer=window.setTimeout(()=>{shownRef.current=beat.index;setShown(beat.index);setTransition('in');},170);
  return()=>window.clearTimeout(timer);
 },[beat.index,reduced,ready]);
 const display=reduced?beat.index:shown;
 return <div className="story-narration" data-static={reduced} data-beat={ready?beat.index:display} data-visual-beat={beat.index} data-visual-complete={ready} data-displayed-beat={display} data-transition={reduced?'steady':transition} data-word-animation-complete={reduced||beat.animation===1}>{lines.map((line,i)=><p key={i} className={i===display?'story-line is-current':'story-line'} aria-hidden={!reduced&&i!==display}><AnimatedWords text={line} progress={display===beat.index?Math.max(0,Math.min(1,(beat.local-readyAt)/Math.max(.01,1-readyAt))):1} reduced={reduced}/></p>)}</div>;
}
