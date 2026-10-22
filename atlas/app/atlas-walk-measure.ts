// An exploratory measuring tool at eye level: two points picked on what is drawn (the smooth model, the
// block build or the terrain), with the horizontal distance, the height difference and the slope distance
// between them. It measures the display model, not the ground, and it is not a test: frozen tests fix their
// readings, cubit lengths and tolerances before looking at evidence (AGENTS.md, "Tests that can fail").
export const MEASURE_LABEL='Exploratory measurement on the display model — not a test';
export const MEASURE_LIMIT='Frozen tests fix their readings, cubit lengths and tolerances before looking at evidence; this tool cannot confirm an identification.';

// Cubit lengths the project already uses, with where it states them. No other values are offered.
export type Cubit={metres:number;name:string;source:string};
export const CUBITS:Cubit[]=[
 {metres:.4,name:'lower end of the exploratory range',source:'0.40–0.60 m per cubit, an exploratory sensitivity range (research/sites/entry25_cave_access_review_2026-10-01.md; research/assessments/entry29_jericho_pools/README.md)'},
 {metres:.445,name:'short cubit',source:'Lower end of the 0.445–0.525 m sensitivity range (research/sites/hyrcania_plan_registration_2026-09-30.md); "short" in research/schematics/searches/search_04_depths.py'},
 {metres:.5,name:'project working value',source:'"Project working value" in research/schematics/searches/search_04_depths.py; the middle of the 0.40–0.60 m exploratory range'},
 {metres:.525,name:'royal cubit',source:'Upper end of the 0.445–0.525 m sensitivity range (research/sites/hyrcania_plan_registration_2026-09-30.md); "royal" in research/schematics/searches/search_04_depths.py'},
 {metres:.6,name:'upper end of the exploratory range',source:'0.40–0.60 m per cubit, an exploratory sensitivity range (research/sites/entry25_cave_access_review_2026-10-01.md; research/assessments/entry29_jericho_pools/README.md)'},
];
// The default is the middle of the project's 0.40–0.60 m range, which is also its stated working value.
export const DEFAULT_CUBIT=.5;

export type MeasurePoint=[number,number,number];
export function measureBetween(a:MeasurePoint,b:MeasurePoint){
 const horizontal=Math.hypot(b[0]-a[0],b[2]-a[2]),rise=b[1]-a[1];
 return {horizontal,rise,slope:Math.hypot(horizontal,rise)};
}
