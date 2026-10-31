#!/usr/bin/env python3
"""EXPLORATORY post-hoc diagnostic (written after the confirmatory run; not part of the frozen test).
For each conjunctive match: does it survive when only name_as_printed is scored (other_names dropped)?
other_names can carry an editor's gloss copied by the extractor.
Run from the lane folder: python3 -I scripts/posthoc_name_field.py > results/posthoc_name_field_diagnostic.txt
"""
import sys, csv
sys.path.insert(0, "scripts")
sys.argv = ["x", ".", "../../agent_review_2026-10-07/wave1/T01_place_names", "../../agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3"]
import medieval_match as M
from toponym import heb_tokens, score
R = list(csv.DictReader(open("results/conjunctive_matches.csv")))
P = {r["rec_id"]: r for r in csv.DictReader(open("data/medieval_records_placed.csv"))}
print("group\tvariant\trec_id\tname_as_printed\tscore_name_only\tsurvives")
seen = set()
for r in R:
    k = (r["group"], r["rec_id"], r["variant"])
    if k in seen:
        continue
    seen.add(k)
    H = heb_tokens(r["variant"])
    s = max([score(H, list(A))[0] for A in M.name_skeletons(P[r["rec_id"]]["name_as_printed"])] or [0])
    print(f"{r['group']}\t{r['variant']}\t{r['rec_id']}\t{r['name_as_printed'][:50]}\t{s:.3f}\t{s >= 0.75}")
