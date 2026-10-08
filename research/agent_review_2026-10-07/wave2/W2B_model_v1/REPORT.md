# W2-B — Joint model v1 and re-ranking of the entry-60 targets

**8 October UTC implementation:** K2 is now the active default in both model
runners; legacy Sinkhorn and all historical output files remain explicit.
[Kernel correction](KERNEL_CORRECTION.md) records the bounded validation and
nonstationary-prior limit. [Entry-60 registry v2](registry_v2_entry60.json) updates
the search specifications with the follow-up and supersedes the historical
entry-60 records. The tables and heuristic probabilities below retain their
original agent-report scope; no target probability or confidence upgrade is claimed.

Agent report, 7 October 2026, saved by the coordinator (the agent could not write report files). Wave-1 files were read only. Labels: EVIDENCE / INFERENCE.

## What was done
Reproduced T06 exactly (log ML 8.6831). Added 10 places for the Koḥlit proposals and for Janoaḥ, each with a sourced coordinate. Old Israel grid references were converted with EPSG:28191 (Palestine Grid; EPSG:28193 only matches with +1000 km northing) and checked against 8 NEAEHL control points (most within 0.2 km). Ran variants — order on/off, order-derived exclusions, Koḥlit names tied/untied, XII 10 readings with a Janoaḥ coupling — under T06's kernel (K1), two density-neutral kernels (K2 fixed normaliser; K4 fixed + 5-km background grid), K3 (Sinkhorn + grid), and a uniform 5-km grid model (G-model, 1,316 cells). Re-ranked the entry-60 targets in `registry_v1_entry60.csv`.

## Key findings
1. **Wave 1's order-based demotion of Tell es-Sultan is a modelling artifact** (high confidence on the mechanism). T06 rescales its kernel over the project's place list, which is crowded around Jericho, Jerusalem and Qumran; that damps moves into crowded clusters and makes isolated places sticky. On T06's own inputs, density-neutral kernels leave P(entry 60 = Tell es-Sultan) at 0.28 (prior 0.30), not 0.10. With all ten proposals added, T06's kernel sends Koḥlit to Carmel (up to 0.40), 120–130 km from every neighbour.
2. **The order cannot separate the Koḥlit proposals** (medium-high). For entry 60 alone every proposal is within a factor of 3 of Tell es-Sultan; ʿEin Samiya scores −0.03 to +0.18 (log10 Bayes factor, density-neutral models). The order only says that entry 60, if not at a proposed site, probably lies north near entries 57–59. Tied results depend on treating block A (entries 1–19) as an itinerary; that pull goes to Jerusalem/Mount Zion and is circular.
3. **On Lefkovits's reading the pit is at Janoaḥ itself** (high). Lefkovits p. 425: "the deep pit which is in Janoah". So the wave-1 registry target P60-T3 (ʿEin Samiya tombs, justified by that reading) contradicts itself; the consistent target is Kh. Yanun (new P60-T8). It is also where the order fits entry 60 best (up to ~3×), but the epigraphy is against the reading.
4. **Under the Janoaḥ reading, ʿEin Samiya beats Tell es-Sultan by 2–4×** (low-medium). Don't count this twice — Zissu already used Janoaḥ to choose ʿEin Samiya.

**Moves an identification?** No. A wave-1 demotion is withdrawn and a registry target is corrected.

## Coordinates added (WGS84)
| place | lat, lon | σ km | source |
|---|---|---|---|
| ʿEin Samiya valley (Zissu) | 31.99231, 35.32671 | 0.7 | NEAEHL 5 p. 2118, OIG 181010/155470; Kh. Marjameh OIG 181600/155400 (p. 2121) → 31.99167, 35.33295; Zissu 181/155 (p. 150) → 31.98807, 35.32660 |
| Kh. Yanun = Janoaḥ | 32.15802, 35.36127 | 0.5 | Zissu p. 149 citing Finkelstein et al. 1997: 828–29, OIG 18425/17385 |
| Tell Muḥalḥil (PROXY) | 31.78648, 35.43180 | 2.0 | Nebi Musa (Wikidata Q2909131); "adjacent to Nebi Musa" (Zissu p. 148) |
| Beit Kahil | 31.56966, 35.06600 | 1.0 | Wikidata Q2898790 |
| Kh. Kuḥlah (PROXY) | 31.29310, 35.05530 | 3.0 | Kukhleh, Wikidata Q7214177 |
| Carmel, Wadi ʿEin es-Siaḥ | 32.80100, 34.97500 | 2.0 | Wikidata Q4025762; Milik DJD III p. 275 |
| Mount Zion | 31.77167, 35.22861 | 0.3 | Wikidata Q332444 |
| Transjordan (broad area) | Machaerus & Amathus | 15 | modelling proxy |
| ʿEin el-Ghuweir–Turabeh | 31.62768, 35.41255 | 1.5 | Dahari, ʿAtiqot 41 p. 246, OIG 18920/11505 |
| ʿAyn Feshkha | 31.71444, 35.45333 | 0.5 | Wikidata Q405816 |

## The T06 kernel artifact (entry 60, T06 inputs, untied, Tell es-Sultan prior 0.30)
| Kernel | Order | P(Tell es-Sultan) | P(north of 32.05°N) |
|---|---|---|---|
| K1 (T06) | off / on | 0.30 / 0.10 | 0.07 / 0.71 |
| K2 fixed | on | 0.28 | 0.10 |
| K3 Sinkhorn + grid | off / on | 0.30 / 0.15 | 0.30 / 0.67 |
| K4 fixed + grid | off / on | 0.30 / 0.28 | 0.30 / 0.39 |
| G-model | off / on | — | 0.28 / 0.49 |

Part of the north pull is real (entry 60's unidentified location near entry 59); the specific penalty on Tell es-Sultan comes from the kernel.

## Circularity notes
Puech's Tell es-Sultan partly derives from the order; entry 16's Tell es-Sultan candidate exists only because Koḥlit = Tell es-Sultan; Secacah = Qumran rests on the order; block A "temple" readings assume a Jerusalem tour; Zissu chose ʿEin Samiya partly via Janoaḥ; itinerary weights are fitted on lists with order-derived rows; Kuḥeila ~ Kaḥelet name likeness is the kind T01 found at chance level. Zissu (p. 146): "no continuity or pattern can be found" in the Koḥlit entries; Milik (DJD III p. 274): the Koḥlit caches are "dispersées capricieusement".

## Re-ranked entry-60 targets (medium-low)
| New | Old | Target | Reason |
|---|---|---|---|
| 1 | 1 | T1 Tell es-Sultan N/NW | demotion withdrawn; tell, spring with pool east, shaft field north co-occur; area built over |
| 2 | 3 | T3 re-scoped: ʿEin Samiya, pit north of Kh. el-Marjama / Kh. Samiya (Milik/Puech readings) | reading penalty misapplied; Early Roman kokhim tomb with ossuary fragments (Zissu p. 155) |
| 3 | new | T8 Kh. Yanun (Janoaḥ reading only) | target fixed whatever Koḥlit is; P(reading) ≈ 0.15 |
| 4 | 2 | T2 ʿEin el-Ghuweir | map placement only, no tell |
| 5 | — | T7 Feshkha | order support circular; no tell |
| 6 | 4 | T4 Qumran–Buqeia district | no anchor |
| 7 | new | T9 Tell Muḥalḥil | phonetic only; small structure |
| 8 | — | T6 Carmel | located; medieval legend; its T06 boost was an artifact |
| 9 | — | T5 Transjordan | no site |

## Best next step
Library checks: Finkelstein et al. 1997 pp. 822–829 (Kh. Yanun caves/pits/tombs) for P60-T8; the 1941 El Mughaiyir sheet 15-18 with Lapp 1966 and Dever 1972 for what lies north of Kh. el-Marjama (P60-T3). Replace the T06 kernel with a density-neutral one before using the order term again.

Files: registry_v1_entry60.csv; inputs/places_v1.csv, grid_conversions.csv, kohlit_proposals_v1.csv; outputs/table_order_BF_summary.csv, table_G_group_posteriors.csv, posterior_grid_v1.csv; scripts/ (grid_convert.py → build_inputs_v1.py → analysis_v1.py all → gmodel.py → summarize_v1.py → make_registry_v1.py; ~30 min on 2 cores).

