"""Summarize hits.csv and finds.csv into summary.json (deterministic).

    python3 -I scripts/summarize.py            # from this folder: writes summary.json
    python3 -I scripts/summarize.py --check    # exit 1 if summary.json is stale
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def decade(year):
    y = int(str(year)[:4])
    return "%ds" % (y // 10 * 10)


def inc(d, k, n=1):
    d[k] = d.get(k, 0) + n


def build():
    hits = load("hits.csv")
    finds = load("finds.csv")
    vols = load("volumes.csv")
    s = {}
    # coverage per year
    cov = {}
    for v in vols:
        if v["role"] != "searched":
            continue
        y = v["label"][:4]
        c = cov.setdefault(y, {"items": 0, "items_with_text": 0, "hits": 0, "kept": 0, "dropped": 0, "uncoded": 0})
        c["items"] += 1
        if v["searchtext_sha256"] or v["djvu_txt_sha256"]:
            c["items_with_text"] += 1
    for h in hits:
        y = h["ia_identifier"].split("_", 1)[1][:4]
        c = cov[y]
        c["hits"] += 1
        c[h["status"]] += 1
    s["coverage_by_item_year"] = dict(sorted(cov.items()))
    tiers = {}
    for h in hits:
        t = tiers.setdefault("tier" + h["tier"], {"hits": 0, "kept": 0, "dropped": 0, "uncoded": 0})
        t["hits"] += 1
        t[h["status"]] += 1
    s["hits_by_tier"] = dict(sorted(tiers.items()))
    drops = {}
    for h in hits:
        if h["status"] == "dropped":
            inc(drops, h["drop_reason"])
    s["drop_reasons"] = dict(sorted(drops.items()))
    keyc = {}
    for h in hits:
        k = keyc.setdefault(h["key"], {"hits": 0, "kept": 0, "dropped": 0, "uncoded": 0})
        k["hits"] += 1
        k[h["status"]] += 1
    s["hits_by_key"] = dict(sorted(keyc.items()))
    first = [f for f in finds if not f["same_find_as"]]
    s["find_rows"] = len(finds)
    s["distinct_finds"] = len(first)
    per_place, per_type, per_dec, per_kind, per_conf = {}, {}, {}, {}, {}
    for f in first:
        inc(per_place, f["place_id"])
        for t in f["find_type"].split(";"):
            inc(per_type, t.strip())
        inc(per_dec, decade(f["year"]))
        inc(per_kind, f["report_kind"])
        inc(per_conf, f["georef_confidence"])
    s["distinct_finds_by_place"] = dict(sorted(per_place.items(), key=lambda x: (-x[1], x[0])))
    s["distinct_finds_by_type"] = dict(sorted(per_type.items(), key=lambda x: (-x[1], x[0])))
    s["distinct_finds_by_decade"] = dict(sorted(per_dec.items()))
    s["distinct_finds_by_report_kind"] = dict(sorted(per_kind.items()))
    s["distinct_finds_by_georef_confidence"] = dict(sorted(per_conf.items()))
    # recall checks (descriptive; the index check and post-freeze finds are exploratory)
    ocr = load("ocr_recall.csv")
    s["ocr_recall_1869_1908"] = {
        "primary_occurrences": sum(int(r["primary_occurrences"]) for r in ocr),
        "second_ocr_occurrences": sum(int(r["second_ocr_occurrences"]) for r in ocr),
        "lower_bound_primary_misses": sum(max(0, int(r["second_ocr_occurrences"]) - int(r["primary_occurrences"]))
                                          for r in ocr),
    }
    ir = {}
    for r in load("index_recall.csv"):
        inc(ir, r["status"])
    s["index_recall_status"] = dict(sorted(ir.items()))
    s["post_freeze_finds"] = len(load("post_freeze_finds.csv"))
    return s


def main():
    s = build()
    path = os.path.join(HERE, "summary.json")
    text = json.dumps(s, indent=1, ensure_ascii=False, sort_keys=False) + "\n"
    if "--check" in sys.argv:
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if old != text:
            print("summary.json is stale")
            sys.exit(1)
        print("summary.json is current")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path)


if __name__ == "__main__":
    main()
