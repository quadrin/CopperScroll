# Koḥlit rarity count: pre-registration (entries 11 and 60)

**Approved by Alex Kesin on 8 October 2026 UTC (7 October Los Angeles), with all nine recommended defaults in §7.** Drafted 7 October 2026. **Nothing has been counted, matched or scored.** The feasibility checks read only field lists and whole-dataset formats. Freeze the Stage 1 script and word lists by commit hash before Stage 1 runs. Schematics: [qualifying site](../schematics/entry_11_60_kohlit.svg), [all variants](../schematics/entry_11_60_kohlit_variants.svg).

**Question.** Within a fixed region, how many settlements have a pool to the east (entry 11) and a pit to the north with graves at its mouth (entry 60)? The answer is reported as "k of N, m unknown". It measures how common the combination is. It cannot identify Koḥlit (§6).

**Exposure.** The project has already read evidence for Tell es-Sultan, ʿEin Samiya (Kh. el-Marjama, Kh. Samiya), Kh. Yanun, Tell Muḥalḥil, ʿAin Feshkha, Qumran and the ʿEin el-Ghuweir stretch (W2C, follow-ups A–E). These sites are coded only from the §5 sources, like every other unit. Other knowledge stays out of k.

## 1. Readings

- **Entry 11 (II 13–14)**, בברכא שבמזרח כחלת במקצע הצפני, "in the pool east of Koḥlit, in the northern corner". Milik, Allegro 1964, Lefkovits and Puech all read it this way. Allegro 1960 ("in a hole") was replaced by his own 1964 reading. Lefkovits has "in the east of" (p. 135), so a pool in the site's eastern part also counts.
- **Entry 60 (XII 10–11)**, בשית שב··צפון כחלת … וקברין על פיה. **Branch A** follows the reading shared by everyone who examined the original (Milik, Wolters, Puech): a pit north of Koḥlit with graves at its mouth. The disputed second word (שבצח/שכנה/שבנה) does not change the geometry. The opening ("to the north", Milik; "hidden", Puech) is recorded, not required. **Branch B** ("buried", registry RB-B) drops the graves condition. **Janoaḥ (שבינח)** is not counted. It would put the pit at Janoaḥ and make Koḥlit a district, so it waits for the frozen XII 10 image protocol (`fd3f334`).
- The IV 1 restorations (Lefkovits שב[כ]חלת vs Puech שב[צפון כ]חלת) bear only on entry 15, which is not used, so no "cistern to the north" is imported. The count assumes entries 11 and 60 name one locality. If Koḥlit is a district (Goranson; Rashi), the count does not apply.

## 2. Unit of analysis

A unit is a recorded **settlement** (tell, ruin with buildings, village, fort, monastery) with **Hellenistic or Roman** occupation recorded (Hel, Rom, Rom1, Hel-Rom; major or other). The window is the registry's 50 BCE–70 CE (to 135 CE). Surveys cannot split it more finely: WBADB folds Hasmonean into Hel and Herodian into Rom1 (sourcebook p. 17), and *Highlands* leaves Roman undivided (p. 18).

Isolated caves, cisterns, tombs and installations are features, not units. One sensitivity run admits any settlement or tell older than 70 CE, because a name can attach to a ruin.

## 3. Region

Neighbouring entries imply no district. Entry 11 sits among Temple entries (9–10, 12–14), and entry 60 follows Gerizim, Beth Shean and Bezek (W2B `entries_v1`). So the region is geographic.

- **R1 (default):** all West Bank land east of Old Israel Grid **E 175.0 km** (a straight stand-in for the watershed), to the Jordan and the Dead Sea. This is the desert/rift side of the hills. Its edges follow the watershed and the West Bank boundary, not any candidate, and one gazetteer covers all of it.
- **R2:** land within **30 km of Kh. Qumran** (31.7418 N, 35.4594 E; `places_v1`), east of E 175, i.e. the find-spot plus a day's walk. It is not the default because its edge cuts the ʿEin Samiya valley, 30.1 km away (W2A `distances.txt`).
- Transjordan and Carmel lie outside. Results mean "if Koḥlit lay in this region", and the east bank is reported as uncovered.

## 4. Conditions and tolerances

Bearings and distances are measured from the unit's recorded centre point (grid north; it differs from true north by <1°, INFERENCE).

| Condition | Counts as present | Primary tolerance | Sensitivity |
|---|---|---|---|
| **C1 Pool east** (11) | An open basin or reservoir, built or rock-cut, including spring pools. It must be ≥3 m a side, or be called a pool/reservoir/birka/tank. Not: covered cisterns, vats, troughs. | 45°–135°, or the source puts it in or east of the site's eastern part; ≤1 km | ≤0.5; ≤2 km |
| **C2 Pit north** (60) | A non-funerary cavity with a surface opening: cistern, pit, silo, shaft, underground chamber, tunnel, rock-cut cave. Anything the source calls a tomb is excluded. | 315°–45°; ≤1 km | Tomb shafts allowed |
| **C3 Graves at mouth** (60A) | Any grave, tomb, burial cave or kokh | *Text level:* ≤10 m from the C2 opening (source or plan). *Survey level:* graves in the same north sector (≤1 km) | Dropped in branch B |
| **Dating** (all) | D = dated in or before the window; U = undated; L = securely after 135 CE | D or U pass; L fails | D only |
| Recorded only | The pool has corners; the opening faces north | n/a | n/a |

**Why these tolerances.** The scroll uses only four direction words (מזרח, צפון, דרום, מערב), and at VIII 11 it gives "west" and "south" separately rather than a combined term. So each word covers a 90° quadrant; the legacy registry's exploratory 315°–45° range is the same. *1 km* means immediate surroundings, since no text gives a distance. *10 m* means adjacent, with an allowance for plan error (the legacy registry used 5 m).

**Position rules.** (1) A plan or the source's own words beat grid points. (2) A bearing is computed from grid points only if the distance is at least 3× the coarser point's precision; otherwise it is UNKNOWN. (3) A verbal NE, SE or NW that sits on a quadrant edge is UNKNOWN. *Disclosure:* rule 2 was written knowing that the ʿAin es-Sultan spring point is 102 m SSE of the tell point, while SWP III p. 222 says the spring "comes out beneath the mound on the east" (W2C). The rule decides that case.

## 5. Sources and coding

**Fixed sources, in order, the same for every unit**
1. **WBADB** (Greenberg & Keinan 2009) XLSX: the units, points, periods, component text and nearby feature rows.
2. The **original survey entry** named in `Survey_Ref`.
3. **SWP Memoirs II–III**.
4. For excavated units only, the **first publication** listed in WBADB, limited to the plan and the water/burial passages, with a one-hour cap.
5. *(Decision 7)* **Nigro (ed.) 2011** Jericho-oasis catalogue, used for the oasis only.

Nothing else enters k. Kenyon beyond rule 4, Dorrell, Zissu and Mazar go into an "outside protocol" note.

**Stage 1 (scripted, all units).** Search sources 1 and 3 within 2 km of each unit for pool words (pool, reservoir, birke/birket, tank, basin, spring-house). If none is found, C1 is "not recorded" (UNKNOWN) and the unit stops there.

**Stage 2 (by hand).** For units with a pool word, extract every feature from sources 1–5. Each row of the sheet records type, source and page, position (plan, words, or grid point with its precision), distance, bearing and date code.

**Matching and coders.** A script applies §4 to the sheet; the script and word lists are committed by hash before Stage 1. One coder works in random unit order, and a second redoes a random 20% plus every match. Each condition is MATCH, FAIL or UNKNOWN. A FAIL needs a positive contradiction. **Silence is never a FAIL.**

**Report**, per branch and per level: N, k, f and m. Split m into "not recorded under a full-coverage survey" and "no adequate coverage". Also give excavated vs unexcavated, where each exposed candidate lands, every unit matching two of the three conditions, and one sensitivity table.

## 6. What results would mean

- **How to read k:** if Koḥlit lay in the region and the sources were complete, it would be one of k sites, or of up to k + m.
- **Small k and small m:** the combination is uncommon in the recorded landscape. The survey level is looser than the text, so a small survey-level k is the stronger result.
- **k ≥ about 5:** "fits reasonably well" carries little weight for any one site.
- **k = 0:** the current fits rest on evidence or tolerances outside the protocol. This is not a rejection.
- **m ≫ k:** rarity is *not measurable from available evidence*, the likely result at the text level.
- **What does NOT follow:** an identification (AGENTS.md needs discrimination plus an unseen prediction, and the candidates are exposed); anything about the treasure; anything outside the region or for the Janoaḥ/district readings; rarity on the ground rather than in the record.

## 7. Decisions for Alex

| # | Decision | Recommended default |
|---|---|---|
| 1 | Readings | Branches A and B; defer Janoaḥ until XII 10 is imaged |
| 2 | Region | R1, east of E 175 (R2 optional) |
| 3 | Unit periods | Hel/Rom recorded; one "any pre-70 ruin" run |
| 4 | Tolerances | §4: 90° quadrant, ≤1 km, ≤10 m |
| 5 | Headline level for graves | Survey level, text level beside it |
| 6 | Undated features | Allowed; dated-only also reported |
| 7 | Nigro oasis catalogue | Include; report k with and without it |
| 8 | Survey silence | UNKNOWN, with the split reported |
| 9 | Coding | Agent plus a second coder on 20% and all matches; freeze by commit hash |

## 8. Feasibility

| Source | Findings | Verdict |
|---|---|---|
| **DAAHL** | EVIDENCE: searchable by period and site/feature type, with drawn-area search and KML output; no bulk download stated ([Home.php](https://daahl.ucsd.edu/DAAHL/Home.php)). A record is lat/long + period/feature-type "components" + bibliography (Savage & Levy, *NEA* 77.3 (2014) 243–245). **Blocked:** proxy 502; robots.txt failure on `/DAAHL/Search.php` and `/About.php`; the [UCSD PDF](https://library.ucsd.edu/dc/object/bb5947262p/_1.pdf) is bot-checked. | INFERENCE: no positions within a site. Not needed. |
| **WBADB** | EVIDENCE: the [XLSX](https://emekshaveh.org/en/wp-content/uploads/2020/08/WBADB_data1.xlsx) has 6,050 survey and 980 excavation rows (grid X/Y, periods, free-text `Site_Components`, `Survey_Ref`); 44% are rounded to 100 m. [Sourcebook](https://www.tau.ac.il/humanities/abraham/publications/WBADB_sourcebook.pdf): components are "principal discoveries" (p. 17); one central point per site (p. 16); isolated features are listed inconsistently (p. 14); >70% full coverage, with a firing-zone gap (p. 11); the Emergency Survey recorded "only known sites" (p. 13); no survey "in densely settled Palestinian areas"; Israeli sources only (p. 28). | Supplies the frame, periods and Stage 1. No close bearings, mouth relations or feature dates. |
| **IAA ASI** | EVIDENCE: [survey.iaa.org.il](https://survey.iaa.org.il/) returned only a JavaScript shell. The ASI maps touch only the West Bank's western edge (sourcebook p. 11). | INFERENCE: does not cover R1. |
| **Printed surveys** | EVIDENCE: Bar-Adon 1972 (Kochavi ed., pp. 92–149, Hebrew; 346 WBADB rows) is online only as a [citation](https://dig.corps-cmhl.huji.ac.il/node/9141). Kallai 1972 is library-only (follow-ups B, E). *Highlands* is open access (follow-up C). SWP is public domain ([archive.org](https://archive.org/details/surveyofwesternp03conduoft)) and states relations in words. Kenyon enters only via rule 4. ESI/ʿAtiqot caves are already in WBADB. | Needed for Stage 2. The two core 1972 surveys are not in hand. |

**Coverage gaps:** the camp north of Tell es-Sultan, built since 1948 (follow-up D); Jericho town (sourcebook p. 28); the firing zones. INFERENCE: the p. 13 coverage table lists no full survey of the Jericho plain (check against Fig. 5).

**Effort (INFERENCE):** Stage 1 takes about 2 days. Stage 2 covers tens of units at 30–45 minutes each, plus library scans: about 1–2 weeks part-time.

**Biggest risk.** Bearings, distances, mouth relations and feature dates are in neither DAAHL nor WBADB. They must be hand-coded from survey volumes, and the two core volumes are Hebrew, library-only and not in hand. Surveys almost never record "graves at its mouth", and the key Jericho ground is built over. The text-level count will probably be mostly UNKNOWN.
