# Salvage records: ancient recovery accounts and modern searches

**What it is.** A catalogue of 27 ancient and late-antique accounts of hiding or recovering valuables and sacred objects, and a ledger of 27 modern searches that looked for the scroll's deposits or covered places the scroll names.
**Main result.** Every EVIDENCE-grade ancient account that bears on the scenarios describes removal soon after a loss (custodians, captives' information, systematic digging); support for "real but unrecovered" comes only from traditions and claims. No modern search has a documented target volume and depth, so none is a verified negative at a predicted target.
**What stays unknown.** Where Allegro dug in 1959–60, what Bull's Gerizim trench was, and the cave-by-cave coverage of the 1952, 1993 and 2017 surveys; the primary reports are copyrighted or unread.

Exploratory work of 9 October 2026 (analogues round, worker "salvage-records"). The idea comes from the Atocha search: Spanish salvage records showed where people had already looked. No identification, deposit or outcome-ledger count is made here.

## Files

| File | Content |
|---|---|
| [catalogue.csv](catalogue.csv) | 27 accounts: reference, date of composition, place, objects, action, agent, kind (EVIDENCE / TRADITION / CLAIM), what it bears on, scenario coding, a quote of 12 words or fewer, sources. |
| [searches.csv](searches.csv) | 27 searches: who, when, where, method, extent and depth, finds, result, documentation, sources, coverage notes. Join columns: `place_id`, `record`, `looked_at`, `result`, `notes`. |
| [sources.csv](sources.csv) | 44 sources with access status (read, owner's copy, via repo, not accessed, failed). |
| [source_files.csv](source_files.csv) | URL, size and SHA-256 of each of the 102 files read. No source text is stored in the repository. |
| [PLAN.md](PLAN.md) | The coding rules for the scenario columns, written before coding. |
| [summarize.py](summarize.py) | Validates the tables and writes [summary.json](summary.json) (descriptive counts). |
| [tests/](tests/test_salvage_records.py) | Schema, sourcing and quote-length tests. |

## Freeze record

`PLAN.md` was written at 2026-10-09T18:22:12Z, before any scenario value was entered. SHA-256: `8c1fd70c97a187ebc68712a044eb34f5ee859b5bd2135c02c1cfedf97171a65b`. The plan attaches no decision rule to the counts. The coding was not changed after the counts were seen.

## What the repo already had (linked, not redone)

- Treatise of the Vessels, 2 Maccabees 2 and 2 Baruch 6 as legendary amount corpora: [T08](../../agent_review_2026-10-07/wave1/T08_real_or_legend/REPORT.md). Catalogue row C24 points there and adds nothing new.
- Thebuthi and the Greek letters at II 4: hypothesis H1b in `tables/phase4_hypotheses.csv` and record `e7-the` in `text/readings.json` (weak).
- Antiquities 18.85 on Gerizim: cited by Milik (DJD III p. 274) and Høgenhaven (p. 86 n. 84) in `tables/phase5_reports.csv`.
- Gerizim archaeology and locus P5178 (R05): [follow-up](../../sites/gerizim_locus5178_followup_2026-10-01.md) and `registration/gerizim_magen_neaehl_extracted.md`.
- Christmas Cave objects and grids: [provenance note](../../sources/christmas_cave_provenance_2026-09-30.md) and [primary follow-up](../../sites/christmas_hyrcania_primary_followup_2026-09-30.md).
- Twin Cave, 3Q and the 1985/86 survey: [ESI 6 review](../../sources/esi6_cave_survey_review_2026-10-01.md), [Bar-Adon capture review](../../sources/baradon1989_capture_direct_review_2026-10-01.md), [plan access](../../sources/twin_cave_plan_access_2026-10-01.md). The repo spells Jones's name in Hebrew there, so a search for "Vendyl" finds nothing.
- The 1993 survey regions: `registration/atiqot41_region_v_extracted.md` and the [IV/11 and IV/17 review](../../sources/atiqot41_iv11_iv17_review_2026-10-01.md).
- Qumran and Ketef Jericho hoards: [T02 hoards](../../agent_review_2026-10-07/wave1/T02_hoard_match/hoards.csv). These belong to the concealment worker; the ledger only notes them as finds.
- The 2017 IAA survey: [T09](../../agent_review_2026-10-07/wave1/T09_T12_T19_landscape_field/REPORT.md), finding 4.

## The catalogue

Kinds: 10 EVIDENCE, 15 TRADITION, 2 CLAIM. The 27 rows fall into 16 dependency groups (for example, all rabbinic ark traditions are one group). Count groups, not rows, when judging how many independent witnesses there are.

- **Jerusalem, 70–71 CE (Josephus, EVIDENCE).** A priest hands over lampstands, tables, vessels and vestments (C01, War 6.387–389). The treasurer shows the stores (C02, 6.390–391). The treasuries burn with private deposits (C03, 6.282). Soldiers search the underground passages and find valuables (C04, 6.429–433). Simon bar Giora emerges from an old passage (C05, 7.26–36). Buried valuables in the ruins are dug up, most through captives' information (C06, 7.113–115). The table, lampstand, Law and veils reach Rome (C07, 7.148–162).
- **Earlier recoveries (EVIDENCE).** Antiochus IV takes "the hidden treasures which he found" (C11, 1 Macc 1:23). A priest reveals a gold beam hidden in a hollow wooden beam to Crassus (C09, Ant. 14.105–109). Hyrcanus I and Herod open David's tomb (C10).
- **Gerizim (CLAIM and TRADITION).** A Samaritan leader promises to show vessels buried by Moses; Pilate stops the crowd (C08, Ant. 18.85–89). Samaritan and rabbinic traditions place hidden objects under Gerizim (C26, C27).
- **Hidden sacred objects (TRADITION).** Altar fire hidden in a dry pit and recovered (C12). Jeremiah hides the tent, ark and altar; his followers cannot find the cave (C13, 2 Macc 2:1–8). Angels or Jeremiah commit the vessels to the earth (C14 2 Baruch 6:7–10; C15 4 Baruch 3; C16 Eupolemus). Rabbinic texts hide the ark under the Temple, with the manna jar and the anointing oil (C19–C23). The Treatise of the Vessels (C24).
- **Inventories (TRADITION).** Ezra 1:7–11 counts the returned vessels; Ezra 8:24–34 weighs gold, silver and two copper vessels to the priests and records the weight at the Temple (C17, C18). INFERENCE (arithmetic): the items in Ezra 1:9–10 sum to 2,499, not the stated 5,400. Both are candidate additions to T08's comparison corpora (R12).
- **Later history.** Procopius says Justinian sent "the treasures of the Jews" to Jerusalem in 534 CE (C25, CLAIM about identity).

Not catalogued: the Lives of the Prophets (Jeremiah and the ark in a rock). No open-access text was found in this round.

## The search ledger

The ledger has 27 rows. Four were searches for the scroll's deposits (S03 Allegro 1959–60; S14 and S15 Vendyl Jones; S17 the 2009 probe at Kh. Qumran). Three were motivated by a scroll identification (S09 and S10 at Twin Cave; S13 the 1988 juglet). The rest are surveys for manuscripts or excavations of places the scroll may name.

Results: 19 other finds, 3 negative, 2 claimed finds, 3 unknown. Five rows are CLAIM-grade documentation (press, blogs, Wikipedia without citations).

What a later coverage worker can and cannot use:

- **No row gives a target volume.** None of the scroll-motivated searches has a published plan, section or depth tied to an entry's locator. Under AGENTS.md none counts as a negative excavation at a predicted target.
- **Gerizim (entry 57).** Two large excavations covered the summit: Bull at Tell er-Ras (1964, 1966) and Magen (1983–2006). Bull proposed his trench as the scroll's upper pit (Lefkovits 2000 p. 412; Bull's CLAIM). Neither reports a deposit. Whether any candidate "step of the upper pit" was cleared to its first-century surface is not established.
- **Qumran cliffs (entries 20–26).** The 1952 expedition searched about forty caves; Patrich surveyed from Nahal Og to Wadi Auja in 1983–1987; the 1993 Region XI team covered 1.4 km of escarpment but could not re-identify earlier caves from their grids. Joining these surveys cave by cave needs Reed 1954, Patrich's reports and the IAA archive (requested 7 October, ACTIVE_TEST).
- **Entry 25 (Cave of the Column).** Twin Cave was excavated in 1971, 1977, 1982 and 1986, partly with Jones's volunteers and partly because of the scroll identification. No northern-threshold datum is published, so the three-cubit target is not covered. Jones's 1992 dig was in a different cave north of his Cave of the Column.
- **Entries 31 and 35.** The 1993 Region VII report does not describe the Dok summit fortress. The Region XIV survey covers the Kidron outlet, not Mar Saba.
- **Christmas Cave and Kh. Mazin.** Allegro dug both. The repo assigns no scroll entry to either.

### Joining with the search-effectiveness looks table

`searches.csv` uses the same `place_id`, `record`, `looked_at`, `result` and `notes` names as `research/models/search_effectiveness/looks.csv`. Its `result` values differ: `negative`, `other_finds`, `claimed_find`, `unknown`. Proposed mapping: `negative` means looked and nothing found, with footprint unknown; the other three give no information on absence. `place_match` says whether the `place_id` is exact or only the nearest of the 49 places; joins should keep `near` rows separate.

### Conflicts kept open

- Allegro's expedition: "1959-60" (Davies, Copper Scroll Studies p. 28) against 1962 (Wikipedia, citing VanderKam 2010 pp. 92–93). Davies p. 35 n. 20 lists explorations in 1959, 1962 and 1963.
- Christmas Cave: found on Christmas Day 1960 during work at Kh. Mazin (Rasmussen et al. 2022 p. 2). If this was the first expedition, Davies's dates imply 1959. Not resolved.
- Jones 1992: press conference 30 April (Lindell 2026) or 8 May (Deseret News 1992). Jones's season count: seven (Deseret) or eight (Wikipedia).
- "Operation Scroll" names both the 1993 IAA survey and the 2017 programme.

## Analysis: what these records say about three scenarios

The counts in `summary.json` are descriptive. Rows are not independent, and a count is not a weight of evidence.

**1. Deposits real and removed in antiquity.** The contemporary accounts describe three ways hidden valuables were found within months of the fall of Jerusalem: custodians handed them over (C01, C02), soldiers searched underground passages (C04), and captives told where things were buried (C06). Earlier rulers did the same with Temple and tomb treasure (C09, C10, C11). INFERENCE: if the scroll's deposits were real and made around 66–70 CE by people who could be captured, these mechanisms make early removal of some deposits likely. The limits are strong. All these accounts concern Jerusalem; none concerns the desert, Jericho or Qumran; none mentions a written list; none names a place that the scroll names. Modern scholars hold this view as opinion: the 1996 Manchester symposium majority thought any treasure was probably recovered in antiquity (Brooke, Copper Scroll Studies p. 8). That is a CLAIM, not evidence.

**2. Deposits real but unrecovered.** No EVIDENCE row supports this scenario. All 11 supporting rows are TRADITION or CLAIM, and 10 of them also support the literary scenario: they are beliefs that sacred objects stay hidden. Silence is not absence: the lack of an ancient recovery record says nothing about any single deposit. The modern ledger does not help either. The three negative rows (S03, S10, S17) have unknown or tiny footprints. INFERENCE: the scenario is neither supported nor weakened by these records; only located, dated and fully excavated target volumes could test it.

**3. A literary or legendary list.** Lists and stories of hidden Temple objects were a living literary form from the second century BCE to late antiquity (C12–C16, C19–C24, C26). These texts share famous objects, famous hiders, supernatural keeping and an end-time frame. The scroll has none of these (T08). INFERENCE: the motif shows that such a list could be composed as literature, but the scroll's form differs from every legend catalogued here. This weakens a reading of the scroll as a legend of the 2 Baruch kind. It does not exclude a realistic composed list, which T08 also left open.

### Antiquities 18.85–89 and the scroll's Gerizim entry (entry 57)

**What Josephus reports (EVIDENCE of the event).** About 36 CE a Samaritan leader called his people to Mount Gerizim. He promised to show them the sacred vessels buried there by Moses (18.85; the Greek says "buried"). An armed crowd gathered at the village Tirathana (18.86). Pilate's horse and foot blocked the ascent and killed many (18.87). The Samaritan council accused Pilate before Vitellius, and Pilate was sent to Rome (18.88–89). Josephus reports no digging on the mountain.

**The buried vessels are a CLAIM resting on a TRADITION.** Later Samaritan tradition holds that the holy vessels were hidden when God's favour left Gerizim, to be revealed by the Taheb (Montgomery 1907 pp. 241, 243). A rabbinic polemic speaks of idols hidden under Gerizim by Jacob (Montgomery p. 168).

**The scroll's entry.** In Puech's reading (2015 p. 108) entry 57 places a chest with its vessels and 60 karsh of silver under the step of the upper pit or shaft on Mount Gerizim. This is an edition-based reading.

INFERENCE, labelled as such:

1. The passage is not a search record. The crowd never reached the mountain, so it adds no coverage for any spot on Gerizim.
2. It shows that, in the first century, many people believed sacred objects lay buried on Gerizim. A Gerizim entry in a first-century list therefore fits two opposite readings: a real deposit placed in a place with that meaning, or a list-maker using a known motif. The passage cannot decide between them.
3. The objects differ. Josephus's vessels are Mosaic relics with no location beyond the mountain. The scroll lists an ordinary container, silver by weight and an architectural locator. The scroll's entry does not carry the marks of the motif (famous hider, relics, end time).
4. Puech (2015 p. 108) notes that the name is written in two words, not in Samaritan practice, and (pp. 16–17) relates the Gerizim mention to possible Samaritan links. These are interpretations; this note adds none.
5. The summit was abandoned from about 110 BCE to the fourth century CE, with seven early Roman coins read as chance finds (Magen, via the repo). Abandoned ruins do not exclude a hiding place. The R05 records (the P5178 plan and stratigraphy, JSP 8 and JSP 20) and Bull's 1965 and 1968 reports (the trench's depth and date) are the observations that would bear on the entry. This note does not change R05.

## Access log and failed links

- New York Times, 16 Feb 1989 (the 1988 juglet): https://www.nytimes.com/1989/02/16/world/balsam-oil-of-israelite-kings-found-in-cave-near-dead-sea.html. Web reader: site blocked; direct request: HTTP 403.
- Jerusalem Report, 29 June 2017, "Operation Scroll": https://www.jpost.com/jerusalem-report/operation-scroll-498251. Body behind a login wall.
- Times of Israel, 16 March 2021: https://www.timesofisrael.com/dead-sea-scroll-discovery-brings-tantalizing-prospect-of-more-yet-to-be-found. Read through the web reader; a direct download returned HTTP 403, so the stored hash is of the error page.
- Patrich's project page: https://pluto.huji.ac.il/~patrichj/my_web_site/Research_Projects.html. Read through the web reader; a direct download returned a security error page.
- Allegro 1960 (2023 reprint, epub, owner's Drive 1JDz__fYchccCaP8Bx7QOKz5oQKaFRY6S): not accessed. The Drive text tool does not read epub.
- Copper Scroll Studies (owner's Drive): the text export stopped at 152,616 characters. Brooke's introduction and Davies's chapter were within it; Eshel's Hyrcania chapter was not.
- Not accessed (copyright or paywall; routes given): Reed, BASOR 135 (1954) 8–13 (JSTOR); Bull and Wright, HTR 58 (1965) 234–237; Bull, BA 31 (1968) 58–72; Patrich and Arubas, IEJ 39 (1989); Browning, BA 59 (1996) 74–89; Amar, Dead Sea Discoveries (1998); Allegro, Search in the Desert (1964/1965) and the 1964 second edition of The Treasure of the Copper Scroll; Magen and Peleg, JSP 18 (2018); Magen, JSP 8 (2008) and JSP 20.

## How to run and test

From the repository root:

```
python3 -I research/history/salvage_records/summarize.py
python3 -I -B -m unittest discover -s research/history/salvage_records -t research/history/salvage_records
```

`summarize.py` validates the four tables against `places_v1.csv` and writes `summary.json`. The tests check columns, controlled vocabularies, `place_id` values, that every row has a source that was actually read, that downloaded sources have hashes, that quotes are 12 words or fewer, that `summary.json` is current, and that this README records the plan's hash.
