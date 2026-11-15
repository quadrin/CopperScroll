# OSM springs and caves against the scroll's water and cave entries: OSM misses the key springs (ʿAin es-Sultan, ʿEn Rogel, the Beth Shean spring); it adds no candidate. No change — 14 November 2026

## Result first

1. **36 entry–candidate rows** have a water or cave word in the entry (spring, cave, cistern or pit, pool, aqueduct, tomb; stems found in the ETCBC text, with number words such as ארבעין and שבעין left out). For each, I counted OSM springs and cave entrances within 500 m and 1 km of the candidate point (OSM extract of 15 November; 772 springs, 551 caves).
2. **OSM has no point for the springs that matter most:**
   - **ʿAin es-Sultan (Elisha's spring):** no OSM spring near Tell es-Sultan; the nearest is ʿAin Duk, 3.4 km away (entries 11, 15, 19, 60).
   - **ʿEn Rogel / Bir Ayyub:** not in OSM; the only spring near the Jerusalem candidates is the Gihon (161–912 m).
   - **Beth Shean, entry 58 "the mouth of the spring" (המבוע):** nearest OSM spring 3.2 km.
   - Kh. Ibziq (entry 59): nearest OSM spring 9.5 km.
3. **Caves:** OSM has two cave entrances within 500 m of the Kh. Qumran point (one named "Qumran cave", 42 m) and cave or tunnel features at Hyrcania. It has none within 1 km of the Jericho, Wadi Kuteif, ʿAṣla or Tell el-Qos candidates, although the cliffs there have many recorded caves (ʿAtiqot 41; the project's cave table has 665 rows).
4. **So OSM is a much weaker source than the project's own tables** for springs and caves in this area. Use it only as a list of named modern points. No rating, candidate or count changed.

## Table

`osm_springs_caves_vs_entries_2026-11-14.csv`: entry, lines, feature words, candidate, point precision, rating label, springs within 500 m / 1 km and the nearest, caves within 500 m / 1 km and the nearest.

## Limits

- Feature words are found by stems in the ETCBC text. A word with a broken stem is missed; the list is not an editorial reading.
- Distances are from the candidate points, whose precision is 50 m to 5 km (column in the table).

## Not done

- A check of OSM springs against the project's water table (`research/regional/water_systems/water.csv`) for names that the project lacks.

## Where the files are

- Drive, register folder: `osm_springs_caves_vs_entries_2026-11-14.csv`.
- Session: `/home/claude/cs/os/osmcmp.py`.

No rating or candidate was changed.
