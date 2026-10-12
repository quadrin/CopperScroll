# Number roles in the Herodium labels

Exploratory application, 12 October 2026. New evidence obtained: an observation-by-role dataset for the inspected Herodium publication, with exact source-indexed Masada electronic-edition controls and explicit diagnostic predictions. Project baseline `3b2d5c44b8c0add84a69d25f8e72cd16acc886db`.

Herodium's proposed numbers remain compatible with identifiers for places or portable referents. Counts and contents measures require relations that the available fragmentary text cannot establish. A separate locator-message branch requires an explicit spatial or retrieval relation. The noun's hiding-place/hidden-object alternatives leave its referent open. **The Herodium number roles are not identifiable from available evidence.**

## Applied distinction

A label's physical carrier, referent, number role, contents and use are separate fields. Ink on a jar identifies the carrier. It leaves open whether the text concerns that jar, its contents, a batch or a destination.

The exact Masada control, masa0595/*Masada I* no. 595, links 23 to the unit `לג` in the electronic edition and repeats 23 in two numeral systems. That explicit relation supplies a measure-role comparison; Herodium supplies no verified equivalent. Electronic metadata dates the control probably 66–73 CE. Its tentative fruit reading leaves commodity identity unresolved. The project makes no conversion to volume or scroll weight.

Masa 0302/*Masada I* nos. 302–312 retains wine/ten/tithe alternatives for yod. This provides an ambiguity control. A letter resembling a numeral cannot select numerical function by itself.

## Files and scoring

- [evidence.json](evidence.json) separates records, exact locators, source/date bases, uncertainty and field ancestry.
- [branch_rules.json](branch_rules.json) fixes the finite exploratory branches and their required relations.
- [comparison.csv](comparison.csv) records each source's relation to each role. PRESENT_IN_EDITION marks a positive edited relation; COMPATIBLE marks permission; UNKNOWN retains missing or unresolved evidence. Scores are categorical, without totals or probabilities.
- [predictions.csv](predictions.csv) names what would distinguish each Herodium role and what could contradict the exact claim.
- Per-source [Herodium](extracts/herodium_source_record.md), [Masada 595](extracts/masada_0595.md) and [Masada 302 group](extracts/masada_0302.md) extracts retain short numerical/date quotations and provenance scope.
- `compare.py build` derives the CSVs; `compare.py check` validates references, explicit uncertainty and deterministic reproduction.

## Limits and next discriminating evidence

The place branch needs an associated text or fixed-feature label assigning a number to a location. The object branch needs an associated text assigning it to a portable referent separately from place/amount. The count branch needs complete count syntax naming counted units. The contents-measure branch needs a unit-number relation. A recovered commodity name or residue result alone would settle none of those number roles.

These are prospective diagnostic requirements drawn after exposure. No unseen source is registered or inspected. Any independently proposed acquisition must audit prior exposure and association before becoming a confirmatory test. A few labels cannot measure regional rarity, and role branches can coexist in one administrative system.

Modern scroll entries 35/40 and Masada catalogue numbers are editorial locators. Herodium's tentative 40/35 supply no demonstrated correspondence with ancient Copper Scroll IDs. The already recorded scroll 40 tokens sit beside `ככר/ככ` at I 15/III 7; their unit interpretations remain in the closed [R12 audit](../../text/inventory_scope_2026-10-06.md). That audit's retrieval-form, ownership, units, chronology and ordering conclusions are preserved. No repeated numeric test, new mass total, date inference or historical-deposit claim is made here.

Herodium A/B share one excavation/specialist report. Masada records share Yadin's 1963–1965 field campaign and the 1989 catalogue. Electronic, archival and project representations add access without independent corroboration. Masada is a semantic control; its positive unit relation cannot transfer a function to Herodium.

## Access and publication

[Brown's masa0595 web view](https://library.brown.edu/iip/viewinscr/masa0595/) returned “not accessible via this tool”. Brown's [documentation](https://www.inscriptionsisraelpalestine.org/documentation/) provided the official GitHub fallback. Exact XML records were directly read at tree `0b7dc8358ccdfd0c9391f049da4839fbd91c26e5`. The catalogue identification was verified in archival masa0595. The failed view supplies no reading; recovery is through the electronic edition.

Brown identifies its data as CC BY-NC 4.0. Ancient words and authored paraphrases with attribution are included; no source images, PDFs or full modern commentary are copied. The pruned Herodium packet was not recovered in this worker's session; preceding native inspection is cited as source history.

Web opens of the exact [masa0595 XML URL](https://github.com/Brown-University-Library/iip-texts/blob/0b7dc8358ccdfd0c9391f049da4839fbd91c26e5/epidoc-files/masa0595.xml) and [masa0302 XML URL](https://github.com/Brown-University-Library/iip-texts/blob/0b7dc8358ccdfd0c9391f049da4839fbd91c26e5/epidoc-files/masa0302.xml) returned DisabledError. Connected GitHub file reads successfully supplied both exact XML records. This reader-specific failure leaves their electronic-edition reading complete; original catalogue pages and photographs remain a separate dependency.

**Obtained:** finite Herodium role comparison, exact Masada electronic-edition controls and diagnostic predictions. Herodium's place/object/count/contents/instruction assignments remain unknown.

