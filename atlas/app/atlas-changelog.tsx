"use client";
import {AtlasPage} from './atlas-field-notes';
import {CHANGES,EDIT_LOG} from './atlas-changelog-data';
import {REPO} from './atlas-field-notes-data';
import './atlas-field-notes.css';

export default function AtlasChangelog(){
 return <AtlasPage title="Changelog">
  <header className="fa-title">
   <p className="fa-sc fa-spaced">The Copper Scroll</p>
   <span className="fa-rule"/>
   <h1>Changelog</h1>
   <p className="fa-subtitle">what changed in the records, with the earlier value and the reason</p>
   <p className="fa-edition">13–14 November 2026 · <a href="#field-notes">back to the field notes</a><br/><i>The full log, from 13 November, is the <a href={REPO+EDIT_LOG} target="_blank" rel="noreferrer">edit log</a> in the repository.</i></p>
  </header>
  {CHANGES.map(sec=><section key={sec.id} className="fa-chapter" aria-labelledby={'cl-'+sec.id}>
   <h2 id={'cl-'+sec.id}>{sec.title}</h2>
   {sec.intro&&<p className="fa-note">{sec.intro}</p>}
   <table className="fa-reg fa-log"><thead><tr><th>Date</th><th>Item</th><th>Before</th><th>Now</th><th>Reason</th><th>Log</th></tr></thead>
    <tbody>{sec.rows.map(r=><tr key={r.item+r.now}><td className="fa-sc">{r.date}</td><td>{r.item}</td><td className="fa-before">{r.before}</td><td>{r.now}</td><td>{r.why}</td><td className="fa-sc">{r.ref?.toLowerCase()??''}</td></tr>)}</tbody></table>
  </section>)}
  <p className="fa-end">No rating, candidate or strength of a match was changed.</p>
 </AtlasPage>;
}
