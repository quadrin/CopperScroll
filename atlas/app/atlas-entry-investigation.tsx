"use client";
import {lazy,Suspense,useCallback,useEffect,useId,useRef,useState,type CSSProperties} from 'react';
import CandidateMap from './atlas-intro-candidate-map';
import {INTRO_PRIVATE_IMAGES} from './atlas-intro-media';
import {CopperReflection,FieldworkReflection} from './atlas-intro-reflections';
import './atlas-entry-investigation.css';
const IntroExplore=lazy(()=>import('./atlas-intro-explore'));

const base=import.meta.env.BASE_URL??'/';
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const ease=(v:number)=>{const t=clamp(v);return t*t*(3-2*t);};
type Scene='source'|'hebrew'|'cave'|'map'|'comparison'|'alteration'|'surface'|'datum'|'result'|'copper-reflection'|'landmark-reflection'|'hypothesis-reflection'|'fieldwork-reflection'|'explore';
type Cue={id:string;scene:Scene;line:string;he?:string;action?:number;reflection?:boolean};
export const entryCues:Cue[]=[
 {id:'source',scene:'source',line:'Let’s follow one: Entry 25.'},
 {id:'hebrew',scene:'hebrew',line:'Here is what it says.'},
 {id:'pillar',scene:'cave',action:0,he:'מערת העמוד',line:'“[In] the cave of the pillar…”'},
 {id:'openings',scene:'cave',action:1,he:'של שני [ה]פתחין צופא מזרח',line:'“…with two entrances, facing east…”'},
 {id:'north',scene:'cave',action:2,he:'[ב]פתח הצפוני',line:'“…[at] the northern entrance…”'},
 {id:'measure',scene:'cave',action:3,he:'חפור [א]מות שלוש',line:'“…dig three cubits.”'},
 {id:'jar',scene:'cave',action:4,he:'שמ קלל',line:'“There is a jar…”'},
 {id:'manuscript',scene:'cave',action:5,he:'בו ספר אחד',line:'“…in it one scroll…”'},
 {id:'silver',scene:'cave',action:6,he:'תחתו ככ 42',line:'“…beneath it, 42 silver-weight units.”'},
 {id:'find',scene:'map',action:0,line:'Could we find that cave?'},
 {id:'regions',scene:'map',action:1,line:'Three caves have been suggested.'},
 {id:'look',scene:'comparison',line:'What would we look for?'},
 {id:'features',scene:'comparison',action:3,line:'A pillar—and two entrances facing east.'},
 {id:'compare-pillar',scene:'comparison',action:0,line:'A pillar is described at all three.'},
 {id:'compare-openings',scene:'comparison',action:1,line:'Twin Cave and IV/17 also have two openings.'},
 {id:'compare-direction',scene:'comparison',action:2,line:'But are these the openings the writer knew?'},
 {id:'alteration',scene:'alteration',line:'Entrances can collapse or be rebuilt.'},
 {id:'ancient-surface',scene:'surface',line:'Ground levels can rise.'},
 {id:'datum',scene:'datum',line:'And “dig three cubits” only helps if we know where to start.'},
 {id:'result',scene:'result',line:'We still need to establish what these caves looked like when the instructions were written.'},
 {id:'intended-reader',scene:'copper-reflection',reflection:true,line:'Someone engraved these directions in copper. Who were they expecting to read them?'},
 {id:'familiar-landmark',scene:'landmark-reflection',reflection:true,line:'Perhaps a cave name or a familiar landmark was enough for that person to know where to go. What would they have recognized that we’re missing?'},
 {id:'predictions',scene:'comparison',action:3,reflection:true,line:'We can use the surviving clues to propose places—and work out what we should find there if a proposal is right.'},
 {id:'field-prediction',scene:'hypothesis-reflection',reflection:true,line:'For this cave, that might mean an older entrance floor, or evidence that both openings existed at the same time.'},
 {id:'fieldwork',scene:'fieldwork-reflection',reflection:true,line:'Those are hypotheses we can take into the field. Archaeological records, a site survey or excavation could help us test them.'},
 {id:'atlas-hypotheses',scene:'explore',action:0,reflection:true,line:'The Atlas lets us compare readings and proposed locations, then ask what evidence would distinguish one possibility from another.'},
 {id:'where-start',scene:'explore',action:1,reflection:true,line:'Where would you start?'},
];
const hebrew=['[ב]מערת העמוד של שני','[ה]פתחין צופא מזרח','[ב]פתח הצפוני חפור','[א]מות שלוש שמ קלל','בו ספר אחד תחתו','ככ 42'];
// Scroll selects a cue; one finite timeline owns action, phrase departure,
// caption fade and settled hold. It cannot advance to another cue by itself.
const ACTION_MS=1100,OUT_MS=180,IN_MS=260;
type Playback={index:number;previous:number;progress:number;caption:number;opacity:number;departure:number;settled:boolean};
function useInvestigation(){
 const ref=useRef<HTMLDivElement>(null);
 const mapReady=useRef(false);
 const markMapReady=useCallback(()=>{mapReady.current=true;},[]);
 const [reduced,setReduced]=useState(()=>typeof matchMedia!=='undefined'&&matchMedia('(prefers-reduced-motion: reduce)').matches);
 const [play,setPlay]=useState<Playback>({index:0,previous:0,progress:0,caption:-1,opacity:0,departure:0,settled:false});
 useEffect(()=>{
  const query=matchMedia('(prefers-reduced-motion: reduce)');let animation=0,scheduled=0,current=-1,caption=-1,started=0,previous=0,waitingAt=0;
  const frame=(now:number)=>{
   const elapsed=now-started;
   if(elapsed<OUT_MS){
    setPlay({index:previous,previous,progress:1,caption,opacity:caption<0?0:1-ease(elapsed/OUT_MS),departure:ease(elapsed/OUT_MS),settled:false});
    animation=requestAnimationFrame(frame);return;
   }
   if(entryCues[current].scene==='map'&&!mapReady.current){
    if(!waitingAt)waitingAt=now;setPlay({index:current,previous,progress:0,caption:-1,opacity:0,departure:1,settled:false});
    animation=requestAnimationFrame(frame);return;
   }
   if(waitingAt){started+=now-waitingAt;waitingAt=0;}
   const actionTime=now-started-OUT_MS,progress=ease(actionTime/ACTION_MS),complete=actionTime>=ACTION_MS;
   caption=complete?current:-1;
   const opacity=complete?ease((actionTime-ACTION_MS)/IN_MS):0,settled=actionTime>=ACTION_MS+IN_MS;
   setPlay({index:current,previous,progress,caption,opacity,departure:1,settled});
   if(!settled)animation=requestAnimationFrame(frame);
  };
  const update=()=>{
   scheduled=0;const el=ref.current;if(!el||query.matches)return;
   const rect=el.getBoundingClientRect(),stage=el.firstElementChild as HTMLElement|null,height=stage?.offsetHeight||innerHeight;
   if(rect.top>height*.1||rect.bottom<height*.2)return;
   const p=clamp(-rect.top/Math.max(1,rect.height-height)),target=Math.min(entryCues.length-1,Math.floor(p*entryCues.length));
   if(target===current)return;
   const initial=current<0;cancelAnimationFrame(animation);previous=initial?target:current;current=target;started=performance.now()-(initial?OUT_MS:0);
   if(entryCues[current].scene==='map'&&entryCues[previous].scene!=='map')mapReady.current=false;
   waitingAt=0;
   setPlay({index:previous,previous,progress:initial?0:1,caption,opacity:caption<0?0:1,departure:0,settled:false});
   animation=requestAnimationFrame(frame);
  };
  const schedule=()=>{if(!scheduled)scheduled=requestAnimationFrame(update);};
  const preference=()=>{setReduced(query.matches);cancelAnimationFrame(animation);current=-1;schedule();};
  const visibility=()=>{cancelAnimationFrame(animation);if(!document.hidden&&current>=0)animation=requestAnimationFrame(frame);};
  window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);query.addEventListener('change',preference);document.addEventListener('visibilitychange',visibility);
  const observer=new ResizeObserver(schedule);if(ref.current)observer.observe(ref.current);schedule();
  return()=>{cancelAnimationFrame(animation);cancelAnimationFrame(scheduled);observer.disconnect();window.removeEventListener('scroll',schedule);window.removeEventListener('resize',schedule);query.removeEventListener('change',preference);document.removeEventListener('visibilitychange',visibility);};
 },[reduced]);
 return {ref,play,reduced,markMapReady};
}

function SourcePassage({phase,progress}:{phase:'source'|'hebrew';progress:number}){
 return <div className={'investigation-passage investigation-'+phase} style={{opacity:ease(progress*2),transform:'translateY('+((1-progress)*12)+'px)'}}>
  {phase==='source'?(INTRO_PRIVATE_IMAGES?<div className="investigation-radiographs">{['12g','12c','12d'].map(tag=><img key={tag} src={base+'introduction/entry25-'+tag+'.jpeg'} alt={'Published column VI radiograph '+tag.toUpperCase()+'; Entry 25 region.'}/>)}</div>:<svg className="investigation-column-locator" viewBox="0 0 900 440" role="img" aria-label="Entry 25 is in column VI, lines 1–6. Schematic column locator, not a manuscript reconstruction.">{Array.from({length:12},(_,i)=><g key={i}><rect x={20+i*73} y="80" width="54" height="270" fill={i===5?'#dbc4a0':'#e8e1d3'} opacity={i===5?1:.45}/><text x={47+i*73} y="390" textAnchor="middle" fill="#7b6248" fontSize="16">{['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII'][i]}</text>{i===5&&<path d="M383 95H437V209H383Z" fill="#a56a3b" opacity={.2*progress}/>}</g>)}</svg>):
   <div className="investigation-passage-text"><span className="investigation-source-label">VI 1–6 · Entry 25</span>{hebrew.map((line,i)=><p key={i} lang="he" dir="rtl">{line}</p>)}</div>}
 </div>;
}

// Outlines follow the NEW illustrative artwork, never a surveyed cave.
function CaveArt({action,progress,surface=false,alteration=false,datum=false,testOpenings=false}:{action:number;progress:number;surface?:boolean;alteration?:boolean;datum?:boolean;testOpenings?:boolean}){
 const id=useId().replace(/:/g,'');
 const reveal=(n:number)=>surface||alteration?0:action>n?1:action===n?progress:0;
 return <div className="investigation-cave-wrap" data-cave-action={surface?'surface':action} style={{'--cave-pan':surface?'0%':action===0?'10%':action===2?'33%':action>=4?'-15%':'0%'} as CSSProperties}><svg className="investigation-cave" viewBox="0 0 1200 850" role="img" aria-label={surface?'Illustrative cave section with two possible ground levels; the ancient surface is unknown.':'Illustrative two-entrance cave. Pillar, orientation, measurement and listed contents appear in sequence; no particular archaeological site is reconstructed.'}>
  <defs>
   <linearGradient id={id+'-light'} x1="0" x2="1"><stop stopColor="#f3d99a" stopOpacity="0"/><stop offset="1" stopColor="#f3d99a" stopOpacity=".7"/></linearGradient>
   <linearGradient id={id+'-pot'}><stop stopColor="#8a492d"/><stop offset=".48" stopColor="#bb7547"/><stop offset="1" stopColor="#8d4b2c"/></linearGradient>
   <clipPath id={id+'-pillar'}><path d="M442 274L584 188L643 257L584 359L564 496L586 559L528 602L332 605L363 552L402 493L420 394Z"/></clipPath>
   <clipPath id={id+'-left'}><path d="M204 310L357 272L416 344L379 483L355 538L198 531Z"/></clipPath>
   <clipPath id={id+'-right'}><path d="M644 263L766 215L945 260L994 349L949 533L575 571L600 379Z"/></clipPath>
  </defs>
  <g transform={surface?'translate(-55 -35) scale(.93)':undefined}>
   <image href={base+'introduction/entry-investigation/limestone-cave.svg'} width="1200" height="800" opacity={surface?.68:action===0?.3+.7*progress:1}/>
   {action===0&&<g clipPath={'url(#'+id+'-pillar)'}><image href={base+'introduction/entry-investigation/limestone-cave.svg'} width="1200" height="800"/><path d="M442 274L584 188L643 257L584 359L564 496L586 559L528 602L332 605L363 552L402 493L420 394Z" fill="#ac6e35" fillOpacity={.12*progress} stroke="#a36737" strokeWidth="0" pathLength="1" strokeDasharray="1" strokeDashoffset={1-progress}/></g>}
   <g opacity={reveal(1)}>
    <path d="M1180 290L785 360L784 540L1180 625Z" fill={'url(#'+id+'-light)'} opacity={action===1?.65:.15}/>
    {[id+'-left',id+'-right'].map(key=><g key={key} clipPath={'url(#'+key+')'}><rect x="160" y="200" width="850" height="400" fill="#d7b471" opacity={action===1?.2:0}/></g>)}
    <path d="M1055 240H1145M1125 230L1145 240L1125 250" stroke="#997044" strokeWidth="2" fill="none"/><text x="1100" y="218" textAnchor="middle" className="investigation-svg-label">E</text>
   </g>
   <g opacity={reveal(2)*(action===2?1:.4)}>
    <ellipse cx="284" cy="460" rx="86" ry="95" fill="#dfc48c" fillOpacity=".08" stroke="#9c603b" strokeWidth="2.5" strokeDasharray="6 7"/>

   </g>
   <g opacity={reveal(3)}>
    <path d="M260 565L398 655M249 578L271 551M387 669L410 642" stroke="#955c36" strokeWidth="3" fill="none" pathLength="1" strokeDasharray="1" strokeDashoffset={action===3?1-progress:0}/>
    <text x="234" y="675" className="investigation-svg-label">3 cubits</text>

   </g>
   <g transform={'translate(755 '+(578+(1-reveal(4))*28)+')'} opacity={reveal(4)}>
    <ellipse cy="98" rx="64" ry="9" fill="#594b36" opacity=".12"/>
    <path d="M-37-8C-73-32-76 10-50 31M37-8C73-32 76 10 50 31" fill="none" stroke="#75452c" strokeWidth="11"/>
    <path d="M-34-24Q-40-13-52 2C-65 29-41 69-24 91Q0 100 24 91C41 69 65 29 52 2Q40-13 34-24Z" fill={'url(#'+id+'-pot)'} stroke="#70452d" strokeWidth="2.5"/>
    <path d="M-32-23H32L29-35H-29Z" fill="#b97d50" stroke="#70452d" strokeWidth="2"/><ellipse cy="-36" rx="31" ry="7" fill="#4f3426"/>
    <path d="M-44 6Q0 16 44 6M-38 61Q0 70 38 61" stroke="#d69761" strokeWidth="2" fill="none"/>
    <g transform={'translate(0 '+(-reveal(5)*70)+')'} opacity={reveal(5)}>
     <path d="M-14-8V-62Q0-70 14-62V-8Q0-1-14-8Z" fill="#ddc5a0" stroke="#826b4c" strokeWidth="1.5"/><ellipse cy="-62" rx="14" ry="6" fill="#f1dfbd" stroke="#826b4c" strokeWidth="1.5"/>
     <path d="M-6-59Q6-63 7-59Q-2-55-5-59M-8-49V-13M1-48V-12" stroke="#a88c64" fill="none"/>
    </g>
    <g opacity={reveal(6)} transform={'translate(0 '+(120+(1-reveal(6))*12)+')'}>
     <path d="M-54 0L-26-12L9-5L-12 8ZM-10 7L19-7L54 0L30 14Z" fill="#b7b9ae" stroke="#737d74" strokeWidth="1.5"/>
     <path d="M-54 0V10L-12 18V8M-10 7V17L30 25V14M54 0V10L30 25M9-5V4L-12 18" fill="#8c978e" stroke="#737d74" strokeWidth="1.5"/>
    </g>
   </g>
   {alteration&&<g opacity={progress}>
    <g transform={'translate(0 '+(-100*(1-progress))+')'}>
     <path d="M225 430L270 398L312 425L300 481L248 492L205 465Z" fill="#bc9e75" stroke="#987d59" strokeWidth="2"/>
     <path d="M270 398L281 443L248 492L300 481L312 425Z" fill="#9c805d"/>
     <path d="M180 502L230 467L283 493L305 531L251 556L188 548Z" fill="#d7bd96" stroke="#987d59" strokeWidth="2"/>
    </g>
    {[0,1,2].map(row=>[0,1,2].map(col=><path key={row+'-'+col} d={'M'+(642+col*65+(row%2)*20)+' '+(535-row*28)+'h60v25h-60Z'} fill={row%2?'#c2ab88':'#b59a74'} stroke="#8b7659" strokeWidth="1.5" opacity={clamp(progress*3-row*.6)}/>))}
   </g>}
   {testOpenings&&<g opacity={clamp((progress-.5)*2)} fill="none" stroke="#98603a" strokeWidth="3" strokeDasharray="7 8"><ellipse cx="284" cy="460" rx="86" ry="95"/><ellipse cx="790" cy="434" rx="172" ry="133"/></g>}
   {surface&&<g>
    <path d={'M80 '+(600-90*(datum?1:progress))+'Q400 '+(585-90*(datum?1:progress))+' 1070 '+(635-90*(datum?1:progress))+'L1080 735Q550 760 75 690Z'} fill="#d6c5aa" opacity={.7*progress}/>
    <path d="M100 610Q480 590 1080 640" stroke="#7d816c" strokeWidth="2" strokeDasharray="7 7" fill="none"/>
    <path d={'M100 '+(610-90*(datum?1:progress))+'Q480 '+(590-90*(datum?1:progress))+' 1080 '+(640-90*(datum?1:progress))} stroke="#9c603b" strokeWidth="3" fill="none"/>
    {datum&&<g opacity={progress}>
     <path d="M440 523V660M426 523H454M426 660H454M550 613V750M536 613H564M536 750H564" fill="none" stroke="#945b34" strokeWidth="3"/>
     <text x="460" y="585" className="investigation-svg-label">3 cubits</text><text x="570" y="690" className="investigation-svg-label">3 cubits</text>
    </g>}
    <text x="970" y="497" className="investigation-svg-label" opacity={progress}>later ground</text><text x="985" y="688" className="investigation-svg-label">earlier surface?</text>
   </g>}
  </g>
 </svg></div>;
}

const candidateNames=['Twin Cave','IV/17','IV/11'];
function EvidenceComparison({action,progress,summary=false}:{action:number;progress:number;summary?:boolean}){
 return <div className="investigation-comparison" data-comparison-clue={summary?'summary':['pillar','openings','direction','combined'][action]}>{candidateNames.map((name,i)=><figure key={name}>
  <a className="investigation-evidence-image" href={i===0&&!INTRO_PRIVATE_IMAGES?'https://github.com/quadrin/CopperScroll/blob/main/research/assessments/entry25_iv17/README.md':base+'introduction/'+['twin-cave-figure.webp','iv17-plan.webp','iv11-plan.png'][i]} target="_blank" rel="noreferrer" aria-label={'Open '+name+' source '+(i===0?'photograph':'plan')}>
   {i===0&&!INTRO_PRIVATE_IMAGES?<div className="investigation-public-locator"><svg viewBox="0 0 660 615" aria-label="Regional locator near Qumran, not a photograph of Twin Cave"><path d="M80 100Q260 40 490 220L570 515L305 475L85 220Z" fill="#d8cfbb"/><path d="M440 265L570 515L470 480L395 320Z" fill="#a5b5ac"/><circle cx="330" cy="265" r="9" fill="#9c603b"/><text x="330" y="310" textAnchor="middle">Near Qumran</text></svg></div>:<svg viewBox={i===2?'0 0 594 510':i===1?'0 0 660 615':'0 0 1200 520'} role="img" aria-label={name+': '+(i===0?'published exterior photograph':'complete published survey plan, retaining scale and north arrow')}>
    <image href={base+'introduction/'+['twin-cave-figure.webp','iv17-plan.webp','iv11-plan.png'][i]} width={i===2?594:i===1?660:1200} height={i===2?510:i===1?615:520} preserveAspectRatio="xMidYMid meet"/>
    {i===1&&!summary&&<g opacity={progress} fill="#ad713b" fillOpacity=".12" stroke="#a15d32" strokeWidth="3">{action===3?<><ellipse cx="415" cy="380" rx="80" ry="82"/><ellipse cx="562" cy="416" rx="34" ry="35"/><ellipse cx="231" cy="442" rx="44" ry="30"/></>:action===0?<ellipse cx="415" cy="380" rx="80" ry="82"/>:action===1?<><ellipse cx="562" cy="416" rx="34" ry="35"/><ellipse cx="231" cy="442" rx="44" ry="30"/></>:<ellipse cx="133" cy="119" rx="49" ry="62"/>}</g>}
   </svg>}
  </a>
  <figcaption><strong>{name}</strong><span>{i===0?'near Qumran':'near Jericho'}</span></figcaption>

 </figure>)}</div>;
}
function InvestigationVisual({cue,progress,onMapReady}:{cue:Cue;progress:number;onMapReady?:()=>void}){
 if(cue.scene==='copper-reflection')return <CopperReflection progress={progress}/>;
 if(cue.scene==='landmark-reflection')return <CaveArt action={0} progress={progress}/>;
 if(cue.scene==='hypothesis-reflection')return <CaveArt action={3} progress={progress} surface datum testOpenings/>;
 if(cue.scene==='fieldwork-reflection')return <FieldworkReflection progress={progress}/>;
 if(cue.scene==='explore')return <Suspense fallback={<div className="intro-atlas-loading"/>}><IntroExplore progress={cue.action===0?progress:1} active={cue.action===1&&progress===1}/></Suspense>;
 if(cue.scene==='source'||cue.scene==='hebrew')return <SourcePassage phase={cue.scene} progress={progress}/>;
 if(['cave','surface','alteration','datum'].includes(cue.scene))return <CaveArt action={cue.action??3} progress={progress} surface={cue.scene==='surface'||cue.scene==='datum'} alteration={cue.scene==='alteration'} datum={cue.scene==='datum'}/>;
 if(cue.scene==='map')return <div className="investigation-map"><CandidateMap progress={cue.action===0?.24*progress:.24+.76*progress} onReady={onMapReady}/></div>;
 return <EvidenceComparison action={cue.action??0} progress={progress} summary={cue.scene==='result'||cue.id==='look'}/>;
}
export default function EntryInvestigation(){
 const {ref,play,reduced,markMapReady}=useInvestigation(),cue=entryCues[play.index],old=entryCues[play.previous],sameScene=cue.scene===old.scene;
 if(reduced)return <section className="entry-investigation-static" aria-label="Following Entry 25">{entryCues.map(cue=><article key={cue.id} data-cue={cue.id} data-reflection={!!cue.reflection}>
  {cue.id!=='find'&&cue.id!=='atlas-hypotheses'&&<div className="investigation-static-art"><InvestigationVisual cue={cue} progress={1}/></div>}{cue.he&&<p className="investigation-hebrew" lang="he" dir="rtl">{cue.he}</p>}<p className="investigation-static-caption">{cue.line}</p>
 </article>)}<FurtherReading/></section>;
 return <><div ref={ref} className="entry-investigation" aria-label="Following Entry 25" style={{'--investigation-beats':entryCues.length} as CSSProperties} data-cue={cue.id} data-index={play.index} data-cue-count={entryCues.length} data-reflection={!!cue.reflection} data-settled={play.settled} data-action-complete={play.progress===1} data-caption-index={play.caption} data-motion="single-controller">
  <div className="investigation-sticky">
   <div className="investigation-art">
    {!sameScene&&play.progress<.5&&<div key="outgoing" className="investigation-art-layer" aria-hidden="true" inert style={{opacity:1-ease(play.progress*2)}}><InvestigationVisual cue={old} progress={1}/></div>}
    <div key="current" className="investigation-art-layer" style={{opacity:sameScene?1:ease(play.progress*2)}}><InvestigationVisual cue={cue} progress={play.progress} onMapReady={markMapReady}/></div>
   </div>
   <div className="investigation-reading">
    <div className="investigation-phrase" aria-hidden="true">
     {cue.he&&<p className="investigation-hebrew" lang="he" dir="rtl" style={{opacity:play.caption===play.index?play.opacity:0}}>{cue.he}</p>}
    </div>
    <p className="investigation-caption" style={{opacity:play.opacity}}>{play.caption>=0?entryCues[play.caption].line:'\u00a0'}</p>
   </div>
  </div>
 </div><FurtherReading/></>;
}
function FurtherReading(){return <aside className="investigation-further"><details><summary>Notes on the reading and the proposed caves</summary><div>
 <p>The illustration follows one reading of Entry 25. “Pillar” may instead mean a platform or terrace; the direction of the three-cubit instruction and the ancient starting surface remain uncertain. “Beneath it” can refer to the jar or the manuscript, and the silver’s weight unit is disputed.</p>
 <p>The map marks the Qumran and Jericho regions, not individual cave mouths. IV/17 has two present openings facing roughly southeast; IV/11’s report does not establish two exterior entrances. The illustration follows one possible reading and is not a surveyed reconstruction. No deposit has been verified at these proposed locations.</p>
 <p>For the whole scroll, proposed explanations include a practical recovery record, Temple property, property of another community, and a literary account. The material and detailed instructions do not settle its ownership or purpose.</p>
 <p>The final entry mentions another copy with explanations and measurements. That copy remains unidentified; it is a separate reference from the manuscript listed in Entry 25.</p>
 <a href="#entry-25/scroll">Read the passage and its alternatives</a>
 </div></details></aside>;}
