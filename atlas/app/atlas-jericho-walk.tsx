import "./atlas-jericho-walk.css";

type Props = {layer: string; onLayer: (id: string) => void; open: boolean; setOpen: (open: boolean) => void};

export default function JerichoWalk({layer, onLayer, open, setOpen}: Props) {
  const base = import.meta.env?.BASE_URL ?? "/";
  const image = base + "dossiers/trumper2018-fig22-p286.jpg";
  return <details className="jericho-walk" open={open} onToggle={event => setOpen(event.currentTarget.open)}>
    <summary>Compare pool phases</summary>
    <div className="jericho-walk-card">
      <div className="jericho-walk-phases" role="group" aria-label="Pools Complex phase">
        <button aria-pressed={layer === "stage6"} onClick={() => onLayer("stage6")}>Stage 6 · two pools</button>
        <button aria-pressed={layer === "herodian"} onClick={() => onLayer("herodian")}>Herodian · joined basin</button>
      </div>
      <p>{layer === "herodian"
        ? "Netzer records the loss of the plaza strip and the upper northern stair when the two basins were joined. The date of the alteration at the northern channel mouth remains unknown."
        : "Follow the northern branch from settling tank A(B)99 toward the pool. On folded Plan 15 the paired edges give way to a single line about 2.1 m from the wall. The walk trims the final stretch of channel to that limit. The receiving opening remains unrecorded."}</p>
      <figure>
        <svg viewBox="355 470 325 305" role="img" aria-label="Stage 6 plan detail showing the northern channel. A circle marks the approximate limit of its paired edges transferred from Plan 15.">
          <image href={image} width="1039" height="896"/>
          <circle cx="530.8" cy="669.7" r="8" fill="none" stroke="white" strokeWidth="5"/>
          <circle cx="530.8" cy="669.7" r="8" fill="none" stroke="#963d1b" strokeWidth="3"/>
        </svg>
        <figcaption>Stage 6 detail. The circle marks the approximate end of the paired edges on Plan 15, transferred to the Stage 6 drawing.</figcaption>
      </figure>
      <p className="jericho-walk-citations"><a href={image} target="_blank" rel="noreferrer">Full Stage 6 plan</a> · Trümper 2018, fig. 22 after Netzer, Plan 20 · <a href="https://creativecommons.org/licenses/by-nc/3.0/" target="_blank" rel="noreferrer">CC BY-NC 3.0</a></p>
      <p className="jericho-walk-citations">Netzer 2001, pp. 76–85, 99–100 · <a href="https://drive.google.com/file/d/1ozeSGXTBAoxosjkd_Gl1Rwrod3Pf7Pww/view" target="_blank" rel="noreferrer">Folded Plan 15</a></p>
    </div>
  </details>;
}
