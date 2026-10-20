// Traced plans: published figures turned into metric geometry (research/models/traced_plans).
// Built by scripts/build-traced-plans.mjs into atlas-traced-plans.json; read by buildModel.
export type TracedPoint = [number, number];
export type TracedGeometry =
 | { type: "polyline"; points: TracedPoint[]; closed?: boolean; width?: number }
 | { type: "polygon"; points: TracedPoint[] }
 | { type: "point"; points?: undefined; at: TracedPoint; radius?: number }
 | { type: "raster"; cell: number; origin: TracedPoint; cols: number; rows: number; rle: string | number[] };
export type TracedElement = {
 id: string; label?: string; kind: string; layers: string[]; status: "observed" | "published-reconstruction" | "project-inference";
 lineStyle?: string; geometry: TracedGeometry;
 levels?: { top?: number | null; bottom?: number | null; floor?: number | null; rim?: number | null };
 height?: { value: number | null; basis: string }; steps?: { count?: number | null; down?: "n" | "s" | "e" | "w" };
 source?: string; locator?: string; note?: string;
};
export type TracedPlan = {
 id: string; title: string;
 frame: { origin: string; north: string; datum: string | null; ground: number | null };
 sources: { id: string; citation: string }[];
 layers: { id: string; label: string; kind: "observed" | "published-reconstruction" }[];
 elements: TracedElement[];
 features?: { id: string; at: TracedPoint }[];
 walkStart?: { at: TracedPoint; bearing: number };
  focus?: TracedPoint;
};

export function decodeRaster(g: Extract<TracedGeometry, { type: "raster" }>) {
 const runs = typeof g.rle === "string" ? g.rle.split(/[\s,]+/).filter(Boolean).map(Number) : g.rle, mask = new Uint8Array(g.cols * g.rows);
 let at = 0, on = 0;
 for (const run of runs) { if (on) mask.fill(1, at, at + run); at += run; on ^= 1; }
 if (at !== mask.length) throw Error(`Raster runs cover ${at} cells, expected ${mask.length}`);
 return mask;
}
// Maximal rectangles of set cells (row-major greedy), as [col, row, width, height].
export function rasterRectangles(mask: Uint8Array, cols: number, rows: number) {
 const seen = new Uint8Array(mask.length), out: [number, number, number, number][] = [];
 for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
  const n = r * cols + c; if (!mask[n] || seen[n]) continue;
  let w = 1; while (c + w < cols && mask[n + w] && !seen[n + w]) w++;
  let h = 1; grow: while (r + h < rows) { for (let k = 0; k < w; k++) { const m = (r + h) * cols + c + k; if (!mask[m] || seen[m]) break grow; } h++; }
  for (let y = r; y < r + h; y++) seen.fill(1, y * cols + c, y * cols + c + w);
  out.push([c, r, w, h]);
 }
 return out;
}
export function elementPoints(e: TracedElement): TracedPoint[] {
 const g = e.geometry;
 if (g.type === "raster") return [g.origin, [g.origin[0] + g.cols * g.cell, g.origin[1] + g.rows * g.cell]];
 if (g.type === "point") return [g.at];
 return g.points;
}
