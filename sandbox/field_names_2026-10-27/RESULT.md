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
