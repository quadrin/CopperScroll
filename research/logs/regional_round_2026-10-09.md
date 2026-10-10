# Regional round, 9 October 2026

The project owner asked whether the project had used all the regional data: IAA finds, sites east of the Jordan, maps and landscape, and recorded features such as cisterns and walls. It had not. The owner asked for four gaps to be filled at once.

Four workers ran in parallel. Each worker owned one folder. The integrator owned shared files and Git. All work is exploratory. No registered result changed. No identification, deposit or outcome-ledger count was added. No image of XII 8–12 or of the 21/22 cut was opened.

## What was built

| Source | Folder | Main result |
|---|---|---|
| IAA excavation reports (*Hadashot Arkheologiyot*, ESI, HA-ESI) | [regional/haesi_features](../regional/haesi_features/README.md) | 5,738 table-of-contents items screened; 777 candidates; 73 reports read from 7 volumes (the owner's Drive copies and the open 2026 volume). 89 feature rows near the places; the reports date 23 of them to the window (Jerusalem, the Jericho palaces, Herodium). No report read describes an in-window feature at a Koḥlit place outside Jerusalem. 651 candidates stay unread: the online reports are closed to robots, and the portal PDFs sit behind a browser check. |
| Survey of Palestine 1:20,000 sheets, 1940s (Palestine Open Maps) | [regional/mandate_maps](../regional/mandate_maps/README.md) | The published tiles sit 3–19 m from the printed grid (median 10 m). 190 features and 248 names coded near the places. Of 125 features checked against 2025 imagery, 27 are built over. The ʿAin ed Duk point in the gazetteer lies 512 m from the 1940s spring. Sheet 19-14 (Tell es-Sultan) was opened under the registration protocol: the registration was rejected (check error 48.6 m), and the strip prints no opening or grave. |
| Sites east of the Jordan (ADAJ and other open reports) | [regional/peraea](../regional/peraea/README.md) | 25 sites, 13 with documented Second Temple Jewish, Hasmonean or Herodian occupation (12 in Peraea proper); 75 features, 43 dated in the window. A model variant ([inputs_v3](../agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/)) replaces the one "transjordan" proxy with the 12 sites: P(entry 60 east of the Jordan) rises from 0.0025 to 0.0089. A draft pre-registration for a count east of the Jordan (R3) waits for the owner. |
| Archaeological Survey of Israel (survey.iaa.org.il) | [regional/asi_jerusalem](../regional/asi_jerusalem/README.md) | The survey site's own public services give the records without a browser. 1,258 records from 17 maps lie within 3 km of a place; 315 within 1 km were read in full. Near Jerusalem places, the records date 182 feature mentions at 70 sites to the window, mostly Herodian tombs; only 6 water features are dated in the window. No record lies inside the Old City walls or describes the Siloam pool itself. |

## Integration

- Every new suite passes (haesi 10, mandate 18, peraea 12, ASI 10 with 2 skipped without the local cache). The registration record validates as `rejected`, as reported. The chain, arrival and frozen-rule checks still pass.
- After review, the ASI tables were cut to limit how much survey text they reproduce: features.csv holds no quotes, and sites.csv holds one quote of 12 words or fewer for each of the 315 records within 1 km.
- Shared files changed: ACTIVE_TEST (last-session line, question 2, key reports) and its history file; OPEN_QUESTIONS R06 and R07 and the byte-identical atlas copy; the W2B report (v3 note); the Koḥlit chain (two new records on SULTAN-1: the opened 1:20,000 sheet and the unopened 1940s RAF mosaic, and the regenerated ranking, in which SULTAN-1 moves to tier 1 because an open record now exists).

## Exposure

- Sheet 19-14 is now exposed. It was opened under the protocol and cannot test SULTAN-1.
- Palestine Open Maps also serves a georeferenced 1940s RAF aerial mosaic that covers the strip. It was not opened. It is the cheapest record that could test SULTAN-1, and it must be opened only under the protocol.
- No HA-ESI or ASI text read in this round describes the strip. Five unread Jericho items in the IAA corpus might.

## Proposed but not made

- Gazetteer: move ain_duk to 31.89483, 35.42204 (±53 m), in a new input version.
- reference_points.json: add a grid-intersection candidate type and the worker's imagery reference points (listed in the registration record).
- search-effectiveness: join looks_haesi.csv and looks_asi.csv. Their detection numbers are null, so the join moves no posterior yet.
- Pre-registration R3 (east of the Jordan): needs the owner's approval and a site inventory (MEGA-Jordan or EAMENA).
- Access requests for MEGA-Jordan and EAMENA: drafts in [access_requests.md](../regional/peraea/access_requests.md). The owner decides whether to send them.
- Needs a person with a browser: the HA-ESI map search and the portal PDFs listed in the haesi README; the printed ASI volumes for page numbers; the 1:20,000 sheet margins.

## Follow-up, 10 October: the open RAF 1940s layer

The owner approved opening the Palestine Open Maps RAF layer for the strip north of Tell es-Sultan under the registration protocol ([RAF 1940s](../regional/raf_1940s/README.md); records `registrations/POM-aerial1940s-z16-jericho.*`).
- A resolvability gate was declared before the zone could be opened: a 1 m opening must span about 2 pixels (0.5 m effective resolution).
- The layer stops at zoom 16 (2.03 m pixels). Its effective resolution outside the zone is 9.2 m. The gate failed, so the zone was never viewed. The strip stays unexposed in every RAF image.
- The registration is invalid: only two of the declared controls can be identified at this resolution. SULTAN-1 is not tested.
- The next record is the RAF scans at the Hebrew University aerial archive (PS30 5107/5137, PS32 5069–5070; sorties of March–April 1945, 1:15,000). At 600 dpi they give about 0.64 m per pixel, just above the gate, so a higher scan resolution should be asked for. Ordering needs the owner (fee).
- The main source list now has a section for the datasets of this round ([sources.md](../sources/sources.md)).

