# R12: inventory form, units and dating

Exploratory audit, 6 October 2026 UTC / 5 October Los Angeles. Base: `5a0e9561135fddec6af6030e8c19e52a9dd7edae`. The user requested this focus change alongside ordering and Jericho inventory work. No unseen observation or confirmatory identification test was registered.

## Result

The retained text has the form of an inventory with retrieval instructions: object descriptions, quantity/unit labels, local directions and a final reference to a duplicate document with measurements and details. This descriptive classification survives removing flagged token hits. **Ownership, historical deposits and compilation/deposition dates are not identifiable from this evidence.** Temple property, offerings held by contributors or administrators, other religious/community holdings and a literary treasure catalogue remain compatible interpretations.

The analysis supplies a [per-entry feature result](inventory_features_2026-10-06.json) and [reproducible extractor](inventory_extract.py). It preserves the existing readings and translations. Counts describe one edited transcription under the repository's 61 canonical entry boundaries; they count neither independently observed manuscript letters nor distinct archaeological deposits.

## Sources and extraction

The main input is the existing [Abegg/ETCBC display transcription](../../data/scroll-text.js), derived from ETCBC `dss` 2.0.1, with morphology by Martin G. Abegg Jr., James E. Bowley and Edward M. Cook and conversion by Jarod Jacobs, Martijn Naaijer and Dirk Roorda. Derivative token data retain CC BY-NC 4.0 attribution. [The display builder](../../tools/build_scroll_text.py) defines each editorial flag. This transcription supplies another edited reading; it adds no independent original-manuscript observation.

[The entry concordance](../../tables/entry_concordance.csv) fixes the boundaries. The extractor assigns every token once. It separates entries2/3 inside I6 at בבור, following Puech p179 and the existing `deep_analysis/features.py` correction, and separates12/12a after III4. It keeps entry56 as one canonical row while recording its two plural-unit hits; different edition divisions remain in the concordance.

Inclusive counts retain all matching displayed tokens. The conservative `source_unflagged` sensitivity removes every nonempty display class—uncertain, restored, corrected, raised or removed—and any explicit ◦ or … character. It describes editorial notation, **not authentication of original strokes**. The display data do not preserve numeral-level uncertainty, so this pass makes no complete quantity total or numeral-readability judgment.

Comparative web sources were read as text only. The Josephus page also links a [Jerusalem illustration](https://penelope.uchicago.edu/josephus/Jerusalem.gif); image retrieval returned an unsupported-GIF error. Its pixels, date, authorship and reuse permission remain unverified, so the image is linked without redistribution or a cartographic-inspection count.

Seven input files have SHA-256 hashes in the result. Lemma matching removes vowel points and dataset homograph suffixes; exact-unit matching uses the displayed surface. This catches the medial-mem spelling חרמ in IX10, which an exact חרם substring search misses. It does not count the ככ inside the place name סככא as a unit.

## Accounting and object features

- **דמע:**12 tokens across10 entries (4,12,13,22,33,50,51,54,55,58). Source-unflagged sensitivity gives10 tokens across9 entries. XI4's first hit is דמע◦; XI14 has uncertainty/correction flags. Entry51 retains its second unflagged hit; entry55 drops.
- **חרם:**3 lemma hits, entries41/43/52, all unflagged in this transcription. Exact meanings remain edition-dependent. At entry41 the [retained apparatus](../../text/readings.json) contrasts offering silver and consecrated matter; Phase1 records a whole-line disagreement. The count establishes a repeated designation without resolving that disagreement.
- **Second tithe:**the explicit מעסר שני crosses I10–11 in entry4 and is unflagged in this transcription. The adjacent מפוגל / מפי גל alternatives mean disqualified tithe or a direction from a heap ([e4-disqualified](../../text/readings.json); Puech/Milik). The ritual-status claim depends on that branch. השבעי in I10 is an ordinal; treating it as a dated sabbatical year requires an additional interpretation and supplies no absolute date here.
- **Vessels:**17 כלי lemma tokens in16 entries; unflagged sensitivity14 tokens in14 entries. A vessel may be a valued object or a deposit container. Silver/gold context does not resolve that distinction. The בדין/כדין alternatives at entries10/30/38 preserve bars/pitchers alternatives (Phase1 §3).
- **Writing:**six כתבן suffix tokens occur in entries8/22/50/51/54/55. Five have the complete אצלם/אצלן formula; II5 is the separate bare occurrence. The retained כ reading permits accounts beside the objects. Puech's ב and Milik/Lange's locative/distance readings remain available; edition divisions attach the phrase differently. Their word positions persist, but those positions cannot settle the letters or semantics ([g-ktbn](../../text/readings.json); Puech2006 p189 n226; Milik1960 items25/53/54/57/58; the prior Pfann/Lange intake in [F2.19](../logs/findings_log.md)). The ordering thread audits the corresponding statistics separately.
- **Scroll/book nouns:**two ספר lemma hits have separate contexts. VI4–5 (entry25) specifies a jar with one scroll in it. VIII3 (entry33) has a plural-scroll clause with an uncertain continuation and Wolters's alternative first-person suffix. XII11–13 (entry60) separately refers to a duplicate of this document, its explanation, measurements and details. The final document wording survives the unflagged filter independently of the five disputed account formulas.
- **Garments:**III9's לבושין is one inclusive hit and zero unflagged hits. Puech's garments, Milik's resin and Wolters's first-person garment reading remain alternatives. I9's אפודת is unflagged in this transcription, with its garment/ephod meaning still interpretive. No author or owner follows from the object label.

The modern meaning arguments above are reused from the repository's source-scoped notes and apparatus, rather than newly read edition pages. In particular, Wolters's June1991 observations and Patrich's objection to his first-person ownership inference are recorded at [F2.10](../logs/findings_log.md): Wolters1994 pp292–295, discussion p296. This audit adds no new suffix verdict or high-priest attribution.

## What the units can establish

Exact matching gives **30 ככ tokens in30 entries**, **15 ככרין tokens in14 entries**, and one partly restored singular ככר in entry5. Unflagged sensitivity gives29 ככ,13 ככרין in12 entries, and zero singular hits. The morphology labels ככ as ככר, but that edited expansion cannot independently decide the disputed abbreviation.

Two concrete contexts reproduce the existing unit arguments without converting a total:

1. **II6 versus IV12:**each associates silver with seventy, using ככרין and ככ respectively. The parallel syntax permits the talent-abbreviation reading. Two deposits with the same numeral can use different units, so the parallel supplies compatibility rather than equality of units.
2. **XII1:**gold precedes ככ and a numeral rendered five. A uniform literal כסף כרש (“silver karsh”) expansion needs a further valuation or metal-dependent convention here. A generic karsh unit is a separate possibility. This identifies an explanation dependency; it does not refute Lefkovits's full argument, which was not reaccessed in this pass.

[F2.20](../logs/findings_log.md) records Lefkovits's selected corrections to full spellings and Elephantine abbreviation comparison (*Copper Scroll Studies*, ch9 pp139–154), Puech's adoption (ch5 p80 n56;2006 p174 n40), and Høgenhaven's parallel-syntax, redundant-silver and gold objections (2020 pp157–158). The selective-correction observation is reported scholarly evidence here, not a fresh surface inspection.

Retain both talent and karsh interpretations. Under the stated ten-shekel karsh / three-thousand-shekel talent convention, an abbreviated-unit amount differs by300-fold. That factor applies only to affected quantities; it cannot divide the entire scroll total by300. Full spellings, numerals, item counts and whether an amount weighs contents or counts objects require their own branches. The displayed English “talents” supplies a presentation choice, not independent unit evidence. Deposit scale consequently cannot yet identify its owner or demonstrate that the deposits existed.

## Explicit interpretation checks

**Inventory/retrieval form:**object categories, metrology and final duplicate-document wording remain available when every flagged feature hit is excluded and the five disputed formulas supply no account interpretation. Result: compatible as a textual-form description. This classification leaves both administrative use and literary imitation possible.

**Temple ownership from cultic/accounting vocabulary:**the second-tithe and dedication designations permit a religious-property reading. They establish neither the particular institution nor custody. As an external control, [Deuteronomy14:22–26](https://mechon-mamre.org/p/pt/pt0514.htm) prescribes tithe-related money and consumption by the addressee/household at the chosen sanctuary. This directly checked primary-text passage shows why a cultic designation cannot by itself identify a sanctuary's treasury as owner. It supplies no independent interpretation of the scroll's variant words and no date. Result for specifically Jerusalem-Temple ownership: **not identifiable from available evidence**.

**Written accounts beside deposits:**five formulas permit that reading under כ; retained ב/locative alternatives give different functions. Result: **not identifiable from available evidence**. No variant is removed on the basis of the compatible inventory form.

**Actual treasure and historical origin:**object/unit lists and the proposed duplicate can occur in both an administrative record and a literary catalogue. The retained units change hypothetical deposit size without supplying an independently identified hoard. Result: **not identifiable from available evidence**. No deposit, institution or whole-scroll account is confirmed.

## Chronology checks

**Entry22 / “Solomon's reservoir”:**Q37 records Milik's later-name argument at DJDIII D10–D11 pp263–264/C201 p257. Its original pages were not newly inspected. [Josephus, War5.4.2 (=BJ5.145)](https://penelope.uchicago.edu/josephus/war-5.html) was directly rechecked in Whiston's translation: the retrospective description of Jerusalem's old wall names Solomon's pool near Siloam and Ophel. This establishes a comparative literary name in Jerusalem's pre-destruction setting. It neither dates the name at Secacah nor identifies its reservoir; retrospective narration is also not a contemporary dated inscription. The parallel cannot set a compilation terminus or settle Milik's particular argument. [Prior question and scope](../logs/open_questions.md).

**Entry49 / Siloam:**the existing [foundation-coin audit](../measurements/cycle10/README.md) directly links Ariel2020 coin20, L105/basket1092, to a69/70CE issue (pp90*–91*). Accepting the published context gives a lower installation bound for that particular floor. A model in which the entry refers to that built phase must accommodate its construction date; an older dam or neighboring pool supplies no replacement date for the floor. The reading, feature identification and phase relation remain conditional. This is no date for the entire scroll or its cave deposition.

Keep **landmark construction, continued use/visibility, the time described by an instruction, source-list compilation, copying onto copper and cave deposition separate**. A ruin may remain a landmark, and a copied list may describe earlier arrangements. None of the selected controls currently bridges those stages to an absolute compilation or deposition date.

## Access, validation and stopping point

The publisher reaccess to Høgenhaven's chapter returned403. Exact needed source: *The Cave3 Copper Scroll: A Symbolic Journey* (2020), chapter4 “What Is Real? The Copper Scroll as a Material Artefact,” pp157–158, [publisher chapter](https://brill.com/display/book/9789004429581/BP000011.xml). For the full opposing argument, use Lefkovits's ch9 pp139–154 and Puech ch5 p80 n56 in *Copper Scroll Studies* (Brooke/Davies,2002/2004; [publisher preview](https://api.pageplace.de/preview/DT0400.9780567618313_A23695806/preview-9780567618313_A23695806.pdf)); a preview is not claimed to expose those pages. A surfaced2024 Copenhagen/Aarhus author-file link and Sefaria comparison pages also failed to provide usable text. They add no evidence. Repeated retrieval hunts remain parked; no outreach or fees occurred.

Run `python research/text/inventory_extract.py --check`. The script validates181 source lines,61 rows, complete unique assignment of every source token, critical uncertainty cases and five complete formulas, then compares the deterministic JSON bytes. Exact source tokens/indices and input hashes permit independent rechecking. The paired original inputs, translation, reading apparatus, candidate confidence, coordinates and outcome ledger remain unchanged.

This is one completed bounded inventory/units/chronology audit using existing research. It adds no newly inspected modern-edition or archaeological source scope, no independent campaign, identification, formal model exclusion or question closure. R12 can move from Queued to Inprogress. Reopen the bounded attribution/date questions for an authenticated ownership designation, independent deposit/context match, secure phase-to-instruction join or a documented correction to the retained textual branches. Those observations must discriminate the surviving alternatives; another compatible accounting phrase cannot do so alone.

## Supplied source reinspection — 6 October 2026 UTC

The user supplied Høgenhaven's full 278-page PDF again. Native PDF pages168–169 correspond to printed157–158; the title and rights leaves were also inspected. This resolves the chapter's reading dependency through the supplied copy. The publisher403 above remains historical; no recovery of that endpoint is claimed. The book was already supplied and used before this tracker (source registry; F2.20), so reinspection adds no new source scope or bounded check.

The pages confirm the retained disagreement. Høgenhaven prefers the talent interpretation, using the II6/IV12 parallel, redundant silver designation and gold context, while acknowledging selective corrections as evidence for a possible meaning difference. VIII6–7 supplies an additional mixed silver/gold example. Footnote62 reports **at least seven** corrected occurrences: I4;II6;X10;XII1,3,7–9. The proposal of another corrector is tentative. These are the author's reports and arguments; this inspection authenticates neither the manuscript corrections nor a second hand. Footnote66's approximate3660-talents figure is conditional context, not a newly calculated project total. Both unit branches remain open.

The source gives the full opposing routes as Lefkovits, *The Copper Scroll*, pp471–488 (especially479–480), and his *Copper Scroll Studies* chapter pp139–154. Puech's original acceptance note remains at CSS p80 n56. Those full original arguments were not reaccessed here; they remain the precise unit-source dependencies. No whole-scroll total, conversion, owner or date changes.

Both user-supplied PNGs now open. They show the same Jerusalem schematic layout, including “Solomons Pool,” Fountain Siloam, Temple and city walls. The compass places west at top, east at bottom, south at left and north at right. This is one illustration in two renditions, without a verified author, date, scale or survey registration. The larger rendition makes the labels easier to inspect. The earlier [GIF link](https://penelope.uchicago.edu/josephus/Jerusalem.gif) is associated through conversation context; exact file equivalence and server recovery are unverified. Pixel access is satisfied through the uploads. This illustration establishes no pool construction date, Secacah identification, metric datum or deposit location. It adds no source-verified cartographic intake.

Attachment provenance (user-supplied originals; SHA-256):

- Høgenhaven PDF:2,170,845bytes;278pages; `e2ba87457ee5e00466c1e59be149ac41f8aaed329fa9df200b901256fea76c36`. Printed page = one-based PDF page minus11 at the inspected target.
- `image.png`:121,316bytes;686×576RGBA; `7036b43c5d97b09dbd7e25e416ce765d0e880285aad402acf2359c444ba3253c`. Original viewed; a local white-background rendering also used to read its transparent pixels, with original bytes unchanged.
- `image(1).png`:713,537bytes;1350×1106RGBA; `30e1dcbdf02adb6da131709dd4f8a4625ccd08dd80ac7afeb76992564a46de9c`. Original viewed directly.

The PDF rights leaf reserves reproduction rights; the schematic's reuse permission is unknown. Source files and page renders are retained as supplied/local inspection material and are not redistributed in this GitHub update. This access/provenance update and the F2.20 wording correction add **zero** scopes, checks, cartographic intakes or campaigns. Activity remains71/5/81; all question states, outcomes, confidence, coordinates and analytical extraction fields remain unchanged. The findings-log input hash is refreshed to reflect the wording correction.
