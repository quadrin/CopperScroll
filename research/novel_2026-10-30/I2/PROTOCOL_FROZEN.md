# Lane I2 protocol (frozen): three new sources for the lane I test (medieval place names 1100–1600)

Frozen 31 October 2026, before any scroll name or control name was scored against any record of these sources. Never edited after the freeze commit.

## Reopening basis
Lane I (`research/novel_2026-10-30/I/`, protocol SHA-256 `f3d1a1c6b8f8e248c6ab5416b2d193132909d7a3550bdda3dd9d8e3b9977d201`, freeze commit `fd3fbf9`, result commit `01d6cf2`) closed C1, C2 and the tomb sub-test as rejected for the sources read. It named three reopening observations: (a) Kaftor va-Ferach, (b) the Hütteroth–Abdulfattah defter names, (c) Abbot Daniel. All three are now readable. This lane runs them as a new, separately frozen test. Lane I's result and files stay unchanged.

## What is unchanged (lane I frozen protocol, cited by its SHA-256 above)
The following are lane I's, unchanged. The I2 matcher imports lane I's `scripts/medieval_match.py` (SHA-256 `e7f059c75c58283369b548be7ff5cc9429a070a5ee1f5828d6ec77f4ede0cc20`) and reads lane I's `data/name_constraints.json` (`d75b3522a0d1eb3683eea70a51d717ab7713bd8c87379257dcff3d8444ae01f2`) in place:
- claims C1 (26 test names), C2 (non-biblical test names), T (tomb sub-test: ha-Melaḥ, Kippa, Absalom, Zadok, Obed);
- scorer: T01 `toponym.score` with rules R1–R14, H1–H3, A3–A4 (`toponym.py` `dea86acb74a54f3a49fa96066a1044087d295f928b57c30a2ad89a7910399d77`; `sound_rules.csv` `629798de76b8ce91f70a0f394e6e28e5bb2a0624f881c6afc3ef30f5d8489911`; `scroll_names.json` `bfaef21601de684ce7ae5443f600a961e72949f23029b8c3d01f7905146fcf6c`);
- Latin-script rendering rules M1–M9 (`name_skeletons`);
- conjunction: name score ≥ 0.75 AND feature class allowed for the scroll name AND position within (record radius + candidate sigma + 5 km) of a candidate place (`places_v3.csv` `381894a6e383d8f763197048d751bc8c89a5506144b295b3b77d338cc9ad3b9c`, `candidates_v3.csv` `f8d70eb7fda81a8cbbc07bfaa22a8c48785dc423e73e0d989139c717cf51b2a5`), or region code in the name's mapped regions for an unplaced record;
- feature classes and per-name allowed classes; biblical flags; test, known-survival and tomb name lists;
- chance baseline: NRAND = 200 random Hebrew-like cores per variant (T01 `chance.py` construction, `rand_core`), same eligible records, seed 20261030, same seed formula per group;
- statistic, one-sided p = (1 + #random ≥ observed)/(NRAND + 1), pass mark = observed total > random p99 (C1, C2, T);
- positive-control rule: 8 controls (Jericho, Siloam, Bethlehem, Anathoth, Tekoa, Kidron, Gerizim, Beth-Hoglah), area and core from name_constraints.json, feature class ANY, pass = at least 6 of 8 with ≥ 1 conjunctive record; tomb controls (Zechariah, Huldah, Simeon the Just), class TOMB, pass = at least 2 of 3. A control failure closes the test as "not identifiable from available evidence";
- layer rule (primary layer = by_editor false AND year of writing 1100–1600; speaker date, else segment date);
- placement rules 1–3 and lane I's 29 anchors (`anchors.csv` `dbd1bf521c8963ee37776b49e4a96119a693046a130c8e98c25105c460819117`) and distance units;
- meaning of outcomes (obtained / not obtained / partly) and failure condition.

## Additions (fixed before matching)
### (a) Rendering rules for the new scripts (`scripts/medieval_match_i2.py`)
- **HS (Hebrew script).** A name string with a Hebrew letter is mapped to the scorer's record-side alphabet (the alphabet of T01 `lat_tokens`): HS1 strip niqqud; HS2 letter map א dropped, ב b, ג g, ג׳ j, ד d, ד׳ dh, ה h (word-final ה → -eh token, A3), ו w, ז z, ח h, ח׳ kh, ט t, ט׳ dh, י y, כ/ך k, כ׳ kh, ל l, מ/ם m, נ/ן n, ס s, ע ʿ, ע׳ gh, פ/ף f, צ/ץ s, צ׳ dh, ק k, ר r, ש sh, ת t, ת׳ th; HS3 Hebrew generic words removed (list in the script), every remaining word and the whole phrase compared (as M2); HS4 variants without the article ה- and without Arabic אל-; HS5 adjacent identical tokens collapsed (A4); HS6 the extractor's Latin `translit` field is not scored; HS7 a single non-initial ו or י is a vowel letter and is dropped (as lat_tokens drops Latin vowels), a doubled וו/יי is the consonant.
- **K1 (Khitrowo OCR).** Each Latin string is also scored with every "f" before a letter read as "s" (long s of the 1889 print).
- **D1 (Hütteroth DMG transliteration).** š→sh, ġ→gh, ḫ→kh, ṯ→th, ḏ→dh, ž→j, OCR "$"→sh, OCR "7", "*", "£", "#", "®" before a word-initial letter → ʿayn; digits and other noise removed; DMG generic words removed (Ḫirbat, Mazraʿa(t), Kafr, Fawqā, Taḥtā, Qibliyya, etc.; list in the script). Then lane I M1–M9.
- **T1.** Tomb sub-test and tomb controls use the Jewish source of this layer, Kaftor va-Ferach (seg `kaftor`). Lane I used Adler/Carmoly/Benjamin.

### (b) Inputs (SHA-256)
| Input | Path | SHA-256 |
|---|---|---|
| Kaftor va-Ferach, Luncz 1897 (HebrewBooks 32811), text layer, 7 jsonl files | `blind_extraction/source_text_sha256.txt` | per file there (pages 1–418 complete) |
| Hütteroth & Abdulfattah 1977, text layer, 2 jsonl files (PDF pp. 1–229; pp. 230–242 = legend, bibliography, back matter, not downloaded) | same | per file there |
| Khitrowo 1889 OCR (archive.org itinrairesrusse00khitgoog) | `khitrowo1889.txt` | 690b940912ace61eb2896074e9728a72d83ac0bb831cb1a9c83aa754caf1b045 |
| Passage selector | `blind_extraction/select_passages_i2.py` | 3c6f8686849d7d909067fc70eab9006baf215dac4b22ad8a4ede292c879d099b |
| Selection manifest | `data/selection_manifest_i2.json` | 8c8b8c50a54aee3bac8feff55cae2b99db9c76433f2f0cde7ca4ec80d6be09df |
| Extractor instructions (byte copy of lane I) | `blind_extraction/extractor_instructions.txt` | 37ca6edc9a24034dce5db27de00e48c874875d9f58f9ded2f8de44ffe9b14bd3 |
| Source addenda | `blind_extraction/addendum_hebrew.txt`, `addendum_french.txt`, `addendum_hutt.txt` | aa4b223492c637fa3fc41ed9315be3cc2fb4bea7509474553c881cf1b7ededcf; c0483e839ea66e2ddcbbd9e60514912395cc7d88216348f8ec8a62a442f8bf1c; cb3a9cbda1d9d762b7a513d2ae8e48afd8a26e9ae2c6294ff6a88ac072d349f7 |
| Extractor runner | `blind_extraction/run_extract_i2.sh` | 2cd481b461f156897c6f390610f6e3bf21c68d3885df532852514a43baa40cec |
| Extractor input / output hashes | `blind_extraction/extractor_inputs_sha256.txt`, `extractor_outputs_sha256.txt` | d2b648f95702a8ebec372fefaff2b9355f462c27e8dd2617f620204e46bc6cb1; 8ecb8df541691e68c2c668f19adc623880ba35a576b7a65ca0e335302d7d3222 |
| Self-report check | `blind_extraction/self_report_check.md` | 583731094b66cafcf70496b4b844e288aa5c9285c61ed572ef153008da644c68 |
| Hütteroth gazetteer parser | `scripts/parse_hutteroth.py` | ca39efd6364dc569c11d065ab9d3b31752541f6abfab934c4829d47f82d2565e |
| Parsed gazetteer (liwāʾ Quds, Nāblus, ʿAjlūn: 599 entries; facts only) | `data/hutteroth_gazetteer_parsed.csv` | 50fb8be7046854ad33b5d9092ff3bbdf1ad7229e846d46e79fe7aa67e53b4704 |
| Record collector | `scripts/collect_records_i2.py` | ba1e7a6d545f41cb9f6d5098f9e59c0ea34e550419796f82151e9c295e204634 |
| Records, unredacted (not committed: holds short Hütteroth phrases) | scratchpad `records_i2_full.csv` | c9a06774413c47def70e87cb35571a9aa03f48acb07f1f8e16d7b54e09140234 |
| Placement script | `scripts/place_records_i2.py` | d85b24b8bf1d47c4fac27de200828da22911173392f26399a26a5ad2b60a0f2d |
| Hebrew-script anchor forms (same 29 anchors) | `data/anchors_hebrew.csv` | d18f9f2ac2615ea755d502ede3821ab4d9d030b7bad480788500e1168120b250 |
| French/Russian-pilgrim anchor spellings (same 29 anchors) | `data/anchors_extra_latin.csv` | be2c60b1fdb3af8fa7b42d43a65e1df9334f5d87e5cadd5b1c963feb35f59566 |
| Placed records (matcher input; Hütteroth running-text phrases redacted) | `data/records_i2_placed.csv` | bd7f9205108c5a67c16374cd78f342dd757e5acec1578893e3e872f095cc601a |
| I2 matcher | `scripts/medieval_match_i2.py` | 1ab310cc993e074a041eb6c760bc0cde6e2a3b3e01578fd952c1bb2f3458bcf3 |

Placement additions (in `place_records_i2.py`): Hütteroth grid E/N km × 1000 = EPSG:28191 → EPSG:4326 (pyproj; repo convention), radius 1.0 km (0.5 km print resolution + 0.5 km for the authors' identification); Hebrew and French anchor spellings for the same 29 anchors (same coordinates and sigma); units verst 1.07 km, Hebrew mil 1.5 km, parsa 5 km, day 30 km, hour 4 km. Gazetteer units are records only with a grid position inside the region boxes stated in the script (JER ≤ 6 km from the Ḥaram; JJV; DES incl. the Bethlehem–Tekoa edge; GER ≤ 10 km from Nablus; PER east of the lower Jordan); tribes are not records. Gazetteer year = 1596 (primary layer).

Records (all / primary layer): Kaftor 100 / 88; Khitrowo 555 / 538; Hütteroth 100 / 92 (gazetteer 57, chapters I–V 35). Total 755 / 718.

### (c) Expected positive controls (stated before matching)
The pass rule is lane I's, applied to the pooled layer: at least 6 of the 8 lane I controls found. Expected sources per control (descriptive prediction, not a pass condition):
- Jericho: Kaftor, Daniel and the later Russian pilgrims, Hütteroth (Arīḥā, liwāʾ Quds).
- Siloam: Daniel/Russian pilgrims (Siloé); Hütteroth (Silwān) if the unit has a grid position.
- Bethlehem: Russian pilgrims; Hütteroth (Bayt Laḥm); Kaftor.
- Anathoth: Hütteroth (ʿAnātā); possibly Kaftor.
- Tekoa: Hütteroth (Tuquʿ); possibly Daniel.
- Kidron: Russian pilgrims (Cedron / Josaphat is not Kidron by name); Kaftor (קדרון, 1 occurrence in the text).
- Gerizim: Kaftor (גריזים, 7 occurrences); Russian pilgrims less likely.
- Beth-Hoglah: uncertain (Kaftor or Hütteroth Ḥajla only if named).
Tomb controls (Kaftor only, class TOMB, pass at least 2 of 3): weak expectation. Kaftor is not a tomb list, and only 5 Kaftor records are eligible for each tomb control. If the tomb controls fail, the tomb sub-test closes as not identifiable (lane I rule).

### (d) Layers
Primary: the three sources pooled (C1, C2, T, controls). Descriptive only: the same statistics per source (kaftor, khitrowo, hutteroth), with the same random cores restricted to that source's records. A per-source result cannot pass or fail the test.

## Coverage (fixed before matching)
- Kaftor: PDF pp. 1–41 (Luncz's 1897 front matter) not read; chapter 11 (the geography chapter, PDF pp. 288–354) read in full; elsewhere ±100-word windows around Hebrew region keywords (332 hits, 110 passages in all).
- Khitrowo: Daniel (1106–1107), Ignace of Smolensk (1389–1405), Grethenios (c. 1400), Epiphane (c. 1416), Zosime (1419–1421), Basile (1465–1466), Clément and Grégoire (1500–1547), Sophronius (1547), Basile Posniakov (1558–1561) read in full. Not read (Constantinople or Athos only): Antoine of Novgorod (c. 1200), Étienne of Novgorod (c. 1350), the scribe Alexandre (1393), anonymous Description of Constantinople (1424–1453), Isaïe (1489), Païssius (1550).
- Hütteroth: gazetteer of liwāʾ Quds (book pp. 112–124), Nāblus (125–141), ʿAjlūn incl. nāḥiyas Salṭ and Jibāl Karak (162–174) parsed by script; liwāʾ Ġazza, Lajjūn, Ṣafad and qaḍāʾ Ḥawrān not read (outside the five regions). Chapters I–V: ±150-word windows around English region keywords (174 hits, 32 passages). PDF pp. 230–242 not downloaded.

## Exposure log (before the freeze)
I read the contents pages, running heads and page structure of the three sources, one Kaftor page of chapter 11 (to check the OCR), the Hütteroth abbreviation key and the first gazetteer page. I looked at extractor outputs only for structure (counts per chunk, malformed lines, non-JSON text) and at placement counts. I ran the I2 matcher with `--dry` once: it prints the number of eligible records per group and per source; it scores no name. I checked the HS and D1 rendering on eight sample place strings (Jerusalem, Bethlehem, Jericho, ʿAin es-Sulṭān and similar) and fixed three defects found there (vowel letters HS7, the Hebrew generic list, and the DMG apostrophe in the generic-word test). No scroll name or control core was scored before the freeze. The DES region box was widened (E 175 → 166) to include the Bethlehem–Tekoa edge named in lane I's DES definition, before matching.
