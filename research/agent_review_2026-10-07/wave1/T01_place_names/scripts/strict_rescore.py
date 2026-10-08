#!/usr/bin/env python3
"""Re-score manually verified candidates against their ARABIC-SCRIPT spelling (read from the Palmer page
images), keeping the distinctions Palmer's Latin transliteration drops (q/k, ṭ/t, ṣ/s, ḥ/h).
Arabic codes: Q=ق k=ك 7=ط t=ت C=ص s=س S=ش H=ح h=ه X=خ 3=ع G=غ '=ء/ا(hamza) E=ة
Run: python3 -I strict_rescore.py ROOTDIR -> data/verified_candidates.csv (merged with data/verified_input.json)
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import toponym as T

STRICT = {k: dict(v) for k, v in T.SUB.items()}
STRICT["k"] = {"k": (0, "R6"), "X": (0.3, "R6"), "Q": (0.6, "R6*"), "j": (0.7, "R6"), "G": (0.8, "R6")}
STRICT["q"] = {"Q": (0, "R6"), "k": (0.6, "R6*"), "G": (0.6, "R6"), "j": (0.6, "R6")}
STRICT["7"] = {"7": (0, "R1"), "t": (0.6, "R9*"), "d": (0.6, "R9")}
STRICT["t"] = {"t": (0, "R1"), "T": (0.3, "R9"), "7": (0.6, "R9*"), "d": (0.6, "R9")}
STRICT["C"] = {"C": (0, "R8"), "D": (0.3, "R8"), "s": (0.6, "R8*"), "z": (0.5, "R8")}
STRICT["s"] = {"s": (0, "R2"), "S": (0.3, "R2"), "C": (0.6, "R2*"), "z": (0.6, "R2")}
STRICT["$"] = {"s": (0, "R2"), "S": (0, "R2"), "T": (0.4, "R2"), "C": (0.6, "R2*")}
STRICT["H"] = {"H": (0, "R3"), "X": (0.3, "R3"), "h": (0.6, "R3*"), "3": (0.5, "R3"), "E": (0.6, "R3")}
STRICT["h"] = {"h": (0.2, "R1"), "E": (0.1, "A3"), "H": (0.6, "R3*")}
STRICT["3"] = {"3": (0, "R1"), "G": (0.3, "R4"), "H": (0.5, "R4"), "'": (0.5, "R4"), "E": (0.6, "R4")}
T.SUB = STRICT
T.AR_NAME.update({"Q": "q", "7": "ṭ", "C": "ṣ", "H": "ḥ"})

def main():
    root = sys.argv[1]
    items = json.load(open(os.path.join(root, "data", "verified_input.json"), encoding="utf-8"))
    rows = []
    for it in items:
        H = T.heb_tokens(it["hebrew"])
        A = it["arabic_codes"].split()
        s, c, path = T.score(H, A)
        it2 = dict(it)
        it2["heb_skeleton"] = T.heb_str(H)
        it2["arabic_script_skeleton"] = T.ar_str(A)
        it2["strict_score"] = round(s, 3)
        it2["strict_rule_path"] = " ".join(path)
        rows.append(it2)
        print(it["scroll_name"], it["palmer_name"], it["latin_score"], "->", round(s, 3), " ".join(path))
    keys = list(rows[0].keys())
    with open(os.path.join(root, "data", "verified_candidates.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    main()
