"use client";
import {Narration,stepAt,useScrollScene} from './atlas-intro-motion';
import {AnimatedWords} from './atlas-intro-words';
import {AtlasGlyph} from './atlas-intro-glyphs';
import {INTRO_PRIVATE_IMAGES,EditionPassage} from './atlas-intro-media';
import CandidateMap from './atlas-intro-candidate-map';
const base=import.meta.env?.BASE_URL??'/';
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const hebrew=['[ב]מערת העמוד של שני','[ה]פתחין צופא מזרח','[ב]פתח הצפוני חפור','[א]מות שלוש שמ קלל','בו ספר אחד תחתו','ככ 42'];
const english=['[In] the cave of the pillar with two entrances,','facing east, [at] the northern entrance,','dig three cubits. There is a jar,','in it one scroll; beneath it,','42 silver-weight units.'];
export function EntryReveal(){
 const scene=useScrollScene(),p=scene.value;
 const lift=scene.reduced?1:clamp((p-.25)/.10),translation=scene.reduced?1:clamp((p-.60)/.10);
 const imageOpacity=scene.reduced?1:1-clamp((p-.25)/.10);
 const phase=p<.30?'image':p<.65?'hebrew':'english';
 return <div className="story-scene story-entry-reveal" ref={scene.ref} data-progress={p.toFixed(3)} data-reduced={scene.reduced} data-reading-phase={phase}><div className="story-sticky">
  <div className="story-entry-art">
   <div className="story-entry-radiographs" style={{opacity:imageOpacity,transform:scene.reduced?undefined:`scale(${1+p*.12})`}}>{INTRO_PRIVATE_IMAGES?['12g','12c','12d'].map(tag=><img key={tag} src={`${base}introduction/entry25-${tag}.jpeg`} alt={`Published column VI radiograph ${tag.toUpperCase()}, containing the Entry 25 passage.`}/>):<EditionPassage/>}</div>
   <div className="story-entry-hebrew" lang="he" dir="rtl" style={{opacity:scene.reduced?1:lift*(1-translation),transform:scene.reduced?undefined:`translateY(${(1-lift)*8}px)`}} aria-hidden={!scene.reduced&&(lift<.5||translation>.5)}>{hebrew.map((line,i)=><p key={i}>{line}</p>)}</div>
   <blockquote className="story-entry-english" style={{opacity:translation,transform:scene.reduced?undefined:`translateY(${(1-translation)*8}px)`}} aria-hidden={!scene.reduced&&translation<.5}>{english.map((line,i)=><p key={i}><AnimatedWords text={line} progress={scene.reduced?1:clamp((p-.56-i*.025)*7)} reduced={scene.reduced}/></p>)}</blockquote>
  </div>
  <Narration progress={p} reduced={scene.reduced} lines={[
   'We will follow one example: Entry 25. It occupies column VI, lines 1–6.',
   'The Hebrew lifts into modern type. Brackets mark letters supplied by editors.',
   'Read it in English. A cave, an instruction, and a deposit.',
  ]}/>
 </div></div>;
}
const clauses=[
 {he:'מערת העמוד',en:'the cave of the pillar',body:'“Pillar” may describe a rock feature. Some editors read it as a platform or terrace.'},
 {he:'של שני [ה]פתחין צופא מזרח',en:'two entrances, facing east',body:'Two openings, facing east. Does the direction describe the cave, or each entrance?'},
 {he:'[ב]פתח הצפוני חפור [א]מות שלוש',en:'at the northern entrance, dig three cubits',body:'Three cubits from an entrance. We still need its ancient surface and the intended direction.'},
 {he:'שמ קלל בו ספר אחד תחתו ככ 42',en:'a jar, one scroll, and 42 silver-weight units',body:'A jar, a manuscript, and silver. “Beneath it” could refer to the jar or the manuscript.'},
];
export function EntryMeaning(){
 const scene=useScrollScene(),step=stepAt(scene.value,4);
 return <div className="story-scene story-entry-meaning" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced}><div className="story-sticky">
  <div className="story-clause-art"><svg className="story-clue-drawing" viewBox={scene.reduced?'0 0 800 220':step===3?'500 0 300 220':'80 0 470 220'} aria-hidden="true" data-asset-family="atlas-relief-studies"><AtlasGlyph name="cave" x={100} y={0} width={360} height={215} opacity={scene.reduced||step!==3?1:.25}/><g opacity={scene.reduced||step===1?1:0}><path d="M445 168H510M499 159L510 168L499 177" fill="none" stroke="#9b613e" strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={scene.reduced?0:1-clamp((scene.value*4%1)*3)}/></g><g opacity={scene.reduced||step===2?1:0}><path d="M477 84V190M469 84H485M469 190H485" fill="none" stroke="#9b613e" strokeWidth="2"/></g><AtlasGlyph name="jar" x={530} y={42} width={115} height={160} opacity={scene.reduced||step===3?1:0}/><AtlasGlyph name="silver" x={650} y={84} width={140} height={115} opacity={scene.reduced||step===3?1:0}/></svg>{clauses.map((c,i)=><div key={i} data-reading={i} className={scene.reduced||i===step?'is-current':''} aria-hidden={!scene.reduced&&i!==step}><p lang="he" dir="rtl">{c.he}</p><p><AnimatedWords text={c.en} progress={scene.reduced?1:clamp((scene.value*4%1)*2)} reduced={scene.reduced}/></p></div>)}</div>
  <Narration progress={scene.value} reduced={scene.reduced} lines={clauses.map(c=>c.body)}/>
 </div></div>;
}
const candidates=[
 {name:'Twin Cave near Qumran',image:'twin-cave-figure.webp',alt:'Bar-Adon’s published exterior photograph of the Twin Cave area, looking from the southeast.',text:'Twin Cave shares a pillar and two reported east-facing openings. Its ancient thresholds and architectural date remain uncertain.'},
 {name:'IV/17 near Jericho',image:'iv17-plan.webp',alt:'Sion’s published plan of IV/17, showing a dividing pillar and two present openings.',text:'IV/17 has a surveyed plan and a rock-cut pillar. The plan shows two roughly southeast-facing openings.'},
 {name:'IV/11 near Jericho',image:'iv11-plan.png',alt:'Feig’s published plan of IV/11, including its scale and north arrow.',text:'IV/11 also has a pillar. Its published report does not establish two exterior entrances.'},
];
export function CandidateComparison(){
 const scene=useScrollScene(),step=stepAt(scene.value,4),all=scene.reduced||step===3;
 return <div className="story-scene story-candidates" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced} data-candidate={all?'comparison':candidates[step].name}><div className="story-sticky">
  <div className={`story-candidate-art${all?' compare-all':''}`}>{candidates.map((c,i)=><figure key={c.name} style={{opacity:all||i===step?1:0}} aria-hidden={!all&&i!==step}>{i===0&&!INTRO_PRIVATE_IMAGES?<div className="story-candidate-locator"><CandidateMap progress={1} reduced/></div>:<img src={`${base}introduction/${c.image}`} alt={c.alt}/>}{all&&<figcaption>{c.name}</figcaption>}</figure>)}</div>
  <Narration progress={scene.value} reduced={scene.reduced} lines={[
   ...candidates.map(c=>c.text),
   'Compare the same clues at all three sites. None establishes the ancient cave or a surviving deposit.',
  ]}/>
 </div></div>;
}
export function DuplicateEntry(){
 const scene=useScrollScene(),p=scene.value;
 return <div className="story-scene story-copy" ref={scene.ref} data-progress={p.toFixed(3)} data-reduced={scene.reduced}><div className="story-sticky">
  <div className="story-copy-art"><svg className="story-copy-drawing" viewBox="0 0 800 160" aria-hidden="true" data-asset-family="atlas-relief-studies"><AtlasGlyph name="document" x={155} y={0} width={150} height={155}/><AtlasGlyph name="document" x={505} y={0} width={150} height={155} opacity={scene.reduced?.45:.45*clamp((p-.35)*3)}/><path d="M335 77H474M462 67L474 77L462 87" fill="none" stroke="#9b613e" strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={scene.reduced?0:1-clamp((p-.18)*3)}/></svg><p lang="he" dir="rtl" style={{opacity:scene.reduced?1:clamp(p*4)}}>משנא הכתב הזא</p><blockquote style={{opacity:scene.reduced?1:clamp((p-.35)*4)}}>a copy of this document</blockquote></div>
  <Narration progress={p} reduced={scene.reduced} lines={[
   'The final entry points to another copy. It describes explanations, measurements and details of the listed items.',
   'That copy has not been identified. It is separate from the manuscript in Entry 25. Such explanations could have helped a reader recover hidden valuables.',
  ]}/>
 </div></div>;
}
