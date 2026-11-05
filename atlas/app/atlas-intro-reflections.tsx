"use client";
import {AtlasGlyph} from './atlas-intro-glyphs';
const base=import.meta.env.BASE_URL??'/';
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
// Each pose reframes the existing photographs. No generated inscription or
// graphic date implies a settled attribution. The Temple is a modern model.
const mysteryFrames=[
 [325,10,350,595,1,100,0,800,610,0],
 [310,0,380,640,1,100,0,800,610,0],
 [275,-60,450,760,1,100,0,800,610,0],
 [325,10,350,595,0,100,0,800,610,1],
 [625,60,265,480,1,30,35,540,550,.8],
 [305,-20,390,660,1,30,35,540,550,0],
 [340,25,320,550,1,100,0,800,610,0],
 [300,-25,400,675,1,100,0,800,610,0],
 [315,0,370,625,1,100,0,800,610,0],
 [335,25,330,560,1,100,0,800,610,0],
];
export function MysteryReflection({action,previousAction,progress}:{action:number;previousAction:number;progress:number}){
 const from=mysteryFrames[previousAction],to=mysteryFrames[action],frame=to.map((n,i)=>from[i]+(n-from[i])*clamp(progress));
 return <svg className="intro-reflection-art" viewBox="0 0 1000 620" role="img" data-mystery-action={action} aria-label={action===3||action===4?'Photograph of a modern Temple model, shown as a proposed historical context, not evidence of ownership.':'Copper Scroll strip 13 photograph, reframed to examine the surviving writing and material.'}>
  <AtlasGlyph name="sanctuary" x={frame[5]} y={frame[6]} width={frame[7]} height={frame[8]} opacity={frame[9]}/>
  <AtlasGlyph name="copper" x={frame[0]} y={frame[1]} width={frame[2]} height={frame[3]} opacity={frame[4]}/>
 </svg>;
}
export function FieldworkReflection({progress}:{progress:number}){
 const sight=clamp(progress*2),section=clamp((progress-.4)/.6);
 return <svg className="intro-reflection-art" viewBox="0 0 1200 850" role="img" aria-label="Illustrative field investigation: survey sightlines and a shallow section through possible entrance layers. No excavation or observation is asserted at a candidate site.">
  <image href={base+'introduction/entry-investigation/limestone-cave.svg'} x="160" y="-20" width="920" height="614"/>
  <g transform="translate(165 370)" opacity={sight}>
   <path d="M-10 0L-65 220M0 0V230M10 0L70 220" fill="none" stroke="#766e59" strokeWidth="6"/>
   <path d="M-8 0H8V-40H-8Z" fill="#9e9b84" stroke="#605e4c" strokeWidth="2"/><path d="M-25-45H45V-27H-25Z" fill="#7e8978" stroke="#53604e" strokeWidth="2"/><circle cx="-24" cy="-36" r="11" fill="#4e5c4e"/>
   <path d="M45-36L415 63M45-36L665 99" fill="none" stroke="#a66e3d" strokeWidth="1.5" strokeDasharray="6 8" pathLength="1" strokeDashoffset={1-sight}/>
  </g>
  <g opacity={section}>
   <path d="M420 558L935 590L990 716L473 677Z" fill="#b99d73"/><path d="M420 558L473 677L473 776L420 656Z" fill="#8f7656"/>
   <path d="M473 677L990 716V800L473 776Z" fill="#d1b68e"/>
   <path d="M473 705Q660 695 990 745M473 739Q690 733 990 775" fill="none" stroke="#a38b66" strokeWidth="3"/>
   <path d="M580 572L798 586L822 660L604 645Z" fill="#665d48"/>
   <path d="M580 572L604 645V721L580 648Z" fill="#9c8260"/><path d="M604 645L822 660V738L604 721Z" fill="#bc9e76"/>
   <path d="M604 668L822 683M604 695L822 710" fill="none" stroke="#8a7556" strokeWidth="2"/>
  </g>
 </svg>;
}
