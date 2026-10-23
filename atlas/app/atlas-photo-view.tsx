"use client";

import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { X } from "lucide-react";
import type { WalkController } from "./atlas-map-walk";
import type { MapSiteRuntime } from "./atlas-map-site-layer";
import { DEFAULT_EYE_HEIGHT, photoFrame, viewpointEye, viewpointJson, viewpointStatus, type PhotoViewpoint } from "./atlas-photo-viewpoints";
import "./atlas-walk-tools.css";

// licenseUrl is null for the project owner's own photographs: shown with his permission, no open licence.
export type ReferencePhoto = { key: string; src: string; thumb: string; title: string; credit: string; license: string; licenseUrl: string | null; sourceUrl: string; date?: string; caption: string; width?: number; height?: number };
type Props = { photo: ReferencePhoto; start: PhotoViewpoint | null; edit?: boolean; planId: string; walker: () => WalkController | null; site: () => MapSiteRuntime | null; container: () => HTMLElement | null; onExit: () => void };

const today = () => new Date().toISOString().slice(0, 10);
const norm = (deg: number) => ((deg % 360) + 360) % 360;

// A new viewpoint from the walker's present camera, for a photo that has none yet.
function cameraViewpoint(planId: string, walker: WalkController | null, runtime: MapSiteRuntime | null, el: HTMLElement | null): PhotoViewpoint {
  const camera = walker?.camera(), eye = camera?.eye ?? [0, DEFAULT_EYE_HEIGHT, 0], ground = runtime?.groundAt(eye[0], eye[2]) ?? null;
  const canvasAspect = el ? el.clientWidth / Math.max(el.clientHeight, 1) : 1.5;
  const hfov = camera ? 2 * Math.atan(Math.tan(camera.fov * Math.PI / 360) * canvasAspect) * 180 / Math.PI : 60;
  return { plan: planId, position: [eye[0], eye[2]], ...(ground == null ? { y: eye[1] } : { eyeHeight: eye[1] - ground }), bearing: norm(camera?.bearing ?? 0), pitch: camera?.pitch ?? 0, hfov: Math.min(120, hfov), status: "aligned by eye", uncertainty: {}, note: "", alignedBy: "", date: today() };
}

// A photo shown from where it was taken: the walker stands at the viewpoint, the camera takes the photo's
// bearing, pitch and field of view, and the photo is drawn over the canvas at the scale that matches the
// camera, with an opacity slider between model and photo. Walking is paused; Esc or × returns to walking.
// The editor section lets the people who set viewpoints move the camera and copy it as viewpoint JSON for
// atlas-photo-viewpoints.json. Nothing is saved by the page.
export default function PhotoView({ photo, start, edit = false, planId, walker, site, container, onExit }: Props) {
  const host = container();
  const [viewpoint, setViewpoint] = useState<PhotoViewpoint>(() => start ?? cameraViewpoint(planId, walker(), site(), container()));
  const [edited, setEdited] = useState(false);
  const [opacity, setOpacity] = useState(.5);
  const [editing, setEditing] = useState(edit || !start);
  const [json, setJson] = useState("");
  const [copyState, setCopyState] = useState("");
  const [size, setSize] = useState(() => ({ width: host?.clientWidth ?? 1, height: host?.clientHeight ?? 1 }));
  const [aspect, setAspect] = useState(photo.width && photo.height ? photo.width / photo.height : 1.5);
  const base = import.meta.env?.BASE_URL ?? "/";
  // The latest values for listeners and effects that must not re-run on every render of the map.
  const latest = useRef({ viewpoint, onExit, walker, site });
  useEffect(() => { latest.current = { viewpoint, onExit, walker, site }; });

  // Keep the overlay's size; the camera's field of view follows it.
  useEffect(() => {
    if (!host || typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(([entry]) => setSize({ width: entry.contentRect.width, height: entry.contentRect.height }));
    observer.observe(host); return () => observer.disconnect();
  }, [host]);
  const frame = photoFrame(viewpoint.hfov, aspect, size.width, size.height);
  // Set the camera at the viewpoint; release it when the view closes.
  useEffect(() => {
    const runtime = latest.current.site(), eye = viewpointEye(viewpoint, (x, z) => runtime?.groundAt(x, z) ?? null);
    latest.current.walker()?.setView({ eye, bearing: viewpoint.bearing, pitch: viewpoint.pitch, fov: frame.vfov });
  }, [viewpoint, frame.vfov]);
  useEffect(() => () => latest.current.walker()?.setView(null), []);
  // Esc leaves the photo view (and not the walk). Another tool may take Esc first (the measuring tool).
  useEffect(() => {
    const escape = (e: KeyboardEvent) => { if (e.key !== "Escape" || document.pointerLockElement) return; e.stopPropagation(); e.preventDefault(); latest.current.onExit(); };
    document.addEventListener("keydown", escape, true); return () => document.removeEventListener("keydown", escape, true);
  }, []);

  function update(change: Partial<PhotoViewpoint>) { setViewpoint(v => ({ ...v, ...change })); setEdited(true); setJson(""); setCopyState(""); }
  // Editor keys: move, turn, tilt, zoom, roll and raise the camera in fine steps (Shift for coarse ones).
  useEffect(() => {
    if (!editing) return;
    const key = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement).closest("input,select,textarea") || e.ctrlKey || e.metaKey || e.altKey) return;
      const k = e.key.toLowerCase(), big = e.shiftKey ? 10 : 1, v = latest.current.viewpoint, a = v.bearing * Math.PI / 180;
      const move = (forward: number, right: number) => { const d = .1 * big; return { position: [v.position[0] + (Math.sin(a) * forward + Math.cos(a) * right) * d, v.position[1] + (-Math.cos(a) * forward + Math.sin(a) * right) * d] as [number, number] }; };
      const raise = (d: number) => v.y != null ? { y: v.y + d } : { eyeHeight: (v.eyeHeight ?? DEFAULT_EYE_HEIGHT) + d };
      const change: Partial<PhotoViewpoint> | null = k === "w" || k === "arrowup" ? move(1, 0) : k === "s" || k === "arrowdown" ? move(-1, 0) : k === "a" || k === "arrowleft" ? move(0, -1) : k === "d" || k === "arrowright" ? move(0, 1)
        : k === "q" ? { bearing: norm(v.bearing - .1 * big) } : k === "e" ? { bearing: norm(v.bearing + .1 * big) } : k === "r" ? { pitch: v.pitch + .1 * big } : k === "f" ? { pitch: v.pitch - .1 * big }
        : k === "z" ? { hfov: Math.max(5, v.hfov - .1 * big) } : k === "x" ? { hfov: Math.min(150, v.hfov + .1 * big) } : k === "[" || k === "{" ? { roll: (v.roll ?? 0) - .1 * big } : k === "]" || k === "}" ? { roll: (v.roll ?? 0) + .1 * big }
        : k === "t" || k === "pageup" ? raise(.05 * big) : k === "g" || k === "pagedown" ? raise(-.05 * big) : null;
      if (!change) return;
      e.preventDefault(); e.stopPropagation(); update(change);
    };
    document.addEventListener("keydown", key, true); return () => document.removeEventListener("keydown", key, true);
  }, [editing]);
  // Editor drag: turn and tilt the camera so the model follows the pointer; the wheel changes the field of view.
  const drag = useRef<{ x: number; y: number } | null>(null);
  function dragMove(e: React.PointerEvent) {
    if (!drag.current) return;
    const perPixel = viewpoint.hfov / frame.width, dx = e.clientX - drag.current.x, dy = e.clientY - drag.current.y;
    drag.current = { x: e.clientX, y: e.clientY };
    update({ bearing: norm(viewpoint.bearing - dx * perPixel), pitch: viewpoint.pitch + dy * perPixel });
  }

  async function copy() {
    const text = viewpointJson(photo.key, { ...viewpoint, status: "aligned by eye", date: edited ? today() : viewpoint.date });
    setJson(text);
    try { await navigator.clipboard.writeText(text); setCopyState("Copied. Paste it into app/atlas-photo-viewpoints.json under \"viewpoints\"."); }
    catch { setCopyState("The browser did not allow copying: select the text below and copy it."); }
  }
  const number = (label: string, value: number | undefined, step: number, set: (n: number) => void, unit: string) =>
    <label>{label}<input type="number" aria-label={label} step={step} value={value == null ? "" : Number(value.toFixed(3))} onChange={e => { const n = e.currentTarget.valueAsNumber; if (Number.isFinite(n)) set(n); }} /><span>{unit}</span></label>;
  const absolute = viewpoint.y != null, u = viewpoint.uncertainty ?? {};

  const overlay = host ? createPortal(<div className="photo-view-overlay" data-editing={editing} onPointerDown={e => { if (!editing) return; e.currentTarget.setPointerCapture(e.pointerId); drag.current = { x: e.clientX, y: e.clientY }; }} onPointerMove={dragMove} onPointerUp={() => { drag.current = null; }} onPointerCancel={() => { drag.current = null; }} onWheel={e => { if (editing) update({ hfov: Math.min(150, Math.max(5, viewpoint.hfov * (e.deltaY > 0 ? 1.01 : 1 / 1.01))) }); }}>
    <img src={`${base}${photo.src}`} alt={photo.caption} draggable={false} onLoad={e => { const i = e.currentTarget; if (i.naturalWidth && i.naturalHeight) setAspect(i.naturalWidth / i.naturalHeight); }}
      style={{ left: frame.left, top: frame.top, width: frame.width, height: frame.height, opacity, transform: viewpoint.roll ? `rotate(${viewpoint.roll}deg)` : undefined }} data-frame={[frame.left, frame.top, frame.width, frame.height].map(n => n.toFixed(1)).join(",")} />
  </div>, host) : null;

  return <>
    {overlay}
    <aside className="photo-view-panel" aria-label="Photo viewpoint" data-photo={photo.key}>
      <header><strong>View from the photo</strong><button onMouseDown={e => e.preventDefault()} onClick={onExit} aria-label="Leave the photo viewpoint"><X size={15} /></button></header>
      <p className="photo-view-title">{photo.title}</p>
      <p className="photo-view-status" role="status">{start && !edited ? viewpointStatus(viewpoint) : start ? "Viewpoint changed here and not saved." : "No viewpoint is recorded for this photo. The view starts from the walker’s camera."}</p>
      {start && !edited && viewpoint.note && <p className="photo-view-note">{viewpoint.note}</p>}
      <label className="photo-view-opacity"><span>Model</span><input type="range" min={0} max={1} step={.05} value={opacity} aria-label="Photo opacity: 0 shows the model only, 1 the photo only" onChange={e => setOpacity(e.currentTarget.valueAsNumber)} onPointerUp={e => e.currentTarget.blur()} /><span>Photo</span></label>
      <p className="photo-view-credit">{photo.date && <span>{photo.date} · </span>}<a href={photo.sourceUrl} target="_blank" rel="noreferrer">{photo.credit}</a> · {photo.licenseUrl ? <a href={photo.licenseUrl} target="_blank" rel="noreferrer">{photo.license}</a> : <span>{photo.license}</span>}</p>
      <p className="photo-view-limit">{start?.status === "from EXIF/GPS" ? "The camera position comes from the photo’s record; the model is not surveyed." : "The camera was placed by eye, not measured: an inference that carries the model’s own errors."} Walking is paused; Esc or × returns to walking.</p>
      <button className="photo-view-edit-toggle" aria-pressed={editing} onMouseDown={e => e.preventDefault()} onClick={() => setEditing(v => !v)}>{editing ? "Close the viewpoint editor" : "Adjust viewpoint (for editors)"}</button>
      {editing && <div className="photo-view-editor" aria-label="Viewpoint editor">
        <small>Drag the photo to turn and tilt, wheel to zoom. Keys: W A S D move 0.1 m · Q E turn · R F tilt · Z X field of view · [ ] roll · T G height; Shift for ten times.</small>
        <div className="photo-view-fields">
          {number("x (east)", viewpoint.position[0], .1, n => update({ position: [n, viewpoint.position[1]] }), "m")}
          {number("z (south)", viewpoint.position[1], .1, n => update({ position: [viewpoint.position[0], n] }), "m")}
          {absolute ? number("y (model)", viewpoint.y, .05, n => update({ y: n }), "m") : number("Eye height", viewpoint.eyeHeight ?? DEFAULT_EYE_HEIGHT, .05, n => update({ eyeHeight: n }), "m")}
          {number("Bearing", viewpoint.bearing, .1, n => update({ bearing: norm(n) }), "°")}
          {number("Pitch", viewpoint.pitch, .1, n => update({ pitch: n }), "°")}
          {number("Roll", viewpoint.roll ?? 0, .1, n => update({ roll: n }), "°")}
          {number("Field of view", viewpoint.hfov, .1, n => update({ hfov: Math.min(150, Math.max(5, n)) }), "°")}
          {number("± position", u.position, .5, n => update({ uncertainty: { ...u, position: n } }), "m")}
          {number("± bearing", u.bearing, .5, n => update({ uncertainty: { ...u, bearing: n } }), "°")}
          {number("± height", u.height, .5, n => update({ uncertainty: { ...u, height: n } }), "m")}
        </div>
        <label className="photo-view-wide">Height<select aria-label="Height reference" value={absolute ? "y" : "eye"} onChange={e => { const runtime = site(), eye = viewpointEye(viewpoint, (x, z) => runtime?.groundAt(x, z) ?? null), ground = runtime?.groundAt(viewpoint.position[0], viewpoint.position[1]) ?? 0; update(e.currentTarget.value === "y" ? { y: eye[1], eyeHeight: undefined } : { eyeHeight: eye[1] - ground, y: undefined }); e.currentTarget.blur(); }}><option value="eye">above the ground</option><option value="y">absolute (model y)</option></select></label>
        <label className="photo-view-wide">Note<textarea aria-label="Note" rows={2} value={viewpoint.note} onChange={e => update({ note: e.currentTarget.value })} /></label>
        <label className="photo-view-wide">Aligned by<input aria-label="Aligned by" type="text" value={viewpoint.alignedBy} onChange={e => update({ alignedBy: e.currentTarget.value })} /></label>
        <div className="photo-view-actions"><button onClick={() => void copy()}>Copy viewpoint JSON</button></div>
        {copyState && <small role="status">{copyState}</small>}
        {json && <textarea className="photo-view-json" aria-label="Viewpoint JSON" readOnly rows={8} value={json} onFocus={e => e.currentTarget.select()} />}
      </div>}
    </aside>
  </>;
}
