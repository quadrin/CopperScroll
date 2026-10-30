# Run 23 result (draft): how deep would a wadi-bed cache lie today?

Draft, 30 Oct 2026. Evidence agent's report for the integrator. Rule: [RULE.md](RULE.md), commit 8c6c2de, SHA-256 aaebf829d26f921c9f161ff61b91fccb217e17ec3c77e8a5f3ac54d54f914015 (checked). Exploratory. Nothing here changes main-project records.

## Verdict summary
- **No candidate point reaches a firm verdict under the strict reading.** All nine positions (P1–P8, with P4 in two) score **unknown**. No tier 1 source exists for any of them. The only tier 2 sources are qualitative, or sit on a different channel or surface.
- **One point is reachable under a lenient reading: P5 (Wadi Qelt at Choziba).** That reading counts the Netzer 2001 erosion evidence from the same catchment as tier 2. Net change is ≤ 0, so D_now ≤ 1.34 m (short cubit) or 1.58 m (long cubit). Under the strict reading P5 is unknown, leaning reachable.
- **Leans (not verdicts):**
  - Reachable: P1, P2, P3 (short cubit only), P4a, P5.
  - Deep: P6 (7 cubits = 3.12 or 3.68 m before any change) and P7 (9 cubits = 4.01 or 4.73 m, if the cache survives).
  - No lean: P4b, P8, and P3 on the long cubit.
- **Likely removed:** no point. No tier 1–2 source shows incision greater than the stated depth, or a channel moving across a point.
  - The lean is "removed" at P1, P4a, P5 (bedrock gorges, scoured to rock by floods) and P7 (a migrating river over 2,000 years). These leans rest on tier 3–4 evidence, so they cannot become verdicts.
- **Entry 17** (P2, P3) and **entry 35** (P4a, P4b) each have at least one candidate that is not leaning toward "removed". **No entry has every candidate in "likely removed".**
- **Calibration failed.** The two controls do not reproduce one rate:
  - C1, Kh. Mazin on the shore: 1–3 m of fill over a Hasmonean slipway.
  - C2, the Jericho palaces on the Qelt fan: 0.65–1.2 m of erosion below a Hasmonean floor.
  - Every D_now is therefore **uncalibrated**.

## Fixed inputs
- **Points:** fixed before any sediment source was read. [out/points.csv](out/points.csv), 30 Oct 2026 18:15 UTC, SHA-256 2e0ed7f9…37ae0. Each comes from the atlas `places` record (or a water-inventory row), snapped to the channel on a DEM.
  - P7 has no record coordinate (no ford is identified). It uses the Qasr el-Yahud record point.
  - P8 uses Milik's main-torrent branch (Mukellik/Og). Clermont-Ganneau's small-wadi branch is noted but not scored.
- **Lake level:**
  - 1st century CE: −395 to −400 m (Hirschfeld 2004 p. 39, citing Frumkin 1997). Frumkin et al. 2001 Table 1 gives a maximum near −390 m for 2100–1700 ¹⁴C BP.
  - 2022: −437 m (Frumkin 2023 p. 77).
  - Net base-level fall: 37–47 m, almost all of it after c. 1930. The 1896 level was −388.4 m (Bowman et al. 2007).
- **Rule for base-level incision:** on the west shore, entrenchment from the falling lake fades within about 1 km of the retreating shore (Bowman et al. 2007, tier 3). Measured from the −395 m contour, every point is at least 1.6 km upstream (out/form_dem.csv). The modern fall is therefore not, on present evidence, the main control at any point.
  - P7 is the exception. On the Jordan, incision had travelled 8–11 km upstream by 1983–1993 (Hassan and Klein 2002), and P7 lies 10.3 km above the DEM shore. That datum is not stated in the abstract.

## Per-point table
D_now = stated depth + net change. Each D_now cell shows the short cubit (0.445 m), then the long cubit (0.525 m). "unk" means the source gives no bound.

| Point | Entry, depth | Regime | Net change since 60 CE (m) | Tier | D_now (m), short / long cubit | Survival | Verdict |
|---|---|---|---|---|---|---|---|
| P1 Wadi Qumran below Kh. Qumran | 20, 1 cubit | incising, flood scour below the waterfall | unk to 0 (form only) | 4 | unk–0.45 / unk–0.53 | unknown, lean removed | unknown, lean reachable |
| P2 Buqeia plateau bed | 17, 3 cubits | unincised; aggrading or stable | 0 to +0.8 | 3 | 1.33–2.13 / 1.58–2.38 | unknown | unknown, lean reachable |
| P3 Wadi Nuweimeh, lower course | 17, 3 cubits | channel entrenched 7–25 m on the plain margin | unk to +1.45 | 3 (upper) + 4 | unk–2.79 / unk–3.03 | unknown | unknown; lean reachable (short), no lean (long) |
| P4a Kidron at Mar Saba | 35, 3 cubits | bedrock gorge, cut and fill | unk | 4 | unk (1.34 / 1.58 if net ≈ 0) | unknown, lean removed | unknown, lean reachable |
| P4b Kidron exit (fan apex) | 35, 3 cubits | fan apex; two-sided | unk to +3.0 | 3 (C1 transfer) | unk–4.33 / unk–4.58 | unknown | unknown, no lean |
| P5 Wadi Qelt at Choziba | 32, 3 cubits | bedrock gorge; same catchment eroding (C2) | unk to 0 | strict 3/4; lenient 2 (sign only) | unk–1.34 / unk–1.58 | unknown, lean removed | strict: unknown, lean reachable. Lenient: **reachable** |
| P6 Wadi Kuteif | 24, 7 cubits | incised valley | unk | 4 | unk (3.12 / 3.68 before change) | unknown | unknown, lean deep |
| P7 Lower Jordan at Qasr el-Yahud | 28, 9 cubits (partly restored) | meandering; incising since c. 1980 | unk | 3 + 4 | unk (4.01 / 4.73 before change) | unknown, lean removed | unknown, lean deep if present |
| P8 Wadi el-ʿAṣla / Og at the scarp | 18, none | incised fan channel | unk | 4 | unk (no stated depth) | unknown | unknown, no lean |

The single record that would narrow each range most is listed in [out/results.csv](out/results.csv). The most useful ones:
- **P4b:** the Stutchbury and Nicholl 1962 sections, giving gravel thickness over the dated floor, plus one dated section at the Kidron fan apex.
- **P5:** the level of a dated Qelt aqueduct intake or culvert near Choziba, relative to today's bed.
- **P6:** a levelled plan of the stepped chamber in Wadi Kuteif.
- **P7:** a series of channel positions at the crossing: the 1870s SWP sheet, 1940s air photos, and today.

## Calibration (C1–C2)
Both controls were chosen before any sediment source was read. The reasons are in points.csv.

- **C1, Kh. Mazin (Mezad Qidron).** A Hasmonean anchorage on the shore below the Mazin/Kidron fans.
  - Traubman 2024 (HA-ESI 136), Fig. 2: the slipway base lies at about −394 m. Over it are 1–3 m of layered sand, soil and fallen stone, read from the drawing (±0.5 m). Stutchbury and Nicholl 1962 report "later gravels" over the original floor; that is via project coding, and the PDF was not re-read.
  - Neither rate used reproduces this cleanly:
    - The terraced-field rate (Bruins et al. 2020) predicts about 0.8 m, which is too little.
    - The Jericho-plain OSL profile (Lazar et al. 2010) predicts about 1.3–1.45 m. That falls inside the observed range, but the fill is partly wall collapse and lake-margin sediment. The lake also stood above −394 m in 1896 and in the 4th and 11th–12th centuries. So the burial mechanism is mixed, and a match does not test the rate.
- **C2, Tulul Abu el-ʿAlayiq (Qelt fan).** Netzer 2001 p. 86: erosion removed the Hasmonean plaza floor in the eastern sector. The surface before excavation lay 0.65–1.2 m below that floor. Both rates predict burial, so both have the **wrong sign** here.
- **Outcome:** no rate reproduces both controls. Every D_now is **uncalibrated**. The two controls themselves differ in sign within 25 km. That suggests net change since 60 CE depends on the site, not the region, so a regional (tier 3) rate should not be trusted at any single point.

## Caveats
- **Positions.** Every position is a project label point snapped to a 16 m DEM channel cell. Narrow gorges (P4a, P5, P1) are smoothed on the DEM, so the relief values are approximate. The DEM is SRTM-era; it is not today's surface near the shore.
- **C1 is not the Kidron channel.** The project's ADAJ coding puts Kh. Mazin on the Wadi Mazin delta. The transfer to P4b is therefore tier 3, not tier 2.
- **Unchecked figures.** The Bookman et al. 2004 level curve (full text) was not accessed. Lake-level values come from Hirschfeld 2004 and the Frumkin et al. 2001 table. The table prints the calibrated range for −390 m as "100 BCE–300 BCE", probably a misprint for 300 CE. Neither value was taken from memory.
- **No constant rates.** None was used beyond its source span. The Bruins et al. rate covers about 1,300 years; it is applied to 2,000 only as a tier 3 INFERENCE, and C1–C2 do not support it.
- **P7's depth.** The 9-cubit numeral is partly restored. It is scored as read.
- **Search effort per point.** P1–P8 each had at least two targeted web searches plus Drive and repo searches.
  - **Nothing fluvial or dated was found for P6 (Kuteif) or P8 (ʿAṣla/Og).** That is recorded as unknown, not as evidence of stability.
  - P4a and P4b had extra searches. The Kidron has no published Holocene fluvial study that was found.

## Not accessed
- **ADAJ 6/7 (1962)**, Stutchbury and Nicholl, pp. 96–103, Kh. Mazin sections. https://publication.doa.gov.jo/uploads/publications/54/ADAJ_1962_6_7.pdf. The server's TLS certificate has expired, and it was not bypassed.
- **Frumkin et al. 2001**, direct PDF download (to read Table 1 myself). A curl call with a browser user-agent was refused by the permission system. The table was read through WebFetch instead.
- **Bookman et al. 2004, full text** (GSA Bulletin 116: 555–571, doi 10.1130/B25286.1). Paywalled; abstract only.
- **Kagan et al. 2015**, *Radiocarbon*. The Arizona journal link redirects to a front page.
- **Ben Moshe et al. 2008, Hassan and Klein 2002, Dente et al. 2019, Bowman et al. 2007, Bowman et al. 2010.** Abstracts only; the full texts may hold per-stream incision numbers.
- **OSM Overpass** waterway query: the connection was reset (overpass-api.de) or timed out (kumi mirror). The DEM was used instead.

## Sources
- Hirschfeld, Y. 2004. Excavations at ʿEin Feshkha, 2001: final report. *IEJ* 54: 37–74, pp. 39, 66. https://www.jstor.org/stable/27927058. Owner's Drive copy read.
- Frumkin, A., Kadan, G., Enzel, Y. and Eyal, Y. 2001. *Radiocarbon* 43(3): 1179–1189, Table 1 p. 1187, p. 1184. https://www.cambridge.org/core/journals/radiocarbon/article/radiocarbon-chronology-of-the-holocene-dead-sea-attempting-a-regional-correlation/512C35213B4D0566515B903F8D4DD3D4
- Frumkin, A. 2023. Geology, geomorphology and formation processes of the Qumran caves. IAA, pp. 77–83. https://www.jstor.org/stable/jj.10329820.6. Drive copy read, CC BY-NC 4.0.
- Bookman, R. et al. 2004. Late Holocene lake levels of the Dead Sea. *GSA Bulletin* 116: 555–571. https://cris.huji.ac.il/en/publications/late-holocene-lake-levels-of-the-dead-sea/. Abstract only.
- Neumann, F. H. et al. 2010. *J. Arid Environments* 74: 756–764, pp. 757, 760, 762. https://core.ac.uk/download/29139285.pdf
- Bowman, D., Shachnovich-Firtel, Y. and Devora, S. 2007. *Geomorphology* 92: 60–75. https://manuscript.isc.ac/Inventory/10/2359605.htm. Abstract only.
- Ben Moshe, L. et al. 2008. *Geomorphology* 93: 524–536. https://cris.huji.ac.il/en/publications/incision-of-alluvial-channels-in-response-to-a-continuous-base-le/
- Ben Moshe, L. and Lensky, N. G. 2024. *Remote Sensing* 16: 1346. https://mdpi.com/2072-4292/16/8/1346
- Storz-Peretz, Y. et al. 2011. *ESPL* 36: 467–480. https://cris.bgu.ac.il/en/publications/rapid-incision-of-a-small-coarse-and-steep-fan-delta-in-response/
- Hassan, M. A. and Klein, M. 2002. *Geomorphology* 45: 21–33. https://cris.haifa.ac.il/en/publications/fluvial-adjustment-of-the-lower-jordan-river-to-a-drop-in-the-dea/
- Klein, M. 1985. *ESPL* 10: 525–531. https://cris.haifa.ac.il/en/publications/the-adjustment-of-the-meandering-pattern-of-the-lower-jordan-rive/
- Dente, E. et al. 2019. *ESPL* 44: 781–795. https://cris.huji.ac.il/en/publications/sinuosity-evolution-along-an-incising-channel-new-insights-from-t/
- Al-Husban, A. K. 2018. *EREM* 74(2): 34–51. https://erem.ktu.lt/index.php/erem/article/view/20917
- Lazar, M. et al. 2010. *J. Geology* 118: 261–276, p. 268, Table 2 p. 271. https://www.tau.ac.il/~shmulikm/Publications/Lazar-Jericho-JGeol-2010.pdf
- Bruins, H. J. et al. 2020. *Quaternary International* 545: 87–101. https://cris.bgu.ac.il/en/publications/ancient-runoff-farming-and-soil-aggradation-in-terraced-wadi-fiel/
- Gibson, S., Lewis, R. Y. and Taylor, J. E. 2023. Springer, doi 10.1007/978-3-031-27330-8_36. https://cris.biu.ac.il/en/publications/the-buqeisup%CF%B2supa-plateau-of-the-judean-desert-in-the-southern-le/
- Traubman, D. 2024. Khirbat Mazin. *HA-ESI* 136, Fig. 2. https://hadashot.iaa.org.il/reports_eng.aspx?id=137. Drive copy read; figure viewed and not stored.
- Netzer, E. 2001. *Hasmonean and Herodian Palaces at Jericho I*, pp. 9, 75, 85, 86. Owner's Drive page photos.
- Stacey, D. Three notes on Qumran. https://bibleinterp.arizona.edu/articles/stacey
- UNESCO Baptism Site nomination, p. 3. https://whc.unesco.org/document/169171
- DEM: Terrarium z13 tiles (AWS open data), https://s3.amazonaws.com/elevation-tiles-prod/terrarium/ (scripts in out/scripts/).

## Files
- [out/points.csv](out/points.csv): positions and controls, fixed first.
- [out/evidence.csv](out/evidence.csv): 55 source facts with tiers.
- [out/results.csv](out/results.csv): per-point results.
- [out/calibration.csv](out/calibration.csv): control outcomes.
- [out/form_dem.csv](out/form_dem.csv): DEM relief and distances to the shoreline contours.
- [out/scripts/](out/scripts/): the scripts. DEM tiles and downloads are kept in the scratch folder only.
