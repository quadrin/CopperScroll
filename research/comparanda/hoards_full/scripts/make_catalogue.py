#!/usr/bin/env python3
"""One-off: create hoards.csv from the precedent's comparanda.csv plus the coding added in this lane.

Run once on 11 October 2026 UTC. After that, hoards.csv is the master file and is edited by hand;
`hoards_full.py build` recomputes its derived columns and `tests/` check that precedent rows keep the
precedent's coding except the documented recode.

Usage (from the repository root):
  python3 -I research/comparanda/hoards_full/scripts/make_catalogue.py <chre_years.json> <out.csv>

<chre_years.json> holds the CHRE "Date of discovery (from)" year and terminal years parsed from the
CHRE detail pages cached in the scratch folder (not committed). All coding below is INFERENCE from
the quoted wording, which is EVIDENCE. Quotes are 12 words or fewer.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREC = os.path.join(HERE, "..", "concealment_contexts", "comparanda.csv")

PREC_INPUT = ["id", "site", "lat", "lon", "country", "date_from", "date_to", "object_type", "container",
              "setting", "placement", "context_reported", "how_found", "source", "cluster_id", "include",
              "exclusion_reason", "flags", "judaea_by_name", "t02_id"]
NEW_INPUT = ["origin", "first_read", "unexposed_at_freeze", "object_class", "temple_related", "depth_m",
             "depth_datum", "depth_text", "landmark", "landmark_text", "discovery_year", "terminus_text",
             "sources_pages", "recode_reason", "prec_setting", "prec_placement", "prec_include", "prec_date"]

# ------------------------------------------------------------------ landmark coding (PLAN 10)
# (classes, quote <= 12 words, where the wording was read)
LANDMARK = {
    "chre5386": ("corner", "found in the NE corner of the NW room",
                 "CHRE 5386 site comment, quoting Leibner 2010, 225"),
    "chre5387": ("corner", "in the northwestern corner of the room",
                 "CHRE 5387 site comment, quoting Leibner and Bijovsky 2013, 118"),
    "chre7288": ("corner", "niche is located in the southwestern corner of the main hall",
                 "CHRE 7288 associated features, quoting Farhi et al. 2010, 61-2"),
    "chre7495": ("wall_face", "The hoard was found in the wall of a Jewish house",
                 "CHRE 7495 site comment"),
    "chre7496": ("threshold", "inside the hollow part of a doorframe in the tepidarium",
                 "CHRE 7496 site comment"),
    "chre7596": ("wall_face", "between two pieces of rock adjacent to the western wall",
                 "CHRE 7596 site comment, quoting Zissu et al. 2011, 268-9"),
    "chre7601": ("wall_face", "between the second wall in the west and the corridor",
                 "CHRE 7601 site comment, quoting Baruch 2000, 63"),
    "chre7631": ("corner", "discovered in the corner of Room 30",
                 "CHRE 7631 site comment; Porat et al., INJ 17 (2009-10), 98"),
    "chre7692": ("threshold", "to the right of the door on entering",
                 "CHRE 7692 site comment (de Vaux 1956, 567)"),
    "chre18786": ("threshold", "to the right of the door on entering",
                  "CHRE 18786 site comment (de Vaux 1956, 567)"),
    "chre18785": ("threshold;wall_face", "to the right of the door's entrance. Against the north wall",
                  "CHRE 18785 site comment"),
    "chre7703": ("threshold", "scattered on the threshold of one of the shops",
                 "CHRE 7703 site comment, quoting Bijovsky 2009, 74"),
    "chre7704": ("corner;wall_face", "Immediately below this floor and at the corner of the wall",
                 "CHRE 7704 site comment, quoting Hamburger 1959, 133"),
    "chre7832": ("threshold", "under the doorway of the great room",
                 "CHRE 7832 site comment, quoting Kelso 1950, 20"),
    "chre8172": ("threshold", "within a natural crevice at the threshold of the door",
                 "CHRE 8172 site comment, quoting Bijovsky 2004, 244"),
    "chre8178": ("wall_face", "A hoard was found in the wall of a building",
                 "CHRE 8178 comment, quoting Zissu and Eshel 2000-2, 165"),
    "chre8469": ("threshold", "at the entrance to one of the grain-storage installations",
                 "CHRE 8469 site comment (HA 7-8, 197)"),
    "chre18771": ("corner", "concealed in the corner of a room",
                  "CHRE 18771 site comment"),
    "chre18784": ("threshold", "located in the entrance of the fortified tower",
                  "CHRE 18784 site comment"),
    "t02H18": ("wall_face", "next to a collapsed wall in the food-preparation area",
               "T02 H18; Live Science 5 Jan 2025 (Univ. of Haifa statement)"),
    "t02H22": ("threshold", "a basket of bronze vessels ... at the cave entrance",
               "T02 H22 (Wikipedia, Cave of Letters)"),
    "t02X05": ("wall_face", "in a rock crevice, against a wall",
               "T02 X05; IAA via Israel National News 213378 (7 Jun 2016)"),
}
LANDMARK_NOTE = {
    "chre7698": "found scattered on the floor; Meshorer 1989, 74 thinks originally hidden in the wall",
    "chre8044": "'entrance room' names the room, not a placement",
}

# ------------------------------------------------------------------ depth coding (PLAN 9)
DEPTH = {
    "chre7288": (3.5, "feature_top", 'hoard niche "3.5 m below the shaft leading into the hall"; '
                 'also "0.5 m above the beaten chalk floor"', "CHRE 7288, quoting Farhi et al. 2010, 61-2"),
    "chre7813": (1.55, "present_surface", 'shaft "to a depth of about 1.8 m"; hoard '
                 '"some 20-30 cm above the floor" (1.8 - 0.25 = 1.55, computed)',
                 "CHRE 7813, quoting Farhi and Melamed 2014, 113"),
    "chre8472": (0.4, "present_surface", '"At 40 cm, a beaten earth floor"; purse "found at this depth"',
                 "CHRE 8472, quoting Porat et al. 2007, 38"),
    "chre8474": (0.2, "present_surface", 'under a large stone, "at a depth of about 20 cm"',
                 "CHRE 8474, quoting Porat et al. 2003-6, 83"),
    "chre7732": (0.5, "feature_top", 'underneath "a thick (at least 50 cm) undisturbed layer of quarry chips"'
                 ' (minimum)', "CHRE 7732, quoting Ariel et al. 2014, 152-153"),
}

# ------------------------------------------------------------------ recodes (PLAN 8)
RECODE = {
    "chre8178": {"placement": "wall_cavity",
                 "reason": "CHRE comment quotes Zissu and Eshel 2000-2, 165: hoard 'found in the wall of a "
                           "building'; precedent had not_stated"},
}

EXTRA_FLAGS = {
    "chre7617": "Atiqot 112 abstract (Abadi-Reiss et al.): hoard lay near a female skeleton in the pit; "
                "grave-good status not stated",
    "t02H20": "Atiqot 112 abstract (Klein et al.): wooden box 'in a crevice near a shaft'",
    "chre8095": "= Noe 1925 p. 228-229 'Unknown loc. (Palestine)', 18+ AR (same hoard)",
    "chre8079": "= Noe 1925 p. 41 'Bittir, Palestine, 1889' (Chebron, see Bittir)",
    "chre8091": "= Noe 1925 p. 102 'Jerusalem', 120-500 AR",
    "chre8097": "= Noe 1925 p. 170 'Samaria, 1910'",
}


def object_class(r):
    ot = r["object_type"]
    if ot.startswith("documents"):
        return "documents"
    if ot.startswith("metal"):
        return "metal_objects"
    if r["id"] == "chre7617":
        return "coins_and_metal"
    return "coins"


def new_rows():
    base = {k: "" for k in PREC_INPUT + NEW_INPUT}

    def row(**kw):
        r = dict(base)
        r.update(origin="new", first_read="after_freeze", unexposed_at_freeze="0", temple_related="0",
                 include="1", judaea_by_name="0")
        r.update({k: str(v) for k, v in kw.items()})
        if not r["cluster_id"]:
            r["cluster_id"] = r["id"]
        return r

    noe = "Noe, A Bibliography of Greek Coin Hoards (NNM 25, 1925)"
    hendin = "Hendin, Guide to Biblical Coins, 6th ed. (ANS 2021)"
    wiki = ("Wikipedia, 'List of the Dead Sea Scrolls' and 'Qumran Caves' (read 11 Oct 2026): "
            "https://en.wikipedia.org/wiki/List_of_the_Dead_Sea_Scrolls")
    out = [
        row(id="n01_haifa1906", site="HAIFA 1906 (Noe: 'Haiffa, Syria, 1906')", country="Israel",
            date_from=-145, date_to=-125, object_type="coins (silver)", setting="unknown", placement="not_stated",
            how_found="unknown", source=f"{noe}, p. 99 s.v. Haiffa (Tourneur 1906; Dupriez sale 1906)",
            object_class="coins", discovery_year=1906,
            terminus_text="latest named issues Demetrius II Nicator (145-138, 129-125 BCE)",
            sources_pages=f"{noe}, p. 99", flags="38+ tetradrachms; date = reigns of the latest king named"),
        row(id="n02_nablus1891", site="NABLUS 1891? (Noe: 'Naplus, Palestine, 1891?')",
            country="Palestinian Territories", date_from=-125, date_to=-125, object_type="coins (silver)",
            setting="unknown", placement="not_stated", how_found="unknown",
            source=f"{noe}, p. 141 s.v. Naplus (Hamburger sale 1892)", object_class="coins",
            discovery_year=1891, terminus_text="Noe: burial c. 125 B.C.", sources_pages=f"{noe}, p. 141",
            flags="c. 400 AR, dispersed; find year queried by Noe; distinct from CHRE 8036 (Nablus 1930-36)"),
        row(id="n03_rafah1968", site="RAFAH 1968 / Gaza Strip (IGCH 1609)", country="Palestinian Territories",
            date_from=-99, date_to=-98, object_type="coins (silver)", setting="unknown", placement="not_stated",
            how_found="unknown",
            source="Gitler and Master, INR 5 (2010) 67-98, at pp. 88 and 90-91, citing IGCH p. 222 no. 1609 "
                   "= CH IX p. 59 no. 550 (IGCH and CH not read)",
            object_class="coins", discovery_year=1968,
            terminus_text="latest coins autonomous Ascalon tetradrachms of year 6 (99/8 BCE), per Gitler and Master",
            sources_pages="Gitler and Master 2010, pp. 88, 90-91 (read via academia.edu/367783)",
            flags="closing date from the coins Gitler and Master cite; full IGCH entry not read"),
        row(id="n04_barag1988", site="HASMONEAN 'YEHOHANAN' HOARD (Jerusalem dealer, 1988)",
            country="Israel, Palestinian Territories (dealer in Jerusalem; findspot unknown)",
            date_from=-135, date_to=-104, object_type="coins (1,021) and eight small objects",
            setting="unknown", placement="not_stated", how_found="looting_recovered",
            source=f"{hendin}, pp. 140-141 (Barag's account; 1,021 coins examined at the Hebrew University)",
            object_class="coins", discovery_year=1988,
            terminus_text="no coin of Jannaeus; latest Yehohanan (Hyrcanus I, 135-104 BCE) per Hendin",
            sources_pages=f"{hendin}, pp. 140-141",
            flags="acquired from an antiquities dealer; date = reign of the latest ruler represented"),
    ]
    for i, note in enumerate(["at least 50 pieces", "at least 50 pieces", "possibly smaller"], 1):
        out.append(row(
            id=f"n0{4 + i}_jannaeus_lead{i}", site=f"JANNAEUS LEAD-TOKEN HOARD {i} (Hendin)",
            country="Jordan (dealer attribution: 'may have originated in Jordan')",
            date_from=-79, date_to=-78, object_type="coins (lead tokens of Alexander Jannaeus)",
            setting="unknown", placement="not_stated", how_found="looting_recovered",
            source=f"{hendin}, p. 174 and p. 485 n. 129", object_class="coins",
            terminus_text="lead issue of Jannaeus 'in about 79/78 bce' (Hendin p. 174)",
            sources_pages=f"{hendin}, p. 174; p. 485 n. 129",
            flags=f"Hendin examined portions of three 'true hoards'; this one {note}"))
    out += [
        row(id="n08_swords2023", site="EN GEDI NATURE RESERVE, ROMAN SWORDS CACHE (2023)",
            country="Israel", judaea_by_name=1, date_from=132, date_to=136,
            object_type="metal objects (four swords, a pilum head)", container="wooden scabbards (three swords)",
            setting="cave", placement="not_stated",
            context_reported="pilum in 'a hidden narrow crevice'; swords found soon after",
            how_found="excavation",
            source="Religion News Service, 8 Sep 2023, https://religionnews.com/2023/09/08/roman-swords-in-the-judean-desert/ "
                   "(IAA press conference 6 Sep 2023)",
            object_class="metal_objects", discovery_year=2023, landmark="none_stated",
            terminus_text="IAA links the cache to the Bar Kokhba revolt (CLAIM); C-14 pending when reported",
            sources_pages="RNS 8 Sep 2023 (web page)",
            flags="weapons as valuables (PLAN 4 clarification); a Bar Kokhba coin found in the cave"),
        row(id="n09_iaa2021_cache", site="JUDEAN DESERT, BAR KOKHBA COIN CACHE (IAA, 2021)",
            country="Israel, Palestinian Territories", judaea_by_name=1, date_from=132, date_to=136,
            object_type="coins", setting="unknown", placement="not_stated",
            context_reported="'a cache of rare coins'; cave not named", how_found="excavation",
            source="IAA press release, 16 Mar 2021, via Embassy of Israel London: https://embassies.gov.il/london/"
                   "NewsAndEvents/Pages/New-scroll-fragments-uncovered-in-the-Judean-Desert-Nature-Reserve-.aspx",
            object_class="coins", discovery_year=2021, terminus_text="Bar Kokhba coins (harp, date palm)",
            sources_pages="IAA release (web page)",
            flags="Operation Scroll find; release names no cave and no context"),
    ]
    qum = [("2Q", "unknown", 1952, "about 33 manuscripts listed"),
           ("4Q", "looting_recovered", 1952, "about 500 texts; cave cut into the marl terrace"),
           ("5Q", "looting_recovered", 1952, "about 25 manuscripts listed; source says found by Bedouin"),
           ("6Q", "looting_recovered", 1952, "about 31 manuscripts listed"),
           ("7Q", "excavation", 1955, "Greek fragments; collapsed marl cave (1955 terrace survey)"),
           ("8Q", "excavation", 1955, "five manuscripts; tefillin cases and jars listed"),
           ("9Q", "excavation", 1955, "one papyrus manuscript"),
           ("11Q", "looting_recovered", 1956, "about 21 texts, Temple Scroll among them")]
    for sig, hf, yr, note in qum:
        out.append(row(
            id=f"n_qumran_{sig}", site=f"QUMRAN CAVE {sig[:-1]} ({sig}) MANUSCRIPTS", country="Palestinian Territories",
            judaea_by_name=1, date_from=68, date_to=68, object_type="documents (scrolls)", setting="cave",
            placement="not_stated", context_reported="manuscripts found in the cave", how_found=hf,
            source=wiki, object_class="documents", discovery_year=yr,
            terminus_text="deposit dated by convention to 68 CE, as for Cave 1 (precedent t02H09)",
            sources_pages=wiki, landmark="none_stated",
            flags=f"qumran_cave; {note}; deliberate concealment versus library or dwelling is debated "
                  "(Patrich 1994, 93, via Wikipedia: 'stores and hiding places')"))
    out += [
        row(id="n_qumran_12Q", site="QUMRAN CAVE 12 (2017), BROKEN SCROLL JARS", country="Palestinian Territories",
            judaea_by_name=1, date_from=68, date_to=68, object_type="documents (broken scroll jars and lids; no text)",
            setting="cave", placement="not_stated", context_reported="completely broken storage jars",
            how_found="excavation", source=wiki + "; Sci-News 2017 (cited there)", object_class="documents",
            discovery_year=2017, terminus_text="convention as for Cave 1", sources_pages=wiki,
            landmark="none_stated",
            flags="qumran_cave; jars emptied by earlier looting (source); counted under PLAN 4 (scroll jars)"),
        row(id="n_qumran_10Q", site="QUMRAN CAVE 10 (10Q) OSTRACA", country="Palestinian Territories",
            judaea_by_name=1, date_from=68, date_to=68, object_type="documents (two ostraca)", setting="cave",
            placement="not_stated", how_found="excavation", source=wiki, include=0,
            exclusion_reason="ostraca only; no manuscript deposit or scroll jar reported",
            object_class="documents", discovery_year=1955, sources_pages=wiki, flags="qumran_cave"),
        row(id="n_or_aqiva", site="OR 'AQIVA (NORTH), HELLENISTIC BRONZE HOARD", country="Israel",
            date_from=-222, date_to=-187, object_type="coins (bronze)", setting="unknown", placement="not_stated",
            how_found="excavation",
            source="Bijovsky, 'The Coins from Or 'Aqiva (North)', Atiqot 61 (2009) 75-79, abstract only "
                   "(https://publications.iaa.org.il/atiqot/vol61/iss1/19/); PDF blocked",
            object_class="coins", terminus_text="Ptolemy II to Antiochus III (222-187 BCE)",
            sources_pages="Atiqot 61, pp. 75-79 (abstract)",
            flags="22 coins; date = reign of the latest king named; context not in the abstract"),
        row(id="n_givati_rings", site="JERUSALEM, GIV'ATI PARKING LOT, BUILDING 110 JEWELLERY DEPOSITS",
            country="Israel, Palestinian Territories", judaea_by_name=1, date_from=-225, date_to=-175,
            object_type="metal objects (four gold ornaments, three bronze earrings)", setting="structure",
            placement="under_floor", context_reported="deposited in or below the building's floors",
            how_found="excavation",
            source="Sindel, Bocher et al., 'Gold Rings for Young Girls', Atiqot 121, abstract only "
                   "(https://publications.iaa.org.il/atiqot/vol121/iss1/6/); PDF blocked",
            object_class="metal_objects", discovery_year="", landmark="none_stated",
            terminus_text="late third to early second centuries BCE (authors)",
            sources_pages="Atiqot 121, article 6 (abstract)",
            flags="authors: ritual deposition 'on different occasions' (CLAIM); one cluster; not a shrine"),
        row(id="n_thirdwall_tools", site="JERUSALEM, THIRD WALL AREA B, IRON QUARRYING TOOLS",
            country="Israel, Palestinian Territories", judaea_by_name=1, date_from=-516, date_to=70,
            object_type="metal objects (iron quarrying tools)", setting="unknown", placement="not_stated",
            how_found="excavation",
            source="Weksler-Bdolah, Atiqot 88, Hebrew pp. 1*-8*, English summary pp. 153-154, abstract only "
                   "(https://publications.iaa.org.il/atiqot/vol88/iss1/9/)",
            include=0, exclusion_reason="a stonemason's tool kit; not described as concealed; date only "
                                        "'Second Temple period'",
            object_class="metal_objects", sources_pages="Atiqot 88 (abstract)"),
        row(id="n_ethri", site="HORVAT 'ETHRI HOARD", country="Israel", date_from=132, date_to=136,
            object_type="coins", setting="unknown", placement="not_stated", how_found="unknown",
            source=f"{hendin}, bibliography p. 533: Zissu and Hendin 2012, 'Te'omim Cave and Horvat 'Ethri "
                   "Hoards' (not read)",
            object_class="coins", terminus_text="Bar Kokhba War (title)", sources_pages=f"{hendin}, p. 533",
            flags="known here only from a publication title; contents and context not read"),
    ]
    return out


def main():
    years = json.load(open(sys.argv[1]))
    out_path = sys.argv[2]
    with open(PREC, newline="", encoding="utf-8") as f:
        prec = list(csv.DictReader(f))
    rows = []
    for p in prec:
        r = {k: p[k] for k in PREC_INPUT}
        r.update({k: "" for k in NEW_INPUT})
        r.update(origin="precedent", first_read="before_freeze", unexposed_at_freeze="0", temple_related="0",
                 object_class=object_class(p))
        cid = p["id"]
        if cid.startswith("chre"):
            y = years.get(cid[4:], {})
            r["discovery_year"] = y.get("year", "")
            if y.get("te", "") != "":
                r["terminus_text"] = f"CHRE terminal year {y['te']} to {y['tl']}"
        if cid in DEPTH:
            d, datum, txt, src = DEPTH[cid]
            r.update(depth_m=d, depth_datum=datum, depth_text=txt)
            r["sources_pages"] = src
        if p["include"] == "1" and p["setting"] != "unknown":
            if cid in LANDMARK:
                cls, q, src = LANDMARK[cid]
                r.update(landmark=cls, landmark_text=q)
                r["sources_pages"] = "; ".join(x for x in (r["sources_pages"], src) if x)
            else:
                r["landmark"] = "none_stated"
                r["landmark_text"] = LANDMARK_NOTE.get(cid, "")
        if cid in RECODE:
            rc = RECODE[cid]
            r.update(prec_setting=p["setting"], prec_placement=p["placement"], prec_include=p["include"],
                     prec_date=f"{p['date_from']}..{p['date_to']}", recode_reason=rc["reason"])
            r["placement"] = rc.get("placement", r["placement"])
        if cid in EXTRA_FLAGS:
            r["flags"] = "; ".join(x for x in (r["flags"], EXTRA_FLAGS[cid]) if x)
        rows.append(r)
    rows += new_rows()
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PREC_INPUT + NEW_INPUT, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in PREC_INPUT + NEW_INPUT})
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
