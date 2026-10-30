# Kochavi 1972 Stage 2: rarity coding of Kallai's Benjamin / Mount Ephraim survey (29 Oct 2026)

**Task.** This closes the part-2 pending item of `outcomes/kochavi-1972_2026-10-19b.json` (branch `method8-djd3-leg-2026-10-24`): "Stage 2 rarity coding of the 18 Kallai units". It was blocked only by the missing full-size photos of Kallai pp. 158–193.

**Protocol followed.** The procedure is `research/rarity/kohlit/stage2/PROTOCOL.md` (§3–§10), with the source-2 addendum procedure (`addendum_s2/PROCEDURE.md`) applied unchanged. Kallai 1972 is the original survey entry named in each unit's WBADB Survey_Ref, so it counts as source 2. Coder A coded only the new Kallai entry; `merge_source.py` appended those features (id prefix `s2k_`) after the Zertal Vol. I sheets. `match.py` and `protocol_constants.json` were not changed.

**Result.** No count changes anywhere. Main set, R1 Hel/Rom, branch A survey level: **k = 0, f = 20, m = 313 of N = 333**, the same as after Zertal Vol. I. Every row of the headline, the without-Nigro results, the sensitivity variants, the exposed-candidate table, the two-of-three list and coder agreement is identical to the vol1 result. Rarity stays **not measurable from available evidence** (pre-registration §6): m ≫ k. The landscape-wide frequency stays null. Nothing here identifies a site.

## Inputs and checks

- **Photos.** Downloaded from Drive folder `19KrO7YInKR35KZ17F34jWOnSME-lcyv_` using the manifest (`00_manifest.csv`). Each HEIC (5712 × 4284 px) matched its manifest `source_sha256`. I coded from crops of the converted images. The OCR draft was used only to locate entry headers by site number and grid; no coding value comes from it.
- **Packet inputs.** WBADB, SWP II and III, *Highlands* and Nigro 2011 were each fetched from their public sources and each matched the frozen SHA-256 values. *Highlands* came from TAU Alma open access and Nigro from the expedition's public Drive file.
  - `build_packets.py` rebuilt all 244 base packets byte for byte against `addendum_s2/vol1/packet_manifest_base.csv`.
  - `run_addendum_vol1.sh` on those packets reproduced the committed vol1 `summary.json`, `unit_results.csv` and `coder_comparison.csv` byte for byte. That vol1 output is the baseline here.
- **Run.** The chain is: first run → source-4 addendum → Zertal Vols. 2–4 → Zertal Vol. I → Kallai (`s2k_`) → `match.py run`. All merged sheets pass `match.py validate`.

## Per-unit coding

Columns:
- **Kallai-only** = conditions computed from the Kallai features alone.
- **Merged** = the registered value after the merge.
- A_s / A_t / B = branch A survey level, branch A text level, branch B.
- Pages are printed pages. In each spread photo the even page is on the right.

| Unit | Site | Page | Photo | Kallai features coded | Kallai-only (C1/C2/C3s/C3t) | Merged (C1/C2/C3s/C3t) → A_s/A_t/B | Exposed |
|---|---|---|---|---|---|---|---|
| S798 el-Qulʿah | 9 | 165 | IMG_1698 | none: fortress 28 × 28 m; plan (walls only, 10 m scale) | U/U/U/U | U/FAIL/U/U → FAIL/FAIL/FAIL (pre-70 set only) | no |
| S825 ʿAskar | 12 | 166 | IMG_1697 | pool (plastered, not in use, beside the village spring), no position | U/U/U/U | U/U/U/U → U | no |
| S827 Deir el-Ḥaṭab | 13 | 166 | IMG_1697 | cisterns in the village (none); cistern S of the village (S); ruined sheikh's tomb beside that cistern (S, mouth "beside", cavity false) | U/U/U/U | U/U/U/U → U | no |
| S1488 Kh. Sara | 38 | 169 | IMG_1696 | rock-cut cistern in the ruin (none) | U/U/U/U | U/U/U/U → U | no |
| S1525 Kh. er-Rafid | 42 | 169 | IMG_1696 | lime pit at the SE end of the summit (SE) | U/U/U/U | U/U/MATCH/U → U | no |
| S1623 Kh. Abu Falaḥ | 55 | 171 | IMG_1695 | none: village; apart from an olive press, no ancient remains found | U/U/U/U | U/U/U/U → U | no |
| S1658 Kh. Marjame | 65 | 172–173 | IMG_1694 | water pool adjoining the church on its E, with remains of a roofing vault (pool_def yes; E relative to *other*, the church at the tell's W foot) | U/U/U/U | U/U/MATCH/U → U | no |
| S1667 Kh. Samiyye | 66 | 173 | IMG_1694 | none: buildings, columns; water mill 300 m NE | U/U/U/U | U/MATCH/MATCH/U → U | no |
| S1963 Kh. Ḥaiyan | 96 | 178–179 | IMG_1691 | none: few remains, terraces | U/U/U/U | U/U/U/U → U | no |
| S2253 Kh. Tell el-ʿAskar | 105 | 180 | IMG_1690 | two bell-shaped cisterns on the hilltop (none) | U/U/U/U | U/U/U/U → U | no |
| S2376 Tell Maryam | 115 | 182 | IMG_1689 | elliptical rock-cut cistern 10 × 6 m at the fortress centre (none); pool 15 × 7 m at the hill foot, N slope (N) | U/U/U/U | U/MATCH/MATCH/U → U | no |
| S2411 Kh. ed-Dawwara | 117 | 182 | IMG_1689 | cisterns in the N (N); cisterns in the W (W) | U/**MATCH**/U/U | U/MATCH/U/U → U | no |
| S2431 Kh. el-Qubbe | 118 | 182 | IMG_1689 | cisterns and rock-cuttings (none) | U/U/U/U | U/MATCH/U/U → U | no |
| S2565 Kh. et-Tinat | 130 | 184 | IMG_1688 | none: buildings; rock-cut winepress in the W | U/U/U/U | U/MATCH/U/U → U | no |
| S2686 Kh. ʿEin Fara | 137 | 185 | IMG_1688 | none: tower, rock-cut moat NW, central building, dam at the wadi junction; **no cave sentence** | U/U/U/U | U/U/U/U → U | no |
| S2698 Kh. Abu ʿAum | 149 | 186 | IMG_1687 | built plastered pool "on the slope" (none); lime kiln in the building centre not coded | U/U/U/U | MATCH/U/U/U → U | no |
| S2759 Kh. Abu Musarraḥ | 147 | 186 | IMG_1687 | blocked water cistern inside the central building (none); cave sentence withheld (unmeasured) | U/U/U/U | U/MATCH/U/U → U | no |
| S2990 Qaṣr er-Rawabi | 157 | 188 | IMG_1686 | lime pit on the building's NW side (NW); cave sentence withheld (unmeasured) | U/U/U/U | U/MATCH/U/U → U | no |

Each unit's paraphrased evidence sentences are in `kochavi_stage2_units.csv`, column `evidence_paraphrase`. The sheets are in `kochavi_stage2_coded_A/`.

**Exposed flag.**
- No unit is flagged exposed. The owner's 25 Oct rule marks a unit exposed only when held Wadi Qelt material *with measurements* enters a packet. None did:
  - Site 137 has no cave sentence.
  - The cave sentences of sites 147 and 157 give no scale, dimension or level, so they stay unused, as the rule requires.
- The four units near ʿEin Farʿa / Wadi er-Rawabi are flagged `held_area_vicinity` in the CSV.
- The pool at site 149 (500 m E of ʿEin Farʿa) and the other non-cave features of 137, 147 and 157 were coded as ordinary entry content. D2 and the owner decision cover only the cave sentences. This is logged as an ambiguity (below).

**What the Kallai coding adds.** Only one Kallai feature satisfies any condition: the S2411 cisterns "in the north" (C2). C2 was already MATCH there from earlier sources. No merged condition value, unit verdict or count changes.

## Counts (`match.py`, primary rules, with Nigro; unchanged from Zertal Vol. I)

| Set | Branch | N | k | f | m | m full-coverage | m no adequate coverage | m stopped at Stage 1 |
|---|---|---|---|---|---|---|---|---|
| R1 Hel/Rom (main) | **A survey (headline)** | 333 | **0** | **20** | **313** | 248 | 65 | 143 |
| R1 Hel/Rom | A text | 333 | 0 | 19 | 314 | 249 | 65 | 143 |
| R1 Hel/Rom | B | 333 | 5 | 19 | 309 | 245 | 64 | 143 |
| R1 pre-70 | A survey | 499 | 0 | 32 | 467 | 380 | 87 | 255 |
| R1 pre-70 | A text | 499 | 0 | 31 | 468 | 381 | 87 | 255 |
| R1 pre-70 | B | 499 | 6 | 31 | 462 | 377 | 85 | 255 |
| R2 Hel/Rom | A survey | 101 | 0 | 0 | 101 | 59 | 42 | 24 |
| R2 Hel/Rom | B | 101 | 3 | 0 | 98 | 56 | 42 | 24 |
| R2 pre-70 | A survey | 138 | 0 | 0 | 138 | 84 | 54 | 39 |
| R2 pre-70 | B | 138 | 4 | 0 | 134 | 81 | 53 | 39 |

- The landscape-wide match frequency k/N_true is **null**, because m ≫ k (pre-registration §6).
- The full `summary.json` is attached as `kochavi_stage2_summary.json`.
- Coder agreement (63 double-coded units) is unchanged.

**Coder B.**
- Three of the 18 units are in coder B's sample: S1488, S1667 and S2565.
- The procedure ("Coder B, random sample") requires a blind coder B to code their Kallai entries. **That was not done.** This agent is coder A and cannot be blind, so their merged values rest on coder A's Kallai coding plus coder B's earlier sheets.
- For all three, the Kallai-only coding gives UNKNOWN on every condition, so a coder-B Kallai sheet with the same content could not change a merged value.
- No unit became a new coder-A match in any branch, variant or Nigro setting, so no full coder-B coding is triggered. S2565 matches branch B under the C1 ≤ 2 km variant, but it already did before this addendum.

## Ambiguities (recorded, not resolved by results)

Each was settled by the protocol text and earlier coders' practice, before matching. The sensitivity column shows what the other reading would give. All were computed after the run and are exploratory.

1. **S1623, site 55.** Kallai says that, apart from an olive press, no ancient remains were found.
   - PROTOCOL §7 needs a statement that a *feature class* is absent. This names none, so it is not coded as explicit_absence.
   - Read as an absence of C1, C2 and C3, it would make C2 and C3s FAIL. The unit is in the pre-70 set only, and that would add 1 FAIL to pre-70 branches A and B.
2. **S1658, site 65.**
   - The "water pool" has remains of a roofing vault. PROTOCOL §3 makes a pool that the source says is roofed into a pit. Kallai calls it a pool and reports only remains of a vault, so it is coded pool_def yes.
   - Its direction is east of the church, not of the tell (relative_to other, so UNKNOWN). That matches the arrival outcome `bearing-or-phase-miss:not-east`.
   - Recoded as a pit, nothing changes.
3. **Rock-cut moats (sites 65 and 137).** Both are coded as ditches, not pits, following the earlier coder note for S829.
   - Coded as a pit N of the unit, S1658 C2 would become MATCH. Branch A would still be UNKNOWN (C1 UNKNOWN), so no count changes.
   - The S2686 moat is NW, a quadrant edge, so it stays UNKNOWN either way.
4. **Lime pits and kilns.** The lime pits (sites 42 and 157, *bor sid*) are coded as pits, following S1380 and S2565. The lime kiln at site 149 is not coded, because a kiln is not a cavity with an opening.
5. **Site-internal directions.** "In the north / in the west" of the ruin (site 117) and "in the south of the village" (site 13) are coded as words relative to the unit, following S203, S577 and S1137.
6. **Held-area scope.**
   - D2 and the owner's 25 Oct decision cover the *cave sentences* of sites 137, 147 and 157. The other sentences of those entries, and site 149 (also at ʿEin Farʿa), were treated as unheld.
   - If the owner meant the whole entries: dropping them changes nothing except S2698 C1, whose MATCH comes from WBADB rows, not from Kallai. So no count would move.
7. **Edition and coverage.** Kallai's Introduction (pp. 153–157) was not used. `coverage.json` classes Kallai 1972 as partial, and these units keep the coverage class their Survey_Ref gives.

## Deviations

- **D-K1.** No blind coder B for S1488, S1667 and S2565 (see above).
- **D-K2.** Kallai's Hebrew is read in translation by the coder. The quotes in the sheets are short Hebrew strings, each under 15 words. Paraphrases are in English.
- **D-K3.** Packets were built without the Kallai text inside them: they are base packets, so they carry no Kallai excerpt. Coder A coded directly from the photos. This addendum therefore has no "packet v6" manifest. The matching uses only packet geometry, which is identical.
- **D-K4.** Site 152 (Kh. ʿAlmit, S2806; Tier-1) is not in the 19b pending list, and its entry on p. 187 was not opened. S2806 keeps its earlier coding.

## Exposure log

- **Opened:**
  - Kallai pp. 164–189 (11 HEIC spreads, IMG_1686–1698).
  - The OCR draft, pp. 152–195 block, used only to locate entry headers.
  - The Drive manifest.
- **Not opened:**
  - Spreads pp. 152–163 and 190–195.
  - Site 152's entry.
  - `00_README.md`.
  - ASI 1 pp. 92–150 (Bar-Adon) and pp. 196–242 (Gophna & Porath).
  - Anything on Yanun/Janoaḥ.
  - Any Copper Scroll image or XII 10 material.
- **`research/preregistration/`.** The only file opened there was the outcome record `kochavi-1972_2026-10-19b.json`, which the task named. Repo searches listed file paths there (for example `arrivals/items/kochavi-1972.md`) without opening them. Most greps excluded the folder.
- **Incidental Yanun exposure.**
  - `rarity/kohlit/README.md` (Stage 1a/1b sections) names Kh. Yanun and Yanun among the exposed candidates.
  - I also printed the Stage 1a rows of S1001 and S1053 (name, grid, Survey_Ref) to confirm that Kallai does not cover them. He does not.
  - Neither touches XII 10 or the Janoaḥ test, and nothing from them was used in the coding.
- **Held material seen:** the unmeasured cave sentences of sites 147 and 157 were read in order to judge whether they carry measurements. They do not, so they are unused.

## Files

- `kochavi_stage2.md`: this report.
- `kochavi_stage2_units.csv`: one row per unit with the coded features, Kallai-only and merged condition values, flags and paraphrase.
- `kochavi_stage2_coded_A/*.json`: the 18 coder-A Kallai sheets (PROTOCOL §10 format, before the merge adds `sources`).
- `kochavi_stage2_summary.json`: `match.py` summary after the merge.
- The working scripts and packets are in (session workspace) (not in the repo).
