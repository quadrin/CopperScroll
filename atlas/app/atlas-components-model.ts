import components from "./atlas-components.json";
import type { Candidate, Entry } from "./atlas-types";

/** Evidence components (research/assessments/evidence_components/RUBRIC.md): reading, place, feature, date, uniqueness. */
type Level = 0 | 1 | 2 | 3;
export type ComponentRow = {
  levels: Record<"R" | "P" | "F" | "D", Level>;
  basis: Record<"R" | "P" | "F" | "D" | "U", string>;
  u: string; weakest: Level; label: string; limitedBy: string[]; limitingWord: string; next: string;
};
const rows = components.rows as Record<string, ComponentRow>;
export const names = { R: "Reading", P: "Place", F: "Feature", D: "Date" } as const;
export const keys = ["R", "P", "F", "D"] as const;
export const componentLinks = { rubric: components.rubric, table: components.table };

export function componentsFor(entryId: string, placeId: string | null | undefined): ComponentRow | null {
  return placeId ? rows[`${entryId}|${placeId}`] ?? null : null;
}

/** The candidate whose weakest link is highest; ties keep atlas order. */
export function strongestCandidate(entry: Entry): { placeId: string; row: ComponentRow } | null {
  let best: { placeId: string; row: ComponentRow } | null = null;
  for (const c of entry.candidates) {
    const row = componentsFor(entry.id, c.placeId);
    if (row && (!best || row.weakest > best.row.weakest)) best = { placeId: c.placeId, row };
  }
  return best;
}

/** Sort key: weakest link first, then the sum of the four levels. */
export function evidenceScore(entry: Entry): number {
  const best = strongestCandidate(entry);
  if (!best) return -1;
  const sum = keys.reduce((s, k) => s + best.row.levels[k], 0);
  return best.row.weakest * 100 + sum;
}

/** Candidate sort key within an entry. */
export function candidateScore(entryId: string, c: Candidate): number {
  const row = componentsFor(entryId, c.placeId);
  return row ? row.weakest * 100 + keys.reduce((s, k) => s + row.levels[k], 0) : -1;
}
