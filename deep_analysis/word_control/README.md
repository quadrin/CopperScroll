# R11 common-noun control

This exploratory comparison asks whether the frozen107-form Ilan pilot covers the Greek groups better than equally sized samples of common-noun forms. Source: PROIEL/Syntacticus Greek New Testament XML at commit525cee4fb40590d7d514376c11acaed1bdd91c15, [exact source](https://github.com/syntacticus/syntacticus-treebank-data/blob/525cee4fb40590d7d514376c11acaed1bdd91c15/proiel/greek-nt.xml). The29,134,492-byte XML SHA256 is3e3839a7f1a32efc027eb0d0e525b0527354b1979dd01b85f2f8c5236e2e8cc6. This choice preceded new prefix queries. The older20180408 file was acquired for schema exploration only, never queried; it is not a retained scoring branch.

XML metadata identifies Tischendorf's *Novum Testamentum Graece*, eighth critical edition, Leipzig1869; Ulrik Sandborg-Petersen electronic version2.0 from2008; annotation export23 April2023. All11,506 present sentence elements are reviewed. This does not establish full NT text or complete ancient vocabulary: README completeness warnings are older, and absent source text cannot be inferred from XML statuses. The token form may reflect annotation splitting, rather than an independently inspected ancient manuscript word. Source edition/spelling/genre and the Ilan collection differ; NT text is not an independently localized/pre70 attestation corpus or a holdout. Ilan already cites NT and the groups were exposed.

Eligibility fixes reviewed/annotated nonempty Nb(common noun) tokens, excluding Ne proper nouns and every other POS. A source-neutral audit inspected all1,894 Nb lemmas, including all96 uppercase cases, without querying prefixes.92 lemmas are named people/places/ethnics/sects/epithets and excluded; eight ambiguous designations are withheld, including Caesar and seven lowercase contextual cases.1,794 remaining lemmas use the source Nb classification. Uppercase typography triggered inspection rather than automatic exclusion. The audit does not verify every token sense. Generic office/abstract/religious categories remain lexical common uses; title/designation ambiguity is explicit.

`extract_words.py` applies the SAME normalization as the Ilan pilot: accents/breathings removed, sigma shapes unified, uppercase24-letter Greek, no joining or back-transliteration, iota subscript rejected.1,837 Nb occurrences fail this spelling rule;82 are withheld semantic unknowns and292 excluded named-designation occurrences. Deduplicate literal normalized forms uniformly. Frequency and repeated inflections do not add sampling weight. Selected3,791 forms each carry source lemma and a token/citation exemplar.18 forms also occur with Ne form/lemma classification elsewhere. Retain their source-common uses in the primary population; remove those18 only in a fixed secondary sensitivity(3,773 forms). Names also used as common words are not deleted through Ilan overlap. Synthetic/empty nodes and unsupported inputs cannot supply a match.

Freeze `word_forms.csv`, semantic decisions, audit, source hash, name CSV hash and code BEFORE scoring. Reading UNION is primary for this comparison, preserving ΘΕ/ΞΕ,ΤΡ/ΤΡΙ,ΣΚ/ΧΚ/ΞΚ opportunities for both populations; literal-primary and all12 combinations are reported sensitivities. No result picks the smallest tail. The original name-pilot primary/union definitions and results remain unchanged.

Draw107 distinct forms uniformly without replacement from the common-noun population. The exact finite-population distribution counts how many of seven slots have at least one compatible prefix. It preserves dependencies between slots and shared/nested alternatives. Report each slot, all compatible word forms, all name matches, expected score, full score distribution and the fraction of107-form samples scoring at least as high as the fixed name list. Complete-word-list coverage is descriptive, not a fair comparison with107 names. These are benchmark probabilities, not the chance that personal initials are true; selected name forms are not a random sample. No arbitrary significance threshold or historical rejection is declared. Historical meaning remains not identifiable without discriminating evidence and an unused observation.

Reproduce intake by downloading the exact XML, verifying its hash, then running from repository root:

```
python deep_analysis/word_control/extract_words.py SOURCE.xml --decisions deep_analysis/word_control/lemma_decisions.json --out deep_analysis/word_control
python -m unittest discover -s deep_analysis/word_control -p test_word_control.py
python deep_analysis/word_control/benchmark_sample.py --self-test
```

After the input commit publishes, run:

```
python deep_analysis/word_control/benchmark_sample.py --words deep_analysis/word_control/word_forms.csv --names deep_analysis/ilan2002/pilot_forms.csv --freeze deep_analysis/word_control/freeze.json > deep_analysis/word_control/results.json
python deep_analysis/word_control/verify_distribution.py deep_analysis/word_control/results.json
```

No target-prefix scoring had run at this input freeze. The independent integer generating-function calculation verifies inclusion/exclusion output without importing the benchmark. Full XML and continuous text are not bundled. Existing Phase4 evidence and ACTIVE_TEST hold the result; this folder holds reproducible data/code.

## Attribution and data licence

PROIEL/Syntacticus, University of Oslo; Dag T. T. Haug and Marius L. Jøhndal(2008), *Creating a Parallel Treebank of the Old Indo-European Bible Translations*, LaTeCH2008, pp27–34. Source contributors/metadata are preserved in `extraction_audit.json`. Underlying electronic Greek text is public domain according to its XML metadata; source annotation and derived form/lemma/token data are licensed [CC BY-NC-SA4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: Nb selection, semantic exclusions, Unicode normalization, deduplication, mixed-use flags and reduced exemplars. The licence applies to this derived source data; original project code and analysis retain repository terms. No source endorsement is implied.
