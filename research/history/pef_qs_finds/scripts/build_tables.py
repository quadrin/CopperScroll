"""Build hits.csv and finds.csv from the search output and the hand codes.

    python3 -I scripts/build_tables.py OUT_DIR        # OUT_DIR holds hits_raw.csv from qs_search.py

Hand codes live in coding/:
  decisions.txt     one line per hit or range: 'H0001 keep' or 'H0002-H0010 not_find' (a drop reason)
  finds_manual.txt  one line per find row, 16 '|' fields:
      seq | author | place_as_written | place_id | distance_direction | find_type | report_kind |
      date_period | finder | disposition | quote | georef | relevance | ocr_flag | same_find_as | find_page
Hit sequence numbers (H0001...) sort hits by tier, year, item, leaf, key.
Tiers (frozen coding order): 1 non-JER keys; 2 JER strong 1869-1900; 3 JER strong 1901-1914;
4 JER feature 1869-1900; 5 JER feature 1901-1914.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REASONS = {"not_find", "other_place", "apparatus", "ocr_noise", "duplicate_page", "too_vague"}


def tier(h):
    y = int(h["year"][:4])
    if h["region"] != "JER":
        return 1
    if h["hit_class"] == "strong":
        return 2 if y <= 1900 else 3
    return 4 if y <= 1900 else 5


def main():
    out = sys.argv[1]
    with open(os.path.join(out, "hits_raw.csv"), newline="", encoding="utf-8") as f:
        raw = list(csv.DictReader(f))
    raw.sort(key=lambda h: (tier(h), h["year"], h["ia_identifier"], int(h["leaf"]), h["key"]))
    order = ["H%04d" % i for i in range(1, len(raw) + 1)]
    by_seq = dict(zip(order, raw))
    dec = {}
    for line in open(os.path.join(HERE, "coding", "decisions.txt"), encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        a, code = line.split()[:2]
        if "-" in a:
            s, e = a.split("-")
            rng = [x for x in order if s <= x <= e]
        else:
            rng = [a]
        for x in rng:
            if x not in by_seq:
                sys.exit("unknown seq " + x)
            if code != "keep" and code not in REASONS:
                sys.exit("bad code %s %s" % (x, code))
            dec[x] = code
    rows = []
    for n, line in enumerate(open(os.path.join(HERE, "coding", "finds_manual.txt"), encoding="utf-8")):
        if not line.strip() or line.startswith("#"):
            continue
        f = [x.strip() for x in line.rstrip("\n").split("|")]
        f += [""] * (16 - len(f))
        if len(f) != 16:
            sys.exit("bad field count line %d" % (n + 1))
        s = f[0]
        if dec.get(s) != "keep":
            sys.exit("finds row for non-kept hit %s" % s)
        h = by_seq[s]
        iss = h["issue"]
        vol = "QS %s" % h["year"]
        if h["ia_identifier"].endswith("1869-1870"):
            vol = "QS 1869-70" if iss != "reports" else "QS 1869-70 (reprinted Reports 1867-69)"
        rows.append({
            "find_id": "", "hit_seq": s, "hit_id": h["hit_id"], "volume": vol, "year": h["year"], "issue": iss,
            "printed_page": h["printed_page"], "page_source": h["page_source"],
            "find_page": f[15] or h["printed_page"], "ia_identifier": h["ia_identifier"],
            "leaf": h["leaf"], "matched_key": h["key"], "author_or_reporter": f[1], "place_as_written": f[2],
            "place_id": f[3], "distance_direction": f[4], "find_type": f[5], "report_kind": f[6],
            "date_period": f[7], "finder": f[8], "disposition": f[9], "quote": f[10],
            "georef_confidence": f[11], "relevance": f[12], "ocr_flag": f[13], "same_find_as": f[14]})
    kept_rows = {r["hit_seq"] for r in rows}
    missing = [s for s, c in dec.items() if c == "keep" and s not in kept_rows]
    if missing:
        sys.exit("kept without rows: %s" % missing[:20])
    for i, r in enumerate(rows, 1):
        r["find_id"] = "F%04d" % i
    first = {}
    for r in rows:
        first.setdefault(r["hit_seq"], r["find_id"])
    for r in rows:
        if r["same_find_as"].startswith("H"):
            r["same_find_as"] = first[r["same_find_as"]]
    with open(os.path.join(HERE, "finds.csv"), "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    hf = ["seq", "tier", "status", "drop_reason"] + list(raw[0].keys())
    with open(os.path.join(HERE, "hits.csv"), "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=hf)
        w.writeheader()
        for s in order:
            h = dict(by_seq[s])
            c = dec.get(s)
            st = "uncoded" if c is None else ("kept" if c == "keep" else "dropped")
            h.update({"seq": s, "tier": tier(by_seq[s]), "status": st, "drop_reason": "" if c in (None, "keep") else c})
            w.writerow(h)
    print("hits", len(order), "decided", len(dec), "find rows", len(rows))


if __name__ == "__main__":
    main()
