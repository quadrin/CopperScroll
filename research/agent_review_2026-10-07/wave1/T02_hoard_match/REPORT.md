# T02 — Reverse hoard match

Agent report, 6 October 2026, saved by the coordinator. Labels: EVIDENCE / INFERENCE.

## What was done
- Built a database of 76 records; 63 are in period (c. 200 BCE–135 CE) and in or at the edge of the scroll's region, and only those were scored. Out-of-region and out-of-period finds are flagged, not scored.
- Main source: Oxford Coin Hoards of the Roman Empire database (CHRE, chre.ashmus.ox.ac.uk), with primary citations (de Vaux, Meshorer, Kadman, Ariel); also ʿAtiqot 112, DJD I, Encyclopaedia Judaica.
- Scoring rules written before scoring (`scoring_rules.json`); all 3,843 record × entry pairs scored; 2,000-run null that shuffles find locations.

## Findings
1. **No hoard matches any entry; nothing moves an identification.** INFERENCE, high. Best score 9/12: Qumran Cave 1 scroll jars ↔ entry 25 (a jar with one scroll in a cave) — a match of deposit type, not place. No pair met the pre-stated "worth testing" bar. Pairs scoring ≥ 7: 14 observed vs 12 expected by chance (p = 0.40).
2. **Shortlist unchanged.** EVIDENCE. Entry 21: Qumran's L120 silver hoard lay inside the building, "to the right of the door … between the floors of Period Ib and II" (de Vaux 1956: 567, via CHRE), not at the aqueduct head. Entry 31: only small Bar Kokhba coin clusters (Cave of the Sandal). Entry 32: no hoards recorded at Choziba. Entry 49: the "Siloam" pyxis hoard is attributed to Silwan only by a dealer.
3. **The karsh reading fits real hoard sizes; the talent reading does not.** INFERENCE, medium. As talents, every numbered amount exceeds any regional silver hoard (largest about 4–7 kg). As karsh (71 g), 22 of the 30 abbreviated amounts are at or below that size; the Qumran-sector amounts (entries 20, 21, 23, 25, 26) come to 0.5–3 kg, about the size of each L120 pot. Plausibility only; partly Lefkovits's own argument. The fully spelled ככרין amounts stay implausibly large under either reading.
4. **Post-hoc lead, low:** the Ramat Raḥel hoard (15 Tyrian shekels, 204.5 g, closing 11/10 BCE) lay in a niche in the SW corner of a shaft-entered underground dovecote, "0.5 m above the floor and 3.5 m below the shaft" (Farhi et al., INJ 17, 2010, 59–76). Compare entry 44 ("dovecote … its way down from above"), two entries before the atlas's Ramat Raḥel candidate (46). Against: ~3× too little silver, ~75 years too early, such dovecotes are common.
5. **Source discrepancy:** Leonard (1999) gives the ʿIsfiya hoard as 7.8 kg; CHRE's count (3,850 tetradrachms) implies about 56 kg.

## Key in-region records (EVIDENCE)
- H01–H03 Kh. Qumran L120 (1955): 561 silver coins in two pots plus a jug; latest coin 9/8 BCE (CHRE 7692, 18786, 18785; de Vaux RB 63, 1956, 567–568; Ariel 2018 p. 404 reads it as a possible foundation deposit).
- H08 cave near ʿEin Feshkha (1953): ≥ 277 silver coins; closes 117–138 CE (CHRE 7586).
- H09 Qumran Cave 1: jars with covers holding scrolls (DJD I).
- H13 "Jericho 1874": ~100 Jewish War shekels in a pot with a lead seal; findspot unrecorded (CHRE 8082; Kadman 1960 p. 81).
- H15 Cave of the Sandal (Ketef Jericho): 26 Bar Kokhba-period coins (CHRE 8052–8054).
- H20 Murabbaʿat Cave II (2022): 15 Ptolemaic silver tetradrachms in a wooden box in a wall crack, c. 170 BCE (ʿAtiqot 112, 2023).
- H22 Cave of Letters: 19 bronze vessels in a basket, 132–135 CE (Freund's entry-25 proposal scores only 4/12 here).
- H36 Ramat Raḥel (2008): see finding 4 (CHRE 7288).
- H37 "Siloam" pyxis: ≥ 12 shekels, c. 67/68 CE, dealer attribution (CHRE 8000).
- H39 Jewish Quarter (1975): 13 Revolt shekels "in a small pool of a building" (Avigad 1983 pp. 195–196).
- Not found: any in-period hoard at Mount Gerizim or Beth Shean, or any ingot cache.

## Limits
CHRE under-represents Hellenistic/Hasmonean hoards (coinhoards.org blocked by robots); many records lack findspots; depth/side rarely published; entry features are mechanical; a Jericho hoard (H19) rests only on a 1999 mailing-list post.

## Best next step
Read Leonard 2000, "Numismatic Evidence for the Authenticity of the Copper Scroll" (Proceedings of the XII International Numismatic Congress, Berlin 1997, vol. I, pp. 683–692), the only entry-by-entry comparison of regional shekel hoards with the scroll; Leonard says one treasure "corresponds fairly closely with a known coin hoard, in size and location".

Files: hoards.json/.csv, entry_features.json/.csv, scoring_rules.json, scores_all.csv, top_pairs.csv, best_per_record.csv, best_per_entry.csv, null_test.json, quantity_overview.csv, chre_*.{csv,json}, scripts/, downloads/.
