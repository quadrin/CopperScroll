"use client";
import {AtlasGlyph} from './atlas-intro-glyphs';
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
];
export function MysteryReflection({action,previousAction,progress}:{action:number;previousAction:number;progress:number}){
 const from=mysteryFrames[previousAction],to=mysteryFrames[action],frame=to.map((n,i)=>from[i]+(n-from[i])*clamp(progress));
 return <svg className="intro-reflection-art" viewBox="0 0 1000 620" role="img" data-mystery-action={action} aria-label={action===3||action===4?'Photograph of a modern Temple model, shown as a proposed historical context, not evidence of ownership.':'Copper Scroll strip 13 photograph, reframed to examine the surviving writing and material.'}>
  <AtlasGlyph name="sanctuary" x={frame[5]} y={frame[6]} width={frame[7]} height={frame[8]} opacity={frame[9]}/>
  <AtlasGlyph name="copper" x={frame[0]} y={frame[1]} width={frame[2]} height={frame[3]} opacity={frame[4]}/>
 </svg>;
}
