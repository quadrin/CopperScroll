import type { Candidate, Entry, Place } from "./atlas-types";
import { candidateScore, evidenceScore } from "./atlas-components-model";

export type SortOrder = "scroll" | "confidence" | "ancient" | "candidate" | "region";
export const sortLabels: Record<SortOrder, string> = {
  scroll: "Scroll order", confidence: "Evidence · weakest link highest first", ancient: "Ancient name · A–Z", candidate: "Candidate name · A–Z", region: "Region · A–Z",
};
const statusRank: Record<string, number> = { preferred: 2, possible: 1, weak: 0 };
const regionNames: Record<string,string> = {jericho:"Jericho & Qumran",jerusalem:"Jerusalem",region:"Judean hills & north",unplaced:"Unplaced"};
const compare = (a: string, b: string) => a.localeCompare(b, "en", { numeric: true, sensitivity: "base" });
export function sortEntries(entries: Entry[], order: SortOrder, places: Record<string, Place>) {
  return [...entries].sort((a, b) => {
    let result = 0;
    if (order === "confidence") result = evidenceScore(b) - evidenceScore(a);
    if (order === "ancient") result = compare(a.title, b.title);
    if (order === "candidate") result = compare(a.candidates[0] ? places[a.candidates[0].placeId].shortName : "\uffff", b.candidates[0] ? places[b.candidates[0].placeId].shortName : "\uffff");
    if (order === "region") result = compare(regionNames[a.region]??a.region, regionNames[b.region]??b.region);
    return result || compare(a.id, b.id);
  });
}
export function sortCandidates(candidates: Candidate[], order: string, places: Record<string, Place>, entryId = "") {
  return [...candidates].sort((a, b) => {
    if (order === "alphabetical") return compare(places[a.placeId].shortName, places[b.placeId].shortName);
    if (order === "confidence") return candidateScore(entryId, b) - candidateScore(entryId, a) || (statusRank[b.status] ?? 0) - (statusRank[a.status] ?? 0);
    return (statusRank[b.status] ?? 0) - (statusRank[a.status] ?? 0);
  });
}
