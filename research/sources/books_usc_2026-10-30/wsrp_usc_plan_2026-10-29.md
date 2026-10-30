# WSRP 1988 Copper Scroll photographs: processing pipeline and reading plan (29 Oct 2026)

Source: WSRP 1988, private study copy (93 TIFFs, 28.6–58.4 MB, supplied by USC/WSRP to the owner; held in the owner's private Drive). The 4.5 GB zip is not used. **No image, crop, preview or figure from this delivery is in this repository**: the owner undertook to USC that the images would not be published. Frames are cited by file name (for example DSS_3Q15_CT6_RCB_T). Repo baseline: `main` 36d8d18 (read only).

## 1. What the files are (established before any pixel was read)

- **Every Drive file matches a USC Digital Library record by exact byte size.** All 93 file sizes equal the "Archival File Size" of a `3Q15 Cut n … color` record in `research/sources/usc_copper_scroll_images/index.csv`. In all 93 cases the catalogue cut number equals the CT number. They are the 1988 colour-transparency drum scans by Bruce and Kenneth Zuckerman, catalogued at 1200 ppi from 4 × 5 in film. All are **recto**: no versos and no b&w negatives were delivered.
- **The suffixes name the light, not a tile.** The catalogue descriptions of the cut 5 and cut 7 frames show the whole segment upright in each portrait frame, with a grey scale and colour strip. So each of the 2–9 frames of a segment is the same strip under a different light. The table gives the inferred meanings (WSRP has not confirmed them):

| Code | Catalogue title | Code | Catalogue title |
|---|---|---|---|
| RLT / RCT / RRT | recto, left / centre / right top light | RT / RB | recto, top / bottom light (CT4, CT17, CT21) |
| RLB / RCB / RRB | recto, left / centre / right bottom light | RET / REB | recto, edge top / bottom light (CT16) |
| FRS | recto, fragments (CT10: probably AWS 22, the seven loose fragments from cut 10's lower right edge) | RFR | recto, "frgs" (CT16) |
| RCS | recto, centre side light (CT23) | RBC / RTC | recto, bottom centre / top centre (CT23) |

  One anomaly: the catalogue titles both CT19_RCT and CT19_RCB "ctr top light". This is metadata only; nothing was opened.
- **Frames per segment:** CT2 4, CT3 6, CT4 2, CT5 6, CT6 6, CT7 6, CT8 6, CT10 7, CT11 6, CT16 9, CT17 2, CT18 6 (66 open). CT19 6, CT20 6, CT21 2, CT22 6, CT23 7 (27 held).
- **Absent from this delivery but catalogued at USC as 1988 colour recto:** cut 1 (1 frame), 9 (6), 12 (6), 13 (4), 14 (4) and 15 (8). Also absent are 25 colour versos and all 147 b&w negatives. So segments 1, 9 and 12–15 *were* photographed; the masters were simply not sent.

### Is CTn = segment n?

- **CTn = USC "Cut n": certain.** All 93 byte sizes are identical.
- **USC "Cut n" = the DJD III / Puech segment n: high, about 90%, not verified.** Three things agree:
  1. The repo's column → segment map (`research/text/letter_controls/controls_manifest.csv`, taken from Puech 2006's radiograph captions) is identical to the map in the brief: I = 1–4, II = 5–6, III = 7–8, IV = 9–10, V = 10–11, VI = 11–12, VII = 13–14, VIII = 15, IX = 16–17, X = 17–18.
  2. Reed's DSS Inventory gives AWS 21 = cut 10 and AWS 23 = cut 11 for the column V photographs, matching DJD III pl. LVII ("cuts 10*–11").
  3. The 6 Oct original-photo audit found cut 13–14 views compatible with the column VII assembly.

  Against: the same audit records unverified "cut 17/18 and later 19/20" proposals for IX 7, and says no shared cut-to-column map has been assigned.
- **Which segment holds a given word within a column: low–medium.** It is inferred only from the word's character position along the line (ETCBC text, `data/scroll-text.js`) and the right-to-left order (the lowest segment number carries line starts). Segment widths are unequal. Per the letter-controls protocol, each line must be registered from its neighbouring Hebrew on the previews before any reading counts.

## 2. Pipeline (`wsrp_previews.py` + `WSRP previews runner.ipynb`)

The preview script and its Colab runner are in the owner's private Drive (WSRP previews 2026-10-29); they are not in this repository, because their outputs are image derivatives.

It follows the house style of `hexcolab.py`: Colab mounts Drive, the work runs one file at a time on Google's servers, and the run can be restarted.

- **CT2–CT18 (66 files).**
  1. Stream from Drive to Colab's local disk in 16 MB chunks while hashing (sha256).
  2. Read the first-page TIFF tags: width/height, bits per sample, samples, dtype, photometric, compression, planar config, orientation, X/Y resolution, unit, dpi and implied print size, ImageDescription, Software, DateTime, Make, Model, Artist, Copyright, HostComputer, DocumentName, ICC profile description, XMP (first 4,000 characters), plus every tag in `all_tags`.
  3. Make a 4 × 4 block-mean **1/4-scale JPEG** (`previews_q4/<name>_q4.jpg`, q90) and a 1/16 **contact JPEG** (`contact_q16/<name>_q16.jpg`). The reduction is row-chunked from a memmap (with imread fallback), uses no rotation and no contrast change, and scales 16-bit to 8-bit linearly.
  4. Delete the local copy.
  5. At the end, write one labelled contact sheet per segment (`contact_sheets/CTnn_contact.jpg`).
- **CT19–CT23 (27 files) and any file name without a readable CT number:** the bytes are read from Drive only to compute the sha256. They are never written to disk, never parsed as TIFF and never decoded. A second guard in `make_previews` refuses any held name.
- **Records.**
  - `manifest.json` is rewritten atomically after every file. It holds per-file status, bytes, sha256, the expected bytes, the matched USC title and UC identifier, the inferred suffix meaning, tags, preview names and pixel sizes, and seconds taken.
  - It also lists missing and unexpected files, the script's sha256 and the library versions.
  - `run_log.txt` gets one line per file.
  - Errors are logged and the file is skipped. Files marked `ok` or `held_hash_only` are skipped on a rerun; `--redo` forces a fresh run.
- **Tested locally** on synthetic files (16-bit RGB, deflate RGB, greyscale, planar RGB, a corrupt TIFF, a non-TIFF named CT19, a real TIFF named CT21 and an unparsable name):
  - Open files produced their tags and previews.
  - The corrupt file was logged as an error and skipped.
  - Both held files and the bad name were hashed only, and the hash matched.
  - A rerun skipped finished files.
- **Expected run result:** `ok: 66, held_hash_only: 27`, about 70 MB of previews. Every output is under 10 MB, so the previews can be pulled into a later session with the Drive connector.

## 3. Reading plan

Lines per column (text shown): I 15, II 15, III 13, IV 14, V 14, VI 14, VII 16, VIII 16, IX 17, X 17. The "position" column gives the word's span as a fraction of the line from its start (right edge) and the line's height on the strip. The second figure assumes the strip stands upright, column top at the top of the frame; confirm this on the previews.

**Status key:**
- **OPEN** – the segment is in this delivery.
- **ABSENT** – the segment exists at USC but is not in this delivery.
- **HELD** – CT19–CT23; must not be opened.

### Entries whose `decisive_next` names the WSRP masters

| Entry | Line | What must be decided (letters) | Competing readings | Segment(s) and position | Status |
|---|---|---|---|---|---|
| 4 (Tell es-Sultan) | I 12 | The letter(s) before ק in the immersion word: one closed letter (מ) or a short נ + י. Rounds 2 and 3: cannot decide. | ניקרת "cleft" (Milik; Wolters, Schiffman); נקרת (Eshel 2002); מקרת "frigidarium" (Puech 2006); Lefkovits 2010 hesitates between mqdt and mqrt. Also Puech 2015 restores a ה in a lacuna on this line. | Column I = CT1–4. Word at 0.41–0.59 of the line, so probably CT2 or CT3 (CT4 if the outer segments are narrow). Line 12/15, about 0.8 down. | **OPEN** (CT2 ×4, CT3 ×6, CT4 RT/RB). CT1 is absent, but it carries line starts only. |
| 7 (Temple enclosure) | II 3 (and II 4) | In the house word, the 1st letter ה/ח and the 3rd ד/ר. The 4th already leans to ה (one source). Secondary: II 4 line end, Θ against Ξ in ΘΕ. | המדה (Puech 2006/2015); המרה (Milik 1962); המדח (Wolters; text shown); חמדה (Lefkovits 2000, who says each letter is ambiguous). ΘΕ (Milik, Puech, Lefkovits) against ΞΕ = 65 (Ullendorff, Muchowski). | Column II = CT5–6. Word at 0.40–0.56, near the CT5/CT6 boundary; check both. ΘΕ at the end of II 4 (0.93–1.00), so CT6. Line 3/15, about 0.2 down. | **OPEN** (CT5 ×6, CT6 ×6) |
| 12 (Temple enclosure) | III 1 | Whether *any* trace survives in the 6–9-letter gap after בח, and which letter stands at the gap's left edge (ב/ל against ט/ע/מ). Rounds 2 and 3: metal missing, no traces. | בחצ[ר ש(ל) ]דיאט(?) (Puech 2006); בח[צר נב]ט (Lefkovits 2000); peribolos, no letters (Milik 1962); the text shown leaves ◦◦◦. | Column III = CT7–8. Gap about 0.18–0.40, so CT7. Top line. | **OPEN** (CT7 ×6). Low expectation: `decisive_next` says no reproduction can supply the name. |
| 13 (Temple enclosure) | III 8 | In the place word after שבמל: ה or ח, and is there a closed final ם after it? Rounds 2 and 3 split. | שבמלה "embankment" (Puech 2015); Millo/Esplanade (Puech 2006; Milik 1962); "salt" (Puech 2002); מלח, the place Melaḥ; the text shown has שבמלחמ. | Column III = CT7–8. Word at 0.28–0.61, near the CT7/CT8 boundary; check both. Line 8/13, about 0.6 down. | **OPEN** (CT7 ×6, CT8 ×6) |
| 14 (Temple enclosure) | III 11 (plus III 12–13) | (a) The same ה/ח + ם question at III 11 (0.28–0.61, under a blister). (b) The cover word split across lines: is the end of III 12 + the start of III 13 המ\|ת or a form of מדף? (c) The sum in III 13: 13 or 14. | (a) as entry 13. (b) המת "the dead" (Milik 1960, Lefkovits; text shown) against מדף "slab" (Milik 1962 DJD, Puech 2006) and "the trap" (Puech 2015). (c) 13 (Milik, Lefkovits) against 14 (Puech 2006). | (a) CT7/CT8, line 11/13. (b) End of III 12 (0.88–1.00), so CT8. Start of III 13 (0.00–0.07), so CT7. (c) Numerals at 0.79–0.93 of III 13, so CT8. Bottom of the strip. | **OPEN** (CT7, CT8) |
| 32 (Wadi el-Qelt, Choziba) | VII 14–15 (and VII 16) | 2nd letter of הכוז\|בא: כ or ב. Rounds 1 and 4: a square base with no projecting stroke. Secondary: הטור/הסור at the end of VII 15; the numeral count (60/80) in VII 16. | הכוזבא Koziba (Milik, Puech, Allegro final, Eshel); הבוזבא "of Buz" (Lefkovits); hbybʾ (early Allegro). טור (Milik, Puech) against הסור (Eshel) and ṭyp (Allegro). 80 (Puech) against 60 (Milik, Lefkovits). | Column VII = CT13–14. הכוז ends VII 14 (0.83–1.00), so CT14. בא opens VII 15, so CT13. Lines 14–16 of 16, the bottom of the strip. | **ABSENT** (CT13 and CT14 both missing; USC holds 4 + 4 colour recto frames) |
| 37 (Valley of Shaveh) | VIII 14 | The first word (letters 2–4: ר/ד, ו/י, י/ר/ן) and the letter after בצ in the chamber word (ו or ר). Round 2: ו possible for both readers. The line crosses a strip seam. | ברוי "irrigated land" (Milik, Puech 2015); בדין (Lefkovits 2000); בדור (Beyer; text shown). The engraved בצויח against Puech 2015's correction בצריח "chamber"; cippus (Milik 1962). | Column VIII = CT15 only. First word at 0.00–0.12, chamber word at 0.39–0.55. Line 14/16, bottom. The seam means one end may sit on CT14 (absent) or CT16 (open), but the disputed words are probably on CT15. | **ABSENT** (CT15; USC holds 8 colour recto frames, including edge-light views) |
| 41 (unplaced) | IX 10 | In בקומעה: the first letter after ב (ק?), the extra vertical between ו and the box (ו/ז), and the box itself (מ against ב). Round 2 leans to מ; round 3 cannot decide. | קומעה "hole" (Puech 2015; Høgenhaven 2020); Qovaʿ, a place name (Lefkovits 2000); Qobʿeh, a place name by emendation (Milik 1962). Entry boundaries also disputed (Luria, Beyer, Lefkovits). | Column IX = CT16–17. Word at 0.00–0.33, so CT16. Line 10/17, about 0.6 down. | **OPEN** (CT16 ×9, including RET/REB edge light) |
| 53 | XI 8 | — not read (exposure rule) | — | Column XI = CT19–20 by the brief's map | **HELD CLOSED** |
| 54 | XI 9–11 | — not read | — | Column XI | **HELD CLOSED** |
| 55 | XI 12–15 | — not read | — | Column XI | **HELD CLOSED** |

### Other lines in the owner's 17 Oct request (their `decisive_next` does not name WSRP)

| Entry | Line | Question | Segment and position | Status |
|---|---|---|---|---|
| 21–23 (Qumran) | V 1–9 | V 1–2: the restored link word to Sekakah (smooth lacuna; round 2 found no traces). V 9: word division at the start of the line, שלומ\|ו עד or שלום \| ועד (Q41). | Column V = CT10–11 (AWS 21/23). Line starts, so CT10. The CT10 FRS frame is probably the loose fragments from cut 10's lower right edge (AWS 22). | **OPEN** (CT10 ×7, CT11 ×6) |
| 40 (Ḥoron) | IX 7 | ים "west" (Milik, Lefkovits) against דרום "south" (Puech): are there ד/ר traces in the 1–2 letter-spaces before ו/י + ם, next to the saw cut? | Column IX = CT16–17. The direction word (0.93–1.00) lies beyond the saw cut, so CT17. The gap before it is at CT16's left edge or the CT16/17 cut. Line 7/17. The audit's "19/20 proposal" is unverified; if IX 7 really sat on CT19/20 it would be held, but Puech's map puts it on 16–17. | **OPEN** (CT16 RET/REB, CT17 RT/RB) |
| 49 (Siloam) | X 15–16 | The letter after ש-ל: a cursive waw (שלוח, Siloam: Puech, Milik) against ר (רחיל, Rachel: Lurie, Beyer, Wolters) against Jehu (Lefkovits). | Column X = CT17–18. Word at 0.54–0.83, probably CT18 (the 6 Oct audit's lead came from cut 18 centre views). Line 15/17, bottom. | **OPEN** (CT18 ×6, CT17 ×2) |

### Order of work once the previews exist

1. **Check orientation and registration.** For each open segment, use the `contact_sheets/` file to confirm the strip orientation. Then register the target line from the neighbouring Hebrew; a CT number does not locate a line.
2. **Freeze before reading.** Before any confirmatory reading, record the crop windows and the reading question for I 12, II 3–4, III 1/8/11–13, IX 10 (and IX 7, X 15, V 9) in a frozen note. Blind readers then see crops from all lighting frames of the segment, with letter controls from the same segment and the same lighting.
3. **Use full-resolution crops for reading.** The q4 previews (about 300 ppi of the film) are for locating only. Readings need full-resolution crops, made by a second Colab pass that writes small crops from the CT2–CT18 masters only.
4. **Entries 32 and 37 cannot move on this delivery.** Request CT13–15.

## 4. Request to WSRP

A short note to Bruce Zuckerman was drafted for the owner: thanks for the scans; a request for cuts 1, 9 and 12–15 (especially 13–15, columns VII–VIII); confirmation of the file-name lighting codes and of the cut numbering; and the CT19 RCT/RCB catalogue-title anomaly. The text is not kept here.

## 5. Exposure log (this session)

- **Drive.**
  - Listed the source folder's metadata only (names, sizes, IDs) for all 93 files, including CT19–CT23.
  - Downloaded no content from the source folder or the zip.
  - Downloaded `hexcolab.py` and the HEXAGON runner notebook, plus my own two uploads to verify them.
  - Writes: one folder and two files, nothing else.
- **Repo files read in full or in part:**
  - AGENTS.md.
  - The USC index README.
  - `index.csv`. For cuts 19–23 only the title, lighting, film and size fields were printed. Description fields were printed only for colour recto frames of cuts 5 and 7, to check framing.
  - `ratings.csv`. Full rows only for entries 4, 7, 12, 13, 14, 32, 37, 41 (and `decisive_next` for 21–23, 31, 40, 49). For 53–55 only the entry and line fields.
  - `readings.json` for those entries only.
  - `plate_check.csv` rows filtered to exclude XI/XII.
  - The plate_check.md sections on the original-photo audit, filtered.
  - `translation_en.json` and `scroll-text.js` for columns I–X only.
  - The findings_log entry for 17 Oct.
- **Incidental lines surfaced by `grep`.** These were method, request and exposure statements, with no letter readings and no images:
  - `research/text/xii10_owner_external_ai_exploratory_2026-10-22.md` lines 3 and 37: a method header, and an exposure note that the owner's screenshot showed part of a segment 21–23 frame.
  - `research/text/letter_controls/PROTOCOL.md` lines 36 and 75–76: "Column XII contains the 21/22 cut"; "At XII 10 the context does not decide between R1–R7".
  - ACTIVE_TEST lines 25, 39 and 55: pending requests that mention XII 10.
  - The plate_check.md line on unverified "19/20 proposals" for IX 7.
- **Not opened:** `research/preregistration/` (excluded from every search), any XII 10 commentary file, and any image of columns XI–XII.
- **Repo and Claude project:** not written. The repo was not committed or pushed.
