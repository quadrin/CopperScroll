# Side-quest C4, round 2: published geophysics (6 Nov 2026)

What this round builds on: the round-1 cards C4-1 (the Qumran plateau shaft of 2002), C4-2 (the 2002 Qumran ERT section) and C4-3 (the Cave of Letters metal null), and review R5. New inputs read this round:
- the full text of all 4,748 Hadashot reports (local copy of `hadashot/derived/hadtext_pdftotext.tgz`), searched for geophysics in English and Hebrew; 50 English reports mention it;
- the ʿAtiqot texts (`atiqot/text/`, 1,420 files);
- a keyword search of the PDF store (ESI, HA-ESI, NEAEHL, Humbert–Gunneweg 2003);
- Magen & Peleg 2018, the refuse-dump section;
- Frumkin 2023 (`reading/04 …/Frumkin 2023 – Geology…Qumran Caves`);
- the unopened S34 figures (Reeder fig. 4.8);
- a pixel re-analysis of the 2002 ERT figure.

Data files in this folder:
- `geophysical_targets_tested_register.csv`: 17 published geophysical targets and what happened to them;
- `ert_connectivity_qumran_west.json`: the numbers behind card 3.

Private products (IAA figure extracts and the classified ERT array) are in `/home/claude/swarm/private2/C4/`.

---

FIND CARD
Title (one line): At Horbat Ha-Gardi, a candidate site for the Tomb of the Maccabees, a 2009 GPR/EM survey found a "large subterranean cavity" beneath Sheikh Gharbawi's tomb. No one has dug it, and the 2024 final report on the 2015 IAA excavation does not mention the 2009 survey at all.
Lane: C4
Round-1 link: new
What is odd (2–4 sentences):
- Re'em 2011 reports the August 2009 survey (U. Basson; GPR plus frequency-domain EM over about 6 dunams). In his words, "beneath the tomb of Sheikh Gharbawi there is a large subterranean cavity, whose eastern part is cut by a deep modern trench".
- The same survey found "dense architecture and underground cavities that can be divided into three and even four secondary compounds" between the tomb and the northern embankment.
- In August 2015 the IAA dug about 100 m² to test whether the site is the Tomb of the Maccabees. The work was at the el-Qalʿa burial chamber, 18 m north of the shrine.
- The 2024 final report lists every earlier investigation: 1870–71, the 1980s, the surveys of 2000 and 2005, and the 2006 dig. It leaves out the 2009 survey, and it never discusses the cavity or the shrine again.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- **HA 123 report 1712** (Re'em, 30/06/2011, map ref. 19960/64910), bucket `hadashot/pdf/en/vol-123/01712_h-orbat-ha-gardi.pdf`:
  - the paragraph that begins "Geophysical tests were undertaken within the precincts of the ruin in August 2009";
  - Fig. 19, "Map of geophysical tests; note the cavity beneath the sheikh's tomb" (PDF page index 26, image xref 240, 533×705 px). On its 20 m scale bar, the magenta zone around and south-east of the shrine is about 15–20 m across. This is my estimate from the figure; the report gives no size or depth.
  - Fig. 2 site plan (page index 13): the "Southern Dugout Pit" adjoins the shrine on the south.
- **HA 136 report 26469** (Re'em & Shachar, 26/03/2024; Permit A-7490), bucket `hadashot/pdf/en/vol-136/26469_h-orbat-ha-gardi.pdf` and the Hebrew version:
  - a full-text search of both language versions for geophys*, GPR, radar, cavit*, subterranean, Basson, גיאופיז, מכ"ם, רדאר and חלל found no geophysics (the one Hebrew hit for חלל is "the room's space");
  - "Sheikh Gharbawi" occurs once, in the site description;
  - the Fig. 4 plan covers only the chamber and the Mamluk farmstead to its north (walls W114, W116, W239, W240).
- Extracted figures (private, IAA images): `private2/C4/HaGardi_HA123_fig19_geophysics_map.png`, `…fig2_site_plan.png`, `HaGardi_HA136_fig4_plan_2015.png`.
Literature check (queries run, result, tag):
- Repo main and branch_only grep: "Gardi" gives only unrelated hits (Yoḥanan ha-Gardi in Allegro and Hyrcania extracts); "Gharbawi" and "Basson" give no hits.
- Web searches: "Horbat Ha-Gardi Sheikh Gharbawi tomb ground penetrating radar cavity Maccabees" and "Ha-Gardi Re'em Maccabees tomb geophysical survey Basson subterranean cavity".
- Pages read: the bibleplaces.com blog of July 2011 (summarises the 2011 report, no geophysics); artnet (no geophysics); Bible History Daily, 25 Sep 2015 (no geophysics; it quotes "the search for the elusive Tomb of the Maccabees continues").
- Tag: the cavity itself is published (2011). That it remains untested, and that the 2024 report drops the survey, I found in no publication: **NEW TO THE LITERATURE**.
Why it might matter:
- It is the only published "large cavity" at this candidate tomb, and it lies under a standing shrine.
- The 2015 dig targeted the Byzantine chamber, and its own dating of Strata VI–V is "uncertain". So the earlier rock-cut phase that a Hasmonean identification would need could lie in the untested zone.
- The 2015 plan also gives the first chance to check the 2009 prediction of "massive partition walls" north of the chamber, and nobody has made that check.
How to confirm or kill it (with data in hand, or what is missing):
- With data in hand: co-register Fig. 19 (grid lines labelled 199 550/199 600 E and 649 100/649 150 N) with the 2024 Fig. 1 and Fig. 4. Then ask whether walls W114, W116, W239 and W240 fall on the 2009 east–west magenta bands. If they do, the survey's reading of walls gains weight, and so does its cavity.
- Missing: Basson's 2009 report (not in the corpus) for depth and size. Also any IAA permit or publication after 2015 that touches the shrine.
- To kill: a publication showing that the cavity was entered (for example, as a cistern) or that it is the modern dugout.
- A small loose end: the 2011 report links the trench that cuts the cavity to Jewish National Fund works ("probably"); the 2024 report describes 1948 combat trenches of Outpost 219 on the ruin. These may be different features.
Confidence: high (that the cavity is published and not tested, and that the 2024 report leaves out the survey); low (that the cavity is a tomb chamber).
Touches the Copper Scroll? no.

---

FIND CARD
Title (one line): The corpus holds 9 published geophysical "void" targets that were later dug. Four were archaeological, one was an empty natural cave, and four were nothing. In the Lisan marl only the shallow cliff-edge target (0.5–1 m) was real; the deep plateau targets failed.
Lane: C4
Round-1 link: C4-1 (adds second witnesses and the consequence), with ARGUMENT for C4-2 and C4-3
What is odd (2–4 sentences): Round 1 had one negative test of a deep "cavity" (Qumran 2002). The corpus actually contains a small, usable track record, and nobody has put it together:
- **Positive, archaeological:**
  - Sepphoris 1985 (Strange's radar: entrances and cisterns, "probes confirmed their locations and depths");
  - the Naḥal Bet ha-ʿEmeq aqueduct shafts (3 of 3 located);
  - Cave of Letters GPR follow-ups (finds among the boulders);
  - Qumran "Cave 2001" (1 of 2 cliff targets at 0.5–1 m).
- **Natural void:** Har Karkom HK22lb (cavities to 4–8 m; the one dug was a natural empty cave).
- **Nothing:**
  - Qumran plateau west (16 m, stone lines);
  - Qumran plateau east (geologic);
  - the second Qumran cliff target;
  - Gezer 2003 (vertical electrical soundings; the trench to bedrock found nothing, and "the geophysical survey was not at all suitable for the rock structure").

The same J. F. Strange whose radar worked in limestone at Sepphoris ran the 1996 Qumran probe that failed in marl.
Evidence (exact sources: file path / page / figure / frame / coordinates): `geophysical_targets_tested_register.csv`, rows G01–G10, each with its source:
- HA 117 report 126 (Qumran; English and Hebrew; the Hebrew confirms "החפירה הידנית", the hand-dug shaft; the target depth of 16 m was "the approximate elevation of the entrance to Cave IV");
- HA 121 report 1294 (Gezer; Geophysical Institute of Israel report 03/347/278);
- store PDF `HA-ESI-113-2001…` page index 194 (Har Karkom 1999–2001);
- store PDF `ESI-4-1986…` page index 108–109 (Sepphoris, "Soil Interface Radar Survey");
- ʿAtiqot 70 text 1527 (Bet ha-ʿEmeq: "Shafts 1, 4 and 5 were located by Uri Bason using geophysical techniques");
- HA 118 report 327 (Garden Tomb: "probably the outer wall of a water cistern, revealed in a ground penetrating radar examination");
- Drive S34 notes `1b77R4NN3JVk2vxA1YF3xqxpwm7IFZdioxgpn92ZutUk` (Cave of Letters; Qumran 2001).

Context on how Lisan caves form: Frumkin 2023 (bucket `reading/04 Articles and chapters/Frumkin 2023 – …pdf`, p. 80–83):
- Lisan-terrace caves are either "entirely artificial" caves "dug within soft-layered sediments" (4Q, 5Q, 7Q–10Q), or piping caves carved by ephemeral streams;
- the terrace contains "conglomerates and gypsum layers".
Literature check (queries run, result, tag):
- Repo main and branch_only grep for "soil interface radar", "Bason", "HK22", "georadar", "geo-radar", "03/347" and "Yazersky": no hits. "Har Karkom" appears only in HA/ESI screening tables.
- Web search "geophysical cave detection Qumran marl false positive 'natural stones' seismic GPR Price 2002 review success rate archaeology Israel": no review or tally. The hits were unrelated geophysics papers and the Orion entry for Jol et al. 2002.
- Tag: each case is published. Gezer, Har Karkom, Sepphoris and Bet ha-ʿEmeq are **NEW TO THE PROJECT**. The tally and its split by substrate and depth are **NEW TO THE LITERATURE** (none found).
Why it might matter:
- The project codes geophysical "possible caves" as open leads (S34 notes; Witten's "likely a cave"; Freund's "still remains to be excavated"). The corpus's own record says how much weight such a lead deserves.
- Every confirmed archaeological void was either shallow (0–2 m) or in hard limestone settlement and aqueduct contexts.
- Both tested targets with a stated depth of more than 3 m were not archaeological: Qumran at 16 m was geological, and Har Karkom was a natural cave.
- Of 4 tested targets in the Lisan marl, only the shallow cliff-edge one was real.
ARGUMENT (kept apart from the evidence):
- (a) The untested Qumran ERT bodies of 2002 (register rows G13–G14; 4–9 m deep in marl, on the plateau beside the buildings) belong to the class that has failed every time it was tested. Three points lower their prior further:
  - Frumkin's two formation routes (caves hewn into slope faces; piping along runoff paths) give no reason to expect a sealed natural chamber deep in the plateau;
  - the terrace's conglomerate and gypsum layers are a ready source of resistive bodies;
  - the 1996 search, aimed at "the approximate elevation of the entrance to Cave IV", found no void at that level.
  
  For any scroll entry placed at Kh. Qumran, these anomalies should count as weak leads, not as candidate caves.
- (b) For the Cave of Letters (entry 25 in Freund 2004), the opposite holds. GPR there did lead to finds at 0–2 m, so the shallow survey was effective; this supports the round-1 reading that the metal null is informative near the surface. It says nothing about the deep debris (G15).
- (c) Small numbers: n = 9, classified by me. One confirmed deep marl void would overturn (a).
How to confirm or kill it (with data in hand, or what is missing):
- Extend the register from the remaining HA/ESI volumes before 2004 (keyword search here only; Hebrew-only reports before 116 not scanned) and from Frumkin 2015 (not in the store as a whole).
- Missing reports: the TAU 1990 report; GII report 03/347/278; the Strange 2006 chapter; Parry et al. 1998 (the BYU radar at Qumran; its outcome is unknown and could add a case).
- To kill (a): find a published deep (more than 4 m) cavity in Lisan marl that geophysics found and digging confirmed.
Confidence: medium (the facts are high; the classification and small n make the rate rough).
Touches the Copper Scroll? maybe. It sets how much weight geophysical "caves" at Qumran and the Cave of Letters deserve as places for scroll entries; it identifies nothing.

---

FIND CARD
Title (one line): In the 2002 Qumran ERT section ("west of ruins over dump"), the labelled "possible cave" is not a closed body. Its 100–180 Ω·m envelope rises to the surface through a neck 1.5–2 m wide at 39–41 m along the line, directly under the WALL marker at about 41 m. The second body (round-1 C4-2) is closed at every threshold.
Lane: C4
Round-1 link: C4-2 (and R5's "wall footing" alternative)
What is odd (2–4 sentences):
- Every published description treats body 1 as a closed void: "possible cave"; "a cave-like feature about 15 ft below the surface" (Freund 2009); "likely a cave" (Witten).
- When the colours are classified against the figure's own colour bar, body 1 reaches the surface at every threshold from 100 to 180 Ω·m, through a narrow neck at 39.0–41.8 m along the line and 2–3.5 m deep. It touches the surface at 34.6–41.3 m, between the FENCE marker (about 34 m) and the WALL marker (about 41 m).
- Only its ≥200 Ω·m core is detached (3.7–9.0 m deep, 30.3–39.4 m along the line).
- Body 2 (54–65 m, top at 4.2–5.8 m depending on threshold) is closed at every threshold from 100 to 150 Ω·m. There is no near-surface resistive pocket above it, although it sits under the WALL marker at 59 m.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Drive `Qumran_Freund2012_fig3.2_ERT_west_of_ruins_Bauman.png` (`1iT4sAYZ-iGWpebUW2Dq7CZlwcjOMxCZZ`).
- Method: pixels classified to the nearest colour of the 207-px colour bar (row py 588, px 380–586, read as linear 50–240 Ω·m), then 4-connected components. Round-1 calibration: x 8.93 px/m with 0 m at px 148; z 10.2 px/m with 0 m at py 355.
- All numbers are in `ert_connectivity_qumran_west.json`. The classified array is in `private2/C4/qumran_ert_west_resistivity_classified.npy`.
- Near-surface ≥200 Ω·m pockets (0.2–1.0 m deep) lie at 0.6–10.6, 13.2–19.4, 34.6–41.3, 51.4–53.9 and 72.6–79.7 m. They match the WALL markers at about 8, 41 and 74 m, but not those at about 24 and 59 m.
Literature check (queries run, result, tag):
- R5 read the same section in Bauman et al. 2002 (*CSEG Recorder* 27(10), Fig. 4): it has a caption only.
- The S34 notes, Witten 2006 §13.8.2 and Freund 2009 (via the S34 notes) all describe a closed cave-like body.
- Repo and branch_only grep for "QWEST", "possible cave" and "neck": only the round-1 C4 files and the S34 coding note.
- Tag: **NEW TO THE LITERATURE**.
Why it might matter:
- It changes how body 1 should be read. A body tied to a mapped wall at the surface could be:
  - (a) a shaft or entrance;
  - (b) a deep foundation trench or robber trench under that wall;
  - (c) dry dump fill in a hollow ("over dump");
  - (d) the inversion smearing a resistive wall or fence footing downwards.
- Readings (b)–(d) need no void.
- It also shifts R5's alternative: "wall footing" fits body 1, which is linked to a surface wall, better than body 2, which is linked to nothing at the surface. Body 2 stays the more "buried" of the two, and also the less resolved (its halo is open at the base of the section).
How to confirm or kill it (with data in hand, or what is missing):
- The published image is a smoothed contour rendering, so the neck could be a drawing artefact. Kill it with:
  - the inversion model (Komex file `J:\51660100\QWEST-ERT`);
  - a sharper copy of CSEG Fig. 4 that shows a closed contour between 2 and 3.5 m at 39–41 m.
- Missing:
  - the line's ground position, needed to identify the wall at 41 m (SPIE 4758 full text; Freund 2009 fig. 6.2);
  - which dump the line crossed. The corpus does not map it: Reeder's 2002 site map (`1YK3CbohS4uu4GREvVv1mkGm-sFlFymnn`) shows only an "Outline of January 2002 Spoil Pile" east of the ruins, over the Eastern Refuse Dump that Magen & Peleg excavated in 2001–2002 (print p. [59]). Freund 2009 puts the ERT over de Vaux's 1951 dump on the west, and the file tag is "QWEST".
- No field test is allowed in this swarm.
Confidence: high (that the figure shows the neck and the closure contrast at these thresholds); low (on what body 1 is).
Touches the Copper Scroll? maybe. The survey was a search for scroll caves; this weakens the "sealed cave" reading of its main anomaly.

---

## Dead ends

- Fitting the ERT WALL-marker spacing (8, 24, 41, 59, 74 m) to south–north transects on the Magen & Peleg 2018 Fig. 9 plan, with scale 0.85–1.15 and ±2 m tolerance: many columns fit 5 of 5, including lines inside the buildings. The spacing cannot locate the line.
- Reeder fig. 4.8 (Cave of Letters cross-sections a–v and long section): it shows only the open void outlines, not the thickness of the fill. It cannot settle the dispute over the depth of the C4-3 rubble (R5).
- Qumran cemetery GPR counts: 124 (Eshel's Brill chapter); more than 100 (Jol); "37 points near to the Qumran buildings" and "six concealed tombs on the Southern extension" (Eshel et al. 2002, as cited by Norton in Humbert–Gunneweg 2003, store page index 148 and 156); "20 graves" north–south near the settlement (Freund 2009). These are probably subsets of one survey, not a clean contradiction. Dropped.
- Hadashot full-text scan (English and Hebrew): of 50 reports, most geophysics is wall mapping in Galilee, on the coast or in the Negev (Rekhesh, Ḥaluẓa, Legio, Shimron, ʿEn Esur). Only Qumran, Gezer, the Garden Tomb and Ha-Gardi have void targets.
- ʿAtiqot texts: 20 papers mention geophysics, mostly magnetometry for walls (Ashqelon, Magdala, Legio). Only Bet ha-ʿEmeq was used.
- HA 101–102 (1993): Witten and Levy's geophysical diffraction tomography and GPR at Tel Dan, Kedesh, Gilat and Shiqmim. HA 104: Tel Ḥalif, where three methods were "unreliable". Neither gives a void target with an outcome.
- Masada ramp thickness survey (Gil et al. 2000, cited in NEAEHL): known, and not a void target.
- Price's 2004–08 Qumran seasons and the running text of Bauman 2018 ch. 6: no report or text found (web search on Bauman, EM61 and rockfall thickness gave only unrelated papers).
- HA 117 Hebrew version (round-1 open item): it confirms hand digging ("החפירה הידנית") and the Cave IV target elevation. Nothing beyond the English.

## Blocked inputs

- Basson 2009 geophysical report on Ḥorbat Ha-Gardi: not in the corpus (cited only by Re'em 2011). Fig. 19 is held only at 533×705 px (`Images//5149-19.jpg` inside the HA PDF).
- Geophysical Institute of Israel report 03/347/278 (Gezer, vertical electrical soundings 2003): not in the corpus.
- Still blocked from round 1:
  - Jol et al. 2002, SPIE 4758 (full text);
  - Strange 2006 (STDJ 57: 41–54);
  - Parry et al. 1998 (Flint & VanderKam vol. 1: 496–515);
  - the TAU 1990 Qumran survey;
  - the running text of Bauman 2018 ch. 6.
- `gsutil -m cp -r gs://copper-scroll-cog-1030/atiqot/text` took more than 300 s in the foreground. It finished in the background (1,420 files); no error.
