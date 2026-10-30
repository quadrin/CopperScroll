# Kochavi 1972 Stage 2: rarity coding of Gophna & Porat (Ephraim and Manasseh) and Bar-Adon (Judaean Desert and Jericho plain) (30 Oct 2026)

**Task.** This is an addendum to the Koḥlit rarity count (Stage 2), following the Kallai addendum of 29 October (Addendum 4). Coder A coded the survey entries of Gophna & Porat 1972 and Bar-Adon 1972, both in Kochavi (ed.), *Judaea, Samaria and the Golan* (ASI 1), for every Stage 2 unit whose WBADB Survey_Ref names one of them. The frozen matcher was then rerun.

**Protocol followed.**
- The procedure is `research/rarity/kohlit/stage2/PROTOCOL.md` (§3–§10), with the source-2 addendum procedure (`addendum_s2/PROCEDURE.md`) applied unchanged.
- Each chapter is the original survey entry named in the unit's Survey_Ref, so it counts as source 2.
- Coder A coded only the new entry. `merge_source.py` appended those features after the Kallai sheets (`s2k_`): first Gophna & Porat (`s2gp_`), then Bar-Adon (`s2ba_`).
- `match.py` and `protocol_constants.json` were not changed.
- **Held-area rule (owner, 25 Oct).** The boundary is H1 (E ≥ 189.0, N 130.5–152.0, plus the strip E 187–189, N 140–152) and H2 (E 178–189, N 136–141.5), with a 0.5 km buffer.
  - In the nine held units, only measured content was coded, and no cave sentence was coded.
  - Every held unit is flagged EXPOSED.

## Result

**Headline: no change.**
- Main set, R1 Hel/Rom, branch A survey level: **k = 0, f = 20, m = 313 of N = 333**, the same as Addenda 4 and vol1.
- Every row of the headline is identical to the Kallai baseline. So are the without-Nigro table, the excavated split, the exposed-candidate table, the two-of-three list and coder agreement.
- Rarity stays **not measurable from available evidence** (pre-registration §6), because m ≫ k. Nothing here identifies a site.

**One sensitivity variant changes:** branch B with C1 ≤ 2 km gains one unit in all four sets. The unit is Tell Mugheifir (S2629, main set, R2).

| Variant | Before (k / f / m) | After (k / f / m) |
|---|---|---|
| R1 main, B, C1 ≤ 2 km | 11 / 19 / 303 | **12** / 19 / 302 |
| R1 pre-70, B, C1 ≤ 2 km | 15 / 31 / 453 | **16** / 31 / 452 |
| R2 main, B, C1 ≤ 2 km | 8 / 0 / 93 | **9** / 0 / 92 |
| R2 pre-70, B, C1 ≤ 2 km | 12 / 0 / 126 | **13** / 0 / 125 |

**Why S2629 changes.**
- Bar-Adon site 70 describes a cistern, a channel and a pool about 2.5 m deep in the courtyard of a palace of about 60 × 40 m. Its plan is on p. 116, with a 10 m scale and north up.
- On the plan, the cistern is a circle drawn with a small square mouth. I measured it about 9 m from the building's centre, at 340°. That makes C2 MATCH.
- C1 ≤ 2 km was already MATCH, from Birket Jiljulieh (SWP, Mem III p. 24, at row S2531).
- The unit is in held area H1, so the plan is the measured content that the owner's rule allows. The unit is EXPOSED.
- This variant match depends entirely on one coder's reading of an unlabelled plan symbol. If the cistern is given no position, or if the circle and the rectangle are swapped, nothing changes (see ambiguity A1).

**Other condition changes (coder A, every variant; no unit verdict or count changes).**
- **S3881** (Bar-Adon 92a): C2 UNKNOWN → MATCH. The entry has a water cistern north of the Israelite fortress. C1 and C3s stay UNKNOWN.
- **S4167** (Bar-Adon 104, Mughair el-Makari): C1 UNKNOWN → MATCH. The entry has a pool east of the fortress, 25 m across and 2 m deep. C2 and C3s stay UNKNOWN.
- **S2629**: C2 UNKNOWN → MATCH in the primary rules too. C1 is UNKNOWN there, so no branch changes.
- All three drop out under "dated only", because their features are dated U.

## Counts (`match.py`, primary rules, with Nigro)

| Set | Branch | N | k | f | m | m full-coverage | m no adequate coverage | m stopped at Stage 1 |
|---|---|---|---|---|---|---|---|---|
| R1 Hel/Rom (main) | **A survey (headline)** | 333 | **0** | **20** | **313** | 248 | 65 | 143 |
| R1 Hel/Rom | A text | 333 | 0 | 19 | 314 | 249 | 65 | 143 |
| R1 Hel/Rom | B | 333 | 5 | 19 | 309 | 245 | 64 | 143 |
| R1 pre-70 | A survey | 499 | 0 | 32 | 467 | 380 | 87 | 255 |
| R1 pre-70 | A text | 499 | 0 | 31 | 468 | 381 | 87 | 255 |
| R1 pre-70 | B | 499 | 6 | 31 | 462 | 377 | 85 | 255 |
| R2 Hel/Rom | A survey | 101 | 0 | 0 | 101 | 59 | 42 | 24 |
| R2 Hel/Rom | A text | 101 | 0 | 0 | 101 | 59 | 42 | 24 |
| R2 Hel/Rom | B | 101 | 3 | 0 | 98 | 56 | 42 | 24 |
| R2 pre-70 | A survey | 138 | 0 | 0 | 138 | 84 | 54 | 39 |
| R2 pre-70 | A text | 138 | 0 | 0 | 138 | 84 | 54 | 39 |
| R2 pre-70 | B | 138 | 4 | 0 | 134 | 81 | 53 | 39 |

All twelve rows are identical to the Kallai baseline. The full summary is `summary.json`.

### Two-of-three units (branch A survey; list unchanged)

| Unit | Entry | Merged C1 / C2 / C3s | What the new entry adds |
|---|---|---|---|
| S845 Kh. es-Saleh | G&P 170 | U / M / M | Nothing: foundations on three hillocks. C1 stays UNKNOWN. |
| S1137 Qarawet et-Tahta | G&P 190 | U / M / M | Nothing: the ruin at the foot of T. eṣ-Ṣimadi, with columns. C1 stays UNKNOWN. |
| S6040 Tell esh-Sheikh Dhiab | Bar-Adon 13 | M / M / U | A new Arab cemetery by the tell, which is S1537, 1 km south. It is dated L and lies south, so C3s stays UNKNOWN. |
| S1283 Qarn Sarṭaba | Bar-Adon 5 | M / M / U | Two pools to the NW (a quadrant edge, so UNKNOWN) and eight rock-cut caves, some of them plastered reservoirs, with no position. No grave, so C3s stays UNKNOWN. |
| S2430 Tell es-Samrat (held) | Bar-Adon 61 | U / M / M | Measured content: mudbrick walls 6–7 m high. No pool, so C1 stays UNKNOWN. EXPOSED. |
| S3961 (Bar-Adon 98c) | Bar-Adon 98 | U / M / M | A casemate fortress 40 × 60 m. Sub-sites a–e name no pool, pit or grave. C1 stays UNKNOWN. |

Branch-B matches in the main set are unchanged: S1283 and S6040 are still MATCH, and no new primary-rule match was added.

## Inputs and checks

- **Packet inputs**, each fetched from its public source and checked against its frozen SHA-256:
  - WBADB: emekshaveh.org, `3db734cd…`.
  - SWP II and III: Internet Archive `_djvu.txt`, `e09da5ef…` and `102742aa…`.
  - *Highlands*: the TAU Alma IIIF manifest's PDF, `20740205…`.
  - Nigro 2011: the expedition's public Drive file, `0c7fefdf…`.
- **Packets.** `build_packets.py` (unchanged) rebuilt all 244 base packets. Its manifest is byte-identical to `addendum_s2/vol1/packet_manifest_base.csv`, and so are all 244 packet hashes.
- **vol1 baseline.** The `run_addendum_vol1.sh` chain on those packets reproduced the committed vol1 `summary.json`, `unit_results.csv` and `coder_comparison.csv` byte for byte.
- **Kallai (Addendum 4) re-applied** from the committed unit table:
  - `scripts/kallai_from_table.py` rebuilt the 18 `s2k_` sheets. It takes features, positions and the S827 mouth from the table and report, and sets pools to pool_def yes and dates to U.
  - Merged after vol1, the result is **k = 0, f = 20, m = 313 of N = 333**, and `summary.json` and `unit_results.csv` are byte-identical to vol1.
  - All three result files are also byte-identical to the 29 October session's Kallai output, which was still in the scratch area. That is the reproduction check.
  - `coder_comparison.csv` differs from vol1 only in S2411's feature list (`s2k_k1`), as expected.
- **Photos.**
  - 25 HEIC spreads were downloaded from Drive folder `19KrO7YInKR35KZ17F34jWOnSME-lcyv_` through `00_manifest.csv` (sha256 `9e852625…`).
  - All 25 match their manifest `source_sha256` (log: `work/photo_checks.csv`).
  - I coded from crops of JPEG conversions (5712 × 4284). No OCR was used.
  - Spreads: Gophna & Porat pp. 208–229 (IMG_1676–1666) and Bar-Adon pp. 102–129 (IMG_1730–1717).
- **Run.** The chain was: first run → source-4 addendum → Zertal Vols. 2–4 → Zertal Vol. I → Kallai `s2k_` → G&P `s2gp_` → Bar-Adon `s2ba_` → `match.py run` (`scripts/run_chain.sh`).
  - `merge_source.py` merged 25 G&P and 31 Bar-Adon sheets, with 0 invalid.
  - `match.py validate` passed: 244 coder-A sheets with 0 errors, and 63 coder-B sheets with 0 errors.
- **Repo.** Read only. `git status` is clean at `4f03cbb`. Python ran with `-I -B`, so no bytecode was written into the repo.

## Unit selection (written and hashed before any entry was opened)

**Rule.**
- Unit set: the 244 unit_ids in `stage2/packet_manifest.csv`.
- Survey_Ref: the unit's own WBADB row, as carried in its base packet.
- Selected if the Survey_Ref matches `/Gophna\s*(and|&)\s*Porat?h?\s*,?\s*1972/i` or `/Bar[- ]?Adon\s*,?\s*1972/i`.
- All spellings in the 244 refs were listed first. Only "Gophna and Porat 1972, Site N" and "Bar-Adon 1972, Site N[letter]" occur.
- The Yanun units S1001 and S1053 are not Stage 2 units, so nothing about them was printed.

**Record.**
- The list is in `selection_2026-10-30.md` (sha256 `516c4a85…`), written at 14:54 UTC before the Drive manifest was downloaded.
- The machine list is `work/selected_units.csv` (sha256 `0c74b315…`).

**Selected: 56 units.**
- **Gophna & Porat, 25 units:**
  - main set: S103, S153, S178, S219, S223, S278, S331, S398, S440, S444, S563, S592, S676, S709, S743, S790, S836, S845, S848, S874, S1116, S1137;
  - pre-70 set only: S112, S137, S152.
- **Bar-Adon, 31 units:**
  - main set: S1080, S1283, S1253, S1441, S1481, S1486, S1509, S1537, S6040, S1579, S1593, S1739, S1785, S1798, S1808, S1876, S2430, S2530, S2605, S2629, S3875, S3881, S3896, S3897, S3961, S4115, S4167, S4183;
  - pre-70 set only: S1072, S1765, S3883.
- **Held: 9 units**, all Bar-Adon: S1739, S1785 (strip), S1765, S1798, S1808, S2430, S2530, S2605, S2629. The nearest unheld unit is 2.85 km from an edge.

## Per-unit coding

Columns:
- **Entry-only** = conditions computed from the new entry's features alone.
- **Merged** = the registered value after the merge.
- C1 / C2 / C3s / C3t: M = MATCH, U = UNKNOWN, F = FAIL.
- Pages are printed pages. In each spread photo the even page is on the right.
- All new feature dates are U, except the S1537 and S6040 cemetery, which is dated L.

| Unit | Entry | Page | Photo | Features coded (position) | Entry-only | Merged → A_s / A_t / B | Exposed |
|---|---|---|---|---|---|---|---|
| S103 Kh. Balʿame | GP 18 | 210 | IMG_1675 | blocked tunnel opening at the tell's foot (E) | UUUU | UUMU → U/U/U | no |
| S112 Kh. en-Najjar | GP 19 | 210 | IMG_1675 | none | UUUU | UUUU → U | no |
| S137 Kh. Sabʿein | GP 24 | 210 | IMG_1675 | none | UUUU | UUUU → U | no |
| S152 Kh. Zaʿtara | GP 29 | 211 | IMG_1675 | none (fort 35 × 30 m) | UUUU | UUUU → U | no |
| S153 Kh. Umm el-Buṭm | GP **28** (WBADB 72) | 211 | IMG_1675 | none | UUUU | UUUU → U | no |
| S178 Kh. Tannin | GP 34 | 211 | IMG_1675 | none | UUUU | UUUU → U | no |
| S219 Tilfit | GP 38 | 212 | IMG_1674 | none | UUUU | UMUU → U | no |
| S223 Kh. esh-Sheikh Safiryyan | GP 37 | 212 | IMG_1674 | sheikh's tomb (none); cemetery beside it (none); rock-cut tombs with sarcophagi (SE, cavity true) | UUUU | UMUU → U | no |
| S278 es-Sahl A | GP 49 | 213 | IMG_1674 | none | UUUU | UUUU → U | no |
| S331 Kh. Ibziq | GP 51 | 213 | IMG_1674 | cistern in the courtyard house (none); rock-cut storage cave (none) | UUUU | UMUU → U | no |
| S398 Tayasir | GP 69 | 216 | IMG_1672 | built mausoleum el-Qasr (W, cavity false) | UUUU | UUUU → U | no |
| S440 Kh. el-Maliḥ A | GP 84 | 217 | IMG_1672 | none (hot springs not a pool) | UUUU | UUUU → U | no |
| S444 Kh. el-Maliḥ B | GP 85 | 217 | IMG_1672 | none | UUUU | UUUU → U | no |
| S563 Yaṣid | GP 105 | 220 | IMG_1670 | none | UUUU | UUUU → U | no |
| S592 Kh. Burj el-Fariʿa | GP 115 | 221 | IMG_1670 | none | UUUU | MUUU → U | no |
| S676 Kh. ʿAṭuf | GP 135 | 223 | IMG_1669 | caves used as storerooms (none) | UUUU | UUFU → F/U/U | no |
| S709 Kh. eṣ-Ṣunʿa | GP 146 | 224 | IMG_1668 | storage cave under the building (none) | UUUU | UUUU → U | no |
| S743 Kh. Mufiyye | GP 153 | 225 | IMG_1668 | cistern in a Byzantine house's courtyard (none) | UUUU | UUUU → U | no |
| S790 Bab en-Naqb | GP 159 | 225 | IMG_1668 | none | UUUU | UFMU → F/F/F | no |
| S836 Kh. el-Ghirur | GP 169 | 227 | IMG_1667 | none | UUUU | UUUU → U | no |
| S845 Kh. es-Saleh | GP 170 | 227 | IMG_1667 | none | UUUU | UMMU → U | no |
| S848 Kh. Maraḥ el-ʿInab | GP 174 | 227 | IMG_1667 | built plastered water pool (NW, pool_def yes) | UUUU | UUMU → U | no |
| S874 Kh. Baṣaliyye | GP 176 | 227 | IMG_1667 | none | UUUU | UUUU → U | no |
| S1116 Tell eṣ-Ṣimadi | GP 190 | 229 | IMG_1666 | none | UUUU | UUMU → U | no |
| S1137 Qarawet et-Tahta | GP 190 | 229 | IMG_1666 | none | UUUU | UMMU → U | no |
| S1072 Farʿa el-Juftlik | BA 2 | 102 | IMG_1730 | many cave openings in the cliff (none) | UUUU | UUUU → U | no |
| S1080 Tell el-Mazar | BA 3 | 102 | IMG_1730 | none (built and rock-cut water channel not coded) | UUUU | UFUU → F/F/F | no |
| S1283 Qarn Sarṭaba | BA 5 | 103–104 | IMG_1730, 1729 | two water pools (NW); eight rock-cut caves, some plastered reservoirs (none) | UUUU | MMUU → U/U/**M** | no |
| S1253 ed-Dirs | BA 6 | 104 | IMG_1729 | none | UUUU | UUUU → U | no |
| S1441 el-Marmale | BA 9 | 104 | IMG_1729 | round pool, 52 m across (none); elliptical pool 28 × 13 m (none) | UUUU | UUUU → U | no |
| S1486 Rujm Abu Muḥeir | BA 10a | 104 | IMG_1729 | pool 8 m across at sub-site 10b (grid S1472, 288°) | UUUU | UUUU → U | no |
| S1481 (10c) | BA 10c | 104 | IMG_1729 | the same pool (grid S1472, 288°) | UUUU | UUUU → U | no |
| S1509 (10g) | BA 10g | 104 | IMG_1729 | the same pool (grid S1472, 292°) | UUUU | MUUU → U | no |
| S1537 Tell esh-Sheikh Dhiab | BA 13 | 105 | IMG_1729 | new Arab cemetery (none, L) | UUUU | UUUU → U | no |
| S6040 Tell esh-Sheikh Dhiab | BA 13 | 105 | IMG_1729 | the same cemetery (grid S1537, 186°, L) | UUUU | MMUU → U/U/**M** | no |
| S1579 Kh. Faṣayil | BA 15 | 107 | IMG_1728 | pool 60 × 50 m (N, yes); plastered enclosure, perhaps a reservoir, 75 × 65 m (S, 250 m, unclear) | UUUU | UUUU → U | no |
| S1593 Kh. ed-Dashe | BA 17 | 107 | IMG_1728 | robbed water pool (none) | UUUU | UUUU → U | no |
| S1739 Kh. el-Beyadat | BA 22 | 109 | IMG_1727 | none (measured: ruin 600 × 250 m) | UUUU | UUUU → U | **yes** |
| S1785 Kh. el-ʿAwja | BA 26 | 108 | IMG_1727 | none (unmeasured cemetery withheld) | UUUU | UMUU → U | **yes** |
| S1765 Kh. el-ʿAwja et-Taḥta | BA 27 | 108 | IMG_1727 | none | UUUU | UUUU → U | **yes** |
| S1798 Kh. Umm ʿAzbe | BA 32 | 110 | IMG_1726 | none (cave sentence withheld) | UUUU | MUUU → U | **yes** |
| S1808 Malkhaka el-Wadin | BA 34 | 110 | IMG_1726 | vaulted plastered cistern, 3.80 m across (none); built pool 1.5 × 2 m (none, pool_def no) | UUUU | UUMU → U | **yes** |
| S1876 Kh. Abu Rashid | BA 39 | 110–111 | IMG_1726 | none (plan shows walls only) | UUUU | UUUU → U | no |
| S2430 Tell es-Samrat | BA 61 | 114 | IMG_1724 | none | UUUU | UMMU → U | **yes** |
| S2530 (68c) | BA 68c | 115 | IMG_1724 | none (unmeasured pool of 68b withheld) | UUUU | UUUU → U | **yes** |
| S2605 Kh. Mugheifir | BA 69 | 115 | IMG_1724 | none | UUUU | UUUU → U | **yes** |
| S2629 Tell Mugheifir | BA 70 | 115–116 | IMG_1724, 1723 | cistern (plan 340°, 9 m); pool about 2.5 m deep (plan 292°, 13 m, yes) | U**M**UU | U**M**UU → U (B **M** at C1 ≤ 2 km) | **yes** |
| S3883 Kh. Karm Abu Ṭabaq | BA 91 | 120 | IMG_1721 | none | UUUU | UUUU → U | no |
| S3881 (92a) | BA 92a | 120 | IMG_1721 | cistern north of the fortress (N); Bedouin cemetery at 92b (grid S3875, 293°) | U**M**UU | U**M**UU → U | no |
| S3875 (92b) | BA 92b | 120 | IMG_1721 | cistern at S3881 (113°); Bedouin cemetery (none) | UUUU | UUUU → U | no |
| S3896 (92d) | BA 92d | 120 | IMG_1721 | cistern at S3881 (296°); cemetery at S3875 (296°) | UUUU | UUUU → U | no |
| S3897 (92e) | BA 92e | 120 | IMG_1721 | cistern at S3881 (319°, bearing invalid); cemetery at S3875 (bearing invalid) | UUUU | UUUU → U | no |
| S3961 (98c) | BA 98c | 122–123 | IMG_1720 | none | UUUU | UMMU → U | no |
| S4115 Karm es-Samra | BA 102 | 123 | IMG_1720 | none (dams not coded) | UUUU | UUUU → U | no |
| S4167 Kh. el-Makari | BA 104 | 123 | IMG_1720 | pool with an earth bank, 25 m across, 2 m deep (E, yes) | **M**UUU | **M**UUU → U | no |
| S4183 Naḥal Qidron | BA 107 | 124 | IMG_1719 | none | UUUU | UUUU → U | no |

- Paraphrased evidence for each unit is in `units_2026-10-30.csv`, column `evidence_paraphrase`. That file keeps the Kallai table's column names: the `kallai_*` columns hold the G&P or Bar-Adon entry values, and a trailing `source` column says which.
- The sheets are in `coded_A/gp/` and `coded_A/ba/`, with quotes as short Hebrew strings of 12 words or fewer.

**Name and grid check.** Every entry was found by its site number and checked by name and printed grid. All 56 match, except two:
- **S153** (Umm el-Buṭm). WBADB gives "Site 72". G&P site 72 is Kh. el-Masqufe at 1556 1935, about 25 km away. G&P site 28, Kh. Umm el-Buṭm at 1786 2035, matches the unit's name and grid, so that is the entry coded.
- Neither entry names a pool, pit or grave, so the choice changes nothing (deviation D1).
- **S6040** (Tell esh-Sheikh Dhiab). Bar-Adon site 13 is printed at 1908 1615, which is S1537's point, 1 km south of S6040. The name matches, so the entry was coded for both units (A7).
- S1137 shares G&P site 190 with S1116; it lies 400 m south of the printed grid, in the ruin "at the foot, mainly south".

## Coder B

**Random-sample units.**
- 14 of the 56 units already have coder-B sheets: S103, S112, S137, S178, S563, S592, S676, S790, S836 (G&P); S1283, S1509, S1808, S2605, S6040 (Bar-Adon).
- The procedure ("Coder B, random sample") requires a blind coder B to code the new entries for these units. **That was not done.** This agent is coder A and cannot be blind.
- For all 14, the entry-only coding gives UNKNOWN on every condition, and coder A's values did not change in any variant.
- So a coder-B sheet with the same content could not change a merged value. One with *different* content could: for example, a coder-B position for a feature I left without one.

**New coder-A match: full coder-B coding required.**
- **S2629** Tell Mugheifir has become a coder-A match in branch B under the C1 ≤ 2 km variant (with and without Nigro), and coder B has never coded it.
- The procedure therefore requires a **full blind coder-B coding of S2629**.
- **A coder-B result can change the merged value.** S2629 now has only a coder-A sheet. Under the merge rule, if coder B does not also give C2 MATCH, merged C2 becomes UNKNOWN. That would undo the only count change in this addendum: R1 main B at C1 ≤ 2 km would go 12 → 11, with the matching changes in the other three sets.
- The same holds for C1 under the 2 km variant.
- Coder B should get the base packet plus the Bar-Adon site 70 entry and its p. 116 plan. The entry is held-area material, so coder B's reading is also EXPOSED.

**No other unit triggers coder B.**
- S3881 and S4167 gained one condition each but are not a match in any branch, variant or Nigro setting.
- No other unit changed.

## Coder B, S2629 (added 30 Oct, after the run above)

**Input.**
- The coordinator supplied a full blind coder-B sheet for S2629: `coded_B_full/S2629.json`, copied from `scratchpad/coderB_S2629/B/S2629.json` (sha256 `3a74660d…`).
- It codes the whole base packet plus Bar-Adon site 70, with held-area material limited to measured content. It is marked EXPOSED.

**How it was merged.**
- It was added the way `run_addendum.sh` adds `coded_B_full` sheets: copied into the merged coder-B folder.
- S2629 had no coder-B sheet before, so nothing was replaced.
- `match.py run` was then rerun on the Addendum 5 coder-A sheets (`work/tmp_gpba/A6`, unchanged), using that coder-B folder (`work/B4`). The output is in `work/out_gpba_B/`.
- `match.py validate` passed: 244 coder-A sheets and 64 coder-B sheets, all with 0 errors.
- `match.py` and `protocol_constants.json` are unchanged.

**S2629, merged C1 / C2 / C3s / C3t.** Coder A, coder B and the merged value are identical in every variant, with and without Nigro. Merging therefore makes no value UNKNOWN.

| Variant (with and without Nigro) | C1 | C2 | C3s | C3t | A survey / A text / B |
|---|---|---|---|---|---|
| primary | UNKNOWN | MATCH | UNKNOWN | UNKNOWN | U / U / U |
| C1 ≤ 0.5 km | UNKNOWN | MATCH | UNKNOWN | UNKNOWN | U / U / U |
| C1 ≤ 2 km | MATCH | MATCH | UNKNOWN | UNKNOWN | U / U / **MATCH** |
| C2 tomb shafts | UNKNOWN | MATCH | UNKNOWN | UNKNOWN | U / U / U |
| dated only | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | U / U / U |

**The branch-B C1 ≤ 2 km change survives.** The counts are R1 main 11 → 12, R1 pre-70 15 → 16, R2 main 8 → 9 and R2 pre-70 12 → 13, the same as with coder A alone.

**The headline is unchanged.** All 12 rows are identical to the Counts table above and to the Kallai baseline (main set R1 A survey: k 0, f 20, m 313 of 333).
- `unit_results.csv` is byte-identical to the coder-A-only run.
- The only `summary.json` section that changes is `coder_agreement`, and the two-of-three list is unchanged.

**Coder agreement after adding S2629** (now 64 double-coded units; S2629 agrees on all four conditions):

| Condition | Before (63 units): agreement, κ | After (64 units): agreement, κ |
|---|---|---|
| C1 | 1.000, 1.000 | 1.000, 1.000 (MATCH/MATCH 11, U/U 53) |
| C2 | 0.937, 0.890 | 0.938, 0.892 (S2629 is a new MATCH/MATCH) |
| C3s | 0.952, 0.861 | 0.953, 0.862 |
| C3t | 1.000, n/a | 1.000, n/a |

**Disagreements.** There are none at condition level, so the merge rule (PROTOCOL §1: keep the value where the coders agree, UNKNOWN where they differ) leaves every value as coded. The coders differ only at feature level, and none of the differences changes a condition:
- **Plan readings.** Both coders read the circle on the p. 116 plan as the cistern and the rectangle as the pool.
  - Coder B measures the cistern at 352°, 9 m and the pool at 295°, 12 m. Coder B measured from the centroid of the building outline and corrected the north arrow by +2°; from the bounding-box centre B gets 345° and 294°.
  - Coder A measured 340°, 9 m and 292°, 13 m.
  - Both readings of the cistern fall in the 315°–45° sector, so C2 is MATCH for both.
  - Coder B rates the identification at about 75%. Ambiguity A1 still applies: if the two plan symbols were swapped, both coders' C2 would fall.
- **C1 at 2 km.**
  - Coder B's C1 at 2 km rests on Birket Jiljulieh, coded twice: the WBADB name of S2531 and SWP Mem III p. 24, both at grid S2531.
  - Coder A's rests on the SWP pool at S2531 alone.
- **Other features.** Coder B also codes WBADB components (S2629, its duplicate row E376, S2601) and Nigro catalogue entries 66, 74, 78, 79 and 84.
  - All are dated L, have no position, or lie outside the sectors.
  - None gives a C1 MATCH in the primary rules or a C3s MATCH.
- **Exposure.** Coder B's note says Nigro cat. 79 cites Bar-Adon pp. 115–116, so it may describe the same site.

**What remains.** No other unit needs coder B under the procedure. The 14 random-sample units listed under Coder B above still have no coder-B coding of the new entries (D2). `units_2026-10-30.csv` needed no change, because no value changed. `summary.json` has been refreshed from `work/out_gpba_B/` (sha256 `34e75de5…`).

## Ambiguities (recorded, not resolved by results)

Each was settled by the protocol text and earlier coders' practice before the run. The sensitivity results were computed after the run and are exploratory (`scripts/sens.py`).

1. **A1. S2629 plan (decisive for the variant change).**
   - The plan shows a circle with a small square inside, linked by a double line to a rectangle that is shaded along two sides. The text names a cistern, a channel and a 2.5 m-deep pool.
   - I read the circle as the cistern (the small square is the mouth) and the rectangle as the pool.
   - I measured from the centre of the building's bounding box. Measuring from the centre of the courtyard instead still puts the cistern in the north sector.
   - **Sensitivity:**
     - Circle and rectangle swapped: no change from the baseline anywhere.
     - No plan positions (both features `none`): no change anywhere.
   - Using a plan in a held unit follows the owner's measured-content rule, and the unit is EXPOSED.
2. **A2. S2629, cistern without its own measurement.**
   - The text sentence about the cistern carries no measurement. Only the scaled plan does.
   - If the owner's rule is read as requiring a measurement *of the feature in the text*, the cistern would drop out, and with it the variant change (as in A1, "no plan positions").
3. **A3. Held units: unmeasured sentences withheld.**
   - The sentences withheld are: the S1798 caves on the ruin's east side (cave sentence); the S1785 new cemetery; the 68b plastered pool, which belongs to a sub-site of S2530; and the general "cisterns and pools" sentence of S1808.
   - If they had been coded, none could have satisfied a condition. The caves lie east, the cemetery is L, the 68b pool lies about 150 m W of S2530, and the S1808 items have no position.
4. **A4. S1080, water channel.**
   - Tell el-Mazar has a built and rock-cut water channel. It is a channel, not a cavity with an opening, so it was not coded, as at Bar-Adon 13 and 17.
   - If it were coded as a tunnel (a pit) with no position, S1080 C2 would go FAIL → UNKNOWN. The FAIL rests on Zertal's "Cisterns: none".
   - The main-set headline would then be **k 0, f 19, m 314**, with f falling by 1 in every R1 branch.
5. **A5. Dams and springs.**
   - S4115 has "several dams for collecting water" near the fortress, and S440 has hot springs and baths. Neither is called a pool, so neither was coded.
   - If they were coded, they would have no position, so nothing would change.
6. **A6. pool_def.**
   - S1808: the "built pool 1.5 × 2 m" is called a pool but is shown to be smaller than 3 m, so I coded it `no`. As `yes` it would still have no position, so nothing changes.
   - S1579: the enclosure "perhaps used as a reservoir" is `unclear` and lies S, so nothing changes.
7. **A7. Shared entries.**
   - Bar-Adon 10, 13 and 92 cover several WBADB units. Each unit got the entry's features. A feature of another sub-site took that sub-site's WBADB row as a `grid` reference (PROTOCOL §4).
   - None falls in a qualifying sector with a valid bearing.
   - S6040: the printed grid of site 13 is S1537's point, 1 km south, so the tell's features are south of S6040.
8. **A8. Dates.**
   - Features were dated U unless the entry dates the feature itself. The S743 cistern lies in a house the entry dates as Byzantine, but the cistern itself is undated, so it is U.
   - The S1537 and S6040 cemetery is called "new", so it is L. The Bedouin cemetery at 92b is undated, so it is U.
9. **A9. S223 rock-cut tombs.** The entry gives "south-east of the ruin" and a grid of 1817 2006. There is no WBADB row there, so they are coded as words SE, a quadrant edge that gives UNKNOWN. From the grid, the bearing is about 117°, so either way they are not north.
10. **A10. Manifest held flag.**
    - `00_manifest.csv` marks every Bar-Adon spread `held=True`, with the note "location-only treatment … no substantive summary or OCR".
    - I applied the task's geographic rule instead: H1 and H2 plus the buffer, per site. Bar-Adon entries for unheld sites were coded in full.

## Deviations

- **D1.** S153 was coded from G&P site 28 (name and grid match), not from the site 72 that WBADB names.
- **D2.** No blind coder B was used for the 14 random-sample units, and the required full coder-B coding of S2629 has not been done (see Coder B).
- **D3.** The Kallai sheets are not committed, so they were rebuilt from the committed unit table.
  - Their quotes are the table's English descriptions, and their dates are U, because the table gives none.
  - The rebuild reproduces Addendum 4's three output files byte for byte.
- **D4.** The chain script is the repo's `run_addendum_vol1.sh` logic with two changes: `-B`, and a temporary folder in the scratch workspace. The merge order, prefixes and `match.py` are unchanged.
- **D5.** Hebrew is read in translation by the coder, and the paraphrases are in English. No OCR was used.
- **D6.** The units CSV keeps the Kallai column names (`kallai_*` = new entry) and adds a `source` column.
- **D7.** Photos were coded directly. Packets carry no G&P or Bar-Adon text, and matching uses only packet geometry, as in D-K3 of the Kallai report.

## Exposure log

**Opened (photos):**
- **Gophna & Porat:**
  - Entries read: sites 18, 19, 24, 28, 29, 34, 37, 38, 49, 51, 69, 72, 84, 85, 105, 115, 135, 146, 153, 159, 169, 170, 174, 176 and 190.
  - Spreads viewed only at overview resolution: pp. 208–217 and 220–229. P. 218–219 (IMG_1671) was downloaded and converted but not viewed.
- **Bar-Adon:**
  - Entries read: sites 2, 3, 4 (pottery list and plans only, while locating site 5), 5, 6, 9, 10, 13, 15, 17, 22, 26, 27, 32, 34, 39, 61, 68 (sub-sites b–e), 69, 70, 91, 92, 98, 102, 104 and 107.
  - Overviews of pp. 102–125 were viewed. Pp. 126–129 (IMG_1718 and 1717) were downloaded and converted but not viewed.
  - Not opened: pp. 92–101 (introduction) and 130–149.
- **Held material seen:**
  - The full entries of the nine held units, including the unmeasured sentences listed in A3, which were read to judge whether they carry measurements.
  - Other held-area entries on the same spreads were visible at overview resolution and were not read. That includes the overview of p. 114, which shows entries near Tell es-Sultan. The S2430 entry itself places that tell south of Tell es-Sultan.
- **Qumran area:** the Bar-Adon site 98 entry (Feshkha area, for S3961) was read. Site 94 (Nukb Kumran, p. 121) and the other Qumran-area entries were visible in overview and not read.

**Repo and project:**
- `research/preregistration/` was never opened.
- One grep listed lines of `research/ACTIVE_TEST.md`, including the SULTAN-1 paragraph and the filename `C_kenyon_jericho_II_and_kh_yanun.md`. It was a search for the source URLs of *Highlands* and Nigro.
- `sources/full_reads_2026-10-12/highlands1997/source_manifest.json` was read for the TAU URL. Its exposure list names "Kh. Yanun scoped entries".
- Neither of those touches XII 10 or the Janoaḥ test, and nothing from them was used.
- `research/sources/books_usc_2026-10-30/README.md` was read for its table of files. It gives one-line summaries of the 30 Oct notes, including "Sheikh Dhiab link stays open" for `held_asi1_deirhajleh`. No 30 Oct sweep note was opened apart from the Kallai report and unit table.
- `research/assessments/kohlit_chain/` was not opened.
- The owner's 25 Oct decision file was located by name but not opened: the task's statement of the rule was used.

**Scratch area:**
- Folder names in the session scratchpad were listed, which shows that a `janoah` folder exists. It was not opened.
- In the 29 Oct Kallai folder (`scratchpad/kochavi/`), only `work/res_kallai/*` was used, and only through byte comparison (`cmp`). `ocr_benjamin.txt` and the images were not opened.

**Never opened:** Copper Scroll images; columns XI–XII; the XII 10 commentary; anything on Yanun or Janoaḥ.

**Writes:** nothing was written to the repo, Drive or any project. Photos, conversions and crops stay in `stage2_gp_ba/photos/` and `work/`.

## Files (all in the session scratch folder `stage2_gp_ba/`)

- `stage2_gp_ba_2026-10-30.md`: this report.
- `units_2026-10-30.csv`: one row per unit (56).
- `summary.json`: the `match.py` summary after the merge, refreshed with coder B for S2629 (sha256 `34e75de5…`). The coder-A-only version was `57256d82…` and is kept at `work/out_gpba/summary.json`.
- `coded_B_full/S2629.json`: coder B's full sheet for S2629, as supplied.
- `coded_A/gp/*.json` (25) and `coded_A/ba/*.json` (31): coder-A sheets (PROTOCOL §10 format, before the merge adds `sources`).
- `selection_2026-10-30.md` and `work/selected_units.csv`: the selection made before opening any entry.
- `scripts/`:
  - `select_units.py`, `kallai_from_table.py`, `run_chain.sh`, `build_sheets.py`, `evaluate.py`, `units_table.py`, `sens.py`;
  - helpers `intake.py`, `crop.py`, `cov.sh`, `gridcrop.py`.
- `work/`: the packets (`base/`), the Kallai sheets (`kallai_A/`), the runs (`out_vol1/`, `out_kallai/`, `out_gpba/`, `out_ba_*` sensitivity runs), `eval.json` and `photo_checks.csv`. Packets and photos are copyright material and stay in scratch.
