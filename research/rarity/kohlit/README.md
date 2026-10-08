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
