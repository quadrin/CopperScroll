# Koḥlit rarity count (entries 11 and 60)

This folder runs the count fixed by the [approved pre-registration](../../preregistration/kohlit_rarity_2026-10-08.md). It asks: within a fixed region, how many settlements have a pool to the east (entry 11) and a pit to the north with graves at its mouth (entry 60)? The result is "k of N, m unknown". Rarity alone identifies nothing (pre-registration §6).

## Freeze

`words.json` and `stage1_screen.py` were committed before the screen was run. The results arrive in a later commit, so the order of commits is the only record that the freeze came first; there is no outside timestamp.

The dataset is not copied into the repo because it is third-party data. It is the West Bank Archaeological Database (Greenberg & Keinan 2009), `WBADB_data1.xlsx`, from <https://emekshaveh.org/en/wp-content/uploads/2020/08/WBADB_data1.xlsx>. Its SHA-256 is `3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b`, and the script stops if the file differs.

## Choices made before the run

The pre-registration does not spell out the following points. They were fixed after looking only at the whole dataset's field list and its most common opening words. No regional subset and no pool words had been looked at.

1. **Units.**
   - **Rows:** a unit is any Surveyed row, plus any Excavation row not marked as surveyed.
   - **Settlement test:** the row must name a settlement term in its name or components (tell, ruin, village, settlement, town, city, fort, fortress, fortified, fortification, monastery, farmstead, farm, hamlet, palace, buildings, building remains, structural remains). A name beginning Tell, Tel, Kh., Khirbet, Deir, Qasr or Kafr also qualifies. Isolated caves, tombs, cisterns and installations are features, not units.
2. **Periods.**
   - **Main set:** the WBADB Hel or Rom flag is greater than 0.
   - **Sensitivity set:** any flag before 70 CE.
3. **Region.**
   - **R1:** WBADB easting X greater than 175,000 m on the Old Israel Grid.
   - **R2:** within 30 km of Kh. Qumran. The centre is converted with pyproj (EPSG:28193), minus the 1,000,000 m false northing that WBADB does not use.
4. **Pool words** (§5): pool, reservoir, birke/birkeh/birket/birka/birkat, tank, basin, spring-house.
   - **Matching:** whole words, any case, plurals allowed.
   - **Where searched:** the name, other names, components and comments of every WBADB row, in either sheet and any region, within 2 km of the unit (the unit's own row included).
5. **Stage 1 is split into two parts.**
   - **1a** screens WBADB, with this script.
   - **1b** screens the SWP Memoirs. The Memoirs cannot be placed within 2 km by script: their grid squares are about 7 × 9 km. So 1b will match Memoir site entries to units by name, under rules to be frozen before it runs.
   - Until 1b runs, a unit with no WBADB hit is "pending SWP screen", not "not recorded".
   - This changes the order of work, not the rules.

## Run

```
python3 -I stage1_screen.py /path/to/WBADB_data1.xlsx stage1a/
```

It writes `stage1a/stage1a_units.csv` (one row per unit, with its pool-word hits within 2 km) and `stage1a/stage1a_summary.json`.

## Stage 1a result (8 October 2026 UTC), frozen screen 75b0af9

| Set | Units | Pool word within 2 km → Stage 2 | No WBADB hit → pending SWP | Excavated |
|---|---|---|---|---|
| R1, Hellenistic or Roman (main) | 333 | 186 | 147 | 77 |
| R1, any period before 70 CE (sensitivity) | 499 | 240 | 259 | 95 |
| R2, Hellenistic or Roman | 101 | 76 | 25 | 38 |
| R2, any period before 70 CE | 138 | 98 | 40 | 48 |

518 WBADB rows contain a pool word.

**Which words drive the main-set hits** (number of units with each word within 2 km):

| Word | Units |
|---|---|
| pool | 104 |
| reservoir | 76 |
| basin | 59 |
| birkat / birket | 12 |
| tank | 2 |

29 units are flagged by "basin" alone. Stage 2 decides whether a "basin" meets C1 (≥3 m across, or called a pool).

### Where the exposed candidates land (Stage 1a)

These are reported as the protocol requires. They do not change the rules.

- **Tell es-Sultan.** WBADB holds it only as an Excavations row: E334, the 1992 limited excavation, periods "EB". It records no Hellenistic or Roman occupation for the tell, so the tell is **not a unit in the main set**. It enters only the pre-70 sensitivity set, where it goes to Stage 2 with one pool-word hit within 2 km. Jericho's Roman cemetery is a separate row, S2446 (Rom). The town is a known WBADB coverage gap (sourcebook p. 28). The rules allow no outside correction.
- **Kh. Marjame (S1658, 181600/155400; Hel, Rom).** This is the Kh. el-Marjama at ʿEin Samiya. Main set, R1, goes to Stage 2. Its own components list a pool and an aqueduct, with no position given.
- **Kh. Marjama (S2488, 177750/140350; Hel).** A different site with the same name. Main set, R1 and R2, goes to Stage 2.
- **Kh. Yanun (S1001) and Yanun (S1053).** Main set, R1, with no pool word within 2 km. Both are pending the SWP screen.
- **ʿEin el-Ghuweir (S4546).** Main set, R2, pending the SWP screen.
- **Kh. Qumran (E754).** Main set, R2, goes to Stage 2.

## Stage 1b rules (frozen in `stage1b_swp.py` before the run)

Source 3 is the SWP *Memoirs*, volumes II (Samaria) and III (Judaea). The script reads archive.org's OCR text of each volume and stops if a file's SHA-256 differs from the frozen value.

1. **Entries.** A Memoir entry starts at a line with a name, a map square such as `(L s)`, and a dash. A list number before the name is allowed. The entry text runs to the next entry, up to 4,000 characters. Page numbers come from the running heads and are approximate.
2. **Position.** A square gives only a point at its centre. The calibration is the one in `agent_review_2026-10-07/wave1/T01_place_names`. An entry can link to a unit only if the square centre is within 9 km of the unit: half the square's diagonal (about 5.7 km) plus the calibration error (about 3 km).
3. **Names.** The unit's WBADB name and Other_Names are compared with the Memoir name.
   - **Dropped words:** articles (el, es, …) and feature-type words (Khirbet, Tell, ʿAin, Wadi, Bir, Birket, Qasr, Khallet, Rujm and their spellings). One source can write "Kh. X" where the other writes "X".
   - **Name parts:** Beit, Deir, Kafr, Umm, Abu, Ras, Jebel, Sheikh and Nabi. The name is tried both with and without them.
   - **Skeleton:** each name becomes a consonant skeleton (kh→h, q→k, doubled letters once, vowels out, y kept). An alternative name in "X, or Y" or in brackets is tried as well.
   - **Match:** skeletons of 3 or more letters match at a difflib ratio of 0.85 or more. A 2-letter skeleton must be equal. A shorter name is not matched.
4. **Pool words.** These are the same words as in Stage 1a (`words.json`), searched in the whole entry text.
5. **Result.** A unit goes "to Stage 2" if Stage 1a or a linked Memoir entry has a pool word. If not, it is "not recorded", and C1 is UNKNOWN for that unit, never FAIL.

**Before the freeze**, the parser was tested on the Memoir text only: header counts, sample names, and the keys of sample names. No unit was compared with a Memoir entry before this commit.

**Limits.**
- OCR errors in a name (for example "Am1eh") can stop a link. The cost of a missed link is an UNKNOWN, not a FAIL.
- A false link only adds a Memoir entry to a unit's Stage 2 packet, and the coder rejects it there.
- Units with no WBADB name (42 rows named "-") can link only through Other_Names.

## Stage 1b result (8 October 2026 UTC), frozen screen 75ceb80

```
python3 -I stage1b_swp.py SWP_II.txt SWP_III.txt stage1a/stage1a_units.csv WBADB_data1.xlsx stage1b/
```

The parser found 2,162 Memoir entries (II: 1,040; III: 1,122). 169 of them contain a pool word. 147 of the 499 units link to one or more entries (180 links), and 18 links carry a pool word. `stage1b/swp_entry_index.csv` keeps the text of each linked entry for Stage 2.

| Set | Units | → Stage 2 (1a or 1b) | Added by 1b | Not recorded (C1 UNKNOWN) |
|---|---|---|---|---|
| R1, Hellenistic or Roman (main) | 333 | 190 | 4 | 143 |
| R1, any period before 70 CE | 499 | 244 | 4 | 255 |
| R2, Hellenistic or Roman | 101 | 77 | 1 | 24 |
| R2, any period before 70 CE | 138 | 99 | 1 | 39 |

The four units added by the Memoirs are Tayasir (S398, "basin"), Yaṣid (S563, "tank"), Kh. Burj el-Fariʿa (S592, "birket") and Rammun (S1845, "tank").

### Where the exposed candidates land (Stage 1b)

- **Tell es-Sultan (E334).** It links to "Tell es Sultan" (Mem III p. 220, square O s), whose entry has "reservoir", and to the cross-reference "ʿAin es Sultan" (p. 24). It was already in Stage 2.
- **Kh. Yanun (S1001) and Yanun (S1053).** Both link to "Khurbet Yanun" (Mem II p. 394, square N o: "Traces of ruins above a small spring"). The entry has no pool word, so both units are **not recorded (C1 UNKNOWN)**.
- **ʿEin el-Ghuweir (S4546).** No link: **not recorded (C1 UNKNOWN)**.
- **Kh. Marjame (S1658), Kh. Marjama (S2488) and Kh. Qumran (E754).** No link. All three were already in Stage 2 from Stage 1a.

### What the frozen parser missed (found after the run; no change to the result)

A check of the exposed candidates after the run found three Memoir entries that the frozen rules could not link. They are reported here and the result above stays as it is. Stage 2 packets may give coders any passage of source 3, so these entries can still be used there.

- **Kh. Qumran.** The entry is OCR'd as "K h ft r b e t K u m r a n (O t)". The garbled "Khftrbet" stops the name link, and square O t is more than 9 km from the unit. The entry has a "small birkeh" **outside the wall on the west**. Qumran is in Stage 2 already.
- **Yanun village.** The list number "8." is OCR'd as "S.", so the header is not found. The entry ("a small spring about 1 mile to the north") has no pool word, so the status does not change.
- **ʿAin el Ghuweir.** It is in a numbered spring list with no map square, so the parser cannot place it. The spring "forms a shallow basin". If it had linked, the unit would have gone to Stage 2. The basin is natural, so it would probably not meet C1. The unit stays "not recorded" under the frozen rules.

## Stage 2 freeze

The coding protocol, the matching script and its constants are in [`stage2/`](stage2/PROTOCOL.md). They were committed before any unit was coded, and `stage2/test_match.py` tests the matching rules on synthetic data only.

**Deviation.** §5 of the pre-registration says the matching script is committed before Stage 1. It was committed after Stage 1 and before Stage 2. Stage 1 output holds no condition data, so no condition could be seen before the freeze.

**Sources used in Stage 2, besides WBADB and the SWP Memoirs.** These files are under copyright and are not in the repo. The packet builder stops if a file differs from its hash.

| Source | File and access | SHA-256 |
|---|---|---|
| 2: Finkelstein, Lederman and Bunimovitz 1997, *Highlands of Many Cultures* | `MS_14_Highlands.pdf`, open access through the [TAU monograph series](https://en-humanities.tau.ac.il/archaeology/publications/monographseries) | `2074020593f986fdc2189448f74c3037b577fb0093bb35b658eadcf47085c16c` |
| 5: Nigro, Sala and Taha (eds) 2011, *Archaeological Heritage in the Jericho Oasis* (ROSAPAT 07) | Public download from the [expedition's publications page](https://sites.google.com/uniroma1.it/sapienzatojericho/publications) | `0c7fefdf676abb796c6cccf4f33dd6289c499d6a54249322e0b2ea672122af73` |

The other original surveys (source 2) are library-only, so the packets mark them "not accessed". The project owner later supplied Zertal Vols. 2–4 (source-2 addendum). Source 4 excerpts are gathered only where the first publication is lawfully online.

The original survey entries (source 2), mainly Bar-Adon 1972 and Kallai 1972, are in Hebrew and exist only in libraries.

## Result

Full result: [`stage2/RESULTS.md`](stage2/RESULTS.md). Coder A coded all 244 Stage 2 units, and coder B coded 60 of them.

- **Headline** (R1, main set, branch A, survey level): **k = 0, f = 1, m = 332 of N = 333.**
- **Branch B** (no graves condition): k = 4 (Tell esh-Sheikh Dhiab, Tulul Abu el-ʿAlaiq, Kypros, el-Muntar), m = 329.
- **Text level:** every unit is UNKNOWN.
- **Reading (§6):** m ≫ k, so rarity is not measurable from the available evidence. k = 0 for branch A means that the current candidate fits rest on evidence or tolerances outside the protocol. It is not a rejection.
- **Source-4 addendum** ([`stage2/addendum_s4/ADDENDUM.md`](stage2/addendum_s4/ADDENDUM.md)): 24 more first publications were read, from PDFs the project owner supplied. The headline is unchanged.
  - Qumran gains a northern cemetery (C3), Tell Shiloh, Kh. el-Khudriya and Tananir gain a northern pit (C2), and Tell Shiloh becomes a branch-B match when C1 is extended to 2 km.
  - Qumran now matches two of three conditions; C1 is still UNKNOWN.
- **Source-2 addendum** ([`stage2/addendum_s2/ADDENDUM.md`](stage2/addendum_s2/ADDENDUM.md)): Zertal's survey entries were read for 78 units, from the English edition the project owner supplied. Branch A still has k = 0, but f = 20 and m = 313 of 333.
  - Every new FAIL is a C2 FAIL (19 in the main set, 30 in the pre-70 set). Each rests on "Cisterns: none" in the entry's data block.
  - Qarn Sarṭaba (S1283) becomes a branch-B match, so branch B has k = 5.
- **Exploratory audits after the result** (8 October; the registered numbers stand):
  - [Feature-level audit](feature_audit/README.md): only Qarn Sarṭaba's C2 rests on different physical features for the two coders. Of 26 units with two or more matched conditions, 3 are jointly compatible, 22 only if an undated feature existed in the window, and Tananir is not shown compatible.
  - [Observation-process audit](observation_process/README.md): every FAIL rests on a site-level absence statement that covers at most about 1% of the 1 km sector. If an absence counts only within its scope, f = 0 in every row.
