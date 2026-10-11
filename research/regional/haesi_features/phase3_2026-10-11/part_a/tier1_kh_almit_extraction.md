# Tier-1 record Kh. ʿAlmit in the part-A volumes: extraction only

**What it is.** Everything the 50 part-A volumes of *Hadashot Arkheologiyot* (1961–1979) say about Kh. ʿAlmit, extracted by the phase-3 part-A reader. Extraction only: no comparison with any prediction was made. The reader did not open `research/preregistration/arrivals/items/`, the arrival `MANIFEST.md` predictions or `research/assessments/kohlit_chain/chain.json`, and did not search the repository for earlier notes on Kh. ʿAlmit.

**Result of the search.** No notice devoted to Kh. ʿAlmit occurs in the part-A volumes. The site is named twice, in passing, in one regional survey report (HA 26, 1968). Both passages are extracted below.

**Status and ordering (deviation).** The reader first read HA 26 on 11 October 2026, after the phase-2 freeze (d0f8c7c) and the phase-3 scope freeze (4d8325e). The two mentions were read as part of the survey report and were not recognised as a Kh. ʿAlmit record at first reading. The report's coding row (`HA26-019-ephraim-benjamin-survey`, committed in ac45765) lists "Almit" among the sites named in the settlement history and codes no feature. The mentions were recognised by a full-text search for the name at the end of the reading. So this extraction is committed after that coding row, not before it. Nothing else has been coded from these passages, and nothing will be. The integrator decides whether this counts as exposure under `research/preregistration/arrivals/ARRIVAL_PROCEDURE.md`.

**Labels.** EVIDENCE = the volume says it (Hebrew quotes verbatim from the text layer, 12 words or fewer). INFERENCE = the reader's reasoning. Nothing here is a CLAIM of identification.

## Source

| item | value |
|---|---|
| Volume | Hadashot Arkheologiyot 26 (1968), Hebrew, typed |
| Report | "הר אפרים ובנימין – מרכז (חולייה מס' 5)": the central Ephraim and Benjamin team of the 1967–68 emergency survey of Judea, Samaria and the Golan; author Z. Kallai; printed pp. 19–24 |
| Local file | owner's Mac, `~/Downloads/IAA portal volumes/IAA_HA_26_1968.pdf`, 49 PDF pages |
| PDF SHA-256 | `a0ef49e7027868070b54c343509d6350b5a88692c9b6da81f590a0629df0a2c2` (matches `../partition.csv`) |
| Text | `pdftotext -raw` (SHA-256 `508c7cf1a0dd9b68a1e739ff765a56b5b44b6d1c5ba00e5734ee8301ae625b7c`) and `pdftotext -layout` (SHA-256 `6c0af1dcb7706ce14217f40fc9460162c7e5d1b70a28f05492143a6c3c932edc`), kept on the Mac outside the repository |
| Page | both passages are on PDF p. 28. The page number is not in the text layer; printed p. 23 by the sequence 21, 22, 24 on PDF pp. 26, 27 and 29 (INFERENCE) |
| Span hash rule | SHA-256 of raw-file lines a–b, bidi control characters removed, form feeds to spaces, whitespace collapsed to single spaces, UTF-8 |

Search scope: the raw text of all 50 part-A volumes was searched for "עלמית", "עלמת", "עלמון" and the substring "למית" (every other hit is a different word, such as "צלמית", "מוסלמית", "שולמית" or "גלמית"), and for Latin "Almit" and "Alamit". The two passages below are the only hits. No heading in the portal tables of contents names the site (the only "למית" hits there are the personal name "שולמית"). Pages without a text layer (listed in `NOTES.md`) could not be searched.

## 1. Kh. ʿAlmit as a reference point for Kh. Abu Musrah

Raw lines 6593–6639, span SHA-256 `71c7e5d5ee9c456043aa947b067c7b6b4901bcb04c67310b20279e5d21d76d17`.

EVIDENCE:
- Context: the paragraph opens as the survey enters the land of Benjamin. Beyond the main identifications known before, no further identifications could be resolved for now.
- If the historical settlement of Parah ("הפרה") is linked to Nahal Prat (Wadi Fara), the only site to be considered for now is Kh. Abu Musrah. The text places it "שבין ח' עלמית (עלמת) לעין פארה": between Kh. ʿAlmit (ʿAlmat) and ʿEin Fara.
- Nothing more is said here about Kh. ʿAlmit: no finds, periods, remains, map reference or distance.

INFERENCE: "(עלמת)" in brackets gives the biblical name the author attaches to the site; the text does not argue the identification.

## 2. Kh. ʿAlmit among the sites east and south of Michmash

Raw lines 6660–6725, span SHA-256 `3cc5a0ee6c93ea07618b44988122b67e53892a9d4fdce1c6ae6e29368677f920`.

EVIDENCE:
- "נתגלו שני יישובים מתקופת הברזל הקדומה": on the edge of the Judean Desert, east and south beyond Michmash, the survey found two settlements of the early Iron Age. One is at a "Tell el-ʿAsmar(?)" ("תל עסמר-אל", order garbled in the text layer) and one at Kh. Dawara. At Dawara settlement seems not to continue after this period. At small sites south of Michmash, settlement seems to begin at the end of the period.
- "במכמש עצמה ובג'בע (גבע בנימין) נמצא ממצא הולם": at Michmash itself and at Jebaʿ (Geba of Benjamin) "fitting" finds were found ("Jebaʿ" is printed with an asterisk-like mark in the text layer).
- "והוא הדין בח' עלמית": and the same holds for Kh. ʿAlmit.
- At Hizma (Azmaveth), on the other hand, no finds of this period have been found so far. The text layer reads "בחזסה"; "Hizma" is the reader's correction of an evident OCR error (INFERENCE).
- Not given: what the finds at Kh. ʿAlmit are (pottery is not named), how many there are, where on the site they were found, any feature (cistern, pool, channel, cave, tomb, installation) or any map reference.

INFERENCE: "this period" refers back to the early Iron Age named at the start of the passage. "הולם" ("fitting") is ambiguous. It may mean finds of the early Iron Age in general, or finds that fit the settlement starting at the end of the period, as at the small sites south of Michmash. The text does not decide between these. Periods other than the early Iron Age at Kh. ʿAlmit are not mentioned in this report.

## Not found

- No excavation, salvage, inspection or conservation notice on Kh. ʿAlmit in HA 1–39, 41–43, 46–58 or 61–72 (the part-A set; HA 40, 44, 45 and 59–60 are not part-A files).
- No feature of the eligible classes is described for Kh. ʿAlmit in any part-A volume.
