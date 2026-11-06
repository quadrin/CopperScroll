# Side-quest D1, round 2 (loose ends parked by AGENTS.md): finds, 6 November 2026

Worker: lane D1, round 2. Main read at `origin/main` = bb612c3. AGENTS.md was removed by PR #93. The merge changed only README.md, atlas/README.md, the two OPEN_QUESTIONS copies and ACTIVE_TEST.md (the AGENTS links). No data file changed.

**What round 2 did.** I listed the items that were parked only because of AGENTS-era rules: Tier-1 "register before reading" records, held-area "existence only" text, EXPOSED labels and frozen contradiction wording. There are 18 of them, in `agents_parked_items.csv`. I then closed what the corpus can close.
- The biggest group is the nine Tier-1 next links of the Koḥlit chain (`research/assessments/kohlit_chain/next_links.md`, ranks 1–9). They waited to be registered as unseen tests, and the protected records behind them were never compared.
- Seven of the nine are now closed (cards 1–2). One record is misrouted (card 2), and one link stays open (S3961, record not identified).
- The held ASI 1 text for Tell Muhalhil is closed in card 3.

Private products: `/home/claude/swarm/private2/D1/`. It holds crops of ʿAtiqot 41 Plans 6 and 8, crops of ASI 1 p. 118 and Benjamin p. 380, and the OCR of Benjamin p. 380. These are IAA and other publishers' page images, so none of them are public.

---

FIND CARD
Title (one line): ʿAtiqot 41's own plans and captions give the opening facings that the project codes as "no facing in the record" (XI/18 faces about NNE–NE, XI/20 faces S, VIII/29 has a north-facing entrance). This closes the Koḥlit opening-facing links for Kh. Qumran and Tell es-Samrat.
Lane: D1
Round-1 link: new
What is odd (2–4 sentences):
- The entry-25 cave inventory reads facings from words only.
- `research/regional/caves_entry25/aspect.csv` codes A41:XI/18, XI/20, VIII/28 and VIII/29 "no facing in the record". Overall, 33 of the 48 ʿAtiqot 41 caves whose record cites a plan are coded that way.
- The same records contain the facing:
  - XI/18: Plan 6 has a north arrow, and the opening lies 5–45° true. Fig. 11 independently shows the entrances of XI/18 and XI/19 "looking south-west".
  - XI/20: Plan 8 has a north arrow and shows the wide opening on the south side. The inventory says "published_plan: none" for this cave.
  - VIII/29: the text says outright that it has a "northern opening, facing (הפונה) the ledge at the foot of Cave VIII/28", which lies about 10 m to the north. The Region VIII Fig. 2 and Fig. 3 captions view that cliff "looking south" and "looking south-west".
- These are the very records that the Koḥlit chain's Tier-1 opening-facing links were waiting for.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Region XI, Baruch, Mazor and Sandhaus. Bucket `atiqot/pdf/vol-041/iss-1/2563_region-xi-…pdf`:
  - printed p. 194 (PDF p. 8): Plan 6, XI/18, 19345/12851;
  - p. 195 (PDF p. 9): Fig. 11 caption, "מבט לדרום-מערב";
  - p. 197 (PDF p. 11): Plan 8, XI/20, 19335/12838.
- English summary: `iss-2/2585_…pdf` pp. 180–181 (XI/18 entrance 1.2 × 0.7 m; XI/20 "broad, high entrance", 3 × 2.7 m).
- Region VIII, Eshel and Zissu. `iss-1/2552_…pdf` PDF p. 11 (VIII/29 text) and the Fig. 2 and Fig. 3 captions. English summary: `iss-2/2569_…pdf` p. 122 ("two entrances: a northern one facing the terrace at the foot of Cave VIII/28 and a southern one that opens onto the cliff").
- Region IX, Weiss. `iss-1/2558_…pdf` Table 1. It gives cliff position and size only. Of IX/1–22 only IX/14 has a plan.
- Geometry from the chain anchors in `chain.json`:
  - Kh. Qumran (E754, 193650/127650) → XI/18: 883 m at 347°; → XI/20: 789 m at 338°.
  - Tell es-Samrat (S2430, 191700/141300) → VIII/29: 967 m at 321°.
  - All of these lie inside the links' 315°–45° / 1 km sector. The plan crops are in private2.
- Measuring the XI/18 plan: the north arrow is about 45° clockwise of page-up. The mouth normal lies at 52° page bearing, which is 6° true, and the cave axis is 90° page, which is 44° true. So the opening faces about 6–45° true.
Literature check (queries run, result, tag): the facts are published in ʿAtiqot 41 (2002). Repo greps for "XI/18", "VIII/29" and "opening-facing" across main and `branch_only`, and across the round-1 and round-2 swarm folders, found no reading of the plans for facing. `aspect.csv` and `next_links.md` still list the links as unread. Tag: **NEW TO THE PROJECT**.
Why it might matter:
- Results for the chain links:
  - QUMRAN-1-opening-facing: **success** (XI/18).
  - S2430-2: **success** (VIII/29, with VIII/28 by the captions).
  - S2539-2 and S2589-2: **not decidable from this record**. Region IX gives no per-cave facing, only "the slope facing the Jericho Valley".
  - S3961-2: still open. Its caves are WBADB excavation rows (Q-4 = E761; B-49 = S3900) whose reports were not found in the corpus.
- The inventory's facing column under-reads its own sources, so any aspect statistic built on `aspect.csv` (618 "no facing in the record" rows) has a measurable, fixable gap.
- Side note: WBADB WBS:4143 "Scroll Cave" (XI/19) copies the publication's misprint 19343/12391, which lies 4.6 km south of XI/18. The project's `caves.csv` already flags the misprint. B2b's join marks the row "agree" at 0 m, so this error class was not caught there.
- **ARGUMENT (scroll consequence, entry 60, Milik's "opening to the north" branch RB-M):** the success is cheap.
  - The Qumran fault cliff runs N–S and the Ketef Jericho caves of Region VIII sit in a cliff viewed "looking south", so openings at 0–45° are common there.
  - The relation is met at two of the four decidable model sites on the first reading. It therefore adds little or no discrimination for Kh. Qumran against the other Koḥlit models.
  - It should not be counted as support for the Qumran = Koḥlit model, beyond showing that RB-M is not contradicted there.
How to confirm or kill it (with data in hand, or what is missing):
- Confirm: re-measure the north arrows of Plans 6 and 8 at full resolution. If the XI/18 arrow is more than about 10° steeper than measured, the facing could fall outside 45°; Fig. 11's "looking south-west" makes that unlikely.
- Kill: a published plan of XI/18 or VIII/29 with a different north.
- Extend: measure the other 32 plan-bearing ʿAtiqot 41 caves the same way. That is cheap, and all the PDFs are in the bucket.
Confidence: high (VIII/29 text, XI/20 plan); medium-high (XI/18, near the 45° edge).
Touches the Copper Scroll? yes. It closes entry 60 RB-M links at Qumran and Tell es-Samrat (exploratory; the support is weak, see ARGUMENT).

---

FIND CARD
Title (one line): The four "protected" Tier-1 records of the Koḥlit chain, read at last. Kh. ʿAlmit meets "a tomb at a cave/pit mouth" by an explicit adjacency phrase. Tananir's only pool is on the west. Highlands does not contain the er-Ras features WBADB attributes to it. The Sheikh Dhiab record is misrouted.
Lane: D1
Round-1 link: new (method extends D1-3's "stale status line" class)
What is odd (2–4 sentences):
- `next_links.md` ranks 6–9 still say "record supplied, not yet read for this relation". The records were set aside to be registered as unseen tests, and that step was never done (arrival README step 5).
- Two of them had in fact been read:
  - HA 28–29 and the Kh. ʿAlmit notices were extracted on 11 Oct (phase-3 `tier1_*_extraction.md`).
  - Dinur and Feig site 496 was summarized in the 12 Oct Benjamin full read ("west-slope tomb access, a nearby columbarium").
- Nobody compared them with the chain. Meanwhile, the 30 Oct held screen "skipped" site 496 as protected.
- Comparing them now gives four different outcomes, set out under "Why it might matter".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- **Kh. ʿAlmit (S2849-2-mouth): success.**
  - Benjamin survey, Hebrew printed p. 380, site 496 (Drive photo `1-heb p380-381 (IMG_1871).HEIC`, id `1COzvobFsdTTMAG66BdIRRGEAS12lZObn`): "במדרון המערבי נמצאת מערת-קבורה, ובחזיתה 5 מדרגות … בסמוך לפתח המערה נראה פתח עליון של מערת-קולומבאריום, ובה 70 גומחות. קוטר המערה 7 מ'". In English: a burial cave on the west slope, with five steps in front; near the cave's opening, the upper opening of a columbarium with 70 niches, 7 m across.
  - Pottery: Hellenistic/Roman "the majority" (p. 381).
  - Second witness: HA-ESI 115 p. 48*, where cist graves are "cut … directly above Cave A", a burial cave with pottery of the 2nd c. BCE to the mid-1st c. CE (`haesi_features/phase3_2026-10-11/part_c/tier1_kh_almit_extraction.md`).
  - The chain's S2849 evidence (`chain.json` M-S2849) uses only WBADB S2806 components and has no columbarium.
- **Tananir (E99-1-pool-east): inconclusive, leaning west.**
  - HA 28–29 pp. 39–40 (`part_a/tier1_HA28-29_extraction.md` §1): "a rectangular pool, cut in the rock and plastered", "about 50 m west of the main building".
  - The other water feature is an MB IIB round pit inside the lower building.
  - There is no east pool and no absence statement.
- **Udala (S1032-2-mouth): inconclusive; the record does not hold the features.**
  - Highlands of Many Cultures site 17-17/64/01 er-Ras (store PDF `Finkelstein-Lederman-Bunimovitz-1997-…-717cc393`, PDF p. 735, printed p. 700). The description lists "A number of cisterns" and the en-Nabi ʿUzeir sheikh-tomb complex only.
  - WBADB S990's "rock-cut caves" and "rock-cut tomb nearby", which the rarity coding counts (`research/rarity/kohlit/feature_audit/features_behind_matches.csv` rows S1032 f4–f5), are not in this record.
  - Its previous-survey reference reads "Kallai 1972: 167", where the chain cites "Kallai site 28".
- **Tell esh-Sheikh Dhiab (S6040-1): record misrouted.**
  - The chain names "Zertal Vol. 4 site 194". The MHCS 4 extract (Drive `117OzQfX92CEKxiekTLJXQF5SHWeJ21Dh`) cites the tell itself as "Zertal 2012a: site 23" and, elsewhere, "site Z3 and appendix 7".
  - Vol. 4 site 194 is ʿArkan es-Suwaneh (S1454), per chain.json itself.
Literature check (queries run, result, tag): all four records are published. Repo greps for "columbar" in `kohlit_chain/` and `rarity/kohlit` find WBADB component rows only (S3001 and others), nothing on ʿAlmit. Greps for "Kallai 1972: 167" and "Zertal 2012a" in the chain find nothing. Tag: **NEW TO THE PROJECT**.
Why it might matter:
- Results for the chain links:
  - S2849-2-mouth: **success** (exploratory).
  - E99-1: inconclusive. The only pool lies in the west sector, at 270°.
  - S1032-2: inconclusive. Also, the WBADB-only components behind Udala's grave condition need a source other than Highlands.
  - S6040-1: needs the right Zertal volume.
- `next_links.md`'s "not yet read" for ʿAlmit contradicts two notes that had read it (11–12 Oct).
- **ARGUMENT (entry 60, "tombs at its mouth" branch):**
  - The first non-Jericho model whose full record is read meets the relation by an explicit phrase: a burial cave beside the shaft mouth of a columbarium, at a site whose pottery is mostly Hellenistic–Roman.
  - So the relation is not rare in the Benjamin desert fringe. It cannot favour Tell es-Sultan or Kh. el-Marjama over Kh. ʿAlmit.
  - ʿAlmit (biblical ʿAlemeth/ʿAlmon) does not become a Koḥlit candidate from this alone: the chain still has no pool or pit date for it.
How to confirm or kill it (with data in hand, or what is missing):
- ʿAlmit: open the Benjamin p. 380 photo; the sentence is in column 1. Kill it if Dinur and Feig's plan (not in hand) puts the columbarium mouth more than 10 m from the tomb opening.
- Udala: find which WBADB source gives "rock-cut tomb nearby" (Sion 2001 site 313, or Kallai). Neither is in the store.
- Sheikh Dhiab: identify "Zertal 2012a". The full MHCS 4 PDF (`1EuhZuJYvThNVh08IE0Bal6AeMikL3I84`, 42.8 MB) carries its bibliography but is over the connector limit.
Confidence: high (what each record says); medium (that "בסמוך" means within 10 m).
Touches the Copper Scroll? yes. Entry 60 (Koḥlit) chain links; exploratory.

---

FIND CARD
Title (one line): Bar-Adon's full ASI 1 entry for Tell Muhalhil (site 83), held under the 25 Oct rule, has no pool, cistern or tomb in any of its five components and no Hellenistic or Roman pottery at all.
Lane: D1
Round-1 link: new
What is odd (2–4 sentences):
- The project's Koḥlit proposal "muhalhil" (Lurie) has two probes waiting on this page: P03 (entry 4, "a tell") and P04 (entry 11, "a cornered pool east of Koḥlit, in use 50 BCE–135 CE"). The matching looks L05 and L22 say "Bar-Adon 1972 not read by the project".
- The 30 Oct held screen transcribed only the measured items, and said the page "cannot supply an absence statement, because the unmeasured text is not summarized".
- The full text lists five sub-sites:
  - א: elliptical enclosure 33 × 25 m;
  - ב: elliptical enclosure 45 × 18 m with an inner wall;
  - ג: round building 4.40 m with an observation post;
  - ד: oval enclosure 50 × 40 m with rooms;
  - ה: "Tell Mahalhal", a 3.5 × 2.5 m building of large flint stones, with a wall 11 m long about 35 m to its north, a threshold and a semicircular room.
- Pottery is listed per sub-site: א Iron; ב Chalcolithic and Iron; ג Iron I, Iron II, Arab and Crusader; ד Iron. ה has no pottery line. No water installation, tomb or mound profile is described.
Evidence (exact sources: file path / page / figure / frame / coordinates): ASI 1 (Kochavi ed. 1972), Bar-Adon chapter, Hebrew pp. 118–119, site 83 (header "T. Muḥalhil", 192 133, −80 m). Drive photo `1-heb p118-119 (IMG_1722).HEIC` (id `1JRyNT86dHTpZyW2Y8UUk3wRB-x7mvOFc`). Sub-site א is at the foot of column 1 of p. 118; ב–ה and the pottery list are at the top of column 2. The store copy `01-ASI1-Kochavi-1972-indexed-81b7cd39` has no text for this chapter by design ("Location-only index"). The project records are `research/models/search_effectiveness/next_records.csv` P03–P04, `looks_v2.csv` L05 and L22, and `books_usc_2026-10-30/held_asi1_deirhajleh_2026-10-30.md` §4–5.
Literature check (queries run, result, tag): web search `"Muhalhil" Kohlit Copper Scroll Lurie Bar-Adon survey` returned only general Koḥlit pages ([Wikipedia: Kohlit](https://en.wikipedia.org/wiki/Kohlit); [BAS: The Mysterious Copper Scroll](https://library.biblicalarchaeology.org/article/the-mysterious-copper-scroll)), with nothing on Bar-Adon's site 83. A repo grep for "muhalhil" finds the probe rows and the Sion/ASI Kalia records only. Tag: **NEW TO THE PROJECT** (Bar-Adon is published; the project had not read it).
Why it might matter:
- P04/L22: still no explicit absence statement. But the complete record has no pool and no pottery of the period the probe needs (50 BCE–135 CE), so "silent" should read "read; no pool; no Second Temple pottery".
- P03/L05: the "tell" is named, but the record describes a small building, not a mound.
- **ARGUMENT (entries 4, 11, 60; muhalhil model):**
  - Muhalhil was carried as a Koḥlit candidate with unknown support because this page was held.
  - Read in full, it gives no Second Temple period occupation at any of its five sub-sites. That is a large negative for any model that needs a pool in use between 50 BCE and 135 CE at Koḥlit.
  - It is not a formal contradiction: a survey cannot prove absence, and Sion's Kalia map (ASI 109/5/83–100) records nine more "Tell Muhalhal" units 1.0–1.9 km from the proxy point.
How to confirm or kill it (with data in hand, or what is missing):
- Confirm: read the p. 118 photo; the crops are in private2. Check Sion's ASI Kalia records 109/5/83–100 (online) for Roman pottery.
- Kill: any Roman-period find at these coordinates in Sion's survey would restore the candidate, but not a pool.
Confidence: high (content of the record); medium (consequence).
Touches the Copper Scroll? yes. Entries 4 and 11 (and 60) under the muhalhil/Koḥlit proposal.

---

## Dead ends

- D1-1 (Birket Musa 21.5 m): `pdf-search` for "Birket Musa", "Birket Mus", "Birket Moussa" and "Birkat Musa" across all store PDFs finds only ROSAPAT 07 (pp. 31, 48, 74, 76, 108, 132, 202). No second depth figure is in hand, so the source of the number is still untraced (Augustinović 1951, Robinson–Smith 1970 and Netzer p. 378 are still not in the corpus).
- S3961-2 (caves Q-4 = WBADB E761 and B-49 = S3900): no report for "Cave Q-4 (Hizmi and Richardson)" found in the corpus. Link left open.
- Region IX facings (S2539-2, S2589-2): only IX/14 has a plan, and the table has no facing column. Not decidable.
- S2096-2 Kafr Nata: without the frozen wording it is simply "no dated tomb". No new data. Left to the owner.
- Entry 24 Ekteif windows (EXPOSED): the rule that blocked a re-read is gone, but a re-read is imagery work (C lanes). Not attempted.
- The other held Benjamin and ASI 1 sites: readable now, but no open question is attached to them. Listed in the CSV only.

## Blocked inputs

- Drive `Magen & Finkelstein (eds.) 1993 – … Benjamin (IAA, Hebrew).pdf` (`1evqJT-QX-3HMFqr-ON069yuLnyp1Te_8`, 237 MB): over the connector limit. I used the HEIC page photos instead.
- Drive `Zertal & Bar 2019 – MHCS 4 … .pdf` (`1EuhZuJYvThNVh08IE0Bal6AeMikL3I84`, 42.8 MB): over the connector limit. The 5.4 MB extract has no site catalogue or bibliography. MHCS is not in the bucket PDF store.
- The store's `01-ASI1-Kochavi-1972-indexed` holds no text for the Bar-Adon chapter (location-only by design). I used the Drive photos.

Files: `agents_parked_items.csv` (18 AGENTS-parked items with round-2 status). Scratch is in `/home/claude/swarm/scratch/D1r2/`.
