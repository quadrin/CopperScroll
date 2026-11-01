import planData from "./atlas-site-plans.json";
import atlasData from "./atlas-data.json";
import { entryHash, parseAtlasHash } from "./atlas-navigation";
import {isInspectionView,type InspectionView} from './atlas-context-routes';
export type Camera = { center: [number, number]; zoom: number; bearing: number; pitch: number };
export type ModelCamera = { position: [number,number,number]; target: [number,number,number]; zoom: number; up?: [number,number,number]; projection?: "orthographic"|"perspective"; navigation?: "pan"|"orbit" };
export type Viewport = { x: number; y: number; zoom: number };
export type SiteFeature = { id: string; label: string; x: number; y: number; path?: string; kind: string; entryIds: string[]; description: string; limit: string; sources: string[]; sourceUrl: string };
export type SitePlan = { id: string; placeIds: string[]; label: string; kind?: "site-plan" | "survey-map"; width: number; height: number; transform?: string; image?: string; shapes?: { d: string; kind: string }[]; annotations?: { x: number; y: number; text: string }[]; north?: { x: number; y: number; dx: number; dy: number }; scale?: { x: number; y: number; length: number; label: string }; features: SiteFeature[]; source: string; sourceUrl?: string; credit: string; licenseUrl?: string; limit: string; traced?: string; layers?: PlanLayer[]; terrain?: "wide" };
// A traced plan can be shown as excavated remains or as a published reconstruction of one phase.
export type PlanLayer = { id: string; label: string; kind: "observed" | "published-reconstruction" };
export const sitePlans = planData as SitePlan[];
export const plansForPlace = (id: string | null) => sitePlans.filter(p => id && p.placeIds.includes(id));
export type ExplorerState = {
 entryId: string; placeId: string | null; mode: string; planId: string | null; featureId: string | null;
 siteView: "plan" | "photo"; highlightId?: string | null; scrollPhoto: boolean; scroll3d?: boolean; workbench: string | null; recordId: string | null;
 representation?: "model" | "source" | "walk"; modelCamera?: ModelCamera;
 explicitPlace?: boolean;
 inspection?:InspectionView|null;
 camera?: Camera; viewport?: Viewport; photoViewport?: Viewport; scrollTop?: number; scrollColumn?: number;
};
export const initialExplorer: ExplorerState = { entryId: "21", placeId: "kh_qumran", mode: "site", planId: "qumran-ilan", featureId: null, siteView: "plan", scrollPhoto: false, workbench: null, recordId: null };
export function archaeologyForPlace(entryId:string,placeId:string|null):ExplorerState {
 return {...initialExplorer,entryId,placeId,mode:"site",planId:plansForPlace(placeId)[0]?.id??null,featureId:null};
}
export function explorerHash(s: ExplorerState) {
 if (s.workbench) return `#workbench/${s.workbench}?entry=${s.entryId}`;
 const base=s.mode === "site" && s.planId?`#entry-${s.entryId}/site/${s.planId}${s.featureId ? `/${s.featureId}` : ""}${s.siteView === "photo" ? "/photo" : s.representation ? "/"+s.representation : ""}`:entryHash(s.entryId,s.mode)+(s.mode==='scroll'&&s.scrollPhoto?'/photo':s.mode==='scroll'&&s.scroll3d?'/3d':'');
 const params=new URLSearchParams();
 if(s.explicitPlace&&s.placeId&&(["2d","3d","landscape","dossier","ground","scroll"].includes(s.mode)||s.inspection))params.set('place',s.placeId);
 if(s.inspection){params.set('inspect',s.inspection);if(s.recordId)params.set('record',s.recordId);}
 return base+(params.size?'?'+params.toString():'');
}
export function explorerFromHash(hash: string, primaryPlace: (id: string) => string | null): ExplorerState | null {
 // Evidence links retain the chosen locality even when it has no source plan
 // or mapped coordinate. Reject unknown/repeated parameters and arbitrary IDs.
 if(hash.includes("?")&&!hash.startsWith("#workbench")){
  const parts=hash.split("?");if(parts.length!==2)return null;
  const params=new URLSearchParams(parts[1]);
  const keys=[...params.keys()],placeId=params.get("place"),inspection=params.get('inspect'),record=params.get('record');
  if(!keys.length||new Set(keys).size!==keys.length||keys.some(key=>!['place','inspect','record'].includes(key)))return null;
  if(params.has('place')&&(!placeId||!atlasData.places.some(place=>place.id===placeId)))return null;
  if(params.has('inspect')&&!isInspectionView(inspection))return null;
  if(params.has('record')&&(!inspection||!record))return null;
  const parsed=explorerFromHash(parts[0],primaryPlace);
  if(!parsed)return null;
  if(!inspection&&!["2d","3d","landscape","dossier","ground","scroll"].includes(parsed.mode))return null;
  if(placeId&&parsed.mode==='site'&&!sitePlans.find(plan=>plan.id===parsed.planId)?.placeIds.includes(placeId))return null;
  return {...parsed,...(placeId?{placeId,explicitPlace:true,planId:parsed.mode==='site'?parsed.planId:plansForPlace(placeId)[0]?.id??null}:{}),inspection:isInspectionView(inspection)?inspection:null,recordId:record};
 }
 const overview=hash.match(/^#entry-((?:[1-9]|[1-5]\d|60|12a))\/site$/);
 if(overview)return archaeologyForPlace(overview[1],primaryPlace(overview[1]));
 const site = hash.match(/^#entry-([\da-z]+)\/site\/([\w-]+)(?:\/([\w-]+))?(?:\/(photo|source|model|walk))?$/);
 if (site) {
  const [,entryId, planId, part, explicitView] = site;
  const views=["photo","source","model","walk"];if(explicitView&&views.includes(part))return null;
  const selectedView=explicitView??(views.includes(part)?part:undefined);
  if (!/^(?:[1-9]|[1-5]\d|60|12a)$/.test(entryId)) return null;
  const plan = sitePlans.find(p => p.id === planId); if (!plan) return null;
  const featureId = views.includes(part) ? null : part ?? null;
  if (featureId && !plan.features.some(f => f.id === featureId)) return null;
  return { ...initialExplorer, entryId, placeId: plan.placeIds[0], mode: "site", planId, featureId, siteView: selectedView === "photo" ? "photo" : "plan", representation: selectedView === "source" ? "source" : selectedView === "model" ? "model" : selectedView === "walk" ? "walk" : undefined };
 }
 const parsed = parseAtlasHash(hash); if (!parsed) return null;
 const id = parsed.entryId ?? initialExplorer.entryId;
 if(/^#entry-(?:[1-9]|[1-5]\d|60|12a)$/.test(hash))return archaeologyForPlace(id,primaryPlace(id));
 return { ...initialExplorer, entryId: id, placeId: primaryPlace(id), planId:null, mode: parsed.mode ?? initialExplorer.mode, workbench: parsed.workbench, scrollPhoto: /\/scroll\/photo$/.test(hash) || hash === "#scroll/photo", scroll3d: /\/scroll\/3d$/.test(hash) || hash === "#scroll/3d" };
}
