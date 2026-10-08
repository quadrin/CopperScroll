"use client";
import { useState } from "react";
import { ArrowLeft, Download, ExternalLink, FlaskConical } from "lucide-react";
import snapshot from "./atlas-workbench.json";
import "./atlas-workbench.css";
type Status = "compatible" | "contradicted" | "unknown" | "mixed" | "info";
type Source = {
    id: string;
    title: string;
    citation: string;
    repo_path: string;
    url?: string;
    inspection: string;
    original_campaign?: unknown;
};
type Feature = {
    id: string;
    name: string;
    kind: string;
    site: string;
    geometry: unknown;
};
type Check = {
    id: string;
    label: string;
    status: Status;
    detail: string;
    value?: unknown;
    source_ids: string[];
    feature_ids?: string[];
};
type Result = {
    id: string;
    title: string;
    claim: string;
    status: Status;
    checks: Check[];
    unknowns: string[];
    source_ids: string[];
    feature_ids: string[];
};
type Observation = {
    id: string;
    feature_id: string;
    property: string;
    value: unknown;
    evidence_kind: string;
    source_ids: string[];
    exposure: string;
    phase?: unknown;
    reference_frame?: unknown;
    uncertainty?: unknown;
};
type State = {
    id: string;
    feature_id: string;
    label: string;
    status: string;
    source_ids: string[];
    phase?: unknown;
    geometry?: unknown;
    reference_frame?: unknown;
    uncertainty?: unknown;
    note?: string;
};
type Module = {
    id: string;
    number: number;
    title: string;
    summary: string;
    scope: string;
    results: Result[];
    data: Record<string, unknown>;
    observation_ids: string[];
    state_ids: string[];
    source_ids: string[];
};
type Workbench = {
    reviewed: string;
    method: string;
    modules: Module[];
    register: {
        features: Feature[];
        sources: Source[];
        observations: Observation[];
        states: State[];
    };
};
const workbench = snapshot as unknown as Workbench;
const sources = Object.fromEntries(workbench.register.sources.map(source => [source.id, source]));
const features = Object.fromEntries(workbench.register.features.map(feature => [feature.id, feature]));
const repo = "https://github.com/quadrin/CopperScroll/blob/main/";
const labels: Record<Status, string> = { compatible: "Compatible", contradicted: "Contradicted", unknown: "Unknown", mixed: "Mixed branches", info: "Context" };
const shortTitles: Record<string, string> = { relationships: "Relationships", inventory: "Inventory", states: "Historical states", coverage: "Coverage", decisions: "Next observations" };
function readable(value: unknown): string {
    if (value === null || value === undefined)
        return "Unknown";
    if (typeof value === "boolean")
        return value ? "Yes" : "No";
    if (typeof value !== "object")
        return String(value).replaceAll("_", " ");
    if (Array.isArray(value))
        return value.map(readable).join(" · ");
    return Object.entries(value).map(([key, item]) => `${key.replaceAll("_", " ")}: ${readable(item)}`).join("; ");
}
function StatusMark({ status }: {
    status: Status;
}) { return <span className={`wb-status wb-${status}`}>{labels[status] ?? readable(status)}</span>; }
function SourceLinks({ ids }: {
    ids: string[];
}) {
    return <span className="wb-source-links">{Array.from(new Set(ids)).map(id => { const source = sources[id]; return source ? <a key={id} href={`${repo}${source.repo_path}`} target="_blank" rel="noreferrer" title={`${source.title} · ${source.citation} · ${readable(source.inspection)}`}>{source.citation}<ExternalLink size={11}/></a> : null; })}</span>;
}
function Pick({ label, value, onChange, options }: {
    label: string;
    value: string;
    onChange: (id: string) => void;
    options: {
        id: string;
        label?: string;
        title?: string;
    }[];
}) {
    return <label className="wb-pick"><span>{label}</span><select value={value} onChange={event => onChange(event.target.value)}>{options.map(option => <option key={option.id} value={option.id}>{option.label ?? option.title ?? option.id}</option>)}</select></label>;
}
function Checks({ checks }: {
    checks: Check[];
}) {
    return <div className="wb-checks">{checks.map(check => <section key={check.id}><div><h4>{check.label}</h4><StatusMark status={check.status}/></div><p>{check.detail}</p><SourceLinks ids={check.source_ids}/></section>)}</div>;
}
function ResultCard({ result }: {
    result: Result;
}) {
    return <article className="wb-result"><div className="wb-result-title"><h3>{result.title}</h3><StatusMark status={result.status}/></div><p>{result.claim}</p><Checks checks={result.checks}/>{result.unknowns.length > 0 && <div className="wb-unknowns"><strong>Still needed</strong><ul>{result.unknowns.map((unknown, index) => <li key={index}>{unknown}</li>)}</ul></div>}</article>;
}
type RelationshipsData = {
    readings: {
        id: string;
        label: string;
        summary: string;
    }[];
    windows: {
        id: string;
        label: string;
    }[];
    assignments: {
        id: string;
        label: string;
        roles: Record<string, string | null>;
        reading_ids: string[];
    }[];
    branches: {
        id: string;
        label: string;
        reading_id: string;
        window_id: string;
        assignment_id: string;
        result_id: string;
    }[];
};
function Relationships({ module }: {
    module: Module;
}) {
    const data = module.data as unknown as RelationshipsData;
    const [reading, setReading] = useState(data.readings[0].id), [window, setWindow] = useState(data.windows[0].id), [assignment, setAssignment] = useState(data.assignments[0].id);
    const branch = data.branches.find(branch => branch.reading_id === reading && branch.window_id === window && branch.assignment_id === assignment);
    const result = module.results.find(result => result.id === branch?.result_id);
    const selected = data.assignments.find(item => item.id === assignment)!;
    const readingOptions = data.readings.filter(item => selected.reading_ids.includes(item.id));
    function chooseAssignment(id: string) {
        const allowed = data.assignments.find(item => item.id === id)!.reading_ids;
        setAssignment(id);
        if (!allowed.includes(reading)) setReading(allowed[0]);
    }
    return <><div className="wb-controls"><Pick label="Feature assignment" value={assignment} onChange={chooseAssignment} options={data.assignments}/><Pick label="Text branch" value={reading} onChange={setReading} options={readingOptions}/><Pick label="Period window (exploratory)" value={window} onChange={setWindow} options={data.windows}/></div><p className="wb-note">{data.readings.find(item => item.id === reading)?.summary}</p><div className="wb-role-grid" aria-label="Proposed feature assignments">{Object.entries(selected.roles).map(([role, id]) => <div key={role}><span>{readable(role)}</span><strong>{id ? features[id]?.name ?? readable(id) : "Feature unresolved"}</strong></div>)}</div>{result ? <ResultCard result={result}/> : <p>No branch has been evaluated for this combination.</p>}<p className="wb-note">All retained combinations are available in the reviewed data. A branch contradiction applies to its stated relation and assignment.</p></>;
}
type InventoryData = {
    catalog: {
        id: string;
        name: string;
        properties: Record<string, {
            value: unknown;
            unit?: string;
            phase?: unknown;
            reference_frame?: unknown;
            uncertainty?: unknown;
            note?: string;
            evidence_kind?: string;
            source_ids: string[];
        }>;
    }[];
    dimensions: {
        id: string;
        label: string;
        options: {
            id: string;
            label: string;
        }[];
    }[];
    queries: {
        id: string;
        title: string;
        claim: string;
        branch_dimensions: string[];
        branches: {
            id: string;
            choices: Record<string, string>;
            depth_metres?: unknown;
        }[];
        candidate_results: {
            candidate_id: string;
            status: Status;
            branches: {
                branch_id: string;
                status: Status;
                checks: Check[];
            }[];
        }[];
    }[];
};
function Inventory({ module }: {
    module: Module;
}) {
    const data = module.data as unknown as InventoryData;
    const [queryId, setQueryId] = useState(data.queries[0].id), [choices, setChoices] = useState<Record<string, string>>({});
    const query = data.queries.find(query => query.id === queryId)!;
    const dimensions = data.dimensions.filter(dimension => query.branch_dimensions.includes(dimension.id));
    const activeChoices = Object.fromEntries(dimensions.map(dimension => [dimension.id, choices[dimension.id] ?? query.branches[0].choices[dimension.id]]));
    const branch = query.branches.find(branch => dimensions.every(dimension => branch.choices[dimension.id] === activeChoices[dimension.id])) ?? query.branches[0];
    return <><div className="wb-controls"><Pick label="Saved query" value={queryId} onChange={id => { setQueryId(id); setChoices({}); }} options={data.queries}/>{dimensions.map(dimension => <Pick key={dimension.id} label={dimension.label} value={activeChoices[dimension.id]} onChange={id => setChoices(current => ({ ...current, [dimension.id]: id }))} options={dimension.options}/>)}</div><p className="wb-note">{query.claim}</p>{branch.depth_metres !== undefined && <p className="wb-note">Exploratory digging conversion: {readable(branch.depth_metres)} m. Ancient origin and datum must be established separately.</p>}<div className="wb-candidate-grid" aria-live="polite">{query.candidate_results.map(candidate => { const item = data.catalog.find(item => item.id === candidate.candidate_id)!; const outcome = candidate.branches.find(outcome => outcome.branch_id === branch.id)!; return <article className="wb-result" key={candidate.candidate_id}><div className="wb-result-title"><h3>{item.name}</h3><StatusMark status={outcome.status}/></div><Checks checks={outcome.checks}/></article>; })}</div><details className="wb-details"><summary>Catalog properties and missing measurements</summary>{data.catalog.map(item => <section key={item.id}><h3>{item.name}</h3><dl className="wb-property-list">{Object.entries(item.properties).map(([key, property]) => <div key={key}><dt>{readable(key)}</dt><dd>{readable(property.value)}{property.unit && <> {property.unit === "deg" ? "degrees" : property.unit}</>}{property.evidence_kind && <p className="wb-meta">{readable(property.evidence_kind)}</p>}{property.phase !== undefined && <p className="wb-meta">Phase: {readable(property.phase)}</p>}{property.reference_frame !== undefined && <p className="wb-meta">Frame: {readable(property.reference_frame)}</p>}{property.uncertainty !== undefined && <p className="wb-meta">Uncertainty: {readable(property.uncertainty)}</p>}{property.note && <p className="wb-meta">{property.note}</p>}<SourceLinks ids={property.source_ids}/></dd></div>)}</dl></section>)}</details><p className="wb-note">Each control receives the same branch. This selected inventory has no established regional boundary or eligible denominator.</p></>;
}
type StatesData = {
    reference_frames: {
        id: string;
        label?: string;
        kind: string;
        size_px?: [
            number,
            number
        ];
        units?: string;
        scale?: {
            length: number;
            unit: string;
            endpoints_px: [
                number,
                number
            ][];
        };
        north?: {
            tail_px: [
                number,
                number
            ];
            tip_px: [
                number,
                number
            ];
            convention: string;
        };
    }[];
    views: {
        id: string;
        title: string;
        description: string;
        state_ids: string[];
        query_ids: string[];
        reference_frame: string;
        native_shapes: string[];
    }[];
    transitions: {
        id: string;
        from: string;
        to: string;
        relation: string;
        evidence_kind: string;
        note: string;
        source_ids: string[];
    }[];
    dependencies: Record<string, unknown>[];
    saved_queries: { id: string; required_access_phase?: string; window_basis?: string }[];
};
function NativePlan({ states, frame }: {
    states: State[];
    frame: StatesData["reference_frames"][number];
}) {
    const segments = states.filter(state => state.geometry != null).map(state => ({ state, shape: state.geometry as {
            type: string;
            points: [
                number,
                number
            ][];
        } }));
    if (!segments.length || !frame.size_px)
        return null;
    const points = segments.flatMap(segment => segment.shape.points);
    const scalePoints = frame.scale?.endpoints_px ?? [];
    const xs = [...points, ...scalePoints].map(point => point[0]), ys = [...points, ...scalePoints].map(point => point[1]);
    const x = Math.min(...xs) - 65, y = Math.min(...ys) - 42;
    const width = Math.max(...xs) - x + 40, height = Math.max(...ys) - y + 52;
    return <figure className="wb-native-plan"><svg viewBox={`${x} ${y} ${width} ${height}`} role="img" aria-label="IV/17 aperture chords in the original source-crop coordinates; no cave outline or geographic registration">
    {segments.map(({ state, shape }) => { const [a, b] = shape.points, cx = (a[0] + b[0]) / 2, cy = (a[1] + b[1]) / 2; return <g key={state.id}><line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} className="wb-aperture"/><circle cx={a[0]} cy={a[1]} r="3"/><circle cx={b[0]} cy={b[1]} r="3"/><text x={cx} y={cy - 19} textAnchor="middle">{state.feature_id === "iv17-north-mouth" ? "Northern opening" : "Southern remaining gap"}</text><text x={cx} y={cy + 30} textAnchor="middle" className="wb-coordinate">{readable(shape.points)} px</text></g>; })}
    {frame.scale && <g><line x1={scalePoints[0][0]} y1={scalePoints[0][1]} x2={scalePoints[1][0]} y2={scalePoints[1][1]} className="wb-scale"/><text x={(scalePoints[0][0] + scalePoints[1][0]) / 2} y={scalePoints[0][1] + 21} textAnchor="middle">Published scale · {frame.scale.length} {frame.scale.unit}</text></g>}
  </svg><figcaption>Project endpoint annotations in {frame.size_px.join(" × ")} source-crop pixels; origin at top left, y increases downward. {frame.north?.convention ?? "Source north unestablished"}. The crop's placement supplies no world coordinate, ancient mouth shape or traversal observation.</figcaption></figure>;
}
function HistoricalStates({ module }: {
    module: Module;
}) {
    const data = module.data as unknown as StatesData;
    const states = workbench.register.states.filter(state => module.state_ids.includes(state.id));
    const stateById = Object.fromEntries(states.map(state => [state.id, state]));
    const [viewId, setViewId] = useState(data.views[0].id), [featureId, setFeatureId] = useState("all");
    const view = data.views.find(view => view.id === viewId)!;
    const inView = states.filter(state => view.state_ids.includes(state.id));
    const featureIds = Array.from(new Set(inView.map(state => state.feature_id)));
    const selected = inView.filter(state => featureId === "all" || state.feature_id === featureId);
    const related = module.results.filter(result => view.query_ids.includes(result.id) && (featureId === "all" || result.feature_ids.includes(featureId)));
    const frame = data.reference_frames.find(frame => frame.id === view.reference_frame)!;
    const transitions = data.transitions.filter(transition => view.state_ids.includes(transition.from) && view.state_ids.includes(transition.to));
    return <><div className="wb-controls"><Pick label="Configuration" value={viewId} onChange={id => { setViewId(id); setFeatureId("all"); }} options={data.views}/><Pick label="Feature" value={featureId} onChange={setFeatureId} options={[{ id: "all", label: "All features in this configuration" }, ...featureIds.map(id => ({ id, label: features[id].name }))]}/></div>
    <p className="wb-note">{view.description}</p><NativePlan states={inView.filter(state => view.native_shapes.includes(state.id))} frame={frame}/>
    <div className="wb-state-grid">{selected.map(state => <article className={`wb-state wb-state-${state.status}`} key={state.id}><span className="small-caps">{readable(state.status)}</span><h3>{state.label}</h3>{state.note && <p>{state.note}</p>}<dl><dt>Phase</dt><dd>{readable(state.phase)}</dd><dt>Reference frame</dt><dd>{state.reference_frame ? data.reference_frames.find(frame => frame.id === state.reference_frame)?.label ?? readable(state.reference_frame) : "Unknown"}</dd><dt>Uncertainty</dt><dd>{readable(state.uncertainty)}</dd></dl>{state.geometry !== null && state.geometry !== undefined && <details><summary>Native geometry</summary><p>{readable(state.geometry)}</p></details>}<SourceLinks ids={state.source_ids}/></article>)}</div>
    {transitions.length > 0 && <details className="wb-details"><summary>Recorded relations and proposed transitions</summary>{transitions.map(transition => <section key={transition.id}><span className="small-caps">{readable(transition.evidence_kind)}</span><h4>{stateById[transition.from].label} → {readable(transition.relation)} → {stateById[transition.to].label}</h4><p>{transition.note}</p><SourceLinks ids={transition.source_ids}/></section>)}</details>}
    {related.map(result => { const query = data.saved_queries.find(query => query.id === result.id); return <div key={result.id}>{query?.window_basis && <p className="wb-note">{query.window_basis} Required access context: {query.required_access_phase}.</p>}<ResultCard result={result}/></div>; })}
    <details className="wb-details"><summary>Next records needed</summary>{data.dependencies.map((dependency, index) => <section key={index}><p>{readable(dependency)}</p></section>)}</details>
    <p className="wb-note">Native plan records and described sequences stay in their original frames. These pilots have no registered geographic overlay.</p></>;
}
type CoverageData = {
    sectors: {
        id: string;
        label?: string;
        name?: string;
        scope_limit?: string;
    }[];
    notices: {
        id: string;
        label: string;
        sector_id: string;
        record_kind: string;
        coverage_detail: unknown;
        flags: unknown;
        physical_identity: unknown;
        source_ids: string[];
    }[];
    targets: {
        id: string;
        label: string;
        feature_ids: string[];
        gates: {
            id: string;
            label: string;
            status: Status;
            detail: string;
            source_ids: string[];
        }[];
        missing_gate_ids: string[];
        negative_deposit_status: string;
    }[];
    obligations: { id: string; label: string; detail: string; next_observation: string; source_ids: string[] }[];
};
function Coverage({ module }: {
    module: Module;
}) {
    const data = module.data as unknown as CoverageData;
    const [targetId, setTargetId] = useState(data.targets[0].id), [sector, setSector] = useState("all");
    const target = data.targets.find(target => target.id === targetId)!;
    const notices = data.notices.filter(notice => sector === "all" || notice.sector_id === sector);
    return <><div className="wb-controls"><Pick label="Target coverage" value={targetId} onChange={setTargetId} options={data.targets}/></div><article className="wb-result"><h3>{target.label}</h3><p className="wb-note">Negative-deposit inference: {readable(target.negative_deposit_status)}</p><Checks checks={target.gates}/></article><details className="wb-details"><summary>Jericho documentary coverage · {data.notices.length} source notices</summary><div className="wb-controls"><Pick label="Documentary sector" value={sector} onChange={setSector} options={[{ id: "all", label: "All sectors" }, ...data.sectors.map(item => ({ id: item.id, label: item.label ?? item.name ?? item.id }))]}/></div>{sector !== "all" && <p className="wb-note">{data.sectors.find(item => item.id === sector)?.scope_limit}</p>}<div className="wb-notice-list">{notices.map(notice => <article key={notice.id}><span className="small-caps">{notice.id} · {readable(notice.record_kind)}</span><h4>{notice.label}</h4><p>{readable(notice.coverage_detail)}</p><p>Physical identity: {readable(notice.physical_identity)}</p><p>Preservation and coverage flags: {readable(notice.flags)}</p><SourceLinks ids={notice.source_ids}/></article>)}</div></details><details className="wb-details"><summary>Unresolved coverage obligations · {data.obligations.length} records</summary>{data.obligations.map(obligation => <section key={obligation.id}><h4>{obligation.label}</h4><p>{obligation.detail}</p><p>Next observation: {obligation.next_observation}</p><SourceLinks ids={obligation.source_ids}/></section>)}</details><p className="wb-note">Excavation coverage, disturbance and detection limits remain separate gates. Documentary notices do not provide a count of independent eligible pools or a geographic coverage percentage.</p></>;
}
type DecisionData = {
    tasks: {
        id: string;
        title: string;
        priority: string;
        priority_reason: string;
        claim: string;
        current_evidence: {
            status: string;
            detail: string;
        };
        request: {
            status: string;
            scope: string;
            delivery: unknown;
            reply: unknown;
        };
        record_needed: string[];
        access: {
            status: string;
            route: unknown;
            detail: string;
        };
        effort: {
            level: string;
            detail: string;
        };
        next_action: string;
        freeze: {
            status: string;
            commit?: string;
            unused_status: string;
            detail: string;
        };
        outcomes: {
            id: string;
            label: string;
            status: string;
            condition: string;
            consequences: string[];
            remaining_unknowns: string[];
            claim_scope: string;
            recorded: false;
        }[];
        source_ids: string[];
    }[];
    historical_queue: {
        tracks: {
            id: string;
            target: string;
            execution_state: string;
            next_action: string;
        }[];
    };
};
function Decisions({ module }: {
    module: Module;
}) {
    const data = module.data as unknown as DecisionData;
    const [taskId, setTaskId] = useState(data.tasks[0].id), [outcomeId, setOutcomeId] = useState("");
    const task = data.tasks.find(task => task.id === taskId)!;
    const outcome = task.outcomes.find(outcome => outcome.id === outcomeId);
    return <><div className="wb-controls"><Pick label="Next observation" value={taskId} onChange={id => { setTaskId(id); setOutcomeId(""); }} options={data.tasks}/></div><article className="wb-result"><div className="wb-result-title"><h3>{task.title}</h3><span className="wb-status wb-info">{readable(task.priority)} priority</span></div><p>{task.claim}</p><p className="wb-note">{task.priority_reason}</p><dl className="wb-property-list"><div><dt>Current evidence</dt><dd>{task.current_evidence.detail}</dd></div><div><dt>Recorded request</dt><dd>{readable(task.request.status)} · {task.request.scope}<br />Delivery: {readable(task.request.delivery)}; reply: {readable(task.request.reply)}</dd></div><div><dt>Access and effort</dt><dd>{readable(task.access.status)} · {task.access.detail}<br />{readable(task.effort.level)}: {task.effort.detail}</dd></div><div><dt>Freeze and unused evidence</dt><dd>{task.freeze.detail} · {readable(task.freeze.unused_status)}{task.freeze.commit && <><br /><a href={`https://github.com/quadrin/CopperScroll/commit/${task.freeze.commit}`} target="_blank" rel="noreferrer">Recorded freeze<ExternalLink size={11}/></a></>}</dd></div></dl><h4>Exact record needed</h4><ul>{task.record_needed.map((record, index) => <li key={index}>{record}</li>)}</ul><p><strong>Next action:</strong> {task.next_action}</p><SourceLinks ids={task.source_ids}/><div className="wb-hypothetical"><Pick label="Explore a possible outcome" value={outcomeId} onChange={setOutcomeId} options={[{ id: "", label: "Choose a hypothetical outcome…" }, ...task.outcomes]}/>{outcome && <div aria-live="polite"><span className="small-caps">Hypothetical · no result recorded</span><h4>{outcome.condition}</h4><ul>{outcome.consequences.map((consequence, index) => <li key={index}>{consequence}</li>)}</ul><p>Claim scope: {outcome.claim_scope}</p>{outcome.remaining_unknowns.length > 0 && <><strong>Still unresolved</strong><ul>{outcome.remaining_unknowns.map((unknown, index) => <li key={index}>{unknown}</li>)}</ul></>}</div>}</div></article><details className="wb-details"><summary>Historical measurement tracks · preserved source statuses</summary>{data.historical_queue.tracks.map(track => <section key={track.id}><h3>{track.id} · {track.target}</h3><p>{readable(track.execution_state)}</p><p>{track.next_action}</p></section>)}</details></>;
}
function FeatureRegister({ module }: {
    module: Module;
}) {
    const observations = workbench.register.observations.filter(observation => module.observation_ids.includes(observation.id));
    const featureIds = Array.from(new Set([...observations.map(observation => observation.feature_id), ...module.results.flatMap(result => result.feature_ids)]));
    const [featureId, setFeatureId] = useState(featureIds[0] ?? "iv17-cave");
    return <details className="wb-details wb-register"><summary>Shared feature register · observation provenance</summary><div className="wb-controls"><Pick label="Registered feature" value={featureId} onChange={setFeatureId} options={featureIds.map(id => ({ id, label: features[id].name }))}/></div><p className="wb-note">Showing this module’s observations. Each observation retains its evidence kind, source and exposure.</p>{observations.filter(observation => observation.feature_id === featureId).map(observation => <article key={observation.id}><span className="small-caps">{readable(observation.evidence_kind)} · {readable(observation.exposure)}</span><h4>{readable(observation.property)}</h4><p>{readable(observation.value)}</p>{observation.phase !== undefined && <p>Phase: {readable(observation.phase)}</p>}{observation.reference_frame !== undefined && <p>Frame: {readable(observation.reference_frame)}</p>}{observation.uncertainty !== undefined && <p>Uncertainty: {readable(observation.uncertainty)}</p>}<SourceLinks ids={observation.source_ids}/></article>)}</details>;
}
function downloadData() {
    const url = URL.createObjectURL(new Blob([JSON.stringify(snapshot, null, 2)], { type: "application/json" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "copper-scroll-feature-workbench.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export default function AtlasWorkbench({ moduleId, onModule, onClose }: {
    moduleId: string;
    onModule: (id: string) => void;
    onClose: () => void;
}) {
    const module = workbench.modules.find(module => module.id === moduleId) ?? workbench.modules[0];
    return <section id="research-workbench" tabIndex={-1} className="workbench-surface" aria-label="Copper Scroll research tools"><div className="wb-heading"><div><span className="small-caps"><FlaskConical size={14}/> Feature workbench · {workbench.reviewed}</span><h2>Test features, preserve unknowns</h2><p>Compare the same constraints across candidates and see which observation could resolve the next question.</p></div><div className="wb-actions"><button onClick={downloadData}><Download size={14}/>Reviewed data</button><button onClick={onClose}><ArrowLeft size={14}/>Back to atlas</button></div></div><nav className="wb-tabs" aria-label="Research methods">{workbench.modules.map(item => <button key={item.id} aria-current={item.id === module.id ? "page" : undefined} onClick={() => onModule(item.id)}><span>{item.number}</span>{shortTitles[item.id]}</button>)}</nav><div className="wb-body" key={module.id}><header className="wb-module-heading"><h2>{module.title}</h2><p>{module.summary}</p><details><summary>Pilot scope and evidence limits</summary><p>{module.scope}</p><p>{workbench.method}</p></details></header>{module.id === "relationships" && <Relationships module={module}/>}{module.id === "inventory" && <Inventory module={module}/>}{module.id === "states" && <HistoricalStates module={module}/>}{module.id === "coverage" && <Coverage module={module}/>}{module.id === "decisions" && <Decisions module={module}/>}<FeatureRegister module={module}/><details className="wb-details"><summary>Source inspection and original campaigns</summary>{module.source_ids.map(id => { const source = sources[id]; return <section key={id}><h4>{source.title}</h4><p>{source.citation} · {readable(source.inspection)}</p>{source.original_campaign != null && <p>Original campaign: {readable(source.original_campaign)}</p>}<a href={`${repo}${source.repo_path}`} target="_blank" rel="noreferrer">Reviewed evidence record<ExternalLink size={12}/></a>{source.url && <a href={source.url} target="_blank" rel="noreferrer">Source route<ExternalLink size={12}/></a>}</section>; })}</details></div></section>;
}
