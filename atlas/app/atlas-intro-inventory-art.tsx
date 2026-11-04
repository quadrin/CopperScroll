"use client";
import {useEffect,useState} from 'react';
import {AtlasGlyph} from './atlas-intro-glyphs';
const base=import.meta.env?.BASE_URL??'/';
export type InventoryArt='places'|'directions'|'deposit'|'entries'|'structure';
function Icon({name,x,y,width,height,opacity=1}:{name:'landscape'|'cave'|'jar'|'document';x:number;y:number;width:number;height:number;opacity?:number}){
 return <image href={`${base}introduction/inventory-illustrations/${name}.svg`} x={x} y={y} width={width} height={height} opacity={opacity} data-glyph={name} data-render="illustrative-vector"/>;
}
export function InventoryArtScene({art,progress=1}:{art:InventoryArt;progress?:number}){
 const [compact,setCompact]=useState(false);
 useEffect(()=>{const query=matchMedia('(max-width:650px)'),update=()=>setCompact(query.matches);update();query.addEventListener('change',update);return()=>query.removeEventListener('change',update);},[]);
 const t=Math.max(0,Math.min(1,progress)),geography=['places','directions','deposit'].includes(art);
 const viewBox=compact?(art==='structure'?'0 0 360 570':geography?'0 0 500 590':'0 0 500 500'):'0 0 1000 460';
 const landscape=compact?{x:50,y:0,width:400,height:250}:{x:25,y:25,width:430,height:340};
 const cave=compact?{x:80,y:280,width:330,height:250}:{x:560,y:65,width:370,height:305};
 return <svg className="story-sequence-art story-inventory-art" viewBox={viewBox} preserveAspectRatio="xMidYMid meet" role="img" aria-label={geography?'Illustrative landscape and cave: a route, a measurement, and a possible concealed jar; not a surveyed site or observed deposit.':art==='entries'?'Copper Scroll photograph with animated brackets illustrating editorial groupings of the writing.':'A place, a locating instruction, and a deposit, joined in one entry.'} data-art={art} data-layout="wide" data-compact={compact} data-asset-family="atlas-inventory-illustrations">
  {geography&&<>
   <Icon name="landscape" {...landscape}/><Icon name="cave" {...cave}/>
   {art==='directions'&&<>
    <path data-inventory-route d={compact?'M240 220C165 265 165 330 240 390':'M330 350C475 410 635 365 740 325'} fill="none" stroke="#9b613e" strokeWidth="2.5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-t}/>
    <g opacity={t}><path data-inventory-measure d={compact?'M450 475V545M442 475H458M442 545H458':'M950 330V410M942 330H958M942 410H958'} fill="none" stroke="#9b613e" strokeWidth="2"/><text x={compact?440:940} y={compact?575:445} textAnchor="end" fill="#76563d" fontSize={compact?28:26}>3 cubits</text></g>
   </>}
   {art==='deposit'&&<g data-inventory-deposit opacity={t}><path d={compact?'M120 475H410':'M620 325H910'} fill="none" stroke="#a39379" strokeWidth="1.5" strokeDasharray="5 7"/><Icon name="jar" x={compact?270:730} y={compact?425:275} width={compact?90:100} height={compact?130:145}/></g>}
  </>}
  {art==='entries'&&<>
   <AtlasGlyph name="copper" x={compact?130:355} y={5} width={compact?240:290} height={compact?475:440}/>
   {[0,1,2].map(i=><path key={i} data-entry-bracket={i} d={compact?`M120 ${100+i*115}h-18v75h18M380 ${100+i*115}h18v75h-18`:`M345 ${80+i*105}h-18v70h18M655 ${80+i*105}h18v70h-18`} fill="none" stroke="#a46035" strokeWidth="2.2" opacity={Math.max(0,Math.min(1,t*3-i))}/>) }
  </>}
  {art==='structure'&&<>
   <Icon name="cave" x={compact?70:70} y={compact?0:75} width={compact?220:260} height={compact?170:270}/>
   <Icon name="document" x={compact?100:405} y={compact?190:60} width={compact?160:210} height={compact?170:290} opacity={Math.min(1,t*2)}/>
   <Icon name="jar" x={compact?120:760} y={compact?390:80} width={compact?120:165} height={compact?160:260} opacity={Math.max(0,Math.min(1,(t-.25)*2))}/>
   <path d={compact?'M180 175V190M180 365V390':'M345 220H385M635 220H725'} fill="none" stroke="#bca487" strokeWidth="2"/>
  </>}
 </svg>;
}
