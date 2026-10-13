import planData from "./atlas-site-plans.json";
import { entryHash, parseAtlasHash } from "./atlas-navigation";
export type Camera = { center: [number, number]; zoom: number; bearing: number; pitch: number };
export type Viewport = { x: number; y: number; zoom: number };
export type SiteFeature = { id: string; label: string; x: number; y: number; path?: string; kind: string; entryIds: string[]; description: string; limit: string; sources: string[]; sourceUrl: string };
export type SitePlan = { id: string; placeIds: string[]; label: string; width: number; height: number; transform?: string; image?: string; shapes?: { d: string; kind: string }[]; features: SiteFeature[]; source: string; credit: string; licenseUrl?: string; limit: string };
export const sitePlans = planData as SitePlan[];
export const plansForPlace = (id: string | null) => sitePlans.filter(p => id && p.placeIds.includes(id));
export type ExplorerState = {
 entryId: string; placeId: string | null; mode: string; planId: string | null; featureId: string | null;
 siteView: "plan" | "photo"; highlightId?: string | null; scrollPhoto: boolean; workbench: string | null; recordId: string | null;
 camera?: Camera; viewport?: Viewport; photoViewport?: Viewport; scrollTop?: number; scrollColumn?: number;
};
export const initialExplorer: ExplorerState = { entryId: "21", placeId: "kh_qumran", mode: "3d", planId: null, featureId: null, siteView: "plan", scrollPhoto: false, workbench: null, recordId: null };
export function explorerHash(s: ExplorerState) {
 if (s.workbench) return `#workbench/${s.workbench}`;
 if (s.mode === "site" && s.planId) return `#entry-${s.entryId}/site/${s.planId}${s.featureId ? `/${s.featureId}` : ""}${s.siteView === "photo" ? "/photo" : ""}`;
 return entryHash(s.entryId, s.mode) + (s.mode === "scroll" && s.scrollPhoto ? "/photo" : "");
}
export function explorerFromHash(hash: string, primaryPlace: (id: string) => string | null): ExplorerState | null {
 const site = hash.match(/^#entry-([\da-z]+)\/site\/([\w-]+)(?:\/([\w-]+))?(?:\/(photo))?$/);
 if (site) {
  const [,entryId, planId, part, photo] = site;
  if (!/^(?:[1-9]|[1-5]\d|60|12a)$/.test(entryId)) return null;
  const plan = sitePlans.find(p => p.id === planId); if (!plan) return null;
  const featureId = part === "photo" ? null : part ?? null;
  if (featureId && !plan.features.some(f => f.id === featureId)) return null;
  return { ...initialExplorer, entryId, placeId: plan.placeIds[0], mode: "site", planId, featureId, siteView: photo || part === "photo" ? "photo" : "plan" };
 }
 const parsed = parseAtlasHash(hash); if (!parsed) return null;
 const id = parsed.entryId ?? initialExplorer.entryId;
 return { ...initialExplorer, entryId: id, placeId: primaryPlace(id), mode: parsed.mode ?? initialExplorer.mode, workbench: parsed.workbench, scrollPhoto: /\/scroll\/photo$/.test(hash) || hash === "#scroll/photo" };
}
