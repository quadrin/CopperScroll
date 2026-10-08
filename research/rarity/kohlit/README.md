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

## Next

1. **Stage 1b.** Run the frozen script and commit the result.
2. **Stage 2.** Freeze the §4 matching script and the coding protocol, then code every unit that goes to Stage 2 from sources 1–5.

The original survey entries (source 2), mainly Bar-Adon 1972 and Kallai 1972, are in Hebrew and exist only in libraries.
