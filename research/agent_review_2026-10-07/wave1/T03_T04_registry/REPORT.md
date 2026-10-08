# T03 + T04 — Prediction registry and the last entry

Agent report, 6 October 2026, saved by the coordinator. Labels: EVIDENCE / INFERENCE.

## Task 3: registry
- 79 dated, falsifiable prediction records covering 35 entries: every best-supported or medium entry, plus 23, 25 and 29, plus the Koḥlit entries 4, 11, 15, 16, 19 and 60. Each competing reading or site is its own record.
- Each record gives the edition-specific reading, the predicted feature, a common period rule (50 BCE–70 CE, extended to 135 CE), orientation, and the coordinate copied from places.json (null if absent). Cubits converted at 0.445–0.525 m (0 mismatches on check).
- Each has CONFIRM, MISS and INCONCLUSIVE rules on a five-level scale (L0–L4, plus MISS) and the fields an excavation report must record to be scorable.
- README.md covers the schema, a blind-scoring protocol and timestamping options (signed commit, Zenodo, OSF, OpenTimestamps). Nothing was posted. `registry_hashes.txt` and `MANIFEST.sha256` are ready for timestamping.

## Findings
1. **INFERENCE, high:** the entry 9 (East Gate), 29 (Hyrcania) and 46 (Ramat Raḥel) candidates already fail against recorded features, so only new observations can confirm them.
2. **EVIDENCE:** entry 60's target turns on two readings — "north" (Milik) or "hidden" (Puech), and "tombs" or "buried" at its mouth (Lurie, via Wikipedia). Scored as four branches.
3. **"Copy of this document"** — three published views (EVIDENCE): a duplicate (Schiffman), a more detailed copy (Pixner; Encyclopaedia Judaica), or symbolic (Høgenhaven 2016 p. 70). INFERENCE, medium: the phrase echoes Deut 17:18 "a copy of this Teaching", and the nouns after it ("its explanation, and their measurements, and the details of each and every one") point to a copy plus a key.
4. **Koḥlit:** ten proposals found (`kohlit_proposals.csv`). INFERENCE, medium: entries 19 and 60 together imply at least two pits north of the anchor.
5. **Ranked targets for entry 60** (all high priority): Tell es-Sultan north cemetery first; then the ʿEin el-Ghuweir cemetery north of the building; then ʿEin Samiya shaft tombs (which depend on a reading the plates don't support). Four more targets have no site yet.

**Moves an identification?** No.

## Blocked
Zissu article (PEQ) returned 403; the Lefkovits and Allegro books on archive.org are lending-only.

## Best next step
Timestamp the registry, then desk-test P60-T1/P19-A against published Jericho tomb records: shafts north of the tell, mouth orientation, tombs within 5 m, Roman reuse.

Files: registry.json, registry.csv, registry_schema.json, registry_hashes.txt, MANIFEST.sha256, README.md, entry60_readings.csv, copy_interpretations.csv, kohlit_proposals.csv, kohlit_joint_constraints.csv, kohlit_context_and_access.csv, scripts/, downloads/.
