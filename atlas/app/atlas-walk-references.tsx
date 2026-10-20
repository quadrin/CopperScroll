"use client";

import { useState } from "react";
import { Camera, X } from "lucide-react";
import galleryData from "./atlas-site-gallery.json";
import sceneData from "./atlas-scenes.json";

// licenseUrl is null for the project owner's own photographs: shown with his permission, no open licence.
type Photo = { key: string; src: string; thumb: string; title: string; credit: string; license: string; licenseUrl: string | null; sourceUrl: string; date?: string; caption: string };
const gallery = galleryData as { id: string; placeId: string; web: string; thumb: string; title: string; credit: string; license: string; licenseUrl: string | null; sourceUrl: string; date: string; caption: string }[];
const scenes = sceneData as { placeId: string; src: string; title: string; author: string; license: string; licenseUrl: string; sourceUrl: string; date?: string; caption: string }[];

function photosFor(placeId: string | null): Photo[] {
  if (!placeId) return [];
  return [
    ...scenes.filter(s => s.placeId === placeId).map(s => ({ key: s.src, src: s.src, thumb: s.src, title: s.title, credit: s.author, license: s.license, licenseUrl: s.licenseUrl, sourceUrl: s.sourceUrl, date: s.date, caption: s.caption })),
    ...gallery.filter(g => g.placeId === placeId).map(g => ({ key: g.id, src: `dossiers/site-photos/gallery/${g.web}`, thumb: `dossiers/site-photos/gallery/${g.thumb}`, title: g.title, credit: g.credit.replace(/,?\s*(CC[\w .-]*|Public domain|No known restrictions[^,]*)$/i, ""), license: g.license, licenseUrl: g.licenseUrl, sourceUrl: g.sourceUrl, date: g.date, caption: g.caption })),
  ];
}

// Photographs of the place, beside the eye-level model, for comparing the
// render with the real ground. The model is not registered to any photo's camera.
export default function WalkReferences({ placeId }: { placeId: string | null }) {
  const photos = photosFor(placeId);
  const [open, setOpen] = useState(false);
  const [index, setIndex] = useState(0);
  const base = import.meta.env?.BASE_URL ?? "/";
  if (!photos.length) return null;
  const photo = photos[Math.min(index, photos.length - 1)];
  // Keep keyboard focus off the buttons so W/A/S/D keep moving the walker.
  const release = () => (document.activeElement as HTMLElement | null)?.blur();
  if (!open) return <button className="walk-reference-toggle" onMouseDown={e => e.preventDefault()} onClick={() => { setOpen(true); release(); }} aria-label={`Show ${photos.length} reference photographs`}><Camera size={15} />Reference photos · {photos.length}</button>;
  return <aside className="walk-references" aria-label="Reference photographs">
    <header><strong>Reference photos</strong><button onMouseDown={e => e.preventDefault()} onClick={() => { setOpen(false); release(); }} aria-label="Hide reference photographs"><X size={15} /></button></header>
    <a className="walk-reference-photo" href={photo.sourceUrl} target="_blank" rel="noreferrer" title="Open the photograph at its source"><img src={`${base}${photo.src}`} alt={photo.caption} /></a>
    <p className="walk-reference-credit">{photo.date && <span>{photo.date} · </span>}<a href={photo.sourceUrl} target="_blank" rel="noreferrer">{photo.credit}</a> · {photo.licenseUrl ? <a href={photo.licenseUrl} target="_blank" rel="noreferrer">{photo.license}</a> : <span>{photo.license}</span>}</p>
    <div className="walk-reference-strip" role="listbox" aria-label="Choose a reference photograph">{photos.map((p, i) => <button key={p.key} role="option" aria-selected={i === index} aria-label={`${i + 1}. ${p.title}`} onMouseDown={e => e.preventDefault()} onClick={() => { setIndex(i); release(); }}><img src={`${base}${p.thumb}`} alt="" loading="lazy" /></button>)}</div>
    <p className="walk-reference-limit">For comparison only: the model is not aligned to these cameras.</p>
  </aside>;
}
