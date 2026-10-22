"use client";

import { useEffect, useState } from "react";
import { CUBITS, DEFAULT_CUBIT, MEASURE_LABEL, MEASURE_LIMIT, measureBetween, type MeasurePoint } from "./atlas-walk-measure";
import "./atlas-walk-tools.css";

const STORE = "atlas-measure-cubit";
function storedCubit() { try { const v = Number(localStorage.getItem(STORE)); return CUBITS.some(c => c.metres === v) ? v : DEFAULT_CUBIT; } catch { return DEFAULT_CUBIT; } }

// The numbers of the eye-level measuring tool (atlas-walk-measure.ts), in metres and in a chosen cubit.
// The points are picked on the display model; the card says so, and that it is not a test.
export default function WalkMeasureCard({ points, style, units, onClear }: { points: MeasurePoint[]; style: "minecraft" | "smooth" | null; units: "metres" | "relative" | null; onClear: () => void }) {
  const [cubit, setCubit] = useState(storedCubit);
  const [locked, setLocked] = useState(() => typeof document !== "undefined" && !!document.pointerLockElement);
  useEffect(() => { const sync = () => setLocked(!!document.pointerLockElement); document.addEventListener("pointerlockchange", sync); return () => document.removeEventListener("pointerlockchange", sync); }, []);
  const chosen = CUBITS.find(c => c.metres === cubit) ?? CUBITS.find(c => c.metres === DEFAULT_CUBIT)!;
  const m = points.length === 2 ? measureBetween(points[0], points[1]) : null;
  const cubits = (metres: number) => `${(metres / cubit).toFixed(1)} cubits`;
  const row = (label: string, key: string, metres: number, text = `${metres.toFixed(2)} m`) => <div data-measure={key}><dt>{label}</dt><dd><span>{text}</span><span>{cubits(Math.abs(metres))}</span></dd></div>;
  return <>
    {locked && <div className="walk-measure-crosshair" aria-hidden="true" />}
    <aside className="walk-measure-card" aria-label="Measurement">
      <header><strong>Measure</strong>{points.length > 0 && <button onMouseDown={e => e.preventDefault()} onClick={onClear}>Clear</button>}</header>
      <p className="walk-measure-warning">{MEASURE_LABEL}</p>
      {m ? <dl>
        {row("Horizontal", "horizontal", m.horizontal)}
        {row("Height difference", "rise", m.rise, `${m.rise >= 0 ? "+" : "−"}${Math.abs(m.rise).toFixed(2)} m${Math.abs(m.rise) >= .005 ? ` (B ${m.rise > 0 ? "above" : "below"} A)` : ""}`)}
        {row("Slope distance", "slope", m.slope)}
      </dl> : <p className="walk-measure-hint">{points.length ? "Click a second point (B)." : "Click a point (A) on the model or the ground."}{locked ? " With the mouse captured, the point is under the cross." : ""}</p>}
      <label className="walk-measure-cubit">Cubit<select value={cubit} onChange={e => { const v = Number(e.currentTarget.value); setCubit(v); try { localStorage.setItem(STORE, String(v)); } catch { /* per-viewer convenience only */ } e.currentTarget.blur(); }}>
        {CUBITS.map(c => <option key={c.metres} value={c.metres}>{c.metres.toFixed(3)} m · {c.name}{c.metres === DEFAULT_CUBIT ? " (default)" : ""}</option>)}
      </select></label>
      <small className="walk-measure-source">{chosen.source}.{chosen.metres === DEFAULT_CUBIT ? " Default: the middle of the project’s 0.40–0.60 m range." : ""}</small>
      {units === "relative" && <small className="walk-measure-caveat">This model is drawn in relative units: these numbers are not metres on the ground.</small>}
      {style === "minecraft" && <small className="walk-measure-caveat">Blocks: an edge or a height can be off by up to half a block.</small>}
      <small className="walk-measure-caveat">Many heights and sizes in the display model are illustrative (Sources &amp; assumptions).</small>
      <p className="walk-measure-limit">{MEASURE_LIMIT}</p>
      <small className="walk-measure-hint">A third click starts a new measurement · Esc clears.</small>
    </aside>
  </>;
}
