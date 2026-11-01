# Run 28 fork log

Every decision taken after the rule was frozen (63c7858, RULE.sha256 `ba94214f…`), with the time and what had been seen.

## 31 Oct 2026, ~20:10 PT: scripts and interpretations, before any describer file or concordance existed

Seen at this point: no reader output of any kind for run 28.

- `scripts/agreement.py`: copied unchanged from the attribute inventory. Readers write `keyed/<src>_<R>.csv`; it is copied to `keyed/<src>_<R>_g1.csv` before agreement is run, because the script reads `_g*.csv`.
- `scripts/consolidate28.py`: the attribute-inventory `consolidate.py` with one change. It keeps sub-feature rows and `parent_id`, because a survey *site* is keyed with its caves as sub-features. The merge rule is unchanged.
- **Whole feature, for a describer** (RULE step 4): a row with no parent, or whose parent is not itself in an item class group (cave, water, channel, tomb). A cave keyed under a site is a whole feature; a chamber of a cave is not.
- **Concordance matching:** references and describer keys are compared after normalisation (upper case, no spaces, leading SITE/CAVE/NO./# removed). A site reference with no row of its own covers that site's child features. Any item linked by a `copied = yes` row is excluded.
- **Grids:** two groups of 4–6 digits, E first. If E/N falls outside the survey extent and N/E falls inside, N/E is used and flagged.
- **Rank** (reported, not gated): 1 + the number of candidates with a strictly higher posterior than the best truth member.
- **Scroll coding file format** for `score28.py`: `entry, class_group, n_openings, opening_dir, pillar, steps, notes`.
- `scripts/model28.py`, `bench28.py` and `score28.py` were tested only on synthetic describer files in a scratch copy of the folder. Checks 1 and 2 were run there for crashes only; their results were not printed.

## 31 Oct 2026, ~20:25 PT: concordance merged; 1952 list to third reading

Seen at this point: both concordance files (the main session listed their describer rows), the two 1952-list reader reports (attribute counts, no values compared against the inventory), and the agreement summary for the 1952 list.

- `scripts/concordance_merge.py` keeps a link when both readers give the same describer, 1993 keys and cited number. Result: four links — Benjamin list No. 7 = II/49; 1952 caves 19 = XI/19, 20 = XI/20, 37 = XIII/2. Both readers agree on all four; neither has a link the other lacks, so no third reading of the concordance was needed. Page and name citations (Region II to the Benjamin survey by page; "probably excavated by de Vaux") cannot define a truth set and are not kept.
- No concordance row of a run-28 describer is marked `copied = yes`; the six copied rows name other sources (Goldfus 1984, Frumkin 1988, Patrich & Arubas 1989, the Center for Cave Research, Bar-Adon 1989).
- Neither concordance reader found any 1993 feature identified with a Bar-Adon 1972 site.
- 1952 list: 14 disagreements (7 opening counts, 4 classes, 3 sizes) went to a third reader. Its brief adds one clarification of the schema: a phrase that says only which way a cave opens gives a direction, and counts as one opening only if the text clearly describes a single entrance.

## 31 Oct 2026, ~20:35 PT: 1952 list consolidated

- Third reading: A 8, B 2, both 4, neither 0. Opening counts are left blank where the text gives only a direction (sites 7, 15, 18, 20, 36); the doorway rows 4.A and 39.A get 1.
- Rows 29.B and 29.C were a numbering mismatch between readers (sub-features of cave 29 ordered differently). The third reader's values for them are explanatory text, and they are carried into `out/djd3_consolidated.csv` as written. They are parts of a cave, so they are not benchmark items (bench28 drops them) and cannot affect the gate.

## 31 Oct 2026, ~20:55 PT: Benjamin survey agreement; third reading limited to the model's fields

Seen at this point: both Benjamin reader reports and the agreement summary (matched 167; class 148/167; sizes 83/133; opening counts 7/8; no directions, steps or pillars in either file).

- The 53 size disagreements come from one source problem: the cave list prints "a × b × c m" without labels, and reader A keyed the typeset left-to-right order while reader B keyed the Hebrew reading order. Sizes are not used by the run 28 model, so they are not sent to the third reader; `consolidate28.py` keeps them as `A|B`. This limit is reported.
- The third reading covers the 20 disagreements on fields the model uses (19 classes, 1 opening count): `out/ben93_to_adjudicate_model_fields.csv`.
- Reader-only rows (A 29, B 44) are kept as single-reader rows, as for the Qumran sources.

## 31 Oct 2026, ~21:05 PT: Bar-Adon consolidated; all describer tables final

- Bar-Adon agreement: matched 75; class 65/75; opening counts 6/10; directions 4/5. Third reading of the 15 model-field differences: A 11, B 3, neither 1. Ten of them were the same key used by the two readers for different sub-features; following the brief, the consolidated value is the one for reader A's feature, and reader B's feature under that key drops out. The doorway rows 110.A, 118.A and 128.B.1 get one opening. The dolmen at 129.A is classed tomb.
- As for the Benjamin survey, size differences were not sent to the third reader; sizes are not used by the model.
- All three describer tables (`out/djd3_consolidated.csv`, `out/ben93_consolidated.csv`, `out/ba72_consolidated.csv`) and `keyed/concordance.csv` are now final. Next: `bench28.py gate`, run once.
