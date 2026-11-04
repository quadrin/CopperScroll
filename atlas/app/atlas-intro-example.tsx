"use client";
import {Narration,VisualBeat,stepAt,useScrollScene} from './atlas-intro-motion';
import {AtlasGlyph} from './atlas-intro-glyphs';
import {INTRO_PRIVATE_IMAGES} from './atlas-intro-media';
import CandidateMap from './atlas-intro-candidate-map';
import {PassageLines,useReadingStage,useReadingTime} from './atlas-intro-line-reading';
const base=import.meta.env?.BASE_URL??'/';
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const hebrew=['[ב]מערת העמוד של שני','[ה]פתחין צופא מזרח','[ב]פתח הצפוני חפור','[א]מות שלוש שמ קלל','בו ספר אחד תחתו','ככ 42'];
const english=['[In] the cave of the pillar with two entrances,','facing east, [at] the northern entrance,','dig three cubits. There is a jar,','in it one scroll; beneath it,','42 silver-weight units.'];
export function EntryReveal(){
 const scene=useScrollScene(),p=scene.value,visible=useReadingStage(scene.ref);
 const lift=scene.reduced?1:clamp((p-.28)/.05),translation=scene.reduced?1:clamp((p-.61)/.05);
 const imageOpacity=scene.reduced?1:clamp(p/(.65/3))*(1-clamp((p-.28)/.05));
 const phase=p<1/3&&INTRO_PRIVATE_IMAGES?'image':p<2/3?'hebrew':'english';
 return <div className="story-scene story-entry-reveal" ref={scene.ref} data-progress={p.toFixed(3)} data-reduced={scene.reduced} data-reading-phase={phase} data-source-images={INTRO_PRIVATE_IMAGES}><div className="story-sticky">
  <div className="story-entry-art">
   {INTRO_PRIVATE_IMAGES&&<div className="story-entry-radiographs" style={{opacity:imageOpacity}}>{['12g','12c','12d'].map(tag=><img key={tag} src={`${base}introduction/entry25-${tag}.jpeg`} alt={`Published column VI radiograph ${tag.toUpperCase()}, containing the Entry 25 passage.`}/>)}</div>}
   <div className="story-entry-hebrew" lang="he" dir="rtl" style={{opacity:scene.reduced?1:(INTRO_PRIVATE_IMAGES?lift:1)*(1-translation),transform:scene.reduced?undefined:`translateY(${INTRO_PRIVATE_IMAGES?(1-lift)*8:0}px)`}} aria-hidden={!scene.reduced&&((INTRO_PRIVATE_IMAGES&&lift<.5)||translation>.5)}><PassageLines lines={hebrew} language="he" active={visible&&p>=.34&&p<.60} reduced={scene.reduced}/></div>
   <blockquote className="story-entry-english" style={{opacity:translation,transform:scene.reduced?undefined:`translateY(${(1-translation)*8}px)`}} aria-hidden={!scene.reduced&&translation<.5}><PassageLines lines={english} language="en" active={visible&&p>=.68} reduced={scene.reduced}/></blockquote>
  </div>
  <Narration progress={p} readyAt={p<1/3?.65:.05} reduced={scene.reduced} lines={[
   'Let’s follow one example: Entry 25, column VI, lines 1–6.',
   'Brackets in the Hebrew mark letters supplied by editors.',
   'In English: a cave, an instruction, and a deposit.',
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
 const scene=useScrollScene(),scrollStep=stepAt(scene.value,4),visible=useReadingStage(scene.ref),time=useReadingTime(visible,scene.reduced,scrollStep);
 const cycle=6500,step=scene.reduced?scrollStep:Math.min(3,scrollStep+Math.floor(time/cycle)),local=time%cycle,leaving=!scene.reduced&&step<3&&local>=5800;
 return <div className="story-scene story-entry-meaning" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced} data-reading-step={step} data-playing={visible&&!scene.reduced}><div className="story-sticky">
  <div className="story-clause-art story-clause-reading">{clauses.map((c,i)=><div key={i} data-reading={i} data-motion={i===step?(leaving?'leaving':'reading'):'waiting'} className={scene.reduced||i===step?'is-current':''} aria-hidden={!scene.reduced&&i!==step}><p lang="he" dir="rtl">{c.he}</p><p>{c.en}</p></div>)}</div>
  <Narration readyAt={.4} progress={scene.reduced?1:(step+local/cycle)/4} reduced={scene.reduced} lines={clauses.map(c=>c.body)}/>
 </div></div>;
}

const candidates=[
 {name:'Twin Cave near Qumran',image:'twin-cave-figure.webp',alt:'Bar-Adon’s published exterior photograph of the Twin Cave area, looking from the southeast.',text:'Twin Cave has a pillar and two reported east-facing openings; its ancient thresholds remain uncertain.'},
 {name:'IV/17 near Jericho',image:'iv17-plan.webp',alt:'Sion’s published plan of IV/17, showing a dividing pillar and two present openings.',text:'IV/17’s plan records a rock-cut pillar and two roughly southeast-facing openings.'},
 {name:'IV/11 near Jericho',image:'iv11-plan.png',alt:'Feig’s published plan of IV/11, including its scale and north arrow.',text:'IV/11 has a pillar, but its report does not establish two exterior entrances.'},
];
export function CandidateComparison(){
 const scene=useScrollScene(),step=stepAt(scene.value,4),all=scene.reduced||step===3;
 return <div className="story-scene story-candidates" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced} data-candidate={all?'comparison':candidates[step].name}><div className="story-sticky">
  <VisualBeat progress={scene.value} count={4} reduced={scene.reduced}><div className={`story-candidate-art${all?' compare-all':''}`}>{candidates.map((c,i)=><figure key={c.name} style={{opacity:all||i===step?1:0}} aria-hidden={!all&&i!==step}>{i===0&&!INTRO_PRIVATE_IMAGES?<div className="story-candidate-locator"><CandidateMap progress={1} reduced/></div>:<img src={`${base}introduction/${c.image}`} alt={c.alt}/>}{all&&<figcaption>{c.name}</figcaption>}</figure>)}</div>
  </VisualBeat><Narration progress={scene.value} reduced={scene.reduced} lines={[
   ...candidates.map(c=>c.text),
   'None of these comparisons establishes the ancient cave or a surviving deposit.',
  ]}/>
 </div></div>;
}
export function DuplicateEntry(){
 const scene=useScrollScene(),p=scene.value;
 return <div className="story-scene story-copy" ref={scene.ref} data-progress={p.toFixed(3)} data-reduced={scene.reduced}><div className="story-sticky">
  <VisualBeat progress={p} count={2} reduced={scene.reduced}><div className="story-copy-art"><svg className="story-copy-drawing" viewBox="0 0 800 160" aria-hidden="true" data-asset-family="atlas-relief-studies"><AtlasGlyph name="document" x={155} y={0} width={150} height={155}/><AtlasGlyph name="document" x={505} y={0} width={150} height={155} opacity={scene.reduced?.45:.45*clamp((p-.18)/.145)}/><path d="M335 77H474M462 67L474 77L462 87" fill="none" stroke="#9b613e" strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={scene.reduced?0:1-clamp((p-.08)/.245)}/></svg><p lang="he" dir="rtl" style={{opacity:scene.reduced?1:clamp(p*4)}}>משנא הכתב הזא</p><blockquote style={{opacity:scene.reduced?1:clamp((p-.18)/.145)}}>a copy of this document</blockquote></div>
  </VisualBeat><Narration progress={p} reduced={scene.reduced} lines={[
   'The final entry describes another copy with explanations, measurements and details.',
   'That copy remains unidentified; its explanations could have helped recover the valuables.',
  ]}/>
 </div></div>;
}
