import planData from './atlas-site-plans.json';
import scenes from './atlas-scenes.json';
import gallery from './atlas-site-gallery.json';
import type {Place} from './atlas-types';

export const explorationFilters=[{id:'walkable',label:'Walkable'},{id:'plan',label:'Has plan'},{id:'photos',label:'Has photos'}] as const;
export const siteRegions=[{id:'jerusalem',label:'Jerusalem'},{id:'jericho',label:'Jericho & Jordan Valley'},{id:'dead-sea',label:'Qumran & Dead Sea'},{id:'hills',label:'Judean hills & desert'},{id:'north',label:'Northern sites'}] as const;
export const siteFeatureTypes=[{id:'pools',label:'Pools & reservoirs'},{id:'cisterns',label:'Cisterns & wells'},{id:'caves',label:'Caves'},{id:'tombs',label:'Tombs'},{id:'channels',label:'Channels & aqueducts'},{id:'walls',label:'Gates & walls'},{id:'buildings',label:'Courtyards & buildings'}] as const;
export type ExploreFilter=typeof explorationFilters[number]['id'];
export type SiteRegion=typeof siteRegions[number]['id'];
export type SiteFeatureType=typeof siteFeatureTypes[number]['id'];
export type SiteFilters={explore:ExploreFilter[];region:SiteRegion|'';features:SiteFeatureType[]};
export const emptySiteFilters:SiteFilters={explore:[],region:'',features:[]};

const photographed=new Set([...scenes,...gallery].map(item=>item.placeId));
const deadSea=new Set(['kh_qumran','wadi_qumran','ein_feshkha']);
const north=new Set(['gerizim','beth_shean','ibziq','kh_salhab']);
export function regionForSite(place:Place):SiteRegion{
 if(deadSea.has(place.id))return 'dead-sea';
 if(north.has(place.id))return 'north';
 return place.region==='jerusalem'?'jerusalem':place.region==='jericho'?'jericho':'hills';
}
// Browse tags describe structures documented in the existing plan/dossier or
// gazetteer records, not the entry's requested feature or an identification.
// Untagged localities stay searchable; an omitted tag does not establish absence.
export const featuresForSite:Partial<Record<string,SiteFeatureType[]>>={
 jer_temple:['cisterns','walls'],jer_east_gate:['walls','cisterns'],jer_south_wall:['walls'],
 jer_kidron_mon:['tombs','buildings'],jer_kidron_east:['tombs'],jer_siloam:['pools','channels','walls'],
 jer_bir_ayyub:['cisterns'],jer_bethesda:['pools','cisterns','caves','channels'],jer_tombs_kings:['tombs'],
 hyrcania:['pools','cisterns','channels'],natuf:['caves'],nuweimeh:['caves','cisterns','buildings'],
 doq:['cisterns','channels'],tell_es_sultan:['walls','buildings'],jericho_palaces:['pools','channels','buildings'],
 kh_qumran:['pools','cisterns','channels','walls','buildings'],wadi_qumran:['channels'],gerizim:['walls','buildings'],
 ibziq:['cisterns','caves','tombs'],beth_horon:['tombs'],abu_saraj_iv17:['caves'],jer_givati:['pools','buildings'],
 ein_feshkha:['pools','channels','buildings'],fasael:['pools','channels','buildings'],cypros:['cisterns'],
};
export function explorationForSite(place:Place){
 const plans=planData.filter(plan=>plan.placeIds.includes(place.id));
 return {walkable:place.lat!==null&&place.lon!==null&&plans.some(plan=>!('kind' in plan)||plan.kind!=='survey-map'),plan:plans.length>0,photos:photographed.has(place.id)};
}
export function siteMatchesFilters(place:Place,query:string,filters:SiteFilters){
 const search=query.trim().toLocaleLowerCase();
 if(search&&!`${place.name} ${place.shortName}`.toLocaleLowerCase().includes(search))return false;
 if(filters.region&&regionForSite(place)!==filters.region)return false;
 const available=explorationForSite(place);
 if(!filters.explore.every(key=>available[key]))return false;
 return !filters.features.length||filters.features.some(key=>featuresForSite[place.id]?.includes(key));
}
