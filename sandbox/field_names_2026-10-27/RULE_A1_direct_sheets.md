# Run 19, addendum A1: direct reading of the owner's 1:20,000 sheets

Fixed 28 Oct 2026 before any sheet was transcribed. Exploratory. This follows the coverage gap in [RESULT.md](RESULT.md): the open digitisation is almost empty on the core desert sheets.

## Data
- **S4:** every name printed on the owner's Drive scans of sheets **18-12 Deir Mar Saba (1943)**, **18-13 Wadi el-Qilt (1941, overprint 1942)** and **19-14 Jericho (provisional topo-cadastral, 1928)**. Sheets 19-12 and 18-14 are online-only on the owner's Mac and are not in this addendum; they will be added under the same rule if they arrive (A1b).
- Transcription is done by fresh subagents who are **not told** what the names are for, and are not given the scroll's names. Each transcribes the printed text exactly (with macrons and ʿ), with tile and pixel position and a feature class.
- Positions: sheet pixels to Palestine Grid by a similarity fit to the repo's own located items on the same sheet (research/regional/mandate_maps/names.csv), matched by printed name; then to WGS84 with mm_lib.to_wgs. Positions are used for reporting only.
- S4 is built, counted and hashed (gazetteer_manifest.json) before any match is run. Latin script, **branch** mode (as S2).

## Matching, controls and decision
Unchanged from [RULE.md](RULE.md): same scripts (scripts/match.py), same skeleton rules, same C1 (100 shuffles, seed 20261027) and C2 (40 Joshua names). Run on S4 alone and on S1+S4.

A **new lead** is, as before, a match for an unplaced name or landmark word with C1 ≤ 0.10, inside the region, reported with sheet, position and the printed spelling. Relations of the entry are reported, not scored.

## Not done
Sheets 19-12 and 19-13 hold Qumran and the northern Dead Sea shore; 19-13 is not in the owner's folder. A negative result on S4 covers the Mar Saba, Wadi Qelt and Jericho sheets only.
