"use client";

import { useCallback, useEffect, useRef, useState, type PointerEvent as ReactPointerEvent } from "react";
import { ChevronLeft, ChevronRight, Focus, Minus, Plus, RotateCcw, SlidersHorizontal } from "lucide-react";
import photo from "./atlas-photo-data.json";
import { plain, ReadingCard, Segments, useScrollText } from "./atlas-text";
import ReaderBranches from "./atlas-reader-branches";
import { photoTarget, wordOwner } from "./atlas-reader-model";
import { parseAtlasHash } from "./atlas-navigation";
import "./atlas-reader.css";

type Box = { x: number; y: number; width: number; height: number };
type Layer = (typeof photo.views)[number];
const START: Box = { x: 170, y: 330, width: 700, height: 1000 };
const clamp = (n: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, n));
const viewDescriptions: Record<string, string> = {
  photo: "The published museum photograph, full size.",
  grooves: "Computed groove contrast from the photograph. Corrosion pits and cracks can also appear as dark lines.",
  relief: "Computed grayscale with noise reduction and local contrast.",
};
function bounded(b: Box): Box {
  return { ...b, x: clamp(b.x, -300, photo.width - b.width + 300), y: clamp(b.y, -300, photo.height - b.height + 300) };
}
// Image, hit regions and strokes share a single SVG coordinate system.
// Panning and zooming only change its viewBox; nothing is positioned in CSS pixels.
export default function PhotoReader({ entryId, onEntry, onText, onUnavailable }: { entryId: string; onEntry: (id: string) => void; onText: () => void; onUnavailable: () => void }) {
  const { data, failed, lineWords, notesFor } = useScrollText();
  const [selection, setSelection] = useState<{ entryId: string; index: number | null }>(() => ({ entryId, index: data ? photoTarget(data, entryId).index : null }));
  const selected = selection.entryId === entryId && selection.index !== null ? selection.index : data ? photoTarget(data, entryId).index : 1;
  const [view, setView] = useState<Box>(START);
  const [tracing, setTracing] = useState(false);
  const [viewId, setViewId] = useState("photo");
  const [opacity, setOpacity] = useState(.85);
  const [original, setOriginal] = useState(false);
  const [imageState, setImageState] = useState<"loading" | "loaded" | "failed">("loading");
  const [retry, setRetry] = useState(0);
  const svg = useRef<SVGSVGElement>(null);
  const drag = useRef<{ id: number; x: number; y: number; view: Box; scale: number; moved: boolean } | null>(null);
  const moved = useRef(false);
  const pinch = useRef<{ distance: number; view: Box } | null>(null);
  const pointers = useRef(new Map<number, { x: number; y: number }>());
  const item = photo.words[selected];
  const line = Object.values(data?.entries ?? {}).flat().find(l => l.ref === item.line);
  const word = line?.w[item.word];
  const owner = data ? wordOwner(data, item.line, item.word) : undefined;
  const base = import.meta.env?.BASE_URL ?? "/";
  const layer: Layer = photo.views.find(v => v.id === viewId) ?? photo.views.find(v => v.id === "photo")!;
  // Register changes without image coverage return to that entry's full text.
  // Opening the labelled example is a separate explicit action in ScrollView.
  useEffect(() => {
    if (!data) return;
    const target = photoTarget(data, entryId);
    // A hash change can reach the child before the atlas restores its entry.
    // Wait for that entry rather than replacing the new route with the old one.
    const requestedEntry = parseAtlasHash(window.location.hash)?.entryId;
    if (target.entryId !== entryId && (!requestedEntry || requestedEntry === entryId)) onUnavailable();
  }, [data, entryId, onUnavailable]);
  function chooseView(id: string) {
    if (id === viewId) return;
    setImageState("loading");
    setViewId(id);
  }

  const zoom = useCallback((factor: number, cx?: number, cy?: number) => {
    setView(b => {
      const w = clamp(b.width * factor, 150, 1400), f = w / b.width;
      const x = cx ?? b.x + b.width / 2, y = cy ?? b.y + b.height / 2;
      return bounded({ x: x - (x - b.x) * f, y: y - (y - b.y) * f, width: w, height: b.height * f });
    });
  }, []);
  function focus(index = selected) {
    const [x, y, w, h] = photo.words[index].box;
    const rect = svg.current?.getBoundingClientRect();
    const aspect = rect ? rect.width / rect.height : .8;
    const width = Math.max(w + 100, (h + 160) * aspect);
    const height = width / aspect;
    setView(bounded({ x: x + w / 2 - width / 2, y: y + h / 2 - height / 2, width, height }));
  }
  function pick(index: number, center = false) {
    const word = photo.words[index];
    const nextOwner = data ? wordOwner(data, word.line, word.word) : undefined;
    setSelection({ entryId: nextOwner ?? entryId, index });
    if (nextOwner && nextOwner !== entryId) onEntry(nextOwner);
    if (center) focus(index);
  }
  function next(delta: number) { pick((selected + delta + photo.words.length) % photo.words.length, true); }
  function start(e: ReactPointerEvent<SVGSVGElement>) {
    if (e.button !== 0) return;
    e.currentTarget.setPointerCapture(e.pointerId);
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const rect = e.currentTarget.getBoundingClientRect();
    drag.current = { id: e.pointerId, x: e.clientX, y: e.clientY, view, scale: Math.min(rect.width / view.width, rect.height / view.height), moved: false };
    moved.current = false;
    if (pointers.current.size === 2) {
      const [a, b] = [...pointers.current.values()];
      pinch.current = { distance: Math.hypot(a.x - b.x, a.y - b.y), view };
    }
  }
  function move(e: ReactPointerEvent<SVGSVGElement>) {
    if (!pointers.current.has(e.pointerId)) return;
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.current.size === 2 && pinch.current) {
      const [a, b] = [...pointers.current.values()], p = pinch.current;
      const width = clamp(p.view.width * p.distance / Math.max(1, Math.hypot(a.x - b.x, a.y - b.y)), 150, 1400);
      const height = p.view.height * width / p.view.width;
      setView(bounded({ x: p.view.x + (p.view.width - width) / 2, y: p.view.y + (p.view.height - height) / 2, width, height }));
      moved.current = true; return;
    }
    const d = drag.current;
    if (!d || d.id !== e.pointerId) return;
    const dx = e.clientX - d.x, dy = e.clientY - d.y;
    if (Math.hypot(dx, dy) > 4) { d.moved = true; moved.current = true; }
    if (d.moved) setView(bounded({ ...d.view, x: d.view.x - dx / d.scale, y: d.view.y - dy / d.scale }));
  }
  function end(e: ReactPointerEvent<SVGSVGElement>) {
    const wasPinch = pointers.current.size > 1 || !!pinch.current;
    pointers.current.delete(e.pointerId);
    if (e.currentTarget.hasPointerCapture(e.pointerId)) e.currentTarget.releasePointerCapture(e.pointerId);
    // Pointer capture retargets clicks to the SVG. Hit-test in the same viewBox
    // coordinates instead of relying on the browser's click target.
    if (!moved.current && !wasPinch && e.type !== "pointercancel") {
      const matrix = e.currentTarget.getScreenCTM();
      if (matrix) {
        const point = new DOMPoint(e.clientX, e.clientY).matrixTransform(matrix.inverse());
        const i = photo.words.findIndex(({ box: [x, y, w, h] }) => point.x >= x && point.x <= x + w && point.y >= y && point.y <= y + h);
        if (i >= 0) pick(i);
      }
    }
    drag.current = null; pinch.current = null;
  }
  useEffect(() => {
    const el = svg.current;
    if (!el) return;
    function wheel(e: WheelEvent) {
      e.preventDefault();
      const matrix = el!.getScreenCTM();
      const p = matrix ? new DOMPoint(e.clientX, e.clientY).matrixTransform(matrix.inverse()) : null;
      zoom(Math.exp(clamp(e.deltaY, -150, 150) * .002), p?.x, p?.y);
    }
    el.addEventListener("wheel", wheel, { passive: false });
    return () => el.removeEventListener("wheel", wheel);
  }, [zoom]);

  if (data && photoTarget(data, entryId).entryId !== entryId) return <div className="reader-reader reader-original-desk"><p className="scroll-status" role="status">Entry {entryId} has no aligned photograph. Opening its full text…</p></div>;

  return <div className="reader-reader reader-original-desk">
    <header className="reader-head"><div><span className="small-caps">{layer.id === "photo" ? "Original photograph" : `${layer.label} · computed`} · Jordan Museum</span><h2>{photo.title}</h2><span className="reader-context">Entry {owner ?? "…"} · {item.line}</span></div><div className="reader-head-actions"><button className="reader-text-button" onClick={onText}>Full text</button><details className="reader-image-tools"><summary><SlidersHorizontal size={14}/>Image tools</summary><div className="reader-tools-panel">
        <div className="reader-controls" aria-label="Photograph controls">
          <button onClick={() => zoom(1.3)} aria-label="Zoom out"><Minus size={17}/></button><button onClick={() => zoom(1 / 1.3)} aria-label="Zoom in"><Plus size={17}/></button><button onClick={() => setView(START)} aria-label="Reset photograph view"><RotateCcw size={16}/></button><button onClick={() => focus()} aria-label="Focus selected word"><Focus size={17}/></button>
          <span>{Math.round(START.width / view.width * 100)}%</span>
        </div>
        <label className="reader-view-choice">Image version<select aria-label="Image version" value={layer.id} onChange={e => chooseView(e.target.value)}>{[...photo.views].sort((a, b) => Number(b.id === "photo") - Number(a.id === "photo")).map(v => <option key={v.id} value={v.id}>{v.id === "photo" ? "Original photograph" : `${v.label} · computed`}</option>)}</select></label>
        <p className="reader-view-description">{viewDescriptions[layer.id]}</p>
        <div className="reader-options"><label><input type="checkbox" checked={tracing} onChange={e => setTracing(e.target.checked)}/>Provisional tracing</label><label className="reader-opacity">Trace opacity<input type="range" min=".15" max="1" step=".05" value={opacity} onChange={e => setOpacity(+e.target.value)}/></label></div>
        <button className="reader-hold-photo" aria-pressed={original} onPointerDown={e => { e.currentTarget.setPointerCapture(e.pointerId); setOriginal(true); }} onPointerUp={() => setOriginal(false)} onPointerCancel={() => setOriginal(false)} onLostPointerCapture={() => setOriginal(false)} onKeyDown={e => { if (e.key === " " || e.key === "Enter") setOriginal(true); }} onKeyUp={() => setOriginal(false)} onBlur={() => setOriginal(false)}>Hold for original photo</button>
        <p className="reader-tool-hint">Drag to pan · scroll or pinch to zoom. Use the arrow keys to move between words.</p>
      </div></details></div></header>
    <div className="reader-workspace">
      <section className="reader-stage" aria-label="Photograph with word tracings">
        <svg ref={svg} className="reader-canvas" data-view={layer.id} viewBox={`${view.x} ${view.y} ${view.width} ${view.height}`} preserveAspectRatio="xMidYMid meet" aria-label={`Copper Scroll strip 13, ${layer.label.toLowerCase()} view. Select an outlined word; drag to pan or scroll to zoom.`} tabIndex={0}
          onPointerDown={start} onPointerMove={move} onPointerUp={end} onPointerCancel={end}
          onDoubleClick={() => zoom(.65)} onKeyDown={e => {
            if (["ArrowRight", "ArrowLeft", "+", "=", "-", "0", " "].includes(e.key)) e.preventDefault();
            if (e.key === "ArrowRight") next(-1); if (e.key === "ArrowLeft") next(1);
            if (e.key === "+" || e.key === "=") zoom(.8); if (e.key === "-") zoom(1.25); if (e.key === "0") setView(START); if (e.key === " ") setOriginal(true);
          }} onKeyUp={e => { if (e.key === " ") setOriginal(false); }} onBlur={() => setOriginal(false)}>
          <image key={`${layer.id}-${retry}`} href={`${base}${layer.image}`} x={0} y={0} width={photo.width} height={photo.height} onLoad={() => setImageState("loaded")} onError={() => setImageState("failed")}/>
          {original && layer.image !== photo.image && <image href={`${base}${photo.image}`} x={0} y={0} width={photo.width} height={photo.height}/>}
          {!original && imageState === "loaded" && photo.words.map((w, i) => <g key={w.id} className={`reader-word ${i === selected ? "selected" : ""}`} data-word-id={w.id}>
            <rect x={w.box[0]} y={w.box[1]} width={w.box[2]} height={w.box[3]} rx={9} className="reader-hit" vectorEffect="non-scaling-stroke"/>
            {i === selected && tracing && <g className="reader-trace" opacity={opacity} pointerEvents="none">{w.paths.map((d, j) => <g key={`${w.id}-${j}`}><path d={d} className="trace-shadow"/><path d={d} className="trace-line" pathLength={1}/></g>)}{w.inferred.map((d, j) => <g key={`${w.id}-i${j}`}><path d={d} className="trace-shadow trace-inferred"/><path d={d} className="trace-line trace-inferred"/></g>)}</g>}
          </g>)}
        </svg>
        {imageState === "loading" && <div className="reader-loading" role="status">Loading the {layer.id === "photo" ? "photograph" : `${layer.label.toLowerCase()} image`}…</div>}
        {imageState === "failed" && <div className="reader-loading" role="alert">The image could not load.<button onClick={() => { setImageState("loading"); setRetry(v => v + 1); }}>Retry</button></div>}
      </section>
      <aside className="reader-reading" aria-label="Selected word interpretation">
        <div className="reader-word-nav"><button onClick={() => next(-1)} aria-label="Previous mapped word"><ChevronLeft size={16}/></button><select aria-label="Choose a mapped word" value={selected} onChange={e => pick(+e.target.value, true)}>{photo.words.map((w, i) => <option key={w.id} value={i}>{lineWords[w.line]?.[w.word] ? plain(lineWords[w.line][w.word]) : "…"} · {w.line}</option>)}</select><button onClick={() => next(1)} aria-label="Next mapped word"><ChevronRight size={16}/></button></div>
        {failed ? <p>The text could not load. Reload to retry.</p> : !data || !word || !line ? <p role="status">Loading the reading…</p> : <>
          <div className="reader-modern" lang="he" dir="rtl"><Segments w={word}/></div>
          <p className="reader-gloss">{word.m?.map(m => data.gloss[m[1]]).filter(Boolean).join(" · ") || plain(word)}</p>
          <div className="reader-line-context"><span className="reader-label">{item.line}</span><p className="reader-line-he" dir="rtl" lang="he">{line.w.map((w, i) => <span key={i} className={i === item.word ? "active" : ""}>{w.n ?? plain(w)} </span>)}</p>
          <p className="reader-translation">{line.tr.map(s => typeof s === "string" ? s : s[0]).join("")}</p>
          </div>
          {owner && ["31", "49"].includes(owner) && <details className="reader-disclosure" key={owner}><summary>Compare readings</summary><ReaderBranches entryId={owner}/></details>}
          <details className="reader-disclosure"><summary>Lettering &amp; tracing</summary><p className="reader-provisional">Provisional tracing</p><p className="reader-legend"><span className="legend-solid"/>visible groove <span className="legend-dashed"/>radiograph-supported</p><p className="reader-note">{item.note}</p><ReadingCard data={data} line={line} sel={{ line: item.line, word: item.word }} notesFor={notesFor} lineWords={lineWords} onClose={() => {}}/></details>
        </>}
      </aside>
    </div>
    <footer className="reader-credit"><p><a href={photo.source} target="_blank" rel="noreferrer">{photo.author}</a>, 2020 · <a href={photo.licenseUrl} target="_blank" rel="noreferrer">{photo.license}</a></p><details className="reader-source-details"><summary>Sources &amp; coverage</summary><div className="reader-source-content"><p><strong>{layer.id === "photo" ? "Original photograph." : "Computed photograph transform."}</strong> {viewDescriptions[layer.id]} Eight mapped words in VII 7–11; the rest of the surface is unaligned. Solid strokes follow grooves visible in the photograph; dashed strokes are supported by the separately published radiograph.</p><p>The Grooves and Relief images and the tracings are derived from the photograph and use the same licence.</p><p>{photo.alignmentReference} A facsimile photographs a copy; it is not the original metal. Grooves and Relief are computed transforms of the museum photograph, not X-rays or infrared images. {photo.imageProcessing}</p><p>Hebrew: Abegg / ETCBC, CC BY-NC 4.0. Translation and edition summaries: this project. Tracings are provisional, not a diplomatic transcription.</p></div></details></footer>
  </div>;
}
