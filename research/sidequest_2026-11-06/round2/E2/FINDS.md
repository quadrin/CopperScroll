# Side-quest E2, round 2: joins nobody has made (6 Nov 2026)

Round 1 (E2) joined coin hoards and HA-ESI road reports with the Itiner-e road layer. Round 2 does three things:
- It takes the strongest round-1 card further (E2-2, the Ḥorbat Devora road).
- It makes a new join: Itiner-e (2025) against TIR Iudaea-Palaestina North (1993, Roll's roads), across the whole sheet. Itiner-e's own paper calls TIR "the principal source for the southern Levant". WBADB's 30 milestone rows serve as arbiter.
- It runs the round-1 E2-1 kill tests that were left open: a GLO-30 terrain-matched null, and WBADB as a survey-based second witness.

**Novelty search.** Before starting I listed `out2/*/` (21 lanes). C2 compared Itiner-e with SWP on sheet XVIII only, and checked TIR by eye in two windows (Buqeia, Hyrcania). No lane and no branch joins TIR with Itiner-e as data, and none joins WBADB with Itiner-e. I grepped main and `branch_only/` for "itiner", "TIR", "Dabaritta/Devora" and "Livias"; the hits are intake notes and C2 only.

**Files**
- `tir_roads_off_itinere.csv`: TIR road stretches more than 2 km from any Itiner-e line (20 clusters; OIG, lat/lon, TIR pixel).
- `itinere_lines_off_tir.csv`: Itiner-e lines with ≥3 km of their length more than 1.5 km from any TIR road (56).
- `wbadb_milestones_romroads_vs_itinere.csv` (144 rows; no coordinates) and `wbadb_milestones_itinere_vs_tir.csv` (30).
- `hoards_roads_terrain_null.csv`.
- `scripts/`.

**Private files** (`private2/E2/`): the TIR, SWP and Mandate overlays. TIR is © Israel Academy / Survey of Israel; it is held in the repo by the user's authorisation, so the overlays stay private.

---

FIND CARD
Title (one line): The Dabaritta road is missing from both standard Roman-road layers. Itiner-e (2025) and TIR North (1993) draw no road in the whole Tabor block, but HA excavated a 7.5 m-wide 2nd-century road at Ḥorbat Devora. A 2023 IAA report ties the site to the main road from eastern Galilee to the Jezreel Valley that Josephus implies at Dabaritta.
Lane: E2
Round-1 link: E2-2 (Ḥorbat Devora road outside Itiner-e; R6: SURVIVES, report dates it Roman)
What is odd (2–4 sentences): Round 1 showed that Itiner-e has no line within 8.3 km of the curbed 7.5 m road of HA 122 report 1606. TIR North, which Itiner-e names as its main Levant source, has the same gap. Its Roman road network (Roll) runs Sepphoris–Tiberias and Legio–Scythopolis around the block, and the area between them is empty: Nazareth, Exaloth, Dabaritta, Thabor Mons, Helenoupolis(?)/Kafr Kama and Sarona. The gap stands although the place is a known stage on a route. HA 135 report 26342 (Distelfeld, Klein & Silberklang, 24 Jul 2023) cites Josephus, *Life* 62 [318] (Jonathan's men seized at Dabaritta on the way from Tiberias to Jerusalem) and *War* 2.21.3 [595] (the Dabaritta ambush on Ptolemy's baggage train). It concludes that "the site was located on the main road that led from the eastern Galilee to the Jezreel Valley and southward to Jerusalem", and it cites the 2007 road (Cinamon 2010) as "a second-century CE Roman road".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HA 122 id 1606 (`hadtext/en/vol-122/01606_h-orbat-devora.txt` l. 26–61): "total width 7.5 m"; Late Roman sherds from road and roadbed; "unknown to the research on Roman roads in the Galilee". Map ref. 23576–82/73392–96.
- HA 135 id 26342 (`hadtext/en/vol-135/26342_h-orbat-devora.txt` l. 9–41): hiding complex, licence S-1070/2020, map ref. 235768/733707. The Josephus passages and the "main road" sentence are quoted above.
- TIR North: `research/assets/plans/tir-michigan/north/` (native JPEG rebuilt from the 23 parts). Pixel window x 5800–8400, y 4300–6100: no red road symbol between the Sepphoris–Tiberias and Legio road lines (`private2/E2/tir_tabor_s.png`).
- Itiner-e: nearest lines are fid 3232 Sepphoris–Tiberias at 8,266 m, 3669 at 10.9 km and 3229 at 11.7 km (round 1; R6 recomputed them).
- Older maps (`private2/E2/swp_devora_z15_s.png`, `m20k_devora_z15_s.png`; POM layers `pal63k-1880`, `pal20k-1940s`): the HA point lies about 1 km NE of Dabburiya beside ʿEin Dabburiya. On the 1940s 1:20,000 sheet a track runs from Dabburiya ENE toward Kefar Tavor (Mas-ha). On SWP 1880 tracks leave Deburieh NE toward Khan et-Tujjar.
- SWP *Memoirs* I (archive.org `surveyofwesternp01conduoft`), Sheet VI "Roads": the only main road named is "the great Damascus road, running from Beisan up past Mount Tabor on the east, past Khan et Tujjar". The Deburieh entry names Dabaritta ("Δαβαριττων κώμη of Josephus") and gives no road.
Literature check (queries run, result, tag):
- Itiner-e data paper (Sci. Data 2025, PMC12592351): TIR is the Levant's principal source, and there is no Levant-specific validation against TIR.
- Round-1 web queries (Devora/Dabburiya Roman road, Legio–Tabor–Tiberias) found nothing that places the road in a network.
- ʿAtiqot 41–121 full text (1,420 articles): "Devora" gives no hit; "Daburiyya" hits only a burial cave (Aviam 2002) and Khan et-Tujjar finds.
- Tag: **NEW TO THE PROJECT.** The road and the Josephus argument are published by the IAA (2010, 2023). That both TIR and Itiner-e lack them has not been stated in anything found.
Why it might matter: Any Galilee route, least-cost or "on a Roman road" test built on either layer treats the Tabor gap between Sepphoris, Tiberias and Legio as roadless. Yet it held a 7.5 m road from the 2nd century CE and a 1st-century route attested by Josephus. Both layers share the gap, so a second layer cannot be used to cross-check it.
How to confirm or kill it (with data in hand, or what is missing):
- Kill it with a Roll or Tepper publication (Tepper's Legio *caput viarum* paper; Roll's Galilee roads) that draws a Legio/Dabaritta–Tiberias road. None is in the corpus. An Itiner-e release that adds the road would also kill the omission.
- Confirm it by tying the HA 1606 trench to the 1940s track on a registered aerial (1940s RAF layer). Not done.
Confidence: high (both layers lack the road; the road is published as Roman); medium (that it was a through route rather than a local link)
Touches the Copper Scroll? no (Galilee; it affects the project's road layer only)

---

FIND CARD
Title (one line): First full join of Itiner-e with TIR Iudaea-Palaestina North. The two agree closely (85% of TIR road length lies within 1 km of an Itiner-e line), and WBADB milestones sit nearer Itiner-e (median 79 m against 276 m). But in the scroll region Itiner-e leaves its own cited sources in two places. Its Bethlehem–Ein Gedi line follows the SWP 1880 track, a median 3.4 km from TIR's desert road via Thecoa and the fort at Rujm en-Naqa. Its Jericho–Livias line ends at Tall el-Hammam, 3.3 km from TIR's Livias (Tell er-Rameh).
Lane: E2
Round-1 link: new
What is odd (2–4 sentences): Itiner-e calls TIR its principal Levant source and marks both lines as citing TIR. Fid 3428 Bethlehem–Ein Gedi (Conjectured; bibliography "TIR Iudaea-Palaestina, SWP"; 36.0 km) has 83% of its length more than 1.5 km from TIR's road (median 3.4 km, maximum 6.8 km). It runs from Herodium past Kh. Umm el-ʿAmed along the track SWP draws through the Taʿamireh, and it skips TIR's Thecoa–Umm ez-Zuweitine–Rujm Jemʿah–Rujm en-Naqa–Naḥal David line. Fid 3365 Jericho–Livias (Conjectured; bibliography "Isaac 1992, Roll 2002, TIR") passes 1.1 km north of Tell er-Rameh and ends 3.3 km NE of it, at 31.8400 N 35.6751 E (Tall el-Hammam). It crosses the Jordan about 1.4 km north of TIR's Bethabara crossing. Only the adjoining Livias–Esbus stub (fid 3682) cites Graves & Stripling 2011, who put Livias's administrative centre at Tall el-Hammam.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- TIR North native image, rebuilt from `research/assets/plans/tir-michigan/north/tir-north-native-resolution.part000–022` (11,163 × 14,630 px).
- Georeferencing: 17 printed easting lines (80–240 km, x 548–10612.5) and 20 northing lines (300–90 km, y 902–14077.5), fitted linearly. Residuals ≤160 m (E) and ≤111 m (N). Checks: TIR and Itiner-e coincide on the Beth Horon road (`private2/E2/tir_bethhoron_ov_s.png`).
- Red road mask (R>150, G<110, B<130, R−G>80) in 64 m blocks: 94,599 blocks, legend and inset removed. Within 300 m / 1 km / 2 km of Itiner-e: 47.8% / 85.4% / 94.7%. Scripts: `scripts/tir_red.py`, `tir_vs_itinere.py`.
- Bethlehem–Ein Gedi: `scripts/engedi_arbitrate.py`; overlays `private2/E2/tir_engedi_ov_s.png` (TIR + Itiner-e) and `swp_engedi_s.png` (SWP 1880 + Itiner-e). The legend (`tir_legend_s.png`) shows that TIR's double-dashed line is a "Desert road".
- Jericho–Livias: `private2/E2/tir_judaea_ov_s.png`. Itiner-e GPKG attributes of fid 3365, 3364 and 3682. Tell er-Rameh is at 31.8256 N 35.6444 E (Wikipedia, "Tell er-Rameh"), the traditional Livias.
- Milestones: the 30 WBADB rows with "milestone": median 79 m to Itiner-e and 276 m to TIR red; Itiner-e is closer in 22 of 30 (`wbadb_milestones_itinere_vs_tir.csv`). The TIR figure includes its 1:250,000 line width.
- Full tables: `tir_roads_off_itinere.csv` (TIR-only stretches), `itinere_lines_off_tir.csv` (Itiner-e-only lines). Most Itiner-e-only "Certain" lines (Diospolis–Jerusalem variants) are the Fischer–Isaac–Roll 1996 Jaffa–Jerusalem routes, which postdate TIR. They are additions, not errors.
Literature check (queries run, result, tag):
- Web: "Itiner-e Roman roads dataset Iudaea Palaestina comparison Tabula Imperii Romani Roll roads differences". This found the data paper (PMC12592351) and news items. The paper gives TIR as the principal source, describes Conjectured lines as following known remains and later roads, and has no Levant comparison with TIR.
- Web: "Graves Stripling 2011 Livias Tall el-Hammam" confirms their two-site proposal.
- Corpus: C2 (rounds 1–2) eyeballed TIR in the Buqeia/Hyrcania windows only. No branch has a TIR raster join.
- Tag: **NEW TO THE LITERATURE** for the join and the measured divergences. The Livias identification debate itself is KNOWN (Graves & Stripling 2011).
Why it might matter: The project uses Itiner-e as its Roman-road layer (atlas, Tobler routes, round-1 distance tests). The join shows where that layer is better than TIR (milestones) and where it silently departs from TIR. The departures are the Herodium–Ein Gedi desert route and the Jordan crossing to Livias, both on the eastern edge of the scroll region. A route test from Jericho toward the Plains of Moab, or across the Judean desert to Ein Gedi, changes by 1–7 km depending on which layer is used.
How to confirm or kill it (with data in hand, or what is missing):
- The CSVs are candidates, not verdicts. My mask can miss pale dashed TIR lines; I checked that the Thecoa–Engaddi desert road was captured (53–104 blocks around Rujm en-Naqa and Umm ez-Zuweitine).
- Each listed divergence needs one look at the overlay. The largest TIR-only clusters (south of Hebron near OIG 155.6/93.7; SW of Jerusalem near OIG 163.5/126.5; Madaba–Dibon in Transjordan) were not inspected.
- Kill condition for the Ein Gedi case: an Itiner-e source note saying the SWP track was preferred on purpose (e.g., Hirschfeld's Judean Desert roads). Its bibliography field names only TIR and SWP.
Confidence: high (agreement statistics, the two scroll-region divergences); medium (the full divergence lists)
Touches the Copper Scroll? maybe. ARGUMENT: no scroll entry is placed on these roads. But any route model from Jericho/Secacah east to the Jordan crossing, or south-west across the desert to Ein Gedi, inherits Itiner-e's choice. The two layers differ by 1–7 km exactly where the scroll's desert entries would be routed.

---

FIND CARD
Title (one line): Round-1 E2-1's open kill tests, run. Matching the excavation null on GLO-30 terrain moves the hoard-to-road percentile from 0.48 to 0.43–0.46; at the strictest match the CI only just excludes 0.5. A weak road preference is therefore possible. WBADB survey data show no local road signal either (Roman–Byzantine sites 0.505 against non-Roman sites within 5 km).
Lane: E2
Round-1 link: E2-1 (hoards no closer to roads than excavations; R6: SURVIVES, medium), kill test (c)
What is odd (2–4 sentences): Round 1 used the other excavations within 15 km as the null and found a mean percentile of 0.483 (CI 0.427–0.535). It did not control for terrain. With GLO-30 elevation and slope sampled at all 4,530 points and the null restricted to excavations in the same terrain band, the estimate falls as the match tightens:
- elevation ±150 m: 0.479;
- elevation ±75 m and slope ±3°: 0.457 (n = 84, CI 0.395–0.523);
- elevation ±50 m and slope ±2°: 0.430 (n = 76, CI 0.363–0.498).

Hoards sit higher and steeper than the excavations around them (median 280 m against 161 m; slope 5.3° against 4.7°), and higher terrain is farther from the valley roads. That partly hid a road preference in round 1. In the West Bank survey data (WBADB, 4,996 dated rows), sites with Hellenistic–Byzantine periods are no closer to Itiner-e "Certain" lines than sites without those periods within 5 km: 0.505, CI 0.496–0.513. At 10 km the figure is 0.485.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `scripts/terrain_sample.py` samples Copernicus GLO-30 COGs on `copernicus-dem-30m.s3.amazonaws.com` (tiles N30–N33, E034–E036) at each point and at 30 m offsets, for slope. `scripts/terrain_null.py`. Results: `hoards_roads_terrain_null.csv`.
- Inputs: round-1 `scratch/E2/all_dist.csv`, `out/E2/ha_hoard_list.csv`, and `research/comparanda/hoards_full/hoards.csv` (include = 1, deduplicated at 100 m).
- WBADB: `scratch/B2/wbadb_sites.csv` (OIG → ITM through EPSG:28191; `scripts/wbadb_period_test.py`).
- Milestone check of the layer: the 30 WBADB milestone rows lie a median 79 m from Itiner-e, all within 2 km (`wbadb_milestones_romroads_vs_itinere.csv`). The layer is not mispositioned in the West Bank.
Literature check (queries run, result, tag): round-1 queries rerun in spirit; nothing regional. Tag: **NEW TO THE LITERATURE** (as round-1 E2-1; this card refines its estimate).
Why it might matter: It changes the round-1 headline. The claim is no longer "hoards sit where excavations sit". It becomes "no strong road preference; a weak one (percentile about 0.43–0.46) cannot be excluded once terrain is matched". The settlement test shows that Itiner-e lines carry no local signal at 5 km even for Roman-period sites. So "near a Roman road" is a weak discriminator for any deposit or site in this region.
How to confirm or kill it (with data in hand, or what is missing):
- The strict-match estimate rests on 76 hoards and was one of 9 variants, so it does not survive correction for multiple comparisons.
- A larger, findspot-precise hoard set would settle it: IGCH / *Coin Hoards*, and the 9 Lorber 2021 hoards B4 found missing.
- WBADB's 100 m grid and Dar 1986's km-node rows (78 of 123 lie on exact km nodes) blur distances under about 1 km.
Confidence: medium
Touches the Copper Scroll? maybe: it weakens "on/near a Roman road" as a property that could separate real ancient deposits from controls.

---

## Dead ends
- ʿAtiqot 41–121 full text × Itiner-e: 89 road-related articles have map refs. The ones off the network are local field roads (Khirbat Ḥasan, ʿAuja aqueduct track) or regex noise ("via"). No new gap.
- WBADB "Rom road" rows × Itiner-e: 31 of 126 are >1.5 km from the network. Almost all are Dar 1986 local roads in western Samaria (on 1-km nodes). WBS:5080 (Kh. el-Firʿa–Idna, 6.5 km) is a local road. WBS:4175 (Hyrcania Valley paved road, Bar-Adon 106 = Patrich 1994a site 113, 12.2 km) is published by Patrich and lies in C2's already-noted Hyrcania gap.
- HA hoards × ʿAtiqot final reports: permit join gives few true pairs (Bet Shean purse ʿAtiqot 67; Naḥal Shalva and Kamon ʿAtiqot 112; Ashqelon Barnea ʿAtiqot 91). B1c and B4 already cover hoard conflicts. Correction to my round-1 list: the Barnea hoard is 7 gold coins of Justinian I (ʿAtiqot 91), not "4th–6th c".
- Radiocarbon lab-number join HA × ʿAtiqot: only 11 lab IDs in HA text, 0 shared. The ʿAtiqot text layer holds only 29 BP values (tables are lost).
- Dead Sea gauge × shore reports: no HA or ʿAtiqot report states a lake level with a number and date.
- Ossuary names (ʿAtiqot) × Ilan: only 14 articles with ≥5 ossuary and ≥5 inscription mentions. The repo's Ilan index has 821 names. Too thin.
- SWP *Memoirs* I: no "Roman road" at Deburieh; Sheet VI names only the Damascus road.

## Blocked inputs
- rasterio/GDAL HTTPS to the Copernicus bucket failed with "self-signed certificate in certificate chain" until `GDAL_CURL_CA_BUNDLE=/root/.ccr/ca-bundle.crt` was set. Resolved.
- Tepper's Legio *caput viarum* paper and Roll's Galilee road studies: not in the corpus.
- Itiner-e GPKG table `itinere_roads_simplify` only (no unsimplified geometry in the repo copy).

## Reproducibility
Run order: `wbadb_roads.py` → `wbadb_period_test.py`; `terrain_sample.py` → `terrain_null.py` (bootstrap seed 0); `tir_red.py` → `tir_vs_itinere.py` → `tir_overlay.py X0 Y0 X1 Y1 out.png 1`, `engedi_arbitrate.py`, `milestone_arbiter.py`; `swpview.py` / `swp_engedi.py` use C2's POM tile cache (`scratch/C2/scripts/tiles.py`). `roadlib.py` reads the round-1 Itiner-e arrays (`scratch/E2/roads_itm.npy`).
