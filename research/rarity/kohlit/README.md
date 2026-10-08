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

### Where the exposed candidates land

These are reported as the protocol requires. They do not change the rules.

- **Tell es-Sultan.** WBADB holds it only as an Excavations row: E334, the 1992 limited excavation, periods "EB". It records no Hellenistic or Roman occupation for the tell, so the tell is **not a unit in the main set**. It enters only the pre-70 sensitivity set, where it goes to Stage 2 with one pool-word hit within 2 km. Jericho's Roman cemetery is a separate row, S2446 (Rom). The town is a known WBADB coverage gap (sourcebook p. 28). The rules allow no outside correction.
- **Kh. Marjame (S1658, 181600/155400; Hel, Rom).** This is the Kh. el-Marjama at ʿEin Samiya. Main set, R1, goes to Stage 2. Its own components list a pool and an aqueduct, with no position given.
- **Kh. Marjama (S2488, 177750/140350; Hel).** A different site with the same name. Main set, R1 and R2, goes to Stage 2.
- **Kh. Yanun (S1001) and Yanun (S1053).** Main set, R1, with no pool word within 2 km. Both are pending the SWP screen.
- **ʿEin el-Ghuweir (S4546).** Main set, R2, pending the SWP screen.
- **Kh. Qumran (E754).** Main set, R2, goes to Stage 2.

### Next

1. **Stage 1b, the SWP screen.** Freeze its rules, then match SWP Memoir site entries to units by name.
2. **Stage 2.** Code the 186 main-set units, plus any that Stage 1b adds, from sources 1–5.

The original survey entries (source 2), mainly Bar-Adon 1972 and Kallai 1972, are in Hebrew and exist only in libraries.
