"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import * as T from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { BookOpen, ExternalLink, RotateCcw } from "lucide-react";
import { columnAt, isHeldSegment, layoutScroll, LIGHT_NAMES, pickFrame, ROMAN, SHEET_HEIGHT_M, sheetPoint, type ScrollLayout } from "./atlas-scroll-3d-model";
import "./atlas-scroll-3d.css";

// The scroll as an object: rolled, unrolled, or cut into its 23 strips. The
// strips carry the edition-based transcription, or, in the access-controlled
// build only, the WSRP 1988 photographs (wsrp/frames.json next to the page).

export type Line3d = { ref: string; no: number; text: string };
type Frame = { segment: number; light: string; strip?: string; full: string; aspect?: number; fragments?: boolean };
type Media = { frames: Frame[]; credit: string };
type Props = { columns: Line3d[][]; column: number; onColumn: (column: number) => void; onClose: () => void };
type Strip = { segment: number; u0: number; u1: number; front: T.Mesh; back: T.Mesh; geometry: T.BufferGeometry; text: T.CanvasTexture; photo?: { map: T.Texture; alpha: T.Texture; light: string } };

const PX_PER_M = 3400;
const SHAPES = [{ id: 0, label: "Rolled" }, { id: 1, label: "Unrolled" }, { id: 2, label: "Strips" }];
const GAP_M = 0.018;
const PHOTO_SITE = ((import.meta.env as unknown as Record<string, string | undefined> | undefined)?.VITE_WSRP_PHOTO_SITE) ?? "";

function median(values: number[]) { const v = [...values].sort((a, b) => a - b); return v.length ? v[Math.floor(v.length / 2)] : 0; }

/** Draw the transcription onto one strip, clipped to the columns it carries. */
function drawText(layout: ScrollLayout, strip: { u0: number; u1: number; columns: number[] }, columns: Line3d[][], font: string) {
  const w = Math.max(8, Math.round((strip.u1 - strip.u0) * PX_PER_M)), h = Math.round(SHEET_HEIGHT_M * PX_PER_M);
  const canvas = document.createElement("canvas"); canvas.width = w; canvas.height = h;
  const ctx = canvas.getContext("2d")!;
  const g = ctx.createLinearGradient(0, 0, w, h); g.addColorStop(0, "#b98455"); g.addColorStop(.5, "#9c6a3f"); g.addColorStop(1, "#7f5331");
  ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = "#6b8f7a22"; for (let i = 0; i < w * h / 900; i++) ctx.fillRect((i * 7919) % w, (i * 104729) % h, 3, 2);
  const margin = .012;
  for (const c of strip.columns) {
    const box = layout.columns[c], lines = columns[c] ?? [];
    if (!lines.length) continue;
    const top = .022, lineH = (SHEET_HEIGHT_M - 2 * top) / Math.max(lines.length, 12);
    const right = (strip.u1 - (box.u0 + margin)) * PX_PER_M, left = (strip.u1 - (box.u1 - margin)) * PX_PER_M;
    let size = lineH * PX_PER_M * .6;
    ctx.font = `${size}px ${font}`;
    const longest = Math.max(...lines.map(l => ctx.measureText(l.text).width));
    if (longest > right - left) size *= (right - left) / longest;
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, w, h); ctx.clip();
    ctx.font = `${size}px ${font}`; ctx.direction = "rtl"; ctx.textAlign = "right"; ctx.textBaseline = "middle";
    lines.forEach((l, i) => {
      const y = (top + (i + .5) * lineH) * PX_PER_M;
      ctx.fillStyle = "#fbd7a644"; ctx.fillText(l.text, right + 1.2, y + 1.2);
      ctx.fillStyle = "#2c1b0ee0"; ctx.fillText(l.text, right, y);
    });
    ctx.restore();
  }
  const t = new T.CanvasTexture(canvas); t.colorSpace = T.SRGBColorSpace; t.anisotropy = 4; return t;
}

/** An alpha mask from a cut-out photograph, so the back face keeps the broken outline. */
function alphaFrom(image: HTMLImageElement | ImageBitmap) {
  const canvas = document.createElement("canvas"); canvas.width = Math.max(1, Math.round(image.width / 4)); canvas.height = Math.max(1, Math.round(image.height / 4));
  const ctx = canvas.getContext("2d")!; ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
  const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < data.data.length; i += 4) { const a = data.data[i + 3]; data.data[i] = data.data[i + 1] = data.data[i + 2] = a; data.data[i + 3] = 255; }
  ctx.putImageData(data, 0, 0); return new T.CanvasTexture(canvas);
}

export default function Scroll3d({ columns, column, onColumn, onClose }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const [media, setMedia] = useState<Media | null | undefined>(undefined);
  const [target, setTarget] = useState(1);
  const [surface, setSurface] = useState<"text" | "photo">("text");
  const [light, setLight] = useState<string | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const [failed, setFailed] = useState(false);
  const runtime = useRef<{ setShape: (t: number) => void; fit: () => void; highlight: (column: number, segment: number | null) => void; surface: (s: "text" | "photo", light: string | null) => void } | null>(null);
  const latest = useRef({ onColumn, column });
  useEffect(() => { latest.current = { onColumn, column }; }, [onColumn, column]);

  // The photographs exist only in the access-controlled build.
  useEffect(() => {
    let cancelled = false;
    const base = import.meta.env?.BASE_URL ?? "/";
    fetch(`${base}wsrp/frames.json`, { cache: "no-store" }).then(r => r.ok ? r.json() as Promise<Media> : null).then((m: Media | null) => { if (!cancelled) { setMedia(m && Array.isArray(m.frames) ? m : null); if (m?.frames?.length) setSurface("photo"); } }).catch(() => { if (!cancelled) setMedia(null); });
    return () => { cancelled = true; };
  }, []);

  const layout = useMemo(() => {
    if (media === undefined) return null;
    const bySegment: Record<number, number[]> = {};
    for (const f of media?.frames ?? []) if (!isHeldSegment(f.segment) && f.strip && f.aspect && f.aspect > 0) (bySegment[f.segment] ??= []).push(f.aspect);
    return layoutScroll(Object.fromEntries(Object.entries(bySegment).map(([s, a]) => [s, median(a) * SHEET_HEIGHT_M])));
  }, [media]);

  useEffect(() => {
    const el = host.current;
    if (!el || !layout) return;
    let renderer: T.WebGLRenderer;
    try { renderer = new T.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "low-power" }); } catch { requestAnimationFrame(() => setFailed(true)); return; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); renderer.outputColorSpace = T.SRGBColorSpace; renderer.toneMapping = T.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.1;
    el.appendChild(renderer.domElement);
    const scene = new T.Scene(), group = new T.Group(); scene.add(group);
    const camera = new T.PerspectiveCamera(32, 1, .01, 40);
    const controls = new OrbitControls(camera, renderer.domElement); controls.enableDamping = false; controls.zoomToCursor = true; controls.screenSpacePanning = true; controls.maxDistance = 12; controls.minDistance = .08;
    scene.add(new T.HemisphereLight("#fff6e6", "#5d4a35", 1.6));
    const key = new T.DirectionalLight("#fff2d8", 2.6); key.position.set(-1.2, 1.4, 2.2); scene.add(key);
    const rake = new T.DirectionalLight("#dfe9e2", .9); rake.position.set(2, -.4, 1); scene.add(rake);

    const font = "'Frank Ruhl Libre','SBL Hebrew','Times New Roman',serif";
    const L = layout.length, H = SHEET_HEIGHT_M;
    const strips: Strip[] = layout.strips.map(s => {
      const n = Math.max(2, Math.ceil((s.u1 - s.u0) / .004));
      const geometry = new T.BufferGeometry();
      const pos = new Float32Array((n + 1) * 2 * 3), uv = new Float32Array((n + 1) * 2 * 2), index: number[] = [];
      for (let i = 0; i <= n; i++) { uv.set([i / n * -1 + 1, 0], i * 2); uv.set([i / n * -1 + 1, 1], (n + 1) * 2 + i * 2); }
      for (let i = 0; i < n; i++) { const t0 = n + 1 + i, t1 = n + 1 + i + 1; index.push(i + 1, i, t1, i, t0, t1); }
      geometry.setAttribute("position", new T.BufferAttribute(pos, 3)); geometry.setAttribute("uv", new T.BufferAttribute(uv, 2)); geometry.setIndex(index);
      geometry.userData = { n, u0: s.u0, u1: s.u1 };
      const text = drawText(layout, s, columns, font);
      const front = new T.Mesh(geometry, new T.MeshStandardMaterial({ map: text, metalness: .35, roughness: .55, side: T.FrontSide }));
      const back = new T.Mesh(geometry, new T.MeshStandardMaterial({ color: "#55705d", metalness: .3, roughness: .75, side: T.BackSide }));
      front.userData.segment = back.userData.segment = s.segment;
      group.add(front, back);
      return { segment: s.segment, u0: s.u0, u1: s.u1, front, back, geometry, text };
    });

    // Photographs: strip cut-outs, mapped to the strip rectangle.
    const frames = (media?.frames ?? []).filter(f => f.strip);
    const loader = new T.TextureLoader();
    const base = import.meta.env?.BASE_URL ?? "/";
    const photoCache = new Map<string, Promise<{ map: T.Texture; alpha: T.Texture }>>();
    function photo(f: Frame) {
      let p = photoCache.get(f.strip!);
      if (!p) { p = loader.loadAsync(`${base}${f.strip!}`).then(map => { map.colorSpace = T.SRGBColorSpace; map.anisotropy = 4; return { map, alpha: alphaFrom(map.image as HTMLImageElement) }; }); photoCache.set(f.strip!, p); }
      return p;
    }
    let surfaceNow: "text" | "photo" = "text", lightNow: string | null = null;
    function applySurface(s: "text" | "photo", wanted: string | null) {
      surfaceNow = s; lightNow = wanted;
      for (const strip of strips) {
        const fm = strip.front.material as T.MeshStandardMaterial, bm = strip.back.material as T.MeshStandardMaterial;
        const choice = s === "photo" && !isHeldSegment(strip.segment) ? pickFrame(frames.filter(f => f.segment === strip.segment), wanted) : null;
        if (!choice) { fm.map = strip.text; fm.alphaTest = 0; fm.transparent = false; bm.alphaMap = null; bm.alphaTest = 0; fm.needsUpdate = bm.needsUpdate = true; continue; }
        photo(choice).then(({ map, alpha }) => {
          if (surfaceNow !== s || lightNow !== wanted) return;
          fm.map = map; fm.alphaTest = .5; bm.alphaMap = alpha; bm.alphaTest = .5; fm.needsUpdate = bm.needsUpdate = true; strip.photo = { map, alpha, light: choice.light }; render();
        }).catch(() => {});
      }
      render();
    }

    let shapeNow = 1;
    function place(t: number) {
      shapeNow = t;
      const unroll = Math.min(1, t), spread = Math.max(0, t - 1);
      strips.forEach((s, k) => {
        const { n, u0, u1 } = s.geometry.userData as { n: number; u0: number; u1: number };
        const attr = s.geometry.getAttribute("position") as T.BufferAttribute;
        const dx = (11 - k) * GAP_M * spread;
        for (let i = 0; i <= n; i++) {
          const u = u0 + (u1 - u0) * i / n;
          const [x, z] = sheetPoint(u, unroll, L);
          attr.setXYZ(i, x + dx, -H / 2, z); attr.setXYZ(n + 1 + i, x + dx, H / 2, z);
        }
        attr.needsUpdate = true; s.geometry.computeVertexNormals(); s.geometry.computeBoundingBox(); s.geometry.computeBoundingSphere();
      });
      group.position.x = -(L / 2) * (1 - unroll) + .06 * (1 - unroll);
      render();
    }

    let width = 1, height = 1;
    function render() { renderer.render(scene, camera); }
    function fit() {
      group.updateMatrixWorld(true);
      const box = new T.Box3().setFromObject(group), size = box.getSize(new T.Vector3()), centre = box.getCenter(new T.Vector3());
      const vFov = T.MathUtils.degToRad(camera.fov), aspect = width / height;
      const dist = Math.max(size.y / 2 / Math.tan(vFov / 2), size.x / 2 / (Math.tan(vFov / 2) * aspect)) * 1.18 + size.z / 2;
      controls.target.copy(centre); camera.position.set(centre.x, centre.y + dist * .08, centre.z + dist); camera.near = dist / 200; camera.far = dist * 20; camera.updateProjectionMatrix(); controls.update(); render();
    }
    function resize() { const r = el!.getBoundingClientRect(); width = Math.max(1, r.width); height = Math.max(1, r.height); renderer.setSize(width, height, false); camera.aspect = width / height; camera.updateProjectionMatrix(); render(); }
    let anim = 0;
    function setShapeAnimated(to: number) {
      cancelAnimationFrame(anim);
      const from = shapeNow, reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduced || Math.abs(to - from) < 1e-3) { place(to); fit(); return; }
      const start = performance.now(), ms = 900 + 700 * Math.abs(to - from);
      const tick = (now: number) => { const p = Math.min(1, (now - start) / ms), e = p < .5 ? 2 * p * p : 1 - (-2 * p + 2) ** 2 / 2; place(from + (to - from) * e); if (p < 1) anim = requestAnimationFrame(tick); else fit(); };
      anim = requestAnimationFrame(tick);
    }
    function highlight(c: number, segment: number | null) {
      for (const s of strips) {
        const m = s.front.material as T.MeshStandardMaterial, onColumn = layout!.strips[s.segment - 1].columns.includes(c);
        m.emissive.set(s.segment === segment ? "#a86a2c" : onColumn ? "#5b3a17" : "#000000"); m.emissiveIntensity = s.segment === segment ? .35 : onColumn ? .18 : 0;
      }
      render();
    }

    controls.addEventListener("change", render);
    const observer = new ResizeObserver(() => { resize(); }); observer.observe(el); resize();
    place(1); fit();
    let down: { x: number; y: number } | null = null;
    const pd = (e: PointerEvent) => { down = { x: e.clientX, y: e.clientY }; };
    const pu = (e: PointerEvent) => {
      if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 5) { down = null; return; } down = null;
      const r = el.getBoundingClientRect(), ray = new T.Raycaster();
      ray.setFromCamera(new T.Vector2((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1), camera);
      const hit = ray.intersectObjects(strips.flatMap(s => [s.front, s.back]))[0];
      if (!hit || !hit.uv) return;
      const s = strips[(hit.object.userData.segment as number) - 1], u = s.u1 - hit.uv.x * (s.u1 - s.u0);
      setSelected(s.segment); latest.current.onColumn(columnAt(layout!, u));
    };
    renderer.domElement.addEventListener("pointerdown", pd); renderer.domElement.addEventListener("pointerup", pu);
    runtime.current = { setShape: setShapeAnimated, fit, highlight, surface: applySurface };
    highlight(latest.current.column, null);
    return () => {
      cancelAnimationFrame(anim); runtime.current = null; observer.disconnect(); controls.dispose();
      renderer.domElement.removeEventListener("pointerdown", pd); renderer.domElement.removeEventListener("pointerup", pu);
      for (const s of strips) { s.geometry.dispose(); s.text.dispose(); (s.front.material as T.Material).dispose(); (s.back.material as T.Material).dispose(); }
      photoCache.forEach(p => p.then(({ map, alpha }) => { map.dispose(); alpha.dispose(); }).catch(() => {}));
      renderer.dispose(); renderer.forceContextLoss(); renderer.domElement.remove();
    };
  }, [layout, columns, media]);

  useEffect(() => { runtime.current?.setShape(target); }, [target]);
  useEffect(() => { runtime.current?.highlight(column, selected); }, [column, selected, layout]);
  useEffect(() => { runtime.current?.surface(surface, light); }, [surface, light, layout]);

  const all = media?.frames ?? [], frames = all.filter(f => f.strip);
  const lights = Array.from(new Set(frames.map(f => f.light))).sort((a, b) => a.localeCompare(b));
  const strip = selected && layout ? layout.strips[selected - 1] : null;
  const stripFrames = strip ? frames.filter(f => f.segment === strip.segment) : [];
  const fragments = strip ? all.filter(f => f.segment === strip.segment && f.fragments) : [];
  const shown = strip ? pickFrame(stripFrames, light) : null;
  const base = import.meta.env?.BASE_URL ?? "/";
  const colsOf = (s: { columns: number[] }) => s.columns.map(c => ROMAN[c]).join("–");

  const shape = target;
  return <div className="scroll-3d" data-ready={!!layout && !failed}>
    <header className="scroll-3d-head">
      <div><span className="small-caps">3Q15 · the scroll as an object</span><h2>{shape < .5 ? "Rolled" : shape < 1.5 ? "Unrolled" : "Cut into 23 strips"}</h2></div>
      <div className="scroll-3d-actions">
        <div role="group" aria-label="Shape of the scroll">{SHAPES.map(s => <button key={s.id} type="button" aria-pressed={target === s.id} onClick={() => setTarget(s.id)}>{s.label}</button>)}</div>
        {frames.length > 0 && <div role="group" aria-label="Strip surface"><button type="button" aria-pressed={surface === "text"} onClick={() => setSurface("text")}>Transcription</button><button type="button" aria-pressed={surface === "photo"} onClick={() => setSurface("photo")}>Photographs</button></div>}
        {frames.length > 0 && surface === "photo" && <label className="scroll-3d-light">Light<select value={light ?? ""} onChange={e => setLight(e.target.value || null)}><option value="">Best per strip</option>{lights.map(l => <option key={l} value={l}>{LIGHT_NAMES[l] ?? l}</option>)}</select></label>}
        <button type="button" className="scroll-3d-icon" aria-label="Reset the view" onClick={() => runtime.current?.fit()}><RotateCcw size={15} /></button>
        <button type="button" className="reader-text-button" onClick={onClose}><BookOpen size={14} />Text view</button>
      </div>
    </header>
    <div className="scroll-3d-stage" ref={host} tabIndex={0} role="img" aria-label={`3D model of the Copper Scroll, ${shape < .5 ? "rolled" : shape < 1.5 ? "unrolled" : "cut into strips"}. Select a strip to see its segment and column.`}>
      {!layout && !failed && <p className="scroll-3d-status" role="status">Unrolling the scroll…</p>}
      {failed && <p className="scroll-3d-status" role="alert">3D rendering is not available in this browser. The text view still works.</p>}
      <p className="scroll-3d-help">Drag to turn · scroll or pinch to zoom · right-drag to pan · select a strip</p>
    </div>
    <div className="scroll-3d-foot">
      <div className="scroll-3d-card" aria-live="polite">
        {strip ? <>
          <strong>Segment {strip.segment} · column {colsOf(strip)}</strong>
          <span>Width {((strip.u1 - strip.u0) * 100).toFixed(1)} cm · {strip.measured ? "from the 1988 photograph (strip height = 30 cm), then scaled with all strips to a 2.4 m sheet" : "assumed: the mean of the photographed strips"}</span>
          {isHeldSegment(strip.segment) ? <span>Reserved for a blind reading of XII 10: no photograph is shown for segments 19–23.</span>
            : shown ? <span>WSRP 1988 · {LIGHT_NAMES[shown.light] ?? shown.light} · <a href={`${base}${shown.full}`} target="_blank" rel="noreferrer">full frame <ExternalLink size={11} /></a>{fragments.map(f => <span key={f.full}> · <a href={`${base}${f.full}`} target="_blank" rel="noreferrer">loose fragments <ExternalLink size={11} /></a></span>)}</span>
            : frames.length ? <span>No 1988 frame of this segment in the copy held by the project.</span> : null}
          <button type="button" className="reader-text-button" onClick={onClose}>Read column {ROMAN[column]}</button>
        </> : <span>Select a strip. The strips of column {ROMAN[column]} are lit.</span>}
      </div>
      <details className="scroll-3d-notes"><summary>What is drawn, and what is assumed</summary>
        <p>The sheet is about 2.4 m long and 30 cm high, in 23 strips cut in Manchester in 1955–56. The text is M. G. Abegg Jr.’s transcription in modern type, not the engraved letters.</p>
        <p>Columns I–X follow the segment map in Puech 2006’s radiograph captions. XI = 19–20 and XII = 21–23 are assumed. A segment shared by two columns is split at its middle.</p>
        <p>{frames.length ? "Strip widths with a photograph are measured on it, with the strip height taken as 30 cm; the others get the mean. All are then scaled together to 2.4 m, because the photographs show the strips curved." : "Strip widths are assumed."} The roll is one illustrative roll with the inscribed face inside; the scroll was found as two rolls, and the joins of its three sheets are not drawn.</p>
        {frames.length > 0 ? <p>{media?.credit}</p> : PHOTO_SITE ? <p>The 1988 photographs are available to approved readers on the <a href={PHOTO_SITE} target="_blank" rel="noreferrer">photo version of the atlas</a>, which needs a sign-in.</p> : <p>The 1988 photographs are not published here.</p>}
      </details>
    </div>
  </div>;
}
