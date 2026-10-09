# Concealment contexts: frozen plan

Worker: concealment. Written 9 October 2026 UTC, before any comparison data were coded. The SHA-256 of this file and the freeze time are in README.md. Any later change creates a new, labelled exploratory run; it does not replace this plan.

## 1. Question

Where did people in the southern Levant, 150 BCE to 135 CE, actually hide valuables? Does the Copper Scroll's mix of hiding places look like that record?

This is a base-rate comparison in the manner of the Richard III trait frequencies. It speaks only to the kind of list (R12: inventory form). It says nothing about any location, any identification, or whether any deposit existed.

## 2. Exposure before freezing (honest record)

- I read the T02 report and the T02 `hoards.json` fields for all 76 records, including `findspot_text`, `provenance` and the T02 findspot tags.
- I read the CHRE context fields of two records in T02 `chre_details.json` (Ophel Cave; Hirbet Marzouk).
- I read the project translation of all 61 entries (`text/translation_en.json`) and the labels and edition readings in `text/readings.json`.
- I did not tabulate either distribution. I computed no comparison.
- Prior expectation (general background, not data): hoards are mostly reported from buildings and caves; the scroll names many water installations and tombs. I record this so a reader can judge.

## 3. Window

- Main: 150 BCE to 135 CE (years -150 to 135; no year 0 correction).
- Sensitivity: 63 BCE to 70 CE (-63 to 70).
- Date of a concealment = the source's deposition date range. For coin hoards without one, use the closing date: CHRE "Terminal year (earliest)" to "(latest)", or the latest coin. For documents and vessel caches, use the source's stated deposition period.
- A row is in a window if the midpoint of its date range lies inside the window. Rows without any date are excluded and listed.

## 4. Region

- Main: the southern Levant = findspots in modern Israel, the Palestinian Territories, Jordan and the Golan. CHRE multi-country labels such as "Israel, Palestinian Territories" count as inside.
- Sensitivity: Judaea and the Jordan valley only. Box J (Judaean hills, Judaean Desert, west Dead Sea shore): latitude 31.20 to 32.05, longitude 35.00 to 35.60. Box V (lower Jordan valley floor): latitude 31.70 to 32.55, longitude 35.45 to 35.70. Coordinates as given by the source (WGS84 decimal degrees).
- A row without coordinates is inside the sensitivity region only if the source names a place inside a box (for example Jericho, Jerusalem, Bethlehem, Hebron, "Judaean Desert"). "Israel", "Palestine" or a dealer label alone is outside the sensitivity region but inside the main region.

## 5. What counts as a concealment

Include:
1. Coin hoards: two or more coins deliberately deposited together, as the source classifies them (CHRE "Hoard", or "hoard" in the report).
2. Caches of metal vessels, jewellery, bullion or other valuables deliberately deposited.
3. Deliberately hidden documents or sacred objects (for example scroll jars, document bundles, a genizah-type deposit).

Exclude:
- Grave goods: objects placed with a body as part of the burial. A hoard hidden in a tomb, as the source reports it, stays in.
- Foundation deposits, if the excavator or primary source classifies the deposit as one. If only a later author proposes this, keep the row and flag it.
- Votive offerings at a shrine; mint or workshop debris; single coins; scattered coins that the source does not call a hoard or cache.
- Qumran Cave 3, the Copper Scroll's own findspot.

## 6. Sources and search protocol

Search by object type only ("hoard", "cache", "treasure", "scrolls", "documents", with period or region words). Never search with context words (cistern, pool, channel, tomb, cave, wall, floor, stone, threshold, pillar, field, ruin). This keeps the context distribution from being steered by the scroll's vocabulary.

- S1. T02 `hoards.json` (all 76 records). Reuse its find-context text and citations. Re-apply this plan's window, region and definition.
- S2. CHRE detail pages (chre.ashmus.ox.ac.uk, open access) for every hoard in T02 `chre_list_raw.csv` whose midpoint date lies in the main window, plus a CHRE search for Jordan in the same window. Reuse T02 `chre_details.json` where it already holds the record; fetch the rest.
- S3. Non-coin concealments (vessel caches, documents, sacred objects) in open-access publications.
- S4. A bounded web search for further in-window hoards and caches in open-access reports (HA-ESI, IAA releases, open ʿAtiqot, open journal articles). At most 25 queries. Stop earlier after three consecutive queries add no new eligible row.
- S5. The owner's Drive library, read-only, only if a Drive tool returns usable text quickly. Optional.

Every row cites a source with page, section or URL. Quotes are 12 words or fewer. Failed links go in README.md.

## 7. Unit and duplicates

- One row per reported concealment (one hoard, one cache, one document deposit).
- Rows that one source reports as parts of a single deposit event (same site, same locus, same find season) share a `cluster_id`. Example: several pots from one locus.
- The main test counts clusters. A cluster takes the most frequent fine category among its rows; a tie goes to the lowest row id. Its coarse group follows from that row. A sensitivity run counts rows.
- If two sources describe the same hoard, keep one row and cite both.

## 8. Coding rules

Each row gets three coded fields from the reported wording: `setting`, `placement` and the presence of a container. These give the fine category and the coarse group by a fixed function.

### 8.1 Setting (where)

| setting | report wording or scroll term |
|---|---|
| cistern | cistern, water cistern; scroll בור |
| pool_reservoir | pool, reservoir, miqveh, basin, spring, bath basin; scroll ברכה, אשיח, ים, מעין, מבוע, קבוץ, שוקת |
| channel | channel, aqueduct, conduit, drain, outlet, waterfall; scroll אמה, מזקא, ביב, זרב, יציאת מים, קול מים, חריץ |
| water_pit | scroll only: שית, שיח, שוחה (repo lexicon class "water installation / feature") |
| tomb | tomb, burial cave, kokh, loculus, funerary monument, mausoleum, CHRE context "Burial"; scroll קבר, משכן, בית משכב, נפש, יד |
| cave | natural cave, rock shelter, crevice or fissure in natural rock, refuge cave, hiding complex; scroll מערה, סדק |
| structure | house, room, courtyard, shop, street, building, fortress, casemate, tower, storeroom, columbarium or dovecote, underground chamber, bathhouse room that is not a pool; scroll חצר, צריח, שובך, מצד, משמרה, בית |
| ruin_heap | the source says the deposit was placed in a ruin, heap, cairn or mound; scroll חרבה, יגר, רגם, תל. Hoards found in a building's own destruction debris take the building as setting. |
| open_ground | field, open ground, slope, valley, road, quarry, garden outside buildings; scroll שלף, דור, עמק, גי, נחל, דרך |
| unknown | not reported, or too vague: "near X", a dealer's label, CHRE "Natural feature" with no cave, rock or field detail |

If a deposit lies inside a water installation, tomb or cave that is itself inside a structure, the water installation, tomb or cave is the setting.

### 8.2 Placement (where within the setting)

Order of precedence when several cues are present:
1. under_stone_threshold: under a stone, slab, threshold, doorway, door or steps.
2. wall_cavity: niche, inside a wall, crack between wall stones, door-frame hollow.
3. pillar: at, under or in a column or pillar.
4. under_floor: under or in a floor, between floors, a pit dug in a floor or courtyard, or a scroll "dig (חפור) N cubits" inside a structure.
5. container_buried: a container buried in open ground.
6. corner: at a corner, with no digging or wall cue.
7. upper_storey: in an upper storey.
8. floor_surface: on a floor, in ashes, scattered.
9. not_stated.

### 8.3 Fine category (13 named, plus two residual codes)

| code | fine category | rule |
|---|---|---|
| C01 | cistern | setting cistern; also water_pit in the main coding |
| C02 | pool/reservoir | setting pool_reservoir |
| C03 | channel/aqueduct/conduit | setting channel |
| C04 | tomb or burial cave | setting tomb |
| C05 | natural cave or shelter | setting cave |
| C06 | wall cavity | structure + wall_cavity |
| C07 | under floor | structure + under_floor |
| C08 | under a stone or threshold | (structure, ruin_heap or open_ground) + under_stone_threshold |
| C09 | jar buried in ground | open_ground + container_buried, or open_ground with a container and a scroll "dig" |
| C10 | near a column/pillar | structure + pillar |
| C11 | field or open ground | open_ground, other placements |
| C12 | ruin or heap | ruin_heap, other placements |
| C13 | other (known) | structure + corner, upper_storey or floor_surface |
| C14 | structure, placement not stated | structure + not_stated |
| UNK | unknown | setting unknown |

Water installations, tombs and caves take their setting category whatever the placement.

### 8.4 Coarse groups (main test)

| group | settings |
|---|---|
| G1 water installation | cistern, pool_reservoir, channel, water_pit |
| G2 tomb | tomb |
| G3 cave | cave |
| G4 structure | structure |
| G5 open air | ruin_heap, open_ground |

Unknown is excluded from every test and reported separately. Silence is not absence.

### 8.5 How found

- excavation: first found in a controlled excavation or archaeological survey.
- chance: first found by accident by non-archaeologists (farming, building, hiking) and reported.
- looting_recovered: found by unauthorised digging, or acquired from dealers, the market or a seizure, finder unknown.
- unknown: not stated.

## 9. Scroll coding

- One row per canonical entry (61; `tables/entry_concordance.csv`).
- The primary deposit is the one holding the entry's main valuables (precious metal, vessels, or the document in entry 60); if two are equal, the first named. Secondary deposits are listed but not tested.
- Branch P: the project translation (`text/translation_en.json`).
- Branches Pu (Puech 2006/2015), M (Milik 1960/1962) and L (Lefkovits 2000): the same as P, except where `text/readings.json` records that edition's reading of the primary deposit's setting or placement and that reading maps to a different fine category. Each change cites the readings.json id. All four branches are run.
- Pit sensitivity: scroll water_pit rows are set to unknown.
- Citations: T02 `entry_features.csv` (landmark classes), `tables/landmark_lexicon_index.csv` (term classes), the translation lines, and readings.json ids.

## 10. Statistic

- Table: 2 rows (scroll, comparanda) by the coarse groups G1 to G5, unknown excluded. Columns with zero total are dropped.
- Test statistic: Pearson chi-square. p-value by permutation: shuffle the scroll/comparanda labels over the pooled rows, 20,000 times, `random.Random(20261009)`; p = (1 + count of permuted statistics ≥ observed) / 20,001.
- Effect size: dissimilarity index D = ½ Σ |p_scroll − p_comparanda| (0 = same mix, 1 = no overlap). 95% interval: percentile bootstrap, 2,000 resamples of each side separately, `random.Random(20261009)`.
- Descriptive only: adjusted standardised residuals per group, to show which groups drive any difference.
- Secondary: the same test and D on the fine categories C01 to C14.

## 11. Runs

Main: branch P, main window, main region, clusters, all concealment types, coarse groups.

One-factor sensitivity runs (each changes one thing from the main run):
1. window 63 BCE to 70 CE;
2. region Judaea and the Jordan valley;
3. branch Pu; 4. branch M; 5. branch L;
6. pit sensitivity (scroll water_pit set to unknown);
7. rows instead of clusters;
8. coins and metal only (drop rows whose objects are only documents or sacred non-metal objects, on both sides; scroll entry 60 drops);
9. fine categories (secondary test).

Reporting-bias check:
- B1. Within the comparanda (main window and region, clusters): excavation versus non-excavation (chance plus looting_recovered), same test and D.
- B2. The scroll against excavated comparanda only, and against non-excavated comparanda only.
- B3. Share of unknown context by how found.

## 12. Decision wording (fixed)

For each run, with p and D from section 10:

- **DIFFERENT** if p < 0.05 and D ≥ 0.25: "The scroll's mix of hiding places differs from the recorded regional practice. This is compatible with a literary or idealised list, with a list of a different kind of deposit than the recorded hoards, or with reporting bias in the archaeological record. It does not identify any place and does not show that the deposits did or did not exist."
- **SIMILAR** if p ≥ 0.05 and D < 0.25: "No difference was detected. The scroll's mix is compatible with the recorded regional practice. This does not show that the list is real."
- **INCONCLUSIVE** otherwise: "The test and the effect size disagree; these data cannot separate the two readings."
- **NOT TESTABLE** if a run has fewer than 30 comparanda clusters (or rows, in run 7) with a known context.

The 0.25 threshold is a convention fixed here, not derived from data: a quarter of one list would have to change group to match the other.

Robustness: the main verdict is "robust" if every one-factor run gives the same verdict word. Otherwise the README lists the runs that change it.

Reporting sensitivity: the main verdict is "reporting-sensitive" if B1 gives DIFFERENT, or if the B2 verdicts differ from each other.

## 13. Labels and limits

- EVIDENCE: what a source reports about a find context. INFERENCE: my coding of that report into a category, and every test result.
- The scroll side codes one edited text, not independent observations. Entries are not independent deposits.
- The comparanda are what was found and published, not what was hidden. Hoards that were recovered in antiquity leave no record.
- No identification claim, no outcome-ledger count, no location inference.
