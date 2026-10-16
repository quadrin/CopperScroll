import planData from "./atlas-site-plans.json";
import { entryHash, parseAtlasHash } from "./atlas-navigation";
export type Camera = { center: [number, number]; zoom: number; bearing: number; pitch: number };
export type ModelCamera = { position: [number,number,number]; target: [number,number,number]; zoom: number; up?: [number,number,number]; projection?: "orthographic"|"perspective"; navigation?: "pan"|"orbit" };
export type Viewport = { x: number; y: number; zoom: number };
export type SiteFeature = { id: string; label: string; x: number; y: number; path?: string; kind: string; entryIds: string[]; description: string; limit: string; sources: string[]; sourceUrl: string };
export type SitePlan = { id: string; placeIds: string[]; label: string; kind?: "site-plan" | "survey-map"; width: number; height: number; transform?: string; image?: string; shapes?: { d: string; kind: string }[]; annotations?: { x: number; y: number; text: string }[]; north?: { x: number; y: number; dx: number; dy: number }; scale?: { x: number; y: number; length: number; label: string }; features: SiteFeature[]; source: string; sourceUrl?: string; credit: string; licenseUrl?: string; limit: string };
export const sitePlans = planData as SitePlan[];
export const plansForPlace = (id: string | null) => sitePlans.filter(p => id && p.placeIds.includes(id));
export type ExplorerState = {
 entryId: string; placeId: string | null; mode: string; planId: string | null; featureId: string | null;
 siteView: "plan" | "photo"; highlightId?: string | null; scrollPhoto: boolean; workbench: string | null; recordId: string | null;
 representation?: "model" | "source" | "walk"; modelCamera?: ModelCamera;
 camera?: Camera; viewport?: Viewport; photoViewport?: Viewport; scrollTop?: number; scrollColumn?: number;
};
export const initialExplorer: ExplorerState = { entryId: "21", placeId: "kh_qumran", mode: "site", planId: "qumran-ilan", featureId: null, siteView: "plan", scrollPhoto: false, workbench: null, recordId: null };
export function archaeologyForPlace(entryId:string,placeId:string|null):ExplorerState {
 return {...initialExplorer,entryId,placeId,mode:"site",planId:plansForPlace(placeId)[0]?.id??null,featureId:null};
}
export function explorerHash(s: ExplorerState) {
 if (s.workbench) return `#workbench/${s.workbench}?entry=${s.entryId}`;
 if (s.mode === "site" && s.planId) return `#entry-${s.entryId}/site/${s.planId}${s.featureId ? `/${s.featureId}` : ""}${s.siteView === "photo" ? "/photo" : s.representation ? "/"+s.representation : ""}`;
 return entryHash(s.entryId, s.mode) + (s.mode === "scroll" && s.scrollPhoto ? "/photo" : "");
}
export function explorerFromHash(hash: string, primaryPlace: (id: string) => string | null): ExplorerState | null {
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
 return { ...initialExplorer, entryId: id, placeId: primaryPlace(id), planId:null, mode: parsed.mode ?? initialExplorer.mode, workbench: parsed.workbench, scrollPhoto: /\/scroll\/photo$/.test(hash) || hash === "#scroll/photo" };
}
