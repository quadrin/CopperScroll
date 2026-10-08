#!/usr/bin/env python3
"""Derive per-entry features of the Copper Scroll (3Q15) used for hoard matching.

Inputs (shared, project-supplied): entries.json, places.json, landmark_lexicon_index.csv
Output: entry_features.json / entry_features.csv in the T02 results folder.

Feature sources
- landmark classes: the project's landmark_lexicon_index.csv (entries_puech column) mapped to
  coarse classes (table LEX2CLASS below) + a few text keyword rules.
- containers / contents: regexes on the Abegg/ETCBC Hebrew of the entry's lines.
- amount + unit form: numerals from the project's English translation; unit form from the Hebrew
  ('ככרין' full spelling vs bare 'ככ' abbreviation).  Only the abbreviated form is subject to the
  karsh reading (Lefkovits 2000 App. A p. 481; Puech 2006 I p. 174 n. 40, as summarised in the
  project's findings_log F1.6).
- depth: 'dig N cubits' numerals from the English.
- position cues: keywords in the English.
All of this is mechanical and approximate; numerals depend on the project translation.
"""
import csv
import json
import os
import re
import sys

BASE = "session-scratch/cs"
SHARED = os.path.join(BASE, "shared")
OUT = os.path.join(BASE, "results", "T02_hoard_match")

LEX2CLASS = {
    "bor": "cistern", "shit": "pit", "shuhah": "pit", "berekhah": "pool", "ashiah": "reservoir",
    "ammah_conduit": "conduit", "mazqa": "conduit", "biv": "conduit", "zarav": "conduit",
    "harits": "conduit", "qibbuts": "reservoir", "yam_basin": "basin", "mayan": "spring",
    "mabbua": "spring", "shoqet": "basin", "yetsiat_mayim": "outlet", "qol_mayim": "outlet",
    "miqveh_tevilah": "pool",
    "qever": "tomb", "kokh": "tomb", "beit_mishkav": "tomb", "mishkan": "tomb", "nefesh": "monument",
    "yad": "monument",
    "mearah": "cave", "sedeq": "fissure", "tseriah": "chamber", "shovakh": "dovecote",
    "hatser": "court", "peristylon": "court", "ganah": "court", "otsar": "building", "migreh": "building",
    "stoa": "building", "exedra": "building", "metsad": "fortress", "aliyah": "building",
    "mishtah": "fortress", "maalot": "steps", "mesibbah": "steps", "saf": "threshold", "biah": "threshold",
    "mavo": "threshold", "petah": "threshold", "pinnah": "corner", "miqtsoa": "corner", "amud": "pillar",
    "even": "stone", "masma": "stone", "madaf": "stone", "homah": "wall", "nidbakh": "wall",
    "sela": "rock", "shen_sela": "rock", "tel": "mound", "horebbah": "ruin", "yagar": "cairn",
    "regev": "cairn", "emeq": "valley", "gay": "valley", "nahal": "valley", "tsuq": "valley",
    "shelaf": "field", "rewi": "field", "havalah": "field", "derekh": "road", "migzat": "road",
}

NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
       "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
       "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
       "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}


def words_to_num(s):
    s = s.lower().replace("-", " ").replace(",", " ")
    toks = [t for t in s.split() if t not in ("and",)]
    total, cur = 0, 0
    seen = False
    for t in toks:
        if t.isdigit():
            cur += int(t); seen = True
        elif t.endswith("½") and t[:-1].isdigit():
            cur += int(t[:-1]) + 0.5; seen = True
        elif t in NUM:
            cur += NUM[t]; seen = True
        elif t == "hundred":
            cur = (cur or 1) * 100; seen = True
        elif t == "thousand":
            total += (cur or 1) * 1000; cur = 0; seen = True
        else:
            break
    return total + cur if seen else None


NUMWORD = r"((?:\d+(?:½)?|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|and|[-\s])+))"


def lex_index():
    m = {}
    with open(os.path.join(SHARED, "landmark_lexicon_index.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            cls = LEX2CLASS.get(r["term_id"])
            if not cls:
                continue
            for tok in re.findall(r"\b(\d+a?)\b", r["entries_puech"].split("(")[0]):
                m.setdefault(tok, set()).add(cls)
    return m


def main():
    entries = json.load(open(os.path.join(SHARED, "entries.json")))
    places = {p["id"]: p for p in json.load(open(os.path.join(SHARED, "places.json")))}
    lex = lex_index()
    out = []
    for e in entries:
        eid = e["entry"]
        heb = " ".join(l["hebrew"] for l in e["lines"])
        eng = " ".join(l["english"] for l in e["lines"])
        eng = re.sub(r"[\[\]…]", "", eng).replace("(", "").replace(")", "")
        eng = re.sub(r"\s+", " ", eng)
        engl = eng.lower()
        lm = set(lex.get(eid, set()))
        # containers
        cont = set()
        if re.search(r"שד[הא]|שדת", heb): cont.add("chest")
        if re.search(r"כדין|בדין", heb): cont.add("jar")        # kaddin 'jars' (Puech: bars)
        if re.search(r"קלל", heb): cont.add("jar")
        if re.search(r"דודין", heb): cont.add("pot")
        if re.search(r"כוזין", heb): cont.add("juglet")
        # contents
        cnt = set()
        if "כסף" in heb or "כספ" in heb: cnt.add("silver")
        if "זהב" in heb: cnt.add("gold")
        if "עשתות" in heb: cnt.add("ingots")
        if re.search(r"כלי|כלין|כאלין|כלכליה|כליה|מזרקות|כוסות|קסאות|כפורין", heb): cnt.add("vessels")
        if "דמע" in heb: cnt.add("offering")
        if re.search(r"ספר|כתב", heb) and eid != "34": cnt.add("scroll_or_record")
        if "לבושין" in heb: cnt.add("garments")
        if "אסתרין" in heb: cnt.add("staters")
        if "חרם" in heb: cnt.add("devoted")
        # amount & unit form
        has_full = bool(re.search(r"ככרין|(^|\s)ככר(\s|$)", heb))
        has_abbr = bool(re.search(r"(^|\s)ככ(\s|$)", heb))
        unit_form = "mixed" if (has_full and has_abbr) else ("full" if has_full else ("abbr" if has_abbr else "none"))
        amounts = [words_to_num(m.group(1)) for m in re.finditer(NUMWORD + r"\s+talents", eng)]
        amounts = [a for a in amounts if a]
        talent_total = sum(amounts) if amounts else None
        unspecified_metal = bool(talent_total) and not ({"silver", "gold"} & cnt)
        if unspecified_metal:
            cnt.add("unspecified_amount")
        # depth
        depth = None
        m = re.search(r"dig\s+(?:[a-z ]{0,25}?\s)?" + NUMWORD + r"\s*(?:and a half\s*)?cubit", engl)
        if m:
            depth = words_to_num(m.group(1))
        elif re.search(r"dig a cubit", engl):
            depth = 1
        # position cues
        pos = set()
        for k in ("north", "south", "east", "west"):
            if re.search(r"\b" + k, engl): pos.add(k)
        if "corner" in engl: pos.add("corner")
        if re.search(r"under (the )?(great |black )?(stone|slab)|on the stone", engl): pos.add("under_stone")
        if re.search(r"threshold|entrance|opening|as you go in", engl): pos.add("threshold")
        if "floor" in engl: pos.add("floor")
        if re.search(r"course of stones|wall", engl): pos.add("wall")
        if "upper storey" in engl: pos.add("upper_storey")
        if "pillar" in engl: pos.add("pillar")
        if "steps" in engl or "stair" in engl: pos.add("steps")
        if re.search(r"tomb|dead", engl): lm.add("tomb")
        if "cave" in engl: lm.add("cave")
        if "guard post" in engl: lm.add("fortress")
        if "house" in engl or "bathhouse" in engl: lm.add("building")
        cands = []
        for c in e["candidates"]:
            p = places.get(c["placeId"], {})
            cands.append({"placeId": c["placeId"], "status": c["status"], "lat": p.get("lat"), "lon": p.get("lon"),
                          "precision": p.get("precision"), "region": p.get("region")})
        out.append({
            "entry": eid, "title": e["title"], "confidence": e["confidence"],
            "landmarks": sorted(lm), "containers": sorted(cont), "contents": sorted(cnt),
            "amount_talents_as_translated": talent_total, "unit_form": unit_form,
            "depth_cubits": depth, "position_cues": sorted(pos), "candidates": cands,
            "hebrew": heb, "english": eng,
        })
    json.dump(out, open(os.path.join(OUT, "entry_features.json"), "w"), ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "entry_features.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["entry", "title", "landmarks", "containers", "contents", "amount", "unit_form", "depth_cubits",
                    "position_cues", "candidate_places"])
        for r in out:
            w.writerow([r["entry"], r["title"], ";".join(r["landmarks"]), ";".join(r["containers"]),
                        ";".join(r["contents"]), r["amount_talents_as_translated"], r["unit_form"], r["depth_cubits"],
                        ";".join(r["position_cues"]), ";".join(c["placeId"] for c in r["candidates"])])
    print(len(out), "entries")


if __name__ == "__main__":
    main()
