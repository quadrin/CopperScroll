"use client";

import { ExternalLink } from "lucide-react";
import { componentLinks, componentsFor, keys, names, strongestCandidate, type ComponentRow } from "./atlas-components-model";
import type { Entry } from "./atlas-types";
import "./atlas-components.css";

export { componentsFor, strongestCandidate } from "./atlas-components-model";
type Level = ComponentRow["weakest"];

function Pips({ level }: { level: Level }) {
  return <span className="ec-pips" aria-hidden="true">{[1, 2, 3].map(i => <i key={i} className={i <= level ? "on" : ""} />)}</span>;
}

/** Compact strip for candidate lists: R2 P1 F2 D2 · weak (P). */
export function EvidenceChips({ entryId, placeId }: { entryId: string; placeId: string }) {
  const row = componentsFor(entryId, placeId);
  if (!row) return <small className="ec-missing">Not rated</small>;
  const limit = row.limitedBy.map(k => names[k as keyof typeof names]).join(", ");
  return <span className={`ec-strip ec-${row.label}`} aria-label={`Evidence: ${keys.map(k => `${names[k]} ${row.levels[k]} of 3`).join(", ")}. Weakest link ${row.label}, set by ${limit}. Uniqueness ${row.u}.`}>
    {keys.map(k => <span key={k} className={`ec-chip ${row.limitedBy.includes(k) ? "limit" : ""}`} title={`${names[k]} ${row.levels[k]}/3: ${row.basis[k]}`}><b>{k}</b><Pips level={row.levels[k]} /></span>)}
    <span className="ec-label">{row.label}</span>
  </span>;
}

/** Short label for the scroll register: the weakest link of the strongest candidate. */
export function EvidenceLabel({ entry }: { entry: Entry }) {
  const best = strongestCandidate(entry);
  if (!best) return <span className="register-confidence unplaced">unplaced</span>;
  return <span className={`register-confidence ec-${best.row.label}`} title={`Weakest link: ${best.row.limitedBy.map(k => names[k as keyof typeof names]).join(", ")}`}>{best.row.label}</span>;
}

/** Full breakdown with the basis for each component. */
export function EvidenceComponents({ entryId, placeId }: { entryId: string; placeId: string | null | undefined }) {
  const row = componentsFor(entryId, placeId);
  if (!row) return <p className="unreviewed-note">This candidate has no evidence-component rating.</p>;
  return <section className="ec-panel" aria-label="Evidence components">
    <header><span className="small-caps">Evidence components</span><strong className={`ec-label ec-${row.label}`}>Weakest link: {row.label}</strong></header>
    <dl>
      {keys.map(k => <div key={k} className={row.limitedBy.includes(k) ? "limit" : ""}><dt>{names[k]}<span>{row.levels[k]}/3<Pips level={row.levels[k]} /></span></dt><dd>{row.basis[k]}{k === "R" && row.limitingWord && <em> Limiting word: <span lang="he">{row.limitingWord}</span>.</em>}</dd></div>)}
      <div><dt>Uniqueness<span>{row.u}</span></dt><dd>{row.basis.U}</dd></div>
    </dl>
    {row.next && <p className="ec-next"><strong>Would change it:</strong> {row.next}</p>}
    <p className="ec-method">Each part is rated 0–3 from the repository's records; the weakest part sets the label. None counts as an identification without all four at 3 and a test against controls. <a href={componentLinks.rubric} target="_blank" rel="noreferrer">Rubric<ExternalLink size={12} aria-hidden="true" /></a> · <a href={componentLinks.table} target="_blank" rel="noreferrer">All ratings<ExternalLink size={12} aria-hidden="true" /></a></p>
  </section>;
}
