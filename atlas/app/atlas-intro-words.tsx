"use client";
import {useEffect,useRef,useState,type CSSProperties} from 'react';
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const terms=/\b(Copper Scroll|copper|gold|silver|three cubits)\b/gi;
export function AnimatedWords({text,progress=1,reduced=false}:{text:string;progress?:number;reduced?:boolean}){
 const amount=reduced?1:clamp(progress);
 return <>{text.split(terms).map((part,i)=>{
  const key=part.toLowerCase();let kind='';
  if(key==='copper'||key==='copper scroll')kind='copper';else if(key==='gold'||key==='silver')kind=key;else if(key==='three cubits')kind='ink';
  if(!kind)return part;
  return <span key={i} className={`story-word story-word-${kind}`} data-word={part} style={{'--word-progress':amount,'--word-position':`${110-amount*145}%`} as CSSProperties}>{part}</span>;
 })}</>;
}
export function ScrollParagraph({children}:{children:string}){
 const ref=useRef<HTMLParagraphElement>(null),[progress,setProgress]=useState(0);
 useEffect(()=>{
  const query=matchMedia('(prefers-reduced-motion: reduce)');let frame=0;
  const update=()=>{frame=0;const r=ref.current?.getBoundingClientRect();if(r)setProgress(query.matches?1:clamp((innerHeight*.88-r.top)/(innerHeight*.65)));};
  const schedule=()=>{if(!frame)frame=requestAnimationFrame(update);};update();window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);query.addEventListener('change',schedule);
  return()=>{cancelAnimationFrame(frame);window.removeEventListener('scroll',schedule);window.removeEventListener('resize',schedule);query.removeEventListener('change',schedule);};
 },[]);
 return <p ref={ref}><AnimatedWords text={children} progress={progress}/></p>;
}
