"use client";

import { useEffect, useRef, useState, type MouseEvent as ReactMouseEvent, type PointerEvent as ReactPointerEvent } from "react";
import { ArrowUpLeft, ArrowUpRight, ChevronDown, ChevronLeft, ChevronRight, ChevronUp, ChevronsUp, Maximize2, Minimize2 } from "lucide-react";
import type { WalkController } from "./atlas-map-walk";
import "./atlas-walk-touch.css";

// On-screen controls for touch screens, after Minecraft Pocket Edition: a D-pad at the bottom left and a jump
// button at the bottom right; look by dragging the view. A finger can slide between the arrows; the diagonal
// arrows appear while moving forward; the centre is crouch. Double-tap forward to sprint and jump to fly, as with
// the keys (atlas-walk-physics.ts). The controls press the same keys as the keyboard, so the walk is unchanged.
type Arrow = "forward" | "back" | "left" | "right" | "forward-left" | "forward-right";
type Cell = Arrow | "centre" | null;
const KEYS: Record<Arrow, string[]> = { forward: ["w"], back: ["s"], left: ["a"], right: ["d"], "forward-left": ["w", "a"], "forward-right": ["w", "d"] };
const GRID: Cell[][] = [["forward-left", "forward", "forward-right"], ["left", "centre", "right"], [null, "back", null]];
const PAD: [Arrow, string, typeof ChevronUp][] = [["forward-left", "Forward left", ArrowUpLeft], ["forward", "Forward", ChevronUp], ["forward-right", "Forward right", ArrowUpRight], ["left", "Left", ChevronLeft], ["right", "Right", ChevronRight], ["back", "Back", ChevronDown]];
const diagonal = (cell: Cell) => cell === "forward-left" || cell === "forward-right";

export default function WalkTouchControls({ walker, flying, crouched, sprintEnabled }: { walker: () => WalkController | null; flying: boolean; crouched: boolean; sprintEnabled: boolean }) {
  // Each finger on the D-pad holds one cell and its keys.
  const fingers = useRef(new Map<number, { cell: Cell; keys: string[] }>());
  const [cells, setCells] = useState<Cell[]>([]);
  const [buttons, setButtons] = useState<string[]>([]);
  const [fullscreen, setFullscreen] = useState(false);
  const canFullscreen = typeof document !== "undefined" && !!document.fullscreenEnabled;
  const keysHeld = () => [...new Set([...fingers.current.values()].flatMap(f => f.keys))];
  const place = (id: number, cell: Cell | undefined) => {
    const before = keysHeld();
    // A diagonal works only while forward is held, as it appears only then.
    const live = cell !== undefined && diagonal(cell) && !before.includes("w") ? null : cell;
    if (live === undefined) fingers.current.delete(id); else fingers.current.set(id, { cell: live, keys: live && live !== "centre" ? KEYS[live] : [] });
    const after = keysHeld(), w = walker();
    for (const k of before) if (!after.includes(k)) w?.release(k);
    for (const k of after) if (!before.includes(k)) w?.press(k);
    setCells([...fingers.current.values()].map(f => f.cell));
  };
  const cellAt = (pad: HTMLElement, x: number, y: number): Cell => {
    const r = pad.getBoundingClientRect(), col = Math.min(2, Math.max(0, Math.floor((x - r.left) / r.width * 3))), row = Math.min(2, Math.max(0, Math.floor((y - r.top) / r.height * 3)));
    return GRID[row][col];
  };
  // Capture keeps a finger's moves on its control; a pointer that cannot be captured still works.
  const capture = (e: ReactPointerEvent<HTMLElement>) => { try { e.currentTarget.setPointerCapture(e.pointerId); } catch { /* not an active pointer */ } };
  const down = (e: ReactPointerEvent<HTMLDivElement>) => {
    e.preventDefault(); capture(e);
    const cell = cellAt(e.currentTarget, e.clientX, e.clientY);
    if (cell === "centre" && !flying) walker()?.toggleCrouch();
    place(e.pointerId, cell);
  };
  const move = (e: ReactPointerEvent<HTMLDivElement>) => { if (fingers.current.has(e.pointerId)) place(e.pointerId, cellAt(e.currentTarget, e.clientX, e.clientY)); };
  const up = (e: ReactPointerEvent<HTMLDivElement>) => { if (fingers.current.has(e.pointerId)) place(e.pointerId, undefined); };
  // Keyboard or screen-reader activation (a click without a pointer) takes one short step.
  const step = (e: ReactMouseEvent, keys: string[]) => { if (e.detail !== 0) return; const w = walker(); keys.forEach(k => w?.press(k)); setTimeout(() => keys.forEach(k => w?.release(k)), 250); };
  const holdKey = (key: string) => {
    const release = () => { walker()?.release(key); setButtons(b => b.filter(x => x !== key)); };
    return {
      onPointerDown: (e: ReactPointerEvent<HTMLButtonElement>) => { e.preventDefault(); capture(e); walker()?.press(key); setButtons(b => [...b, key]); },
      onPointerUp: release, onPointerCancel: release, onLostPointerCapture: release,
      onClick: (e: ReactMouseEvent) => step(e, [key]),
    };
  };
  useEffect(() => {
    const sync = () => setFullscreen(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", sync);
    const held = fingers.current;
    return () => { document.removeEventListener("fullscreenchange", sync); held.clear(); if (document.fullscreenElement) void document.exitFullscreen().catch(() => {}); };
  }, []);
  const forward = cells.some(c => c === "forward" || diagonal(c));
  return <div className="walk-touch" aria-label="Touch controls">
    <div className="walk-touch-pad" role="group" aria-label="Move" onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerCancel={up} onLostPointerCapture={up}>
      {PAD.map(([cell, label, Icon]) => <button key={cell} className={`walk-touch-${cell}`} aria-label={label} hidden={diagonal(cell) && !forward} data-held={cells.includes(cell)} onClick={e => step(e, KEYS[cell])}><Icon size={26} strokeWidth={2.5} /></button>)}
      <button className="walk-touch-centre" aria-label="Crouch" aria-pressed={crouched} disabled={flying} onClick={e => { if (e.detail === 0) walker()?.toggleCrouch(); }}><span /></button>
    </div>
    <div className="walk-touch-actions">
      {canFullscreen && <button className="walk-touch-small" aria-label={fullscreen ? "Exit full screen" : "Full screen"} aria-pressed={fullscreen} onClick={() => { if (document.fullscreenElement) void document.exitFullscreen().catch(() => {}); else void document.documentElement.requestFullscreen().catch(() => {}); }}>{fullscreen ? <Minimize2 size={18} /> : <Maximize2 size={18} />}</button>}
      <button className="walk-touch-small" aria-pressed={flying} title="Creative-mode flight (or double-tap jump)" onClick={() => walker()?.toggleFly()}>Fly</button>
      <button className="walk-touch-small" aria-pressed={sprintEnabled} title="Sprint (or double-tap forward)" onClick={() => walker()?.toggleSprint()}>Sprint</button>
      {flying && <button className="walk-touch-big walk-touch-down" aria-label="Down" data-held={buttons.includes("shift")} {...holdKey("shift")}><ChevronDown size={30} strokeWidth={2.5} /></button>}
      <button className="walk-touch-big walk-touch-jump" aria-label={flying ? "Up" : "Jump"} data-held={buttons.includes(" ")} {...holdKey(" ")}>{flying ? <ChevronUp size={30} strokeWidth={2.5} /> : <ChevronsUp size={30} strokeWidth={2.5} />}</button>
    </div>
  </div>;
}
