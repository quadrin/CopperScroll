"use client";
import { dossierSources, entryArguments } from "./atlas-dossiers-data";
import gallery from "./atlas-site-gallery.json";
import { useSiloamNavigation } from "./atlas-siloam-navigation";
import { defaultSubject, type SiloamSubject } from "./atlas-siloam-reading";
import "./atlas-siloam-comparison.css";

type Feature = {label: string; observation: string; unresolved: string; source: string; photo?: string};
const features: Record<SiloamSubject, Feature> = {
  "tunnel-mouth": {label: "Tunnel outlet", observation: "Water emerges at the tunnel mouth into the smaller Silwan pool. Szanton proposes this pool as ancient Siloam.",
    unresolved: "Which dated trough or gutter lay at the outlet?", source: "siloam-names", photo: "jer_siloam-tunnel-outlet-2009"},
  "stepped-basin": {label: "Birket al-Hamra", observation: "The 2024 excavation plan records steps along the larger basin. Figure 6 reconstructs its full outline.",
    unresolved: "Can a contemporary pipe be joined to a bathing floor in this basin?", source: "siloam-2024", photo: "jer_siloam-steps-2017"},
  receiver: {label: "Small receiving basin", observation: "Greenhut and Mazor record a plastered floor inside the small receiver and interpret the basin as overflow storage.",
    unresolved: "What establishes bathing or another required use during the relevant phase?", source: "siloam-plan"},
  conduit: {label: "Conduit L103", observation: "L103 crosses wall W1. Its bottom stands 0.75 m above the small receiver floor. That measurement applies to this receiver alone.",
    unresolved: "Can the conduit fabric and the surface beneath it satisfy the selected reading in one phase?", source: "siloam-plan"},
};

export default function SiloamComparison() {
  const nav = useSiloamNavigation();
  if (!nav?.reading) return null;
  const reading = entryArguments.find(entry => entry.entryId === "49")?.branches.find(branch => branch.id === nav.reading);
  if (!reading) return null;
  const active = nav.subject ?? defaultSubject[nav.reading];
  const feature = features[active];
  const source = dossierSources.find(item => item.id === feature.source);
  const photo = gallery.find(item => item.id === feature.photo);
  const imageRoot = (import.meta.env?.BASE_URL ?? "/") + "dossiers/site-photos/gallery/";
  const preferred = defaultSubject[nav.reading];
  const subjects = [preferred, ...(Object.keys(features) as SiloamSubject[]).filter(id => id !== preferred)];
  return <section className="siloam-comparison" aria-label="Entry 49 reading and feature">
    <header><div><small>X 15–16 · Entry 49</small><h3>{reading.label}</h3></div><button type="button" onClick={nav.read}>Back to passage</button></header>
    <p>{reading.reading}</p>
    {nav.reading === "water-closet-jehu" && <p>This reading leaves the locality open. These Siloam features serve as comparisons.</p>}
    <label>Compare a water feature
      <select value={active} onChange={event => nav.inspect(event.target.value as SiloamSubject)}>
        {subjects.map(id => <option key={id} value={id}>{features[id].label}</option>)}
      </select>
    </label>
    <div aria-live="polite"><p>{feature.observation}</p><p><b>Open question</b> {feature.unresolved}</p>
      {source && <a href={source.url} target="_blank" rel="noreferrer">{source.title} · {source.locator}</a>}
    </div>
    {photo && <figure><img src={imageRoot + photo.web} alt={photo.alt} loading="lazy"/><figcaption><a href={photo.sourceUrl} target="_blank" rel="noreferrer">{photo.date} · {photo.author}</a> · {photo.licenseUrl ? <a href={photo.licenseUrl} target="_blank" rel="noreferrer">{photo.license}</a> : photo.license}</figcaption></figure>}
    <p className="siloam-frame-note">The map pin marks the pool complex. The plan below shows L103 and the small receiver in excavation coordinates.</p>
  </section>;
}
