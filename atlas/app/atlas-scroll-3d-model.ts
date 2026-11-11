// Geometry and frame bookkeeping for the 3D scroll object. No imports, so the
// node test can transpile and run this file on its own.

export const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];

/** Sheet height. About 30 cm (Facsimile Editions' description of the scroll). */
export const SHEET_HEIGHT_M = 0.3;
/** Overall length used when no strip is measured. About 2.4 m (same source). */
export const SHEET_LENGTH_M = 2.4;
export const SEGMENT_COUNT = 23;

/**
 * Segments that carry each column, I to XII, from the radiograph captions of
 * Brizemeure, Lacoudre and Puech 2006, plates CCCXXXIII–CCCLVI (I–X also in
 * research/text/letter_controls/controls_manifest.csv; XI = 19–20 and
 * XII = 21–23 read from the plates on 2026-11-11).
 */
export const COLUMN_SEGMENTS: [number, number][] = [[1, 4], [5, 6], [7, 8], [9, 10], [10, 11], [11, 12], [13, 14], [15, 15], [16, 17], [17, 18], [19, 20], [21, 23]];


export type StripBox = { segment: number; u0: number; u1: number; measured: boolean; columns: number[] };
/** One strip of the registered model: lengths in metres, and the tangent angle (radians) of its cross-section at equal steps along the surface. */
export type StripFit = { arc: number; chord: number; height: number; measured: boolean; tangent: number[] };
export type ColumnBox = { index: number; u0: number; u1: number };
export type ScrollLayout = { length: number; strips: StripBox[]; columns: ColumnBox[] };

/**
 * Lay the sheet out along u (metres from the start of column I; the text runs
 * right to left, so u grows to the left). `widths` gives strip widths in
 * metres by segment, measured on photographs; the other strips get their mean.
 * All widths are then scaled together so the sheet keeps its ~2.4 m length:
 * the photographs show curved strips, so their widths are short.
 * With `absolute`, the widths are lengths along the surface (the registered
 * model) and are used as they are.
 */
export function layoutScroll(widths: Record<number, number> = {}, absolute = false): ScrollLayout {
  const measured = Object.entries(widths).filter(([s, w]) => +s >= 1 && +s <= SEGMENT_COUNT && w > 0);
  const measuredSum = measured.reduce((t, [, w]) => t + w, 0);
  const unmeasured = SEGMENT_COUNT - measured.length;
  const mean = measured.length ? measuredSum / measured.length : SHEET_LENGTH_M / SEGMENT_COUNT;
  const scale = absolute ? 1 : SHEET_LENGTH_M / (measuredSum + unmeasured * mean);
  const fill = mean * scale;
  let u = 0;
  const strips: StripBox[] = [];
  for (let s = 1; s <= SEGMENT_COUNT; s++) {
    const w = widths[s] > 0 ? widths[s] * scale : fill;
    strips.push({ segment: s, u0: u, u1: u + w, measured: widths[s] > 0, columns: COLUMN_SEGMENTS.flatMap(([a, b], i) => (s >= a && s <= b ? [i] : [])) });
    u += w;
  }
  // A segment shared by two columns is split at its middle.
  const columns = COLUMN_SEGMENTS.map(([a, b], index) => {
    const first = strips[a - 1], last = strips[b - 1];
    const sharedStart = index > 0 && COLUMN_SEGMENTS[index - 1][1] === a;
    const sharedEnd = index < COLUMN_SEGMENTS.length - 1 && COLUMN_SEGMENTS[index + 1][0] === b;
    return { index, u0: sharedStart ? (first.u0 + first.u1) / 2 : first.u0, u1: sharedEnd ? (last.u0 + last.u1) / 2 : last.u1 };
  });
  return { length: u, strips, columns };
}

export function columnAt(layout: ScrollLayout, u: number) {
  const hit = layout.columns.find(c => u >= c.u0 && u < c.u1);
  return hit ? hit.index : u < 0 ? 0 : layout.columns.length - 1;
}

/**
 * Position of sheet point u in the horizontal plane, as [x, z].
 * `unroll` 0 = fully rolled, 1 = flat. The flat part lies on z = 0 with the
 * inscribed face towards +z; the rest stays in an Archimedean roll on the +z
 * side, whose core is the end of column XII, with the inscribed face inside.
 */
export function sheetPoint(u: number, unroll: number, length: number, core = 0.014, pitch = 0.0075): [number, number] {
  const up = Math.max(0, Math.min(1, unroll)) * length;
  if (u <= up) return [length / 2 - u, 0];
  const b = pitch / (2 * Math.PI);
  const theta = (s: number) => (-core + Math.sqrt(core * core + 2 * b * s)) / b;
  const point = (t: number): [number, number] => { const r = core + b * t; return [r * Math.cos(t), -r * Math.sin(t)]; };
  const S = length - up, tS = theta(S), t = theta(length - u);
  const r = core + b * tS;
  // Tangent in the direction of growing s (towards the flat part).
  const tx = b * Math.cos(tS) - r * Math.sin(tS), tz = -b * Math.sin(tS) - r * Math.cos(tS);
  const phi = -Math.atan2(tz, tx), c = Math.cos(phi), sn = Math.sin(phi);
  const [px, pz] = point(t), [ox, oz] = point(tS);
  const dx = px - ox, dz = pz - oz;
  // Mirror the roll to +z, so it curls towards the inscribed face and keeps it inside.
  return [length / 2 - up + (c * dx - sn * dz), -(sn * dx + c * dz)];
}

/**
 * Cross-section of a curved strip, as [x, z] for n + 1 points from its right
 * edge (start of the line) to its left edge. `tangent` is sampled from the left
 * edge to the right edge of the photograph. `amount` 0 = flat, 1 = as measured.
 * The chord is laid on z = 0 and the middle of the strip stands back from it,
 * so the inscribed face is the hollow side, towards +z.
 */
export function stripProfile(tangent: number[], width: number, n: number, amount: number): [number, number][] {
  const m = tangent.length - 1, ds = width / n, px = [0], pz = [0];
  const at = (f: number) => { const t = Math.max(0, Math.min(m, f * m)), i = Math.min(m - 1, Math.floor(t)); return (tangent[i] + (tangent[i + 1] - tangent[i]) * (t - i)) * amount; };
  for (let i = 0; i < n; i++) { const a = at((i + .5) / n); px.push(px[i] + ds * Math.cos(a)); pz.push(pz[i] + ds * Math.sin(a)); }
  const turn = -Math.atan2(pz[n] - pz[0], px[n] - px[0]), c = Math.cos(turn), s = Math.sin(turn);
  const pts = px.map((x, i) => [x * c - pz[i] * s, x * s + pz[i] * c] as [number, number]);
  const mid = (pts[0][0] + pts[n][0]) / 2, edge = Math.max(pts[0][1], pts[n][1]);
  // Left-to-right order becomes right-to-left, the order of the strip's vertices.
  return pts.map(([x, z]) => [x - mid, z - edge] as [number, number]).reverse();
}

/** Light codes in the WSRP 1988 file names. Meanings are inferred; WSRP has not confirmed them. */
export const LIGHT_NAMES: Record<string, string> = {
  RLT: "left top light", RCT: "centre top light", RRT: "right top light",
  RLB: "left bottom light", RCB: "centre bottom light", RRB: "right bottom light",
  RT: "top light", RB: "bottom light", RET: "edge top light", REB: "edge bottom light",
  RCS: "centre side light", RBC: "bottom centre light", RTC: "top centre light",
  FRS: "fragments", RFR: "fragments",
  // Layers of the registered model, all on one grid for each strip.
  MT: "top light (three frames blended)", MB: "bottom light (three frames blended)", MR: "relief (top against bottom light)",
  MN: "b&w negative, 1988", MF: "EDF facsimile", MA: "Allegro, 1955–56", MM: "Milik's hand copy on the relief", MX: "EDF radiograph",
};

export type FrameName = { ok: true; segment: number; light: string; key: string } | { ok: false; reason: "unrecognised" };

/** Read the segment and light from a name like DSS_3Q15_CT4_RB_T_q4.jpg. */
export function parseFrameName(name: string): FrameName {
  const m = name.match(/(?:^|[^A-Za-z0-9])CT[ _-]?0*(\d{1,2})[ _-]+([A-Z]{2,3})(?=[^A-Za-z]|$)/i);
  if (!m) return { ok: false, reason: "unrecognised" };
  const segment = +m[1];
  if (segment < 1 || segment > SEGMENT_COUNT) return { ok: false, reason: "unrecognised" };
  const light = m[2].toUpperCase();
  return { ok: true, segment, light, key: `CT${segment}_${light}` };
}

/** Light preference when a strip has several frames. */
export const LIGHT_ORDER = ["MT", "MB", "MR", "MN", "MF", "MA", "MM", "MX", "RCT", "RT", "RCB", "RB", "RLT", "RRT", "RLB", "RRB", "RET", "REB", "RTC", "RBC", "RCS", "FRS", "RFR"];
export function pickFrame<T extends { light: string }>(frames: T[], wanted: string | null) {
  if (!frames.length) return null;
  if (wanted) { const hit = frames.find(f => f.light === wanted); if (hit) return hit; }
  for (const light of LIGHT_ORDER) { const hit = frames.find(f => f.light === light); if (hit) return hit; }
  return frames[0];
}
