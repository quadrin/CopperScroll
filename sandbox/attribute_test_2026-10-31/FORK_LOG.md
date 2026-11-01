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
