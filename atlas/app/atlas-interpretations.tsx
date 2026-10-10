"use client";

import { useState } from "react";
import { ArrowDown, BookOpen, ExternalLink, GitBranch } from "lucide-react";
import type { Entry, Place } from "./atlas-types";
import { dossierSources, entryArguments } from "./atlas-dossiers-data";
import snapshot from "./atlas-workbench.json";
import "./atlas-dossiers.css";

type Status = "compatible" | "contradicted" | "unknown" | "mixed" | "info";
type SavedSource = { id: string; title: string; citation: string; repo_path: string; inspection: string; url?: string };
type Check = { id: string; label: string; status: Status; detail: string; source_ids: string[] };
type SavedResult = { id: string; title: string; status: Status; checks: Check[]; unknowns: string[] };
type Relationships = {
  readings: { id: string; label: string; summary: string }[];
  windows: { id: string; label: string }[];
  assignments: { id: string; label: string; reading_ids: string[]; roles: Record<string, string | null> }[];
  branches: { reading_id: string; window_id: string; assignment_id: string; result_id: string }[];
};
type Inventory = {
  catalog: { id: string; name: string }[];
  dimensions: { id: string; label: string; note?: string; options: { id: string; label: string }[] }[];
  queries: { id: string; title: string; claim: string; branch_dimensions: string[]; branches: { id: string; choices: Record<string, string>; depth_metres?: number }[]; candidate_results: { candidate_id: string; branches: { branch_id: string; status: Status; checks: Check[] }[] }[] }[];
};
const savedSources = snapshot.register.sources as SavedSource[];
const sourceById = Object.fromEntries(dossierSources.map(source => [source.id, source]));
const repo = "https://github.com/quadrin/CopperScroll/blob/main/";
const statusLabels: Record<Status, string> = { compatible: "Compatible relation", contradicted: "Contradicted branch", unknown: "Unresolved", mixed: "Mixed branches", info: "Context" };

export function ArgumentSources({ ids }: { ids: string[] }) {
  return <div className="ds-source-links">{Array.from(new Set(ids)).map(id => {
    const source = sourceById[id];
    if (source) return <a key={id} href={source.url} target="_blank" rel="noreferrer" title={source.note}>{source.title}<span>{source.locator}</span><ExternalLink size={12} aria-hidden="true" /></a>;
    const saved = savedSources.find(item => item.id === id);
    return saved ? <a key={id} href={`${repo}${saved.repo_path}`} target="_blank" rel="noreferrer" title={`${saved.title} · ${saved.inspection}`}>{saved.title}<span>{saved.citation}</span><ExternalLink size={12} aria-hidden="true" /></a> : null;
  })}</div>;
}

function CheckList({ checks }: { checks: Check[] }) {
  return <div className="ds-checks">{checks.map(check => <section key={check.id}>
    <div><h4>{check.label}</h4><span className={`ds-outcome ds-${check.status}`}>{statusLabels[check.status]}</span></div>
    <p>{check.detail === "Reviewed value True; query equals True." && check.label === "Two exterior openings" ? "The reviewed publication reports two exterior openings." : check.detail}</p><ArgumentSources ids={check.source_ids} />
  </section>)}</div>;
}

function SelectChoice({ label, value, onChange, options }: { label: string; value: string; onChange: (value: string) => void; options: { id: string; label: string }[] }) {
  return <label className="ds-choice"><span>{label}</span><select value={value} onChange={event => onChange(event.target.value)}>{options.map(option => <option value={option.id} key={option.id}>{option.label}</option>)}</select></label>;
}

function RelationshipComparison({ reading, onReading, preferredAssignment }: { reading?: string; onReading?: (id: string) => void; preferredAssignment?: string }) {
  const reviewedModule = snapshot.modules.find(item => item.id === "relationships")!;
  const data = reviewedModule.data as unknown as Relationships;
  const initialAssignment = data.assignments.find(item => item.id === preferredAssignment && (!reading || item.reading_ids.includes(reading))) ?? data.assignments.find(item => !reading || item.reading_ids.includes(reading)) ?? data.assignments[0];
  const [assignmentId, setAssignmentId] = useState(initialAssignment.id);
  const [localReadingId, setLocalReadingId] = useState(reading ?? initialAssignment.reading_ids[0]);
  const readingId = reading ?? localReadingId;
  const [windowId, setWindowId] = useState(data.windows[0].id);
  const assignment = data.assignments.find(item => item.id === assignmentId && item.reading_ids.includes(readingId)) ?? data.assignments.find(item => item.reading_ids.includes(readingId))!;
  const selectedBranch = data.branches.find(branch => branch.assignment_id === assignment.id && branch.reading_id === readingId && branch.window_id === windowId);
  const result = (reviewedModule.results as SavedResult[]).find(item => item.id === selectedBranch?.result_id);
  const features = Object.fromEntries(snapshot.register.features.map(feature => [feature.id, feature.name]));
  function chooseAssignment(id: string) {
    const next = data.assignments.find(item => item.id === id)!;
    setAssignmentId(id);
    if (!next.reading_ids.includes(readingId)) chooseReading(next.reading_ids[0]);
  }
  function chooseReading(id: string) { setLocalReadingId(id); onReading?.(id); }
  return <section className="ds-saved-comparison" aria-label="Saved Koḥlit relationship comparisons">
    <div className="ds-section-title"><GitBranch size={17} aria-hidden="true" /><h3>Test a complete feature assignment</h3></div>
    <p>These saved comparisons apply the same requirements to the retained features. A compatible relation alone does not identify a place.</p>
    <div className="ds-controls">
      <SelectChoice label="Feature assignment" value={assignment.id} onChange={chooseAssignment} options={data.assignments} />
      <SelectChoice label="Text branch" value={readingId} onChange={chooseReading} options={data.readings.filter(reading => assignment.reading_ids.includes(reading.id))} />
      <SelectChoice label="Exploratory use window" value={windowId} onChange={setWindowId} options={data.windows} />
    </div>
    <p className="ds-selected-reading">{data.readings.find(reading => reading.id === readingId)?.summary}</p>
    <dl className="ds-role-list">{Object.entries(assignment.roles).map(([role, id]) => <div key={role}><dt>{role}</dt><dd>{id ? features[id] ?? id : "Feature unassigned"}</dd></div>)}</dl>
    {result ? <div className="ds-saved-result" aria-live="polite"><header><h4>{result.title}</h4><span className={`ds-outcome ds-${result.status}`}>{statusLabels[result.status]}</span></header><CheckList checks={result.checks} /></div> : <p>This combination has no saved evaluation.</p>}
    <p className="ds-limit">The period windows are exploratory project choices. Unknown dates, mouth relations and coverage remain unknown; a conditional exclusion applies only to its selected assignment.</p>
  </section>;
}

function CaveComparison({ reading, onReading }: { reading: string; onReading: (id: string) => void }) {
  const reviewedModule = snapshot.modules.find(item => item.id === "inventory")!;
  const data = reviewedModule.data as unknown as Inventory;
  const [queryId, setQueryId] = useState(data.queries[0].id);
  const [choices, setChoices] = useState<Record<string, string>>({});
  const query = data.queries.find(item => item.id === queryId)!;
  const dimensions = data.dimensions.filter(item => query.branch_dimensions.includes(item.id));
  const activeChoices = Object.fromEntries(dimensions.map(dimension => [dimension.id, dimension.id === "reading" ? reading : choices[dimension.id] ?? query.branches[0].choices[dimension.id]]));
  const branch = query.branches.find(item => dimensions.every(dimension => item.choices[dimension.id] === activeChoices[dimension.id]));
  return <section className="ds-saved-comparison" aria-label="Saved cave feature comparisons">
    <div className="ds-section-title"><GitBranch size={17} aria-hidden="true" /><h3>Give each cave the same requirements</h3></div>
    <div className="ds-controls"><SelectChoice label="Comparison" value={queryId} onChange={id => { setQueryId(id); setChoices({}); }} options={data.queries.map(item => ({ id: item.id, label: item.title }))} />
      {dimensions.map(dimension => <SelectChoice key={dimension.id} label={dimension.label} value={activeChoices[dimension.id]} onChange={id => { if (dimension.id === "reading") onReading(id); else setChoices(current => ({ ...current, [dimension.id]: id })); }} options={dimension.options} />)}
    </div>
    <p>{query.claim}</p>
    {branch?.depth_metres !== undefined && <p className="ds-selected-reading">Selected exploratory conversion: {branch.depth_metres.toFixed(2)} m. This supplies no missing threshold elevation or horizontal path.</p>}
    {branch ? <div className="ds-cave-comparisons" aria-live="polite">{query.candidate_results.map(candidate => {
      const result = candidate.branches.find(item => item.branch_id === branch.id);
      if (!result) return null;
      return <details key={candidate.candidate_id} className="ds-cave-result"><summary><strong>{data.catalog.find(item => item.id === candidate.candidate_id)?.name}</strong><span className={`ds-outcome ds-${result.status}`}>{statusLabels[result.status]}</span></summary><CheckList checks={result.checks} /></details>;
    })}</div> : <p>This combination has no saved evaluation.</p>}
    <details className="ds-assumptions"><summary>What these choices mean</summary>{dimensions.filter(dimension => dimension.note).map(dimension => <p key={dimension.id}><strong>{dimension.label}:</strong> {dimension.note}</p>)}</details>
    <p className="ds-limit">The selected cave catalogue has no established regional denominator. Form compatibility does not establish an ancient threshold, architectural date or deposit location.</p>
  </section>;
}

function InterpretationBody({ entry, place, onRead }: { entry: Entry; place: Place | null; onRead?: () => void }) {
  const argument = entryArguments.find(item => item.entryId === entry.id);
  const [branchId, setBranchId] = useState(argument?.branches[0].id ?? "");
  const branch = argument?.branches.find(item => item.id === branchId) ?? argument?.branches[0];
  if (!argument || !branch) return <section className="ds-argument-generic">
    <span className="small-caps">Entry {entry.id} · {entry.lines}</span><h3>{entry.title}</h3><p>{entry.description}</p>
    <dl className="ds-argument-chain"><div><dt>Required landmark</dt><dd>{entry.landmark || "The register does not identify a particular feature."}</dd></div><div><dt>Published setting</dt><dd>{entry.evidence}</dd></div><div><dt>Dating</dt><dd>{entry.period}</dd></div><div><dt>Open issue</dt><dd>{entry.caution}</dd></div></dl>
    <p className="ds-limit">{place ? `${place.shortName} is the selected locality proposal.` : "No locality is selected."} A branch-by-branch source assessment has not yet been curated for this entry.</p>
    <a className="ds-inline-action" href={`${repo}text/readings.json`} target="_blank" rel="noreferrer">Open the edition-reading register <ExternalLink size={13} /></a>
  </section>;
  return <div className="ds-interpretation">
    <header className="ds-argument-heading"><div><span className="small-caps">Entry {entry.id} · {entry.lines}</span><h3>{entry.title}</h3><p>{argument.summary}</p></div>{onRead && <button className="ds-action" onClick={onRead}><BookOpen size={15} />Read this entry</button>}</header>
    <div className="ds-branch-buttons" role="group" aria-label="Retained reading branches">{argument.branches.map(item => <button key={item.id} onClick={() => setBranchId(item.id)} aria-pressed={branch.id === item.id}>{item.label}</button>)}</div>
    <article className="ds-argument-card" aria-live="polite">
      <div className="ds-argument-attribution"><span>{branch.attribution}</span><span className="ds-outcome ds-unknown">Identification unresolved</span></div>
      <dl className="ds-argument-chain">
        <div><dt><span>01</span>Reading</dt><dd>{branch.reading}</dd></div>
        <div><dt><span>02</span>Required feature</dt><dd><ul>{branch.requirements.map(requirement => <li key={requirement}>{requirement}</li>)}</ul></dd></div>
        <div><dt><span>03</span>Phase and relation</dt><dd>{branch.chronology}</dd></div>
        <div><dt><span>04</span>Reviewed evidence</dt><dd>{branch.evidence}</dd></div>
        <div className="ds-open-issue"><dt><span>05</span>What would decide it</dt><dd>{branch.open}</dd></div>
      </dl>
      <ArgumentSources ids={branch.sourceIds} />
    </article>
    <div className="ds-branch-footnote"><ArrowDown size={14} aria-hidden="true" /><p>The argument keeps its reading, feature and phase together. Source availability and repeated publications add no identification confidence.</p></div>
    {entry.id === "11" && <RelationshipComparison key={branch.id} preferredAssignment={branch.id === "kohlit-marjama" ? "samiya-kallai" : "jericho-historical-ns1"} />}
    {entry.id === "60" && <RelationshipComparison reading={branch.id} onReading={setBranchId} />}
    {entry.id === "25" && <CaveComparison reading={branch.id} onReading={setBranchId} />}
  </div>;
}

export default function Interpretations(props: { entry: Entry; place: Place | null; onRead?: () => void }) {
  return <InterpretationBody key={`${props.entry.id}-${props.place?.id ?? "unplaced"}`} {...props} />;
}
