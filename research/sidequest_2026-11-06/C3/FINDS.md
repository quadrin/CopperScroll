# Side-quest C3: what the terrain says about recorded installations (6 Nov 2026)

Lane C3. DEM: Copernicus GLO-30 tiles N31E035 and N32E035, fetched 6 Nov 2026 from the public AWS bucket (`https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N31_00_E035_00_DEM/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif`, `..._N32_00_E035_00_DEM/..._N32_00_E035_00_DEM.tif`). I mosaicked them to UTM 36N at 30 m (lon 35.00–35.65, lat 31.30–32.20) and derived slope, 150 m relief and D8 flow accumulation (pysheds), as in F's `prep_dem.py`/`derivatives.py` but without the sky-view factor. Every row of `research/regional/water_systems/water.csv` (2,016 placed rows) and `research/regional/caves_entry25/caves.csv` (561 placed rows) was sampled. I also sampled F's 150 P4a depressions, the Mandate 1:20,000 "trig" labels and the elevations printed in *The Aqueducts of Israel* (JRA Suppl. 46, bucket `01-Aqueducts-of-Israel-2002-indexed-0c0e68f6`). Scripts and per-row tables are in `private/C3/` (the per-row tables carry coordinates).

Public data: `water_dup_of_link_audit.csv`, all 499 `dup_of` links in `water.csv`. Columns: link distance, GLO-30 elevation of each end, and a verdict. It gives IDs only, no coordinates.

---

FIND CARD
Title (one line): The water inventory's duplicate linker joins records by site number from the wrong publication: 8 `dup_of` links span 4–38 km, and GLO-30 puts the two ends up to 813 m apart in height
Lane: C3
What is odd (2–4 sentences): The water inventory links WBADB rows to ASI-online rows by site number. In `build_survey.py` `dedup()`, any `Hirschfeld \d{4}, Site N` is sent to ASI Map 108/2 site N, and `Kloner \d{4}, Site [101] N` is sent to ASI-online record 101/N. Neither rule holds in every case. (a) WBADB cites two Hirschfeld surveys. "Hirschfeld 1983" (45 WBADB rows, Jericho–Jordan valley monasteries) is not the Herodium map, "Hirschfeld 1985" (= ASI 108/2). So Zawayat (Hirschfeld 1983 site 28, channels, GLO-30 −377 m) became a duplicate of ʿEin es-Sakhari (108/2/28, +436 m), 37.5 km away. Nusib ʿUweishira (site 17, pool, −91 m) became a duplicate of Kh. Khureitun (108/2/17, +557 m), 28.9 km away. (b) ASI-online Map 101 numbers its records in its own sequence and puts the book number in brackets ("Kh. Beit Kika [25]" is record 101/86). Six Kloner [101] rows were therefore linked to records 4.1–6.8 km away, while the right records (101/68 "[7]", 101/69 "[8]", 101/86 "[25]", 101/95 "[34]") lie 7–100 m from them.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `research/regional/water_systems/scripts/build_survey.py` lines 277–286 (regexes `mh`/`mk`, target `108/2/{n}` and `{map}/{n}`).
- `water.csv` rows `WBADB-S2313-aqueduct` (dup_of `ASI-108/2/28-aqueduct`) and `WBADB-S2514-reservoir_pool` (dup_of `ASI-108/2/17-reservoir_pool`).
- Kloner rows `WBADB-S2832-cistern`→`ASI-101/7`, `S2843`→`101/8`, `S2997` and `S3000`→`101/25`, `S3004` and `S3005`→`101/34`.
- WBADB `survey_ref` in `branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv` (WBS:2313 "Hirschfeld 1983, Site 28"; WBS:2514 "Hirschfeld 1983, Site 17"; WBS:2832 "Kloner 2003, Site [101] 7").
- Distances and GLO-30 heights for all 499 links: `out/C3/water_dup_of_link_audit.csv`. 483 links are ≤ 300 m, 8 are wrong (above) and 8 are same-name links of 300–1,830 m (East Talpiyot, Har ha-Ẓofim, Kh. Irha, Bir el-Ḥajj), for review.
- Effects found in `merged_units.csv` and `build_water.py` lines 210–222 (rows with `dup_of` are not merged):
  - Zawayat's channels (the only row for Hirschfeld 1983 site 28) are missing from the 1,437 merged units.
  - S2514's pool is attached to Khureitun (itself superseded by `LITSITE:chariton`). The same Nuseib pool is still counted, but twice: `WBADB-E360-reservoir_pool` and `HAESI-HA59-038-nuseib-uweishira-reservoir_pool-50` are separate units.
  - Nine more Hirschfeld 1983 rows carry a false note "same site as ASI 108/2/N (ref), type not in ASI text": Kypros S2589 ×3, Tell el-Qasab S2479 ×2, Andrea Church S2522, Tulul Abu el-ʿAlaiq S2539, Penthucla S2732, S2601. Because a reference link skips the name-and-300 m test, those rows were never compared with the right ASI record. The Kypros basin S2589 is its own unit, not linked to ASI 109/5/7 Cypros.
Literature check (queries run, result, tag): This concerns a project table, not a publication. Repo main and `branch_only`: "Zawayat", "Hirschfeld 1983", "101/68" and "online numbering" appear only in the data rows. B2 (`out/B2/FINDS.md`) noted that ASI-online 83/1 uses its own numbering, but it reported "all Kloner rows are linked" and did not check the Map 101 links. No note in the project records these 8 wrong links. Tag: **NEW TO THE PROJECT**.
Why it might matter: `water.csv` and `merged_units.csv` are the denominators for entries 21, 22, 29, 32, 42, 45 and 46. Four of the affected rows are flagged `jericho_oasis = yes` (entry 29's Q-Jericho variant) and three are `cypros = yes`. No clause count changes for certain: the lost Zawayat row is undated and unknown on every clause, and the Nuseib pool is counted twice, not lost. The linker still treats different publications as one, and a terrain or distance check after the link would have caught all 8 wrong links.
How to confirm or kill it (with data in hand, or what is missing): In `water.csv`, compare each `dup_of` row's lat/lon with its target's (2 minutes). Then fix the regexes: require `Hirschfeld 1985` for 108/2, and for Map 101 match the bracketed "[N]" in the ASI name. Add a guard that rejects any reference link longer than 1 km, rebuild, and diff `merged_units.csv`. Kill condition: WBADB's "Hirschfeld 1983" turns out to be the same numbering as 108/2. It cannot be: site 28 is a Jordan-valley monastery in WBADB and a spring near Herodium in ASI 108/2.
Confidence: high
Touches the Copper Scroll? maybe: it changes the inventory behind the entry-29 and entry-45 counts (Jericho oasis, Cypros), not any reading.

---

FIND CARD
Title (one line): WBADB's survey row "Lower Herodium" (WBS:4287, Hirschfeld 1985 site 4) carries the grid of the hill-top palace-fortress, and the project uses it as the end point of the Artas–Herodium aqueduct
Lane: C3
What is odd (2–4 sentences): WBS:4287 "Lower Herodium" (large pool, gardens, service buildings) has OIG 172900/119300. That is exactly the grid of WBE:831 "Herodium, the palace-fortress" (peristyle court, cisterns, tunnels). GLO-30 puts this point at 729 m, about 80 m from the summit cell (746–749 m), on the upper cone. Within 300–450 m in every direction from the summit the ground drops to 630–650 m, where Lower Herodium lies (herodium.org: the 70 × 45 m pool "stands at the center of lower Herodium"). The project carries the fortress-grid point as `site_points.csv` `wbadb:S4287`. It is the destination of `LIT-MAZ-HERODIUM-AQ` (Mazar's aqueduct from ʿEin Artas to the Lower Herodium pool) and the position of `WBADB-S4287-cistern` and `-reservoir_pool`. So the aqueduct's recorded end sits about 80–95 m above the pool it fed. The aqueduct's head, `LIT-MAZ-ARTAS-SPR`, is placed on Rujm Artas (WBS:4223), at 840 m: 97 % of the way up the local 300 m relief, with a D8 catchment of 0.01 km², which a spring cannot occupy. The excavation row WBE:833 "Lower Herodium" (173000/119100, 703 m) is also on the slope.
Evidence (exact sources: file path / page / figure / frame / coordinates): WBADB rows WBS:4287, WBE:831, WBE:833 (`branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv`). `research/regional/water_systems/site_points.csv` (`wbadb:S4287`, `wbadb:S4223`). `water.csv` `LIT-MAZ-HERODIUM-AQ` (dest point, precision 350 m), `LIT-MAZ-ARTAS-SPR`, `LIT-MAZ-ARTAS-DAM`. GLO-30 profile northward from the summit, every 30 m: 745, 748, 746, 740, 724, 709, 698, 686, 675, 668, 659, 650, 644, 638, 635 m. NE profile: 745 … 640 m at about 550 m. The values are in `private/C3/water_terrain.csv`. herodium.org "The Great Pool in Lower Herodium" (https://herodium.org/?p=2057).
Literature check (queries run, result, tag): Repo: no note says that S4287 duplicates the fortress grid. The water lane's §6 rule 2 accepts WBADB points with +250 m precision, but it does not test them against the terrain. Web: "Lower Herodium large pool north foot of the hill Netzer" found herodium.org, which gives the pool's size and capacity (10,000 m³) but not its grid. No WBADB erratum found. Tag: **NEW TO THE PROJECT** (WBADB record-level; **NEW TO THE LITERATURE** if WBADB has no erratum).
Why it might matter: The aqueduct's end point carries a 350 m precision label. GLO-30 shows that the error is in height as well as in plan: the point sits on the fortress cone, not at the pool level. Any gradient or "head above destination" test that uses these points would be biased by about 80–90 m at the lower end. The head spring's placement on a summit would bias it by an unknown amount at the upper end. The WBADB grid copy also merges the two halves of Herodium in any count that uses WBADB points.
How to confirm or kill it (with data in hand, or what is missing): Read the Lower Herodium plan in Netzer, *Greater Herodium* (Qedem 13, 1981), or Netzer 2001 (folder 02) for the pool's grid. Mazar 1989 Fig. 23 (JRA 46 p. 243) gives the aqueduct's end. Check that the pool lies at about 630–650 m, more than 350 m from WBS:4287. Kill condition: WBS:4287 was meant as a whole-site point for "Herodium" and the "Lower" is only a label. That is unlikely, since WBE:831 exists separately for the fortress. For ʿEin Artas, a spring position is needed (Overpass was unreachable, see Blocked inputs).
Confidence: medium (the grid copy is certain; how far it is from the pool needs the plan)
Touches the Copper Scroll? no

---

## Dead ends

- Published fortress elevations against GLO-30, all consistent within DSM error:
  - Hyrcania: Patrich, JRA 46 p. 336, peak 248 m asl; GLO-30 245 m.
  - Alexandrion/Qarn Sartaba: Amit, JRA 46 p. 306, 375 m; GLO-30 371 m. Ras Kunetra 320 m; GLO-30 313 m.
  - Amit's Ras Kunetra catchment, "c. 400 dunams" inside a "c. 5 km" aqueduct loop: the closed region above 282 m around Ras Kunetra is 351 dunams with a 4.9 km perimeter. Consistent; no uphill run and no impossible catchment.
- The three `water.csv` aqueducts with destination points (Artas–Herodium, Hyrcania N, ʿEin es-Sultan–Qasr el-Yahud) all descend on GLO-30 (840→729, 309→236, −209→−363 m). No uphill channel was found in the rows that carry a route.
- Mandate 1:20,000 "trig" labels (32 in `mandate_maps/features.csv`, e.g. Hyrcania "848") are station numbers, not heights. They do not convert to GLO-30 heights in feet or metres.
- Springs and dams more than their stated precision from a D8 channel (≥ 0.05 km²): 48 of 124. The test is not informative, because hillside springs and terrace dams on gullies smaller than 0.05 km² are normal (as in F's failed dam test). Only the LIT fallback points (Solomon's Pools springs on Kh. el-Khawkh; Artas spring and dam on Rujm Artas) are clearly terrain-impossible. They carry a 350 m label. List: `private/C3/spring_dam_channel.csv`.
- Summit reservoirs with no feeder within 1 km (40 of 206 `reservoir_pool` rows): almost all are ASI hill-country ruin centroids (Kh. el-Burj, Nebi Samwil, Kh. Almit, …), where roof and courtyard runoff is the normal source. No capacity data (only 36 rows have `capacity_m3`), so I could not compare the catchment with the volume.
- Caves more than 300 m from any 30 m cliff (73 of 561):
  - Most are misprints that the cave lane already flagged (A41 XIII/14, II/19, XII/52–53, XI/19; E756) or shared site points (ASI 109/4-23, 109/4-29, 147-377).
  - The one unexplained cluster is ʿAtiqot 41 Region X (27 of 57 caves more than 150 m from a cliff, 14 on ground with less than 30 m relief, around −300 m). It is probably the marl terrace below DEM resolution, but I found no source for its geology. Note for F: its P5 "cliff host" predicate cannot see this group.
- Cave height statements (ʿAtiqot 41 II/1, II/3 "30 m above the channel"; XIII/8 "c. 200 m above the Dead Sea"; ASI 109/7-98-C39 "20 m above the wadi") agree with GLO-30 within 10–35 m.
- F's 150 P4a depressions: 10 lie within 150 m of a recorded water row. The deepest (up to 28 m, 3 ha) look like quarries or landfills by size. I did not check them against imagery (budget). List with coordinates in `private/C3/p4a_vs_records.csv`.
- The Aqueducts volumes for more printed elevations: the JRA 46 text layer is a two-column draft OCR, and Judean Desert chapters give few absolute heights. The Hebrew 1989 PDFs in the bucket have no text layer.

## Blocked inputs

- `https://overpass-api.de/api/interpreter` (OSM query for ʿEin Artas and the Solomon's Pools springs): curl error 35 "Recv failure: Connection reset by peer"; agent proxy "ws_closed_mid_exchange".
- `hexview.py pdf-search` with a long regex gave "ugrep: error … exceeds complexity limits". A simpler query returned no hits for "Lower Herodium".
- Hebrew *Aqueducts of Ancient Palestine* 1989 (`Amit-Hirschfeld-Patrich-eds-1989-…-9b4ae0b2`, `…-47ac5e2b`): 354 pp. with no text layer (0 text pages), so it was not searched.

## Seed / reproducibility

Deterministic. Run `python3 -I private/C3/scripts/build_dem.py DEM_DIR OUT_DIR` with the two tiles saved as `N31_00_E035_00.tif` and `N32_00_E035_00.tif`; it produces a 3,371 × 2,124 grid in UTM 36N. Then run `water_terrain.py`, `caves_terrain.py` and `p4a.py`; `samp.py` is the shared sampler. The cliff mask is F's primary setting: slope ≥ 30° and 150 m relief ≥ 30 m. The link audit was computed from `water.csv` alone (haversine-free planar approximation; distances ±1 %).
