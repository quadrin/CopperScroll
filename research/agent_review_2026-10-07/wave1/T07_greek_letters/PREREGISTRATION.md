# T07 pre-registration (written 2026-10-06, before any corpus query or hit was inspected)

## Target groups
Primary: ΚΕΝ, ΧΑΓ, ΗΝ, ΘΕ, ΔΙ, ΤΡ, ΣΚ.
Reading sensitivities (reported separately, never merged into the primary score): ΞΕ (for ΘΕ), ΤΡΙ (for ΤΡ), ΙΣΚ / ΧΚ / ΞΚ (for ΣΚ).
Ligatures, lunate sigma (Ϲ) and epsilon (Є) count as the same letter.

## What counts as a hit
A hit is an occurrence of a target group on an object or document where the group is a
**mark, label, abbreviation or numeral**, i.e. it stands alone, is set off (space, interpunct,
abbreviation stroke, editorial (expansion)), or is a complete short legend. A group that is
merely the beginning or middle of a fully written word in running text is NOT a hit (it is
counted only in the chance baseline).

Window: core = Judaea/Idumaea/Samaria/Galilee/Peraea (incl. Masada, Qumran, Jericho, Herodium,
Jerusalem, Judean Desert caves), c. 200 BCE – 135 CE. Extended (graded down) = rest of
Palaestina/Arabia/Decapolis/Phoenician coast and 135–250 CE. Outside the extended window =
comparanda only (e.g. Egyptian papyri conventions), never scored as a regional hit.

## Grades (assigned per hit before assessing any system)
- **A**: core window; group set off as a mark/abbreviation; editor gives an explicit
  interpretation grounded in context (expanded form on the same object/series, a sequence of
  analogous marks, a measure/numeral system on the same object).
- **B**: as A but interpretation conjectural, OR extended window, OR the group is part of a
  longer abbreviation (e.g. ΤΡΙ as part of ΤΡΙΤ).
- **C**: group set off but meaning unknown/undiscussed, OR only a reconstruction/restoration.
- **X (exclude)**: inside a fully written word; restored letters; outside extended window;
  date unknown and no context.

## System criterion (fixed before looking)
A single interpretive system "explains" the Copper Scroll groups only if:
1. the SAME type of mark (e.g. capacity units, owner initials, numerals, priestly courses,
   months, checker/controller marks, mason's position marks) is attested with grade A/B hits
   for **at least 5 of the 7** primary groups; AND
2. the system plausibly predicts the position (end of an entry, after the amount or
   description) and the confinement to entries 1–15 / columns I–IV; AND
3. it does not require different rules for different groups (cf. Ullendorff's 4+ rules).
Anything less is "compatible for k of 7 groups", not an explanation.

## Chance expectation (method fixed before looking)
- For standalone marks: expected hits for group g in a corpus of N standalone 2–3-letter
  marks = N × p(g), where p(g) = product of letter frequencies (uniform 1/24 per letter as
  the primary null; empirical Greek-inscription letter frequencies from the same corpus as a
  secondary null).
- For abbreviations (word-initial truncations): expected hits ∝ share of word tokens in the
  corpus that begin with g. Groups that are common word openings (expected: ΘΕ, ΔΙ, ΤΡ,
  possibly ΚΕΝ) will produce many abbreviation hits by default; such hits are only
  informative if they come with an explicit system context. ΧΑΓ and ΗΝ are rare openings,
  so any explicit abbreviation hit for them would be more informative.
- Report observed vs expected for every group, including zeros.

## Falsification
For each candidate system the report must state an observation that would refute it on the
scroll itself (e.g. numerals: values must relate to the amounts; capacity units: the unit
must fit the commodity in that entry; owner initials: the same initials should recur when
the same depositor/fund recurs; priestly courses: groups must map onto the 24 course names
of 1 Chr 24; months: groups must map onto month names in Greek or Hebrew).
