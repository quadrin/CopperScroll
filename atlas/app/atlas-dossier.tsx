"use client";

import { useState } from "react";
import { BookOpen, Camera, ExternalLink, FileImage, Layers, MapPin } from "lucide-react";
import type { Entry, Place } from "./atlas-types";
import { dossierSources, placeDossiers, type PlaceDossier } from "./atlas-dossiers-data";
import scenes from "./atlas-scenes.json";
import evidence from "./atlas-evidence.json";
import Interpretations, { ArgumentSources } from "./atlas-interpretations";
import "./atlas-dossiers.css";

export type AtlasDossierProps = { entry: Entry; place: Place | null; onEntry?: (id: string) => void; onLandscape?: () => void; onRead?: () => void };
type Tab = "place" | "interpretations" | "sources";
const assetBase = import.meta.env?.BASE_URL ?? "/";
const royalPoolFigures = [
  { id: "20", label: "Early Pools Complex", file: "trumper2018-fig20-p284.jpg", kind: "Published reconstruction", title: "Phase 3 · reconstructed Pools Complex", locator: "Trümper 2018 Fig. 20, p. 284", credit: "Netzer 2001b, p. 93 plan 17", alt: "Published reconstructed phase-3 plan of the Jericho Pools Complex showing two distinct basins, masonry labels, levels, scale and north arrow pointing right. Original figure caption retained.", note: "The early paired basins have a different longer-side axis from the joined phase. Dashed or reconstructed geometry cannot supply a missing observed inlet or ancient wall-face datum." },
  { id: "22", label: "Later Pools Complex", file: "trumper2018-fig22-p286.jpg", kind: "Published reconstruction", title: "Phase 6 · reconstructed Pools Complex", locator: "Trümper 2018 Fig. 22, p. 286", credit: "Netzer 2001b, p. 7 plan 20 (as printed; possible pagination error retained)", alt: "Published reconstructed phase-6 plan of the Jericho Pools Complex showing a large joined basin and surrounding structures, with scale and north arrow pointing right. Original figure caption retained.", note: "This is a later reconstructed state. A depicted line or the joined basin’s outline does not establish the required contemporaneous conduit contact, collector or floor." },
  { id: "19", label: "Separate Area AC", file: "trumper2018-fig19-p282.jpg", kind: "Published state plan", title: "Area AC · separate water installations", locator: "Trümper 2018 Fig. 19, p. 282", credit: "M. Trümper after Netzer 2001a, plan 13", alt: "Published Area AC state plan labeling pools A(C)90, A(C)94 and AC44 and the Na’aran and Wadi Qelt aqueducts; supply is coloured blue and drainage red. Scale, north arrow and original caption retained.", note: "A(C)94 and its pipe belong to this separate complex. Its inlet, levels and phases cannot be substituted for those of the northern Pools Complex basin." },
];

function RoyalPoolGallery() {
  const [figureId, setFigureId] = useState("20");
  const figure = royalPoolFigures.find(item => item.id === figureId)!;
  return <section className="ds-published-gallery" aria-label="Licensed Jericho plan comparison"><div className="ds-plan-switch" role="group" aria-label="Published Jericho figures">{royalPoolFigures.map(item => <button key={item.id} aria-pressed={figureId === item.id} onClick={() => setFigureId(item.id)}>{item.label}</button>)}</div><figure aria-live="polite"><header><div><span className="ds-source-kind">{figure.kind}</span><h4>{figure.title}</h4></div><a href={`${assetBase}dossiers/${figure.file}`} target="_blank" rel="noreferrer">Open full figure <ExternalLink size={12} aria-hidden="true" /></a></header><img src={`${assetBase}dossiers/${figure.file}`} alt={figure.alt} loading="lazy" /><figcaption><strong>{figure.locator}</strong><p>{figure.note}</p><span>Monika Trümper (2018) · figure credit: {figure.credit}. <a href="https://creativecommons.org/licenses/by-nc/3.0/" target="_blank" rel="noreferrer">CC BY-NC 3.0</a>. Existing figure/caption crop reproduced without further alteration; original orientation retained.</span></figcaption></figure></section>;
}

function ConfidenceAxes({ entry, place, comparison }: { entry: Entry; place: Place | null; comparison: boolean }) {
  const review = evidence.entries.find(item => item.entryId === entry.id && item.placeId === place?.id);
  const candidate = entry.candidates.find(item => item.placeId === place?.id);
  const axes = comparison ? [
    { label: "Reading", value: "Branch-dependent" }, { label: "Site association", value: "Comparison only" }, { label: "Exact feature", value: "Unresolved" }, { label: "Position", value: "Not assigned" },
  ] : [
    { label: "Reading", value: review?.reading ?? "Edition-based" }, { label: "Site association", value: review?.site ?? candidate?.confidence ?? "Unassigned" }, { label: "Exact feature", value: review?.feature ?? "Unresolved" }, { label: "Position", value: place?.precision ?? "Not assigned" },
  ];
  return <section className="ds-confidence" aria-label="Separate assessment axes">{axes.map(axis => <div key={axis.label}><span>{axis.label}</span><strong>{axis.value}</strong></div>)}</section>;
}

function SourceGallery({ dossier }: { dossier?: PlaceDossier }) {
  const records = dossier?.sourceIds.map(id => dossierSources.find(item => item.id === id)).filter(item => !!item) ?? [];
  return <section className="ds-source-gallery"><div className="ds-section-title"><FileImage size={17} aria-hidden="true" /><h3>Plans, photographs and source records</h3></div>
    <p>Exact page and figure references stay attached to each record. The source links distinguish observed plans, published reconstructions and project comparisons.</p>
    {dossier?.id === "jericho_palaces" && <RoyalPoolGallery />}
    {records.length ? <div className="ds-source-grid">{records.map(source => <article key={source.id}><span className={`ds-source-kind ds-kind-${source.kind}`}>{source.kind ?? "Source"}</span><h4>{source.title}</h4><p className="ds-source-locator">{source.locator}</p><p>{source.note}</p><a href={source.url} target="_blank" rel="noreferrer">Open source record <ExternalLink size={13} aria-hidden="true" /></a></article>)}</div> : <p className="ds-limit">This locality has not yet received a curated plan-and-figure gallery. The entry’s register references remain available below.</p>}
  </section>;
}

function DossierBody({ entry, place, onEntry, onLandscape, onRead }: AtlasDossierProps) {
  const [tab, setTab] = useState<Tab>("place");
  const [comparisonId, setComparisonId] = useState<string | null>(null);
  const baseDossier = placeDossiers.find(item => item.id === place?.id || (place?.id === "wadi_qumran" && item.id === "kh_qumran"));
  const dossier = comparisonId ? placeDossiers.find(item => item.id === comparisonId) : baseDossier;
  const comparison = !!comparisonId && comparisonId !== place?.id;
  const scene = !comparison ? scenes.find(item => item.placeId === dossier?.id) : undefined;
  const tabs: { id: Tab; label: string }[] = [{ id: "place", label: "Place & features" }, { id: "interpretations", label: "Interpretations" }, { id: "sources", label: "Source gallery" }];
  return <div className="dossier-surface">
    <header className="ds-heading"><div><span className="small-caps"><MapPin size={13} aria-hidden="true" />Place dossier</span><h2>{dossier?.name ?? place?.shortName ?? "Location unresolved"}</h2><p>{dossier?.subtitle ?? place?.name ?? "Read the entry’s requirements before choosing a locality."}</p></div><div className="ds-heading-actions">
      {onLandscape && !comparison && <button className="ds-action" onClick={onLandscape}><Layers size={15} />Landscape through time</button>}
      {onRead && <button className="ds-action" onClick={onRead}><BookOpen size={15} />Read entry {entry.id}</button>}
    </div></header>
    <ConfidenceAxes entry={entry} place={place} comparison={comparison} />
    <p className="ds-position-note">{comparison ? "This is a source-backed comparison dossier. It has no atlas coordinate or identification grade assigned." : `${place?.precision ? `Map anchor precision: ${place.precision}. ` : ""}Locality precision does not locate a building corner, entrance or deposit.`}</p>
    {(baseDossier?.comparisonIds?.length || comparison) && <div className="ds-comparison-switch" aria-label="Alternative locality dossiers"><span>Compare locality</span><button aria-pressed={!comparison} onClick={() => setComparisonId(null)}>{baseDossier?.name ?? place?.shortName}</button>{baseDossier?.comparisonIds?.map(id => <button key={id} aria-pressed={comparisonId === id} onClick={() => setComparisonId(id)}>{placeDossiers.find(item => item.id === id)?.name}</button>)}</div>}
    <nav className="ds-tabs" aria-label="Dossier sections">{tabs.map(item => <button key={item.id} aria-current={tab === item.id ? "page" : undefined} onClick={() => setTab(item.id)}>{item.label}</button>)}</nav>
    {tab === "place" && <div className="ds-place-body">
      <section className="ds-introduction"><p>{dossier?.summary ?? place?.note ?? entry.evidence}</p>{scene && <figure className="ds-context-photo"><div><img src={scene.src} alt={scene.alt} loading="lazy" /><span><Camera size={13} aria-hidden="true" />Modern landscape context</span></div><figcaption>{scene.caption}<span>Photo: <a href={scene.sourceUrl} target="_blank" rel="noreferrer">{scene.author}</a> · <a href={scene.licenseUrl} target="_blank" rel="noreferrer">{scene.license}</a>. Atlas framing crops the source image.</span></figcaption></figure>}</section>
      {dossier ? <>
        <section className="ds-feature-section"><div className="ds-section-title"><h3>Which physical feature?</h3></div><div className="ds-features">{dossier.features.map((feature, index) => <article key={feature.name} className={`ds-feature ds-feature-${feature.kind.toLowerCase().replaceAll(" ", "-")}`}><header><span className="ds-feature-number">{String(index + 1).padStart(2, "0")}</span><div><span className="ds-feature-kind">{feature.kind}</span><h4>{feature.name}</h4></div></header><p>{feature.observation}</p><p className="ds-feature-limit"><strong>Limit:</strong> {feature.limit}</p><ArgumentSources ids={feature.sourceIds} /></article>)}</div></section>
        <section className="ds-phases"><h3>Archaeological and documented phases</h3><ol>{dossier.phases.map(phase => <li key={phase.label}><h4>{phase.label}</h4><p>{phase.detail}</p><ArgumentSources ids={phase.sourceIds} /></li>)}</ol></section>
        <section className="ds-open-summary"><span className="small-caps">Current limit</span><p>{dossier.unresolved}</p><button onClick={() => setTab("interpretations")}>Inspect the reading → feature argument</button></section>
        <section className="ds-linked-entries"><h3>Entries to compare here</h3><div>{dossier.entryIds.map(id => onEntry ? <button key={id} aria-current={entry.id === id ? "true" : undefined} onClick={() => onEntry(id)}>Entry {id}</button> : <a key={id} href={`#entry-${id}`}>Entry {id}</a>)}</div><p>These links retain locality proposals and feature comparisons; they do not imply a shared cache or confirmed route.</p></section>
      </> : <section className="ds-generic-place"><h3>Entry {entry.id} · {entry.title}</h3><dl><div><dt>Required feature</dt><dd>{entry.landmark || entry.description}</dd></div><div><dt>Published evidence</dt><dd>{entry.evidence}</dd></div><div><dt>Dating</dt><dd>{entry.period}</dd></div><div><dt>Open issue</dt><dd>{entry.caution}</dd></div></dl><button className="ds-action" onClick={() => setTab("interpretations")}>Inspect the entry’s argument</button></section>}
    </div>}
    {tab === "interpretations" && <Interpretations entry={entry} place={comparison ? null : place} onRead={onRead} />}
    {tab === "sources" && <><SourceGallery dossier={dossier} /><section className="ds-register-sources"><h3>Entry register references</h3><p>{entry.sources}</p>{place && !comparison && <p><strong>Map-anchor source:</strong> {place.source}</p>}</section></>}
  </div>;
}

export default function AtlasDossier(props: AtlasDossierProps) {
  return <DossierBody key={`${props.entry.id}-${props.place?.id ?? "unplaced"}`} {...props} />;
}
