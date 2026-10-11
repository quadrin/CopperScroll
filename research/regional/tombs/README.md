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
