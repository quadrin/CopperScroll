"""A2 train / held-out split of the letter controls (written and run BEFORE any relief feature was computed on any
control). Seed 20261031. Stratified by (secure_answer, column). Eligible: BK and HH controls in
research/text/letter_controls/controls_manifest.csv (use == control) with a W2F locator box (crop_box) and at least
one candidate cut present in the bucket. Round-1 held-out controls (exposed on 30 Oct) are forced into training.
Each held-out het is assigned by the same RNG to the HE/HET rule or the HET/TAW rule (scored once).
No sealed key is opened."""
import csv, json, os
import numpy as np
import pandas as pd
from common import HERE, REPO

SEED = 20261031
PRESENT = {2, 3, 4, 5, 6, 7, 8, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23}
EXPOSED_R1 = {"LC-CHH-081", "LC-CHH-084", "LC-CHH-085", "LC-CHH-130", "LC-CHH-132", "LC-CHH-134", "LC-CHH-135",
              "LC-CHH-136"}


def main():
    m = pd.read_csv(f"{REPO}/research/text/letter_controls/controls_manifest.csv")
    m = m[(m.use == "control") & (m.question.isin(["BK", "HH"])) & m.crop_box.notna()].copy()
    m["cuts"] = m.usc_1988_cuts_candidate.astype(str).str.split(";").apply(
        lambda l: [int(x) for x in l if x.strip().isdigit() and int(x) in PRESENT])
    m = m[m.cuts.str.len() > 0].copy()
    rng = np.random.default_rng(SEED)
    m = m.sort_values("candidate_id").reset_index(drop=True)
    m["split"] = "train"
    for (ans, col), g in m.groupby(["secure_answer", "column"], sort=True):
        ids = [i for i in g.index if m.at[i, "candidate_id"] not in EXPOSED_R1]
        ids = list(rng.permutation(ids))
        nh = len(ids) // 2
        for i in ids[:nh]:
            m.at[i, "split"] = "heldout"
    m["rule"] = ""
    for i in m.index:
        a = m.at[i, "secure_answer"]
        if a in ("ב", "כ"):
            m.at[i, "rule"] = "BK"
        elif a == "ה":
            m.at[i, "rule"] = "HE_HET"
        elif a == "ת":
            m.at[i, "rule"] = "HET_TAW"
        else:  # het: one rule, by the seeded RNG (applies to train and held-out alike; training uses hets in both)
            m.at[i, "rule"] = "HE_HET" if rng.random() < 0.5 else "HET_TAW"
    m["exposed_round1"] = m.candidate_id.isin(EXPOSED_R1)
    out = m[["candidate_id", "question", "secure_answer", "column", "ref", "etcbc_word", "char_index", "crop_box",
             "tier", "split", "rule", "exposed_round1"]].copy()
    out["cuts_present"] = m.cuts.apply(lambda l: ";".join(map(str, l)))
    out.to_csv(f"{HERE}/split.csv", index=False)
    print(out.groupby(["split", "secure_answer"]).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()
