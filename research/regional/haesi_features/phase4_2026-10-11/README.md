# Regional inventory phase 4: ʿAtiqot, IAA Reports, QDAP, nineteenth-century surveys, ADAJ

**What it is.** Phase 4 read five more source groups on 11 October 2026 under the phase-2 frozen rules, unchanged. The scope was frozen in [PLAN.md](PLAN.md) (commit b002e03), and five workers ran one part each.
**Main result.** 347 units in the region were read and coded, giving 265 feature rows with one zone: 22 dated by the source to the window, 91 dated outside it, 152 undated. A further 94 SWP rows sit in squares split between two zones. ʿAtiqot and IAA Reports are screened only: their 249 in-region PDFs wait for the owner's approval to download.
**What stays unknown.** Rows are not yet deduplicated against phases 1–3 or across sources: the same tomb or hoard can appear in QDAP, ADAJ and an IAA report. Most survey rows are undated. Placement is by name for every QDAP row and for most survey rows.

All of this is exploratory. It makes no identification claim, and no registered result changed.

## Parts

| Part | Source | Screened | Read in region | Feature rows (yes / no / unknown) | Folder |
|---|---|---|---|---|---|
| E | ʿAtiqot 42–121 | 1,336 articles | 0 (237 PDFs listed: T1 17, T2 208, T3 3, unlocated 9; about 463 MB) | none yet | [part_e_atiqot](part_e_atiqot/README.md) |
| F | IAA Reports 2–6, 8–78 | 82 portal items | 0 (12 PDFs listed: T2 5, T3 7; about 468 MB) | none yet | [part_f_iaa_reports](part_f_iaa_reports/README.md) |
| G | QDAP 1–14 | 346 units | 71 | 88 (8 / 44 / 36) | [part_g_qdap](part_g_qdap/README.md) |
| H | SWP Memoirs III and II, Guérin *Judée* I | 1,817 entries | 200 | 101 (0 / 10 / 91), plus 94 zone-split rows (0 / 14 / 80) | [part_h_surveys](part_h_surveys/README.md) |
| I | ADAJ 1–62 | 1,869 titles and headings | 76 | 76 (14 / 37 / 25) | [part_i_adaj](part_i_adaj/README.md) |

**Rows by zone, G + H + I, single-zone rows only:**

| Zone | Rows |
|---|---|
| Z1 Gerizim | 30 |
| Z2 Jordan Valley | 23 |
| Z3 Judean Desert | 47 |
| Z4 Jerusalem hills | 165 |

**What the in-window rows are:**

- **QDAP, all in Jerusalem and its hills:** a Tyropoeon drain, kokhim tombs, the ʿAin Karim stepped chamber, a quarry, the Citadel's Tenth Legion drain and the Silwan shekel hoard (findspot from a dealer).
- **ADAJ:** Kh. Qumran and ʿAin Feshkha installations (built sites, read normally), Murabbaʿat, Tulul Abu el-ʿAlayiq and a Herodian cave at Siyar el-Ghanam.
- **Nineteenth-century surveys:** none. The authors rarely date the features themselves.

## Protected and held

**Held, citation and first line only:**

- **IAA Reports no. 5** (Schick 1998, *The Cave of the Warrior*, Jericho-area caves).
- **QDAP:** four Tell es-Sultan items. Three are marked `protected_strip = yes`.
- **SWP Memoirs III:**
  - Jebel Kuruntul and its caves;
  - ʿAin ed Duk;
  - the Tell es-Sultan strip;
  - two cliff paragraphs at Deir el Kelt.
- **ADAJ:**
  - seven Qumran-area cave passages (ADAJ 1 p. 6; ADAJ 2 pp. 5–7, 82–83, 89; ADAJ 4/5 Arabic pp. 25–26);
  - Kenyon, "Burial Customs at Jericho" (ADAJ 16 pp. 5–30), held as a precaution for the north strip;
  - ADAJ 2 p. 88.

**Read before the hold was applied (deviations; nothing was coded from them):**

| Part | Deviation | What was read |
|---|---|---|
| F | D1 | The keywords and 25 chapter titles of IAA Reports 5 |
| G | D1 | Opening fragments of about 7 words of the held Jericho units (QDAP 5 pp. 199–201, QDAP 3 p. 176) |
| H | D1 | SWP III p. 190 on ʿAin ed Duk (OCR lines 9957–9964) |
| I | D2–D4 | A few lines of the Qumran cave passages; ADAJ 16 pp. 5–12 of Kenyon's "Burial Customs at Jericho"; the ADAJ 2 p. 88 paragraph |

The exact lines are in each part's `NOTES.md`. These texts are now exposed and cannot serve as unseen evidence.

**Kh. ʿAlmit, extraction only:** SWP III p. 107 ([part H](part_h_surveys/tier1_kh_almit_extraction.md)) and two passing mentions in QDAP 5 pp. 147 and 189 ([part G](part_g_qdap/tier1_kh_almit_extraction.md)). No arrival item exists for these records, so nothing is scored.

## Not read

- ʿAtiqot and IAA Reports bodies: they wait for the owner's approval of the PDF downloads. The portal PDFs refuse scripts, and no workaround was tried.
- QDAP vol. 6 nos. 3–4 (archive.org returned HTTP 500 for the OCR text) and vol. 10 nos. 2–3 (not on archive.org). The British Library EAP1544 page images (records -63 and -69) could fill both.
- Guérin *Judée* II–III and *Samarie* I (time limit); 443 SWP and Guérin entries that could not be located; SWP II pp. 401–408 (missing from the scan).
- ADAJ 6/7 p. 116 (blank in the scan) and ADAJ 11 "Notes & News" (missing). The Arabic parts were read from page images, because the Arabic OCR model was blocked by the proxy.

## Proposed, not applied

- Deduplicate phase-4 rows against the merged IAA inventory and across sources before using any count. The parts list known duplicates: Awarta and ʿUrif hoards, Citadel, Mefjer, Nasbeh, Abu Ghosh, ʿIsawiya, Damascus Gate, the Western Wall Plaza and Givʿati volumes.
- Add the held items above, with their deviations, to the arrival register.
- A georeferenced SWP name gazetteer would place the 360 boundary-square entries and settle the zone-split rows.
- Gazetteer gaps found by eye (el-Jib, Kalandia, Lifta, Howara, ʿUrif, Mandate spellings, "Jerusalem’s", U+02BC): consider them for a later, separately frozen screen.
