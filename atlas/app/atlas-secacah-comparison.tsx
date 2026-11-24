"use client";

import { useState } from "react";
import results from "./atlas-secacah-comparison.json";

type Branch = keyof typeof results;
const branches: Record<Branch, { label: string; detail: string }> = {
  "S-open|F-flow": {
    label: "The conduit receives its supply from the north",
    detail: "The recorded whole-system approach is northern at Naʿaran and western at Qumran. This reading tests the head and flow direction. It leaves the marker unspecified.",
  },
  "S-stone|N-side": {
    label: "A stone marks the north side at the head",
    detail: "Both aqueducts have a recorded head. Neither record places a stone on its north side. Qumran’s intake on the northern bank describes the bank of the wadi.",
  },
  "S-pool|N-side": {
    label: "A pool marks the north side at the head",
    detail: "The recorded Qumran pool fails the north-side condition in the system inventory. The corresponding pool and side at Naʿaran remain unknown. Other proposed local head positions require their own feature checks.",
  },
};
const labels: Record<string, string> = { MATCH: "Fits", FAIL: "Conflicts", UNKNOWN: "Unknown" };
const source = "https://github.com/quadrin/CopperScroll/blob/main/research/regional/water_systems/manual_review_2026-10-12/verified_merged_scores.csv";

export function SecacahComparison() {
  const [branch, setBranch] = useState<Branch>("S-open|F-flow");
  return <section className="kb-compare" aria-label="Entry 21 conduit comparison">
    <h3>The conduit head at Secacah</h3>
    <div className="kb-compare-controls">
      <label>Which relation does “north” describe?
        <select value={branch} onChange={event => setBranch(event.target.value as Branch)}>
          {(Object.keys(branches) as Branch[]).map(key => <option value={key} key={key}>{branches[key].label}</option>)}
        </select>
      </label>
    </div>
    <div aria-live="polite">
      {results[branch].map(row => <div className="kb-plain-check" key={row.site}>
        <strong>{row.site}</strong><span>{labels[row.result]}</span>
      </div>)}
      <p>{branches[branch].detail}</p>
    </div>
    <p className="kb-muted">These results compare two water systems under the selected reading. The site of Secacah, the precise marker, and its date remain open.</p>
    <a className="kb-inline-link" href={source} target="_blank" rel="noreferrer">Water-system tests and recorded clauses</a>
  </section>;
}
