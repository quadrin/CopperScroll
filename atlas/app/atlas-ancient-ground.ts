import contextData from './atlas-site-context.json';
import type {LandscapePad} from './atlas-model-landscape';

// "Ancient ground": a plan placed in its mapped setting (atlas-site-context.json), drawn without
// today's mapped features: graves, roads, paths, stairs, walls, buildings, trees, and the green
// tint and paving on the ground. Nothing else changes. The ground stays today's terrain unless the
// plan's entry below is 'published' and gives levels for it.
//
// To add a published level, set `ground: 'published'`, cite it in `sources` (edition, page,
// figure), say in `note` what it is, and give one or more pads. A pad applies only in this view.
// It is a rectangle in the model's frame, the frame of model.markers (metres, x east, z south;
// for a plan placed in its setting that is the place frame of atlas-site-context.json). Inside
// it the ground is set to `level` metres above sea level, or to `y` in the model's own vertical
// frame; the ground then feathers back to today's terrain over `feather` metres. `turnDeg` turns
// the rectangle as three.js rotation.y turns an object, and `rise` makes it a ramp that climbs
// by that much from its local −z edge to its +z edge. `locator` names the printed level used.
export type AncientGroundPad={x:number;z:number;w:number;d:number;level?:number;y?:number;feather:number;turnDeg?:number;rise?:number;locator:string};
export type AncientGround={plan:string;ground:'illustrative'|'published';note:string;sources:string[];pads?:AncientGroundPad[]};

export const ANCIENT_GROUND:AncientGround[]=[
 {plan:'kidron-bene-hezir',ground:'illustrative',note:'No published ancient level is added: Avigad’s rock path (1954) is the model’s own ground, and Zechariah’s base is buried with no level in the pages read.',sources:[]},
 {plan:'temple-great-sea',ground:'illustrative',note:'No published ancient level is added for the court above the cistern.',sources:[]},
 {plan:'qumran-settlement',ground:'published',note:'The 31 room and court levels printed on Fig. 57 (rooms and courts only; pools and channels left out) range from −323.41 to −326.02 m, median −324.54 m. One pad over the settlement sets the ground to that median; the model stands on it in both views. Single rooms differ from it by up to 1.5 m.',sources:['Magen & Peleg 2018, Site Description, Fig. 57 p. 53 (spot levels, metres below sea level)'],pads:[{x:-62,z:66,w:80,d:110,level:-324.54,feather:12,locator:'median of the 31 room and court spot levels on Fig. 57 (−323.41 to −326.02 m)'}]},
 {plan:'bethesda-pools',ground:'illustrative',note:'No published ancient level is added: Schick 1888 gives the pool’s floor (2,359–2,390 ft) and the 1888 surface, not an ancient ground.',sources:[]},
 {plan:'east-gate-warren',ground:'illustrative',note:'No published ancient level is added: Warren’s levels of 1867 (feet above the Mediterranean) already shape the model’s own ground; they are survey-time surfaces and feature levels, not a dated ancient ground.',sources:[]},
 {plan:'jericho-early',ground:'illustrative',note:'No published ancient ground level is added: Netzer’s levels are on a local site datum with no stated benchmark, and the plaza level (median 100.47) is already the model’s own ground.',sources:[]},
 {plan:'jericho-late',ground:'illustrative',note:'No published ancient ground level is added: Netzer’s levels are on a local site datum with no stated benchmark, and the plaza level (median 100.47) is already the model’s own ground.',sources:[]},
 {plan:'gerizim-precinct',ground:'illustrative',note:'No published ancient level is added; the summit platform sits on today’s summit.',sources:[]},
 {plan:'hyrcania-waterworks',ground:'illustrative',note:'No published ancient level is added around the waterworks.',sources:[]},
];

const mapped=new Set(Object.keys((contextData as unknown as {plans:Record<string,unknown>}).plans));
// Whether a plan has mapped surroundings, and so the Today / Ancient ground choice.
export const hasAncientGround=(planId:string|null|undefined)=>!!planId&&mapped.has(planId);
export function ancientGround(planId:string):AncientGround{
 return ANCIENT_GROUND.find(e=>e.plan===planId)??{plan:planId,ground:'illustrative',note:'No published ancient level is added.',sources:[]};
}

export const TODAYS_TERRAIN='The ground is today’s terrain, shown without modern features; it is not an ancient surface.';
// Published pads in the landscape's form: heights relative to the terrain patch's centre, as the
// model's frame has them. Null when a pad gives a level above sea level and the patch is unknown.
export function ancientGroundPads(entry:AncientGround,centreElevation?:number):LandscapePad[]|null{
 if(entry.ground!=='published'||!entry.pads?.length)return null;
 const pads:LandscapePad[]=[];
 for(const p of entry.pads){
  const height=p.y??(p.level!==undefined&&centreElevation!==undefined?p.level-centreElevation:undefined);
  if(height===undefined||!Number.isFinite(height))return null;
  pads.push({x:p.x,z:p.z,w:p.w,d:p.d,height,feather:p.feather,angle:(p.turnDeg??0)*Math.PI/180,rise:p.rise});
 }
 return pads;
}
// The caption line: `applied` is false when the published pads could not be placed.
export function ancientGroundCaption(entry:AncientGround,applied:boolean){
 if(entry.ground==='published'&&applied)return `Near the site the ground follows published levels (${entry.sources.join('; ')}). Elsewhere it is today’s terrain, shown without modern features; it is not an ancient surface.`;
 return TODAYS_TERRAIN;
}
export function ancientGroundAssumption(entry:AncientGround,applied:boolean){
 return `Ancient ground view: today’s mapped features (graves, roads, paths, stairs, walls, buildings, trees, and the green tint and paving on the ground) are not drawn. ${ancientGroundCaption(entry,applied)} ${entry.note}`;
}
