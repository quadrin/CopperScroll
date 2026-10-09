# Analogues round, 9 October 2026

The project owner compared the project with solved searches: Ephesus (Wood, 1869), Linear B (1952–53), Richard III (2012) and AF447 (2011), and also the Atocha, Kalkriese, Herodium and Vergina. From these, the owner chose seven method extensions and asked for them to run in parallel.

Seven workers built them at the same time. Each worker owned one folder. The integrator owned shared files and Git. All work is exploratory. No registered result changed. No identification, deposit or outcome-ledger count was added. No image of XII 8–12 or of the 21/22 cut was opened.

## What was built

| Tool | Case | Folder | Main result |
|---|---|---|---|
| Failed looks in the joint model | AF447 | [models/search_effectiveness](../models/search_effectiveness/README.md) | A layer over the W2B model (K2) gives each silent or absent look a factor 1 − pd. With all factors = 1 it reproduces K2 exactly. Only 2 of 22 negative looks have a detection probability: Puech's "no mound" notes for ʿAyn Feshkha and ʿAyn el-Ghuweir. The largest change is entry 4 (total variation 0.031). 99.99% of the posterior mass sits in states with combined pd < 0.2. Twenty looks are "phantom coverage", including every look cited against Kh. Yanun, Kh. el-Marjama and the ground north of Tell es-Sultan. |
| Letter confusions between editions | Linear B (Bennett, Kober) | [text/edition_confusions](../text/edition_confusions/README.md) | 664 recorded disagreements; 178 shape confusions counted by place. Six pairs carry 97: ב–כ 26, ה–ח 21, ה–ת 16, ד–ר 12, ב–מ 11, ח–ת 11. Nine of the top ten fall in Lefkovits's look-alike groups (2000 p. 16). Of 125 disputed reading pairs, 38 need a rare confusion; only one is a clean case (VIII 2). XII 8–12 is excluded, and tests enforce it. |
| Predictions before arrival | Linear B (Pylos tablet) | [preregistration/arrivals](../preregistration/arrivals/README.md) | 22 requested or wanted items, each with what every live model predicts, hashed in MANIFEST.md. None has arrived. The four XII 10 image sources tie at the top; they carry no new letter predictions, only a map from the frozen protocol's outcomes to the Koḥlit classes that survive. Kochavi 1972 ranks next. The Tell es-Sultan records can confirm a mouth–tomb pair but cannot contradict it. |
| Salvage records and earlier searches | Atocha | [history/salvage_records](../history/salvage_records/README.md) | 27 ancient accounts (10 EVIDENCE, 15 TRADITION, 2 CLAIM) and 27 modern searches. Every EVIDENCE account that bears on a scenario describes removal soon after a loss. Support for "real but unrecovered" comes only from tradition or claims. No modern search has a documented target volume and depth. Antiquities 18.85–89 shows a first-century belief in vessels buried on Gerizim; it cannot decide entry 57. |
| PEF Quarterly Statement find reports | Kalkriese (Mommsen) | [history/pef_qs_finds](../history/pef_qs_finds/README.md) | All QS issues 1869–1914 searched with frozen terms: 2,311 hits, 257 find reports, 226 distinct finds (145 in Jerusalem). No QS report puts a find in the strip just north of Tell es-Sultan. At Qumran, the graves that Drake and Clermont-Ganneau opened held no objects (QS 1874 pp. 74, 83). OCR misses at least 412 place-name occurrences. |
| Where people really hid valuables | Richard III (base rates) | [comparanda/concealment_contexts](../comparanda/concealment_contexts/README.md) | 158 recorded concealments, 150 BCE–135 CE (68 with a known context), against the scroll's 61 entries. Frozen verdict: DIFFERENT (D = 0.67, p = 0.00005). The scroll puts 48% of entries in water installations; known contexts have 4%. The result is reporting-sensitive and speaks only to the kind of list (R12). |
| Staged objectives and stop rules | Richard III, Ephesus | [plan](../plan/STAGED_OBJECTIVES.md) | Six stages rated before work: S1 A, S2 B, S3 B, S4 C, S5 C, S6 (a deposit) D. 32 lanes mapped. 15 lanes are proposed to park now. Every stop rule is PROPOSED; the owner decides. |

## Integration

- Every new suite passes: 134 tests (14 + 37 + 19 + 15 + 17 + 15 + 17). The edition-confusions parser test runs when `PUECH2015` points to the local extract. No earlier file changed. The earlier suites pass, except two deep_analysis suites that need inputs not in this checkout (deep_analysis/features.json, PyMuPDF); this round does not touch them.
- Shared files changed: ACTIVE_TEST (last-session line, exposure note under question 2, one arrival line, key-report links) and its history file.
- The arrival register counts only if its commit is pushed before an item arrives. Its MANIFEST.md hashes are in the first commit that adds this log.

## Exposure note

The PEF worker read published QS reports about Tell es-Sultan (QS 1874 p. 89; 1894 pp. 176–179; 1904 p. 167; 1907 p. 245; 1910 pp. 59–61). These are not the pending PEF archive records (Garstang Papers, pre-1948 photographs), which stay under the SULTAN-1 registration protocol. The QS items are now exposed and cannot serve as unseen evidence.

## Proposed but not made

These need an editorial decision:
- `text/readings.json`: e48-feet (Puech 2015 p. 91 gives Milik's reading), e4-immersion (Puech 2015 p. 36 n. 131 gives Eshel's reading), e17-achor (Puech's reading corrects an engraved nun that Lefkovits reads).
- OPEN_QUESTIONS R05: link the Antiquities 18.85 section of the salvage-records README; add Bull's reports (HTR 58, 1965; BA 31, 1968) as next records. R12: add the concealment result and Ezra 1:7–11 and 8:24–34 as candidate corpora. (Edit OPEN_QUESTIONS together with its byte-identical atlas copy.)
- T02 hoard match: CHRE 8132 and 18771 are the same hoard.
- W2C: say that "ABSENT_IN_SOURCES" means silent, not absent. Decide whether Qumran (entry 60) and IV/17 (entry 25) become model candidates.
- Before the L-656 file or the IAA cave records arrive: freeze an entry-25 mouth-aspect rule and the IV/17 target declarations.
- Staged objectives: the owner decides which proposed stop rules to adopt.

## Follow-up applied (9 October, owner approval)

The owner approved the first five proposals above and adding both model candidates. Status of each:
1. **Reading notes (applied).** e48-feet: Milik's edition at X 13 is ḥpw{w}r gmwt (Puech 2015 p. 91); his רגמות is the X 6 reading (p. 88 n. 380). e4-immersion: Eshel 2002 reads נקרת, without yod (Puech 2015 p. 36 n. 131). e17-achor: Lefkovits keeps the engraved nun as a dialect form; Puech reads the same nun and corrects it to reš (pp. 51–52, n. 201). The notes, the atlas text and the atlas site were rebuilt.
2. **Backlog links (applied).** R05 and R12 in OPEN_QUESTIONS and its atlas copy, which stay byte-identical.
3. **Duplicate hoard (no change needed).** T02 already merges CHRE 8132 and 18771 as one record (H60); only its raw CHRE list holds both.
4. **Absence label (applied).** The W2C report now says that status A and ABSENT_IN_SOURCES mean "not mentioned in the sources read". No cell, score or ranking changed.
5. **Model candidates (applied, exploratory).** A separate v2 input set adds entry 60 at Kh. Qumran (the project's M-QUMRAN model, not a published proposal) and entry 25 at cave IV/17. Under K2, P(25 at IV/17) = 0.18 and P(60 at Kh. Qumran) = 0.033. The v1 inputs and outputs are unchanged. See [README_v2](../models/search_effectiveness/README_v2.md).
6. **Frozen rules (applied).** The Entry 25 mouth-aspect rule and the eight IV/17 target declarations are frozen in [entry25_iv17_rules](../preregistration/entry25_iv17_rules/README.md). The primary "east" sector is 45°–135°, with declared sensitivity sectors. A mouth passes only if its whole facing interval lies inside the sector. The decisions plan now points to these rules. Phase branches are not frozen.
7. **Stop rules (open).** The owner has not chosen yet.
