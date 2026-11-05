"use client";
import {useEffect,useId,useState} from 'react';
import {AtlasGlyph} from './atlas-intro-glyphs';
const base=import.meta.env.BASE_URL??'/';
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const ease=(n:number)=>{const t=clamp(n);return t*t*(3-2*t);};
const between=(n:number,start:number,end:number)=>ease((n-start)/(end-start));
const mix=(a:number,b:number,t:number)=>a+(b-a)*t;
const pulse=(n:number,start:number,end:number)=>Math.sin(Math.PI*clamp((n-start)/(end-start)));

/** One reversible, finite scene. All settled poses share the same cave and
 * survey datum. Geometry is explanatory, not a measured candidate site. */
export default function ReaderLandscape({stage,previousStage,progress}:{stage:number;previousStage:number;progress:number}){
 const id=useId().replace(/:/g,''),[compact,setCompact]=useState(false);
 useEffect(()=>{const query=matchMedia('(max-width:700px)'),update=()=>setCompact(query.matches);update();query.addEventListener('change',update);return()=>query.removeEventListener('change',update);},[]);
 const q=mix(previousStage,stage,clamp(progress)),pull=between(q,-.95,-.12),leave=between(q,.02,.70),camera=between(q,.03,.70);
 const landscape=between(q,.08,.49),staff=between(q,1.04,1.34),level=between(q,1.30,1.67),threshold=between(q,1.65,2),hypothesis=between(q,2.05,3);
 const firstOpening=between(q,3.04,3.51),secondOpening=between(q,3.48,3.98),section=between(q,4.12,5);
 const width=mix(compact?530:640,compact?335:365,pull)*(1+leave*.75);
 const photoX=(compact?400:720)-width/2-leave*(compact?870:1390),photoY=mix(-150,compact?65:35,pull)-leave*100;
 const photoHeight=width*1.70,photoOpacity=1-between(q,.28,.66),light=q<0?Math.sin(Math.PI*between(q,-.95,-.1))*.34:0;
 const world=compact?'translate(10 330) scale(.65)':'translate(380 50) scale(.82)';
 const ridge=pulse(q,.39,.64),pillar=pulse(q,.55,.78),left=pulse(q,.71,.90),right=pulse(q,.82,1);
 const earlier='M180 636Q420 612 650 632T1035 668';
 return <svg className="intro-reflection-art reader-landscape-art" viewBox={compact?'0 0 800 1000':'0 0 1440 900'} role="img" data-reader-stage={stage} data-reader-position={q.toFixed(4)} data-reader-compact={compact} aria-label="Illustrative sequence from a conserved Copper Scroll strip to a familiar cave landscape, then a survey staff, level reference and tentative earlier threshold. The cave and reconstruction are schematic, not a surveyed candidate site.">
  <defs>
   <radialGradient id={id+'-land-mask'} cx="50%" cy="48%" r="52%"><stop offset="30%" stopColor="white"/><stop offset="100%" stopColor="black"/></radialGradient>
   <mask id={id+'-land'}><rect width="1400" height="1100" fill={'url(#'+id+'-land-mask)'}/></mask>
   <linearGradient id={id+'-rake'}><stop stopColor="white" stopOpacity="0"/><stop offset=".44" stopColor="#fff1cb" stopOpacity="0"/><stop offset=".5" stopColor="#fff1cb"/><stop offset=".56" stopColor="#fff1cb" stopOpacity="0"/><stop offset="1" stopColor="white" stopOpacity="0"/></linearGradient>
   <mask id={id+'-copper-mask'}><AtlasGlyph name="copper" x={photoX} y={photoY} width={width} height={photoHeight}/></mask>
   <mask id={id+'-cave-mask'} maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="800" style={{maskType:'alpha'}}><image href={base+'introduction/entry-investigation/limestone-cave.svg'} width="1200" height="800"/></mask>
   <linearGradient id={id+'-trail'}><stop stopColor="#e4c9a3" stopOpacity="0"/><stop offset=".3" stopColor="#e4c9a3"/><stop offset="1" stopColor="#e4c9a3"/></linearGradient>
   <clipPath id={id+'-pillar'}><path d="M442 274L584 188L643 257L584 359L564 496L586 559L528 602L332 605L363 552L402 493L420 394Z"/></clipPath>
  </defs>
  <g data-reader-world opacity={landscape} transform={'translate('+(compact?400:920)+' '+(compact?640:400)+') scale('+mix(.9,1,camera)+') translate('+-(compact?400:920)+' '+-(compact?640:400)+')'}>
   <g transform={world}>
    <g transform={compact?'translate(-60 -500)':'translate(-600 -140)'} opacity=".65"><image href={base+'introduction/inventory-illustrations/landscape.svg'} width="1400" height="1100" mask={'url(#'+id+'-land)'}/></g>
    <path d={compact?'M-30 805Q-10 690 170 626':'M-470 740C-290 740-170 690-85 640S90 600 190 571'} fill="none" stroke={'url(#'+id+'-trail)'} strokeWidth="21" strokeLinecap="round" opacity={between(q,.31,.82)}/>
    <g data-reader-cave>
     <image href={base+'introduction/entry-investigation/limestone-cave.svg'} width="1200" height="800"/>
     <g mask={'url(#'+id+'-cave-mask)'}><path d="M245 209Q550-50 960 103L1010 176Q630 69 312 272Z" fill="#fff0bf" opacity={ridge*.22}/>
     <g clipPath={'url(#'+id+'-pillar)'} opacity={pillar*.27}><image href={base+'introduction/entry-investigation/limestone-cave.svg'} width="1200" height="800"/><path d="M300 180H660V620H300Z" fill="#ffe4a3" opacity=".40"/></g>
     <path d="M214 520C207 457 224 391 270 351L341 296L407 350L386 465L354 525Z" fill="#f5d89a" opacity={left*.13}/>
     <path d="M588 567L592 439Q597 316 699 259Q827 188 939 294Q985 351 965 442L935 575Z" fill="#f5d89a" opacity={right*.13}/></g>
    </g>
    <g data-reader-survey opacity={staff}>
     <g transform={'translate(120 '+(24*(1-staff))+')'}>
      <path d="M-6 205H6V710H-6Z" fill="#eae1cd" stroke="#74664c" strokeWidth="2"/>
      {Array.from({length:12},(_,i)=><path key={i} d={'M-5 '+(210+i*40)+'H5V'+(230+i*40)+'H-5Z'} fill={i%2?'#6c7867':'#9b6341'}/>)}
      <path d="M-14 710H14M-12 520H12" stroke="#74664c" strokeWidth="3"/>
     </g>
     <path data-reader-level d="M120 520H1005" fill="none" stroke="#667c77" strokeWidth="2.5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-level}/>
     <circle cx="1005" cy="520" r="5" fill="#667c77" opacity={level}/>
    </g>
    <g data-reader-threshold opacity={threshold}>
     <path d="M180 636Q420 612 650 632T1035 668L1030 712Q650 678 180 681Z" fill="#a8b4a5" opacity={hypothesis*.25}/>
     <path d={earlier} fill="none" stroke="#9b6341" strokeWidth={2.5+hypothesis} strokeDasharray="8 9"/>
     <path d="M165 520V636M153 520H177M153 636H177" fill="none" stroke="#9b6341" strokeWidth="2" opacity={hypothesis}/>
    </g>
    <g data-reader-openings fill="none" stroke="#9b6341" strokeWidth="3" strokeDasharray="8 9">
     <path d="M214 520C207 457 224 391 270 351L341 296L407 350L386 465L354 525Z" opacity={firstOpening}/>
     <path d="M588 567L592 439Q597 316 699 259Q827 188 939 294Q985 351 965 442L935 575Z" opacity={secondOpening}/>
    </g>
    <g data-reader-section opacity={section} transform={'translate(0 '+(12*(1-section))+')'}>
     <path d="M500 640L780 660L820 720L540 700Z" fill="#685b46"/>
     <path d="M500 640L540 700V770L500 708Z" fill="#8d785b"/>
     <path d="M540 700L820 720V790L540 770Z" fill="#c4aa83"/>
     <path d="M540 722Q680 718 820 745M540 748Q680 744 820 771" fill="none" stroke="#907c60" strokeWidth="2.5"/>
    </g>
   </g>
  </g>
  <g data-reader-copper opacity={photoOpacity}>
   <AtlasGlyph name="copper" x={photoX} y={photoY} width={width} height={photoHeight}/>
   <g mask={'url(#'+id+'-copper-mask)'} opacity={light}><rect x={photoX-width+between(q,-.95,-.1)*width} y={photoY} width={width*2} height={photoHeight} fill={'url(#'+id+'-rake)'}/></g>
  </g>
 </svg>;
}
