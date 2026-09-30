# Christmas Cave and Hyrcania: primary-source follow-up

Reviewed 30 September 2026. This continues the [three-book intake](https://github.com/quadrin/CopperScroll/blob/main/research/sources/kotar_books_intake_2026-09-30.md). **Result:** Christmas Cave now has a published location and an entrance/neighboring-cave plan; Hyrcania now has a directly read feature inventory. Neither establishes a Copper Scroll deposit. Hyrcania remains possible, low, for entries 16, 29 and 35.

**Later follow-up on the same date:** [plan registration, collection provenance and Salvadora review](https://github.com/quadrin/CopperScroll/blob/main/research/sites/cave_plan_followup_2026-09-30.md). Christmas's cave anchor has now been converted; precise entrance positions remain unresolved. Hyrcania's regional registration trial is insufficient for geographic feature footprints. The source-access limitations below describe this earlier review stage.

## Sources actually inspected

| Source | Scope inspected | Page mapping and access |
| --- | --- | --- |
| Roi Porat, Hanan Eshel and Amos Frumkin, “מערת חג המולד בנחל קדרון תחתון (ואדי א־נר),” in *Refuge Caves of the Bar Kokhba Revolt*, second volume (2009), pp. 31–52 | Chapter text, especially pp. 31, 35–42, 46–47; entrance plan and contextual coin descriptions visually checked | [Cave Research Center PDF](https://www.malham.info/_files/ugd/2121fb_ff7be29e3db44490b0eacddf2f7404aa.pdf), 24 PDF pages; printed page = PDF page + 28 after two cover pages |
| Rasmussen et al., *Heritage Science* 10:18 (2022), “Defining multiple inhabitations of a cave environment using interdisciplinary archaeometry” | Location, collection history, sampling context, dating results and archaeological discussion; Tables 2 and 9 visually checked. Chemical methods were not independently audited. | [Publisher PDF](https://www.nature.com/articles/s40494-022-00652-2.pdf), 22 pages; article page = PDF page; [DOI](https://doi.org/10.1186/s40494-022-00652-2) |
| Joseph Patrich, “אמות המים להורקניה,” in *Ancient Aqueducts in the Land of Israel* (1989), pp. 243–260 | Entire chapter read visually, including numbered survey map, sections, plans and notes | User-supplied ZIP; scans 256–273 = printed 243–260. [Kotar book 6765980](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=6765980) |
| Patrich, Hyrcania chapter in *דרך ארץ: אבן חרס ואדם* (1996), edited by Irit Zaharoni, pp. 322–329 | Entire Hyrcania chapter read visually; Mar Saba pp. 306–307 and 312 sampled, not its entire chapter | User-supplied `derech-eretz.zip`, 408 scans. These inspected scan numbers equal printed page numbers. [Kotar book 96658741](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=96658741) |

The scans and downloaded source PDFs remain outside the public repository. The [feature records](https://github.com/quadrin/CopperScroll/blob/main/registration/christmas_hyrcania_primary_features_2026-09-30.json) contain project-authored factual extractions and explicitly provisional tests.

## Christmas Cave: separate the entrances and find locations

Porat et al. give grid `189887/121095` (p. 31). Figure 5 (p. 35) distinguishes the main northern entrance, southern cliff opening and neighboring caves 710–713. The northern opening is hidden but accessible; the southern opening requires ropes from outside. Allegro's cover shows the southern opening (pp. 31, 37), so it cannot stand for the accessible entrance.

The Agrippa I and Pilate coins are assigned to Christmas Cave; the Nerva denarius to cave 710, about five metres above/north of its main entrance; the Hasmonean coin to shelter 711, about fifteen metres north of 710 (pp. 40–42). Merge these only at regional level. Allegro's excavation disturbed the cave and left spoil and sorting areas outside (pp. 36–37). Coin mint dates do not date a sealed deposit. The chapter's First Revolt interpretation is an inference (pp. 46–47). [Source chapter](https://www.malham.info/_files/ugd/2121fb_ff7be29e3db44490b0eacddf2f7404aa.pdf).

### Scientific dating does not supply a single occupation date

Rasmussen et al. supply New Israel Grid `239887/621095` (p. 2). Sampled materials are surface finds (p. 4). Table 2 gives textile GrA-53274 a 2σ interval of CE 25–220; Table 9 gives flax rope UCI-79814 CE 25–120. Most relevant ranges overlap both revolts; the authors explicitly say the dates cannot securely distinguish one revolt, both, or activity between them (p. 14). The rope's earlier interval is useful, but dates the material rather than its deposition. Table 2's olive stone is medieval, CE 1280–1400.

The museum prefix **QCC** was assigned through a mistaken Qumran association (p. 2). It is not a geographic witness. Table 9's paired laboratory identifiers for wool should not be counted as independent cave contexts. [Scientific study](https://doi.org/10.1186/s40494-022-00652-2).

**Project inference:** the two printed grids differ by exactly 50,000 east and 500,000 north. Record them as two source notations for the same cave, not two independently surveyed entrances. Neither source establishes whether its coordinate marks a particular opening or a cave-level anchor, nor its accuracy. Keep WGS84 and individual entrance coordinates unset until that is resolved. Christmas remains a regional comparison cave, with no assigned Copper Scroll entry.

## Hyrcania: the feature plan now replaces snippet-only access

Patrich 1989 Figure 1 (p. 243) has a north arrow, a kilometre scale, station numbers and a legend separating clear routes from inferred routes. Figure 22 (p. 256) gives a detailed contour plan with a 50-metre scale, labeled cisterns, channels and the double pool. These support source-plan positions; they are not already geographically registered footprints.

| Feature | Specific source evidence | Consequence for testing |
| --- | --- | --- |
| Southern intake, station 1 | Kidron dam about 1,300 m west of the Small Lavra; southern line about 9 km (p. 244) | Distinguish it from both northern intake 44 and downstream dam 42. |
| Downstream dam, station 42 | Runoff diverted into southern line; possible Byzantine reuse from this point (p. 251) | A surviving dam is not automatically the original intake or an Early Roman feature. |
| Northern intake, station 44 | Wadi Abu Shuʿla dam, surviving length 17.5 m (p. 251); northern line 1,950 m, assigned Hasmonean phase (p. 244) | Concrete comparison for the guide's northern-system dam; its grid still needs registration against the primary map. |
| Shared western and eastern bridges, 46 and 48 | Junction at 46 uncertain (pp. 251–252); 48 has lower Hasmonean and upper Herodian masonry (pp. 252–255) | Do not invent a preserved collection cistern at the junction. Distinguish elevations and channels. |
| Double pool west of the summit | Northern and southern members separated by 4.8–5.4 m of quarried rock; northern depth about 5 m, southern maximum about 2.6 m (p. 255; Fig. 22) | Entry 29's “northern reservoir” can be compared with individual basins instead of one fort pin. The name restoration and period of use remain unresolved. |
| Additional southern pool | South of bridge, heavily filled, with no deeper lining or plaster visible (p. 255; Fig. 22) | Retain as a separate, poorly dated feature. Do not silently fold it into the double pool. |
| Covered passage, station 49 | Southwest slope, near cisterns N/A′; length about 11.5 m, height 1.25 m, width 0.75 m; southern end filled and destination uncertain (pp. 257–259; Figs. 25A, 25) | Specific surveyed passage, distinct from the guide's approximately 30-m mysterious tunnel. |
| Cisterns S and F | Stepped installations illustrated in Figs. 26–28; F has later Christian plaster decoration and a possible earlier pool function (pp. 258–260) | Present stepped appearance does not fix the construction phase of every visible element. |

Patrich's general inventory says **20 cisterns and two rock-cut pools** (p. 256), while also describing the separate, filled southern pool (p. 255). *Derech Eretz* p. 327 says **21 cisterns and two pools**. Retain both source counts and compare the actual labeled features; a numerical discrepancy is not evidence for a lost scroll landmark.

Patrich assigns the northern system to the Hasmoneans, the southern to Herod, and distinguishes Byzantine reuse (pp. 244, 251–252, 259). Herodian material, including a coin, is reported in cistern C (p. 259), but does not establish a sealed deposit around CE 70. The chapter argues for abandonment after Herod and notes no Great Revolt use; *Derech Eretz* p. 327 repeats this. This remains a conflict with the period-of-use assumption in the proposed identification, not proof that the earlier structures had vanished.

### What Derech Eretz adds

Pages 323–326 supply photographs of the fort, bridge and pool setting. Page 327 supplies a reconstruction illustration and a concise account of the construction phases; pp. 328–329 explain later monastic occupation. The same author and closely related reconstruction in the 1989 chapter mean these accounts are **dependent evidence**. A reconstruction can help explain a hypothesis but cannot establish a surviving wall or opening. Statements about excavation status describe the situation at publication in 1996.

## An explicit falsification test for entry 16

The [reading record](https://github.com/quadrin/CopperScroll/blob/main/text/readings.json) retains **14, 40 and 41 cubits**, a lost destination, and uncertainty between distance and depth. Hyrcania is supplied by an identification argument; its name does not survive in this entry. Entry 29 likewise retains competing readings of the damaged conduit name and reservoir qualification.

For a **sensitivity test**, use 0.445–0.525 m per cubit, without claiming that interval fixes the scroll's unit:

| Restored number | Modeled length |
| --- | --- |
| 14 | 6.230–7.350 m |
| 40 | 17.800–21.000 m |
| 41 | 18.245–21.525 m |

**Conditional result:** if entry 16 describes horizontal travel along station 49 from its surviving entrance, neither 40 nor 41 cubits fits inside the reported surviving 11.5 m. Fourteen cubits fits within it but identifies no feature at that offset. The filled end means original total length is unknown. This is not a rejection of Hyrcania, a depth interpretation, or an originally longer passage. Do not select the 14-cubit restoration merely because it produces a fit.

## Next discriminating work

1. Register Hyrcania Figs. 1 and 22 against independently located surviving bridge and pool features; preserve observed and reconstructed segments separately. Only then compare the guide's `1837.1261` dam with station 44 and reconcile its 1.2-km line with Patrich's 1.95 km.
2. Trace Christmas object and trench records across Allegro's archive and museum catalogs. Maintain cave 710/711 separation, catalog aliases and repeated sample relationships. This is a productive LLM task when every proposed join retains its source and can be rejected.
3. Obtain Feldman's 1974 Hyrcania water-system study, pp. 316–335, cited by Patrich (1989 p. 260), and the relevant original survey/phase records. Test use around the first century CE independently of the identification proposed for the scroll.

The site-association ratings and deposit coordinates remain unchanged. Source access and physical-feature specificity have improved; those are distinct from evidence identifying a scroll location.
