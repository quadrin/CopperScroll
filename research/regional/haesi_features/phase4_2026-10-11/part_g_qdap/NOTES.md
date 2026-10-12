# Phase 4, part G (QDAP): working notes

Worker notes for the integrator. Counts are in `summary.md`; this file records access, choices, gaps and proposed changes.

## Start checks

- `python3 -I research/preregistration/arrivals/arrival.py check` was run once at the start: `manifest: ok (29 files)`.
- The frozen phase-4 plan (sha256 `5428c4cc…b2da`, commit b002e03) and the phase-2 plan (sha256 `5b1a5c08…b3be`) are checked by the tests.
- `research/preregistration/arrivals/items/*` and `research/assessments/kohlit_chain/chain.json` were not opened. ʿAtiqot 41, Kochavi 1972, the L-656 file and the IAA Archive cave records were not sought.

## What was read

- Source: archive.org collection `pub_quarterly-department-of-antiquities-palestine`, 45 items (issues, double issues, volume indexes, the vol. 9 supplement and two whole-volume items, vols 7 and 14).
- Files: for each item, `<id>_hocr_searchtext.txt.gz` with `<id>_hocr_pageindex.json.gz` gave the text per leaf. `<id>_djvu.txt` was fetched as a check. Where the searchtext was refused, `<id>_djvu.xml` was used (1934_4_1-2). All downloads stayed in the scratch folder. 219 requests were logged (167 HTTP 200, 52 HTTP 500, counting retries), at least 3 s apart.
- Printed pages: the archive.org `_page_numbers.json` files were off by one leaf in the items checked, so they were not used. Printed pages come from the running page numbers in the OCR, taken as the longest increasing chain and interpolated between chain points. Unit ids, `pages` and quotes use these printed pages.
- Screened: every article title in the contents and running heads, and every site paragraph of the annual round-ups ("Excavations in Palestine …", "Other Discoveries …") and the Notes lists. 346 screen rows in all.
- Read: 71 in-region units, in tier order T1 (20), T2 (42), T3 (9). Within each tier the order is ascending sha256 of the unit id (`screen.csv`, `order_position_in_tier`). The stop rule was not needed; nothing is `not read (time limit)`.
- Reading method: short units were read in full. Long units (Mefjer series, North Wall, Citadel 1950, the abbey of St Mary, the Nativity papers and some others) were read with their opening pages in full plus every paragraph that holds an eligible-class keyword. The `reading` field of each record in `data/units/` says which. The text hash always covers the whole span, so an unread paragraph inside a span is still fixed by the hash.

## Deviations and choices (exploratory)

- **D1 (held text displayed).** The paragraph-start screen of the 1934-5 round-up showed the first seven or so words of each OCR paragraph on pp. 199–201 of the held Jericho unit (QDAP5-199-jericho; leaf lines 151.10–153.9). One fragment was "area was selected in the north-east corner". The same screen showed "(1) The tombs. Further Bronze Age tombs were" in the held 1932-3 Jericho unit (QDAP3-176). I stopped at that point. Nothing was coded from these lines. The unit stays citation only with `protected_strip = yes`.
- **Tell es-Sultan held by precaution.** The three Tell es-Sultan units and the Baramki synagogue "near Tell es Sultan" (QDAP 6, pp. 73–77) are held. From the heading alone I could not rule out the north strip. The one-line 1931 Notes entry (QDAP 1, p. 52) names the excavation and nothing else; it is listed with `protected_strip = no`.
- **No held cave-area caves met.** Qumran, Qarantal, Nuweiʿimeh and Qilt appear only in Avi-Yonah's "Map of Roman Palestine" (QDAP 5, pp. 139–193). That item is a gazetteer, coded NOT_FIELD and not read.
- **Spelling variants (screen S-MAN).** The gazetteer missed Mandate spellings, so I added by eye: Mefjer/Mafjar, ʿEin el Fawwar, Qalandia, ʿAin Karim, Tell en Nasbeh, Tyropoeon, Holy Sepulchre, Nativity, ʿEin Hanniya, Khureitun, and the OCR form "Tell el Fal". 23 of 71 units entered this way. The list is a choice made while reading.
- **Tell en-Nasbeh** is not a gazetteer place. It is placed in Z4 from its known position north of Jerusalem (INFERENCE).
- **Name-only zones follow the gazetteer.** No in-region unit gives a Palestine Grid reference (only Transjordan units do, e.g. Meqabelein "146.236"). All rows are placed by name only, with no coordinates and no distances. Umm Qatafa and Khareitun go to Z3 because the gazetteer puts them there.
- **NOT_FIELD.** Bibliographies, museum and coin catalogues, inscriptions and text editions, object studies, the "Mosaic Pavements in Palestine" lists and the "Map of Roman Palestine" are not field reports and were not read.
- **Stepped tanks.** The stepped tanks at Qalandia and in the Citadel are coded `ritual_bath`, with the excavator's own label kept in `feature_subtype`. Neither excavator calls them a miqveh; the class choice is INFERENCE from form.
- **ʿAin Karim.** The stepped rock-cut chamber with Herodian pottery (QDAP 11, pp. 113–115) is coded `cave_with_finds`, window yes. The function is not given.
- **Late hoard check.** After the tiers were done I checked the hoard articles once more. "A Hoard of Tyrian and Jewish Shekels" (Reifenberg, QDAP 11, pp. 83–85) names its findspot as "at or near Silwan", on a dealer's word. It was added as QDAP11-083 (S-MAN, T2) and read last, after the T3 units. It sits at its sha256 position in `screen.csv`, but in fact it was read out of order. Its location confidence is low. "A Hoard of Coins of the Constantinian Period" (QDAP 2) gives only "Northern Palestine" and is OUT_TITLE.
- **Edge cases left out of the region (to decide):** Kh. ʿAsida near Beit ʿUmmar; Tuleilat Ghassul (east of the Jordan, near the Z2 box edge); Tell el Farʿa and the Talluza find; Beitin; et-Tell; ʿAin el Jedide. All are OUT_REGION in `screen.csv` with the reason given.
- **No deduplication by campaign.** Same-site units are kept separate: the Mefjer series, Abu Ghosh (2), the Citadel (4), Tell en-Nasbeh (2), ʿIrq el Ahmar (2), ʿIsawiya (2), Damascus Gate (2), and the abbey of St Mary reported twice.

## Not read, and why

- **Vol. 6, nos. 3–4 (1937).** Every OCR file of the archive.org item was refused with HTTP 500 on three attempts. The vol. 6 index names four in-region units there, recorded as NO_TEXT: "Excavations at Khirbet el Mefjer (II)" (p. 157), "Note on Recent Discoveries outside St. Stephen's Gate, Jerusalem", the round-up "Excavations in Palestine, 1935-6", and the issue as a whole. The ʿAtlit and Ras el ʿAin articles of that issue are out of region.
- **Vol. 10, nos. 2–3.** Not on archive.org (items 1940_10_1 and 1942_10_4 only).
- **Vol. 7.** The brief said most of vol. 7 is missing. Item `quarterly-department-of-antiquities-palestine_1938_7` in fact holds the volume: contents, text pp. 1–67 with plates and the index. All of its 27 units were screened. Only the text of G. Hill, "The Autonomous Shekels of Tyre" (a coin study, NOT_FIELD), was not found in the item.
- **Index items.** 1932_1_index, 1934_3_index and 1945_11_index were partly refused (HTTP 500). They hold no units. The issue contents and running heads were used instead.

## Blocked (exact URLs, last attempt 12 Oct 2026 UTC)

All of these returned HTTP 500 (an Internet Archive server error, 170-byte body).

- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1937_6_3-4/quarterly-department-of-antiquities-palestine_1937_6_3-4_djvu.txt`
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1937_6_3-4/quarterly-department-of-antiquities-palestine_1937_6_3-4_hocr_searchtext.txt.gz`
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1937_6_3-4/quarterly-department-of-antiquities-palestine_1937_6_3-4_hocr_pageindex.json.gz`
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1937_6_3-4/quarterly-department-of-antiquities-palestine_1937_6_3-4_djvu.xml` (also no usable file)
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1944_11_1-2/quarterly-department-of-antiquities-palestine_1944_11_1-2_djvu.txt` (the searchtext was obtained on a later retry and used)
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1934_4_1-2/quarterly-department-of-antiquities-palestine_1934_4_1-2_hocr_searchtext.txt.gz` (the DjVu XML was used instead)
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1932_1_index/quarterly-department-of-antiquities-palestine_1932_1_index_hocr_searchtext.txt.gz` and `…_hocr_pageindex.json.gz`
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1934_3_index/quarterly-department-of-antiquities-palestine_1934_3_index_hocr_searchtext.txt.gz`
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1945_11_index/quarterly-department-of-antiquities-palestine_1945_11_index_hocr_pageindex.json.gz`

The British Library record page `https://eap.bl.uk/archive-file/EAP1544-1-1-54` returned HTTP 202 with an empty body. The IIIF manifests at `<record>/manifest` opened (HTTP 200 for -54 to -79).

## British Library EAP1544 (page images; not OCRed in this pass)

These are the manifest labels and canvas counts. The volume mapping for the unlabelled records is a guess from canvas counts and order, and has not been checked against the images.

| record | label | canvases | could fill |
|---|---|---|---|
| EAP1544-1-1-54 | QDAP 1931-32 | 318 | nothing new (vol. 1 is complete on archive.org) |
| -57 | QDAP 1932-33 | 288 | nothing new |
| -58 | QDAP 1933-34 | 310 | nothing new |
| -59 | QDAP 1934-35 | 380 | a check of vol. 4 nos. 1–2 (searchtext refused) |
| -60 | QDAP 1935-36 | 428 | nothing new |
| -63 | unlabelled | 412 | probably vol. 6: **nos. 3–4 (Mefjer II, St Stephen's Gate note, 1935-6 round-up)** |
| -64 | unlabelled | 234 | probably vol. 7 (the Hill article) |
| -65 | unlabelled | 352 | probably vol. 8 |
| -67 | QDAP 1940 | 140 | vol. 9 or 10 part |
| -69 | unlabelled | 338 | probably vol. 10: **nos. 2–3** |
| -71, -72, -76, -79 | unlabelled | 292, 168, 248, 286 | later volumes (11–14), already on archive.org |

Records -55 (Garstang, Jericho reports), -56 (Nineveh), -61 (scarab catalogue), -62 (Denkmäler), -66 and -70 (PAM gallery books), -68 (Teleilat Ghassul), -73 (Mosquée de Médine), -74, -75 (Syria XXIII), -77 and -78 are not QDAP. Record -55 (Garstang's Jericho reports) would fall under the Tell es-Sultan rule.

## Figures worth archiving later (not stored)

Printed page and figure as cited in the text. The captions themselves are on plate leaves and were not checked.

- QDAP 1, pp. 3–5, Karm al-Shaikh cemetery: Fig. 1 (site plan with tomb positions), Fig. 2 (tomb plan).
- QDAP 2, p. 107, Qalandia bath: Pl. XL (plan).
- QDAP 4, Government House cistern (p. 165 ff.): Fig. 1 (plan and sections); Pl. LXXVIII.
- QDAP 4, pp. 70–80, YMCA cemeteries: plan (cited in the record).
- QDAP 5, p. 1, Mahneh Yehudah column: Fig. 1 (section of the quarry bed).
- QDAP 5, pp. 75–79, Nativity, earlier church: Pl. XXXVI (general plan), Pls. XLI ff.
- QDAP 5, p. 136, Kh. el Mefjer: Pls. LXXVI, LXXXIII, LXXXV and plan.
- QDAP 6, p. 56, monastery outside the Third Wall: Fig. 1 (plan).
- QDAP 6, pp. 63–69, Nativity: Fig. 1 (plan), Fig. 2 (section).
- QDAP 8, pp. 117–136, abbey of St Mary of Jehoshaphat: Pl. I (copy of a 12th-century plan), Fig. 2 (plan), Fig. 6 (elevation).
- QDAP 9, p. 207, Jerusalem Citadel: plan and Pl. LVIII.
- QDAP 10, pp. 1–50, North Wall: Fig. 1 (general plan of soundings), Figs 3, 4, 13, 17–19, 21 (sections and elevations).
- QDAP 11, pp. 51–59, Mafjar sculpture I: Fig. 1; Pl. XVI.
- QDAP 11, p. 114, ʿAin Karim: map figure. QDAP 12, p. 104, Abu Ghosh: map figure. QDAP 5, p. 195, ʿAnata: map figure.
- QDAP 13, p. 3, Mafjar balustrades: Fig. 2 (plan).
- QDAP 14, p. 120, Kh. al-Mafjar: Fig. 1 (plan of the whole site as excavated).
- QDAP 14, pp. 121–186, Citadel 1950: Fig. 23 (site plan), Figs 3–5, 11, 12, 15, 19, 21, 24–31, 34, 35 (plans, sections, period maps); Pls. LV, LVI, LXI (plan of 1865).

## Proposed changes for the integrator

1. Merge `reports.csv`, `features.csv`, `screen.csv` and `held.csv` into the phase-4 tables. Columns match phase 2.
2. Add the four held Tell es-Sultan items (`held.csv`) to the arrival register, with deviation D1 noted.
3. Record the Kh. ʿAlmit extraction (`tier1_kh_almit_extraction.md`): two passing mentions in Avi-Yonah's map gazetteer (QDAP 5, pp. 147 and 189). No field report.
4. Add vol. 6 nos. 3–4 and vol. 10 nos. 2–3 to the source requests: EAP1544-1-1-63 and -69 (page images), or the owner's library. Mefjer II (QDAP 6, p. 157) and the 1935-6 round-up are the in-region items at stake.
5. Deduplicate by campaign when merging (Mefjer, Citadel, Nasbeh, Abu Ghosh, ʿIrq el Ahmar, ʿIsawiya, Damascus Gate, St Mary).
6. Decide the edge cases above, and whether the S-MAN spelling list should go into the gazetteer patterns for later parts.
7. Correct the phase-4 plan note that "most of vol. 7" is missing on archive.org: item 1938_7 holds the volume.
