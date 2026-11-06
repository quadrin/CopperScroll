# Side-quest C1c, round 2: NW Dead Sea shore (Qumran–Feshkha–Ghuweir to ʿEn Gedi), change across image epochs (6 Nov 2026)

Lane C1c, round 2 (rules of `ROUND2.md`). Round 1 (`out/C1c/FINDS.md`, review R4) left three cards. Two of them depended on the claim that GLO-30 sits about 5 m above the 1974 lake level, and both needed a gauge value. Round 2 found the official monthly gauge series and tested the claim on 12 image dates, 1967–2010. **The claim fails.** GLO-30 agrees with the gauge to within about ±1 m on the shore plains. The round-1 June 1974 waterline was drawn too far landward. Card 1 gives the test and its consequences for round-1 cards C1c-2 and C1c-3. Card 2 is an error in the gauge series itself.

Nothing in the repository was changed. No coordinates of unrecorded features are in this folder. The public CSVs hold only shoreline positions along fixed UTM 36N northings, plus the official level series. Private products are in `private2/C1c/`: scripts, transforms, frame footprints, a Wayback image pair and the HEXAGON re-picks.

**New inputs (all open, AI-only access):**
- **Israel Hydrological Service, Dead Sea level** (`מפלס ים המלח`), on data.gov.il. Resource `823479b4-4771-43d8-9189-6a2a1dcaaf10`, read through the CKAN `datastore_search` API: 695 readings, 1 Oct 1976 to 1 Nov 2026. The direct CSV download returns 403 (see Blocked inputs). Copied to `deadsea_level_ihs.csv`.
- **Landsat Collection 2** through the Microsoft Planetary Computer STAC (no login): TM/ETM+ L2 surface reflectance from 1984, and MSS L1 for 1973–1983.

---

FIND CARD
Title (one line): Checked against the official Dead Sea gauge at 11 Landsat waterlines (1980–2010), GLO-30 is within about ±1 m on the west-shore plains. Round 1's "+5 m" came from a June 1974 waterline drawn a median 89 m too far landward. This kills the DEM half of round-1 card C1c-2 and all of C1c-3.
Lane: C1c
Round-1 link: C1c-2 (kill test run; the DEM reading is killed and the waterline table is corrected); C1c-3 (killed)
What is odd (2–4 sentences): Round 1 sampled GLO-30 on its June 1974 waterline and got a median of −392.4 m, about 5 m above the expected lake level, and read this as a DEM bias. A gauge-based test finds no such bias. On 11 dates from 1980 to 2010, the median of (GLO-30 at the Landsat waterline − gauge level on that day) ranges from −1.0 to +0.9 m on the plain transects, with one outlier of +3.0 m (1999). The Landsat MSS waterline of 29 June 1975 sits a median **89 m (IQR 40–172 m) lakeward** of round 1's 1974 picks. It coincides with the GLO-30 −397.6 m contour (DEM median at the line −397.2 m). The 1974 lake cannot have stood 5 m higher than in 1975, so round 1's anomaly was a landward picking or registration bias in the 1974 line. Site 139a then fails outright: GLO-30 at its WBADB point is **−373.0 m**. That is about 24 m above the 1974–75 lake and 15.6 m above the highest level of the last two centuries (−388.6 m in 1896, USGS OF 78-176 p. 1). The point was never in the lake.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `out2/C1c/glo30_vs_gauge_by_date.csv`: per-date medians, IQR and n. It uses transects N 3481.0–3507.5 km with GLO-30 slope < 8 %.
  - 1980-10-06 MSS: +0.39
  - 1983-07-10 MSS: −1.01
  - 1984-10-24 TM: +0.22
  - 1987-09-15: −0.28
  - 1990-07-21: +0.54
  - 1993-09-15: +0.73
  - 1996-11-10: +0.92
  - 1999-10-02: +3.03
  - 2002-11-19 ETM+: −0.80
  - 2005-09-16: +0.15
  - 2010-10-16: +0.18 m
- `out2/C1c/landsat_waterlines_1980_2010.csv`: every transect and date, with scene ID, gauge level, shore easting, DEM value and slope.
- `out2/C1c/hexagon1974_vs_mss1975_waterline.csv`: round-1 1974 pick, the MSS 1975 pick and the GLO-30 −397.6 m crossing, per transect.
- `out2/C1c/pre_gauge_waterlines_1967_1975.csv`: waterlines from before the online gauge series. The GLO-30 median at the line is:
  - MSS 19 Jan 1973: −397.2 (IQR −398.7 to −396.8);
  - MSS 29 Jun 1975: −397.2 (IQR −398.1 to −396.7);
  - CORONA 26 Sep 1967, DF042 tile d: −397.5 (IQR −399.9 to −395.9; registration ±100 m, so weak).
- Waterline rule (scripts `private2/C1c/scripts/ls_shore.py`, `run_series.py`, `run_mss.py`):
  - band: SWIR1 for TM/ETM+, NIR for MSS;
  - threshold halfway between deep water and the 75th percentile of the profile;
  - walk west from the lake to the first sustained land run, with a sub-pixel crossing;
  - MSS scenes are phase-correlated to TM 1984 (shifts 11–66 m);
  - GLO-30 tile `Copernicus_DSM_COG_10_N31_00_E035_00_DEM` is sampled bilinearly.
- GLO-30 flattens the lake at exactly −427.0 m (711,040 water-mask pixels). The gauge read −424.2 to −429.0 m during the 2011–15 acquisitions.
- Site 139a: WBADB WBS:4495. DEM −373.0 m, slope 0.098; its position is in `private/C1c/site_observations_private.csv`.
- **Three regimes in the residuals** (same CSV):
  - (a) Plains (Kidron–Mazin, Ghuweir, south to ʿEn Gedi): about 0 m.
  - (b) Steep shores (the Ras Feshkha cliff foot, N 3508.5–3511.5; a cliff stretch at N 3500.5–3501.5) and the ʿEinot Tsukim/Feshkha spring zone (N 3512–3514). Positive, and growing with the date: at N 3513.0 the residual rises from +0.1 m (1980) to +16.7 m (2010). At the cliffs the line meets ground too steep for the 30 m DEM. In the spring zone, wet ground is taken for water.
  - (c) Wadi mouths: the DEM lies **below** older water levels, by less for later lines. At N 3495.0 (31.567° N) the residual is −17.4 m (1980), −16.2 (1984), −12.2 (1990), −8.4 (1999), −4.4 (2005), −1.9 (2010). At N 3482.5 (31.454° N, the ʿEn Gedi fans) it is −15.6 m (1980), −10.9 (1984), −8.5 (1999), −3.1 (2010). The land surface at those old shorelines has been cut down since they were exposed, by delta entrenchment (Bowman et al. 2007; see below).
Literature check (queries run, result, tag):
- Repository main and `branch_only`: "data.gov.il", "823479b4", "Hydrological Service", "Landsat", "lake level", "dead sea level". There is no gauge series and no Landsat use. Run F uses `L_sea −395 (−390…−400)` (`branch_only/claude__novel-2026-10-30-F/.../run_predicates.py` l. 39). Run 23 measures from the −395 m contour (`branch_only/sandbox__methods/sandbox/wadi_aggradation_2026-10-30/RESULT.md` l. 25–28).
- Web: "Dead Sea water level data table yearly Hydrological Service data.gov.il מפלס ים המלח" found the dataset. "Copernicus GLO-30 DEM accuracy Dead Sea exposed lake floor Landsat shorelines lake level validation" found nothing specific. Mapping Dead Sea shorelines from Landsat is well published, and so is fan entrenchment (Bowman et al. 2007, cited in run 23).
- Tag: **NEW TO THE PROJECT** (the gauge series; the GLO-30 test on the exposed floor; the corrected 1974 line). The wadi-mouth deficits are **KNOWN BUT UNDER-DISCUSSED**: the process is published, and these are per-transect numbers.
Why it might matter:
- (1) Round-1 C1c-2 said that if GLO-30 ran about 5 m high, every shore distance in runs 23 and F would be off by 100–200 m. That correction is withdrawn: on the plains GLO-30 contours can be used as period shorelines to about ±1 m (about ±30 m horizontally at 3 % slope).
- (2) That does not hold at wadi mouths (Darga area, ʿEn Gedi fans), at the Ras Feshkha cliff or in the Feshkha spring zone.
- (3) Round-1 `out/C1c/shorelines.csv` (1974 rows) should be read as 40–300 m landward. Use the MSS 1975 line, or the GLO-30 −397.6 m contour.
- (4) C1c-3 is dead. B2 card 3's reliance on Bar-Adon's shore-zone grids is not weakened by it.
How to confirm or kill it (with data in hand, or what is missing):
- Re-run the script on more dates. Use the 1978-05-05 HEXAGON F007 frame (gauge −399.55 m) once it has a shore-accurate registration.
- The tile-wide homographies from coarse SIFT (`private2/C1c/T_F0*_homog.json`) are 100–400 m off at the shore; see Dead ends.
- Kill condition: a systematic Landsat geolocation bias of ≥30 m eastward on all dates. Tier-1 L2 RMSE is under 12 m, and MSS was tied to TM, so this is unlikely.
- The 1999 outlier (+3.0 m) has not been explained.
Confidence: high (GLO-30 agrees with the gauge on the plains; C1c-3 killed); medium (that the round-1 1974 offset was picking rather than registration); low (the 1967 CORONA level)
Touches the Copper Scroll? maybe. ARGUMENT (separate from the evidence): runs 23 and F place a 1st-century CE shore at −395 to −400 m. GLO-30 is unbiased on the plains, and the measured mid-1970s waterlines lie at −397 ± 1 m. The 1973–75 Landsat MSS lines (and the HEXAGON 1974 frames, once registered properly) are therefore a near-physical picture of where that shore ran on the Kidron–Mazin–Ghuweir plains. This puts Kh. Mazin, ʿEin Feshkha and Rujm el-Baḥr against a measured line rather than a modelled one. At wadi mouths the modern DEM is up to about 17 m below the 1980 surface, so ancient shore distances there need a pre-incision surface. No entry rating changes on this argument.

---

FIND CARD
Title (one line): In the official Dead Sea level series, the 1 December 1979 value (−400.14 m) is a one-month spike that the lake cannot have made (+0.94 m in November, then −0.49 m in December). It is probably a one-digit slip for −401.14.
Lane: C1c
Round-1 link: new
What is odd (2–4 sentences): The series reads −401.08 (1 Nov 1979), **−400.14 (1 Dec 1979)**, −400.63 (1 Jan 1980), −400.44 (1 Feb 1980). The −0.49 m change from 1 Dec to 1 Jan is the largest fall over a month or more in the whole 1976–2026 series. The next largest is −0.37 m over 26 days in midsummer 1995. Every other Dec→Jan change in 49 winters lies between −0.16 and +0.26 m. The +0.94 m change from 1 Nov to 1 Dec is likewise unmatched in any other November: the others range from −0.27 to +0.01 m. A rise from floods followed by an evaporative fall of half a metre in mid-winter is not physical. A datum change would persist instead of reversing, so the 1 Dec value alone is wrong. Reading it as −401.14 gives −0.06 m for November (the median November is −0.08) and +0.51 m for December, which fits the large rise of winter 1979/80 (the lake reached −399.65 m by 1 June 1980).
Evidence (exact sources: file path / page / figure / frame / coordinates): `out2/C1c/deadsea_level_ihs.csv`, rows 1979-11-01, 1979-12-01, 1980-01-01. Source: data.gov.il dataset "מפלס ים המלח", resource 823479b4-4771-43d8-9189-6a2a1dcaaf10, `datastore_search` records with `_id` near the end of the 695-row list, read 6 Nov 2026. The spike scan, a ±0.25 m deviation from the neighbour mean with a reversed sign, also flags a smaller and plausible March 1991 bump (−407.73 → −407.31 → −407.60), left as is.
Literature check (queries run, result, tag): Web: "Dead Sea level 1979 1980 winter flood rise -400 metres December 1979 January 1980 Hydrological Service monthly level"; `"400.14" OR "401.14" Dead Sea level 1979`. No publication or erratum found. Repository: no copy of the series. Tag: **NEW TO THE LITERATURE** (tentative; the IHS yearbooks were not checked).
Why it might matter: The series is the reference for every Dead Sea level-by-date calculation, including the validation in card 1 (its 1980-10 date is not affected). Anyone who fits seasonal or annual rates over 1979/80 inherits a spurious +0.9 m peak.
How to confirm or kill it (with data in hand, or what is missing): Compare with the IHS hydrological yearbook for 1979/80, or with the Arab Potash Company gauge. Neither is in the corpus. An image test is possible: a Landsat MSS scene near 1 Dec 1979 against scenes from November 1979 and January 1980 (path 187 row 38; scenes listed by `ls_shore.search`). A 0.9 m rise moves the shoreline about 30 m on 3 % slopes, which is at the edge of what MSS can show. Kill condition: a source that prints −400.14 for December 1979 together with a flood record.
Confidence: medium-high (that the value is wrong); low (the exact correct value)
Touches the Copper Scroll? no

---

## Round-1 follow-ups (not new finds)

- **C1c-1 (roads at Bar-Adon 117a and 120):** dating narrowed. The paved two-lane corridor beside 117a, and the tracks that wrap the ring at 120, are already on the image behind the earliest Esri Wayback release (2014-02-20, release 10). Its metadata service gives WV02 0.5 m, captured **23 Feb 2011**, for both points (`metadata.maptiles.arcgis.com/.../World_Imagery_Metadata_2014_r01/MapServer/identify`). So the road and the tracks were built between 25 June 1974 and 23 Feb 2011. Private image pair: `private2/C1c/wayback_117a_120.jpg`. R4's verdict on the identity claim stands.
- **C1c-2:** see card 1. The waterline table is kept, but it is biased landward. The DEM bias is withdrawn.
- **C1c-3:** killed (card 1).
- **ʿEn Gedi coverage (open from round 1):** no historical frame in the store reaches ʿEn Gedi. Footprints were estimated by coarse SIFT of 1/32 overviews against Landsat TM red at 30 m (`private2/C1c/frame_footprints.json`):
  - Dec 1974 F018 tile b runs south to about 31.54° N (the Darga area), about 9 km beyond June 1974 F015 (31.62° N).
  - Dec 1974 F017 b ends at about 31.68° N.
  - 1978 F007 c ends at about 31.70° N; F006 lies further north.
  - CORONA DF042 tile d ends at about ʿEin el-Ghuweir.
  - For ʿEn Gedi, Landsat MSS (from 1972) and TM (from 1984) are the only historical epochs. Their waterlines reach N 3481 km (`landsat_waterlines_1980_2010.csv`).
- **Automatic matching (round-1 dead end, partly reversed):** SIFT of HEXAGON and CORONA overviews at about 28 m/px against Landsat TM red at 30 m works where SIFT against Esri at 2–16 m failed. It gives 32–578 inliers per tile. F007 c has 578 inliers with an 18 m median residual. It is good for footprints, but not for shoreline work (next section).

## Dead ends

- Tile-wide homography (1/32 SIFT → Landsat) used to re-pick the HEXAGON waterlines: the inlier residuals are 18–26 m, but at the shore the transform is 100–400 m off, because of panoramic distortion and ties far from the lake. On F015 d the picks land on the Ras Feshkha cliff; on F018 b the DEM median is −403 m, impossible for Dec 1974. Not used. A shore-accurate HEXAGON line needs ties placed by hand along Route 90, as round 1 did.
- CORONA 1967 level: a quadratic transform from 243 ties (Judean hills plus the Jordan farmland), interpolated across the lake. Waterline DEM median −397.5 m, but ±100 m scatter against the MSS 1975 line. Too weak to give a 1967 level.
- MSS 31 May 1977 and 26 May 1978: the picks fell in the lake (DEM −427), probably from haze or glint, so the dates were dropped. MSS 9 Sep 1975: phase-correlation response 0.02, dropped. MSS 1983 (LM04, T2): extra −10 to −20 m residuals at N 3485–3487 on that date only, an artefact.
- WBADB sweep for recorded points on the exposed lake floor (GLO-30 < −385 m): Rujm el-Baḥr (site 86, −397.6) is a known island or peninsula site. "Cave Q-3" (WBE:750) on the plain east of Qumran is already flagged in `caves_entry25` (as E756, Jones 1978, "doubtful"). The 2Q grid misprint (XI/19, 19343/12391) is already flagged in `caves.csv`. "Mizpe Qedem" (WBE:907, DEM −409 m) was not followed up.
- GLO-30 water-body editing: no inland ponds flattened to −427 m west of the Oct 2010 shoreline, so the wadi-mouth deficits are not an editing artefact. The other WBM components (−388 to −397 m) are the southern-basin evaporation ponds.
- No published 1967, 1968 or 1974 gauge values were found on the web. The USGS OF 78-176 text gives only 1818, 1896 and "near −400 m in 1977". Its 1967–76 IHS readings are only plotted.
- Bavarian 1918 and RAF 1940s for this shore: not reached.

## Blocked inputs

- `https://data.gov.il/dataset/ebf0005b-f5fe-4c6c-ab6d-28778167d025/resource/823479b4-4771-43d8-9189-6a2a1dcaaf10/download/823479b4-4771-43d8-9189-6a2a1dcaaf10.csv` returned an HTTP 403 CloudFront error page. The CKAN API (`/api/3/action/datastore_search?resource_id=…&limit=1000`) works and gives the same table.
- The IHS hydrological yearbooks (needed to confirm card 2) are not in the corpus.

## Reproducibility

- Scripts: `private2/C1c/scripts/`.
  - `ls_shore.py`: STAC search, signing, waterline rule, DEM sampling. It reads the DEM from `scratch/C1c2/glo30_N31E035.tif`, downloaded from `copernicus-dem-30m.s3.amazonaws.com`.
  - `run_series.py`: TM/ETM+ dates.
  - `run_mss.py`: MSS dates, phase-correlated to TM 1984.
  - `coreg_corona.py`, `corona_shore2.py`: CORONA.
  - `footprints.py`, `hex_shore.py`: HEXAGON.
  - `wayback.py`
- Transects: every 500 m of UTM 36N northing, N 3514.0–3481.0 km, sampled every 5 m from E 722000 to 742000.
- Deterministic. Scene IDs are in every CSV row.
