"use client";

import { useEffect, useId, useRef, useState } from "react";
import { BookOpen, Box, Pause, Play } from "lucide-react";
import type { Entry } from "./atlas-types";

const models = {
  "11": {
    title: "Pool east of Koḥlit", lines: "II 13–15", cubits: 4,
    text: "In the pool that is east of Koḥlit, in the northern corner, dig four cubits: 22 talents.",
    assumptions: "The rectangular 12 × 8 m envelope, floor 2 m below the rim, and downward measurement from the floor are illustrative assumptions. The text leaves the northern corner’s eastern or western position unspecified. Koḥlit remains unplaced; no site coordinates are used here.",
    reading: "The reading notes flag an editorial disagreement at II 14. The model follows the project’s four-cubit translation. See the Text tab for the alternative Koḥlit proposals and their references.",
  },
  "25": {
    title: "Cave with two entrances", lines: "VI 1–6", cubits: 3,
    text: "[In] the cave of the pillar with the two [en]trances, facing east, [at] the northern entrance, dig three [cu]bits: there is a jar, in it one scroll; under it 42 talents.",
    assumptions: "The cave outline, 12 × 8 m envelope, entrance spacing and downward measurement from an entrance surface are illustrative assumptions. Both mouths face east in this model; Milik’s translation describes the cave as facing east without assigning each mouth a bearing. “Cave of the pillar” establishes no pillar position; none is drawn. No site coordinates are used here.",
    reading: "Restored letters remain in brackets. The deposit marker represents the entry’s claim; no jar, scroll or silver has been observed at the modeled point.",
  },
};

type Props = { entry: Entry; onEntry: (id: string) => void; onText: () => void };

export default function SceneView({ entry, onEntry, onText }: Props) {
  const model = models[entry.id as keyof typeof models];
  const cave = entry.id === "25";
  const [view, setView] = useState("plan");
  const [unit, setUnit] = useState(.5);
  const [corner, setCorner] = useState("east");
  const [progress, setProgress] = useState(1);
  const [playing, setPlaying] = useState(false);
  const [width, setWidth] = useState(600);
  const drawing = useRef<HTMLDivElement>(null);
  const frame = useRef<number | null>(null);
  const pattern = `scene-soil-${useId().replace(/:/g, "")}`;

  useEffect(() => {
    const element = drawing.current;
    if (!element) return;
    const observer = new ResizeObserver(([r]) => setWidth(r.contentRect.width));
    observer.observe(element);
    return () => observer.disconnect();
  }, [model]);
  useEffect(() => () => { if (frame.current !== null) cancelAnimationFrame(frame.current); }, []);

  function finish() {
    if (frame.current !== null) cancelAnimationFrame(frame.current);
    frame.current = null; setPlaying(false); setProgress(1);
  }
  function trace() {
    if (playing) { finish(); return; }
    setView("cutaway");
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setProgress(1); return; }
    setPlaying(true); setProgress(0);
    let start: number | undefined;
    function tick(time: number) {
      start ??= time;
      const next = Math.min(1, (time - start) / 2200);
      setProgress(next);
      if (next < 1) frame.current = requestAnimationFrame(tick);
      else { frame.current = null; setPlaying(false); }
    }
    frame.current = requestAnimationFrame(tick);
  }

  if (!model) return <div className="scene-view scene-empty">
    <span className="small-caps">Entry {entry.id} · Textual scene</span>
    <Box size={32} strokeWidth={1.2} />
    <h2>Choose a modeled description</h2>
    <p>This entry has not yet been converted into a spatial scene. Open either of the two models below; the register and entry panel will follow.</p>
    <div className="scene-examples"><button onClick={() => onEntry("11")}>Entry 11 · Pool and northern corner</button><button onClick={() => onEntry("25")}>Entry 25 · Two cave entrances</button></div>
  </div>;

  const w = Math.max(240, width), h = 340, depth = model.cubits * unit;
  const pw = Math.min(w - 90, 350), ph = pw * 2 / 3, x = (w - pw) / 2, y = (h - ph) / 2;
  const pointX = corner === "east" ? x + pw : x;
  const floor = cave ? 105 : 145, target = floor + depth * 50;
  const shown = floor + (target - floor) * progress, measureX = w * .65;

  return <div className="scene-view">
    <header className="scene-heading"><span className="small-caps">Entry {entry.id} · Textual scene</span><h2>{model.title}</h2><p>Directions and digging instructions from the entry, drawn within an assumed envelope.</p></header>
    <div className="scene-workspace">
      <div className="scene-actions"><div role="group" aria-label="Scene view"><button aria-pressed={view === "plan"} onClick={() => { finish(); setView("plan"); }}>Plan</button><button aria-pressed={view === "cutaway"} onClick={() => { finish(); setView("cutaway"); }}>Cutaway</button></div><button onClick={trace} aria-label={playing ? "Finish depth trace" : "Animate the digging depth"}>{playing ? <Pause size={14} /> : <Play size={14} />}{playing ? "Finish trace" : "Trace depth"}</button></div>
      <div ref={drawing} className="scene-drawing">
        <svg viewBox={`0 0 ${w} ${h}`} style={{ height: h }} role="img" aria-label={`${model.title}, ${view}. Shape and dimensions are assumed. ${model.cubits} cubits modeled as downward digging.`}>
          <defs><pattern id={pattern} width="9" height="9" patternUnits="userSpaceOnUse"><path d="M-2 9 9-2 M7 11 11 7" className="scene-hatch" /></pattern></defs>
          {view === "plan" ? <>
            <text x="16" y="25">Plan · north up</text><text x={w - 16} y="25" textAnchor="end">N ↑</text>
            {cave ? <>
              <path d={`M${x+pw} ${y+ph*.12} Q${x+pw*.5} ${y-18} ${x} ${y+ph*.35} Q${x-20} ${y+ph} ${x+pw*.6} ${y+ph} Q${x+pw} ${y+ph} ${x+pw} ${y+ph*.87}`} className="scene-cave scene-assumed" />
              {[.25,.75].map(f => <g key={f}><line x1={x+pw-12} y1={y+ph*f-12} x2={x+pw+9} y2={y+ph*f-12} className="scene-stated" /><line x1={x+pw-12} y1={y+ph*f+12} x2={x+pw+9} y2={y+ph*f+12} className="scene-stated" /></g>)}
              <circle cx={x+pw} cy={y+ph*.25} r="6" className="scene-deposit" />
              <text x={w/2} y={y-19} textAnchor="middle">Northern entrance selected</text><text x={w/2} y={y+ph/2} textAnchor="middle">Cave</text><text x={w/2} y="301" textAnchor="middle">East-facing mouths · model choice →</text>
            </> : <>
              <rect x={x-10} y={y-10} width={pw+20} height={ph+20} fill={`url(#${pattern})`} className="scene-wall" />
              <rect x={x} y={y} width={pw} height={ph} className="scene-pool scene-assumed" />
              <path d={`M${pointX+(corner==="east"?-30:30)} ${y} H${pointX} V${y+30}`} className="scene-stated" /><circle cx={pointX} cy={y} r="6" className="scene-deposit" />
              <text x={w/2} y={y-23} textAnchor="middle">Selected northern corner</text><text x={w/2} y={y+ph/2+4} textAnchor="middle">Pool</text>
            </>}
            <text x={w/2} y="327" textAnchor="middle">12 × 8 m envelope · assumed</text>
          </> : <>
            <text x="16" y="25">Cutaway · downward digging assumed</text>
            <path d={`M22 ${floor} H${w-22} V290 H22Z`} fill={`url(#${pattern})`} opacity=".7" />
            {cave ? <><line x1="22" y1={floor} x2={w-22} y2={floor} className="scene-assumed" /><text x="30" y={floor-14}>Entrance surface · assumed</text></> : <><path d={`M22 78 H42 V${floor} H${w-42} V78 H${w-22}`} className="scene-pool scene-assumed" /><text x="48" y="65">Rim · assumed</text><text x="48" y={floor-13}>Floor · assumed</text></>}
            <line x1={measureX} y1={floor} x2={measureX} y2={target} className="scene-assumed" /><line x1={measureX} y1={floor} x2={measureX} y2={shown} className="scene-stated" /><line x1={measureX-7} y1={floor} x2={measureX+7} y2={floor} className="scene-stated" />
            <circle cx={measureX} cy={shown} r="7" className="scene-deposit" /><text x={measureX+13} y={(floor+target)/2}>{model.cubits} cubits</text>
            <text x={w/2} y="313" textAnchor="middle">{depth.toFixed(2)} m · depth in this model</text><text x={w/2} y="331" textAnchor="middle">Claimed deposit / assumed origin</text>
          </>}
        </svg>
      </div>
      <div className="scene-key"><span>Textual relation / measure</span><span>Assumed architecture</span></div>
      <div className="scene-controls"><label>Metres per cubit · assumed <output>{unit.toFixed(2)}</output><input aria-label="Assumed metres per cubit" type="range" min=".4" max=".6" step=".01" value={unit} onChange={event => { finish(); setUnit(Number(event.target.value)); }} /></label>{!cave && <label>Northern corner · model choice<select value={corner} onChange={event => { finish(); setCorner(event.target.value); }}><option value="east">Northeast</option><option value="west">Northwest</option></select></label>}</div>
      <p className="scene-result" aria-live="polite">{model.cubits} cubits · {depth.toFixed(2)} m below the assumed {cave ? "entrance surface" : "pool floor"}.</p>
      <div className="scene-text"><span className="small-caps">3Q15 · {model.lines} · Project translation</span><p>{model.text}</p><button onClick={onText}><BookOpen size={14} />Read text & variants</button></div>
      <details className="scene-assumptions"><summary>Reading and model assumptions</summary><p>{model.assumptions}</p><p>{model.reading}</p><p>The slider is an exploratory unit conversion, not an established historical cubit. This scene assigns no candidate coordinates, archaeological phase or observed cache.</p></details>
    </div>
  </div>;
}
