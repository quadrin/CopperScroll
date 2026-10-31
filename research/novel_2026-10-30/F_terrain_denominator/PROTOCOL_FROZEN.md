# Direction F: a terrain-derived denominator. Frozen protocol (30 Oct 2026)

Worker F, branch `claude/novel-2026-10-30-F`, repository base `7a3b3074`. This file is frozen by its SHA-256 (`PROTOCOL_FROZEN.sha256`), and that hash goes in the commit message. The commit is pushed **before** the confirmatory run. Any change after the run is a new exploratory model and is labelled as one.

## 0. Claim and question

**Question.** In each fixed region, how many places exist where each of the scroll's physical landform and water words is *physically possible* on the terrain? The count includes every such place, excavated, surveyed or not.

**Claim tested.** A 30 m elevation model can turn at least one of these words into a predicate whose count is stable across its frozen sensitivity range, and that the DEM can resolve. A stable count gives a terrain denominator. It is set by the terrain, not by excavator labels or survey coverage. Against it, an existing inventory count such as Koḥlit k = 0 of 333, caves 635 or water installations 1,437 can be read as a landscape rate rather than a record rate.

**What it cannot do.** It identifies no place. It says nothing about deposits. It cannot tell a built installation from bare ground. A terrain-possible place is a *host*, not a find.

## 1. Inputs (sha256)

| Input | Path / URL | SHA-256 |
|---|---|---|
| GLO-30 DEM N31 E035 | `https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N31_00_E035_00_DEM/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif` | `29baca4a170117c090c2ab1f2a4ade53ed1dd085cdbbfaa005631049462221cf` |
| GLO-30 DEM N32 E035 | same pattern, `N32_00_E035_00` | `5b088dc8b6d9fab50873ea6daf7459141b4ee2e52cdd23b73297adf6bf602d22` |
| GLO-30 water body mask (WBM) N31 | `…_N31_00_E035_00_DEM/AUXFILES/…_WBM.tif` | `35fcfd9fb9ac9cc72fe39e40985d2cea78c601456440d195b8ef5b0f47c68578` |
| GLO-30 WBM N32 | same pattern | `1aca5f8677aa11b5622ccffc504e28be0c68c6d5b29a79d52bc1654c43f7314d` |
| West Bank polygon | geoBoundaries gbOpen PSE ADM1 (`media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/releaseData/gbOpen/PSE/ADM1/geoBoundaries-PSE-ADM1.geojson`), feature `PS-WBK` | `ac658278bbdec81eade7875ae260565ce881d1076376ee9a60e3b12c648b9f59` |
| Jordan polygon (east-bank mask) | geoBoundaries gbOpen JOR ADM0 | `9234e16ba454e5f5ffc43d34a5941c2f98c7727f2d559c4195006f7d86b72c7d` |
| Mosaic, UTM 36N, 30 m | `dem_utm30.tif` (made by `scripts/prep_dem.py`) | `edf05d1c51474dc25d024e2aaaf66a28bfddf1506732fc41edaabd7cce28f00b` |
| WBM mosaic | `wbm_utm30.tif` | `1235c785a8063ed084bdb26c27b4040c35db2dc72c1a62e7314d1b0bf4e047d8` |
| Derivatives (`scripts/derivatives.py`) | `dem.npy` `17fb8ddf…`, `slope_deg.npy` `e5fcac20…`, `aspect_deg.npy` `428e9d10…`, `relief150.npy` `71b08bc5…`, `svf300.npy` `840544a3…`, `acc_km2.npy` `9923033f…`, `fdir.npy` `1388e1ff…`, `filled.npy` `e0e29bcf…`, `water.npy` `5d2faa3a…` | full hashes in `inputs.sha256` |
| Cave inventory | `research/regional/caves_entry25/caves.csv` (read only) | `16ab5e3437f317fcb01a36639f66beb05c956ad49d9250a1308cd72287528f2d` |
| Water inventory | `research/regional/water_systems/water.csv` (read only) | `8feee7e4be21443ca73279b8d1607bae96c0be74abf68132976c70e24f2d16aa` |
| Koḥlit units | `research/rarity/kohlit/stage1a/stage1a_units.csv` (read only) | `4879fea0e57740015eab79ac31adfdb050ac1b67099c1386855110175bed8015` |
| Scripts | `scripts/prep_dem.py` `7217c1f3…`, `scripts/derivatives.py` `18d872f2…`, `scripts/run_predicates.py` `6b8f2e8c…` | full hashes in `inputs.sha256` |

Software: numpy 2.5.3, scipy 1.18.1, rasterio 1.5.2, pysheds 0.5 (patched: `np.in1d = np.isin`), pyproj 3.8.0, shapely 2.2.0. The rasters stay outside the repository, in `/root/novel/data_F/`.

**No SULTAN-1 HEXAGON material, no reserved image and no scroll photograph is used.**

### DEM limits (recorded before the run)

- **Modern surface.** GLO-30 is a **DSM** from TanDEM-X, acquired 2011–2015 ([Copernicus Data Space COP-DEM description](https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM)). It includes buildings, roads, quarries, terraces, the Jericho town and camps, the Dead Sea evaporation ponds and the lake at its 2011–2015 level, about −425 m. None of that is the 1st-century surface.
- **Accuracy.** The stated absolute vertical accuracy is < 4 m (LE90). Relative accuracy is < 2 m on slopes ≤ 20 % and < 4 m on steeper slopes. A closed depression shallower than about 2 m therefore cannot be told from noise. That is why `d_min` has a primary value of 2 m and a range of 1–4 m.
- **Resolution.** The grid is 30 m. A cave mouth (1–5 m), a cistern or a pool of 3–30 m a side is smaller than one cell. Predicates P4 and P5 therefore count **host terrain**, a place where such a feature can exist, never the feature itself (§4, F-B).
- **Hydrology.** D8 flow on a depression-filled, flat-resolved surface (pysheds). Modern dams, road embankments and the canals of the Jericho oasis are part of the surface.

## 2. Regions (fixed before any count)

All regions are fixed now, by geography or by an existing project boundary. None is fitted to a candidate. Each excludes the Jordan polygon (east bank) and, through the land mask, modern water and the lake below the period level `L_sea`.

| Id | Boundary | Source of boundary |
|---|---|---|
| **RF1** | Qumran–Jericho–Wadi Qelt–lower Kidron block: Old Israel Grid (EPSG:28191, no false northing) E 180,000–200,000, N 118,000–146,000 | New. It holds Kh. Qumran (193616/127717), Tell es-Sultan (192181/142115), Choziba (189081/139046), Mar Saba (181467/123605), Hyrcania (184768/125169) and the Kidron outlet to the shore (N ≈ 119,700). The upper Qelt west of E 180,000 (ʿEin Fara) is outside, as in RF2. |
| **RF2** | E 180,000–197,000, N 91,000–150,000 (EPSG:28191) | The cave inventory box, `research/regional/caves_entry25/PLAN.md` §2 (635 cave rows) |
| **RF3** | WGS 84, 31.600–31.900 N, 35.120–35.560 E, west of the Jordan | The water-systems box, `research/regional/water_systems/PLAN.md` §1 (1,437 merged units) |
| **RF4** | West Bank polygon (geoBoundaries `PS-WBK`) and E > 175,000 (EPSG:28191) | Koḥlit region R1, `research/preregistration/kohlit_rarity_2026-10-08.md` §3 (N = 333 units) |

The polygon in RF4 replaces WBADB's implied coverage. Its edge is approximate (geoBoundaries gbOpen). That limit is recorded here.

## 3. Predicates: from the text to geometry

Readings and meanings come from the project's own concordances: `research/text/location_language/occurrences.json` (one meaning for every occurrence, with Puech 2015, Puech 2006 and Lefkovits 2000 pages) and `tables/landmark_lexicon_index.csv` (the 121-term lexicon, with biblical and Mishnaic usage). Each predicate is defined only from those meanings, before any count.

| Id | Text word, lines, meaning cited | Geometric predicate (cell = 30 m) | Primary | Sensitivity range | Counting unit |
|---|---|---|---|---|---|
| **P1** נחל *naḥal* | V 12 (נחל הכפא), X 3 (הנחל הגדול). Lexicon `nahal`, confidence high, 122 biblical uses, a wadi or stream bed (e.g. 1 Kgs 17:7; Deut 21:4). | A land cell with flow accumulation ≥ **A_min**. | A_min = 1.0 km² | 0.25–4.0 km² | 90 m stretch of channel (channel length / 90 m). The number of reaches between confluences is reported but not used for stability, since it scales with A_min by construction. |
| **P2** הנחל הגדול "the great wadi" | X 3 (entry 45, cistern fed by channels from the great wadi). Same lexicon row. | A channel cell with accumulation ≥ **A_great**. | 100 km² | 50–200 km² | 90 m stretch; the number of connected trunk systems is also reported. |
| **P3** שולי *shulei*, edge sense | I 11 (on the edge of the channel, Puech 2015 p. 121; Lefkovits p. 73), IV 9, IX 1, XI 7. `occurrences.json` meaning `edge_base`: "a position on the feature's margin: its edge, rim, bottom or base". | A P1 channel cell with an adjacent (8-neighbour) non-channel cell of slope ≥ **S_bank**: a break in slope at the channel margin. | A_min 1.0; S_bank 15° | A_min as P1; S_bank 10–25° | 90 m stretch of banked channel |
| **P3b** שולי, outlet / end sense | Same lines. Meaning `outlet_end` (Milik 1962; Puech 2006 p. 208 "au bout du canal", p. 210 "à la sortie"). | A channel junction (≥ 2 channel cells draining in) or a terminal outlet (a channel cell draining off land, into the lake, the edge or a water cell). | A_min 1.0 | 0.25–4.0 | point |
| **P4a** ברכה *berekhah*, closed basin | II 13 (pool east of Koḥlit; Puech 2015 p. 123, Lefkovits p. 135 "the pond"). Lexicon `berekhah`, confidence high: an open pool (2 Kgs 20:20; Neh 3:15–16; Eccl 2:6). | Natural closed depression: (filled DEM − DEM) ≥ **d_min**, not touching modern water cells. | 2 m | 1–4 m | 8-connected cell cluster |
| **P4b** ברכה, runoff-fed pool host | Same. A built or rock-cut pool must lie where it can be filled by runoff or a channel, on ground flat enough to hold a basin. | slope ≤ **S_pool** and accumulation ≥ **A_pool**. | S_pool 5°; A_pool 0.05 km² | S_pool 3–8°; A_pool 0.02–0.2 km² | 8-connected cluster |
| **P5** מערה *mearah* above a channel | II 3, VI 1, VI 7, VII 8 (cave; all editions). Lexicon `mearah`, confidence high. "Above a channel" follows the task brief and the על פי "above the mouth" sense (VII 14, Puech 2015 p. 133). The scroll itself gives no explicit cave-over-wadi line, so P5 is a project composite and is labelled as one. | Cliff cell: slope ≥ **S_cliff** and local relief (max − min within 150 m) ≥ **H_cliff**; within **D_cliff** of a P1 channel cell; and ≥ 10 m above its nearest channel cell. | S_cliff 30°; H_cliff 30 m; D_cliff 150 m; A_min 1.0 | S_cliff 25–40°; H_cliff 20–50 m; D_cliff 90–300 m; A_min 0.25–4 | 8-connected cluster (a cliff face) |
| **P5e** cave "facing east" | VI 2 (entry 25 הצופא מזרח), VI 8–9 (entry 26 "facing east"). | A P5 cell with downslope aspect 45–135°. | as P5 | as P5 | cluster |
| **P5x** (control) | none: any cliff | The cliff condition of P5 without the channel condition | as P5 | as P5 | cluster |
| **P6** צוק *tsuq* "gorge" | VIII 8 (mouth of the Kidron gorge), IX 14 (Puech 2015 "the gorge"; Lefkovits "the peak"). `occurrences.json` meaning `gorge`. | A P1 channel cell with a sky-view factor (radius 300 m, 16 azimuths; Zakšek et al. 2011) ≤ **V_gorge**. | 0.75 | 0.70–0.80 | 90 m stretch |
| **P6m** פי הצוק "mouth of the gorge" | VIII 8, IX 14 | A gorge cell whose next 5 downstream cells (≈ 150–210 m) are channel and not gorge: the gorge opens. | as P6 | as P6 | point |
| **P7** הים "the sea" | Only in the sense "the Dead Sea" (the task's predicate). The text's ים at IX 7 means "the sea = west" (Milik, Lefkovits) or reads "south" (Puech), and at X 8 and X 15 it means "basin" (`occurrences.json` `yam`). No line of the scroll names the Dead Sea as ים. P7 is therefore a **project geographic predicate, not a text predicate**, and is labelled so. | Land cells within **D_sea** of the period lake. The period lake is every cell below **L_sea** that is 8-connected to the modern WBM lake. | L_sea = −395 m; D_sea 1 km | L_sea −390 to −400 m; D_sea 0.5–2 km | km of period shoreline; band area km² |

**Why L_sea = −395 m (−390 to −400 m).** Sandbox run 23 (`sandbox/wadi_aggradation_2026-10-30/RESULT.md`, lines 24–27) cites Hirschfeld 2004 p. 39 (after Frumkin 1997) for −395 to −400 m in the 1st century CE. Frumkin et al. 2001 Table 1 gives a maximum near −390 m for 2100–1700 ¹⁴C BP. This worker did not check those sources again.

**Why the other values.**
- A_min = 1 km² is about 1,100 cells: a wadi that carries floods, not a rill. Its range spans a factor of 16.
- S_bank = 15° is a clear break from a floor of < 5°.
- S_cliff = 30° with 30 m of relief is the scale at which the Judean Desert cave cliffs appear on a 30 m grid. Slope on 30 m cells underestimates vertical faces, hence the low end of 25°.
- D_cliff = 150 m is 5 cells.
- V_gorge = 0.75 is roughly the 5th percentile of SVF over the whole mosaic (0.786). This was seen in the exploratory phase; it is not tuned on any region count.
- S_pool and A_pool describe a site that can catch runoff from at least 5 ha (0.05 km²).

## 4. Counting and failure conditions

**Counting.** Every predicate is counted in every region at its primary values. It is then counted again at the low and the high end of each of its parameters, one at a time, the others held at primary. The rows go to `predicate_counts.csv`. The land mask is `valid DEM & not WBM water & z ≥ L_sea`.

**F-A, stability (per predicate, per region).** Let R be the ratio of the maximum to the minimum count over the predicate's settings. If R > 10, or if the minimum is 0 while the maximum is above 0, the predicate is **UNSTABLE** in that region, and its count may not serve as a denominator. P1_nahal_reaches and LAND are excluded from this test.

**F-B, resolution.**
- **(i) Scale test.** A predicate whose text feature is smaller than 2 cells (60 m) cannot be resolved as a feature. P4a, P4b, P5 and P5e are declared **host-terrain** predicates (fixed now). A pool, cistern or cave mouth is sub-cell.
- **(ii) Empirical test.** Recorded features with point precision ≤ 50 m must fall on or near the host terrain more often than chance.
  - **RT_cave_cliff:** cave rows in RF2 within 60 m of a P5x cliff cell. The test passes if recall ≥ 0.5 and recall ≥ 2 × the areal base rate (the share of RF2 land within 60 m of a cliff cell).
  - **RT_dam_channel:** dam rows in RF3 within 60 m of a P1 channel cell, with the same pass rule.
  - If RT_cave_cliff fails, P5, P5e and P5x are **NOT RESOLVED**: their counts are reported but carry no rarity reading. If RT_dam_channel fails, the same applies to P1, P2, P3, P3b and P6.
  - The recall of the full P5 predicate and of P4 for pools is reported as informative only.

**Direction-level outcome.**
- **Obtained:** at least one text predicate (P1–P6) is stable (F-A) in RF1 and RF2 and resolved (F-B ii, where a test applies), and the Koḥlit terrain denominator (§5) is computed.
- **Partly:** at least one text predicate is stable and resolved in at least one region, but some named predicates are unstable or unresolved.
- **Not obtained:** no text predicate is stable and resolved in any region.

## 5. Inventory comparison and the Koḥlit reading (fixed now)

**Coverage.** For a terrain unit (a P5x cliff cluster or a P5 cluster in RF2; a P4 host cluster, P4a or P4b, in RF3), count the units that hold at least one recorded cave or pool point within 60 m. Coverage = units with a record / all units.
- If coverage is below 0.5, more than half of the terrain-possible places carry no record. An inventory "k of N" then measures the record, not the landscape. Its N (635 or 1,437) is not a landscape denominator.

**Koḥlit, entries 11 and 60.** Definition from `research/preregistration/kohlit_rarity_2026-10-08.md` §4 and `research/rarity/kohlit/README.md`:
- **C1** is a pool east of the unit, at a bearing of 45–135° and ≤ 1 km (sensitivity ≤ 0.5 km and ≤ 2 km).
- **C2** is a non-funerary cavity north of the unit, at a bearing of 315–45° and ≤ 1 km.
- The headline is k = 0, f = 20, m = 313 of N = 333 (R1, main set, branch A, survey level).

**Terrain versions.**
- **C1T:** a P4a or P4b host cell lies in the east quadrant, within R.
- **C2T_natural:** a P5x cliff cell lies in the north quadrant, within R. This covers a natural cave or pit only. A built cistern, pit or shaft (part of C2's definition) is possible on nearly any rock surface. C2 is therefore **terrain-unconstrained by definition**, and its terrain denominator is all units.
- C1T and C2T are computed for every one of the 333 unit points, and for a 300 m lattice over all RF4 land (the landscape base rate). The grid covers S_pool × A_pool × R (3 × 3 × 3).

**Reading rule.**
- If ≥ 90 % of the 333 units are C1T-possible at the primary values, the terrain does not narrow the set. The denominator of k = 0 then stays ≈ 333. k = 0 is a fact about the records: m = 313 are unknown, not terrain-excluded. It cannot be read as rarity of the combination on the ground.
- If fewer than 50 % are C1T-possible, the terrain narrows the set. k = 0 is then read against N_T = the number of C1T units, and the m units that are not C1T become terrain-excluded rather than unknown.
- Between 50 % and 90 %, the result is reported as partial narrowing, with N_T.
- The same thresholds are applied to the lattice (the share of all RF4 land locations), as the landscape base rate.

## 6. Exposure log

- **Exploratory, before this freeze:**
  - derivatives over the whole mosaic;
  - values at eight known points (Qumran, Wadi Qumran, Mar Saba, Choziba, Tell es-Sultan, Feshkha, Hyrcania, Doq) to check that the derivatives are sane;
  - the whole-mosaic percentiles of slope and SVF, and the largest filled depressions;
  - a dry run of `run_predicates.py` on a test box outside every region (OIG E 150,000–165,000, N 95,000–110,000, Hebron hills). That run showed P5 and P5x unstable there (R ≈ 200–300, driven by S_cliff = 40°) and P2 unstable (0 at 200 km²).
- No threshold was changed after the dry run.
- One bug was fixed before this freeze: aspect had been computed as the upslope azimuth. It now gives the downslope azimuth, checked on sample cells, and the derivatives were recomputed.
- No region count, inventory recall or Koḥlit result has been computed.
