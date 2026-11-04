"use client";
import {lazy,Suspense} from 'react';
import {AtlasGlyph} from './atlas-intro-glyphs';
import {INTRO_PRIVATE_IMAGES,EditionPassage} from './atlas-intro-media';
const CandidateMap=lazy(()=>import('./atlas-intro-candidate-map'));
import {Narration,stepAt,useScrollScene} from './atlas-intro-motion';
import {AnimatedWords} from './atlas-intro-words';
const base=import.meta.env?.BASE_URL??'/';
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
type Art='sheet'|'places'|'directions'|'deposit'|'entries'|'structure'|'entry25'|'candidates'|'worked'|'time'|'recovery'|'durability'|'temple'|'community'|'literary'|'unknown'|'evidence';
type Beat={text:string;art:Art};
const inventory:Beat[]=[
 {text:'The Copper Scroll reads like an inventory of concealed treasure.',art:'sheet'},
 {text:'It names places and landmarks.',art:'places'},
 {text:'It gives directions and measurements.',art:'directions'},
 {text:'And records what was supposed to be hidden there.',art:'deposit'},
 {text:'Editors divide the writing into more than sixty “entries.”',art:'entries'},
 {text:'Each usually combines a place, an instruction, and a deposit.',art:'structure'},
 {text:'Entry boundaries and numbering differ between editions.',art:'entries'},
 {text:'Let’s follow one example: Entry 25.',art:'entry25'},
];
const locations:Beat[]=[
 {text:'The entry describes a cave’s features, rather than a modern address.',art:'places'},
 {text:'Researchers have proposed caves near Qumran and near Jericho.',art:'candidates'},
 {text:'Pins mark proposed areas; individual cave mouths are not precisely registered.',art:'candidates'},
 {text:'We can compare the same clues at each candidate site.',art:'candidates'},
];
const worked:Beat[]=[
 {text:'For a closer look, take IV/17 near Jericho.',art:'worked'},
 {text:'Its published plan makes it a useful worked example.',art:'worked'},
 {text:'It has not been established as the scroll’s cave.',art:'unknown'},
];
const time:Beat[]=[
 {text:'The writer knew a landscape that has since changed.',art:'time'},
 {text:'A pillar or entrance must have existed at the right time.',art:'time'},
 {text:'Later building and deposits can change the point we measure from.',art:'directions'},
];
const purpose:Beat[]=[
 {text:'The instructions seem to assume a reader who knew the landscape.',art:'places'},
 {text:'We can read “the northern entrance” and still lack its ancient reference point.',art:'directions'},
 {text:'One interpretation sees a practical inventory for recovering hidden valuables.',art:'recovery'},
 {text:'Copper could have helped the record endure.',art:'durability'},
 {text:'Its durability cannot establish that the deposits were real.',art:'unknown'},
 {text:'But whose property was it?',art:'unknown'},
 {text:'One proposal connects it with the Jerusalem Temple, around the crisis of 70 CE.',art:'temple'},
 {text:'The Temple is shown here in the Israel Museum’s modern reconstruction.',art:'temple'},
 {text:'Another associates it with the Qumran community or another group.',art:'community'},
 {text:'A literary interpretation sees a record of legendary treasure.',art:'literary'},
 {text:'The enormous quantities and obscure directions have encouraged that reading.',art:'literary'},
 {text:'Others see practical detail as evidence for real property.',art:'recovery'},
 {text:'The scroll names no owner who settles the question.',art:'unknown'},
];
const ending:Beat[]=[
 {text:'Perhaps it was a recovery record for people who expected to return.',art:'recovery'},
 {text:'Perhaps it preserved knowledge of valuables they could no longer reach.',art:'literary'},
 {text:'Its author, date, ownership and purpose remain disputed.',art:'unknown'},
 {text:'No independently verified recovery has established a treasure match.',art:'unknown'},
 {text:'A matching landmark would still leave the question of its contents.',art:'deposit'},
 {text:'The Atlas brings the readings, places and archaeological records together.',art:'evidence'},
 {text:'Our cave example is one way into that work.',art:'evidence'},
];

function Illustration({art,progress=1}:{art:Art;progress?:number}){
 const t=clamp(progress),map=['places','directions','deposit','candidates','time'].includes(art);
 return <svg className="story-sequence-art" viewBox="0 0 1000 430" role="img" aria-label={art==='sheet'||art==='durability'?'Actual photograph of Copper Scroll strip 13, showing engraved Hebrew and corroded metal.':art==='temple'?'Photograph of the Israel Museum’s modern reconstruction of the Second Temple, representing a proposed ownership.':art==='community'?'Generic illustrative courtyard representing a proposed community ownership; not a reconstruction of Qumran.':art==='worked'?'Published IV/17 plan.':art==='entry25'?'Published radiograph containing Entry 25.':`Illustrative ${art} scene; not a surveyed landscape or an observed deposit.`} data-art={art} data-asset-family="atlas-relief-studies">
  <g>
  {(art==='sheet'||art==='durability')&&<g transform={`translate(0 ${6*(1-t)})`}><AtlasGlyph name="copper" x={310} y={0} width={380} height={385}/>{art==='durability'&&<path d={`M${320+t*330} 55L${280+t*330} 341`} fill="none" stroke="#e8d9b9" strokeWidth="3" opacity={.2+.3*Math.sin(t*Math.PI)}/>}</g>}
  {art==='entries'&&<><AtlasGlyph name="document" x={300} y={5} width={400} height={365}/>{[0,1,2].map(i=><path key={i} d={`M352 ${126+i*66}h-16v43h16M648 ${126+i*66}h16v43h-16`} fill="none" stroke="#9a613f" strokeWidth="2.2" opacity={clamp(t*2-i*.32)}/>)}</>}
  {art==='structure'&&<><AtlasGlyph name="cave" x={95} y={70} width={240} height={245}/><AtlasGlyph name="document" x={390} y={65} width={220} height={255} opacity={.45+.55*clamp(t*2)}/><AtlasGlyph name="jar" x={700} y={70} width={190} height={245} opacity={.25+.75*clamp((t-.25)*2)}/><path d="M345 200H370M633 200H674" fill="none" stroke="#bca487" strokeWidth="1.8"/></>}
  {map&&<>
   <AtlasGlyph name="landscape" x={65} y={60} width={375} height={285}/>
   <AtlasGlyph name={art==='time'?'strata':'cave'} x={455} y={25} width={440} height={335}/>
   {(art==='directions'||art==='candidates')&&<path d="M385 320C491 355 577 342 662 299" fill="none" stroke="#9b613e" strokeWidth="2.5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-t}/>}
   {art==='directions'&&<g opacity={t}><path d="M884 193V317M876 193H892M876 317H892" fill="none" stroke="#9b613e" strokeWidth="2"/><text x="874" y="365" textAnchor="end" fill="#76563d" fontSize="24">3 cubits</text></g>}
   {art==='deposit'&&<g opacity={t} transform={`translate(0 ${12*(1-t)})`}><AtlasGlyph name="jar" x={697} y={220} width={112} height={151}/><path d="M644 222H862" fill="none" stroke="#a39379" strokeWidth="1.5" strokeDasharray="5 7"/></g>}
  </>}
  {art==='worked'&&<image href={`${base}introduction/iv17-plan.webp`} x="285" y="5" width="430" height="420"/>}
  {art==='temple'&&<AtlasGlyph name="sanctuary" x={245} y={0} width={510} height={385}/>}
  {art==='community'&&<AtlasGlyph name="settlement" x={245} y={5} width={510} height={365}/>}
  {(art==='literary'||art==='recovery'||art==='unknown')&&<>
   <AtlasGlyph name="document" x={175} y={38} width={275} height={310}/>
   {art==='literary'?<AtlasGlyph name="landscape" x={550} y={66} width={340} height={280} opacity={.3+.5*t}/>:<><path d="M478 227C522 190 566 190 607 227" fill="none" stroke="#a16b45" strokeWidth="2" pathLength="1" strokeDasharray={art==='unknown'?'.025 .035':'1'} strokeDashoffset={art==='unknown'?0:1-t}/><AtlasGlyph name="jar" x={635} y={84} width={190} height={250} opacity={art==='unknown'?.24:.25+.75*t}/></>}
  </>}
  {art==='evidence'&&<><AtlasGlyph name="document" x={110} y={65} width={210} height={265}/><AtlasGlyph name="landscape" x={397} y={80} width={215} height={240}/><image href={`${base}introduction/iv17-plan.webp`} x="700" y="80" width="220" height="240"/><path d="M340 212H375M636 212H678" fill="none" stroke="#9a7050" strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={1-t}/></>}
  {art==='entry25'&&(INTRO_PRIVATE_IMAGES?<image href={`${base}introduction/entry25-12g.jpeg`} x="355" y="10" width="290" height="380" opacity={.55+.45*t}/>:<EditionPassage x={210} y={10} width={580} height={380}/>)}
  </g>
 </svg>;
}
export function StorySequence({chapter}:{chapter:'inventory'|'locations'|'worked'|'time'|'purpose'|'ending'}){
 const beats={inventory,locations,worked,time,purpose,ending}[chapter],scene=useScrollScene(),step=stepAt(scene.value,beats.length),local=scene.value===1?1:(scene.value*beats.length)%1;
 return <section className={`story-scene story-sequence story-sequence-${chapter}`} ref={scene.ref} data-chapter={chapter} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced} data-beat={step} style={scene.reduced?undefined:{height:`${80+beats.length*65}svh`}}>
  {scene.reduced?<div className="story-sequence-static">{beats.map((beat,i)=><div key={i}><>{chapter==='locations'?(i===0?<Suspense fallback={<div className="story-regional-map"/>}><CandidateMap progress={1} reduced/></Suspense>:null):<Illustration art={beat.art}/>}</><p><AnimatedWords text={beat.text} reduced/></p></div>)}</div>:<div className="story-sticky">{chapter==='locations'?<Suspense fallback={<div className="story-regional-map"/>}><CandidateMap progress={scene.value}/></Suspense>:<Illustration art={beats[step].art} progress={local*1.5}/>}<Narration lines={beats.map(b=>b.text)} progress={scene.value}/></div>}
 </section>;
}
