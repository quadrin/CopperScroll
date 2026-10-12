#!/usr/bin/env python3
"""Build the part-F tables (IAA Reports nos. 2-6 and 8-78) from the committed data tables.

Inputs: data/volumes.csv, data/files.csv (from prep_data.py) and the decisions below.
Outputs: screen.csv, held.csv, pdfs_needed.csv, reports.csv and features.csv (headers only in this pass),
summary.json. Standard library only.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_f_iaa_reports/scripts/build_part_f.py [outdir]
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
sys.path.insert(0, str(HERE))
import common_f  # noqa: E402

P2 = common_f.P2
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]

# Unit slugs for every portal item (one monograph on one site = one unit; no volume splits into separate sites).
SLUGS = {
    "1": "akeldama", "2": "yiftahel", "3": "manahat", "4": "chalcolithic-golan", "5": "cave-of-the-warrior",
    "6": "central-negev-i", "7": "jericho-cemetery", "8": "rosh-zayit", "9": "south-sinai-monasteries",
    "10": "korazim", "11": "subayba", "12": "efrata", "13": "tel-teo", "14": "upper-galilee-survey",
    "15": "akhziv", "16": "kissufim-road", "17": "maresha-i", "18": "qiryat-ata", "19": "abu-ghosh",
    "20": "negev-highlands-ii", "21": "tiberias-1973", "22": "tiberias-1989", "23": "tell-beit-mirsim-tombs",
    "24": "ashdod-vi", "25": "tel-yoqneam", "26": "crusader-mamluk-pottery", "27": "shoham-north",
    "28": "tel-bet-yerah-1994", "29": "gamla-i", "30": "bet-yerah-i", "31": "en-esur-i", "32": "tel-mor",
    "33": "nysa-scythopolis-caesareum", "34/1": "kadesh-barnea-text", "34/2": "kadesh-barnea-plates",
    "35": "maresha-ii", "36": "bet-guvrin-necropolis", "37": "paneas-i", "38": "paneas-ii", "39": "tel-moza",
    "40": "paneas-iv", "41": "horbat-uza-i", "42": "horbat-uza-ii", "43": "nahal-haggit", "44": "gamla-ii",
    "45": "maresha-iii", "46": "ramat-bet-shemesh-gazetteer", "47": "ramat-bet-shemesh-landscapes",
    "48": "bet-shean-ii", "49": "marys-well-nazareth", "50": "azor-cemetery", "51/1": "akko-i-text",
    "51/2": "akko-i-plates", "52": "jerusalem-givati-i", "53": "caesarea-circus-architecture",
    "54": "bet-yerah-ii", "55": "bet-dagan", "56": "gamla-iii-1", "57": "caesarea-circus-finds",
    "58/1": "bet-shean-iii-stratigraphy", "58/2": "bet-shean-iii-architecture", "59": "gamla-iii-2",
    "60": "akko-ii", "61": "bet-yerah-iii", "62": "bet-shean-iv", "63": "jerusalem-western-wall-plaza-i",
    "64": "jerusalem-western-wall-plaza-ii", "65": "ashqelon-barnea-i", "66/1": "jerusalem-givati-ii-byzantine",
    "66/2": "jerusalem-givati-ii-early-islamic", "66/3": "jerusalem-givati-ii-finds",
    "67": "jerusalem-western-wall-plaza-iii", "68": "en-esur-iii", "69": "kathisma", "70": "ashqelon-barnea-ii",
    "71": "nahal-tanninim-dam", "72": "akko-iii-1", "73": "akko-iii-2", "74/1": "nysa-scythopolis-hellenistic-1",
    "74/2": "nysa-scythopolis-hellenistic-2", "75": "cana-karm-er-ras", "76": "maresha-iv", "77": "khirbat-amra",
    "78": "paneas-v",
}

# Candidates placed by name (no landing page gives a map reference). INFERENCE: zone from the gazetteer term.
CANDIDATES = {
    "3": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Manahat in the Rephaim Valley"),
    "12": ("Z4_JERUSALEM_HILLS", "title term 'efrata'; abstract: a hill on the Hebron-Jerusalem road"),
    "19": ("Z4_JERUSALEM_HILLS", "title term 'abu ghosh'; abstract: in the Jerusalem Hills"),
    "39": ("Z4_JERUSALEM_HILLS", "title term 'moza'; abstract: Tel Moza, just outside Jerusalem"),
    "52": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Giv'ati Parking Lot, City of David"),
    "63": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Western Wall Plaza, Old City"),
    "64": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Western Wall Plaza (pottery volume)"),
    "66/1": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Givati Parking Lot, Tyropoeon Valley"),
    "66/2": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Givati Parking Lot, Tyropoeon Valley"),
    "66/3": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Givati Parking Lot (finds volume)"),
    "67": ("Z4_JERUSALEM_HILLS", "title term 'jerusalem'; abstract: Western Wall Plaza (small finds, quarries)"),
    "69": ("Z4_JERUSALEM_HILLS", "title terms 'jerusalem', 'bethlehem'; abstract: on the Jerusalem-Bethlehem road"),
}

HELD = {
    "5": {
        "first_line": ("During the survey of the caves in the Jericho area, Cave No. 13 revealed a uniquely "
                       "well-preserved burial dating to the early 4th millennium BCE, accompanied by burial goods "
                       "that have rarely been preserved elsewhere, due to the conditions of the cave."),
        "first_line_source": "landing-page description (abstract), first sentence only",
        "held_area": "Jericho escarpment (cave survey of the Jericho area); exact wadi not established from the first line",
        "zone_by_name": "Z2_JORDAN_VALLEY or Z3_JUDEAN_DESERT (Jericho area; not placed)",
        "tier_if_read": "T1 (region-wide term 'Judean desert' in the title)",
    }
}

ALREADY_READ = {
    "1": "read by the tombs lane on 11 Oct 2026 (research/regional/tombs, sources_access.csv source AK; owner's local copy)",
    "7": "read by the tombs lane on 11 Oct 2026 (research/regional/tombs, sources_access.csv source HK; owner's local copy)",
}
REPO_MENTIONS = {
    "17": "pp. 42-45 read by the columbaria lane (research/regional/columbaria/data/sources_read.csv L3)",
    "36": "ch. 4 seen through indexed publisher text (research/sources/burial_primary_followup_2026-10-01.md); chapter downloads 403 then",
    "45": "cited second-hand through IIP (research/agent_review_2026-10-07/wave1/T07_greek_letters); not read",
    "52": "listed as a target, not read (research/sources/mining_targets_2026-10-11.md)",
}
# Incidental gazetteer hits in abstracts of non-candidates (judged by reading the matched phrase only).
ABSTRACT_HIT_NOTES = {
    "51/1": "abstract hit 'jerusalem' is the Latin Kingdom of Jerusalem; site is Akko",
    "51/2": "abstract hit 'jerusalem' is the Latin Kingdom of Jerusalem; site is Akko",
    "43": "abstract hit 'ramot' is Ramot Menashe (as A3's dropped namesake); site in the southern Carmel",
    "30": "abstract hit 'jordan river' is at the Sea of Galilee outlet; site is Bet Yerah",
}
# Multi-site and thematic volumes: why they give no in-region unit (INFERENCE from the title and keywords).
OUT_NOTES = {
    "4": "regional study of the Golan; outside the region",
    "6": "survey volume of the central Negev; outside the region",
    "9": "survey of South Sinai monasteries; outside the region",
    "14": "survey of Upper Galilee; outside the region",
    "20": "survey volume of the Negev Highlands; outside the region",
    "26": "pottery corpus (thematic), no site report",
    "46": "Ramat Bet Shemesh survey area lies west of the Z4 box (lon < 35.10); no site named in the region",
    "47": "Ramat Bet Shemesh survey area lies west of the Z4 box (lon < 35.10); no site named in the region",
}


def unit_id(no):
    return "IAAR%s-%s" % (no.replace("/", "p"), SLUGS[no])


def tier_of(zone, title):
    if zone in ("Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT"):
        return "T1"
    return "T3" if common_f.norm(title).strip().startswith("jerusalem") else "T2"


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main(outdir=None):
    out = Path(outdir) if outdir else PART
    pats = common_f.patterns()
    vols = read(PART / "data" / "volumes.csv")
    files = read(PART / "data" / "files.csv")
    fhits = {}
    for f in files:
        if f["label_hits"]:
            fhits.setdefault(f["no_label"], []).append("%s [%s]" % (f["label"], f["label_hits"]))
    screen, held, needed = [], [], []
    for v in vols:
        no = v["no_label"]
        uid = unit_id(no)
        th = common_f.fmt_hits(common_f.hits(v["title"], pats))
        row = {"unit_id": uid, "no_label": no, "title": v["title"], "authors": v["authors"],
               "year_portal": v["year"], "landing_url": v["landing_url"], "pdf_url": v["pdf_url"],
               "pdf_size": v["pdf_size"], "pages": "", "n_chapter_files": v["n_files"],
               "title_hits": th, "chapter_title_hits": " | ".join(fhits.get(no, [])),
               "abstract_hits": v["abstract_hits"], "keywords": v["keywords"],
               "repo_status": ALREADY_READ.get(no) or REPO_MENTIONS.get(no, ""),
               "decision": "", "region_zone": "", "coordinate_source": "", "tier": "", "flag": "",
               "reason": ""}
        if no in ALREADY_READ:
            row.update(decision="ALREADY_READ (not re-read)", region_zone="Z4_JERUSALEM_HILLS" if no == "1" else "Z2_JORDAN_VALLEY",
                       coordinate_source="name only",
                       reason="outside part F scope (nos. 2-6 and 8-78); landing page not fetched")
        elif no in HELD:
            h = HELD[no]
            row.update(decision="HELD", region_zone=h["zone_by_name"], coordinate_source="name only",
                       tier=h["tier_if_read"].split()[0], flag="held",
                       reason="cave in a held area (plan section 7): " + h["held_area"])
            held.append({"unit_id": uid, "citation": "%s, %s, IAA Reports %s (Jerusalem: Israel Antiquities Authority, %s)"
                         % (v["authors"], v["title"], no, v["year"]),
                         "landing_url": v["landing_url"], "pdf_url": v["pdf_url"], "first_line": h["first_line"],
                         "first_line_source": h["first_line_source"], "held_area": h["held_area"],
                         "zone_by_name": h["zone_by_name"], "tier_if_read": h["tier_if_read"],
                         "protected_strip": "no", "tier1_kh_almit": "no", "status": "held: not read, not downloaded"})
        elif no in CANDIDATES:
            zone, why = CANDIDATES[no]
            if not th:
                raise SystemExit("candidate without a title hit: " + no)
            row.update(decision="CANDIDATE (in region by name)", region_zone=zone, coordinate_source="name only",
                       tier=tier_of(zone, v["title"]), flag="none", reason=why)
        else:
            if th:
                raise SystemExit("title hit not decided: %s %s" % (no, th))
            note = "; ".join(x for x in (ABSTRACT_HIT_NOTES.get(no, ""), OUT_NOTES.get(no, "")) if x)
            if v["abstract_hits"] and not note:
                raise SystemExit("abstract hit not judged: " + no)
            row.update(decision="OUT_TITLE",
                       reason="no gazetteer or A3 term in the title or chapter titles" + ("; " + note if note else ""))
        screen.append(row)
    # pdfs_needed: candidates only, ordered by tier then ascending sha256(unit id)
    cands = [r for r in screen if r["decision"].startswith("CANDIDATE")]
    for r in cands:
        r["_sha"] = hashlib.sha256(r["unit_id"].encode("utf-8")).hexdigest()
    cands.sort(key=lambda r: (r["tier"], r["_sha"]))
    pos = {}
    for i, r in enumerate(cands, 1):
        pos[r["tier"]] = pos.get(r["tier"], 0) + 1
        needed.append({"order": i, "unit_id": r["unit_id"], "no_label": r["no_label"], "title": r["title"],
                       "authors": r["authors"], "year_portal": r["year_portal"], "landing_url": r["landing_url"],
                       "pdf_url": r["pdf_url"], "pdf_size": r["pdf_size"], "pages": "", "region_zone": r["region_zone"],
                       "tier": r["tier"], "order_within_tier": pos[r["tier"]], "sha256_unit_id": r["_sha"],
                       "held_or_tier1_flag": "none", "n_chapter_files": r["n_chapter_files"],
                       "note": "full-text PDF; chapter PDFs listed in data/files.csv"})
        del r["_sha"]
    sfields = list(screen[0].keys())
    write(out / "screen.csv", sfields, screen)
    write(out / "held.csv", list(held[0].keys()), held)
    write(out / "pdfs_needed.csv", list(needed[0].keys()), needed)
    for name in ("reports.csv", "features.csv"):
        with open(P2 / name, newline="", encoding="utf-8") as f:
            hdr = next(csv.reader(f))
        write(out / name, hdr, [])
    by_tier = {}
    for r in needed:
        by_tier[r["tier"]] = by_tier.get(r["tier"], 0) + 1
    dec = {}
    for r in screen:
        k = r["decision"].split(" ")[0]
        dec[k] = dec.get(k, 0) + 1
    summary = {"portal_items": len(screen), "decisions": dec, "pdfs_needed_by_tier": by_tier,
               "pdfs_needed_total": len(needed), "held": len(held), "units_read": 0, "feature_rows": 0,
               "chapter_files_listed": len(files)}
    (out / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1] if len(sys.argv) > 1 else None), indent=1))
