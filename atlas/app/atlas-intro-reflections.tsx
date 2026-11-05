"use client";
import {AtlasGlyph} from './atlas-intro-glyphs';
const base=import.meta.env.BASE_URL??'/';
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
export function CopperReflection({progress}:{progress:number}){
 return <svg className="intro-reflection-art" viewBox="0 0 1000 620" role="img" aria-label="Actual Copper Scroll strip 13 photograph, returning to the engraved writing.">
  <g transform={'translate('+(12*(1-progress))+' 0)'} opacity={.4+.6*progress}><AtlasGlyph name="copper" x={325} y={10} width={350} height={595}/></g>
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
