"use client";
import {lazy,Suspense,useEffect} from 'react';
import {ArrowUpRight} from 'lucide-react';
import AtlasSiteNav from './atlas-site-nav';
import {Narration,stepAt,useScrollScene} from './atlas-intro-motion';
import intro from './atlas-intro-data.json';
import {StorySequence} from './atlas-intro-sequences';
import {AtlasGlyph} from './atlas-intro-glyphs';
import {INTRO_PRIVATE_IMAGES} from './atlas-intro-media';
import {EntryReveal,EntryMeaning,CandidateComparison,DuplicateEntry} from './atlas-intro-example';
import './atlas-introduction.css';
const DesertOpening=lazy(()=>import('./atlas-intro-opening'));
const base=import.meta.env?.BASE_URL??'/';
const repo='https://github.com/quadrin/CopperScroll/blob/main/';
const clamp=(n:number)=>Math.max(0,Math.min(1,n));

const caveLines=[
 'IV/17 has a rock-cut dividing pillar.',
 'The plan records two openings; their ancient shape is unresolved.',
 'The openings face roughly southeast today; their ancient orientation needs testing.',
 'To measure three cubits, we need the ancient entrance surface and direction.',
];
function CaveExample(){
 const scene=useScrollScene(),step=stepAt(scene.value,4),trace=scene.reduced?1:clamp((scene.value-.75)/.1625),depth=scene.reduced||step===3?1:0;
 const active=step===0?['pillar']:step===3?['north-mouth']:['north-mouth','south-mouth'];
 return <div className="story-scene story-cave" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced}><div className="story-sticky">
  <div className="story-cave-art">
   <svg className="story-cave-plan" viewBox="0 0 660 615" role="img" aria-label="Published IV/17 excavation plan, highlighting its pillar and two present openings." style={{opacity:scene.reduced?1:1-depth}}><image href={`${base}introduction/iv17-plan.webp`} width="660" height="615"/>{intro.cave.features.map(f=><g key={f.id} opacity={scene.reduced||active.includes(f.id)?1:0}><circle cx={f.x} cy={f.y} r={scene.reduced?28:14+14*clamp((scene.value*4%1)*3)} fill="#b16d3222" stroke="#a25627" strokeWidth="3"/><circle cx={f.x} cy={f.y} r="5" fill="#9c5024"/></g>)}</svg>
   <svg className="story-cave-depth" viewBox="0 0 660 400" role="img" aria-label="Illustrative downward measurement of three cubits from an assumed entrance surface; no observed deposit." style={{opacity:depth}}><AtlasGlyph name="strata" x={65} y={75} width={530} height={305}/><path d="M30 130H630" stroke="#6c7867" strokeWidth="2" strokeDasharray="8 8"/><path d="M330 130V310" stroke="#9c5024" strokeWidth="3" strokeDasharray="180" strokeDashoffset={180*(1-trace)}/><path d="M318 130H342M318 310H342" stroke="#9c5024" strokeWidth="2"/><circle cx="330" cy={130+180*trace} r="6" fill="#9c5024"/><text x="355" y="230">3 cubits</text></svg>
  </div>
  <Narration progress={scene.value} reduced={scene.reduced} lines={caveLines}/>
 </div></div>;
}
function ConstructionPhases(){
 const scene=useScrollScene(),repair=scene.reduced?1:clamp((scene.value-1/3)/(.65/3)),infill=scene.reduced?1:clamp((scene.value-2/3)/(.65/3));
 return <div className="story-scene story-phase" ref={scene.ref} data-progress={scene.value.toFixed(3)} data-reduced={scene.reduced}><div className="story-sticky">
  <svg className="story-phase-art" viewBox="0 0 760 340" role="img" aria-label="Illustrative construction section: a feature is cut, a repair lining is added, and later fill accumulates. No site-specific dates or samples.">
   <defs><pattern id="story-rock" width="14" height="14" patternUnits="userSpaceOnUse"><path d="M0 14L14 0" stroke="#748779" strokeWidth=".7" opacity=".3"/></pattern><pattern id="story-infill" width="25" height="20" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.5" fill="#8b775c"/><path d="M15 12l5 2" stroke="#8b775c"/></pattern></defs>
   <g><path d="M50 75H710V290H50Z" fill="#ded5bd"/><path d="M50 75H710V290H50Z" fill="url(#story-rock)"/>
   <path d="M225 75V120Q225 140 190 155Q155 175 155 225V255H605V225Q605 175 570 155Q535 140 535 120V75" fill="#f7f5ef" stroke="#536f60" strokeWidth="5"/>
   <path d="M238 105V125Q238 153 202 167Q170 185 170 225V242H590V225Q590 185 558 167Q522 153 522 125V105" fill="none" stroke="#bd8054" strokeWidth="14" opacity={repair}/>
   <g opacity={infill} ><path d="M180 212Q250 180 330 210T580 205V235H180Z" fill="#cfc0a8"/><path d="M180 212Q250 180 330 210T580 205V235H180Z" fill="url(#story-infill)"/></g>
  </g></svg>
  <Narration progress={scene.value} reduced={scene.reduced} lines={[
   'The feature must have existed when the writer knew the place.',
   'A sample may date a repair; the original construction can be older.',
   'Later fill can bury an entrance; dating that fill does not date the original feature.',
  ]}/>
 </div></div>;
}
export default function AtlasIntroduction(){
 useEffect(()=>{document.title='What is the Copper Scroll? · Copper Scroll Atlas';window.scrollTo(0,0);return()=>{document.title='The Copper Scroll Atlas';};},[]);
 return <div className="atlas-introduction">
  <a className="story-skip" href="#story-start" onClick={e=>{e.preventDefault();const el=document.getElementById('story-start');el?.focus();el?.scrollIntoView();}}>Skip to the story</a>
  <AtlasSiteNav entry="25" active="introduction"/>
  <main><Suspense fallback={<header className="story-opening-loading"><h1>What is the <br/>Copper Scroll?</h1></header>}><DesertOpening/></Suspense><div id="story-start" tabIndex={-1}/>
   <StorySequence chapter="inventory"/>
   <EntryReveal/><EntryMeaning/>
   <StorySequence chapter="locations"/>
   <CandidateComparison/>
   <StorySequence chapter="worked"/>
   <CaveExample/>
   <StorySequence chapter="time"/>
   <ConstructionPhases/>
   <StorySequence chapter="purpose"/>
   <DuplicateEntry/>
   <StorySequence chapter="ending"/><div className="story-links"><a href="#entry-25/2d">Compare the cave candidates <ArrowUpRight size={17}/></a><a href="#entry-25/scroll">Read Entry 25 in context <ArrowUpRight size={17}/></a></div>
  </main>
  <footer className="story-sources"><details><summary>Sources & image credits</summary><div>
   <p>Opening relief: <a href="https://mapterhorn.com/attribution/">Mapterhorn terrain</a>, using ASTER GDEM courtesy METI/NASA (isr10, processed by 4cast LTD using VTbuilder) and COPERNICUS GLO-30 (DLR / Airbus, provided under COPERNICUS by the EU and ESA). Modern elevations are visually exaggerated 1.65×. The 46 km regional, 12 km middle and 2.5 km local grids are sampled from Terrarium tiles; source URLs and hashes are retained in the opening terrain provenance file. The camera follows the historical survey point 8 = 3Q; the IAA CaveAtlas location differs by approximately 233 m. The final approach, cliff opening, chamber and two copper rolls are illustrations, not a registered survey or an exact reconstruction of ancient cave geometry. The discovery description records a largely collapsed ceiling and a surviving rear chamber of about 3 × 2 m. Landscape context, discovery location and illustrative interior remain distinct. Procedural limestone grain is illustrative surface detail, not additional surveyed elevation. The introductory landscape, vessels, Temple silhouette, courtyard and recovery diagrams are explanatory illustrations; they establish no architectural reconstruction, deposit, entry boundary or candidate-site coordinate.</p>
   <p>Discovery: W. L. Reed, <cite>BASOR</cite> 135 (1954), pp. 8–13, p. 10. <a href="https://www.jstor.org/stable/1355541">Report</a>. Opening: <a href="https://dqcaas.com/2016/11/24/1953-film-of-cutting-open-of-the-copper-scroll/">original cutting footage and provenance</a>.</p>
   <p>Copper lighting and the 3D scroll are illustrations. The repeating material uses a cropped photograph of strip 13 by Osama Shukir Muhammed Amin (2020), CC BY-SA 4.0; the surface is rearranged for illustration and does not reproduce the original column order. <a href="https://commons.wikimedia.org/wiki/File:Strip_13,_part_of_the_Copper_Dear_Sea_Scrolls,_from_Qumran_Cave_3,_Jordan_Museum.jpg">Photograph</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/">licence</a>. The unfolding is virtual; the brittle original was cut open. Strip widths, coil shape and repeated photographic surface are illustrative. Approximate dimensions: 2.4 m × 0.3 m. Modern Hebrew: M. G. Abegg Jr.’s transcription, <a href="https://github.com/ETCBC/dss">ETCBC</a>, <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>.</p>
   {INTRO_PRIVATE_IMAGES?<p>Worked example: Entry 25, column VI, lines 1–6. Radiographs 12D, 12C and 12G are unchanged embedded images from Brizemeure, Lacoudre and Puech, <cite>Le rouleau de cuivre 3Q15</cite> (2006), pp. 382–383, plates CCCXLIII–CCCXLIV. Original radiographs: EDF, rights reserved; epigraphic assemblies: Émile Puech. The Hebrew is edition-based, shown emerging from the approximate entry region; this is not a new letter-registered tracing. Separate images retain publication order, not a new geometric registration.</p>:<p>Worked example: Entry 25, column VI, lines 1–6. The public build shows an explicitly edition-based Hebrew passage, not a substitute manuscript photograph. The published radiographs in Brizemeure, Lacoudre and Puech (2006), pp. 382–383, plates CCCXLIII–CCCXLIV are cited but not redistributed here. The owner-private build retains the supplied figures. Twin Cave is represented by a regional locator in this public build; Bar-Adon’s copyrighted photograph remains a cited source.</p>}

   <p>Hebrew and interpretation: Puech, <cite>The Copper Scroll Revisited</cite> (2015), pp. 59–60 and 130–131, alongside the project reader. Brackets mark supplied letters; an editorial article correction is discussed in the edition. Western “42” renders the numeral’s value. The English here uses “silver-weight units” to leave the abbreviated unit open: the project reader uses talents, while Puech reads silver karsh. “Beneath it” retains the jar/manuscript ambiguity. The final-copy excerpt comes from XII 10–13 (Atlas Entry 60); the manuscript in Entry 25 is not identified as that copy.</p>
   <p>IV/17: Ofer Sion, 2002, <cite>ʿAtiqot</cite> 41, Plan 5, p. 63. <a href="https://publications.iaa.org.il/atiqot/vol41/iss1/6/">Publication</a>, <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>. Complete plan, original scale and north arrow retained. Highlight markers are project annotations. Entry 25 translation is the project’s; square brackets mark supplied letters. Depth and construction-phase drawings are illustrative, without measured site levels, samples or dates.</p>
   <p>The returning relief map reuses the opening’s modern elevation grid. Candidate pins use the Atlas’s Qumran and Jericho regional anchors for orientation; their screen offsets separate labels and do not register individual caves or entrances. IV/17 and IV/11 share a regional Jericho anchor. Twin Cave is shown in the Qumran region, not at an invented mouth coordinate.</p>
   <p>Candidate comparisons reuse existing source-linked assessments. Twin Cave: Bar-Adon, <cite>ʿAtiqot</cite>, Hebrew Series 9 (1989), pp. [15]–17, Fig. B1 (exterior photograph with original caption, no scale or labelled mouths), <a href="https://www.jstor.org/stable/23456199?seq=25">source</a>; copyright retained. IV/11: Nurit Feig, <cite>ʿAtiqot</cite> 41 (2002), pp. 85–90, Plan 1 p. 85; <a href="https://publications.iaa.org.il/atiqot/vol41/iss1/7/">publication</a>, CC BY-NC 4.0. Published scales, north arrows and captions are retained where present. No source-relative plan has been assigned an invented entrance coordinate. <a href={`${repo}research/assessments/entry25_iv17/README.md`}>IV/17 assessment and comparisons</a>; <a href={`${repo}research/sources/entry25_direction_review_2026-10-02.md`}>direction and reading alternatives</a>.</p>
   <p>Nature and purpose: <a href="https://dornsife.usc.edu/wsrp/copper-scroll/">USC West Semitic Research Project’s overview</a> presents real-treasure, Temple, community and fictional interpretations. <a href="https://cojs.org/the_copper_scroll-_lawrence_h-_schiffman-_reclaiming_the_dead_sea_scrolls-_jewish_publication_society-_philadelphia-_1994/">Lawrence Schiffman, <cite>Reclaiming the Dead Sea Scrolls</cite> (1994), Copper Scroll discussion</a>, argues for a Temple connection and against the fantasy interpretation; this is an attributed scholarly position. Puech 2015, Introduction p. 7, discusses durability and purpose. The page makes no new attribution of authorship, date or ownership.</p>
   <p>Object studies of generic caves, pottery, parchment, soil and metal vessels are generated explanatory renders, with photographic material detail. They are not photographs of excavated objects or surveyed features. The Copper Scroll detail instead uses the actual strip 13 photograph credited above. The Temple passage uses Berthold Werner’s photograph of the Holyland Model at the Israel Museum, a modern reconstruction of Herod’s Temple: <a href="https://commons.wikimedia.org/wiki/File:Jerusalem_Modell_BW_3.JPG">source photograph</a>, public domain. A viewport crop focuses on the Temple; no generative alteration is applied. The reconstruction does not establish the scroll’s ownership. Published manuscript photographs, radiographs and plans retain their separate source credits.</p>
   <p>Textual discussions: Milik (1962), Lefkovits (2000), Brizemeure, Lacoudre and Puech (2006) and later work. <a href={`${repo}research/sources/drive_index.md`}>Edition index</a>. Visual sequences draw on the Atlas and the owner-supplied <cite>Copper Scroll Editable</cite> deck, 2 November 2026. Copper illustration adapted from <cite>Copper Scroll Experimental Approaches</cite>.</p>
  </div></details></footer>
 </div>;
}
