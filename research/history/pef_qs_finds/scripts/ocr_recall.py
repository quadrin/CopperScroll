"""Compare pattern occurrences in two independent OCRs of the same QS years.

    python3 -I ocr_recall.py TERMS.json PRIMARY_DIR GETTY_DIR OUT_CSV

PRIMARY_DIR: the issue items (as for qs_search.py). GETTY_DIR: the
quarterlystateme*pale_djvu.txt files (bound volumes, 1869-1908).
Counts every counted occurrence of each key, page structure ignored.
Descriptive only: it estimates how often one OCR misses a name the other reads.
"""
import csv
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("qs_search", os.path.join(HERE, "qs_search.py"))
qs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qs)

GETTY_YEARS = {
    "01": (1869, 1870), "03": (1871, 1872), "05": (1873, 1874), "07": (1875, 1876),
    "09": (1877, 1878), "11": (1879, 1880), "13": (1881, 1882), "1516": (1883, 1884),
    "17": (1885, 1886), "19": (1887, 1888), "21": (1889, 1890), "23": (1891, 1892),
    "25": (1893, 1894), "27": (1895, 1896), "29": (1897, 1898), "31": (1899, 1899),
    "32": (1900, 1900), "33": (1901, 1901), "34": (1902, 1902), "35": (1903, 1903),
    "36": (1904, 1904), "37": (1905, 1905), "38": (1906, 1906), "39": (1907, 1907),
    "40": (1908, 1908),
}


def compile_all(T):
    exact = set(T["exact_patterns"])
    comp = []
    for k, v in list(T["places"].items()) + list(T["groups"].items()):
        comp.append((k, [qs.compile_pattern(p, exact) for p in v["patterns"]],
                     [qs.compile_pattern(p, exact) for p in v.get("exclude", [])]))
    return comp


def count(norm, comp):
    allm = []
    for k, pats, excl in comp:
        ex = [(m.start(), m.end()) for e in excl for m in e.finditer(norm)]
        for r in pats:
            for m in r.finditer(norm):
                if any(a <= m.start() and m.end() <= b for a, b in ex):
                    continue
                allm.append((m.start(), m.end(), k))
    allm.sort()
    res = {}
    # containment suppression with a sweep (matches are short)
    for i, (s0, e0, k0) in enumerate(allm):
        inside = False
        for j in range(max(0, i - 30), min(len(allm), i + 30)):
            s1, e1, k1 = allm[j]
            if k1 != k0 and s1 <= s0 and e0 <= e1 and (e1 - s1) > (e0 - s0):
                inside = True
                break
        if not inside:
            res[k0] = res.get(k0, 0) + 1
    return res


def main():
    import json
    terms, prim, getty, out = sys.argv[1:5]
    T = json.load(open(terms, encoding="utf-8"))
    comp = compile_all(T)
    rows = []
    for vol, (y0, y1) in sorted(GETTY_YEARS.items(), key=lambda x: x[1]):
        gid = "quarterlystateme%spale" % vol
        gp = os.path.join(getty, gid + "_djvu.txt")
        if not os.path.exists(gp):
            continue
        gnorm, _ = qs.normalize(open(gp, encoding="utf-8").read(), False)
        gc = count(gnorm, comp)
        pc = {}
        for ident in sorted(os.listdir(prim)):
            if "index" in ident or not os.path.isdir(os.path.join(prim, ident)):
                continue
            y = int(ident.split("_", 1)[1][:4])
            if not (y0 <= y <= y1):
                continue
            pages, pn, mode = qs.load_item(os.path.join(prim, ident), ident)
            norm, _ = qs.normalize("\n".join(pages), False)
            for k, n in count(norm, comp).items():
                pc[k] = pc.get(k, 0) + n
        for k in sorted(set(gc) | set(pc)):
            rows.append({"years": "%d-%d" % (y0, y1) if y1 != y0 else str(y0), "getty_id": gid, "key": k,
                         "primary_occurrences": pc.get(k, 0), "second_ocr_occurrences": gc.get(k, 0)})
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["years", "getty_id", "key", "primary_occurrences", "second_ocr_occurrences"])
        w.writeheader()
        w.writerows(rows)
    print(len(rows))


if __name__ == "__main__":
    main()
