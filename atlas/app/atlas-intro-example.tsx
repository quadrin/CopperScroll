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
 const lift=scene.reduced?1:clamp((p-.12)/.35),translation=scene.reduced?1:clamp((p-.56)/.23);
 const imageOpacity=scene.reduced?1:1-clamp((p-.15)*3);
 const phase=p<.22?'image':p<.56?'hebrew':'english';
 return <div className="story-scene story-entry-reveal" ref={scene.ref} data-progress={p.toFixed(3)} data-reduced={scene.reduced} data-reading-phase={phase}><div className="story-sticky">
  <div className="story-entry-art">
   <div className="story-entry-radiographs" style={{opacity:imageOpacity,transform:scene.reduced?undefined:`scale(${1+p*.12})`}}>{INTRO_PRIVATE_IMAGES?['12g','12c','12d'].map(tag=><img key={tag} src={`${base}introduction/entry25-${tag}.jpeg`} alt={`Published column VI radiograph ${tag.toUpperCase()}, containing the Entry 25 passage.`}/>):<EditionPassage/>}</div>
   <div className="story-entry-hebrew" lang="he" dir="rtl" style={{opacity:scene.reduced?1:lift*(1-translation),transform:scene.reduced?undefined:`translate(${(1-lift)*20}%,${(1-lift)*-70}px)`}} aria-hidden={!scene.reduced&&(lift<.5||translation>.5)}>{hebrew.map((line,i)=><p key={i} style={{opacity:scene.reduced?1:clamp((p-.13-i*.025)*7)}}>{line}</p>)}</div>
   <blockquote className="story-entry-english" style={{opacity:translation,transform:scene.reduced?undefined:`translateY(${(1-translation)*30}px)`}} aria-hidden={!scene.reduced&&translation<.5}>{english.map((line,i)=><p key={i}><AnimatedWords text={line} progress={scene.reduced?1:clamp((p-.56-i*.025)*7)} reduced={scene.reduced}/></p>)}</blockquote>
  </div>
  <Narration progress={p} reduced={scene.reduced} lines={[
   INTRO_PRIVATE_IMAGES?'We will follow one entry from the metal to the landscape. Entry 25 occupies the first six lines of column VI, shown here in published radiographs.':'We will follow one example from the text to the landscape. Entry 25 occupies the first six lines of column VI; this public view shows the edition-based passage, rather than a manuscript photograph.',
   'The Hebrew is lifted into modern type so we can read the passage together. Brackets mark supplied letters in damaged areas; the reading comes from editions.',
   'It describes a cave, two entrances, a direction, a measured instruction—and a jar containing a manuscript, with silver beneath “it.” We will work through what those words could mean.',
  ]}/>
 </div></div>;
}
const clauses=[
 {he:'מערת העמוד',en:'the cave of the pillar',body:'First comes the landmark. A pillar might distinguish a cave, but the word has also been interpreted as a platform or terrace. That choice changes the kind of place to look for.'},
 {he:'של שני [ה]פתחין צופא מזרח',en:'two entrances, facing east',body:'Next come the openings and the direction. Does east-facing describe the cave as a whole, or each mouth? Those are different requirements to compare with a site.'},
 {he:'[ב]פתח הצפוני חפור [א]מות שלוש',en:'at the northern entrance, dig three cubits',body:'Then a reference point and a distance. Which surface was the ancient entrance? In which direction was the measurement intended? The number alone cannot supply a digging point.'},
 {he:'שמ קלל בו ספר אחד תחתו ככ 42',en:'a jar, one scroll, and 42 silver-weight units',body:'Finally the contents. “Beneath it” could refer to the jar or the manuscript inside it. Even the abbreviated monetary unit is disputed: the Atlas reader uses talents; Puech interprets silver karsh.'},
];
export function EntryMeaning(){
 const scene=useScrollScene(),step=stepAt(scene.value,4);
 return <div className="story-scene story-entry-meaning" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced}><div className="story-sticky">
  <div className="story-clause-art"><svg className="story-clue-drawing" viewBox="0 0 800 220" aria-hidden="true" data-asset-family="atlas-relief-studies"><AtlasGlyph name="cave" x={100} y={0} width={360} height={215} opacity={scene.reduced||step!==3?1:.25}/><g opacity={scene.reduced||step===1?1:0}><path d="M445 168H510M499 159L510 168L499 177" fill="none" stroke="#9b613e" strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={scene.reduced?0:1-clamp((scene.value*4%1)*3)}/></g><g opacity={scene.reduced||step===2?1:0}><path d="M477 84V190M469 84H485M469 190H485" fill="none" stroke="#9b613e" strokeWidth="2"/></g><AtlasGlyph name="jar" x={530} y={42} width={115} height={160} opacity={scene.reduced||step===3?1:0}/><AtlasGlyph name="silver" x={650} y={84} width={140} height={115} opacity={scene.reduced||step===3?1:0}/></svg>{clauses.map((c,i)=><div key={i} className={scene.reduced||i===step?'is-current':''} aria-hidden={!scene.reduced&&i!==step}><p lang="he" dir="rtl">{c.he}</p><p><AnimatedWords text={c.en} progress={scene.reduced?1:clamp((scene.value*4%1)*2)} reduced={scene.reduced}/></p></div>)}</div>
  <Narration progress={scene.value} reduced={scene.reduced} lines={clauses.map(c=>c.body)}/>
 </div></div>;
}
const candidates=[
 {name:'Twin Cave near Qumran',image:'twin-cave-figure.webp',alt:'Bar-Adon’s published exterior photograph of the Twin Cave area, looking from the southeast.',text:'Twin Cave, about a kilometre north of Qumran, is a plausible comparison: Bar-Adon describes a thick rock pillar and two openings facing east. The photograph supplies no measured entrance plan, and the ancient thresholds and date of that arrangement remain uncertain.'},
 {name:'IV/17 near Jericho',image:'iv17-plan.webp',alt:'Sion’s published plan of IV/17, showing a dividing pillar and two present openings.',text:'IV/17, in the Abu Saraj cliffs near Jericho, offers a surveyed plan with a rock-cut pillar and two present openings. Their plan-derived directions are roughly southeast; ancient orientation, blocking, floor levels and entrance phases still need to be resolved.'},
 {name:'IV/11 near Jericho',image:'iv11-plan.png',alt:'Feig’s published plan of IV/11, including its scale and north arrow.',text:'Nearby IV/11 is called the Cave of the Pillar in modern publications. It has an internal pillar, but the inspected report does not establish the required pair of exterior entrances. The name alone is a weak reason to prefer it.'},
];
export function CandidateComparison(){
 const scene=useScrollScene(),step=stepAt(scene.value,4),all=scene.reduced||step===3;
 return <div className="story-scene story-candidates" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced} data-candidate={all?'comparison':candidates[step].name}><div className="story-sticky">
  <div className={`story-candidate-art${all?' compare-all':''}`}>{candidates.map((c,i)=><figure key={c.name} style={{opacity:all||i===step?1:0,transform:all||scene.reduced?undefined:`translateY(${(1-clamp(scene.value*4%1))*8}px)`}} aria-hidden={!all&&i!==step}>{i===0&&!INTRO_PRIVATE_IMAGES?<div className="story-candidate-locator"><CandidateMap progress={1} reduced/></div>:<img src={`${base}introduction/${c.image}`} alt={c.alt}/>}{all&&<figcaption>{c.name}</figcaption>}</figure>)}</div>
  <Narration progress={scene.value} reduced={scene.reduced} lines={[
   ...candidates.map(c=>c.text),
   'The comparison changes the question. IV/17 has a useful plan; Twin Cave shares the pillar, paired openings and reported eastward aspect; IV/11 supplies only part of the arrangement. None yet establishes the scroll’s cave, its ancient digging surface, or a surviving deposit.',
  ]}/>
 </div></div>;
}
export function DuplicateEntry(){
 const scene=useScrollScene(),p=scene.value;
 return <div className="story-scene story-copy" ref={scene.ref} data-progress={p.toFixed(3)} data-reduced={scene.reduced}><div className="story-sticky">
  <div className="story-copy-art"><svg className="story-copy-drawing" viewBox="0 0 800 160" aria-hidden="true" data-asset-family="atlas-relief-studies"><AtlasGlyph name="document" x={155} y={0} width={150} height={155}/><AtlasGlyph name="document" x={505} y={0} width={150} height={155} opacity={scene.reduced?.45:.45*clamp((p-.35)*3)}/><path d="M335 77H474M462 67L474 77L462 87" fill="none" stroke="#9b613e" strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={scene.reduced?0:1-clamp((p-.18)*3)}/></svg><p lang="he" dir="rtl" style={{opacity:scene.reduced?1:clamp(p*4)}}>משנא הכתב הזא</p><blockquote style={{opacity:scene.reduced?1:clamp((p-.35)*4)}}>a copy of this document</blockquote></div>
  <Narration progress={p} reduced={scene.reduced} lines={[
   'The final entry adds another puzzle. It points to a copy of the document, with explanations, measurements and details of the individual items.',
   'If the inventory was meant to be used, another copy and its explanations would have helped a reader recover what was hidden. The text says that copy existed; it has not been identified. This is a separate claim from the manuscript in our cave example.',
  ]}/>
 </div></div>;
}
