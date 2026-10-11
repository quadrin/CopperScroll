"""Clean the draft Index crosswalk into coded/a41_index_crosswalk.csv (ids and short names only)."""
import csv, re, sys

src, dst = sys.argv[1], sys.argv[2]
heb = re.compile(r"[֐-׿׳״']+")
rows = list(csv.DictReader(open(src, encoding="utf-8")))
out = []
for r in rows:
    reg, cells, eng = r["region"], r["cells"], r["english"]
    no_1993, code, nick = "", "", ""
    m_sec = re.search(r"((Northern|Southern) section.*)$", eng)
    if reg in ("IV", "VI"):
        if m_sec:
            no_1993 = re.sub(r"\s+", " ", m_sec.group(1)).replace("N0.", "No.").replace("Unit I", "Unit 1").replace("Unit l", "Unit 1")
            nick = eng[: m_sec.start()].strip()
    elif reg == "XIV":
        nick = eng
    else:
        parts = [p.strip() for p in cells.replace("||", "|").split("|") if p.strip()]
        for p in parts:
            q = p.replace("א", "a").replace("ב", "b") if re.fullmatch(r"[אב]\d+", p) else p
            q2 = heb.sub("", q).strip(" ,'")
            if re.fullmatch(r"[ABC]\s?[0-9lI]+[ab]?|C7a,C7|C4-1|\)?A[0-9t]\(?|\^5\(", q2):
                code = q2
            elif re.fullmatch(r"\d+[A-Z]?|\d+a|\d+b|(South|North)\s?\d+", q2):
                no_1993 = q2.replace("South6", "South 6")
            elif re.fullmatch(r"[a-z]?\d+", q2):
                no_1993 = q2
        if reg == "II" and not no_1993:
            m = re.search(r"(South|North)\s?\d+", cells)
            no_1993 = m.group(0) if m else ""
        nick = re.sub(r"Under survey permit|Under L-\d+", "", eng).strip()
        m_code = re.search(r"\((A ?\d)\s?\)", nick)
        if m_code:
            code = m_code.group(1).replace(" ", "")
            nick = nick[: m_code.start()].strip()
    if reg == "X" and r["pub_id"] == "A41:X/59":
        code = "A5"
    if reg == "X" and r["pub_id"] == "A41:X/60":
        code, nick = "A1", "Cave of the Button"
    if r["pub_id"] == "A41:X/35":
        nick = "The Cave of the Balsam Oil Juglet"
    out.append({"pub_id": r["pub_id"], "no_1993": no_1993, "code_1993": code, "permit": r["permit"],
                "nickname_en": nick.strip()})
# Hand fixes after checking the text layer against the Hebrew column (OCR slips noted).
FIX = {
    "A41:IV/6": {"no_1993": "Northern section, Unit 3, No. 15 (Hebrew column; English printed 'No. 18')"},
    "A41:IV/11": {"nickname_en": "Cave of the Pillar"},
    "A41:IV/12": {"nickname_en": "(Niche No. 1)"},
    "A41:IV/14": {"no_1993": "Northern section, sub-section of fault escarpment, Unit 1, No. 7"},
    "A41:IV/17": {"nickname_en": "Cave with the Masonry Wall"},
    "A41:IV/18": {"nickname_en": "The Dagger Niche"},
    "A41:VI/37": {"no_1993": "Southern section, Unit 3, No. 7"},
    "A41:VI/43": {"nickname_en": "(Cave No. 2)"},
    "A41:VI/44": {"no_1993": "Southern section, Unit 2, No. 7"},
    "A41:VI/46": {"no_1993": "Southern section, Unit 1, No. 8 (Hebrew column; English printed 'Unit 3, No. 1')", "nickname_en": "(Cave No. 8)"},
    "A41:VI/52": {"no_1993": "Southern section, Unit 1, No. 12 (Hebrew column; English printed 'No. 13')"},
    "A41:X/7": {"no_1993": "7"},
    "A41:XI/10": {"code_1993": "B11"},
    "A41:XI/18": {"no_1993": "35a"},
    "A41:XI/19": {"no_1993": "35b"},
    "A41:XV/3": {"code_1993": "A1"},
}
XIV_NICK = {"2": "Kidron (South) Site", "6": "Amnon's Cave", "7": "The Large Mouth Cave", "8": "Cave of the Crescent",
            "18": "Cave of the Coin", "47": "The Square Mouth Cave"}
seen = set()
final = []
for o in out:
    if o["pub_id"].startswith("A41:XIV/"):
        n = o["pub_id"].split("/")[1]
        if not n.isdigit() or int(n) > 61:
            continue
        o["nickname_en"] = XIV_NICK.get(n, "")
    o.update(FIX.get(o["pub_id"], {}))
    o["nickname_en"] = o["nickname_en"].replace("’", "'").replace("TThe", "The") if o["nickname_en"] else ""
    if o["pub_id"] in seen:
        continue
    seen.add(o["pub_id"])
    final.append(o)
with open(dst, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(final[0].keys()))
    w.writeheader()
    w.writerows(final)
print(len(final))
