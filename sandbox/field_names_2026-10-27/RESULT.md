# Run 19 result: lost names as 1940s Arabic field names

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit ebabf7e, SHA-256 `20e0c59c…36ed1`. Gazetteer counts and hashes recorded before each match ([out/gazetteer_manifest.json](out/gazetteer_manifest.json)). Exploratory.

## Verdict
**No new lead.** No source or deviation gives a match for an unplaced name or landmark word with C1 ≤ 0.10. The matcher recovers known survivals (Koziba, Naṭof, Bezek, Kidron, Jericho, Sekakah ~ Iskaka). The scroll names match no more often than ordinary biblical names.

| Source | Scroll names matched / C1 expected | C2 (Joshua) | Unplaced matched / expected | Leads |
|---|---|---|---|---|
| S1 Palestine Open Maps layers (3,143 names; primary) | 36 / 28.4 (P = 0.0005) | 31 / 40 (Fisher p = 0.22) | 21 of 24 / 18.0 (P = 0.054) | 0 |
| S3 NGA GNS (13,064 names; deviation) | 36 / 30.3 (P = 0.002) | 32 / 40 (p = 0.35) | 21 of 24 / 19.6 (P = 0.24) | 0 |
| S2 repo's own map readings (exposed; deviation) | 17 / 12.4 | 9 | 10 of 24 / 8.75 | 0 |

**The excess over C1 is not a scroll signal:** the Joshua control names beat their own shuffles by just as much (31 of 40 vs 20.0 expected). C2 is the decisive control, and the scroll does not beat it.

## Coverage gap
The open POM digitisation is nearly empty on the core desert sheets: 0 names on 19-12 (Ras Fashkha), 4 on 19-13, 2 on 18-13, 8 on 19-14. Most names lie on the western and northern hill sheets. For the core area this test is close to untested; the real test is reading sheets 18-12, 18-13, 19-12 and 19-13 directly (the owner's Drive copies, via the Mac).

## Notes
- Koḥlit matches only far-off names (Beit Kahil NW of Hebron; ʿEin Kahla; Kahllat Inshit), C1 0.81–0.94; W. Kuheila (repo's own reading, already flagged) has C1 0.34.
- Kippa matches Kafa (sheet 15-18) and El Kaffa (18-19, 32.315 N 35.359 E), C1 0.43.
- The method structurally misses Janoaḥ/Yanun (ḥ lost) and Doq/Duyūk (ك vs the rule's ق).
- Gazetteers are not committed (POM data is ODbL; kept in the scratch folder). Per-unit results: [out/per_unit_all_sources.csv](out/per_unit_all_sources.csv); stats per source: out/*_stats.json; [scripts/](scripts/).
- Not used (robots.txt): GeoNames dump; POM data API and Dropbox sheet downloads.

## Addendum A1, 28 Oct 2026: direct reading of three sheets
Rule: [RULE_A1_direct_sheets.md](RULE_A1_direct_sheets.md), commit 4daab8e, SHA-256 `df48970b…921a`. S4 hashed in [out/gazetteer_manifest.json](out/gazetteer_manifest.json) (commit 264a913) before matching.

**Data.** The owner's Drive scans of sheets 18-12 Deir Mar Saba (1943), 18-13 Wadi el-Qilt (1941/42) and 19-14 Jericho (provisional, 1928), copied through the owner's Mac. Six fresh subagents, not told the purpose, transcribed every printed name from 126 overlapping tiles: 845 raw lines, **478 names after de-duplication** (18-12: 223; 18-13: 168; 19-14: 87). The repo's earlier window readings (S2) had 31, 13 and 74 names on these sheets. Positions come from the neat lines. Proper names that the repo had already located agree to a median of 50–62 m on 18-12 and 18-13, and to 38–150 m on 19-14. The 1928 Jericho sheet spans E 190–202.5 km, not 10 km.

**Verdict: no new lead.** No unplaced name or landmark word matches with C1 ≤ 0.10.

| Gazetteer | Scroll names matched / C1 expected | C2 (Joshua) | Unplaced matched / expected | Placed matched / expected | Leads |
|---|---|---|---|---|---|
| S4 (478) | 20 / 15.3 (P = 0.018) | 5 / 40 (Fisher p = 0.0006) | 11 of 24 / 10.5 (P = 0.48) | 9 of 16 / 4.8 (P = 0.002) | 0 |
| S4 without partial fragments (333; deviation) | 19 / 13.2 (P = 0.004) | 3 / 40 (p = 0.0001) | 10 of 24 / 8.6 (P = 0.26) | 9 of 16 / 4.7 (P = 0.001) | 0 |
| S1 + S4 (3,621) | 36 / 28.8 (P = 0.0007) | 32 / 40 (p = 0.35) | 21 of 24 / 18.1 (P = 0.06) | 15 of 16 / 10.7 | 0 |

**Why the S4 excess over C2 is not a signal.**
- All of it is in names already placed. Unplaced names match at the chance rate (11 vs 10.5).
- Of the 9 placed matches, only 2 are known survivals: Doq ~ DUYUK (18-13 margin) and Beth Haqqoṣ ~ Tell el Qōs (19-14; Milik's placement). The other 7 are chance consonant matches or common words: Kerem ~ Karm ("vineyard"); Jericho ~ W. Rahwa; Gerizim ~ W. el Jurfān; Beth-shean ~ Beit Sūfyā; Horon ~ Khureiyan; Bezek ~ (Birka); Kidron ~ W. Qumrān, by edit distance.
- **C2 does not suit these sheets.** The Joshua 15 and 18 control names belong to the hill country, and these three sheets are desert and the Jordan valley. On the whole region (S1 + S4), C2 matches as often as the scroll (p = 0.35), as before.

**Notes (not leads).**
- Shlomo ~ Tell es Sultān and Marj es Sultān (edit distance 1, C1 0.20). This is above the 0.10 bar, and Sultān is an Arabic title.
- Melaḥ ~ Tlūl el Mallāḥ, W. el Mallāḥa and Ard el Mallāḥ on 19-14 (C1 0.72). "Salt" names are common.
- Obed ~ ʿAbd Rabbu and ʿAbda on 18-12 (C1 0.42).
- "W. Qumrān" is printed on 18-12 at about grid 188.2/127.9, on the upper course of the wadi, 5 km west of Kh. Qumran.

**Coverage.** 19-12 (Ras Fashkha, with Qumran) and 18-14 are online-only on the owner's Mac. 19-13 is not in the folder. The core shore strip around Qumran is therefore still untested.

Files: [out/A1/](out/A1/) (gaz_S4.csv, matches, per-unit tables, stats), [scripts/A1/](scripts/A1/) (tiling, transcription brief, build). The sheet images and tiles are not committed.
