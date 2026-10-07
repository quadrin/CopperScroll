# T09, T12, T19 — Historical imagery, IAA cave-survey request, ground-survey plan

Agent report, 6 October 2026, saved by the coordinator. Labels: EVIDENCE / INFERENCE. The shared web-search budget ran out near the end.

## What was done
Indexed the Bavarian WWI aerial archive (all 2,930 records); pulled 14 frames plus 6 Library of Congress 1931 air views; made a rough 1918-vs-2024 comparison at Tell es-Sultan; researched the IAA cave survey and drafted a data request; drafted the ground-survey plan with permit, legal and ethics analysis.

## Findings
1. **EVIDENCE:** the Bavarian collection (BayHStA "BS Pal.") is online and CC0, with IIIF scans up to 10,944 px. Key frames: Tell es-Sultan BS Pal. 1031 (2 Jul 1918); Jebel Qarantal with the ʿAin Duk aqueducts 1033 (22 Jun 1918); SE of St George's 899/900 (May 1918); Silwan/Kidron 839 (20 Jun 1918). No frame names Kh. Qumran.
2. **EVIDENCE:** CORONA frame DS1101-2168DF041 (KH-4B, Sept–Oct 1967) covers Jerusalem, Jericho and Kh. Qumran; public domain from USGS (free if scanned, otherwise $30 per frame).
3. **INFERENCE, medium:** the open ground north of Tell es-Sultan in 1918 is now ʿEin es-Sultan refugee camp (est. 1948). That is entry 60's sector if Koḥlit is the tell, so historical imagery is the only surface record left there.
4. **EVIDENCE:** the IAA Judean Desert survey began in October 2017, run jointly by the IAA, the Staff Officer for Archaeology and the Heritage Ministry; it reported about 80 km of cliffs and about 500 caves in a computerized database by 2021 (other reports: 120 km / 400 caves). Main publications: *Qadmoniot* 164 (2022) and the IAA volume *New Studies…* (2023) pp. 35–74.
5. **EVIDENCE + INFERENCE, high:** magnetometers cannot detect silver, gold or copper, and GPR performs poorly in saline marl. Qumran and Wadi Qelt are in Area C, where the only available licence (from the Israeli Staff Officer for Archaeology) is contested under international law. Fieldwork at Siloam is not recommended.

## Access routes
- Bavarian frames: metadata via the DDB API; images via IIIF at gda.bayern.de. Frames with no online scan (order from BayHStA): 1032, 1034, 838, 901, 980. Plate header "H.4500 Br.50" read as 4,500 m altitude and 50 cm focal length → scale ~1:9,500 (INFERENCE); the tell measures ~285 m on the 1918 frame vs ~330 m on 2024 Sentinel-2.
- Australian War Memorial B03561 (Jericho, c. 1918): public domain.
- Library of Congress 1931 air views, "no known restrictions": matpc-22117 (Jericho mound), 22118/22119 (Qarantal and Ain Duk), 22121 (St George's), 22138 (Kidron and Siloam).
- Hebrew University aerial archive (RAF 1944–48, WWI German and Australian photos; fee for high-res; catalogue URL unverified); Survey of Israel archive (paid); CAST CORONA Atlas (CC BY-SA non-commercial; check manually); PEF sheets XVII/XVIII on Commons (download hit HTTP 429); NLI "Jericho" 1:1,250 map (1930), public domain.

## Landscape changes
Jericho cable car (1998); Dead Sea falling ~1.2 m/year; Siloam excavation on Greek Patriarchate land leased to a Palestinian family (announced Dec 2022).

## IAA survey (T12)
Named in the official IAA release: Amichay, Hamer and Cohen (survey teams), Betzer (Southern Region head), Sion (Surveys Department), Ganor (Theft Prevention Unit). The repo already has IAA archive threads open; send the request through those rather than a new channel. Draft: `drafts/T12_data_request_email_DRAFT.md` (not sent).

## Survey plan (T19)
Ranked spots: Qumran intake (~1.3–1.6 m target depth), Wadi Qelt (~1.3–1.6 m), Qarantal summit (~3.1–3.7 m). Methods: ERT first (depth reach ~20–30% of the electrode spread, per US EPA; Martínez-López et al. 2013), plus GPR, EM induction and microgravity; sampling per EAC geophysics guidelines. Budget ~$55k–155k (INFERENCE, low). An IAA research licence requires a faculty member with at least an MA in archaeology (Matskevich & Weinblum 2021). Permit authorities: Area C — Staff Officer for Archaeology (1966 Jordanian law plus Military Orders 1166/1167); Area A, including Tell es-Sultan (UNESCO World Heritage since 2023) — Palestinian DACH under Decree-Law 11/2018; East Jerusalem — IAA. Israel is party to the 1954 Hague Convention and First Protocol but not the Second Protocol (Art. 9 limits excavation in occupied territory). A "Heritage Authority" bill for the West Bank passed first reading 11 May 2026 and was frozen 3 June 2026 (per Emek Shaveh); status needs checking. Oslo area class of the Qarantal summit unverified. Draft: `drafts/T19_ground_survey_plan_DRAFT.md`.

## Best next step
Order a scan of BS Pal. 1032 (Tell es-Sultan and the ground north of it) and the RAF 1944–48 verticals from the Hebrew University archive, then georeference them against the CORONA frame for a three-period base (1918, ~1945, 1967).

Files: imagery_catalogue.csv, bayhsta_bspal_index.csv, fig_tell_es_sultan_1918_vs_2024.jpg, fig_qarantal_1918_annotated.jpg, drafts/, downloads/.
