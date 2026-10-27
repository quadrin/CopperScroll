"""Text flags per inventory cave (regex proposals; reviewed by hand in overrides.json).

Inputs: out/all_rows.json, out/inventory.csv, and the repo DJD III extraction
(research/history/djd3_text_cave_list_extracted.md, site table pp. 6-13) for DJD3 rows.
Output: out/flags_auto.json  {cave_id: {flag: [matched snippets]}}
"""
import csv, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
DJD = "/home/claude/copperscroll/research/history/djd3_text_cave_list_extracted.md"

FLAGS = {
    "building": r"\bbuilding|\bhouse\b|\brooms?\b|chapel|monaster|\btower\b|cell built|built in a natural cave|built facade|complex of buildings",
    "three_levels": r"\b(three|four|five|3|4|5|11|several)\b[^.;]{0,25}\b(levels?|storeys?|ledges?|terraces?|steps|courses|tiers)\b|several levels",
    "fissure": r"crack|fissur|crevi|cleft|נקיק|סדק",
    "vessels": r"\bjars?\b|jugs?\b|juglets?\b|\bbowls?\b|\blamps?\b|cooking pot|\bpots?\b|vessels?|\blids?\b|goblet|\bplate\b|pottery",
    "jar": r"\bjars?\b|jarlet",
    "written": r"(?<!scroll )\bscrolls?\b(?! jar)|\btexts?\b|manuscript|papyr|ostrac|inscri|documents?|writing leather|parchment|\bletters?\b",
    "coins": r"\bcoins?\b|prutah|drachm|stater|\bhoard",
    "silver_gold_bars": r"\bsilver\b|\bgold|ingot|\bbars?\b|bullion",
    "heap_boulder": r"(?<!spoil )\bheaps?\b|cairn|boulder|stone pile|pile of stones|tumulus",
    "spring": r"\bspring\b|ʿEin|\bEin\b|מעיין",
    "deposit_signs": r"blocked|sealed|walled|hidden|stored|deposit|robb|plunder|emptied|holes|pits?\b|niche",
}


def djd_table():
    out = {}
    for line in open(DJD, encoding="utf-8"):
        if not line.startswith("| ") or line.startswith("| No.") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        no = cells[0].replace("*", "").split("=")[0].strip()
        if not no.isdigit():
            continue
        out[no] = " ; ".join(cells[2:7])
    return out


def main():
    rows = {r["cave_id"]: r for r in json.load(open(os.path.join(OUT, "all_rows.json"), encoding="utf-8"))}
    inv_ids = sorted({x["cave_id"] for x in csv.DictReader(open(os.path.join(OUT, "inventory.csv"), encoding="utf-8"))})
    djd = djd_table()
    res, texts = {}, {}
    for cid in inv_ids:
        r = rows[cid]
        parts = [r.get(k, "") for k in ("name_number", "feature_type_source", "finds", "notes", "period_stated", "terrace_basis", "pillar_basis", "openings_basis", "facing_basis", "northern_basis", "asi_classes")]
        if cid.startswith("DJD3:"):
            n = cid.split(":")[1]
            if n in djd:
                parts.append("[DJD III table] " + djd[n])
        if cid == "A41:XI/19" and "19" in djd:
            parts.append("[DJD III table site 19 = 2Q] " + djd["19"])
        t = " || ".join(p for p in parts if p)
        texts[cid] = t
        f = {}
        for k, pat in FLAGS.items():
            m = [t[max(0, mm.start() - 40): mm.end() + 40] for mm in re.finditer(pat, t, re.I)]
            if m:
                f[k] = m[:4]
        res[cid] = f
    json.dump(res, open(os.path.join(OUT, "flags_auto.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump(texts, open(os.path.join(OUT, "cave_texts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    from collections import Counter
    print(Counter(k for v in res.values() for k in v))


if __name__ == "__main__":
    main()
