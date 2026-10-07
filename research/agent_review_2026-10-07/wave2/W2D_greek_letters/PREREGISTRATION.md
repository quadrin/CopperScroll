# W2-D pre-registration: CIIP marks + initials base rates

Written 2026-10-07 04:45 UTC. At this point I had not searched CIIP, opened Ilan's Lexicon or the xlsx, or read Lefkovits or Puech on the letters. I had read only the wave-1 T07 PREREGISTRATION/REPORT, the wave-1 SUMMARY, and the repo's phase-4 summary. That summary includes the repo's R11 "Ilan pilot": a 107-form subset, unweighted, which gave 2/7 prefix matches, ΘΕ via Θευδίων and ΣΚ via the Σκαριώθ variant. I know about that result, so my Part B cannot be blind to it. Part B differs from it in being frequency-weighted, covering the whole Lexicon, and having its rules stated here first.

Target groups (primary): ΚΕΝ (I 4), ΧΑΓ (I 12), ΗΝ (II 2), ΘΕ (II 4), ΔΙ (II 9), ΤΡ (III 7), ΣΚ (IV 2).
Reading sensitivities, reported separately and never merged into the primary score: ΞΕ (II 4), ΤΡΙ (III 7), ΙΣΚ / ΧΚ / ΞΚ (IV 2).
Letter equivalences: Ϲ = Σ = ς; Є = Ε; diacritics and breathings are ignored; capitals and lower case are the same letter.

## Part A — CIIP search (vols I.1, I.2, III, IV.1, V.1)

**Hit definition, same as T07.** A hit is a target group standing as a mark, label, abbreviation, monogram, numeral, mason's or quarry mark, or jar or ossuary label. That is: it stands alone, or is set off by a space, interpunct, abbreviation stroke or editorial expansion "( )", or it is a complete short legend. It also counts if the editor discusses the group as a letter group (e.g. "the letters ΚΕΝ may be…").
- A target group that merely begins or sits inside a fully written word in running text is not a hit.
- A target group that is the start of a name or word the editor expands from an abbreviation, e.g. Θε(όδωρος), IS a hit (graded as an abbreviation).

**Grades, same as T07:**
- **A:** core window (Judaea, Idumaea, Samaria, Galilee, Peraea, c. 200 BCE–135 CE); set off as a mark or abbreviation; explicit interpretation from context.
- **B:** conjectural interpretation; or extended window (rest of Palaestina, coast, 135–250 CE); or part of a longer abbreviation.
- **C:** set off but meaning unknown; or restored.
- **X:** inside a full word; restored letters only; outside the window or undated with no context.

**Search procedure, fixed now:**
1. Extract the text layer of each volume page by page.
2. Read any index of abbreviations, symbols, numerals, monograms, mason's marks or Greek words. Look up every target in it.
3. Run a full-text search for each target in Greek capitals, Greek lower case, and OCR look-alike Latin strings (e.g. KEN, XAΓ/XAG, HN, ΘE/OE, ΔI/AI, TP, ΣK/CK). Require a word boundary before the group, then classify each candidate by hand from the edition's own text and commentary.
4. Add searches for the editors' descriptive vocabulary: "mason's mark", "letters", "monogram", "abbreviat", "jar", "ossuary", "dipinto", "graffito", "label", "unexplained", "initials".

**Reporting.** Every candidate goes in data/ciip_candidates.csv, with volume, inscription number, page, object, site, date, editor's interpretation and grade, including the X rejections. I will state which volumes and pages could not be searched (bad OCR, missing text, download failure). An absence claim is made only for pages that were actually searched.

**Scoring.** As in T07, a system "explains" the groups only with grade A/B attestations of the SAME type of mark for at least 5 of 7 groups. It must also predict their position and their confinement to columns I–IV, using a single rule. Anything less is reported as "compatible for k/7".

## Part B — Initials hypothesis: base rates from Ilan, Lexicon I

**Hypothesis H-init.** Each group is the opening letters of a personal name as it would be written in Greek (owner, custodian, priest, depositor).

**Name universe.** Jewish persons in Palestine, 330 BCE–200 CE (Ilan, Lexicon I), and the companion xlsx.

**Weighting, primary.** Each attested bearer or attestation counts once, as Ilan counts them. A name's weight is its number of bearers. If only a per-name total is available, I use that total.

**Universes:**
- **U1 (primary): all bearers, every language of origin.** Each name is mapped to its Greek-script opening. Where Ilan prints Greek forms for the name, I use them. A name with several attested Greek openings is credited to every opening it has, as a set-membership (prefix-compatibility) test.
  - For a Semitic name attested only in Hebrew or Aramaic script, I use the conventional Greek rendering fixed by these rules:
    - ʾ, ʿ, h and ḥ before a vowel → the vowel;
    - y → Ι;
    - š, s, ṣ → Σ;
    - z → Ζ;
    - k → Χ (Κ also accepted);
    - q → Κ;
    - ṭ, t → Θ or Τ;
    - p → Φ or Π;
    - b → Β;
    - g → Γ;
    - d → Δ;
    - l, m, n, r → Λ, Μ, Ν, Ρ;
    - w → Ου;
    - "Yeho-/Yo-" → Ἰω-.
  - The second and third letters follow the same rules with the first vowel as Ilan vocalises it.
  - These mappings are generous on purpose: each one ACCEPTS alternatives. That biases the test toward finding matches, which works against the null.
- **U2 (strict): only names for which Ilan prints at least one Greek-script attested form.** The weight is the number of bearers. If Ilan's structure lets me count Greek-script bearers separately, I will use only those.

**Statistic per group g.** p_name(g) = (weighted bearers whose Greek-script name opens with g) / (total weighted bearers). I also report the unweighted share of distinct names.

**Null (letters).** Random groups of the same length.
- **N1:** letters drawn independently from the letter frequencies of the Greek-script name forms themselves. Position-free unigram frequencies are the primary null.
- **N2:** first-letter frequencies for slot 1 and position-free unigram frequencies for later slots.
- **Uniform 1/24** is secondary.
- For each group I report the ratio r(g) = p_name(g) / p_null(g). r(g) is the probability that a random bearer's name opens with g, divided by the probability that a random letter string of that length equals g. Because a name's opening letters are not random, r is expected to be much greater than 1 for common openings (e.g. ΙΩ, ΣΙ, ΕΛ) and 0 for impossible ones.

**Joint test (fixed now).** The opening distribution of real names is very uneven. So the meaningful comparison is between the seven observed groups and seven random groups drawn from N1 with the same lengths (3, 3, 2, 2, 2, 2, 2). Two statistics:
- **K** = the number of groups attested as an opening (p_name > 0), as in the repo pilot.
- **W** = the sum over groups of p_name(g), i.e. the expected number of the seven name-owners whose names would fit, given a random bearer for each slot.

For each I report the Monte Carlo upper-tail p (100,000 draws) for U1 and U2.

**Support / undercut rules (fixed now).**
- **SUPPORTS H-init (weakly), only if both hold:**
  1. K ≥ 5/7 in U1 AND the joint p for W is < 0.05, i.e. the groups are more name-like than random letter groups;
  2. the three-letter groups ΚΕΝ and ΧΑΓ are each attested openings with at least 1 bearer in U2. Three-letter matches are the informative ones.
- **UNDERCUTS H-init, if either holds:**
  1. K ≤ 3/7 in U1;
  2. W is at or below the null median, i.e. the observed groups are no more name-like than random letters.
- **Otherwise: INCONCLUSIVE.**

Even "supports" would mean only that the groups are compatible with name openings. It would not identify any person. The groups are short, and two-letter openings are common.

**Specific checks (named in advance).**
- ΚΕΝ: Kenedaios (Κενεδαῖος), or any Κεν- name.
- ΧΑΓ: Ḥaggai. Is the Greek Ἀγγαῖος (no Χ) or Χαγγ-? Is any Χαγ- name attested?
- ΘΕ: Theudas, Theudion, Theodotos, Theophilos.
- ΗΝ: any Ἠν-? Expected rare.
- ΔΙ: Diodotos, Dionysios.
- ΤΡ: Tryphon.
- ΣΚ: Skariot/Iskariot (a variant).

For each I report the bearer counts and pages in Ilan.

**Additional fixed rule.** Ilan includes 3Q15 (DJD III) as a source. Any attestation derived from the Copper Scroll itself is excluded.

## Part C — Lefkovits and Puech

I will read Lefkovits 2000 on the Greek letters (around pp. 498–504) and Puech 2006 on the same subject, and record their arguments with page numbers. Then I will state whether any CIIP or papyrus item found in Part A bears on each argument. I will not alter their claims to fit Part A.

## Part D — Conclusion rule

The best system stays at 2/7 unless Part A finds a grade A/B attestation of the same mark type for an additional group. Part B can at most make "personal initials" "compatible for k/7". It cannot raise the system score, because a base rate is not an attestation of the mark type.

## Papyri (CPJ, via Drive)

If downloaded, these are comparanda outside the core window (they are Egyptian). They are searched with the same hit definition and reported separately.

---
## Operational addendum A1 (written 2026-10-07 ~05:20 UTC, BEFORE any Part B scoring)

What I had seen when writing this:
- the CIIP Part A candidate hits;
- the structure of the xlsx and of the Ilan text layer;
- hand-read entries for Hagai (Ilan pp. 93-94) and Kenebon (p. 387), seen while checking the data structure.

I had not computed any p_name, null or Monte Carlo value.

### Data realities that force operational choices

1. **The Ilan Part I PDF is an OCR scan.** Greek and Hebrew come out as Latin junk. The English headwords, the "Index of the Names in English" (pp. 476-484; name, language/gender tag, pages) and the numbered bearer entries are readable.
   - Bearers per name are parsed as the largest entry number in each headword section.
   - Ilan's own Tables 5, 7 and 8 override the parse for the names they cover.
   - A name parsed at 0 bearers is set to 1, because every listed name has at least one bearer.
   - Denominator for weighted rates: the sum of these weights. I also report the result against Ilan's Table 2 total of 3,595 persons.
2. **The xlsx is not a Part I file.** It is a user-compiled list of "distinctively Jewish names", built from Ilan I-IV plus CIIP, CPJ and other corpora. It has 1,207 names, but only 35 Greek names. Its counts mix periods and regions, so I do NOT use them as weights. I use only its "Variant spellings (native script)" column, as a source of attested Greek spellings for names matched to Ilan Part I by English headword. Variants beginning with a lower-case letter are treated as fragments and skipped.
3. **Greek openings:**
   - **U1** = rule-based openings ∪ xlsx-attested openings. The rule-based openings follow the pre-registered Hebrew rules. For Greek, Latin and Persian names they come from a Latin-to-Greek back-transliteration of the headword (Th→Θ, Ch→Χ, Ph→Φ, Ps→Ψ, Rh→Ρ, X→Ξ, C/K/Q→Κ, initial H dropped, V→ΟΥ, J→Ι, Y→Υ). Alternatives are accepted: E→{Ε,Η}, O→{Ο,Ω}, U→{Υ,ΟΥ}, Hebrew T→{Τ,Θ}, P→{Π,Φ}, Kh→{Χ,Κ}.
   - **U2 (strict)** = attested Greek openings only. That means the xlsx Greek variants, plus the standard Greek headword spelling for names Ilan classes as Greek or Semitic-Greek.
4. **Nulls.**
   - N1: position-free unigram letter frequencies of one canonical Greek form per name, weighted by bearers.
   - N2: first-letter frequencies of the canonical forms for slot 1, N1 for later slots.
   - Uniform 1/24.
5. **Sensitivity, NOT pre-registered.** Initial ḥet rendered as Χ (as in LXX Χεβρων), reported separately, because the pre-registered rule renders ḥ as a vowel.
6. **The decision rules in Part B are unchanged.**
