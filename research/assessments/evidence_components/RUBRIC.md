# Evidence components: rubric

Frozen 15 October 2026 (Los Angeles), before any entry was rated. Ratings made under this rubric are in [ratings.json](ratings.json) and [ratings.csv](ratings.csv).

## Why

The atlas gave each entry and candidate one label (low / medium). That label did not say which part of the case was strong and which was weak, and most candidate labels were set by a default in `build_atlas.py` (preferred candidate inherits the entry label; four named pairs get "medium"; all others "low"). A placement is only as strong as its weakest link. This rubric splits the case into five parts and rates each from the evidence the repo records.

This is a description of the evidence, not a test. It identifies nothing and excludes nothing. It does not change the [outcome ledger](../../progress/outcome_ledger.json): identifications stay at 0.

## Unit

One row per atlas candidate (entry × candidate place), 91 rows, plus entry 41 (no candidate). The reading component is per entry and repeats on each of its candidates.

**Anchor words** are the words of the entry that the placement relies on: the place name and the landmark noun(s) used to choose this candidate. Name them in each row.

## Components

Each of R, P, F and D takes a level 0–3. Rate on the weakest anchor word or link. When the evidence is between two levels, take the lower.

### R — Reading: are the anchor words secure?

- **3** — Milik 1962, Puech 2015 and Lefkovits 2000 agree on the letters and on the kind of thing the word names; no plate-check finding against. Spelling variants that leave the word the same do not count against it (e.g. the engraved גויזין for Gerizim).
- **2** — The letters are agreed but the meaning is disputed in a way that changes the kind of landmark looked for (cairn vs dam); or one edition dissents on the letters while the others and any plate check agree.
- **1** — An anchor word depends on a restoration, a correction of the engraved letters, a minority reading, or a reading the plate check leans against.
- **0** — The anchor words are lost or unread.

### P — Place: does evidence outside this entry put the named place at the candidate?

- **3** — The name is attested in an ancient source (Bible, 1–2 Maccabees, Josephus, Mishnah, Eusebius) and its location is fixed independently: by the name surviving at the place, or by unambiguous geography (a named mountain, a named valley with a fixed course).
- **2** — The location rests on a late name survival only (Byzantine or later, Arabic), or on one editorial identification that most editors accept but that has a named alternative.
- **1** — The location is inferred from entry order or the scroll's own context, or from an editorial identification with live alternatives of similar weight.
- **0** — No place name, or the name is unlocated: the candidate was chosen on landscape grounds alone.

P rates the district the name points to. Whether the pin is the right spot inside that district belongs to F.

### F — Feature: is the entry's landmark reported at the candidate?

- **3** — A specific recorded feature has every element and relation the entry describes (kind, number, side, orientation, neighbour).
- **2** — A specific recorded feature has the landmark's kind plus at least one described relation or attribute; the others are unknown and none is contradicted.
- **1** — Only generic features of the kind are reported at the candidate or in its district (cisterns, caves, channels), with no specific one matching the relations.
- **0** — No feature of the kind is reported, or the reported features contradict the description.

A feature known only from a published reconstruction counts one level lower than an observed one.

### D — Date: was the feature there and usable in the window?

The window is the project's 50 BCE–70 CE, extended to 135 CE ([Koḥlit pre-registration](../../preregistration/kohlit_rarity_2026-10-08.md)).

- **3** — The specific feature rated under F is dated in the window by stratified finds or a dated construction phase.
- **2** — The site or complex containing the feature was occupied in the window; the feature's own date is unknown.
- **1** — Only the district shows occupation in the window, or the site's evidence for the window is thin or doubtful (a few surface sherds, an unstratified coin, a later tradition).
- **0** — The evidence puts the site or feature outside the window, or there is no evidence of date at all.

If F is 0 or 1, D rates the site and cannot exceed 2.

### U — Uniqueness: has the candidate been told apart from alternatives?

- **discriminates** — A registered test with controls supports this candidate over the alternatives. (None so far: the ledger has 0 identifications.)
- **not unique** — A documented alternative or control meets the same tested subset (a ledger nonunique comparison, or a named rival feature in the record, e.g. Twin Cave for IV/17, the Strouthion pools for Bethesda).
- **conditionally excluded** — A ledger conditional exclusion rejects a branch of this candidate (name the branch).
- **untested** — No comparison against controls or an inventory.

## Overall

**Weakest link** = min(R, P, F, D), named by the components that set it:

| min | Label |
|---|---|
| 3 | strong |
| 2 | partial |
| 1 | weak |
| 0 | none |

A candidate counts as an identification only with all four at 3 and U = discriminates. No row meets that.

## Rules for raters

- Use what the repo records: [atlas data](../../../atlas/app/atlas-data.json), [readings](../../../text/readings.json), [plate check](../../text/plate_check.md) and [table](../../../tables/plate_check.csv), [lexicon](../../../tables/landmark_lexicon_index.csv), [phase 5 index](../../../tables/phase5_archaeology_index.csv), [feature constraints](../../../tables/feature_constraints.csv), the [findings log](../../logs/findings_log.md), [open questions](../../OPEN_QUESTIONS.md), the assessments, regional rounds and site reviews. Cite a file and section or line for each level, and the edition or report page where the repo gives it.
- Background knowledge (BK) may be noted, marked BK. It can lower a level (by pointing to a contradiction to check) but cannot raise one.
- Record unknowns as unknown. Do not fill a gap with a guess; take the lower level.
- Rate the evidence for the candidate, not the plausibility of the scroll's account. Do not let a good feature raise a weak reading, or a secure name raise a missing feature.

## Calibration examples

Rated while writing the rubric; raters should match this severity.

- **57 / Mount Gerizim.** R 3 (Gerizim agreed; "step" agreed; the pit word varies but every edition reads a pit). P 3 (named mountain). F 1 (Magen's staircases and a courtyard cistern are separate installations; no pit is reported in relation to a step). D 1 (city destroyed about 110 BCE; a later garrison is reported and one Festus coin is catalogued at a locus of unknown context). U untested. **Weak — F, D.**
- **21 / Kh. Qumran.** R 1 ("stone" is restored; the word linking the conduit to Sekakah is lost). P 1 (Sekakah = Qumran rests on entry order and "from Jericho to Sekakah"; no name survives; Milik puts biblical Sekakah at Kh. es-Samra). F 2 (a specific aqueduct with an intake; the stone and the "north" relation unknown; the dam at the head is reconstructed). D 2 (aqueduct in use in the window; which part is the "head" is undecided, and Stacey's phasing makes the dam a later stage). U untested. **Weak — R, P.**
- **31 / Jebel Qarantal (Doq).** R 1 (the fortress needs "guard post"; Puech's "drying place" and the plate check lean the other way). P 3 (Doq in 1 Macc 16:15; the name survives at ʿAin Duk). F 2 (a Hasmonean fortress with corners, under the guard-post reading). D 1 (not shown rebuilt by Herod; first-century use not shown). U untested. **Weak — R, D.**
