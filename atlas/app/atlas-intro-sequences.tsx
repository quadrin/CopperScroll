"use client";
import {InventoryArtScene,ColumnDiagram} from './atlas-intro-inventory-art';
import {Narration,VisualBeat,beatTiming,useScrollScene} from './atlas-intro-motion';
import {AnimatedWords} from './atlas-intro-words';
const inventory=[
 {text:'What did they say?',art:'columns' as const},
 {text:'They described hidden valuables—and gave instructions for finding them.',art:'directions' as const},
 {text:'Editors divide the writing into more than sixty entries.',art:'entries' as const},
];
function InventoryVisual({index,progress=1}:{index:number;progress?:number}){
 return index===0?<ColumnDiagram progress={progress}/>:<InventoryArtScene art={inventory[index].art==='entries'?'entries':'directions'} showDeposit={index===1} showMeasurement={false} progress={progress}/>;
}
export function StorySequence({chapter}:{chapter:'inventory'}){
 const scene=useScrollScene(),timing=beatTiming(scene.value,inventory.length);
 return <section className={'story-scene story-sequence story-sequence-'+chapter} ref={scene.ref} data-chapter={chapter} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced} data-beat={timing.index} style={scene.reduced?undefined:{height:'275svh'}}>
  {scene.reduced?<div className="story-sequence-static">{inventory.map((beat,i)=><div key={i}><InventoryVisual index={i}/><p><AnimatedWords text={beat.text} reduced/></p></div>)}</div>:<div className="story-sticky"><VisualBeat progress={scene.value} count={inventory.length}><InventoryVisual index={timing.index} progress={timing.animation}/></VisualBeat><Narration lines={inventory.map(b=>b.text)} progress={scene.value}/></div>}
 </section>;
}
