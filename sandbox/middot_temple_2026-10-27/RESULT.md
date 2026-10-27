# Run 20 result: the Temple-area entries against Mishnah Middot

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit ebabf7e. Entry relations and scoring fixed before any Middot text was fetched ([out/step1_entry_relations.json](out/step1_entry_relations.json), SHA-256 `89319d0e…8e81`, 06:32:54Z). Exploratory, and **not blind**: most matches repeat Allegro 1960 ch. 6 pp. 107–119, Milik 1962 and Høgenhaven 2020.

## Verdict
**Not supported under the rule's definition of a pass.** No entry has a feature type *and every positional relation* agreeing with a Middot feature (Temple entries 0/11, control 0/10), because Middot never describes the hiding places themselves (cisterns, pits, the tomb).

**Lenient deviation** (type and name agree, no contradiction; fixed in the step-1 file before Middot was opened):

| Branch | Temple passing | Control passing | Fisher p | Temple joint fit (distinct features) |
|---|---|---|---|---|
| Best reading per entry | 8/11 | 1/10 | 0.006 | **6** |
| Text as shown | 7/11 | 0/10 | 0.003 | **5** |
| Puech | 5/11 | 0/10 | 0.023 | **5** |
| Lefkovits | 4/11 | 0/10 | 0.055 | 4 |
| Milik | 3/11 | 0/10 | 0.12 | 3 |

Best joint fit: 5 → the winding passage down to the immersion house (Mid 1:9); 6 → the salt chamber (Mid 5:3); 7 → the rinsers' chamber (Mid 5:3); 8 → the wood chamber, a court in the corner of the Court of Women (Mid 2:5); 9 → the Eastern Gate (Mid 1:3); 10 → the low eastern wall (Mid 2:4).

**Why this is weak:**
- Only entries 8, 9 and 10 pass on every edition. 5, 7, 13 and 14 each pass on one disputed reading (5: samekh plus מנס "refuge"; 7: המדח; 13–14: מלח as "salt").
- **The control is confounded by vocabulary.** Desert words (cairn, cave, ford, valley) cannot match an architectural tract. Scored against another architectural text, Nehemiah 3, the Temple entries pass 2–3 times (9 → "the East Gate", Neh 3:29; 10 → the wall; 5 on the "refuge" reading). Middot's whole edge comes from four name echoes: מלח, מדח, עצ, מסבה.

## Exploratory notes
- m. Eruvin 10:14 names a בור הגדול, "Great Cistern", in the Temple — entry 3's exact phrase (Allegro p. 112) — and a "Cold Well" (באר הקר), a possible echo of entry 30's "cool room".
- Entry 7's "third רובד" echoes the stair with three landings (Mid 3:6) and Bet ha-Moqed's ledges (Mid 1:8); under Allegro's reading of "the Chain", Bet ha-Moqed also has a chain (Mid 1:9).
- Control entry 25 (cave with two east-facing entrances, cache at the northern one) has the shape of the Hekhal's great gate with two wickets, only the northern one used (Mid 4:2; Tam 3:7) — a warning against reading such echoes as signal.
- A proper test needs a name-match-only score fixed in advance against a matched architectural control text (Neh 3; Josephus *BJ* 5.184–247).

## Files
[out/](out/) (step-1 relations, gazetteer of 80 features, all 7 branches × 22 entries × 80 features, summaries); [scripts/](scripts/). Sefaria texts kept in the scratch folder.
