# Koḥlit rarity count east of the Jordan (region R3): pre-registration

**Status: APPROVED, NOT RUN.** The project owner approved this plan with all eight recommended defaults in §8 on 9 October 2026 (in the session chat). Nothing has been counted, matched or scored. It runs only after an inventory source is granted (§8 decision 1). On 9 October the owner registered for EAMENA (access level pending), and a MEGA-Jordan request was drafted for him to send. Drafted 9 October 2026 UTC by the peraea worker ([draft](../regional/peraea/PREREG_DRAFT_R3.md)); this file is the approved copy. It follows the approved [R1 pre-registration](kohlit_rarity_2026-10-08.md) and its [Stage 2 protocol](../rarity/kohlit/stage2/PROTOCOL.md). Every section says only what differs from them.

**Question.** Within a fixed region east of the Jordan, how many settlements have a pool to the east (entry 11) and a pit to the north with graves at its mouth (entry 60)? Report "k of N, m unknown", as for R1. Rarity alone identifies nothing (R1 §6).

**What this count can and cannot say.** Goranson reads Koḥlit as a district east of the Jordan (W2A; *Copper Scroll Studies* pp. 226–228). R1 §1 already states that the count does not apply if Koḥlit is a district. R3 asks a narrower question: *if Koḥlit was one locality in Goranson's region*, how common is the entry 11 + entry 60 combination there? It does not test the district reading.

**Exposure (must be declared before coding).** The peraea worker has read reports for Machaerus, Kh. ʿAtaruz, ʿAin az-Zara, Kh. al-Mukhayyat, Madaba, Tall Hisban, ʿIraq al-Amir, Kh. as-Sur, Umm Hadar, Tall Barakat, Kh. al-Habbasa, Tulul adh-Dhahab, Wadi al-Kharrar, Tall el-Hammam, Tell er-Rameh, Tell Nimrin, Tall al-Kafrayn and Tall al-ʿUmayri ([features.csv](../regional/peraea/features.csv)). Some of those reports place features by direction (for example Machaerus: a reservoir on the northern slope, a cave east of the fortress). These units must be coded only from the §5 sources, like every other unit, and the coder must not be the peraea worker.

## 1. Readings

Unchanged from R1 §1 (branches A and B; Janoaḥ deferred).

## 2. Unit of analysis

Unchanged from R1 §2: a recorded settlement with Hellenistic or Roman occupation (the period labels used by the source). Sensitivity: any pre-70 settlement. The Jordanian record often gives "Hellenistic", "Roman" or "Nabataean" without sub-periods; all count as overlapping the window (as R1 does for Roman).

## 3. Region

- **R3 (default):** the area frozen in [plan.json](../regional/peraea/plan.json): east of the Jordan and the Dead Sea shore polyline, from the Yarmuk to the Arnon (Wadi Mujib), at most 40 km from the polyline. Its edges follow the river, two rivers and a distance, not any candidate.
- **R3a:** Josephus's Peraea (War 3.3.3: from Machaerus to Pella, from Philadelphia to the Jordan), operationally the R3 points between the latitudes of Machaerus (31.567°N) and Pella (32.45°N) and west of 35.93°E (Amman), excluding the Decapolis cities.
- **R3b (optional):** the Jordan-valley floor only (points ≤ 10 km from the polyline), the analogue of R1's rift side.

## 4. Conditions and tolerances

Unchanged from R1 §4 and Stage 2 §4–§11 (C1 45°–135° ≤ 1 km; C2 315°–45° ≤ 1 km; C3 survey ≤ 1 km in the north sector, text ≤ 10 m from the C2 opening; D/U pass, L fails; same variants). Grid bearings are computed from Palestine Grid or WGS84 points with the same precision rule (distance ≥ 3 × the coarser point precision). New: a JADIS/MEGA legacy point is given a precision of 1,000 m unless the record states better, because the legacy points were read from topographic maps (Myers and Dalgity 2012 p. 49).

## 5. Sources and coding

**Fixed sources, in order, the same for every unit** (each needs the owner's decision in §8):

| # | Source | What it supplies | Access now |
|---|---|---|---|
| 1 | **MEGA-Jordan** national inventory (DoA; legacy JADIS data on over 10,400 sites plus later records) | Units, points, periods; site elements (cisterns, tombs, pools) where recorded | Account through the DoA MEGA-Jordan Unit ([access_requests.md](../regional/peraea/access_requests.md)). Not used here. |
| 1-alt | **EAMENA** database (Research Access) | Units with coordinates, periods, feature descriptions, condition | Registration form; assessment of research interest ([access_requests.md](../regional/peraea/access_requests.md)). Not used here. |
| 2 | **The original survey entry** for the unit | Feature descriptions, sometimes directions and distances | Open for: Ji and Lee 1998, 1999, 2002 (ʿIraq al-Amir, Wadi al-Kafrayn; ADAJ 42, 43, 46); Khalil 1996 (Dead Sea east coast, phase 1; ADAJ 40); Dhiban Plateau Survey (ADAJ 41, 42, 44); Wadi Shuʿayb (ADAJ 33; ADAJ 59); Dayr ʿAlla regional project (ADAJ 49-55); Greater Amman survey (ADAJ 35). Not open: East Jordan Valley Survey 1975–76 (BASOR 222; Yassine 1988), Hisban regional survey (Ibach 1987), Glueck's *Explorations in Eastern Palestine* (AASOR 14–28). |
| 3 | **Conder, *Survey of Eastern Palestine* I (PEF 1889)**, the east-bank companion of the SWP Memoirs | Words for pools (birket), cisterns, caves, tombs, with directions | Public domain; to be located on an open archive before Stage 1 (not checked here). It covers only the ʿAdwan country (roughly Wadi Zarqa to Wadi Zarqa Maʿin). |
| 4 | **First excavation publication** for excavated units (plan plus water and burial passages, one-hour cap) | Positions on plans; dates | Open in the DoA archive for many sites (ADAJ, SHAJ); see [sources.csv](../regional/peraea/sources.csv) for those already read. |
| 5 | *(optional)* **ACOR *Archaeology in Jordan*** newsletters (open) | Recent seasons | Open (AIJ 1–3 read for this draft). |

**Stage 1 (scripted).** Search sources 1 (or 1-alt) and 3 within 2 km of each unit for pool words (R1 `words.json`, plus Arabic transliterations *birka*, *birket*, *bassin*, *réservoir*, *Becken* for the French and German reports). **Stage 2 (by hand)** as in the Stage 2 protocol. Coders: one plus a second coder on 20% and all matches; neither may be the peraea worker (exposure).

**Report**, per branch and level: N, k, f, m, with m split into "no adequate coverage" and "not recorded under a coverage survey". Also report which part of R3 each open survey covers (map of survey footprints), because R3 has no single full-coverage gazetteer like WBADB.

## 6. What results would mean

Unchanged from R1 §6. In addition: R1 and R3 results must not be pooled into one k, because their unit lists come from different inventories with different coverage. A small k in R3 under thin coverage is weaker than the same k in R1.

## 7. Coverage that exists now (from this round; EVIDENCE unless marked)

| Part of R3 | Open survey or excavation coverage read or listed | Gap |
|---|---|---|
| Lower Wadi al-Kafrayn and Wadi as-Sir (ʿIraq al-Amir) | Ji and Lee 1998, 1999, 2002 surveys with Palestine Grid points; Umm Hadar excavation (SHAJ 10, 11) | INFERENCE: survey points to 10–100 m; feature directions rarely given |
| Dead Sea east shore, Suwayma to Umm Sidra | Khalil 1996 with grid points per site | South of Umm Sidra not covered in phase 1 |
| Machaerus, ʿAtaruz, Madaba plateau edge, Mount Nebo | Excavation reports (ADAJ, SHAJ, AIJ) | Regional survey (Glueck; Madaba plains surveys) not open |
| Jordan valley floor, Damiya to the Dead Sea | Tell Nimrin, Tall el-Hammam, Wadi al-Kharrar excavations | The 1975–76 East Jordan Valley Survey is not open |
| Middle Jordan valley (Dayr ʿAlla, Zarqa) to Pella | Dayr ʿAlla regional project, Tulul adh-Dhahab, Pella reports | Unit-level inventory needs MEGA-Jordan or EAMENA |
| ʿAjlun hills and Gadara/Yarmuk edge | Gadara hinterland survey (AIJ 2), Wadi al-ʿArab survey | Same |

INFERENCE: without MEGA-Jordan or EAMENA, the unit list (N) cannot be built for R3 with the same completeness as WBADB gives R1. The text-level count would be almost all UNKNOWN, as in R1.

## 8. Decisions (approved by the owner, 9 October 2026: all recommended defaults)

| # | Decision | Recommended default |
|---|---|---|
| 1 | Run R3 at all | Only after an inventory source (MEGA-Jordan or EAMENA research access) is granted |
| 2 | Inventory source | MEGA-Jordan if granted; otherwise EAMENA Research Access; record which |
| 3 | Region | R3 default; R3a and R3b as sensitivity |
| 4 | Survey-entry sources (2) | Open ADAJ/SHAJ surveys listed in §5; list the closed ones as "not accessed" |
| 5 | Conder *Survey of Eastern Palestine* | Include as source 3 if an open scan is found |
| 6 | Coders | Two coders, neither the peraea worker; freeze `match.py` and word lists by commit hash first |
| 7 | Point precision for legacy JADIS/MEGA points | 1,000 m unless stated |
| 8 | Report beside R1 | Yes, never pooled |

## 9. Feasibility

**Biggest risk.** No open, region-wide unit inventory exists east of the Jordan. The two inventories (MEGA-Jordan, EAMENA) need accounts. The open surveys cover patches. Without one of the inventories, N is undefined and the count cannot start. INFERENCE: with research access, Stage 1 would take a few days, and Stage 2 a few weeks part-time, as for R1.
