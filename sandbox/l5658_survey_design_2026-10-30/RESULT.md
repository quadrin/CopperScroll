# Run 24 result: could a non-invasive survey test the L56/58 lead?

Integrated 30 Oct 2026. Rule: [RULE.md](RULE.md), commit 8c6c2de, SHA-256 `135d80e4…cce536` (checked). Exploratory. Nothing here proposes excavation. No one was contacted.

## Verdict
**Not testable non-invasively** (main scoring). No method or pair reaches P ≥ 0.5 in Z1 for T-b. For T-a large (50 kg) the best estimate is 0.35–0.60, with a central value of about 0.45.

- **Rule ambiguity 1, scored both ways.** The T-a 50 kg range straddles 0.5. On the central value the verdict is **not testable**. On the upper bound it is **partly testable (T-a large only)**. The rule does not say which to use.
- **Rule ambiguity 2, scored both ways.** Z1 runs 0–3 m but has no depth prior. With a uniform prior: not testable. If the deposit lies in the top 1.5 m below today's surface: **partly testable** (T-a 50 kg 0.49–0.77). If it lies at 1.5–3 m: clearly not testable (≤ 0.43). See [out/depth_sensitivity_output.txt](out/depth_sensitivity_output.txt).
- **Gate G0 is not met.** Z1 has not been tested by excavation. The pool interiors were dug to their floors. The strip east of L58 was dug only to its ancient floors, plus two small soundings. The crack fill opposite L56/58 is unknown.
- **Controls agree.** L71 scores the same as L56/58. Hyrcania scores better for GPR, but still below 0.8. The verdict is driven by soil and depth, not by the choice of site.

A null survey over Z1 would not count against the lead. It would only clear the top ~1–1.5 m.

## G0: what was dug at and east of L56/58
Details and pages: [out/g0_excavation.csv](out/g0_excavation.csv).

| Part | Class | Basis |
|---|---|---|
| Pool interior (L56, L58) | **excavated to floor** | EVIDENCE. De Vaux 1973 p. 43: Roman clearance debris lay on L56's bottom and in mounds against L58 (Pl. XXIV a). Galor 2006 p. 263: de Vaux cleared most of L58. Magen & Peleg 2018 p. 44: in 2004 they dug the part de Vaux left and found ~0.5 m of clean clay on the bottom. L58 is 4.40 m deep; L56 is at most 2.75 m. |
| Pool floors and below | **excavated to floor**; below the floor **unknown** | EVIDENCE: floors reached. No sounding below the floors is reported in the pages read. |
| Strip from L58's east face to the crack (W607 and channel, L3028, L3034/36, L43, L62, L66, L74) | **excavated to floor**, with small soundings below | EVIDENCE. M&P pp. 41–44, Figs. 41, 46–47. De Vaux cleared the rooms. L62 was dug below L43 to a floor. In 1998, sounding L3033 in L74 found wall W626 resting on fill, not on virgin soil. In 2002 a cut 20 cm below L74's late floor reached the phase A floor. Other 1998 soundings found nothing new. |
| Crack fill opposite L56/58 | **unknown** | De Vaux p. 20 traces the crack across the ruins but reports no excavation of its fill there. M&P describe crack fill only in the eastern dump and the paved square. |

INFERENCE. Today's surface in the strip is roughly the ancient floor level. Any deposit 0–3 m deep in Z1 would lie mostly below the excavated floors. No source read reports a hoard, or a vessel group with a record, from L56/58 or the strip. Excavation therefore removed only the part of Z1 above the floors.

## Method table (Z1, L56/58)
Full grid for Z1–Z3 with all targets: [out/methods.csv](out/methods.csv). Basis codes: PUB = published case; PHYS = physics estimate ([out/scripts/](out/scripts/)); INF = inference.

| Method | T-a 5 kg | T-a 50 kg | T-b | Main failure | Null informative? |
|---|---|---|---|---|---|
| Metal detection (PI large loop / TDEM EM61) | 0.20–0.35 | **0.35–0.60** | 0–0.05 | Depth. A 50 kg group reaches ~1.7–2.8 m; a 5 kg group ~1.0–1.8 m. Walls cut coverage. | Weak, top ~1.5–2 m only |
| GPR 100/250/500 MHz | 0.10–0.25 | 0.20–0.30 | 0.15–0.25 | Marl ≤ ~50 Ω·m: reach ~0.8–1.9 m at 250–500 MHz | No |
| ERT 2D/3D | 0–0.05 | 0.05–0.15 | 0.10–0.25 | A 0.6 m body is resolved only to ~1–1.5 m | No |
| EMI (EM38-type) | 0.10–0.20 | 0.15–0.30 | 0–0.05 | Reach ~1–1.5 m | No |
| Magnetometry | ~0 | 0–0.05 | 0–0.10 | Silver and bronze are non-ferrous; a jar gives < 1 nT at 1.5 m | No |
| Muon (method 5) | ~0 | 0–0.10 | 0–0.20 | Finds chambers ≥ 1 m, not objects. 50 kg gives a 2–3 % contrast; walls give 20–40 % | No |
| Microgravity | 0 | ~0 | 0–0.10 | A jar-sized void gives 3.6 µGal at 1 m, 0.9 at 2 m; noise is 3–5 µGal | No |
| Any method, T-c | ≤ 0.02 | | | Too small | No |

- **Best pair:** PI/TDEM plus GPR. In the model, their union adds almost nothing at depth (0.38–0.54), because both run out at about 2 m.
- **False positives:** metal from the 1950s and 1990s digs, walkways, railings and conservation fixtures; walls, plaster floors, channel M25 and kiln L66. In Z3, graves are the main source: the 2000 walk-over found a strong metal signal over a grave, and it was a zinc coffin (Freund 2009, via the S34 notes). GPR plus PI would separate metal from stone, but not ancient metal from modern metal.
- **Z2 and Z3 (secondary).** Z3 has 230–490 kg at 1.3–2.1 m, which is shallow for the mass: PI/TDEM gives **0.55–0.80**. Two limits remain: the strip's position is not fixed, because run 17's C1 is unknown, and the cemetery adds false positives. Z2 is scored at the outer aqueduct head (gravel and limestone): GPR 0.30–0.60, PI 0.25–0.50. The limits there are the unknown "great stone" and aggradation. If Z2 is instead the sluice L132/137 at the site's edge, its ground is marl and it scores like Z1. The rule's criteria use Z1 only.

### Soil and the "GPR in saline marl" note
- EVIDENCE. The wave 1 T09 note goes back to the T19 draft. That draft cites general sources: the US EPA geophysics pages, and the EAC Guidelines 2 (Schmidt et al.), p. 15, on attenuation in salty soils. For marl at Qumran it cites Wikipedia. It cites no Qumran measurement. The note is a general-principle inference.
- EVIDENCE. Bauman's 2002 ERT line west of the ruins puts the marl in the lowest colour band, ≤ ~50 Ω·m, down to 10–12 m (Freund 2012 Fig. 3.2, Drive copy). That band fits a lossy, clay-rich ground. The "≤ 50" is read off the colour bar.
- EVIDENCE. GPR does work at Qumran at shallow depth. Jol et al. 2002 report grave hyperbolas and targets at 0.5–1.0 m, and more than 100 possible graves (abstract, via the S34 notes). The 2005 3D grid over Tomb 1000 used 225 and 450 MHz. No source gives a penetration depth in the marl.
- EVIDENCE. Magen & Peleg p. 3: the site sits on a marl shelf. M&P p. 38: the marl is unstable and has many cavities. Frumkin 2023 pp. 77–78: the terrace is Lisan Formation (aragonite laminae, detrital silt, gypsum), up to 50 m high. Rainfall is ~100 mm a year and evaporation ~2000 mm.
- INFERENCE. The marl is mostly dry. Its low resistivity comes from clay and salts. A rain event would raise its conductivity further. Brine-saturated Dead Sea sediments, at 0.2–5.8 Ω·m (Ezersky & Frumkin 2017), are not the case on the terrace.

## Controls (same assessment)
Full grid: [out/controls.csv](out/controls.csv).

| Control | Best method, T-a 50 kg | T-b | G0 | Note |
|---|---|---|---|---|
| L71: the crack in the eastern dump | PI/TDEM 0.40–0.60 | GPR or ERT 0.15–0.30 | The pool was dug to its bottom in 2004 (M&P p. 90). The dump squares along W649 and the crack fill were excavated (Figs. 70, 74–75); depth not read. | Same marl. Dump fill adds metal and ash clutter. If the crack fill was dug to its base, L71 is closer to "already tested" than L56/58. |
| Hyrcania double pool: ground to the east | GPR 0.40–0.65; PI 0.30–0.55 | GPR 0.35–0.60 | The pool was sounded only (Patrich 1989 p. 255). The ground to the east is not excavated. | Dry Hatrurim rock suits GPR (INFERENCE 200–2000 Ω·m). Rough rock-cut benches limit coverage. The rock is strongly magnetic (Khesin et al. 2005, title only). |

Neither control reaches 0.8. The method ranking changes with the ground (GPR at Hyrcania, metal detection on the marl). The verdict does not change.

## Permits and cost (estimate)
- **Authority.** Qumran lies in Area C. Survey and excavation there are licensed by the Staff Officer for Archaeology (Staff Office of Archaeology – Judea and Samaria) in the Civil Administration, under COGAT. Sources: the Emek Shaveh note of 3 June 2026; Haber & Gutfeld 2024 p. 103* n. 2, a 2023 season at nearby Hyrcania that names that office. The site is run as Qumran National Park by the Israel Nature and Parks Authority (INPA leaflet, Nov 2025), so park consent would also be needed. Using a metal detector needs explicit permission. A Knesset bill to move this role to a new "Heritage Authority in Judea, Samaria and the Gaza Strip" passed its first reading on 11 May 2026. It was halted on 2 June 2026 but not withdrawn. Its status after June 2026 was not found. Other parties dispute the legitimacy of this licensing (T19 draft §5). This is recorded, not assessed.
- **Best plan, if run anyway (estimate).** Z1, plus Z3 if C1 is ever fixed:
  - Methods: TDEM (EM61-type) and PI large-loop metal detection on a 0.5 m grid; GPR at 100 and 250 MHz on 0.25 m lines; two or three ERT lines across the crack. Magnetometry only as a map of iron litter.
  - Time: 3–5 field days, a 3–4 person team, 2–4 weeks of processing.
  - Cost: **US$15k–40k** (ESTIMATE, low confidence). This excludes the months-long permit process, permit fees and any follow-up. The T19 draft's rate of ~$1k–3k a day for commercial GPR fits this range.
  - What it buys: a check of the top ~1.5–2 m for ≥ 50 kg of metal (P ~0.5–0.75 there). It cannot make a null count against the lead.

## Caveats
1. The P values are physics-and-judgement ranges, not field calibrations. The key inputs are the marl resistivity (read off one ERT colour bar) and the EM61 drum benchmark at 3.5 m (a cave floor, not marl). The 50 kg group's effective size and coupling are assumptions. All inputs are in [out/scripts/detect_model.py](out/scripts/detect_model.py).
2. G0 rests on de Vaux 1973, Galor 2006 and Magen & Peleg 2018. The 1953–54 field notes were not read (Humbert & Chambon 1994; Humbert, Chambon & Pfann 2003). They could show cuts below the floor or a dug crack fill. Either would change G0 only toward "already tested".
3. Run 12's crack position (2.3–5 m east of L58) comes from a schematic plan with no legend. Z1's 2 m half-width may miss the true line.
4. Entry 22 gives no depth or weight. T-a and T-b are the rule's assumptions.
5. The plate number Pl. XXIV a is inferred from the order of the plate list (the OCR is garbled).

## Not accessed (please help if possible)
- Humbert & Chambon 1994, *Fouilles de Khirbet Qumrân et de Aïn Feshkha* I: Internet Archive item `fouillesdekhirbe0000unse` (https://archive.org/details/fouillesdekhirbe0000unse) is access-restricted. Search-inside returned 403. Needed: the field-note entries for loci 56, 58, 62, 74 and the crack.
- Humbert, Chambon & Pfann 2003, *Synthesis of Roland de Vaux's Field Notes*: not in Drive. Catalogue: https://orion-bibliography.huji.ac.il/node/54407.
- Humbert et al. 2016 III A (Drive 280 MB): the connector returned no text.
- Magen & Peleg 2018, eastern-dump text pp. 58–66: not in the readable Drive text (it stops at p. 57). The figures on pp. 63–68 and p. 51 were read. The 77.5 MB chapter is over the limit.
- Jol et al. 2002, SPIE 4758: 91–95 (DOI 10.1117/12.462202): full text not read.
- The UWEC GPR poster, https://people.uwec.edu/jolhm/Past_Students/Bob/Subpages/Research/GPRPoster.htm: WebFetch was blocked by robots.txt and the run did not work around it. The repo holds hashes of its images (registration/qumran_gps_sources.json).
- The gov.il archaeology unit page (https://www.gov.il/en/departments/units/archeology_unit): client error.
- DOAJ (International Journal of Speleology, 2017), https://doaj.org/article/33d1b9805cfc430d98d6766f239dae34: client error.
- Khesin et al. 2005 (*GJI* 162): abstract not shown. Frumkin et al. 2011 (*Geomorphology* 134): abstract only.

## Sources
- de Vaux 1973, *Archaeology and the Dead Sea Scrolls*, pp. 8–9, 20, 27, 43; Pls. XVI, XXIV a, XXXIX. Owner's Drive copy, read as text.
- Galor 2006, "Qumran's Plastered Pools", pp. 259, 262–264, Fig. 8 (repo PDF).
- Magen & Peleg 2018, *Back to Qumran*: p. 3; pp. 36–38, 41–45, 48, 51 (Drive text); Figs. 41, 68–75, 99, 105–107 (repo assets); p. 90. https://www.jstor.org/stable/j.ctv1t8cdq.6
- Patrich 1989, Hyrcania, p. 255, Figs. 22–23 (repo extract). Haber & Gutfeld 2024, pp. 103* n. 2 and 110* (repo extract).
- Freund 2012 Fig. 3.2 (Bauman ERT); S34 extraction notes (Drive): Bauman (EM61/EM38), Jol (GPR), Jol et al. 2002 abstract, Freund 2009.
- CSEG Recorder, Dec 2002: https://csegrecorder.com/articles/view/intrigue-mystery-and-geophysics-dead-sea-archaeology-2001
- Frumkin 2023, *New Studies in the Archaeology of the Judean Desert*, pp. 75–83 (Drive; CC BY-NC).
- Ezersky & Frumkin 2017, *C. R. Géoscience* 349: https://comptes-rendus.academie-sciences.fr/geoscience/articles/10.1016/j.crte.2016.08.001/
- Frumkin et al. 2011: https://cris.huji.ac.il/en/publications/the-dead-sea-sinkhole-hazard-geophysical-assessment-of-salt-disso/
- Abueladas et al., EGU2010-9864 (GPR to ~10 m in Aqaba sediments): https://meetingorganizer.copernicus.org/EGU2010/EGU2010-9864.pdf
- Wave 1 T09 report and T19 draft (research/agent_review_2026-10-07/wave1/T09_T12_T19_landscape_field/).
- Permits: Emek Shaveh, 3 June 2026: https://emekshaveh.org/en/wp-content/uploads/2026/06/Antiquities-Bill-Halted-3-June-2026.pdf ; Times of Israel, 2 June 2026: https://www.timesofisrael.com/netanyahu-said-to-halt-progress-of-controversial-west-bank-and-gaza-antiquities-bill/ ; Asharq Al-Awsat, 25 June 2026: https://english.aawsat.com/arab-world/5288375-palestinians-decry-israeli-push-control-over-ancient-west-bank-sites ; INPA leaflet: https://static.parks.org.il/wp-content/uploads/2025/11/kumeran-en.pdf

## Files
[out/g0_excavation.csv](out/g0_excavation.csv), [out/methods.csv](out/methods.csv), [out/controls.csv](out/controls.csv), [out/physics_model_output.txt](out/physics_model_output.txt), [out/muon_output.txt](out/muon_output.txt), [out/depth_sensitivity_output.txt](out/depth_sensitivity_output.txt), [out/scripts/](out/scripts/). Downloads stayed in the scratch folder; none are committed.
