# Methods sandbox

Started 26 October 2026 at the owner's request: "We could sandbox these approaches not to bleed into the full goal of the project but yes they should be pursued."

The sandbox applies the case-study methods from the challenge plan (Ephesus, Linear B, Richard III, AF447) to the scroll, one run at a time.

## Rules

- **Exploratory only.** Nothing here changes the evidence ratings, the outcome ledger, ACTIVE_TEST, OPEN_QUESTIONS, the arrival register, atlas data or candidate and map data.
- **Read, never write.** Sandbox runs read main-project files. They do not edit them. A sandbox result enters the main records only by a separate owner decision, logged in the main record it changes.
- **Rule first.** Each run commits its rule (relations, candidates, controls, criteria) before evidence is gathered. The result file gives the rule's commit and SHA-256 and reports every candidate and branch, including misses.
- **AGENTS.md evidence rules still apply.** Cite exact pages and figures. Separate EVIDENCE (what a source says) from INFERENCE (our reasoning). Give controls the same search as candidates. Record missing data as unknown.
- **Exposure.** Most published evidence for the main candidates has been read before. Results here are exploratory and are not unseen tests.

## Files

| File | What it holds |
|---|---|
| [clusters.json](clusters.json) | The 8 place names that occur in two or more entries (from the wave-1 place-name list) |
| [linearb_sekakah_2026-10-26/](linearb_sekakah_2026-10-26/) | Run 1: Linear B joint fit for Sekakah and Shlomo (entries 20–24) |

## Runs

| Run | Method | Cluster | Status |
|---|---|---|---|
| linearb_sekakah_2026-10-26 | Linear B: one place must fit every entry that names it | Sekakah, Shlomo (entries 20–24) | **done 27 Oct: not discriminating** ([RESULT](linearb_sekakah_2026-10-26/RESULT.md)) |
| greek_letters_2026-10-27 | The 7 Greek letter groups are numerals or initials of their own entry | entries 1–15 | **done 27 Oct: not supported** ([RESULT](greek_letters_2026-10-27/RESULT.md)) |
| purity_rule_2026-10-27 | Consecrated items never go in tombs (Num. 19) | all entries | **done 27 Oct: not supported** ([RESULT](purity_rule_2026-10-27/RESULT.md)) |
| already_found_2026-10-27 | Some caches are already catalogued as hoards (karsh reading) | all entries with sums | **done 27 Oct: no lead** ([RESULT](already_found_2026-10-27/RESULT.md)) |
| kohlit_south_of_yanun_2026-10-27 | If the pit is in Janoaḥ, Koḥlit is a mound just south of Yanun | Koḥlit (entries 4, 11, 19, 60) | **done 27 Oct: not supported; records too coarse** ([RESULT](kohlit_south_of_yanun_2026-10-27/RESULT.md)) |
| onomasticon_names_2026-10-27 | Lost names survive, located, in Eusebius and the Madaba Map | 40 scroll names | **done 27 Oct: no new lead** ([RESULT](onomasticon_names_2026-10-27/RESULT.md)) |
| samra_hyrcania_valley_2026-10-27 | Valley of Secacah = Naḥal Sekhakha; Sekakah = Kh. es-Samra; conduit head = Hyrcania's intake (from run 1) | entries 20–24 | **done 27 Oct: survives, not preferred over Qumran** ([RESULT](samra_hyrcania_valley_2026-10-27/RESULT.md)) |
| route_travel_time_2026-10-27 | The entry order is a walking route (least-cost, Tobler) | anchored entries | **done 27 Oct: not supported (order short, but walking time adds nothing)** ([RESULT](route_travel_time_2026-10-27/RESULT.md)) |
| greek_architecture_2026-10-27 | Greek architectural loanwords point to Herodian-style buildings | loanword entries (3, 51, …) | **done 27 Oct: not useful, no lead** ([RESULT](greek_architecture_2026-10-27/RESULT.md)) |
| cave_entries_2026-10-27 | Cave entries match caves already excavated | cave entries (7, 22, 25, 26, 30) | **done 27 Oct: not supported** ([RESULT](cave_entries_2026-10-27/RESULT.md)) |
| linearb_achor_2026-10-27 | Linear B joint fit for the Valley of Achor | entries 1, 17 | **done 27 Oct: not discriminating** ([RESULT](linearb_achor_2026-10-27/RESULT.md)) |
| earthquake_fissure_2026-10-27 | Entry 22's "fissure" is the 31 BCE earthquake crack at Qumran | entry 22 | **done 27 Oct: supported (exploratory, fragile): reservoir = L56/58** ([RESULT](earthquake_fissure_2026-10-27/RESULT.md)) |
| text_blocks_2026-10-27 | Formula seams show the regional lists the scroll was compiled from | all entries | **done 27 Oct: seams real (p = 0.0004) but not regional** ([RESULT](text_blocks_2026-10-27/RESULT.md)) |
| imagery_gaps_2026-10-27 | Modern high-resolution imagery fills the survey gaps (calibrated blind first) | runs 1, 5, 11 gaps | **done 27 Oct: calibration weak; no gap filled** ([RESULT](imagery_gaps_2026-10-27/RESULT.md)) |
| hoard_contexts_2026-10-27 | Original reports recover the near-miss hoards' contexts | run 4 near misses | **done 27 Oct: no lead; ADAJ 1953 Feshkha report found** ([RESULT](hoard_contexts_2026-10-27/RESULT.md)) |
| stepped_tunnels_2026-10-27 | Entry 24's tomb in the Wadi of the Vault is a rock-cut stepped tunnel | entry 24 | **done 27 Oct: no lead (strict); weak Hyrcania lead (lenient)** ([RESULT](stepped_tunnels_2026-10-27/RESULT.md)) |
| mac_unblock_2026-10-27 | Read the large Drive PDFs on the owner's Mac (connector limit 10 MB) | runs 1, 9–12, 19 | **partial 28 Oct: de Vaux plate read (run 12 holds); other PDFs online-only** ([RESULT](mac_unblock_2026-10-27/RESULT.md)) |
| chain_l5658_2026-10-27 | Follow the chain from L56/58 to entries 21, 23 (Ephesus method) | entries 20–23 | **done 27 Oct: holds weakly; breaks on the strict C1 reading** ([RESULT](chain_l5658_2026-10-27/RESULT.md)) |
| copy_search_2026-10-27 | The scroll's "copy" survives among small Qumran fragments (formula signature) | entry 60 | **done 27 Oct: no lead; no unidentified fragment hits** ([RESULT](copy_search_2026-10-27/RESULT.md)) |
| field_names_2026-10-27 | Lost names survive as 1940s Arabic field names | 40 names + landmark words | **done 27 Oct: no new lead; A1 28 Oct (sheets 18-12, 18-13, 19-14 read directly): still no lead; 19-12 unread** ([RESULT](field_names_2026-10-27/RESULT.md)) |
| middot_temple_2026-10-27 | Temple-area entries fit Mishnah Middot's layout | entries 3–14 | **done 27 Oct: not supported (strict); lenient fit repeats Allegro** ([RESULT](middot_temple_2026-10-27/RESULT.md)) |
| amount_gravity_2026-10-27 | Bigger caches lie nearer Jerusalem | entries with sums | **done 27 Oct: underpowered; sign reversed** ([RESULT](amount_gravity_2026-10-27/RESULT.md)) |
| reverse_lookup_2026-10-27 | Well-documented sites, looked up against all entries | all entries | **done 27 Oct: not supported; weak lead entry 45 at Qumran** ([RESULT](reverse_lookup_2026-10-27/RESULT.md)) |
| wadi_aggradation_2026-10-30 | How deep a wadi-bed cache would lie today (aggradation or incision since 60 CE) | entries 17, 18, 20, 24, 28, 32, 35 | **done 30 Oct: all nine points unknown (strict); calibration failed** ([RESULT](wadi_aggradation_2026-10-30/RESULT.md)) |
| l5658_survey_design_2026-10-30 | Whether a non-invasive survey could test the L56/58 lead, so a null counts | entries 21–23 (22 primary) | **done 30 Oct: not testable non-invasively (borderline; partly testable for 50 kg in the top 1.5 m); crack fill never excavated** ([RESULT](l5658_survey_design_2026-10-30/RESULT.md)) |
| unknowns_value_2026-10-30 | Which missing records would settle the most sandbox verdicts | runs 1–22 | **done 30 Oct: Bar-Adon 1972, Humbert & Chambon 1994, Magen & Peleg 2018 pp. 58–66 and Stager 1976 settle the most units; 7 runs undecidable by any record** ([RESULT](unknowns_value_2026-10-30/RESULT.md)) |
| baradon_buqeia_2026-10-30 | Run 25 addendum A1: read Bar-Adon 1972 (run 25's top record) for its six linked units | runs 1, 5, 7, 12 | **done 30 Oct: no unit changes; Maqari pool lies east of the fort (bearing note)** ([RESULT](baradon_buqeia_2026-10-30/RESULT.md)) |
| landscape_map_2026-10-31 | Run 26: calibrated landscape map of the landmark words (every 300 m cell a hypothesis), gated on fake-entry calibration | entries with mapped landmarks (50) | **done 31 Oct: not obtained; no model passed both the gate and the 1940s-map check, so the scroll was not scored. Measured coverage: 27 % of 1940s-mapped features have a same-class modern record in their cell (recording rate c ≈ 0.1 after chance matches); class-level evidence moves the odds about 1.4×** ([RESULT](landscape_map_2026-10-31/RESULT.md)) |
| west_bank_inventory_2026-10-31 | Fifth inventory: the West Bank and East Jerusalem Archaeological Database (Greenberg & Keinan 2009) added to lane J's table | all | **done 31 Oct: 6,950 sites; inventory v2 = 16,383 rows** ([README](west_bank_inventory_2026-10-31/README.md)) |
| landscape_map_1km_2026-10-31 | Run 27: 1 km map on inventory v2, gated on 89 fresh 1940s map features read blind from 60 random windows | entries with mapped landmarks | **done 31 Oct: not obtained; calibrated (50 %/90 % coverage 0.49/0.90) but uninformative (mean BF 0.99×), so the scroll was not scored. Class-level landmark matching is closed as a route to place identification** ([RESULT](landscape_map_1km_2026-10-31/RESULT.md)) |

Owner approval for these runs (27 Oct, 00:55 Asia/Shanghai): "Create some new creative/clever hypotheses and run them in parallel. You have my explicit approval ... short of sending emails to people."

Round 2 approval (27 Oct, 13:15 Asia/Shanghai): "Do another run of exploring creative ideas/hypotheses in parallel."

Round 3 approval (27 Oct, 13:55 Asia/Shanghai): "Do another round of creative ideas."

Round 4 approval (27 Oct, 14:26 Asia/Shanghai): "Try 1,2,4,5,6,7,8".

Round 5 approval (30 Oct, 10:50 America/Los_Angeles): "#6, 7, 8 seem interesting" (of nine proposed avenues).

Addendum A1 to run 25 (30 Oct, 14:02 America/Los_Angeles): "go for it".

Run 26 approval (31 Oct, 08:56 America/Los_Angeles): "Sounds good. Shall we begin?"; final revision (09:16): "go ahead".
Run 27 and the fifth inventory (31 Oct, 09:43 and 09:57 America/Los_Angeles): "yes go for these", "yes grab these", "sure this too".
