#!/usr/bin/env python3
"""Write data/landing_decisions.csv: the placement decision for every fetched landing page.

Default rule (plan section 2, report without a map reference): the zone the title names through the gazetteer
(or the manual-screen zone for added names). Overrides below record every decision that needed the landing
page (abstract first lines, keywords) or the portal location map (images.kml); each states its basis.
No landing page gave a map reference. Run once after extract_landing.py; the output is committed.

  python3 -I make_decisions.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import landing_list  # noqa: E402
import screen_lib as L  # noqa: E402

DATA = L.PART / "data"
FIELDS = ["volume", "item_no", "decision", "zone", "zone_basis", "held", "held_area", "tier1_kh_almit",
          "protected_strip", "first_line_seen", "article_kind", "note"]

Z1, Z2, Z3, Z4 = "Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"
RW = "REGION_WIDE (unplaced)"

# (volume, item) -> (decision, zone, basis, note); decision in {in, out, unlocated, held}
OVR = {
    ("42", "33"): ("in", Z3, "name: 'En 'Aneva, the place located in Z3 by phase-2 ESI02-029 (OIG 18225/08435)", "landing page has no abstract or location"),
    ("43", "3"): ("unlocated", "", "", "Khirbet Nisya: no abstract, keywords or map point on the portal; place not in the gazetteer"),
    ("46", "12"): ("unlocated", "", "", "Nahal Samtar (Vered Quarry): no abstract, keywords or map point on the portal"),
    ("52", "55"): ("unlocated", "", "", "Khirbat Kabar, 'northern Hebron Hills' (title); abstract gives no location; may lie south of the Z4 limit"),
    ("53", "8"): ("out", "", "", "landing keywords: Shephelah, Judea (west of the region)"),
    ("53", "11"): ("out", "", "", "landing keywords: Galilee, Hula Valley"),
    ("53", "27"): ("out", "", "", "landing keywords: Sharon plain"),
    ("117", "9"): ("out", "", "", "Khirbat Ibreika, Sharon plain (see 53.27); portal map point 32.2026, 34.9584 outside all zones"),
    ("56", "4"): ("out", "", "", "abstract: southern coastal plain"),
    ("56", "6"): ("in", Z4, "portal location map point 31.7251, 35.1531 (images.kml)", "abstract: near the village of El-Wallaja (gazetteer walaja), Jerusalem periphery"),
    ("56", "9"): ("out", "", "", "abstract: east of Nahariyya, Western Galilee"),
    ("59", "3"): ("in", Z4, "title: Jerusalem (gazetteer); the Z1 hit 'luza' is the spring name 'Ein el-Luza", "abstract: south of the Hinnom-Kidron confluence, Jerusalem; caves not in a held area"),
    ("62", "27"): ("out", "", "", "abstract: Ramat Ha-Nadiv, between Zikhron Ya'aqov and Binyamina"),
    ("63", "2"): ("in", Z4, "abstract: some 8 km north of Jerusalem (gazetteer jerusalem)", ""),
    ("66", "10"): ("out", "", "", "abstract: northwestern outskirts of Baqa el-Gharbiya"),
    ("67", "6"): ("out", "", "", "abstract: near Kefar Tavor"),
    ("69", "3"): ("out", "", "", "abstract: Modi'in Region Industrial Zone"),
    ("70", "2"): ("out", "", "", "abstract: Horbat Burin in the northern Sharon plain, not Burin near Nablus"),
    ("70", "3"): ("out", "", "", "Horbat Burin (East), northern Sharon plain (see 70.2)"),
    ("70", "10"): ("unlocated", "", "", "Horbat Biz'a: abstract and keywords give no location; no map point"),
    ("71", "9"): ("unlocated", "", "", "Khirbat el-Thahiriya: abstract and keywords give no location; no map point"),
    ("75", "6"): ("out", "", "", "abstract: foot of the Hebron Hills, 1 km south of Tell Beit Mirsim"),
    ("101", "3"): ("unlocated", "", "", "Horbat 'Alona: abstract says Nahal Soreq valley, Jerusalem's agricultural hinterland; no point; may lie west of 35.10"),
    ("101", "4"): ("unlocated", "", "", "Horbat 'Alona finds (see 101.3)"),
    ("101", "5"): ("unlocated", "", "", "Horbat 'Alona finds (see 101.3)"),
    ("89", "4"): ("in", Z4, "title: Nahal Qidron, Jerusalem; abstract: salvage excavation by Nahal Qidron, Jerusalem", "title also matched Z3 'nahal qidron'; the Jerusalem stretch is in Z4 (INFERENCE)"),
    ("89", "5"): ("in", Z4, "title: Nahal Qidron, Jerusalem; abstract: south of Jerusalem", "same site as 89.4"),
    ("89", "6"): ("in", Z4, "title: Nahal Qidron, Jerusalem", "same site as 89.4"),
    ("89", "7"): ("in", Z4, "title: Nahal Qidron, Jerusalem", "same site as 89.4"),
    ("89", "8"): ("in", Z4, "title: Nahal Qidron, Jerusalem", "same site as 89.4"),
    ("110", "8"): ("in", Z4, "abstract: excavations at Herodium (gazetteer herodium)", "manual check: no place in the title"),
    ("110", "9"): ("in", RW, "title: region-wide term 'Dead Sea' (Dead Sea Scrolls); portal map point at Kh. Qumran 31.7415, 35.4598", "laboratory study of inkwell residues; held check at first line when read (Qumran)"),
    ("116", "8"): ("in", RW, "title: region-wide term 'Judean Desert'; portal map point at Kh. Qumran 31.7415, 35.4598", "laboratory study of tefillin and mezuzah skins; first line names the Dead Sea Scrolls, not a cave; held check at first line when read"),
    ("110", "19"): ("out", "", "", "'Latin Kingdom of Jerusalem' is a polity; country-wide epigraphic synthesis, not a place in the region"),
    ("112", "10"): ("out", "", "", "'Kingdom of Jerusalem' is a polity; synthesis of Fatimid hoards across Palestine (abstract), not a place in the region"),
    ("112", "4"): ("in", Z3, "title: Murabba'at (gazetteer); abstract: northern bank of Nahal Darga c. 2 km west of the Dead Sea", "Murabba'at is not in a held cave area (plan section 7)"),
    ("112", "6"): ("unlocated", "", "", "Nahal Shalva: abstract and keywords give no location; no map point"),
    ("114", "2"): ("in", Z4, "abstract: winepresses at 'Emeq Lavan, Rogem Gannim and Mordot Arnona in Jerusalem", "manual check: 'Valley of the King' in title"),
    ("114", "3"): ("in", RW, "title: region-wide term 'Samaria' (southern Samaria; abstract: desert fringes)", "survey synthesis; sites may fall in Z3 north box or outside"),
    ("119", "5"): ("out", "", "", "abstract: 'Enot Zippori, c. 2 km west of Nazareth"),
    ("119", "8"): ("out", "", "", "title and abstract: Western Samaria, west of the Z1 and Z3 boxes"),
    ("119", "11"): ("out", "", "", "abstract and keywords: southern coastal plain, Ashqelon"),
    ("120", "4"): ("out", "", "", "abstract: tower near Poriyya above the northern Jordan Valley, north of Z2"),
    ("108", "13"): ("in", Z4, "portal location map point 31.8024, 35.1063 (images.kml); title: near Abu Ghosh", "point lies 0.006 degrees inside the Z4 west limit"),
    ("117", "2"): ("in", Z4, "portal location map point 31.8394, 35.1850 (images.kml); title: Nebi Samwil", ""),
    ("121", "9"): ("in", Z4, "title: Jerusalem area (gazetteer jerusalem)", "synthesis of rural Crusader sites around Jerusalem"),
    ("120", "6"): ("in", Z4, "title: Jerusalem (run together as 'Jerusalemin' on the portal)", "GIS synthesis of access routes"),
}


def default(x, man):
    h = L.hits(x["title"], L.patterns())
    zs = [z for z in ("Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS") if z in h]
    m = man.get((x["volume"], x["item_no"]))
    if m and m["zone_by_name"]:
        return ("in", m["zone_by_name"], "name in title (manual screen): " + m["reason"].replace("manual screen: ", ""), "")
    if len(zs) == 1:
        return ("in", zs[0], "title names %s (gazetteer, plan section 2)" % ", ".join(h[zs[0]]), "")
    raise SystemExit("no default for %s.%s: %s" % (x["volume"], x["item_no"], h))


def main():
    man = {(r["volume"], r["item_no"]): r for r in csv.DictReader(open(DATA / "screen_manual.csv", encoding="utf-8"))}
    meta = {(r["volume"], r["item_no"]) for r in csv.DictReader(open(DATA / "landing_meta.csv", encoding="utf-8"))}
    out = []
    for x in landing_list.candidates():
        k = (x["volume"], x["item_no"])
        if k not in meta:
            raise SystemExit("landing page missing for %s.%s" % k)
        d, z, basis, note = OVR.get(k) or default(x, man)
        out.append({"volume": k[0], "item_no": k[1], "decision": d, "zone": z, "zone_basis": basis,
                    "held": "no", "tier1_kh_almit": "no", "protected_strip": "no", "note": note or basis or "in region by title"})
    with open(DATA / "landing_decisions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(len(out))


if __name__ == "__main__":
    main()
