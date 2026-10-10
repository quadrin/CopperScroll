"use client";

import { useState } from "react";

const repo = "https://github.com/quadrin/CopperScroll/blob/main/";
type Branch = { id: string; label: string; editor: string; hebrew?: string; paraphrase: string; requirement: string; consequence: string; references: string[] };
const branches: Record<string, Branch[]> = {
  "31": [
    {
      id: "drying-place", label: "Drying place", editor: "Puech", hebrew: "המשט⟨ו⟩ח",
      paraphrase: "At Doq, under the eastern corner of the drying place, dig seven cubits.",
      requirement: "A drying floor, place or room, with an eastern corner and a dated surface from which the depth could be measured.",
      consequence: "Doq and ʿAin Duk remain site-level candidates. A fortress on the summit does not establish the drying installation or its corner.",
      references: ["Puech 2006, p. 192", "Puech 2015, p. 67"],
    },
    {
      id: "guard-post", label: "Guard post", editor: "Milik · Lefkovits", hebrew: "המשמרה",
      paraphrase: "At Doq, under the corner of the guard post, the eastern one, dig seven cubits.",
      requirement: "A guard post and a corner. Retain both modifier relations: the eastern corner, or a corner of the eastern guard post.",
      consequence: "The summit fortress supplies context for this reading; its presence cannot choose the letters or locate the particular installation and digging origin.",
      references: ["Milik 1962, DJD III p. 292, D19", "Lefkovits 2000, pp. 232–235"],
    },
  ],
  "49": [
    {
      id: "outlet-siloam", label: "Outlet · Siloam?", editor: "Puech", hebrew: "יציאת המים",
      paraphrase: "At the water outlet associated with Siloam, under the trough. The Siloam reading depends on a cursive waw and a supplied genitive של.",
      requirement: "A water outlet and a trough or gutter in a compatible phase. The place-name reading must be retained as conditional.",
      consequence: "Siloam is a candidate under this branch. The individual outlet–trough relation remains unverified; selecting the branch does not identify a deposit.",
      references: ["Puech 2006, p. 200", "Puech 2015, pp. 86, 91–93"],
    },
    {
      id: "displayed-baths", label: "Base text · baths", editor: "Abegg · project translation", hebrew: "בים בית חמים של רחיל",
      paraphrase: "In the basin(?) of the bathhouse(?) of Raḥil(?), under the trough.",
      requirement: "A basin with a bathhouse function, a trough, and a defensible explanation of the disputed name. This is the base transcription displayed below, not a full reconstructed Milik edition.",
      consequence: "These displayed letters do not supply Puech’s Siloam reading. A Siloam map label therefore requires a separate textual argument.",
      references: ["Milik 1962, pp. 270–271 (baths discussion)", "Project notes: e49-outlet and e49-siloam"],
    },
    {
      id: "water-closet-jehu", label: "Water closet · Jehu", editor: "Lefkovits",
      paraphrase: "A pool associated with a water closet, of Jehu. This reading supplies no Siloam place name.",
      requirement: "The relevant water installation and the name Jehu; neither can be inferred from a Siloam pin.",
      consequence: "The candidate search must stay open beyond Siloam. The name and installation alternatives travel together in this branch.",
      references: ["Lefkovits 2000, pp. 352–354"],
    },
  ],
};

/** Local exploration of retained readings; it does not change research confidence. */
export default function ReaderBranches({ entryId }: { entryId: string }) {
  const choices = branches[entryId];
  const [selected, setSelected] = useState(choices?.[0]?.id);
  if (!choices) return null;
  const branch = choices.find(b => b.id === selected) ?? choices[0];
  return <section className="reader-branches" aria-label={`Reading alternatives for entry ${entryId}`}>
    <div className="reader-branches-heading"><span className="small-caps">Entry {entryId} · reading alternatives</span><span>Edition-based</span></div>
    <div className="reader-branch-tabs" role="group" aria-label="Choose a retained reading">{choices.map(choice => <button key={choice.id} type="button" aria-pressed={choice.id === branch.id} onClick={() => setSelected(choice.id)}><strong>{choice.label}</strong><small>{choice.editor}</small></button>)}</div>
    <div className="reader-branch-result" aria-live="polite">
      {branch.hebrew && <p className="reader-branch-hebrew" dir="rtl" lang="he">{branch.hebrew}</p>}
      <p className="reader-branch-paraphrase"><span>Project paraphrase of this reading</span>{branch.paraphrase}</p>
      <dl><dt>Required feature</dt><dd>{branch.requirement}</dd><dt>Effect on the map</dt><dd>{branch.consequence}</dd></dl>
      <p className="reader-branch-citations">{branch.references.join(" · ")}. <a href={`${repo}text/readings.json`} target="_blank" rel="noreferrer">Edition apparatus</a></p>
      <p className="reader-branch-limit">The original-photo target is unresolved. {entryId === "31" ? "The mapped Doq and ‘under’ words do not adjudicate the disputed landmark." : "Column X has no aligned original photograph in this reader."} <a href={`${repo}research/text/plate_check.md`} target="_blank" rel="noreferrer">Image audit</a></p>
    </div>
  </section>;
}
