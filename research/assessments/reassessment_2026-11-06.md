# Reassessment of the entries touched by the 6 November side-quest

6 November 2026. Entries: 4, 11, 15, 19 and 60 (Koḥlit); 24 (Wadi Kuteif); 25 (cave of the pillar, with the 3Q area); 16, 29 and 35 (Hyrcania); 21 (briefly).

**Inputs.** Repo `main` at bb612c3. PR #94 (`claude/data-fixes-2026-11-06`, e290135) for the corrected cave and water data. The round-1 and round-2 swarm cards and reviews in `/home/claude/swarm/`. AGENTS.md procedures (frozen protocols, held areas, exposure labels, blind readers, outcome labels) are not applied.

**Conventions.**
- *Evidence* means a source says it. *Inference* means our reasoning from it.
- **strong / moderate / weak / none** say how far the evidence picks one candidate over the others. They are my judgement, not the rubric scores.
- Rubric levels (R reading, P place, F feature, D date; 0–3) are quoted from `research/assessments/evidence_components/ratings.csv` ("ratings line N").
- No coordinates of unrecorded features are given. The Mughâret Ekteif positions are in `private/E24b/` only.

---

## Summary

| Entry | Leading candidate | Strength | Change since 5 Nov | Most useful next observation |
|---|---|---|---|---|
| 4, 11, 15, 19, 60 (Koḥlit) | Tell es-Sultan (Puech's hypothesis) | weak (15: none) | Rivals pruned, leader not raised. Carmel loses its only witness. Tell Muhalhil weakened. Two chain relations shown to be common. | A human reading of XII 10–11 on the WSRP 1988 masters (reading) |
| 24 (Kippa ravine) | Wadi Kuteif, on the route only | ravine: weak; tomb: none | The SWP chamber has a map position (±250–300 m) on a reach cut by Route 1. Its description fits water access better than a tomb. | **Field:** zones Z1 and Z2, lower Wadi Ekteif (`private/E24b/`) |
| 25 (cave of the pillar) | No leader: IV/17, Twin Cave and XII/53 tied | none (P is 0 for all) | Data cleaning only (3Q's 1986 record; juglet cave placed; three facings) | IV/17 permit file L-656 (archive) |
| 16 (conduit to …) | Hyrcania and Tell es-Sultan, both on a restored lacuna | weak at best; no lead | None | IV 3 lacuna (reading; low yield) |
| 29 (northern reservoir) | Jericho palace pools | weak | None | VII 3 gap (reading) |
| 35 (cairn, Kidron gorge) | Kidron at Mar Saba | weak (Hyrcania: none) | None | A dated cairn at a gorge mouth |
| 21 (head of the conduit) | Kh. Qumran aqueduct | weak (atlas: medium) | None | None worth its cost now |

---

## 1. Koḥlit: entries 4, 11, 15, 19 and 60

### What the text requires

Readings as in `text/readings.json`:
- **4 (I 9–12):** the mound (תל) of Koḥlit, with an immersion feature. Milik, Wolters and Eshel read ניקרת "crevice"; Puech 2006 reads מקרת "cold room" of a bath. The plate check on I 12 split (ratings line 9).
- **11 (II 13–15):** the pool east of Koḥlit, in the northern corner. All the main editions agree (ratings line 16, R = 3).
- **15 (IV 1–2):** a great cistern with a pillar, "north of Koḥlit". Name and direction are both Puech's restorations; Milik saw only …QH (ratings line 22).
- **19 (IV 11–12):** the eastern pit north of Koḥlit. Allegro reads "hole", with no place name.
- **60 (XII 10–13):** north of Koḥlit, a pit with graves at its mouth. Its opening is "hidden" (Puech) or "toward the north" (Milik). The next word is שכנה (Puech), שבצח (Milik) or שבינח "in Janoaḥ" (Lefkovits, Beyer). The plate check saw no yod and no צ, which leans to Puech.

A full fit needs a tell, a pool on its east, and to the north a pit, a set of pits and graves at a pit mouth, all usable in the window.

### Candidates now

- **Tell es-Sultan (Puech 2006 p. 175 n. 49; 2015 pp. 13–14 n. 49).**
  - For: a ruin-mound. A spring basin at the east foot (SWP's 24 × 40 ft reservoir). To the north, Roman graves (Kenyon III pp. 173–174), burial D9, pit P29, cistern NS1, and quarry pits.
  - Against: Puech offers it only "à titre d'hypothèse". Høgenhaven 2020 p. 89 accepts it only if Achor is Wadi Nuweiʿimeh. There was no Roman occupation on the tell, the basin is undated, and no pit with graves at its mouth is recorded. Every step rests on Kenyon's one expedition (`kohlit_chain/README.md`).
  - Side-quest: no direct change.
- **Kh. el-Marjama / ʿEin Samiya (Zissu 2001).** Kallai 1972 pp. 172–173 put the only pool west of the tell, undated (R07, 19 Oct). Zissu's case also needs the Janoaḥ reading. No change. Its open test is MARJAMA-2, the 1945 RAF dark square.
- **Janoaḥ route (Lefkovits, Beyer).** Exists only if XII 10 reads שבינח. The 30 Oct place-first test was not identifiable. No change.
- **Carmel, ʿEin es-Siah (Milik 1962, DJD III D71 p. 274).** Its only basis is the Massekhet Kelim preface on the lost Beirut plaques. Side-quest card E1-1 (survived RR6):
  - Eshel and Safrai (*Cathedra* 103, 2002, n. 66) convert AM 3331 to "373 BCE". The correct value is 431/430 BCE. They also call the preface "a late addition".
  - Dugan (BAR Summer 2023 sidebar) argues the plaques are modern forgeries, twins of the "Ezekiel tiles" that Schwartz (BGU MA thesis, 2021; not read) judged modern.
  - PaleoJudaica (May 2011, quoting the *Jerusalem Post*): the plaques were lost and their authenticity was "open to question". The blogger dated both sets no earlier than the 7th–8th c. CE (`SUMMARY_ROUND2.md`, last section).
  - Inference: either way, the preface is not a Second Temple witness. Carmel now has **no evidential basis**. Few held it, so the change is small.
- **Tell Muhalhil (Lurie 1963).**
  - D1-3: Bar-Adon's full ASI 1 entry (Kochavi ed. 1972, Hebrew pp. 118–119, site 83) lists five sub-sites. None has a pool, cistern or tomb, and none has Hellenistic or Roman pottery.
  - RR6: ASI 109/5 units 99–100 ("Tell Muhalhal (8)–(9)"), about 1.5 km SE on the plain, have Early and Late Roman and Byzantine pottery. There is no pool anywhere.
  - Judgement: weakened (no mound, no pool), but not dead.
- **Kh. Qumran (Pixner; Thiering; in the chain only through the rarity list).** D1-1: ʿAtiqot 41 Plan 6 shows XI/18, 883 m at 347° from the anchor, opening about 6–45° true. QUMRAN-1 (Milik's "opening to the north") succeeds. The cliff runs N–S, so this is a cheap success. Qumran is not a tell, so entry 4 excludes it.
- **Generic two-of-three units.** Four records were compared with the chain for the first time (D1-2, RR6):
  - **Kh. ʿAlmit (S2849).** Dinur and Feig, Benjamin survey, Hebrew p. 380, site 496: a burial cave with the upper opening of a 70-niche columbarium "near the cave's opening". Pottery is mostly Hellenistic–Roman (p. 381). HA-ESI 115 p. 48* adds graves above a burial cave of the 2nd c. BCE to the mid-1st c. CE. "Tombs at the mouth" is met. The pages had been read on 11–12 Oct; the comparison is new.
  - **Tananir (E99).** HA 28–29 pp. 39–40: the only pool is about 50 m west. This leans against "pool east".
  - **Udala (S1032).** *Highlands of Many Cultures* p. 700 lists only cisterns and a sheikh's tomb. Inconclusive.
  - **Tell es-Samrat (S2430).** VIII/29 has a "northern opening" (ʿAtiqot 41 Region VIII, English p. 122). S2430-2 succeeds, as cheaply as at Qumran.
  - **Tell esh-Sheikh Dhiab (S6040).** Not misrouted (RR6): Zertal Vol. 4 site 194 is the right record, for ʿArkan es-Suwaneh. It is still unread.
  - **Tulul Abu el-ʿAlaiq and Kypros.** Region IX gives no facings. Not decidable.

### Judgement

- **Tell es-Sultan leads, weakly.** The lead comes from an editor's proposal and from Jericho being near other Jericho entries, not from a feature test. Entry 15's support is **none**.
- The side-quest **pruned rivals but did not raise the leader**. It also showed that two of the chain's relations are common: north-facing openings on a N–S cliff, and burial caves beside shaft mouths. Relations met at the first sites read cannot discriminate.
- Inference: the relations that could discriminate are still unknown everywhere. They are a dated pool east of a tell, and a pit in use in the window with graves at its mouth.
- **What would change it.**
  - XII 10 read as שבינח moves Koḥlit toward the Samarian desert edge.
  - XII 11 read as "hidden" removes the opening-facing relation.
  - Kenyon III Pl. 111b could show whether the pits north of the tell were cut while the graves were open (raises Tell es-Sultan) or later (lowers it).

### Single most useful observation

- **XII 10–11 read by a human epigrapher on the WSRP 1988 masters CT19–CT23.** They are unprocessed, on the owner's Mac. The Allegro/DQCAAS frames C.21A and C.22A are in hand (`research/sources/books_usc_2026-10-30/xii_images_released_2026-10-30.md`).
- The 22 Oct external-AI attempt failed: 38 of 48 lines could not be aligned (`research/text/xii10_owner_external_ai_exploratory_2026-10-22.md`).
- Record the reading before comparing it with the editions.

---

## 2. Entry 24: the tomb in the Kippa ravine (V 12–14)

### What the text requires

- "In the tomb (קבר) in the ravine (נחל) of the Kippa, as one comes from Jericho to Sekakah", dig seven cubits.
- Milik, Puech ("certain", 2015 p. 59) and Lefkovits agree (ratings line 35, R = 3). Allegro reads "the eastern entrance", with no Jericho, and takes Kippa = Wadi Qumran (Allegro 1960 pp. 69–70, 74).
- No name survives for Kippa ("rock" or "vault"). Sekakah is Kh. Qumran for Puech and Kh. es-Samra in the Buqeiʿa for Milik 1962.
- So the text needs a tomb in a ravine on a way from Jericho toward Qumran or the Buqeiʿa, usable in the window.

### Wadi Kuteif, before and after

- **Before.** Milik (DJD III D12 p. 264) chose Wadi Kuteif from the route. He pointed to the SWP chamber, "probablement un tombeau". It was held at square level and undated (ratings line 35: F = 1, D = 0, label "none").
- **Round-1 C2-1 (survived R4).** SWP sheet XVIII prints "Mght. Ekteif" on the north side of the lower wadi, near the Nebi Musa track crossings. That is about 2.4–2.6 km east of the project's `kuteif` anchor and the Early Islamic graves WBADB E508. No record lies within about 500 m.
- **Orchestrator hunt (`e24/HUNT_2026-11-06.md`), with RR6's corrections.**
  - Route 1 cuts the gorge loop. It was built between the 1940s and June 1974, and widened by 2023 with fill on most of the north side.
  - Two intact zones remain, Z1 and Z2.
  - No cut is visible at 0.5–2 m resolution. That says little about a roofed passage 1–3 m wide.
  - Position: ±250–300 m. Road building is one possible cause of loss, not the most likely; the SWP already found the chamber "choked up" in 1873.
- **The description.** Memoirs III p. 220: a cut sloping about 1 in 2 for 120 ft, with steps, ending in a choked chamber. A 37 m stepped descent with a 16 m drop fits a cistern or water-chamber access better than a tomb dromos, which in this region is short (inference). RR6 notes that this weakens the chamber as the entry's *tomb*.
- The frozen test of the same day (`e24/RESULT.md`) failed its positive control. It adds nothing.

### Realistic tomb candidates

From the tombs lane, branch 24-J (route within 3 km plus a wadi word; `research/regional/tombs/README.md` lines 105, 134–136, 213–227):
1. **Mughâret Ekteif (SWP chamber).** On the route: all eight Jericho→Secacah corridor lines pass within 3 km. Kind uncertain, now leaning to water. Undated. **Possible, weakened.**
2. **WBADB E508 / Peleg, JSP 10 pp. 257–258 (English p. 29\*).** Four pit graves, read as Early Islamic, 3.2 km from the road line. **Fails on date.**
3. **ʿAqabat Jabr South (3), ASI 109/5/62 (Sion).**
   - For: "hundreds of graves" in a local streambed, 92 m from the road line. Hasmonean, Roman and modern pottery on the site. It is the only recorded burial unit that meets both the route and ravine clauses with window-period pottery present.
   - Against: the graves themselves are undated. It is a cemetery, not "the tomb", and the streambed is unnamed.
   - **The best recorded alternative, untested.**
4. **Jericho cemetery Hills F–G (Hachlili and Killebrew 1999).** F4 and F7 are window-dated and lie by Wadi Tasun. They match only because the 3 km zone wraps round the palaces end of the road. They lie NW of the town, away from Qumran. **Weak; wrong direction.**
5. **Wadi Qumran (Allegro, 24-A).** Only on Allegro's reading. On the majority reading Qumran is Sekakah itself, not a place on the way. Inference: if Sekakah is in the Buqeiʿa, the climb by Wadi Qumran is one way up. But no tomb in that ravine is recorded in the project's layers.
6. **St George/Choziba (ASI 109/4/7–8) and the Wadi Khashna mounds (ASI 109/7/19).** Byzantine and off the route, or undated and only inside 5 km. **None.**

### Is Wadi Kuteif still the best reading of the ravine?

- **Not demonstrably.** Its claim now rests on the route, and the route does not separate it from other ravines.
- **It keeps a small edge in two ways.**
  - If Sekakah is in the Buqeiʿa, the SWP road up to the Buqeiʿa and Hyrcania is said to start at the lower Wadi Ekteif (Memoirs III p. 188, via HUNT). But Thomsen 1917 called that road "wohl erst byzantinische Anlage" (round-2 C2-3).
  - It is the only ravine on the route with a recorded artificial underground chamber.
- **Against it.** The project's anchor sits on the upper reach, where the only dated graves are Early Islamic. The chamber reads better as water access.
- **Judgement.** Ravine: **weak**. Tomb: **none**. On present records ʿAqabat Jabr South (3) is as good a tomb candidate as anything in Wadi Kuteif, and better on period. It fits "the tomb" less well, and nothing dates its graves.
- **What would change it.**
  - A burial chamber at the end of the SWP passage (kokhim, loculi, ossuary fragments) makes Kuteif **moderate**.
  - A cistern there removes Kuteif's only feature.
  - Second Temple grave forms at ʿAqabat Jabr South (3) make it a real rival; Islamic pit graves remove it.

### Single most useful observation

- **FIELD: Z1, then Z2** (`private/E24b/`). Look for a sloping, stepped rock cut 1–3 m wide on the north side of the gorge, and photograph any chamber mouth with a scale.
- First, if possible, check the Route 1 works records and full-resolution 1940s RAF verticals.
- Tie any HEXAGON F014 window locally to the Mandate 1:20,000 ink. A frame-wide fit errs by hundreds of metres (round-2 C1a-3).

---

## 3. Entry 25 and the 3Q area

### What the text requires

- VI 1–6: "the cave of the pillar with the two entrances, facing east, at the northern entrance", dig three cubits.
- Allegro's "platform/terrace" for the pillar noun changes the feature (Puech 2015 p. 60). Milik attaches "facing east" to the cave (1960 p. 140); requiring both mouths east is stricter (R02).
- No place is named, so P = 0 for every candidate (ratings lines 36–37).

### Candidates now

- **Jebel Abu Saraj IV/17.** Two openings, a rock-cut pillar, a distinct northern opening (Plan 5). Normals about 119–123°, so "east" is not rejected. Coins give use in the 2nd–1st c. BCE. Nothing dates the wall, pillar or threshold (ratings line 36). **Possible; weak on date.**
- **Twin Cave near 11Q (Bar-Adon 1989 pp. [15]–17).** A rock pillar divides two units, each with an east-facing opening. No plan, no threshold, finds keyed only "Cave A/B". It is the only both-mouths all-match row (`caves_entry25/scores.csv`, `REPO:TwinCave`), but its atlas crosswalk is unresolved. **Possible; best geometric fit.**
- **XII/53, Naḥal Qumran.** The only cave-level all-match row: an east-facing opening split by a built, undated pillar. **A compatible control.**
- **3Q and the juglet cave X/35.** Not candidates. 3Q is unknown on all clauses but the first; X/35 fails the pillar and two-mouth clauses.

### What the side-quest changed

- **B2-1 (PR #94).** WBADB E756 "Cave Q-3" is 3Q itself, dug in April 1986 under licence L-399/1986 (ESI 6 pp. 68–69). Its point was 2.95 km SE on the plain. It is now merged into DJD3:8. A phantom cave is gone.
- **C3-3.** X/35 = Patrich and Arubas Cave 13 lies 0.43–0.50 km NNE–NE of 3Q (ʿAtiqot 41 grid; IEJ 39, 1989, p. 43). This settles a record question, not entry 25.
- **D1-1 (PR #94).** Facings added for XI/18, XI/20 and VIII/29. About 30 more plan-bearing ʿAtiqot 41 caves can be read the same way. 607 of 635 rows still lack a cave-level facing, so the denominator stays weak.

### Judgement

- **No leader. Strength: none.** Each candidate fits the features in part. None has a dated threshold or pillar. Nothing in the landscape can raise P above 0. The best attainable result is a cave that fits every clause and was in use in the window, and there may be several.
- **What would change it.** A sealed first-century date at the IV/17 northern threshold. Or a Bar-Adon field record that fixes the Twin Cave's northern unit and its threshold.
- **Single most useful observation.** The IV/17 field file, Dadon L-656/1994, baskets 656.17 and 656.20 (archive). Cheaper but weaker: a **field** measurement of the Twin Cave mouths, which gives geometry but no date.

---

## 4. Hyrcania: entries 16, 29 and 35

- **16 (IV 3–5).** The conduit's goal is lost.
  - Eshel restores "Hyrcania", assuming a geographical order (Copper Scroll Studies pp. 102–103). Puech 2015 n. 193 calls it too long; he restores "the pool". The plate check finds no traces (ratings lines 23–24).
  - Eshel's starting point (a trail crossing the northern aqueduct only) is not located. Patrich 1989 p. 251 records only a trail-mark near dam 44.
  - **No lead.** Hyrcania is **weak**, conditional on the restoration.
- **29 (VII 3–7).** The great northern reservoir at the conduit of קי◦: Puech "collection [of the waters]", Eshel Qi[dron] (ratings lines 43–46).
  - The Jericho palace pools have P = 3, F = 2, D = 2.
  - Hyrcania's northern basin (Patrich 1989 p. 255) has no known inlet (Patrich 2002 p. 348; Feldman pp. 328, 332). The Hyrcania assessment is inconclusive (`assessments/entry29_hyrcania/README.md`).
  - **The Jericho palace pools lead, weakly.**
- **35 (VIII 8–9).** יגר = cairn (Milik, Puech 2015 p. 73 n. 298, Høgenhaven) or dam (Luria, Eshel). Patrich 1989 p. 244 found "no remains at all of a diversion dam" at the Kidron intake.
  - **The Mar Saba stretch leads, weakly.** Hyrcania: **none**.
- **Side-quest.**
  - B3-4: Naveh (ʿAtiqot Hebrew series 7, 1974, pp. 56–57) dated the Aramaic monumental fragments from Kh. el-Mird to the first half of the 1st c. BCE. Wikipedia, citing CIIP IV.1, says CE; Haber and Gutfeld 2024 omit the stone. This is neutral: it shows Hasmonean-era building, not 1st-century CE use.
  - A5-3: the tunnel commentary matches NEAEHL vol. 5 pp. 1787–1788. The tunnels are not features of these entries.
- **Judgement.** No change. All three are limited by the reading (R = 1), so no field work at Hyrcania can lift them first.
- **Next observations.** Readings of the IV 3 lacuna and the VII 3 gap, to test whether Qi[dron] fits the space. Expected yield is low.

---

## 5. Entry 21 (V 1–4), briefly

- **Reading.** The head of the conduit of Sekakah, "from the north", with "great [stone]" restored. The link word is lost: "west of" (Puech), "leading to" (Lefkovits, Beyer, Eshel), or "at" (Milik) (ratings line 32, R = 1).
- **Candidate.** The Qumran aqueduct intake (Ilan and Amit 2002 pp. 381–385; dam no. 4 reconstructed only). It was in use in the window (Humbert 2016 pp. 425, 432).
- **Side-quest.** C3-1 moves the Herodium aqueduct rows (Mazar 1989 p. 193, grid 1678 1217). The comparator's flow bearing goes from 285° to 292° and still fails. No score changes.
- **Judgement.** Qumran leads, **weak** (atlas: medium). Unchanged. No next observation is worth its cost: the V 1–2 lacunae are smooth on the plates.

---

## Ranked next observations

Order: (possible change to an identification) ÷ (effort). **FIELD** marks field targets.

1. **XII 10–11 on the WSRP 1988 masters CT19–CT23, read by a human epigrapher, with the Allegro C.21A and C.22A frames.** Reading; low effort. Decides the Janoaḥ branch and the opening relation for entries 60, 11 and 19.
2. **Kenyon, *Jericho* III plate volume, eastern section 37.50–38.00 m N, Pl. 111b.** Library scan; low effort. Tests Tell es-Sultan both ways for entries 60 and 19.
3. **FIELD: lower Wadi Ekteif, Z1 then Z2 (`private/E24b/`).** One day at a roadside site. Decides what entry 24's only feature is.
4. **The same WSRP session: I 12 (entry 4), IV 1 (entry 15), IV 3 (entry 16), VII 3 (entry 29).** Reading; marginal extra effort. Low to moderate yield.
5. **ʿAqabat Jabr South (3), ASI 109/5/62: full record and any IAA salvage reports, then FIELD for grave forms.** Low, then moderate effort. Gives entry 24 a dated rival, or removes one.
6. **Route 1 works records near Nebi Musa (1950s–70s) and full-resolution 1940s RAF verticals of the lower Wadi Ekteif.** Archive and image; moderate effort. Best done before item 3.
7. **Hachlili and Killebrew 1999, Figs. II.1–II.2, georeferenced** (owner's copy). Cheap. Places Hills F–G against Wadi Tasun and the route (24-J).
8. **The other ~30 plan-bearing ʿAtiqot 41 caves read for facing.** Cheap; in the bucket. Better entry 25 denominator. Little effect on any identification.
9. **IV/17 field file, Dadon L-656/1994.** Archive; moderate effort. The only route to a date for the IV/17 threshold (entry 25).
10. **FIELD: Twin Cave mouth bearings, northern unit and threshold.** Moderate effort; geometry only (entry 25).
11. **RAF 1945 verticals of ʿEin Samiya (MARJAMA-2).** Archive; moderate effort. Two-sided for the Kh. el-Marjama model only.
12. **Eshel and Safrai 2015 (JAJSup 18, pp. 113–129), Milik RB 66 (1959) pl. XIV, Davila 2013.** Cheap. Closes the Carmel bookkeeping and tests "373 BCE". Very small effect.

Not ranked: Zertal MHCS 4 site 194 (needs the PDF split); CIIP IV.1 nos. 3209–3214 (neutral); the Hyrcania basin inlet (blocked by the reading).

---

## Limits

- Not read by me or by the swarm: Schwartz 2021, Davila 2013, Eshel and Safrai 2015, CIIP IV.1 pp. 619–630, MHCS 4, Dinur and Feig's ʿAlmit plan, the Kenyon plate volume and the IV/17 field file. Claims about them come from the cards and repo records cited.
- I viewed no private image and no WSRP frame. Ekteif position statements come from C2-1, the HUNT note and RR6.
- These strengths are judgements from the cited records. They change nothing in `ratings.csv`, the atlas or any registered result.
