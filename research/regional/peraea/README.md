# Peraea: Second Temple sites east of the Jordan

**What it is.** A gazetteer of 25 sites east of the Jordan (Yarmuk to Arnon, within 40 km of the river), 75 recorded features, a W2B model variant that replaces the one blurred "transjordan" point with 12 documented Peraea sites, a draft pre-registration for a rarity count east of the Jordan, and access routes for MEGA-Jordan and EAMENA.\
**Main result.** 13 sites are documented (Jewish, Hasmonean or Herodian marker and occupation in the window both EVIDENCE), 12 of them in Peraea proper. In the model, P(entry 60 at transjordan) rises from 0.0025 to 0.0089, and the Koḥlit entries 4-19 move the same way. No entry moves by more than 0.01.\
**What stays unknown.** Whether Koḥlit lay east of the Jordan, and how common the entry 11 + 60 combination is there: no open region-wide inventory exists, and the two inventories need accounts.

Exploratory work, 9 October 2026 UTC, by the peraea worker. No identification claim, no outcome count, no registered result changed. Labels: EVIDENCE (a source states it), INFERENCE (our reasoning), TRADITION, CLAIM (a modern proposal not tested).

## Freeze record

- plan.json SHA-256 `010fa981cd2967b8443a1a30566547332758276c96ff596c820f09138393e707`, frozen 2026-10-09T22:12:02Z, before any site report was read.
- PLAN_v3.md SHA-256 `32499a34abc1c0f1aba8bfec4173c332fcb9d249a8838018eba4582e1278bea6`, frozen 2026-10-09T23:00:45Z, before any model run on v3 inputs.
- Exposure before the plan freeze: one test search of the DoA archive for "Machaerus" (titles only, 22:08:32Z).
- No input, rule or variant changed after the v3 run.

## Files

| File | What it is |
|---|---|
| `plan.json` | Frozen plan: area, period, feature classes, search terms, inclusion rules |
| `gazetteer.csv` | 25 sites: coordinates (WGS84), sigma, occupation and markers with labels and citations, status |
| `features.csv` | 75 features (one row per feature per source): type, period as given, dated_in_window, citation, quote of 12 words or fewer |
| `sources.csv` | Every report read: citation, URL, SHA-256 of the file read, text layer or OCR |
| `doa_search_log.csv` | The 108 frozen DoA archive searches and their hit counts |
| `PLAN_v3.md` | Frozen rule and runs for the model variant |
| `PREREG_DRAFT_R3.md` | Draft pre-registration of a Koḥlit rarity count east of the Jordan; approved 9 October 2026 as [kohlit_rarity_r3_2026-10-09.md](../../preregistration/kohlit_rarity_r3_2026-10-09.md) |
| `access_requests.md` | How to request MEGA-Jordan and EAMENA access, with draft texts (nothing sent) |
| `scripts/build_gazetteer.py` | Builds the three CSV files from the coded data (`--check` verifies) |
| `scripts/run_v3.py` | Runs R0-R2 of PLAN_v3 and writes `W2B_model_v1/outputs_v3/` |
| `tests/test_peraea.py` | 12 unittest tests |
| `../../agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/` | v3 inputs, generator `build_inputs_v3.py` (`--off` gives inputs_v2), `additions_v3.json` |
| `../../agent_review_2026-10-07/wave2/W2B_model_v1/outputs_v3/` | v3 outputs and their README |

## What was searched

- The DoA publication archive (ADAJ, SHAJ): 108 title-and-text searches from plan.json, up to 3 result pages each (`doa_search_log.csv`). Multi-word terms behave as OR searches there, so they return hundreds of unrelated hits. The distinctive single words (for example Ammata, Kharrar, Nimrin, Jadur, Kafrein) carry the search.
- ACOR *Archaeology in Jordan* 1-3 (whole volumes, open access).
- Josephus, *War* and *Antiquities* (Whiston, Project Gutenberg), cited Book.Chapter.Section in Whiston's numbering.
- 41 files were downloaded (37 DoA PDFs, 3 AIJ volumes, 1 Getty article). 32 reports are cited in `sources.csv` with their SHA-256 (23 read by OCR, 9 from the text layer). Seven DoA PDFs were opened but not cited (Voros 2010, 2011, 2013; Ji 2001; Graf 2016; Sparks 2001, whose stone vessels are Bronze Age; Waheeb 2021, whose Early Roman water works at ʿAyn Salim have no marker).

## Gazetteer (EVIDENCE unless marked)

**Documented, Peraea proper (12; these form the v3 mixture).**

| Site | Window evidence | Marker |
|---|---|---|
| Machaerus | Hasmonean fort c. 90 BC; Herodian palace; garrison to 71 AD (ADAJ 59 p. 449) | War 7.6.2; five miqvaot, one Hasmonean (ADAJ 59 pp. 445-449) |
| Kh. ʿAtaruz | late Hellenistic-early Roman fills (SHAJ 10 p. 624) | miqveh on the eastern slope (same) |
| ʿAin az-Zara (Callirrhoe) | Early Roman building and thermal pool (ADAJ 33 pp. 219-222) | War 1.33.5; First Revolt coins (ADAJ 33 p. 223) |
| Kh. al-Mukhayyat | Late Hellenistic miqveh (AIJ 1 p. 50) | miqveh; Jannaeus coins (SHAJ 8 p. 182) |
| Madaba | Late Hellenistic perimeter wall (SHAJ 11 p. 433) | Ant. 13.9.1, 13.15.4, 14.1.4 |
| Tall Hisban | late Hellenistic fort, early Roman village (SHAJ 10 p. 621) | Ant. 13.15.4, 15.8.5; Jannaeus coin; rolling-stone tombs |
| ʿIraq al-Amir | village walls, late 2nd c. BC to mid-1st c. AD (ADAJ 6-7 p. 89) | Jannaeus coins (SHAJ 8 p. 182) |
| Kh. as-Sur | Hellenistic-Byzantine fort (ADAJ 42 p. 597) | one Hyrcanus I coin (SHAJ 8 p. 181) |
| Umm Hadar | fort, mid-2nd to mid-1st c. BC (SHAJ 11 p. 252) | Hasmonean coins; Judaean jar types |
| Tall Barakat | late Hellenistic-early Roman fortress (ADAJ 46 p. 185) | eight Hasmonean coins (SHAJ 8 p. 181) |
| Tulul adh-Dhahab (west) | building of the 2nd-early 1st c. BC, burnt before mid-1st c. BC (ADAJ 57 pp. 92-95) | latest coins of Jannaeus (ADAJ 57 p. 94) |
| Wadi al-Kharrar | Early Roman phase I, ca. 100 BC-AD 73 (ADAJ 46 pp. 562, 569) | chalk stone cups, 1st c. BC (ADAJ 46 pp. 562, 565) |

- **Documented outside Peraea proper:** Pella (Decapolis): a Hasmonean-period destruction, ca. 83/80 BC (AIJ 1 p. 24); Ant. 13.15.4.
- **Partial (10):** Tell er-Rameh (Livias only by TRADITION), Tall el-Hammam, Kh. al-Habbasa, Kh. Sar (identifications are CLAIMs), Tall ʿAmmata (Amathus CLAIM; no coordinate found), Tall al-ʿUmayri (the miqveh reading is Ji's), Tell Nimrin (only "Roman"), Tall Jadur (Gadara of Peraea; occupation UNKNOWN; no coordinate), Tall al-Kafrayn (Abila; Roman occupation UNKNOWN), Umm Qays (not read; an undated hinterland miqveh).
- **Excluded (2):** the Rajib tombs near Amman (no marker; not Ragaba) and the es-Salt Roman tomb (after the window).
- **Not coded (searched, nothing usable found or read):** Besimoth/Tell el-ʿAzeimeh, Ragaba, Zia, Lemba/Libb, Qasr ar-Riyashi, Mount Nebo/Siyagha (one Jannaeus coin only), Gerasa, ʿAyn Salim (only TRADITION as Aenon).
- INFERENCE: Amathus is disputed between Tall ʿAmmata (Kokkinos 2001 p. 481), Tulul adh-Dhahab (Thiel, via Pola 2013 p. 85) and Tall al-Mughanni (Mittmann). The W2B "Amathus" point (Wikidata Q2841350) lies 0.1 km from Tulul adh-Dhahab west. The W2B "Machaerus" point lies 0.9 km east of the citadel, by Mukawir village.
- Coding note: the plan has three statuses. Where occupation is UNKNOWN (silence), the site is "partial", never "excluded".

**Features.** 75 rows: pools 17, walls 17, cisterns 15, channels 8, towers 7, caves 5, tombs 4, hoards 2. 43 are dated in the window by their source, 11 overlap it, 17 are undated and 4 fall outside. The 12 documented sites hold 64 rows, 40 dated in the window. Feature positions are site points; no source gives feature-level coordinates.

Two features worth a look, recorded without interpretation: at Machaerus a Hasmonean tower on the northern slope opens into an 8-m-deep rock-cut reservoir whose entrance "was carefully masked and blocked in antiquity" (Loffreda 1981, ADAJ 25 p. 92). At Umm Hadar, graves were cut into the courtyard soon after the fort's destruction (SHAJ 11 p. 252).

## Model variant (PLAN_v3; K2 default)

- **R0.** The v3 build with the change switched off is byte-identical to inputs_v2. The runner reproduces `outputs_v2/posteriors_v1_v2.csv` exactly (3,199 values, largest difference 0), with P(60 at kh_qumran) = 0.0325 and P(25 at IV/17) = 0.1802.
- **R1 (V3-P).**

| Entry | P(transjordan) v2 | V3-P | P(TRANSJ region) v2 | V3-P | TV(v2, V3-P) |
|---|---|---|---|---|---|
| 4 | 0.0023 | 0.0084 | 0.0037 | 0.0113 | 0.0084 |
| 11 | 0.0019 | 0.0075 | 0.0032 | 0.0102 | 0.0080 |
| 15 | 0.0024 | 0.0085 | 0.0039 | 0.0116 | 0.0084 |
| 19 | 0.0030 | 0.0092 | 0.0048 | 0.0127 | 0.0083 |
| 60 | 0.0025 | 0.0089 | 0.0041 | 0.0121 | 0.0087 |

- Entry 60's top states do not change (U_JER 0.184, U_JERICHO 0.069, U_QUMRAN 0.046, kh_qumran 0.032). The other proposals barely move (Tell es-Sultan 0.0196 in both; ʿEin Samiya 0.0167 to 0.0166).
- The Koḥlit latent puts almost the same mass on transjordan (0.0145 to 0.0147). INFERENCE: the rise comes from the name-tie kernel (1-km scale). A 15-km blur gave the proxy a tiny self-affinity, so tied entries rarely sat at it. Precise sites remove that handicap. The kernel grid shows this: with the tie off (rho 0, K2) P(60 at transjordan) is 0.042 in both v2 and v3; with the tie on (rho 0.9) it is 0.0028 in v2 and 0.0136 in v3.
- No entry has TV(v2, V3-P) above 0.01. Mean TV over all 61 entries: 0.0013. logml 7.648 to 7.634.
- **R2 sensitivity** (entry 60, P(transjordan)): S1 cluster-merge (9 clusters) 0.0079; S2 broad (19 sites) 0.0086; S3 5-km sigma floor 0.0035; S4 split into 12 places with the Goranson odds shared 0.0485 (TV about 0.10 for every Koḥlit entry, mean TV 0.072 over all entries, logml 11.05). INFERENCE: S4's jump is the per-place background prior of 12 new states (the effect KERNEL_CORRECTION.md warns about), not new evidence. Under the Sinkhorn kernel the v2 proxy was boosted as an isolated place (0.089 order-only); v3 halves that (0.043). S6, XII 10 read "Janoaḥ": entries 4-19 rise from 0.0017-0.0027 to 0.0054-0.0068.
- Reading (INFERENCE): replacing the blur with documented sites raises the Transjordan share about 3.5-fold but leaves it below 1% for every Koḥlit entry. The order and the other candidates still dominate. This identifies nothing.

## What stays unknown, and why

- Whether Koḥlit lay east of the Jordan. Goranson's reading is a district; the model needs places, and equal weight per documented site is a choice.
- The real density of Second Temple sites in Peraea. The open record is patchy (surveys of Wadi al-Kafrayn and the Dead Sea shore; excavations elsewhere). The 1975-76 East Jordan Valley Survey and Glueck's surveys are not open. MEGA-Jordan and EAMENA need accounts ([access_requests.md](access_requests.md)).
- Feature positions within sites, and the dates of 28 of the 75 features.
- Coordinates for Tall ʿAmmata, Tall Jadur and Kh. Libb (no open point found).

## Errata found after the v3 freeze

A page check after the run (each quote located on its PDF page) found five wrong page numbers. They change no coordinate, date, label or model number. The frozen files keep them so that their hashes still match PLAN_v3; the corrections are:

| File, row | Recorded | Correct |
|---|---|---|
| gazetteer.csv, tall_barakat, coord_source | ADAJ 46 p. 184 | p. 185 |
| features.csv, tall_barakat-01 to -04 | pp. 184-185 | p. 185 |
| gazetteer.csv, tulul_adh_dhahab_w, coord_source | ADAJ 57 p. 82 | p. 81 |
| gazetteer.csv, tulul_adh_dhahab_w, identification_note | Pola 2013 p. 87 | p. 85 |
| features.csv, callirrhoe-06 | ADAJ 40 p. 437 | p. 436 |

All other feature quotes were found on the cited page (the es-Salt row quotes the article title).

## Deviations and failed links

- **Pleiades was not used.** Its robots.txt disallows the agents ClaudeBot, Claude-Web and anthropic-ai (https://pleiades.stoa.org/robots.txt). Coordinates come instead from printed Palestine Grid references (converted with W2B's EPSG:28191 transformer), Wikidata entity JSON and English Wikipedia page coordinates. For points far east of the Jordan, EPSG:28191 and EPSG:28193 (+1,000 km) differ by up to 0.0008 degrees (about 80 m), so `grid_convert.oig()` refuses them; the builder uses the EPSG:28191 transformer directly.
- After the freeze, the DoA archive was searched for two known report titles ("Kufreyn"; a 1998 survey title) and two volume tables of contents were opened, to find the 1998 and 1999 survey reports that hold the Palestine Grid references. ACOR's site was searched for "Machaerus" and "Archaeology in Jordan". These located sources; they changed no rule.
- OCR (tesseract) was used for the scanned PDFs (23 of the cited reports). Quotes were checked against the OCR text; four differ only by OCR hyphenation or layout.
- Failed: https://megajordan.org/ (TLS: connection reset by peer; the http:// address worked); https://publication.doa.gov.jo/robots.txt (404, no robots file); https://www.getty.edu/projects/mega-jordan/ (404); English Wikipedia titles Callirrhoe, Tulul_adh-Dhahab, Gadara_(Peraea), Amathus_(Jordan), Tall_Jadur, Tell_Ammata, Tall_Iktanu (no such page). DAAHL and the IAA archive were unreachable through the proxy when another worker tried them (proxy log), and were not needed here.
- Nothing was opened that shows the strip north of Tell es-Sultan or column XII of the scroll.

## Run and test

From the repository root (Python 3 with numpy and pyproj, which W2B already needs):

```sh
python3 -I -B research/regional/peraea/scripts/build_gazetteer.py --check
python3 -I -B research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/build_inputs_v3.py --check
python3 -I -B research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/build_inputs_v3.py --off
python3 -I -B research/regional/peraea/scripts/run_v3.py --tables
python3 -I -B -m unittest discover -s research/regional/peraea/tests -t research/regional/peraea/tests
```

The run takes about 20 s and refuses to start if a frozen input changed; it stops if R0 fails. The 12 tests check the plan hashes, the three schemas (including 12-word quotes and citations that resolve to `sources.csv`), that both builders reproduce the committed files, that the switched-off build equals inputs_v2, that only the transjordan components change, that the runner reproduces v2, and that two runs are identical and match `results_v3.json`.
