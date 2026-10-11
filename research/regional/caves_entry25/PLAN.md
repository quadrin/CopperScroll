# Plan: every recorded cave in the region, scored against entry 25 (VI 1–6)

Frozen plan. Written 11 October 2026 (UTC) by the caves_entry25 lane worker, before any cave record was coded or scored and before any unread ʿAtiqot 41 cave entry was opened. Repository base: dd040e3 (branch worktree-agent-a00fe441ed3f14a45). Any later change goes in a separate, labelled amendment file. This file is never edited after its freeze commit.

**What this is.** An exploratory regional inventory and count. It makes no identification claim. It changes no registered outcome, class or closed test. Its product is a denominator: how many recorded caves in the region satisfy, fail or leave unknown each clause of entry 25.

Labels used in the outputs: **EVIDENCE** (the source says it), **INFERENCE** (this worker's reasoning or measurement), **CLAIM** (an author's assertion without a field record). Unknown stays unknown (empty), never zero or "no".

## 1. The text and its clauses (derived before any feature is looked at)

Project text, VI 1–4 (edition-based, ETCBC display; `text/translation_en.json`, `text/readings.json` id `e25-direction`, `research/text/letter_controls/edition_checks.csv` VI 1–3): [ב]מערת העמוד של שני / [ה]פתחין הצופא מזרח / [ב]פתח הצפוני חפור / [א]מות שלוש. Project translation: "[In] the cave of the pillar with the two [en]trances, facing east, [at] the northern entrance, dig three [cu]bits: there is a jar, in it one scroll; under it 42 talents." Concordance: project entry 25 = Lefkovits item 25 (6:1–6:6) = Milik item 27 = Allegro item 26 (`tables/entry_concordance.csv`).

- EVIDENCE: Puech 2015 prints only the line-initial letters of VI 1–4 as restorations, and supplies the article before צופא as an editorial correction (`research/measurements/cycle4/puech_entry25.md`). The letters of מערת, העמוד, שני, פתחין, מזרח and הצפוני are not restorations in Puech.
- EVIDENCE: Milik 1960 p. 140 attaches the eastward aspect to the cave. Puech pp. 59–60 gives no explicit requirement that both mouths face east (`research/sources/entry25_direction_review_2026-10-02.md`).
- EVIDENCE: Puech p. 60 retains "pillar" for העמוד and records Allegro's alternative sense "platform or terrace".
- EVIDENCE: Allegro 1960 (item 26, p. 43; identification p. 104) reads the passage as the inner chamber of the platform of the east-facing Double Gate of the Temple (`research/history/allegro1960_treasure_extracted.md` line 48).
- Not independently checked here: Lefkovits 2000's apparatus for VI 1–3 (the repository records it as pending).

### Reading branches

| Branch | Basis | Feature type | Scored here |
|---|---|---|---|
| **B-PILLAR** | Milik 1960 p. 140; Puech 2015 pp. 59–60 (Lefkovits not independently checked) | a cave with a pillar/column, two openings, facing east, a northern opening | yes |
| **B-TERRACE** | Allegro's sense of עמוד as platform/terrace, recorded by Puech p. 60, kept with the cave (the project's existing "terrace" reading dimension in the decisions module) | a cave with a terrace/platform, two openings, facing east, a northern opening | yes |
| **B-GATE** | Allegro 1960 p. 43 and p. 104: the platform of the east-facing Double Gate (a Temple branch) | not a cave | **no.** This inventory bears on the cave branches only. B-GATE is recorded as "not a cave; not scored". |

Within each scored branch, the facing clause has the two orientation levels of the frozen aspect rule (A8): **cave** (`orientation = cave`, Milik's attachment) and **both-mouths** (`orientation = both-mouths`, the stricter project model). Every cave is scored on both.

### Clauses

| Id | Clause | Branches |
|---|---|---|
| C1 | a cave | B-PILLAR, B-TERRACE |
| C2p | a pillar or column (natural, rock-cut or built), in or at the cave | B-PILLAR |
| C2t | a terrace or platform at the cave | B-TERRACE |
| C3 | two entrances | both |
| C4 | facing east, by the frozen aspect rule, at level `cave` or `both-mouths` | both |
| C5 | a northern entrance (the northern member of the pair) | both |

Descriptors, not clauses: period of use in the window, excavation status, finds, published plan. The three cubits, the jar, the scroll and the 42 talents are not scored: no survey record observes them, and a deposit is a separate claim (AGENTS.md, "Separate claims").

## 2. Region

- **Boundary.** A rectangle on the Palestine/Old Israel Grid, **EPSG:28191** (Cassini-Soldner, Palestine 1923 datum; OIG metres = Palestine-grid km × 1000, no 1,000,000 m false northing): easting **180,000–197,000 m**, northing **091,000–150,000 m**. Corners in WGS84 (pyproj 3.8.0, PROJ 9.8.1): SW 31.4109 N 35.3153 E; SE 31.4106 N 35.4941 E; NW 31.9430 N 35.3160 E; NE 31.9427 N 35.4958 E. The same box in ITM (EPSG:2039) is about E 230,000–247,000, N 591,000–650,000.
- **What it holds.** The eastern Judean Desert: its fault escarpment and cliffs, the wadis cutting them and the marl terraces at their foot, from the Wadi el-Makkuk / Wadi Nuweiʿimeh area north of Jericho, past Jebel Quruntul, Wadi Qelt and Jericho, Qumran and ʿEin Feshkha, Naḥal Kidron, ʿEin el-Ghuweir and ʿEn Gedi, south to Naḥal Ḥever. The northern edge (N 150,000) is the northern frame of the 1993 survey map (ʿAtiqot 41 file 25). The southern edge (N 091,000) lies just south of Naḥal Ḥever. The western edge (E 180,000) is the western edge of the ASI sheets 83/12, 109/4 and 109/7. The eastern edge lies beyond the cliff foot and the Dead Sea shore.
- **Not in it.** Upper Wadi Qelt west of E 180,000 (ʿEin Fara); the Herodium sheet (ASI 108/2, which ends at E 180,000) and Naḥal Teqoa; Naḥal Mishmar and everything south of N 091,000; the Jordan Valley north of N 150,000. These are geographic exclusions fixed now, not source choices.
- **Membership test.** A cave is in the region if its best point lies inside the box (closed). A cave without coordinates is in the region if its source places it at a named locality inside the box ("by description"). A point within its own precision of the edge is kept and flagged `edge`.

## 3. Sources to inventory

Exposure status is defined in §8. Access routes: the owner's Mac (`~/Downloads`, through the remote-device tools, narrow filters only), the owner's Drive (by the IDs in `research/sources/drive_index.md`), the repository's notes, open web data. No browser automation. No sign-ins, loans, paywalls or bot checks are bypassed; such sources go to "Blocked" with their URL and pages.

| Key | Source | Route | What is coded |
|---|---|---|---|
| S1 | de Vaux, DJD III (1962), Part I: cliff sites 1–40, caves A and B, marl caves 7Q–10Q and the unfinished oval cave (pp. 3–17, 26–31) | repo extraction `research/history/djd3_text_cave_list_extracted.md` (read from the book's page images, 10 Oct) | every site the book calls a cave |
| S2 | de Vaux, RB 60 (1953) pp. 540–561, pl. XX | repo extraction and `research/history/devaux1952_cave_points/` | crosswalk and map points for S1 |
| S3 | Reed, BASOR 135 (1954) | Downloads PDF | numbering crosswalk and any cave description not in S1 |
| S4 | *ʿAtiqot* 41 Part 1 (Hebrew, IAA 2002): Regions I–XV, the excavation reports, the Index and the 1993 map | Downloads `Atiqot_Vol41_Iss1.zip` (or the six split zips; same archive, SHA-256 576e957a… per the repo) | every numbered cave and every cave group |
| S5 | ESI cave-survey reports inside the region: every report in ESI 2, 3, 5, 6, 7–8, 9 and 15 (Downloads) whose title or opening names a cave survey or cave excavation inside the box | Downloads PDFs; reports found by a title/heading scan of each volume's text layer for "cave" and the region's place names | every cave the report describes |
| S6 | Patrich and Arubas, IEJ 39 (1989) 43–59 | Downloads PDF | their Cave 13 and any other cave described |
| S7 | Bar-Adon, ʿAtiqot Hebrew Series 9 (1989), ch. B (Twin Cave) | repo notes only (`registration/entry25_twin_cave_features_2026-10-01.json`, `research/sources/baradon1989_*`) | Twin Cave |
| S8 | Jones's "north entrance" (Browning 1996, Amar 1998) | repo salvage records S14 | one row, CLAIM |
| S9 | ASI online maps whose sheet intersects the box | survey.iaa.org.il JSON services, method of `research/regional/asi_jerusalem/access.md`, at most one request per second, cached outside the repo | every site record whose name, additional names or description contains a cave word (§4) |
| S10 | West Bank Archaeological Database (Greenberg and Keinan 2009), `WBADB_data1.xlsx`, SHA-256 3db734cd… | emekshaveh.org URL (not committed) | rows whose name, type or components contain a cave word and whose X/Y lies in the box; added only under the rule in §5 |
| S11 | Zissu 2023 refuge-cave list | repo extraction `registration/zissu2023_extracted.md` | named caves inside the box not otherwise inventoried |
| S12 | Open-access refuge-cave and karst-cave catalogues (Eshel, Porat, Frumkin) | bounded web search, at most eight queries | caves inside the box, if a readable list is found |
| S13 | The 1960–61 Judean Desert expedition reports for Naḥal David and Naḥal Ḥever (IEJ 11–12) and Yadin 1963 | open copies only | caves inside the box, if readable |
| S14 | The four caves the repository already models: Twin Cave, Jones's "north entrance", Abu Saraj IV/11 and IV/17 | `research/feature_workbench/`, `research/schematics/searches/search_06_entry25_column_cave.py`, `registration/entry25_abu_saraj_features_2026-10-01.json` | ordinary rows, coded like any other |

Out of scope by instruction: the L-656 field file and IAA Archive cave records (not sought, not read).

## 4. Eligibility and coding rules

### 4.1 What is a row

1. A row is a cave the source itself calls a cave: מערה / מערות / מערת, "cave", "grotte", "Höhle", including hewn caves, burial caves, cave complexes, "small cave" and caves the source numbers as such.
2. **Not rows** (listed in `excluded.csv` with the reason): records the source types as a rock shelter, crevice, cleft, fissure, niche, pottery heap, pit, cistern, quarry, tomb or building and does not also call a cave. De Vaux's site 2 (heap), 9 and 17 (crevices), 12 (rock shelter), 15, 21 and 30 (clefts) and 35 (building) are therefore excluded by this rule; his 24 ("abri sous roche") likewise.
3. A record that calls the feature "cave or rock shelter" or equivalent is a row with C1 = unknown.
4. Each individually numbered cave is one row, even when its source describes it only inside a group ("V/30–47: all natural caves"). A group with a stated count but no individual numbers is one **cluster row** with `cluster_count`; its clauses are unknown unless a statement covers every member.
5. A row must lie in the region (§2).

### 4.2 Merging (one cave, several records)

- Same source, same number: one row.
- Across sources: merge only when a source states the identity (gives the other number or name), for example DJD III's "grotte 8 = 3Q". A hedged identity ("perhaps") is not merged; it is flagged `possible_duplicate_of`.
- WBADB rows (S10) whose bibliography cites any source in S1–S9 or S11 are not added as new caves. They serve as crosswalks or coordinates only. WBADB rows citing only other sources are added as rows.
- ASI records (S9) are primary records and are added, unless the record cites an S4 or S1 cave number, in which case they merge with that row.
- **Possible duplicates.** Two rows from different field campaigns are flagged `possible_duplicate_of` when their best points lie within **50 m**, or when they carry the same proper name. Rows from one campaign's own numbered list are never flagged against each other.
- N is reported twice: **N_rows** (all rows) and **N_min** (rows after merging every connected group of flagged possible duplicates). Cluster rows are reported separately as records and as their stated counts.

### 4.3 Coding each clause from a record

Coding reads the whole entry. A keyword list guides the search; every hit is read in context and coded by hand. Keywords: pillar words עמוד, עמודים, "pillar", "column", "pier", "pilier", "colonne"; terrace words טרסה, טרסות, משטח, רחבה, חצר, מרפסת, "terrace", "platform", "forecourt", "courtyard", "porch", "porche", "terrasse", "plate-forme", "cour"; opening words פתח, פתחים, פתחה, פתחיה, כניסה, חלון, "opening", "entrance", "mouth", "window", "ouverture", "entrée", "fenêtre"; direction words מזרח, מערב, צפון, דרום and their compounds, and the English and French compass words.

**C1, cave.** Match for every row admitted under 4.1(1). Unknown for 4.1(3) rows.

**C2p, pillar.** Match: the record reports a pillar or column (natural, rock-cut, part natural and part cut, or built) standing in the cave or between its openings, including a rock pillar that divides two halls or two openings. Fail: the record states there is none, or a published plan of the whole cave (with a scale) shows no pillar and the text names none. Unknown: anything else, including a verbal description that does not mention a pillar. The pillar's kind and position are recorded as given.

**C2t, terrace.** Match: the record reports a terrace, platform, forecourt, courtyard or porch in front of or at the cave mouth (built or rock-cut). A natural ledge alone does not count. Fail: the record states there is none, or a published plan that covers the cave front shows none. Unknown otherwise.

**C3, two entrances.** `n_openings` counts the exterior openings the record gives for the cave: entrances, openings, mouths and windows in the cave's walls that open to the outside. Roof holes, chimneys and shafts count only if the record calls them an entrance or opening. A blocked or partly blocked opening counts. Interior doorways between rooms do not count.
- Match: exactly 2.
- Fail: exactly 1, or 3 or more.
- A record that describes the cave's opening in the singular ("its opening faces east", "the entrance is 2 m wide") and mentions no other opening is coded `n_openings = 1`, basis `singular description`.
- Unknown: no count can be read.

**C4, facing east.** The frozen Entry 25 mouth-aspect rule, `research/preregistration/entry25_iv17_rules/RULES.md` and `rules.json` (version 1; SHA-256 794a4e5e… and 24a1377d…), applied unchanged, using the functions of its `check_rules.py` read-only (`word_interval`, `interval`, `verdict`, `combine_mouths`, `cave_interval`, `mean_interval`, `hull`, `northern_member`).
- Inputs per record: a compass word (A4: half-width 45° at 4-point, 22.5° at 8-point, 11.25° at 16-point; resolution 8-point when the **source report** uses any intercardinal word for any opening, otherwise 4-point; no north allowance on words); a stated numeric bearing (h = stated precision or 10°, plus the A2 north allowance); or a plan measurement (A3–A4).
- Coding of words: a facing stated for the cave as a whole ("the cave faces east", "a cave opening to the east") is a cave-level word. A facing stated for each opening, jointly or separately ("both openings face east", "the openings face east"), is a word for each mouth.
- Levels (A8): **both-mouths**: `combine_mouths` over the per-mouth verdicts; not-measurable when the record shows fewer than two mouths; silent when no mouth has a facing. **cave**: a cave-level word or value is used directly; one mouth gives its own interval; two or more mouths give `cave_interval(facade normal, mouth intervals)`, where the facade normal needs the mouths' positions (from a plan); without positions the cave level is not-measurable.
- Plans: a published plan is measured under A3–A4 only for caves that, on the record, have exactly two openings and also a pillar (B-PILLAR) or a terrace (B-TERRACE) stated or drawn. This triage applies to every cave alike. Other plans are used for counts only. For IV/17 the repository's recorded Plan 5 chord endpoints and arrow are used (exposed; exploratory).
- Mapping to the clause: PASS → match; FAIL → fail; INCONCLUSIVE, NOT MEASURABLE, SILENT → unknown. The verdict word is kept beside the clause value. The primary sector (45°–135°) sets the clause. The three sensitivity sectors (67.5°–112.5°, 62°–118°, 22.5°–157.5°) are reported in `aspect.csv` and never change a clause.
- A9 (phase) is applied: if a record shows the aperture was cut or enlarged after the ancient phase, the verdict is marked `reported-only`.
- A10: no verdict in this lane has a class effect. For the roster caves (IV/17, IV/11, Twin Cave), records already in the repository are exposed; any verdict on them is exploratory. If a record first read in this lane gives a facing for a roster cave, its verdict and the candidate outcome id are reported to the integrator and nothing else is done with it.

**C5, northern entrance.** Match: the record names a northern opening of the pair, or describes two openings (or two units with their openings) as northern and southern, or a plan with a north arrow decides the northern member by A6 (`northern_member`). Fail: the record shows fewer than two openings (n_openings = 1 under C3). Unknown otherwise (A6 cannot fail a pair).

### 4.4 Descriptors

- **Period in the window** (Hasmonean to 135 CE, as stated by the source): `yes` when every period the source gives for the cave's use or finds lies in the window (Hasmonean, Herodian, Early Roman, 1st century BCE or CE, late Second Temple, First Revolt, Bar Kokhba, de Vaux's "Qumran type" or "Herodian" pottery and lamps); `partly` when the source gives a period that only partly overlaps (Hellenistic unqualified, late Hellenistic, Roman unqualified, Second Temple unqualified, Hellenistic–Roman); `no` when every stated period is outside; empty when none is stated. A cave can be `yes` with other periods too; then the field reads `yes+other`. For the counts, `partly` is unknown.
- **Excavation status**: `excavated` (the source reports an excavation of the cave), `sounded` (a sounding, trial trench or clearing of part), `surveyed` (surface only), `plundered` added as a flag when the source says so, empty when not stated.
- **Finds**: a short paraphrase, 12 words or fewer quoted.
- **Published plan**: figure or plan number and page, or "none".

### 4.5 Coordinates

- Recorded as printed, with the printed CRS. Converted with pyproj: EPSG:28191 → EPSG:4326 and EPSG:2039 (transformations as in `research/history/devaux1952_cave_points/README.md`). ASI New Israel Grid values: EPSG:2039, as in `research/regional/asi_jerusalem/access.md`. WBADB X/Y: EPSG:28191 without the false northing.
- **Precision**: the source's stated precision; otherwise half the printed unit (for example, 1937/1293 is a 100 m unit, ±50 m; 19035/14370 is a 10 m unit, ±5 m nominal), labelled `nominal`. Group-centre points carry the group box half-diagonal. Map-digitised points carry their stated error.
- The reference point is the source's point (cave, mouth or group centre), recorded in `coord_basis`.

## 5. Output tables

- `caves.csv`: one row per cave. Columns: `cave_id`, `name_number`, `source_records` (source key, printed pages, table/row, figure), `other_ids`, `lineage` (field campaign), `feature_type_source`, `row_kind` (cave / cluster), `cluster_count`, `coord_printed`, `crs_printed`, `x_oig`, `y_oig`, `lat`, `lon`, `precision_m`, `coord_basis`, `in_region`, `n_openings`, `openings_basis`, `opening_facings`, `facing_basis`, `facing_resolution`, `north_case`, `pillar`, `pillar_kind`, `pillar_position`, `pillar_basis`, `terrace`, `terrace_basis`, `northern_member`, `northern_basis`, `published_plan`, `period_stated`, `period_in_window`, `excavation_status`, `finds`, `exposure`, `first_read_utc`, `possible_duplicate_of`, `notes`.
- `scores.csv`: one row per cave × branch (B-PILLAR, B-TERRACE) × orientation (cave, both-mouths) × rule set. Columns: `cave_id`, `branch`, `orientation`, `ruleset`, `c1`, `c2`, `c3`, `c4`, `c4_verdict`, `c5`, `result` (`all-match` / `fail` / `unknown`), `n_match`, `n_fail`, `n_unknown`, `failing`.
- `aspect.csv`: per cave and level, the interval and the verdict under the primary and every sensitivity sector.
- `excluded.csv`: records read but not admitted, with the reason.
- `summary.json` and the README table: counts per branch × orientation × rule set.
- `intake/`: the arrival intake record for ʿAtiqot 41 (§8) and the source manifest (file names, sizes, SHA-256, pages read).
- `scripts/`, `tests/`.

### Rule sets

| Rule set | Change from primary |
|---|---|
| `primary` | as §4 |
| `s_open_ge2` | C3 matches for 2 or more openings; C5 needs 2 or more |
| `s_singular_unknown` | a singular description gives `n_openings` unknown, not 1 |
| `s_pillar_between` | C2p matches only when the pillar stands between the two openings or the two units; unknown when its position is not given; fail when the record places it elsewhere |

## 6. Decision wording

For each branch × orientation × rule set:

- **all-match (k)**: every clause is a match.
- **fail (f)**: at least one clause fails.
- **unknown (m)**: no clause fails and at least one is unknown.
- k + f + m = N.

The README reports: "**k match every clause, f fail at least one, m unknown, of N**", then partial matches by clause (match / fail / unknown for C1–C5), for N_rows and N_min, with cluster records separately. It names the rows in k. It states for each of the four modelled caves which clauses match, fail or stay unknown. It states that a match is compatibility only: no identification follows, no deposit is implied, no registered result changes, and no regional rarity claim can be made while m is large or the inventory has coverage gaps (each gap is listed). B-GATE is reported as "not a cave; this inventory does not bear on it".

## 7. Tolerances and numbers fixed now

- Region box: §2. Possible-duplicate distance: 50 m. Precision: §4.5.
- Aspect sectors, allowances and uncertainty terms: those of `rules.json`, unchanged.
- Plan measurements (when triggered by §4.3): endpoint radius r = max(0.10 m, 0.5 mm at print scale, 2 px on the raster); arrow endpoint e = 0.5 mm at print or 2 px; distortion d = 1°; north allowance per A2 (6° for an unstated north).

## 8. Exposure (what was seen before this freeze) and how records are marked

**This worker read, before writing this plan:** AGENTS.md; the lane rules; ACTIVE_TEST; the frozen aspect rules (RULES.md, rules.json, README); the Koḥlit rarity README (Stage 1a–1b); the ASI Jerusalem README and access note and its maps list; the arrival register README, ARRIVAL_PROCEDURE and the item file `iaa-archive-cave-records.md` (including its predictions); the entry 25 text, reading and concordance rows; the entry 25 schematic; Puech entry 25 audit; the direction review; Allegro's item 26 row; `registration/atiqot41_region_v_extracted.md` (all); `atlas/research/atiqot41_iv11_iv17_review_2026-10-01.md` (all); the ESI 6 and ESI 7–8 reviews (all); the DJD III extraction (all); the de Vaux 1953 extraction (table and §2); the de Vaux 1952 points README and CSV head; `search_06_entry25_column_cave.py` (header and matrix); the Twin Cave and Abu Saraj feature JSON (part); the Zissu 2023 extraction; salvage-record rows S09, S10, S13, S14, S15, S20; the Bar-Adon summary review (part); the ʿAtiqot 41 zip's file list (titles only); and a repository grep for ʿAtiqot 41 cave numbers with their contexts (II/13, IV/1, IV/8, IV/11, IV/17, V/1, V/22, V/26, V/28–30, V/38, V/39, V/48–51, V/59, V/64, V/69, VII/1, VII/3, VII/11, VII/12, VII/15, VIII/28, VIII/29, IX/9, IX/10, IX/17, IX/21, IX/22, X/47, XI/1–5, XI/18–22, XII/49, XII/50, XII/52, XIV/1–4, XIV/51, XIV/53).

So these ʿAtiqot 41 parts are **already exposed**: Sion Regions IV and VI pp. 43 (Map IV–VI), 61–64 (IV/11 context, IV/17, Plan 5), 81–82 (Table 1); Feig IV/11 pp. 85–90; Aronshtam Region V pp. 91–104 (Table 1 rows V/26, V/28–30, V/30–47 header, V/38, V/48, V/49, V/50, V/59, plans of V/50, V/59, V/64); Eisenberg V/49 pp. 105–121; Abeles Region VII pp. 123, 125, 135–137; Baruch et al. Region XI pp. 187, 189, 195–198; Dahari Region XIV pp. 229–241, 246; the Index pp. 257–260; the 1993 map. Some WBADB components naming ʿAtiqot 41 caves near Kh. Qumran and Jericho were quoted in the Koḥlit Stage 2 packets.

**Marks in `caves.csv` (`exposure`):**
- `exposed-repo`: the cave's record content is in the repository at base dd040e3 (found by `scripts/exposure_audit.py`, which greps the repository outside this folder for the cave's number or name, and by the list above).
- `page-opened-before`: the cave's entry stands on a page that an earlier worker opened (the pages listed above), but its content is not recorded in the repository.
- `unexposed-at-freeze`: first read in this lane after the freeze commit. Every remaining ʿAtiqot 41 cave entry (the Tier 1 records of the arrival register) is marked so when read, with the UTC time of first reading.
- `exposed-this-worker`: read by this worker before the freeze (none beyond the repository notes listed above).

**Arrival register.** The ʿAtiqot 41 cave entries for the Qumran cliffs, the Jericho escarpment and Wadi Qelt are the same survey lineage as item `iaa-archive-cave-records` ("whichever is opened first is the observation"). `arrival.py check` printed `manifest: ok (29 files)` on 11 October before this plan. The register (MANIFEST.md, commit 6fee376, committer time 2026-10-09T20:20:05Z) and the aspect rules (commit 2ae0976, 2026-10-09T21:39:21Z) are on GitHub main. Before any S4 text is opened, an intake record (file names, sizes, SHA-256) is written to `intake/`. The extraction is made in `caves.csv`. This worker has already read that item's predictions, so extraction and comparison are not blind; the comparison and the outcome record are left to the integrator (ARRIVAL_PROCEDURE §3.2), and the disclosure is repeated in the intake record.

## 9. What would make a result not usable

- A source in §3 that cannot be read is listed under Blocked with its URL and pages; the region's coverage gap is stated; the counts are not presented as landscape-wide.
- If the coded clauses depend on a coding call that is not EVIDENCE, the row's `notes` says so.
- No result here can support identification: there is no reserved unseen observation in this lane, and none is claimed.
