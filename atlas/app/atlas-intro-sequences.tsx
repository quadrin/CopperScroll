"use client";
import {InventoryArtScene} from './atlas-intro-inventory-art';
import {Narration,VisualBeat,beatTiming,useScrollScene} from './atlas-intro-motion';
import {AnimatedWords} from './atlas-intro-words';
const inventory=[
 {text:'Editors divide the writing into more than sixty “entries.”',art:'entries' as const},
 {text:'Each entry joins a place, an instruction and a deposit.',art:'structure' as const},
 {text:'It gives directions for finding them.',art:'directions' as const},
];
export function StorySequence({chapter}:{chapter:'inventory'}){
 const scene=useScrollScene(),timing=beatTiming(scene.value,inventory.length);
 return <section className={'story-scene story-sequence story-sequence-'+chapter} ref={scene.ref} data-chapter={chapter} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced} data-beat={timing.index} style={scene.reduced?undefined:{height:'275svh'}}>
  {scene.reduced?<div className="story-sequence-static">{inventory.map((beat,i)=><div key={i}><InventoryArtScene art={beat.art} showDeposit={i===2}/><p><AnimatedWords text={beat.text} reduced/></p></div>)}</div>:<div className="story-sticky"><VisualBeat progress={scene.value} count={inventory.length}><InventoryArtScene art={inventory[timing.index].art} showDeposit={timing.index===2} progress={timing.animation}/></VisualBeat><Narration lines={inventory.map(b=>b.text)} progress={scene.value}/></div>}
 </section>;
}
