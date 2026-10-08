#!/usr/bin/env python3
"""Build data/new_candidates_by_name.csv and print summary statistics for REPORT.md.
Run: python3 -I summarize.py ROOTDIR"""
import csv, json, os, re, sys
from collections import defaultdict, Counter
root = sys.argv[1]; D = os.path.join(root, "data")
names = {n["id"]: n for n in json.load(open(os.path.join(D, "scroll_names.json"), encoding="utf-8"))}
rs = list(csv.DictReader(open(os.path.join(D, "candidates_ranked.csv"), encoding="utf-8")))
def region(r):
    if not r["approx_lat"]:
        return "unknown"
    la, lo = float(r["approx_lat"]), float(r["approx_lon"])
    if r["sheet"] == "XVIII" and r["grid"] in {"Os","Ot","Ou","Ps","Pt","Pu","Qs","Qt"}:
        return "Jericho-Qumran"
    if r["sheet"] == "XVIII" or (r["sheet"] in {"XVII","XXI","XXII"} and r["grid"][:1] in {"N","O"}):
        return "Judean desert"
    if r["sheet"] == "XVII" and r["grid"] in {"Mt","Mu"}:
        return "Jerusalem"
    return "other"
out = []
by = defaultdict(list)
for r in rs:
    if names[r["scroll_id"]]["priority"] == 0 or float(r["score"]) < 0.75:
        continue
    r["region"] = region(r)
    r["appellative_gloss"] = "no (p.n./unexplained)" if re.search(r"p\.\s?n", r["gloss"]) else "yes (Palmer gives a meaning)"
    by[r["scroll_id"]].append(r)
keys = ["scroll_id","scroll_name","entries","variant","heb_skeleton","score","palmer_name","ar_skeleton","gloss","sheet","page","grid","approx_lat","approx_lon","region","appellative_gloss","ocr_source","rule_path"]
for sid, L in by.items():
    L.sort(key=lambda r: (-float(r["score"]), r["region"] not in ("Jericho-Qumran","Judean desert","Jerusalem")))
    seen = set()
    for r in L:
        k = (r["sheet"], r["grid"], r["ar_skeleton"])
        if k in seen: continue
        seen.add(k); out.append({x: r[x] for x in keys})
with open(os.path.join(D, "new_candidates_by_name.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(out)
print("new-candidate rows (score>=0.75, lost names only, deduped):", len(out))
c = Counter((r["scroll_id"], r["region"]) for r in out)
for sid in sorted(by):
    print(sid, {reg: c[(sid, reg)] for reg in ("Jericho-Qumran","Judean desert","Jerusalem","other")})
print("appellative share:", Counter(r["appellative_gloss"] for r in out))
# OCR stats
pn = list(csv.DictReader(open(os.path.join(D, "palmer_names.csv"), encoding="utf-8")))
pri = {"XIV","XV","XVII","XVIII","XXI","XXII"}
for src in ("djvu","tess"):
    sub = [r for r in pn if r["source"] == src and r["sheet"] in pri]
    noisy = sum(1 for r in sub if re.search(r"[^A-Za-zÀ-ÿĀ-ž'’‘ \-]", r["name_raw"]))
    print(src, "priority-sheet records:", len(sub), "with non-letter noise in name:", noisy, f"({noisy/len(sub):.0%})")
print("all records:", len(pn), Counter(r["source"] for r in pn))
