"use client";

import { useState } from "react";
import { Camera, X } from "lucide-react";
import galleryData from "./atlas-site-gallery.json";
import sceneData from "./atlas-scenes.json";
import PhotoView, { type ReferencePhoto } from "./atlas-photo-view";
import { viewpointFor, viewpointStatus } from "./atlas-photo-viewpoints";
import type { WalkController } from "./atlas-map-walk";
import type { MapSiteRuntime } from "./atlas-map-site-layer";

const gallery = galleryData as { id: string; placeId: string; web: string; thumb: string; webWidth?: number; webHeight?: number; title: string; credit: string; license: string; licenseUrl: string | null; sourceUrl: string; date: string; caption: string }[];
const scenes = sceneData as { placeId: string; src: string; width?: number; height?: number; title: string; author: string; license: string; licenseUrl: string; sourceUrl: string; date?: string; caption: string }[];

function photosFor(placeId: string | null): ReferencePhoto[] {
  if (!placeId) return [];
  return [
    ...scenes.filter(s => s.placeId === placeId).map(s => ({ key: s.src, src: s.src, thumb: s.src, title: s.title, credit: s.author, license: s.license, licenseUrl: s.licenseUrl, sourceUrl: s.sourceUrl, date: s.date, caption: s.caption, width: s.width, height: s.height })),
    ...gallery.filter(g => g.placeId === placeId).map(g => ({ key: g.id, src: `dossiers/site-photos/gallery/${g.web}`, thumb: `dossiers/site-photos/gallery/${g.thumb}`, title: g.title, credit: g.credit.replace(/,?\s*(CC[\w .-]*|Public domain|No known restrictions[^,]*)$/i, ""), license: g.license, licenseUrl: g.licenseUrl, sourceUrl: g.sourceUrl, date: g.date, caption: g.caption, width: g.webWidth, height: g.webHeight })),
  ];
}

type Tools = { planId?: string | null; walker?: () => WalkController | null; site?: () => MapSiteRuntime | null; container?: () => HTMLElement | null };

// Photographs of the place, beside the eye-level model, for comparing the render with the real ground.
// A photo with a recorded viewpoint (atlas-photo-viewpoints.json) can be shown from where it was taken,
// over the model; the others are not registered to the model's camera.
export default function WalkReferences({ placeId, planId, walker, site, container }: { placeId: string | null } & Tools) {
  const photos = photosFor(placeId);
  const [open, setOpen] = useState(false);
  const [index, setIndex] = useState(0);
  const [viewing, setViewing] = useState<{ photo: ReferencePhoto; edit: boolean } | null>(null);
  const base = import.meta.env?.BASE_URL ?? "/";
  if (!photos.length) return null;
  const photo = photos[Math.min(index, photos.length - 1)];
  const viewpoint = planId ? viewpointFor(photo.key, planId) : null, tools = !!(planId && walker && site && container);
  // Keep keyboard focus off the buttons so W/A/S/D keep moving the walker.
  const release = () => (document.activeElement as HTMLElement | null)?.blur();
  if (viewing && tools) return <PhotoView key={`${viewing.photo.key}/${viewing.edit}`} photo={viewing.photo} start={viewpointFor(viewing.photo.key, planId)} edit={viewing.edit} planId={planId!} walker={walker!} site={site!} container={container!} onExit={() => { setViewing(null); release(); }} />;
  if (!open) return <button className="walk-reference-toggle" onMouseDown={e => e.preventDefault()} onClick={() => { setOpen(true); release(); }} aria-label={`Show ${photos.length} reference photographs`}><Camera size={15} />Reference photos · {photos.length}</button>;
  return <aside className="walk-references" aria-label="Reference photographs">
    <header><strong>Reference photos</strong><button onMouseDown={e => e.preventDefault()} onClick={() => { setOpen(false); release(); }} aria-label="Hide reference photographs"><X size={15} /></button></header>
    <a className="walk-reference-photo" href={photo.sourceUrl} target="_blank" rel="noreferrer" title="Open the photograph at its source"><img src={`${base}${photo.src}`} alt={photo.caption} /></a>
    <p className="walk-reference-credit">{photo.date && <span>{photo.date} · </span>}<a href={photo.sourceUrl} target="_blank" rel="noreferrer">{photo.credit}</a> · {photo.licenseUrl ? <a href={photo.licenseUrl} target="_blank" rel="noreferrer">{photo.license}</a> : <span>{photo.license}</span>}</p>
    {tools && <div className="walk-reference-viewpoint">
      {viewpoint && <button onMouseDown={e => e.preventDefault()} onClick={() => setViewing({ photo, edit: false })} title="Stand where the photo was taken and compare it with the model">View from here</button>}
      <button className="walk-reference-align" onMouseDown={e => e.preventDefault()} onClick={() => setViewing({ photo, edit: true })} title="For the people who set viewpoints: align this photo from the current camera and copy the viewpoint as JSON">Align (editors)</button>
      {viewpoint && <small>{viewpointStatus(viewpoint)}</small>}
    </div>}
    <div className="walk-reference-strip" role="listbox" aria-label="Choose a reference photograph">{photos.map((p, i) => <button key={p.key} role="option" aria-selected={i === index} aria-label={`${i + 1}. ${p.title}${planId && viewpointFor(p.key, planId) ? " (viewpoint)" : ""}`} onMouseDown={e => e.preventDefault()} onClick={() => { setIndex(i); release(); }}><img src={`${base}${p.thumb}`} alt="" loading="lazy" /></button>)}</div>
    <p className="walk-reference-limit">{viewpoint ? "This photo has a viewpoint aligned by eye: an inference, not a measured camera position." : "For comparison only: the model is not aligned to this photo’s camera."}</p>
  </aside>;
}
