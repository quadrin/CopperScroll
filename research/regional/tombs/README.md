# Regional tomb inventory: entries 14, 24, 27, 48, 51–54 and 56

**What it is.** Every tomb record in two fixed regions, coded from the source text by frozen rules and scored against each reading branch of the scroll's tomb entries. The regions are the Jerusalem necropolis (5 km around the Temple Mount) and Jericho with the road to Qumran. The sources are 1,055 records from the online ASI survey maps, WBADB, the HA-ESI lane and Kenyon *Jericho* II, plus (11 October) the 104 tomb units of the Jericho cemetery report (IAA Reports 7).\
**Main result.** Region A has 197 tomb units that the source itself dates to the window. Any landmark clause that a survey can record matches only a handful of them: 1 nefesh, 5 columned façades or porches, 1 inner pillar, 6 named inscriptions, and no ancient garden. The tombs named Absalom (48) and "of the Queen" (27) match one exposed unit each (ASI 102/410, 102/320). No tomb is recorded as Zadok's (51) or Obed's (54). Region B's union count still has only 5 strictly dated units: the 104 Jericho cemetery tombs sit inside the cemetery row WBADB S2446, so the frozen duplicate rule leaves them out of it. Counted on their own, 25 of those tombs are dated to the window; they give 3 matches for 54-M (named family tombs A2, D1, H), 1 for 27-T (Tomb H, whose ossuary names "Queen Agrippina" as a freedman's patron), and none for 24-J or 54-P ([addendum](#addendum-11-october-2026-iaa-reports-7-and-1)).\
**What stays unknown.** Most clauses are silent in survey text, so most results are "unknown", not "fail". Two sources are blocked: Kloner and Zissu 2007 and Avigad 1954. The Jericho report gives no tomb positions, so the road clause of 24-J stays unknown for its tombs. The walled Old City has only scattered WBADB excavation rows. In the frozen rules, entrance orientation is almost never readable (see Amendment 1).

Exploratory regional count, 10–11 October 2026 (UTC). No identification claim. No registered result, outcome count, candidate confidence or atlas value changes. Labels: EVIDENCE (a source says it), INFERENCE (our reasoning), CLAIM (an author's assertion without a field record). Unknown stays unknown.

## Freeze record

- `PLAN.md` was committed alone in **cd394d7** ("Freeze tombs plan") at **2026-10-11T04:08:51Z** (UTC). Its SHA-256 is `206a4e1430da2939bdc7e66b3c540f6ed068118c94c366fb5c8073c2564b229d`.
- **Before the freeze**, no tomb record was fetched or coded. Only the WBADB column list and the IAA Reports 7 chapter list had been seen. The exposure list is in PLAN §1.
- **After the freeze**, every ASI map response was fetched (04:09:49–04:11:56Z), and every WBADB row was read.
- **Implementation fix after the first build.**
  - The frozen lenient rule (§4) also looks for "Second Temple" in a tomb sentence. The first build checked only the WBADB period field.
  - It was fixed to follow the plan. The fix changed 6 WBADB rows from no-evidence to lenient yes. No strict value changed.
- **Implementation choices made before any record was seen** (the plan is silent on them):
  - A WBADB Excavations row marked Surveyed counts as a possible duplicate, as in the Koḥlit count.
  - Kenyon units take the Tell es-Sultan point.
- **Exploratory changes made after seeing records** are in [PLAN_AMENDMENT_1_exploratory.md](PLAN_AMENDMENT_1_exploratory.md). They are reported separately below.
- **Exposure.** Each unit's `exposure` column says whether it was exposed before the freeze or first read after it:
  - 53 units were exposed: named in repo notes before the freeze, or known to me beforehand.
  - 402 ASI units had been coded by the ASI lane on 9 October.
  - Three WBADB rows (Caves V/57, VIII/28 and IX/5) summarise caves of the 2002 northern Judean Desert cave survey. That is the ʿAtiqot 41 lineage, a Tier 1 source. They were first read after this freeze.
  - No ʿAtiqot 41 entry itself, no L-656 file and no IAA Archive record was opened.

## Sources and access

Details and exact URLs: [sources_access.csv](sources_access.csv).

| Source | Region | Read | Units |
|---|---|---|---|
| ASI online maps (`survey.iaa.org.il`, the `GetPolygonsSites` service, the ASI lane's method) | | Every record of the 8 maps whose sheet touches a region | 439 tomb units |
| – Kloner, *Survey of Jerusalem*: Maps 101, 102, 105, 106 | A | | |
| – Sion: 109/4 Wadi Qelt, 109/5 Kalia | B | | |
| – Patrich: 109/7 Mar Saba | B | | |
| – Benjamin survey: 83/12 | B | | |
| WBADB (`WBADB_data1.xlsx`, hash checked) | A, B | Both sheets | 572 tomb rows; 544 are possible duplicates of ASI records |
| HA-ESI lane rows | A | Reused | 21 (6 located, all duplicates; 15 unlocated) |
| Kenyon *Jericho* II, via the repo note | B1 | Reused | 23 |
| Hachlili and Killebrew 1999 (IAA Reports 7), 11 Oct | B1 | ch. I–II, IV–VIII (see [addendum](#addendum-11-october-2026-iaa-reports-7-and-1)) | 104; all possible duplicates of WBADB S2446 |
| Avni and Greenhut 1996 (IAA Reports 1), 11 Oct, exploratory | A | ch. 1; ch. 3 Table 3.1 | 3, kept out of the frozen tables |
| Allegro 1964, via the repo extraction | A | Enrichment column only | 2 |

Coverage (`coverage.csv`, a 100 m sample grid):
- The online ASI sheets cover all of Region A, but no ASI record lies inside the Old City walls (ASI lane). WBADB adds a few excavation rows there: Mughrabi Gate, the Jewish and Armenian Quarters, and the Holy Sepulchre.
- The ASI sheets cover 51% of B1 and 62% of B2. The Map of Jericho is not online, so the rest of Region B rests on WBADB and Kenyon.
- Detection limits are as the ASI lane recorded them: Kloner's teams "were often unable to locate and record all" remains. No detection rate is known.

**Not read.**
- Hachlili and Killebrew 1999 (IAA Reports 7) and Avni and Greenhut 1996 (IAA Reports 1) were blocked on 10–11 October (HTTP 403, Cloudflare challenge, not bypassed). Both were read on 11 October from copies saved to the owner's computer; see the addendum.
- Kloner and Zissu 2007: no open copy; library only.
- Avigad 1954: no digital copy found.
- Kenyon *Jericho* I: not opened (time).
- The printed ASI volumes: the online records carry no page numbers, so record ids are the locators.

## Method

- **Sources.** One unit is a record as the source gives it. 413 units hold more than one tomb or name a cemetery (`multi_tomb_record`).
- **Coding.** Each feature is coded from the record's own English text with the frozen word lists of PLAN §5. No description text is stored; only the matched single terms are.
- **Dating.**
  - **Strict:** a window label stands in the same sentence as a tomb word.
  - **Lenient:** strict, or "Second Temple" in a tomb sentence, or a window label anywhere in the record.
  - "Partly" (Hellenistic, Roman, Second Temple) counts as unknown.
- **Duplicates.** ASI is the primary lineage in Region A and inside ASI sheets. WBADB is primary elsewhere. Other lineages within 150 m count as possible duplicates. Counts below are the union without duplicates unless stated.
- **Manual check.** Every `yes` for monument, porch, inner pillar, named inscription, garden, west-facing or a name was read once and confirmed or rejected (`data/manual_check.csv`, 80 decisions).
  - Rejections include modern park names ("Sanhedrin Garden", "Shulamit Garden", "Mormon's Garden"), columns in a kiln, cistern or quarry, and road mentions of Jericho.
  - Absalom's monument keeps F2: its relief columns make a columned façade, though not a porch.
- **Scoring.** For each unit and branch: match if every clause is yes, fail if any is no, otherwise unknown. Location clauses are unknown when the tolerance lies inside the point's uncertainty.

## Results (frozen rules)

### Feature counts (union of lineages, no duplicates)

| Region, date set | N | Above-ground monument | Columned porch or façade | Inner pillar | Inscription | Named inscription | Ancient garden | West-facing entrance | In road zone (3 km) |
|---|---|---|---|---|---|---|---|---|---|
| A, strict | 197 | 1 | 5 | 1 | 35 | 6 | 0 | 0 | 0 |
| A, lenient | 308 | 4 | 7 | 1 | 53 | 8 | 0 | 0 | 0 |
| A, any date | 444 | 7 | 7 | 1 | 59 | 8 | 0 | 0 | 0 |
| B, strict | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |
| B, lenient | 7 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 7 |
| B, any date | 42 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 38 |

Region A, strict, by distance from the Temple Mount: 15 units at 0–1 km, 73 at 1–2, 73 at 2–3 and 36 at 3–5. All 197 are ASI records.

The rare features in Region A:
- **Monument.** In the strict set the only nefesh is ASI 102/410, Absalom's Tomb, the "Herodian-period nefesh". Any date adds Bene Ḥezir and Zechariah (102/411), the Silwan Iron Age monoliths (102/420), and later mausoleums (102/345, 102/383, 102/400, 105/48).
- **Columned porch or façade.** 102/221 and 102/231 (Sanhedriyya), 102/293 (Mount Scopus), 102/320 (Tombs of the Kings) and 102/410. Lenient adds 102/162 (Umm el-ʿAmed) and 102/411.
- **Inner pillar.** 102/435 (Mount of Olives): relief columns in a passage between chambers.
- **Named inscriptions** on ossuaries or walls: 102/175, 102/245, 102/432, 102/451, 106/65, 106/76 (strict); 102/287 and 102/411 (lenient).
  - The Bene Ḥezir record says only that a Hebrew inscription attests the priestly family of Hezir. It gives no names, so "Obed" cannot be checked in this source.
- **Gardens.** 12 strict units mention a garden, all modern.

In Region B, the 5 strictly dated units are Kenyon's grave-arcosolium graves G66–68, G84 and Q1, whose pottery was matched to Qumran Period II. The cemetery that Hachlili excavated is one WBADB row, S2446 ("Very large Second Temple period cemetery", periods "Rom"). Under the strict rule that row is "partly", so unknown.

### Branch results

Each cell is "k match / f fail / m unknown of N", for the headline region and the union of lineages.

| Branch | Reading | Region | Strict | Lenient | Any date |
|---|---|---|---|---|---|
| 14-M62 | Milik: esplanade; slab over a bone pit | A | 1/190/6 of 197 (102/408) | 2/296/10 of 308 | 2/430/12 of 444 |
| 14-P06 | Puech 2006: Millo; slab | A | 0/190/7 of 197 | 1/296/11 of 308 | 1/430/13 of 444 |
| 14-NAME | ha-Melaḥ as an unlocated name ("salt", "embankment") | A∪B | 0/0/202 | 0/0/315 | 0/0/486 |
| 24-J | Jericho → Secacah road; a wadi | B | 0/0/5 of 5 | 1/0/6 of 7 (109/5/62) | 3/4/35 of 42 |
| 24-A | Allegro: eastern road; Kippa = Wadi Qumran | B | 0/5/0 of 5 | 0/7/0 of 7 | 0/41/1 of 42 |
| 27-T | the Queen's tomb | A∪B | 1/0/201 of 202 (102/320) | 1/0/314 | 1/0/485 |
| 48-Y | Absalom's monument (yad) | A | 1/0/196 of 197 (102/410) | 1/0/307 | 1/0/443 |
| 48-L | Lefkovits: the Place of Absalom | A | 1/0/196 (102/410) | 1/0/307 | 1/0/443 |
| 51-S | stoa corner; Zadok's tomb; pillar of the exedra | A | 0/190/7 | 0/296/12 | 0/430/14 |
| 51-O | Lefkovits: ossuary; Zadok; exedra pillar | A | 0/0/197 | 0/0/308 | 0/0/444 |
| 51-J | Pixner: "the Just"; stoa; exedra pillar | A | 1/190/6 (102/410) | 2/296/10 (+102/411) | 2/430/12 |
| 52-M | Milik: family plot, rock facing west, garden, slab, channel | A | 0/0/197 | 0/0/308 | 0/0/444 |
| 53-P | Puech: under the colonnades | A | 1/195/1 (102/408) | 3/303/2 | 3/437/4 |
| 53-K | rock "knife" (name only) | A | 0/0/197 | 0/0/308 | 0/0/444 |
| 54-P | Puech: tomb of the common people of Jericho | B | 0/0/5 of 5 | 2/0/5 of 7 (109/5/62, S2446) | 21/5/16 of 42 |
| 54-L | Lefkovits: sons of Obed, the Jerichoite | A∪B | 0/1/201 | 0/4/311 | 0/30/456 |
| 54-M | Milik: sons of […], the Jerichoite | A∪B | 0/1/201 | 0/4/311 | 0/30/456 |
| 54-W | Wolters: common people; ritually pure | A | 0/185/12 | 0/282/26 | 0/389/55 |
| 56-P | Puech: western burial chamber; entrance from the west; kokh | A | 0/26/171 | 0/31/277 | 0/34/410 |
| 56-M | Milik: the same with a cistern | A | 0/26/171 | 0/31/277 | 0/34/410 |
| 27-D, 52-P, 52-L, 56-L | non-funerary readings (dwelling, scarp, ruin, alley) | — | not scored | | |

Every branch result in every region and date set is in `scores_summary.csv`, which also gives the primary-lineage view, the per-clause counts and the sensitivity tolerances. The sensitivity tolerances are 1 km for the stoa corner and 5 km for the road; Region A3 is the 3 km circle.

What the matches are, and why most of them say little:
- **102/408** (14-M62, 53-P) is described as a "Herodian (?)" burial cave "on bank of Nahal Qidron", with a repository.
  - Its ASI point lies on the line of the Temple Mount's east wall: it shares its easting with 102/409, and its northing differs by 90 m.
  - INFERENCE: the point is placed approximately. The cave is in the valley below, outside the enclosure, so the 53-P match is an artefact of the circle tolerance.
- **102/410 and 102/320** (48, 27, 51-J) are exposed.
  - Their names, Absalom and Queen Helene, are traditional identifications that the records date to no ancient source.
  - The 51-J match rests on the relief columns of Absalom's monument, which is a nefesh, not an exedra.
- **The lenient additions** include tombs that the records date outside the window: 102/409 (Byzantine tombs at a site with Hasmonean houses) and WBADB E613 (a Mamluk tomb at the Mughrabi Gate). They enter because the lenient rule picks up a window label anywhere in the record.
- **Entry 24.**
  - Any-date matches are St George's and the Choziba cells (109/4/7–8, Byzantine monastic burials) and 109/5/62. The last is ʿAqabat Jabr South (3), "hundreds of graves" in a local streambed, with Hellenistic (Hasmonean), Roman and modern pottery but no stated date for the graves.
  - With the 5 km corridor, ASI 109/7/19 (a dam in Wadi Khashna with eight stone-capped mounds, "graves?") and WBADB **E508 "Wadi Ekteif"** (Milik's Wadi Kuteif) also match. That row holds four pit tombs with glass beads, dated Early Islamic. Under the 3 km rule it fails, 3.2 km from the road line.
  - Allegro's branch (24-A) fails everywhere except Kh. Qumran (E754), whose cemetery row has no wadi word.
- **54-P** any-date matches are cemeteries and graves at Jericho: Kenyon's graves, the ʿAqabat Jabr cemeteries and WBADB S2446. They match because "graves" or "cemetery" is coded as communal (an INFERENCE rule) and the place is Jericho.
- **56-P and 56-M** never match under the frozen rules, because no entrance orientation can be read (next section).

## Exploratory results (Amendment 1)

Written after the frozen build was inspected; see [the amendment](PLAN_AMENDMENT_1_exploratory.md). It adds the ASI direction capitals ("W-facing", "faces E"), pillars standing in a tomb entrance, and WBADB "Rom1" as Early Roman. All 127 new values were checked by hand (`data/manual_check_amendment1.csv`).

- **West-facing entrance.** In Region A, strict set: 24 units yes, 32 no, 141 unknown. Any date: 42 yes, 55 no.
- **Exedra-like pillar** (porch or entrance pillar, F2xa): 9 units in Region A, strict. The new ones are 105/95, 106/42, 106/54 and 106/55.
- **56-P** (multi-chamber, west entrance, kokhim): **10 match**, 56 fail, 131 unknown of 197. The matches are 102/142, 102/145, 102/172, 102/175, 102/184, 102/221, 102/247, 102/262, 106/7 and 106/50. Some of them hold more than one cave with different orientations (102/175, 102/221, 106/50). **56-M** (cistern instead of kokh): 0 match, 56 fail.
- **52-M**: 0 match, 32 fail. Its garden clause is never met.
- **52-P proxy** (west-facing and a slab; the scarp itself is not a tomb): 9 of 197.
- **51-S, 51-O, 51-J**: unchanged. No tomb is named Zadok, and in the strict set the only exedra-type unit within 0.5 km of the south wall is Absalom's monument.
- **"Strict+Rom1"** adds 6 WBADB rows in Region A (N = 203). It changes no match.

INFERENCE: west-facing chamber tombs are common: 24 of the 56 oriented strict units (43%). Clauses about a western entrance or a west-facing rock do little to narrow the field; the name and garden clauses do the narrowing, and no survey record meets them.

## Enrichment from the repo's Kidron work (exploratory, not scored)

`enrich_A64` attaches Allegro 1964's dig at Zechariah to ASI 102/411 (pp. 105–112, Fig. 15, Pl. 32):
- a courtyard, a conduit, and a chamber cut into the pedestal;
- the unfinished tomb to the south, with roughly hewn pillars, a collapsed porch and a slab being cut round.

Allegro's "Zadok" name and his reading of the courtyard as Zadok's garden are excluded under the circularity rule. Fig. 15 (after Avigad 1954) marks a cistern west of Absalom's monument.

With the enrichment, no branch result changes. 51-S still lacks a recorded Zadok name. 54-W still fails because Bene Ḥezir is a family chamber tomb.

## Known limits (measured)

- **Sentence splitting.**
  - "Nahal Qidron. attributed to the Hasmonean period." splits the date from the tomb, so Bene Ḥezir (102/411) is not strictly dated.
  - Abbreviation full stops split other sentences, as in the ASI lane.
- **WBADB period codes.** WBADB uses abbreviations (Rom1, Rom2, Byz, EIs). The frozen lists know none of them, so no WBADB row is strictly dated. Rows with only Byz or EIs are "unknown" instead of "no".
- **HA-ESI dating.** HA-ESI rows keep that lane's dating, which counts "Second Temple period" as in the window. All six located rows are duplicates, so this changes no count.
- **Under-recording in the survey text.** For example, the ASI record of Jason's Tomb (102/379) mentions courtyards, chambers, paintings and inscriptions, but no pyramid and no porch column. Their absence from the text is not evidence of absence. INFERENCE from background knowledge, not checked in a source here.
- **Points.** ASI points can be approximate (102/408). Kenyon tombs have no grid value.
- **Eligibility.** A record qualifies on any tomb word, so monastic sites with burials (109/4/7) and multi-feature records enter as tomb units.

## Addendum, 11 October 2026: IAA Reports 7 and 1

Source HK (Hachlili and Killebrew 1999, IAA Reports 7) is in the frozen source list, so its tombs are coded and scored under the frozen plan. The Akeldama report (Avni and Greenhut 1996, IAA Reports 1) is not, so it is an exploratory addition. No identification claim; no registered result changes.

### Record

- [PLAN_AMENDMENT_2_exploratory.md](PLAN_AMENDMENT_2_exploratory.md) was committed alone in **cd706b0** at 2026-10-11T13:00:00Z (UTC). Its SHA-256 is `e6712b1611a9ff91f89e61fb86d875633ff181d720a07b03d2374b8bb3a1f412`. It was written before any tomb description in either report was read. Part A fixes how HK is coded (the frozen plan lists HK but does not say how). Part B makes Akeldama exploratory.
- Both PDFs on the owner's computer match the hashes given by the integrator: IAA Reports 7 `7c6e6208…a2efb7` (209 PDF pages), IAA Reports 1 `f23c881e…e1d5` (140 PDF pages). Both are page scans without a text layer. OCR (tesseract 4.1.1, English, 300 dpi) ran on the owner's computer; the text stayed outside the repo. Printed page = PDF page − 7 (Reports 7) and − 11 (Reports 1).
- Two readings were checked by eye on cropped strips kept in the scratch folder: "16 km" on p. 166, and the tomb column of Table II.5.
- **Choices made after records were read** (exploratory, logged here):
  1. After the first coding pass, phrases that used a feature word in another sense were reworded. "No ossuaries or coffins" (D3, F4, F7) became "no burial containers", because the frozen coder has no negation. "Grave goods" (Tomb H) and "grave marker" (the nefesh) became "finds" and "marker on a tomb", because the communal rule reads "grave" as a grave field. This removed 3 false ossuary codes and 1 false communal code.
  2. Dating uses the type lists of the classification text (p. 59) and the dates of ch. VII (p. 165). Table II.5 also prints Type III beside C3, C4, C9b, C10 and B1, and the catalogue labels D13 Type III. These are kept in `data/hk_units.csv` (`note`) but not used; they would add up to five strictly dated tombs (B1 conflicts with the text, which gives the type to B2).
  3. A statement about a whole hill was applied to its tombs only where it holds for every tomb: Hill A ("the entrances of all the tombs faced north", p. 5), Hill B (the two excavated tombs, p. 9) and Hill F (entrances facing south, p. 51). "Most of the tomb entrances faced east" on Hill D (p. 12) was not applied.
  4. D20 and D24 are units because the report's Hill D total of 27 implies them, though its text never names them.

### What IAA Reports 7 gives, tomb by tomb

EVIDENCE from the report; codes by the frozen word lists, checked by hand where PLAN §5 asks (`data/manual_check.csv`).

- **Units.** 104: the 103 numbered tombs of Table II.1 (Hills A 7, B 4, C 32, D 27, E 12, F 7, G 9, H 5) and the stone nefesh found out of context on Hill D (p. 162, Fig. VI.2).
- **Position.** The report gives no grid reference for any tomb. Fig. I.1 is a regional map; Figs. II.1–II.2 place the tombs within their hills. All units therefore take the point of WBADB S2446 (the cemetery row), with ±16 km: the report speaks of "the boundaries of the 16 km long Second Temple period cemetery" (p. 166). INFERENCE: probably a misprint for 1.6 km, since the report bounds the cemetery between Hill H and Wadi Quruntul (pp. 2, 166). The 1.6 km value is run as an exploratory sensitivity.
- **Duplicates.** All 104 units lie at the S2446 point, so the frozen rule flags each as `possible_duplicate_of = WBADB S2446`. `linked_to` names S2446 and E349. The report names no tomb that Kenyon dug; it says Kenyon's tombs lie further north (p. 166).
- **Dating.** 25 units are strictly in the window. Type I, wooden coffins, "first century BCE, perhaps continuing into the early first century CE" (p. 165): D2, D6, D8, D9, D10, D11, D12, D14, D15, D16, D18, D22, D27. Type II, collected bones, and Type III, ossuaries, "early first century CE until" 68 CE: D3, D21, D23, F4, F7 and A1, A2, A6, B2, D1, D17, H. F5 is Early Bronze III (no). The other 78, mostly robbed or only surveyed, have no date of their own.
- **Features.**
  - Above-ground monument: only the undated nefesh fragment. The "nefesh columns" in Tomb F4 are a charcoal drawing on its wall (Fig. VI.1); rejected.
  - Columned porch, exedra pillar, inner pillar: none. Tomb H's entrance has a masonry lintel and doorjambs (p. 37).
  - Named inscriptions: 3 tombs. A2: Yehosef (Inscr. 18, p. 158). D1: Ishma'el son of Shim'on son of Palta, Pelatya and Simon, two of them "from Jerusalem" (Inscr. 15–17, pp. 155–158). H: thirteen personal names of the "Goliath" family, among them Yeho'ezer son of Ele'azar, and Theodotos, "freedman of Queen Agrippina" (Inscr. 1–14, pp. 142–155). No Obed, Zadok or Absalom.
  - Ancient garden: none.
  - Entrance direction: 27 tombs, none westerly (north 8, east 12, south 7). The report found "no particular orientation of the tomb entrances" (p. 51).
  - Kokhim 79; bone repository 2 (D27, H); channel 1 (the small channel feeding Tomb H's miqveh, p. 47); closing stones or slabs 17; wadi setting 16 (Hills F and G, beside Wadi Tasun); more than one chamber 1 (H).

### Region B branches, old and new

Each cell is "k match / f fail / m unknown of N", Region B. "Frozen union" is the headline view of PLAN §3 (no duplicates). The last two columns are exploratory (Amendment 2, Part C, chosen after the coding).

| Branch | Date set | Frozen union, 10 Oct | Frozen union, 11 Oct | IAA Reports 7 tombs alone (lineage view) | Union, tombs in place of S2446 and E349, ±16 km | The same, ±1.6 km |
|---|---|---|---|---|---|---|
| 24-J | strict | 0/0/5 of 5 | 0/0/5 of 5 | 0/0/25 of 25 | 0/0/30 of 30 | 2/0/28 of 30 (F4, F7) |
| 24-J | any | 3/4/35 of 42 | 3/4/35 of 42 | 0/0/104 of 104 | 3/4/138 of 145 | 19/4/122 of 145 |
| 24-A | strict | 0/5/0 of 5 | 0/5/0 of 5 | 0/0/25 of 25 | 0/5/25 of 30 | 0/30/0 of 30 |
| 24-A | any | 0/41/1 of 42 | 0/41/1 of 42 | 0/0/104 of 104 | 0/40/105 of 145 | 0/144/1 of 145 |
| 54-P | strict | 0/0/5 of 5 | 0/0/5 of 5 | 0/24/1 of 25 | 0/24/6 of 30 | 0/24/6 of 30 |
| 54-P | any | 21/5/16 of 42 | 21/5/16 of 42 | 0/79/25 of 104 | 20/84/41 of 145 | 20/84/41 of 145 |
| 27-T | strict | 0/0/5 of 5 | 0/0/5 of 5 | 1/0/24 of 25 (H) | 1/0/29 of 30 (H) | 1/0/29 of 30 (H) |
| 54-L | strict | 0/0/5 of 5 | 0/0/5 of 5 | 0/0/25 of 25 | 0/0/30 of 30 | 0/0/30 of 30 |
| 54-L | any | 0/24/18 of 42 | 0/24/18 of 42 | 0/0/104 of 104 | 0/23/122 of 145 | 0/23/122 of 145 |
| 54-M | strict | 0/0/5 of 5 | 0/0/5 of 5 | 3/0/22 of 25 (A2, D1, H) | 3/0/27 of 30 (A2, D1, H) | 3/0/27 of 30 |
| 54-M | any | 0/24/18 of 42 | 0/24/18 of 42 | 3/0/101 of 104 | 3/23/119 of 145 | 3/23/119 of 145 |
| 14-NAME | any | 0/0/42 of 42 | 0/0/42 of 42 | 0/0/104 of 104 | 0/0/145 of 145 | 0/0/145 of 145 |

- **The frozen counts do not change.** No cell of the 10 October `scores_summary.csv` or `features_summary.csv` changed; the new rows are the `lineage_HK` view. The Region A and A∪B headlines are unchanged as well.
- **24-J** (tomb in a wadi on the way from Jericho to Secacah). At ±16 km the road clause is unknown for every Jericho tomb. At ±1.6 km the 16 tombs of Hills F and G match, F4 and F7 strictly. INFERENCE: they match because the 3 km road zone reaches round the palaces end of the road line; Wadi Tasun runs below the Quruntul monastery, north-west of the town, away from the direction of Qumran.
- **54-P** (tomb of the common people of Jericho). The report's tombs are family loculi tombs, so the communal clause fails for 24 of the 25 dated ones. The earlier lenient match of S2446 came from the word "cemetery" in that row.
- **54-M** (sons of […], the Jerichoite). Three family tombs at Jericho carry named inscriptions: A2, D1 and H. All are exposed (PLAN §1). D1's family is "from Jerusalem" by its own inscriptions (Inscr. 15a, 16). **54-L**: no Obed.
- **27-T** (the queen's tomb). Tomb H matches on the name clause only. The queen is Agrippina, named as the patron of a freedman buried there; the tomb is not hers. It was exposed before reading (background knowledge, listed in Amendment 2).
- Other branches in Region B (lineage view, strict): 52-M 0/17/8 and 56-P 0/18/7 (no west-facing entrance); 14-M62, 14-P06, 51-S, 51-J and 53-P fail on location; 48-Y, 48-L and 51-O stay unknown.

### Akeldama (exploratory, Amendment 2 Part B)

- **Coded.** Three caves (pp. 1–32): rock-cut caves of 4, 3 and 4 chambers with loculi, arcosolia with burial troughs, repositories and stone doors; 8, 16 and 16 ossuaries. Caves 2 and 3 have named ossuary inscriptions (Table 3.1, p. 69). All three are dated to the first century CE (strict), with Late Roman and Byzantine reuse. Units and decisions: `amendment2_akeldama_units.csv`, `data/manual_check_amendment2.csv`.
- **Position.** The report gives no grid. The text of ASI 102/484 names these caves (excavated by Avni and Greenhut, 1989), so they take its point (±0.05 km). The ASI map reference given for them lies 54 m away.
- **Result.** All three caves lie within 0.15 km of ASI 102/484, so under the frozen duplicate rule **no Region A count changes**, and the frozen Region A headline stands.
- **If they were counted as new units** (exploratory): Region A strict N goes from 197 to 200. No branch gains a match. 14-M62, 14-P06, 24-J, 24-A, 51-S, 51-J, 53-P, 54-P and 54-W each gain 3 fails; 52-M, 56-P and 56-M gain 1 fail (Cave 3 is entered from the south-east). Named inscriptions in Region A would go from 6 to 8, inner pillars from 1 to 2 (Cave 3's relief pilasters, accepted as for 102/435).
- Hand decisions: Cave 3's "Helene" is a woman buried there, not the queen of Adiabene, so 27-T stays unknown. Cave 1 (entrance in the courtyard's south-west wall) and Cave 2 ("faced northwest") were not accepted as west-facing: both open from their shared courtyard (INFERENCE from p. 2).

### Gaps

- No Jericho tomb has a grid position; all share one point at ±16 km.
- 78 of the 104 units have no date of their own, including all of robbed Hill C.
- The excavators "could examine only a small part of this extensive area" (p. 3). The detection rate is unknown.
- Not read: the rotated Table II.2 (p. 52); the figures themselves (plans are cited only); Akeldama ch. 2 and the full inscription entries of ch. 3.
- Names and numbers come from OCR text. Only "16 km" and the Table II.5 tomb column were checked by eye.
- The introduction (p. 4) says 14 tombs on Hill G were excavated; ch. II (p. 34) and Table II.1 give 9. Nine are coded.

### Figures

IAA Reports are under IAA copyright, so no page image is committed. [data/iaa_reports_figures.csv](data/iaa_reports_figures.csv) lists the maps, plans and tables met (pages, PDF pages, use). Retrieval: the portal pages https://publications.iaa.org.il/iaareports/69 and /74, or the owner's copies under `~/Downloads/IAA portal volumes/` (hashes in `sources_access.csv`).

## IAA inventory view, 11 October 2026 (exploratory)

**What changed.** The merged IAA inventory (`research/regional/haesi_features/merged_2026-10-11/`, commit cf60d97) replaces the 21 phase-1 HA-ESI units, none of which was counted. It adds 78 non-duplicate tomb units: 77 in Region A and 1 in Region B, at 50 distinct merged sites. Region A strict N goes from 197 to 226. No branch gains a match in the strict or lenient date sets. The frozen tables and headline above are unchanged. This is a source extension made after the results were seen, so it is exploratory.

- **Rules.** [PLAN_AMENDMENT_IAA_2026-10-11.md](PLAN_AMENDMENT_IAA_2026-10-11.md) was committed alone as `c14468e` (2026-10-11T17:52:31Z), before any IAA row was mapped. SHA-256 `980a020b4057c447f5127ab60fc1b25f69f27160623414b9183e04300fd1aad0`.
- **How the units were coded.** The frozen `Coder`, `clause_value` and duplicate rule were used unchanged. The frozen units are scored from their committed codes in `tombs.csv`. The script checks that this reproduces every cell of `scores_summary.csv` (views `all_lineages` and `primary`) and of `amendment1_scores_summary.csv`.
- **Units.** 228 IAA tomb units have coordinates and lie in a region (preferred report versions). 150 of them lie within 0.15 km of an ASI or WBADB primary record, so they are possible duplicates under the frozen rule. 78 are new. Hand checks: 5 frozen-code yeses and 5 Amendment 1 orientations ([data/manual_check_iaa.csv](data/manual_check_iaa.csv), [data/manual_check_iaa_amendment1.csv](data/manual_check_iaa_amendment1.csv)).

**k match / f fail / m unknown, of N**, headline region, union of lineages without duplicates (frozen → with the IAA units):

| Branch | Region | Strict | Lenient | Any date |
|---|---|---|---|---|
| 14-M62 | A | 1/190/6 of 197 → 1/218/7 of 226 | 2/296/10 of 308 → 2/325/11 of 338 | 2/430/12 of 444 → 2/502/17 of 521 |
| 14-P06 | A | 0/190/7 of 197 → 0/218/8 of 226 | 1/296/11 of 308 → 1/325/12 of 338 | 1/430/13 of 444 → 2/502/17 of 521 |
| 14-NAME | A∪B | 0/0/202 of 202 → 0/0/231 of 231 | 0/0/315 of 315 → 0/0/345 of 345 | 0/0/486 of 486 → 0/0/564 of 564 |
| 24-J | B | 0/0/5 of 5 → unchanged | 1/0/6 of 7 → unchanged | 3/4/35 of 42 → 3/5/35 of 43 |
| 24-A | B | 0/5/0 of 5 → unchanged | 0/7/0 of 7 → unchanged | 0/41/1 of 42 → 0/42/1 of 43 |
| 27-T | A∪B | 1/0/201 of 202 → 1/0/230 of 231 | 1/0/314 of 315 → 1/0/344 of 345 | 1/0/485 of 486 → 1/0/563 of 564 |
| 48-Y, 48-L | A | 1/0/196 of 197 → 1/0/225 of 226 | 1/0/307 of 308 → 1/0/337 of 338 | 1/0/443 of 444 → 1/0/520 of 521 |
| 51-S | A | 0/190/7 of 197 → 0/218/8 of 226 | 0/296/12 of 308 → 0/325/13 of 338 | 0/430/14 of 444 → 0/502/19 of 521 |
| 51-O | A | 0/0/197 of 197 → 0/0/226 of 226 | 0/0/308 of 308 → 0/0/338 of 338 | 0/0/444 of 444 → 0/0/521 of 521 |
| 51-J | A | 1/190/6 of 197 → 1/218/7 of 226 | 2/296/10 of 308 → 2/325/11 of 338 | 2/430/12 of 444 → 2/502/17 of 521 |
| 52-M | A | 0/0/197 of 197 → 0/0/226 of 226 | 0/0/308 of 308 → 0/0/338 of 338 | 0/0/444 of 444 → 0/2/519 of 521 |
| 53-P | A | 1/195/1 of 197 → 1/224/1 of 226 | 3/303/2 of 308 → 3/333/2 of 338 | 3/437/4 of 444 → 5/510/6 of 521 |
| 53-K | A | 0/0/197 of 197 → 0/0/226 of 226 | 0/0/308 of 308 → 0/0/338 of 338 | 0/0/444 of 444 → 0/0/521 of 521 |
| 54-P | B | 0/0/5 of 5 → unchanged | 2/0/5 of 7 → unchanged | 21/5/16 of 42 → 21/6/16 of 43 |
| 54-L, 54-M | A∪B | 0/1/201 of 202 → 0/1/230 of 231 | 0/4/311 of 315 → 0/4/341 of 345 | 0/30/456 of 486 → 0/30/534 of 564 |
| 54-W | A | 0/185/12 of 197 → 0/207/19 of 226 | 0/282/26 of 308 → 0/305/33 of 338 | 0/389/55 of 444 → 0/444/77 of 521 |
| 56-P, 56-M | A | 0/26/171 of 197 → 0/26/200 of 226 | 0/31/277 of 308 → 0/31/307 of 338 | 0/34/410 of 444 → 0/36/485 of 521 |

Every region, date set and sensitivity is in [iaa_view_2026-10-11.csv](iaa_view_2026-10-11.csv). That file also has the IAA units alone (`iaa_*`) and the "other classes" sensitivity, which adds 24 non-duplicate units of other classes that pass the TOMB-term test and changes no match.

**What drives the change.**
- **The 29 new strictly dated units in Region A.** The largest groups are at Bayit va-Gan (Yosef Hakhami St.), the Mount of Olives, Binyene Ha-Umma and ʿEin el-Lauza. By the frozen word lists they carry kokhim (17), slabs or closing stones (11), ossuaries (7), more than one chamber (5) and repositories (3).
- **No new unit has a monument, a columned porch, an inner pillar, an inscription, a garden or an oriented entrance.** So the new units add fails to the location branches (14, 51-S, 51-J, 53-P) and unknowns elsewhere. No new unit names Zadok, Absalom, Obed or a queen.
- **New matches with any date only:**
  - 14-P06 gains a 13th-century cist grave sealed with slabs at the Western Wall Plaza (HA-ESI 121).
  - 53-P gains a Mamluk grave at the Ha-Maʿaraviyim (Mughrabi) Gate, coded twice (HA 104, ESI 16; see below).
  - All of these are dated outside the window.
- **IAA units alone.** In the lineage view, 53-P gains one strict match: a burial cave at Naḥal Ha-Egoz (HA-ESI 117). Its coded point lies 190 m from the Temple Mount point, but the report puts the cave in the Mount Scopus cemetery. INFERENCE: a position error, as for ASI 102/408. The unit is a duplicate of ASI 102/409, so it does not enter the union.
- **Amendment 1 (exploratory)** ([iaa_amendment1_view.csv](iaa_amendment1_view.csv)). No match changes. 56-P stays at 10 matches, now of 226 (strict), and the 52-P proxy stays at 9. No new strictly dated unit has an entrance orientation. Three strictly dated IAA units do: Reḥavya (north-west), Nisan Beck St. (west) and the Shuʿfat survey (south). All three are duplicates of ASI records (102/380, 102/227 and 102/102).
- **A columned façade the rules miss.** Arzei Ha-Bira (HA-ESI, Second Temple period) has a façade "with engaged pillars". The frozen sentence split at "c." separates the pillars from the word façade, so neither F2 nor F2xa fires, and F3 was rejected by hand. It lies 1.65 km from the Temple Mount, so no branch would change.
- **A class-name artefact.** The coded text includes the class name ("tomb burial cave"), as the frozen HAESI rule did. So every IAA unit carries the family-type term "burial cave". For 4 of the 29 new strict units this changes the communal code: 2 fail on 54-W only because of it, and 2 would otherwise be communal.

**New match worth a closer look:** none.

**Gaps.**
- 165 IAA tomb rows in the Jerusalem hills, 23 in the Judean Desert and 4 in the Jordan Valley have no coordinates. The frozen rule does not count them. Among them is HA 28's kokhim cave on Shmuel ha-Navi St. (a Tier 1 record, extracted by phase 3).
- Two Hebrew–English pairs were not joined by the merged inventory: Ben-Zvi Boulevard (HA 99, ESI 12; same point, strictly dated) and the Ha-Maʿaraviyim Gate (HA 104, ESI 16). The union's strict N is therefore probably one too high. This is reported to the merge lane.
- Under the frozen rule, IAA units at one place are not deduplicated among themselves.
- No IAA tomb unit falls in Region B's strict set. Jericho's tombs still rest on Kenyon and IAA Reports 7.

Files: [iaa_units.csv](iaa_units.csv) (276 units with codes, duplicate flags and Amendment 1 codes; no text), [iaa_scores.csv](iaa_scores.csv), [iaa_view_2026-10-11.csv](iaa_view_2026-10-11.csv), [iaa_amendment1_view.csv](iaa_amendment1_view.csv), [iaa_summary.json](iaa_summary.json), [scripts/iaa_view.py](scripts/iaa_view.py), [tests/test_iaa_view.py](tests/test_iaa_view.py).
- Rebuild: `python3 -I -B research/regional/tombs/scripts/iaa_view.py`. It needs no ASI cache or WBADB file.

## Phase-4 inventory view, 12 October 2026 (exploratory)

**What changed.** The merged inventory over phases 1–4 (`research/regional/haesi_features/merged_2026-10-12/`, commit b4a41cc) replaces the phase 1–3 inventory of the 11 October view. Phase 4 adds ʿAtiqot 42–121, IAA Reports, QDAP, SWP, Guérin and ADAJ. The phase-4 rows give 31 phase-4 tomb units with coordinates in the regions. 18 lie within 0.15 km of an ASI record, and 13 are new. All 13 are in Region A. Region A strict N goes from 226 to 230. No branch gains or loses a match in any region, date set or sensitivity. The frozen tables and headline, Amendments 1 and 2 and the 11 October view files are unchanged.

- **Rules.** [PLAN_AMENDMENT_PHASE4_2026-10-12.md](PLAN_AMENDMENT_PHASE4_2026-10-12.md) was committed alone as `d5a837e` (2026-10-12T04:49:52Z), before any phase-4 tomb row was read. SHA-256 `f9b0ad579e2e551b04708aaa825c828b98c2fae7a82f49b95f953cc40875b9bc`. It applies the IAA amendment's method unchanged.
- **Exposure before the freeze.** The amendment's §1 lists headers, value counts and the two READMEs. One phase-4 tomb report was exposed by name and dating: ʿAtiqot 113 (Mount Scopus chalk quarry, ATQ113-i09), which the merge README lists as moving from undated to in-window.
- B3 refresh (12 Oct): the view was rerun, rules unchanged, on `merged_2026-10-12` as rebuilt under its amendment B3, which adds the Manaḥat miqveh and the Efrata storage cave (IAA Reports chapters). Neither is a tomb row. The Efrata cave passes the TOMB-term test of the other-classes sensitivity but lies outside the regions, so it is only a coverage count ("outside the regions" 53 → 54 in `phase4_summary.json`). No unit, score, view value or match changed, and no new hand check arose. The script and summary now pin the B3 input hashes. Nothing changed in substance.
- **Checks.** The script rebuilds the 11 October view from `merged_2026-10-11` and checks it against `iaa_view_2026-10-11.csv` and `iaa_amendment1_view.csv` cell by cell. It also checks the frozen units against `scores_summary.csv`. Hand checks: 4 frozen-code yeses ([data/manual_check_phase4.csv](data/manual_check_phase4.csv)) and 1 Amendment 1 orientation ([data/manual_check_phase4_amendment1.csv](data/manual_check_phase4_amendment1.csv)). Earlier decisions for the same phase 1–3 rows were reused.

**Units.**
- 244 IAA tomb units have coordinates and lie in a region, against 228 on 11 October.
- 31 come from phase-4 rows. 18 of them are possible duplicates of ASI records (102/93, 102/231, 102/345, 102/374, 102/402, 102/435, 102/439, 102/484, 105/22, 106/68). 13 are new.
- 15 phase 1–3 units dropped out. In each case a phase-4 ʿAtiqot report joined the unit's report group and became the preferred version, so the version rule now takes the ʿAtiqot rows.
  - 14 are replaced by ʿAtiqot units of the same excavation (Arnona, Naḥal Qidron, ʿEin el-Luza, Kh. Kaʿkul, Naḥalat Aḥim, Pisgat Zeʾev E, Mount Scopus East, Abu Ṭor, the Mount of Olives, Givʿat Gonen, Sanhedriyya / Tel Arza).
  - Sallah ed-Din Street lost its point: the preferred ʿAtiqot 80 version is placed by name only. It was a duplicate of ASI 102/332, dated outside the window, so no count moves.
- Non-duplicate units: 78 → 85, at 54 distinct merged sites.

**k match / f fail / m unknown, of N**, headline region, union of lineages without duplicates (11 October view → 12 October view; the frozen values are in the table of the previous section):

| Branch | Region | Strict | Lenient | Any date |
|---|---|---|---|---|
| 14-M62 | A | 1/218/7 of 226 → 1/222/7 of 230 | 2/325/11 of 338 → 2/330/11 of 343 | 2/502/17 of 521 → 2/509/17 of 528 |
| 14-P06 | A | 0/218/8 of 226 → 0/222/8 of 230 | 1/325/12 of 338 → 1/330/12 of 343 | 2/502/17 of 521 → 2/509/17 of 528 |
| 14-NAME | A∪B | 0/0/231 of 231 → 0/0/235 of 235 | 0/0/345 of 345 → 0/0/350 of 350 | 0/0/564 of 564 → 0/0/571 of 571 |
| 24-J | B | 0/0/5 of 5 → unchanged | 1/0/6 of 7 → unchanged | 3/5/35 of 43 → unchanged |
| 24-A | B | 0/5/0 of 5 → unchanged | 0/7/0 of 7 → unchanged | 0/42/1 of 43 → unchanged |
| 27-T | A∪B | 1/0/230 of 231 → 1/0/234 of 235 | 1/0/344 of 345 → 1/0/349 of 350 | 1/0/563 of 564 → 1/0/570 of 571 |
| 48-Y, 48-L | A | 1/0/225 of 226 → 1/0/229 of 230 | 1/0/337 of 338 → 1/0/342 of 343 | 1/0/520 of 521 → 1/0/527 of 528 |
| 51-S | A | 0/218/8 of 226 → 0/222/8 of 230 | 0/325/13 of 338 → 0/330/13 of 343 | 0/502/19 of 521 → 0/509/19 of 528 |
| 51-O | A | 0/0/226 of 226 → 0/0/230 of 230 | 0/0/338 of 338 → 0/0/343 of 343 | 0/0/521 of 521 → 0/0/528 of 528 |
| 51-J | A | 1/218/7 of 226 → 1/222/7 of 230 | 2/325/11 of 338 → 2/330/11 of 343 | 2/502/17 of 521 → 2/509/17 of 528 |
| 52-M | A | 0/0/226 of 226 → 0/0/230 of 230 | 0/0/338 of 338 → 0/0/343 of 343 | 0/2/519 of 521 → 0/3/525 of 528 |
| 53-P | A | 1/224/1 of 226 → 1/228/1 of 230 | 3/333/2 of 338 → 3/338/2 of 343 | 5/510/6 of 521 → 5/517/6 of 528 |
| 53-K | A | 0/0/226 of 226 → 0/0/230 of 230 | 0/0/338 of 338 → 0/0/343 of 343 | 0/0/521 of 521 → 0/0/528 of 528 |
| 54-P | B | 0/0/5 of 5 → unchanged | 2/0/5 of 7 → unchanged | 21/6/16 of 43 → unchanged |
| 54-L, 54-M | A∪B | 0/1/230 of 231 → 0/1/234 of 235 | 0/4/341 of 345 → 0/4/346 of 350 | 0/30/534 of 564 → 0/30/541 of 571 |
| 54-W | A | 0/207/19 of 226 → 0/210/20 of 230 | 0/305/33 of 338 → 0/309/34 of 343 | 0/444/77 of 521 → 0/449/79 of 528 |
| 56-P, 56-M | A | 0/26/200 of 226 → 0/26/204 of 230 | 0/31/307 of 338 → 0/31/312 of 343 | 0/36/485 of 521 → 0/37/491 of 528 |

Every region, date set and sensitivity, the IAA units alone and the other-classes sensitivity (27 non-duplicate units) are in [phase4_view_2026-10-12.csv](phase4_view_2026-10-12.csv). None of them changes a match. Amendment 1 ([phase4_amendment1_view.csv](phase4_amendment1_view.csv)) changes no match either: 56-P stays at 10 and the 52-P proxy at 9 (strict, now of 230). No phase-4 unit has an oriented entrance under Amendment 1.

**What is new, by level** (non-duplicate units; strict / lenient / any date, all in Region A):
- **Rows:** 13 units from phase-4 rows (6 / 7 / 13).
- **Reports:** 1 unit whose report group has no phase 1–3 report (0 / 0 / 1): the Hulda / St Pelagia shrine on the Mount of Olives (ʿAtiqot 42, p. 228), dated outside the window.
- **Sites:** 5 units at sites with no phase 1–3 row (2 / 2 / 5). Counting duplicates too: 31 rows, 10 report units and 10 site units (14 / 4 / 4 strict).
- **The 6 new strictly dated units:**

| Unit | Source unit id | Printed page | Place | Codes |
|---|---|---|---|---|
| P0270 | ATQ54-001 | ʿAtiqot 54, pp. 1–73 | Kh. Kaʿkul (Pisgat Zeʾev H) | kokhim |
| P0275 | ATQ42-i27 | ʿAtiqot 42, pp. 3*–8* (Hebrew) | Abu Ṭor, two burial caves | none |
| P0277 | ATQ69-069s | ʿAtiqot 69, p. 161 (English summary) | near the Kathisma, Hebron Road | kokhim |
| P0288 | ATQ113-i09 | ʿAtiqot 113, from p. [185] (pp. 187–265 seen by the reader) | Mount Scopus chalk quarry (exposed, see above) | kokhim |
| P0293 | ATQ59-021s | ʿAtiqot 59, pp. 21*–35* | ʿEin el-Luza | none |
| P0294 | ATQ63-027 | ʿAtiqot 63, pp. 27–43 | southern slope of Mount Scopus | kokhim |

Three of them replace phase 1–3 units of the same excavation that were already counted: Kaʿkul, ʿEin el-Luza and Abu Ṭor. Abu Ṭor's other cave (P0276) is now a duplicate of ASI 102/484. Net, Region A strict N rises by 4.

**Which phase-4 units meet a clause** (all 31, duplicates included; ids in [phase4_scores.csv](phase4_scores.csv)):
- **14-M62, 14-P06.** Repository (F13): Wadi el-Ḥalaf (ʿAtiqot 48), Arnona (ʿAtiqot 54, p. 154) and the Mount of Olives (ʿAtiqot 49). Slab (F14): the Late Iron Age tomb on Mount Zion (ʿAtiqot 98) and Naḥalat Aḥim (ʿAtiqot 54). All five are duplicates of ASI records. All fail L_millo.
- **The nearest unit to the south wall** is the pair of rock-cut caves with Greek inscriptions (ʿAtiqot 78, pp. 13–24), 0.42 km from the Temple Mount point. It is unknown on L_millo, L_south_corner and L_temple, because the tolerance lies inside its position uncertainty. It is dated outside the window and is a duplicate of ASI 102/345.
- **24-J, 24-A, 54-P.** No phase-4 tomb unit has coordinates in Region B.
- **27-T, 48-L, 51-O, 54-L.** No phase-4 unit, located or not, names a queen, Absalom, Zadok or Obed.
- **48-Y.** F1 holds for the built tomb in the Hulda shrine crypt (ʿAtiqot 42, p. 228). It has no Absalom name and is dated outside the window.
- **51-S, 51-J.** The Tel Arza monumental cave (ATQ106-161, ʿAtiqot 106, pp. 161–176) has a distyle in antis façade, dated from Herod to 70 CE, so F2x holds. It fails L_south_corner (2.5 km). It is a duplicate of ASI 102/231 (Sanhedriyya), whose façade the frozen count already holds.
- **52-M.** Slab on 2 units and a channel on 1. No garden, no west-facing entrance.
- **54-M.** 22 units are family-type tombs. None has a named inscription or a Jericho name.
- **54-W.** "Unfinished" or "unused" on 2 units (Wadi el-Ḥalaf, Kh. Kaʿkul). Kaʿkul fails as a family-type tomb.
- **56-P, 56-M.** Kokhim on 9 units and more than one chamber on 2. No oriented entrance, no cistern.
  - One frozen-rule fail is new, in the any-date set only: the Byzantine monastery in Naḥal Qidron (ʿAtiqot 89, pp. 49–82). The frozen F7 reads "eastern" in "the eastern tomb's staircase" as an entrance facing east.
  - INFERENCE: the word names which tomb, as the Amendment 1 hand check found for the same report's channel row. Frozen "no" codes are not hand-checked, so the fail stands.

**New matches:** none. **Lost matches:** none.

**Protected and held.** Seven phase-4 rows were met and excluded before coding. Their text was not printed or read.
- Held-unit ids:
  - SWP III pp. 192–198, Deir el-Kelt: a tomb row;
  - SWP III pp. 222–223, Tell es-Sultan: a channel and a pool. These two rows also match the strip guard.
- Tell es-Sultan strip, name guard:
  - ADAJ 3 pp. 74–75, Jericho 1954: a tomb and a pool;
  - ADAJ 4/5 (Arabic) pp. 6–9: a tomb.
- Held cave area, name guard: ADAJ 2 p. 90, Wadi en-Nar cave (cave with finds, located).

INFERENCE: the readers probably coded these rows from parts of the entries that they read normally (built sites). This view excludes them anyway, as the amendment's conservative guards require. All three tomb rows are unplaced, so the frozen name-only rule would not have counted them. No row has `protected_strip = yes`. No Kh. ʿAlmit or ʿAtiqot 41 row occurs.

**What stays unknown.**
- **Unplaced rows.** 80 phase-4 tomb rows of preferred versions have no coordinates, so they are not counted: 63 in the Jerusalem hills, 11 Gerizim, 4 Judean Desert, 2 Jordan Valley. 5 are dated to the window.
  - They include 22 QDAP, 22 SWP and Guérin, and 25 ADAJ rows.
  - By reader place they include 2 at the Tombs of the Kings, 1 at Tel Arza and 2 at Qumran.
  - Coded only for listing, none names a queen, Absalom, Zadok or Obed. None has a named inscription. Only one has a monument (F1): the YMCA ashlar family mausoleum (QDAP 4, pp. 70–80), third century AD.
- **Region B gains nothing located.** Jericho's tombs still rest on Kenyon and IAA Reports 7. The phase-4 Jericho tomb texts that might add to them are held: Kenyon's "Burial Customs at Jericho" (ADAJ 16) and ADAJ 2 p. 88.
- **The version rule can drop a point.** When an unplaced ʿAtiqot version becomes preferred, a located HA-ESI version drops out (Sallah ed-Din Street, here).
- **Earlier limits still hold.** The unjoined Hebrew–English pairs, the absence of deduplication among non-primary units, and the class-name artefact of the 11 October view are all unchanged.

Files:
- [phase4_units.csv](phase4_units.csv): 296 units, with phase, novelty flags, codes, duplicate flags and Amendment 1 codes; no text.
- [phase4_scores.csv](phase4_scores.csv), [phase4_view_2026-10-12.csv](phase4_view_2026-10-12.csv), [phase4_amendment1_view.csv](phase4_amendment1_view.csv).
- [phase4_summary.json](phase4_summary.json): exclusions, changes against 11 October, levels and coverage.
- [scripts/phase4_view.py](scripts/phase4_view.py) and [tests/test_phase4_view.py](tests/test_phase4_view.py).
- Rebuild: `python3 -I -B research/regional/tombs/scripts/phase4_view.py`.

**Proposed shared-file changes (integrator).**
- `research/OPEN_QUESTIONS.md`, Jerusalem tomb entries (keep the tracker pair identical): "Phase 1–4 inventory view (regional/tombs, 12 Oct, exploratory): 13 more located tomb units in Region A, none in Region B; Region A strict N 230. No branch gains a match. No ʿAtiqot, QDAP, SWP or ADAJ tomb names Zadok, Absalom, Obed or a queen."
- No change to ACTIVE_TEST, the outcome ledger, PROGRESS_METRICS, atlas data or candidate confidences.
- For the merge lane: the held-unit and strip guards caught 7 coded rows from partly held SWP and ADAJ entries. Consider marking such rows in `features_all.csv`, so that every lane excludes them the same way.

## Blocked: what a person would need to do

1. ~~IAA Reports 7 (Hachlili and Killebrew 1999)~~, https://publications.iaa.org.il/iaareports/69: done, read 11 October (addendum). Still unread there: the rotated Table II.2 (p. 52) and the figures themselves.
2. ~~IAA Reports 1 (The Akeldama Tombs)~~, https://publications.iaa.org.il/iaareports/74: done, read 11 October (addendum, exploratory).
3. **Kloner and Zissu 2007** (Peeters, ISACR 8). Interlibrary loan or purchase. Catalogue: https://library.arce.org/portal/Record/22665 (DS109.25 .K5613 2007). Needed: the tomb catalogue and the necropolis map.
4. **Avigad 1954** (Hebrew). Library only.

## Files

| File | What it holds |
|---|---|
| PLAN.md | Frozen plan (cd394d7) |
| PLAN_AMENDMENT_1_exploratory.md | Post-hoc exploratory rules |
| PLAN_AMENDMENT_2_exploratory.md | Coding choices for IAA Reports 7 (Part A) and the exploratory Akeldama addition (Part B), committed before either report's records were read (cd706b0) |
| tombs.csv | One row per unit (1,159; T1056–T1159 are the IAA Reports 7 units): source, record id, locator, name, lat/lon (EPSG:4326), uncertainty, region flags and distances, duplicate flag, links to earlier rows, every feature code with matched terms, names, period terms, dating, manual rejections, exposure, enrichment, text hash |
| scores.csv | One row per located unit and scored branch (22,880): clause values, result, sensitivity result |
| scores_summary.csv | Per branch × region × date set × view (`all_lineages`, `primary`, `lineage_HK`): N, k/f/m, sensitivity k/f/m, clause counts, matches |
| features_summary.csv | Per region × date set × view: feature counts |
| amendment1_codes.csv, amendment1_scores_summary.csv | Exploratory amendment outputs |
| amendment2_akeldama_units.csv, amendment2_scores_summary.csv | Amendment 2: the three Akeldama caves, coded and scored; Region A counts with and without them; Region B views with the Jericho tombs in place of the cemetery rows |
| data/hk_units.csv | IAA Reports 7: one short transcription per tomb (feature words only), pages, figures, report type, inscriptions |
| data/akeldama_units.csv | IAA Reports 1: the same for the three caves |
| data/manual_check_amendment2.csv | Hand decisions for the caves |
| data/iaa_reports_figures.csv | Figures and plans of both reports: references only, not copied |
| coverage.csv | Share of each region inside online ASI sheets |
| sources_access.csv | Every source, URL, status and what was read |
| data/kenyon_ii_units.csv | Kenyon II units, transcribed from the repo note |
| data/manual_check.csv, data/manual_check_amendment1.csv | Hand decisions with reasons |
| data/exposure.csv | Units exposed before the freeze |
| data/enrichment_a64.csv | Allegro 1964 observations (exploratory) |
| data/asi_manifest.csv, data/asi_selected_maps.json | Hashes and times of the ASI responses; the maps used |
| scripts/ | `fetch_asi_maps.py`, `build_tombs.py`, `amendment1.py`, `amendment2.py`, `coverage.py`, `tombs_common.py` |
| tests/test_tombs.py | Plan hash, schema, rules, reproduction of the scores; rebuild check with the cache |

Run from the repository root:

```
python3 -I -B research/regional/tombs/scripts/fetch_asi_maps.py CACHE
python3 -I -B research/regional/tombs/scripts/build_tombs.py CACHE WBADB_data1.xlsx
python3 -I -B research/regional/tombs/scripts/amendment1.py CACHE WBADB_data1.xlsx
python3 -I -B research/regional/tombs/scripts/amendment2.py CACHE WBADB_data1.xlsx
python3 -I -B research/regional/tombs/scripts/coverage.py CACHE
TOMBS_ASI_CACHE=CACHE TOMBS_WBADB=WBADB_data1.xlsx python3 -I -B -m unittest discover -s research/regional/tombs/tests -v
```

All 20 tests pass with the worker's cache (11 October). Without the cache, the two rebuild tests are skipped.

## Proposed changes for the integrator

1. **`research/ACTIVE_TEST.md`, "Key reports".** Add `· [Tombs](regional/tombs/README.md) (10 October: regional tomb count, entries 14, 24, 27, 48, 51–54, 56)`.
2. **Pending requests.** Add one line: "Owner: download IAA Reports 7 (Jericho cemetery) and IAA Reports 1 (Akeldama) in a browser; the PDFs are free but behind a bot check. Kloner and Zissu 2007 by loan."
3. **`research/OPEN_QUESTIONS.md`.** Add to the Jerusalem tomb entries (2, 27, 48, 51–56): "Regional count done (regional/tombs). Name and garden clauses are met by no survey record. West-facing kokhim tombs are common (exploratory: 24 of 56 oriented strict units). Next evidence: the Hachlili–Killebrew catalogue for Jericho; a dated inscription naming Zadok, Obed or a queen." Keep the OPEN_QUESTIONS/tracker pair identical.
4. **No change** to the outcome ledger, PROGRESS_METRICS, atlas data or candidate confidences.
5. **Housekeeping.**
   - The shared scratch folder `asi_cache/` belongs to another lane. This lane's first fetch wrote 18 files there and appended 17 rows to that folder's `manifest.csv`.
   - The files were moved to `scratchpad/tombs/asi_cache/`, and that manifest was restored to its own 46 rows.
   - The other lane may want to re-verify its manifest.
6. **Addendum, 11 October (IAA Reports 7 and 1).**
   - Pending requests: the request for IAA Reports 7 and 1 is satisfied; drop it if it is listed. Kloner and Zissu 2007 (loan) remains.
   - `research/OPEN_QUESTIONS.md`, entries 24, 27 and 54 (keep the tracker pair identical): "IAA Reports 7 read (regional/tombs addendum, 11 Oct): 103 Jericho tombs and a nefesh, 25 dated to the window. The frozen union counts are unchanged, since all lie inside the cemetery row WBADB S2446. Counted alone: 54-M 3 matches (A2, D1, H; exposed), 27-T 1 (Tomb H, Queen Agrippina as a freedman's patron), 24-J and 54-P none. No tomb has a grid position. Next evidence: georeferenced tomb positions from Figs. II.1–II.2."
   - Akeldama (exploratory): no Region A count changes; nothing to add to the shared files.
