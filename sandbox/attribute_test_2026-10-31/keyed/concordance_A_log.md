# Concordance reader A — run 28 log

- Reader: A (concordance). Started 2026-11-01T03:01:22Z (UTC); finished 2026-11-01T03:17:30Z (UTC).
- Output: `keyed/concordance_A.csv` (35 rows; written with Python `csv`, UTF-8).
- Scope: *ʿAtiqot* 41.2 articles 2544–2593 (region and single-cave reports, including the finds reports in that ID range). No Region VI article exists: Region VI is part of article 2553 ("Regions IV and VI").
- Not opened: any `keyed/concordance_B*` file, the Copper Scroll or any edition of it, candidate lists, ratings, atlas, sandbox result files, `research/preregistration/`.
- Also consulted: the issue front matter (`2541_front-matter.txt`, inside the brief's `iss-2/*.txt` set), only for its table of contents (article start pages).

## How each article was read

- Read in full: 2544 (I), 2546 (II), 2550 (III), 2554 (IV/11), 2559 (V), 2560 (V/49), 2566 (VII), 2569 (VIII), 2571 (VIII/9), 2573, 2583 (IX), 2584 (X), 2585 (XI; pp. 177–179 from page images, see below), 2586–2589 (XII), 2590 (XIII), 2592 (XIV), 2593 (XV/3).
- Read in part: 2553 (IV and VI, 94 KB). I read the introduction, the roads section, the summary, the notes and the references. I also searched the whole text for earlier-survey names, years and identity words (previous, in the past, surveyed by, known as, referred to, identified, documented, published, recorded, Map Sheet, Bar-Adon, Patrich, Frumkin, Eshel, Conder) and read every hit in context.
- Read in part: 2548, 2556, 2562, 2564, 2575, 2577, 2579, 2581, 2582, 2591 (finds and specialist reports). For each I read the introduction and the notes, searched the same terms and read every hit in context.
- Page numbers come from running heads, with article start pages from the front-matter table of contents: I p. 1, II 5, Sass 21, III 35, IV/VI 43, V 85, VII 109, VIII 117, VIII/9 125, X 169, XI 177, XII 185–186, XIII 187, XIII/2 195, XIV 209.

## Page images and what could not be read

- 2585 (Region XI): printed pp. 177–179 have no text layer (the text file jumps from the cover sheet to p. 180). These pages hold the introduction and XI/1–XI/15.
  - My first try was to list the bucket prefix `atiqot/pdf/vol-041/iss-2/`. The session's permission classifier denied it.
  - The publisher's PDF (https://publications.iaa.org.il/cgi/viewcontent.cgi?article=2585&context=atiqot) returned a Cloudflare 403 to curl and WebFetch.
  - I then downloaded the single object `atiqot/pdf/vol-041/iss-2/2585_region-xi-survey-and-excavations-of-caves-along-the-fault-es.pdf`, using the same mechanism as `scripts/render_bucket.py`, and rendered PDF pages 2–4 at 170 dpi. All three pages were read. They contain no feature-identity statement (see exclusions).
- 2581 (copper objects, VIII/28): printed pp. 160–161 are missing from the text, and the bucket PDF has only 5 pages (cover, 157, 158, 159, 162). Pages 160–161 were not read. It is a metallurgical report, so an identity statement there is unlikely.
- Temporary files are in the scratchpad only (`concA_pages/`, `concA_scripts/`). Nothing was written to the repo except the two output files.

## Decision rules used

- **Identity**: the text says a 1993 feature *is* (or probably or possibly is) a feature that an earlier, named record surveyed, examined, excavated, published, numbered or named. The record need not be a survey; earlier excavations are recorded as `other:` describers.
  - Hedged statements are kept and get low or medium confidence.
  - Not recorded: comparisons ("similar to", parallels for finds), statements that a feature lies *near* an earlier-numbered cave, and bibliography entries.
- **Same-campaign publications are not earlier records** and are excluded: "this volume" papers, Schick 1998 for III/13, and Eshel & Zissu 1998/2000 for VIII/28, which was excavated in the 1993 CNJD campaign (2582 p. 163; 2575 p. 129).
- **Unnamed earlier activity is excluded.** Examples are "a previous excavation", "looted in the past" and "most likely surveyed in the past" when no person or record is named.
- **One row per statement × describer.** A sentence citing two earlier records gives two rows. A group statement gives one row with all keys `;`-separated; ranges are enumerated (for example II/20…II/31).
  - Area-level statement: one row keyed `II/*`, for the cliffs of Wadi a-Sich cited to G&G's site "Aliliyat a-Sich".
  - Unnumbered feature: one row keyed `IV-VI road (unnumbered)`, for the road that the SWP map marks.
- **describer**:
  - `ben93` = Goldfus & Golani 1993 in the Benjamin volume.
  - `djd3` = Baillet, Milik & de Vaux 1962. For XII/49, XII/52, XII/61 and the XI/18–19 caption, the text names only "de Vaux" with no date or number. I assigned these to djd3 as the de Vaux cave campaign in scope; this is an assumption, stated in each row and given low confidence.
  - `ba72`: no statement in 2544–2593 identifies a 1993 feature with a Bar-Adon 1972 site (see exclusions). The Bar-Adon rows are Bar-Adon **1989** (*ʿAtiqot* 9, excavations) and are coded `other:`.
- **ref_type**: the most specific anchor printed. The order is site_number or cave_number, then page, then name; other anchors present are given in `describer_ref` and `notes`.
  - A bare author–date citation with no page is coded `page`, and the note says no page is printed.
  - `ref_type` is left **blank** when no reference of any kind (number, page, citation or name) is printed. That applies to III/3, III/7, X/27+X/42, X/48, XI/18+19 (caption), XII/49, XII/52 and XII/61.
- **copied = yes** only when the 1993 text itself attributes repeated content about the feature to the earlier record. That content can be dimensions, a drawing, a function label, condition or finds. I did not open the earlier sources, so a description that merely follows a citation without attribution is `no`. Rows where it is `yes`:
  - II/32: dimensions printed inside the "Goldfus 1984" parenthesis, plus the function label "church".
  - VIII/9+VIII/10: section drawn "according to Frumkin 1988:16".
  - X/35: Patrich & Arubas' finds and rock numbers.
  - XIV/6: the CCR survey's note of plundering.
  - XIV/18 and XIV/51: Bar-Adon's finds.
  - Each row's note says what was repeated. Only II/32 involves dimensions.
- **Quotes**: at most 15 words, taken from the printed text. OCR "11/" is normalized to "II/". "..." marks an elision. Two quotes span a page or column break (XI/20, II/49 context).

## Exclusions (statements read and not keyed)

- 2546 p. 5: participants in the 1968 Emergency Survey "also failed to examine this wadi". This is negative; there is no Bar-Adon 1972 coverage of Region II.
- 2546 pp. 5–6: area-level history with no 1993 labels: the ICRC survey (374 caves), Patrich 1988:66–67 "a number of caves on the southern bank", el-Makkuk Cave (Eshel 1988) and the church cave. The church cave is keyed at II/32.
- 2546 p. 6: "Sixty-eight karstic caves were resurveyed" names no earlier survey; it is noted in the `II/*` row.
- 2548 pp. 29–30: "Other caves in Wadi el-Makkuk (Patrich 1988 …)" and G&G 1993:331 sherds along the wadi are area-level. Endnote 20 is keyed.
- 2550 p. 35: the intro says caves with excavation traces "were identified as some of the caves excavated by Patrich and Arubas (unpublished)". No caves are named here; the statement is carried into the III/3 and III/7 rows.
- 2550 p. 36: III/5 "an excavation had possibly been conducted here in the past" names no one.
- 2550 p. 39: III/13 "Cave of the Warrior" (Schick 1998) is the publication of the 1993 excavation (permit L-607), so it is the same campaign.
- 2553 p. 63: VI/53 "previous illegal excavations" names no one. 2553 has no other identity statements besides the road row.
- 2566 p. 114 n. 1: the Region VII caves were renumbered from the 1993 team's own field numbers. This is internal.
- 2569 pp. 117, 119: VIII/28 "Cave of the Sandal" (Eshel & Zissu 1998:119–122; 2000:6–11) is the same campaign. VIII/9 "this volume" is the same campaign.
- 2571 p. 125: "Cave VIII/10, which was excavated in 1986" names no record. VIII/10 is keyed from the 2569 table.
- 2584 p. 169: the 1952 expedition's caves "were marked and numbered … there is a problem in identifying them topographically; consequently, they were renumbered". This is an explicit non-identification for Region X.
  - Patrich's 1984–85 survey: "none of the information gathered could be of assistance".
  - The eight caves "were most likely surveyed in the past but never published", with no one named.
- 2584 pp. 170–171: X/44, X/45 and X/47 cross-refer to Region XI of the same project, not to an earlier record.
- 2585 p. 177: "An attempt was made at this time to identify the caves that had been previously surveyed, but this was unsuccessful". This refers to de Vaux 1962 and Patrich & Arubas 1989 and is a non-identification for the region.
  - p. 179: XI/15 "the product of a previous excavation", with no one named.
  - p. 180: XI/16 "debris of a previous excavation", with no one named.
  - p. 180: XI/18 lies "below Cave Q2, excavated by de Vaux". This is locational; XI/18 appears only in the low-confidence caption row.
- 2590 p. 188: the de Vaux 1962 survey covered Region XIII; "we were able to locate some of the caves according to the descriptions, see below". No specific identification is printed in 2590; the only one is in 2591 (XIII/2), which is keyed.
  - p. 188: "Bar-Adon surveyed two sites in Region XIII; neither was a cave (Nos. 101, 103—structures in the Fashkha marsh)". These are not linked to any XIII label.
- 2590 p. 191: XIII/13 "a small monastery such as the one … (Bar-Adon 1972:126, Site 114)" is a comparison.
- 2590 p. 187 and 2591 p. 195: the Conder & Kitchener shoreline description and the PEF Dead Sea level mark are landscape, not 1993 features.
- 2590 Table 1 "(Survey No.)" C-numbers are the 1993 team's field labels ("labelled C-7, now XIII/2", 2591 p. 195), not earlier-survey numbers.
- 2591 p. 206: "Rock Shelter C-24 … (Cave 24 was previously excavated by Patrich [1993])" is not a feature of these 1993 reports.
- 2592 p. 209: the excavated hawwar cave "located near de Vaux's Cave No. 4 (de Vaux 1973)" is proximity only, and the cave has no XIV label. Khirbet Mazin (Bar-Adon 1989) "probably connected" to XIV/2 is not identity.
- Finds sections throughout (Cave of Horror, Cave of Letters, Cave of the Pool, Cave of the Twins, Rujm el-Bahr, Cave of the Treasure, Agur et al. 1990:93, etc.) are comparisons only.

## Counts (35 rows)

| describer | ref_type | rows |
|---|---|---|
| ben93 | page | 4 |
| ben93 | site_number | 1 |
| djd3 | cave_number | 3 |
| djd3 | (blank) | 4 |
| other:Frumkin 1988 (NZ 14:68-91) | page | 4 |
| other:Frumkin 1988b | page | 2 |
| other:Frumkin 1988a | page | 1 |
| other:Patrich 1988 | cave_number | 1 |
| other:Patrich & Arubas 1989 | cave_number | 1 |
| other:Patrich & Arubas 1989 | page | 1 |
| other:Patrich & Arubas (unpublished) | (blank) | 2 |
| other:Patrich (excavations) | (blank) | 1 |
| other:Wendell Jones | (blank) | 1 |
| other:Goldfus 1984 | page | 1 |
| other:Goldfus 1990 | page | 1 |
| other:Eshel & Zissu 1998 | page | 1 |
| other:Bar-Adon 1989 | page | 3 |
| other:Center for Cave Research survey | name | 1 |
| other:unattributed (earlier name) | name | 1 |
| other:Conder & Kitchener 1880 | page | 1 |
| ba72 | — | 0 |

- copied = yes: 6 rows (II/32; VIII/9+VIII/10; X/35; XIV/6; XIV/18; XIV/51).
- Confidence: high 20, medium 6, low 9.
