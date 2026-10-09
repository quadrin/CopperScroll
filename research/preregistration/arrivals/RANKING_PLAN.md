# Ranking plan (frozen before the ranking is computed)

Written 9 October 2026 UTC by the arrival-register worker, before `build_register.py` computed any ranking. Its SHA-256 and time are in the README. The ranking is descriptive. No claim, count or test result follows from it.

## Question

Which pending items could separate the most live model classes, if they arrive?

## Class universe

1. **Decision classes (26).** The classes that `research/feature_workbench/decisions/discriminate.py` computes, read-only: 10 Koḥlit classes, 7 XII 10 strings (R1–R7), 6 Entry 25 classes, and the 3 named branches of closed tests (A(C)94, Wadi Nuʿeima, Siloam main basin).
2. **Chain models outside the decision roster (25).** The 28 Koḥlit models in `research/assessments/kohlit_chain/chain.json`, minus the three that the decision classes already hold (Tell es-Sultan, Kh. el-Marjama, the Janoaḥ route). Each has three reading branches: RB-M, RB-P and RB-B. A link excludes only the branches it names.

## Outcomes per item

- **Decision rows.** If an item is the record of a decision task, its rows are that task's rows in `discriminate.py` output. Each row lists the classes it excludes. Row kinds stay as recorded: decisive, partial, not_obtained.
- **Chain links.** Every link in `chain.json` whose record is the item. Outcomes: confirm (its success criterion), contradict (its contradiction criterion; only for two-sided and absence-statement links), inconclusive, silent.
- Two filters, fixed now:
  - No aspect rule for cave mouths is frozen. So L-656 rows that need a mouth bearing are replaced by the matching "bearing undetermined" rows. The IAA cave records get no Entry 25 rows.
  - Høgenhaven's reading is one reader, and the request named the lines. It cannot pass the frozen XII 10 reader gate, so it gets no XII 10 rows.

## Statistic

All numbers are conditional on the item arriving. Whether a reply comes is not modelled.

- **Coverage factor c**, set per item and per link before computing, with a reason:
  - 1: the item is by definition the record of that relation;
  - 1/2: the item was asked for that place or topic, but whether it records the relation is unknown;
  - 1/4: the relation would be an incidental find in the item;
  - 0: the item cannot bear on it under the frozen rules.
  - With probability 1 − c the item is silent on the relation. Silence excludes nothing.
- **Expected decision-class exclusions:** E_dec = c × (½ × mean exclusions over the non-decisive rows + ½ × mean exclusions over the decisive rows). Non-decisive rows are the partial and not_obtained rows. If an item has no non-decisive row, that half counts as zero exclusions.
- **Expected chain exclusions**, in model equivalents: for each model, E = (1/3) × Σ over its branches b of [1 − Π over links l that can exclude b of (1 − p_l)]. For a two-sided or absence-statement link, p_l = c_l × ½ × ½ (the decisive half, then contradiction as one of two decisive outcomes). For a one-sided link, p_l = 0.
- **Best case:** the most classes one outcome can exclude (decision rows), plus the share of branches that some contradictable link names (chain).

## Rank key

1. E_total = E_dec + E_chain, highest first.
2. Ties: best case, then the number of closed results the item can reopen, then the item id.

## Sensitivity

Recompute with the decisive share at ¼ and at ¾ instead of ½. Report every rank that moves.

## Not done

No probability of a reply, no likelihood, no information gain and no prior over models. The equal halves are a declared convention, not an estimate.
