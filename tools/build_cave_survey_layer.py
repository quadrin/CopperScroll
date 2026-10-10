"""Build the atlas overlay of the 1952 Qumran cave survey points.

Usage: python3 tools/build_cave_survey_layer.py

Reads research/history/devaux1952_cave_points/devaux1952_cave_points.csv (the 27
legible numbered points of R. de Vaux, RB 60 (1953) pl. XX, digitized in this
repository; about +/-30 m 1-sigma, +/-60 m at 95%) and writes
atlas/app/atlas-landscape-cave-survey.json for the Landscapes "Map layers"
panel. Standard library only; the output is deterministic.

These are survey points, not candidate places: nothing here touches
atlas-data.json, the entry register or any place count. Coordinates come
unchanged from the CSV.

The one-line site notes paraphrase DJD III, Textes (1962), pp. 6-12, as
extracted in research/history/djd3_text_cave_list_extracted.md. Both sources
use de Vaux's single 1-40 site series (both give 8 = 3Q, 14 = 1Q, 19 = 2Q).
The atlas qualifies a note when the printed number on the plate is only a
probable reading.
"""
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/history/devaux1952_cave_points/devaux1952_cave_points.csv"
OUTPUT = ROOT / "atlas/app/atlas-landscape-cave-survey.json"

# Equivalences stated in DJD III p. 6 (8, 14 and 19 also in RB 60 pp. 542, 553, 555).
CAVES = {
    8: ("3Q", "Cave 3 (3Q), where the Copper Scroll was found"),
    14: ("1Q", "Cave 1 (1Q)"),
    19: ("2Q", "Cave 2 (2Q)"),
    26: ("6Q", "Cave 6 (6Q)"),
}

# DJD III, Textes (1962) pp. 6-12 (pp. 7-8 and 201 for site 8): short paraphrase.
DJD3 = {
    1: "Large cave with an inner chamber; a few Qumran-type sherds above an ash layer 0.75 m thick reaching bedrock.",
    2: "Not a cave: a pottery deposit under fallen rocks, with sherds of at least three Qumran-type jars.",
    3: "Small cave c. 3 m deep with a collapsed ceiling; jars, lids and other pottery at or just below the surface.",
    4: "Large cave opening south; an incomplete wooden basin and sherds, mostly probably Arab, a few possibly Qumran-type.",
    7: "Very small cave (2 × 1.5 m) opening east; a lid and fragments of a Qumran-type jar.",
    8: "Originally c. 10 m wide; the ceiling collapsed except over a rear chamber c. 3 × 2 m. Broken jars and lids lay in front; the two copper rolls lay against the rock wall at the chamber’s north corner (found 20 March 1952).",
    9: "Rock crevice closed by a dry-stone wall; a lamp and a small juglet.",
    10: "Large cave with a wide entrance; fragments of two Qumran-type jars.",
    12: "Not a cave: a very low rock shelter; jars, lids and a bowl lay behind two stones propping the ceiling, with a palm-fibre mat.",
    14: "A few sherds were collected but not kept; the outline of the original entrance was sought.",
    15: "Rock hollow open to the north; a Qumran-type jar with a bowl that served as its lid.",
    17: "High crevice through a spur of the cliff; Qumran-type pottery and five wooden posts sealed under fallen stones.",
    18: "Large cave opening north; fragments of four Qumran-type jars.",
    19: "Irregular two-storey cave opening north-east, emptied by a clandestine dig; pottery recovered from the spoil.",
    21: "Rock fissure with sherds of Qumran-type jars washed in by runoff.",
    22: "Very small cave, 1 m wide and 2 m deep, full of fine earth; the base of a Qumran-type jar.",
    26: "Small cave at the mouth of the Wadi Qumran gorge, below the aqueduct; found and emptied by Bedouin in September 1952.",
    27: "Very large cave on the south side of the Wadi Qumran, with a porch 4 × 6 m; very few sherds (Iron II, Arab, perhaps Qumran); the Bedouin had already sounded it.",
    28: "A shaft above site 29 leading to a small lower chamber; Qumran-type jars and lids.",
    29: "Round chamber reached by a 2 m tunnel; Qumran-type jars and lids, seven intact lids stacked against the wall apart from the jars.",
    30: "Rock hollow 1 m wide; fragments of a Qumran-type jar.",
    31: "Large cave with a rectangular opening; three bowls and two Qumran-type jars.",
    32: "Cave with a wide, low east-facing entrance at the foot of the cliff; Qumran-type jars and a lid, and some Arab sherds.",
    35: "Not a cave: ruins of a rectangular building cut by the Qumran–ʿAin Feshkha track, shown to be Israelite by the 1956 excavation.",
    37: "The largest cave in the list, high in the cliff; Qumran-type sherds (and Chalcolithic, 1953) from two small caves at its entrance.",
    39: "Cave opening north-east, 8 m deep, partly collapsed; Qumran-type jars and lids and an Iron II lamp, some bought from Bedouin who had dug there.",
    40: "Cave smaller than site 39 but similar; one Qumran-type jar.",
}

DOT = re.compile(r"^Dot position (sure|probable|uncertain) ")


def build():
    with SOURCE.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    features = []
    for row in rows:
        point = int(row["point"])
        if row["label_reading"] != row["point"]:
            raise ValueError(f"Point {point}: label reading {row['label_reading']!r} differs from the point number")
        if row["confidence"] not in {"sure", "probable"}:
            raise ValueError(f"Point {point}: unexpected label confidence {row['confidence']!r}")
        dot = DOT.match(row["notes"])
        if not dot:
            raise ValueError(f"Point {point}: notes do not state the dot confidence")
        lat, lon = float(row["lat"]), float(row["lon"])
        if not (31.70 < lat < 31.77 and 35.44 < lon < 35.46):
            raise ValueError(f"Point {point}: {lat}, {lon} lies outside the plate area")
        siglum, cave = CAVES.get(point, (None, None))
        features.append({
            "type": "Feature",
            "id": f"devaux1952-{point}",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "point": point,
                "label": f"{point} = {siglum}" if siglum else str(point),
                "label_confidence": row["confidence"],
                "dot_confidence": dot.group(1),
                "cave": cave,
                "pal_e_km": row["pal_e_km"],
                "pal_n_km": row["pal_n_km"],
                "dist_to_8_m": int(row["dist_to_8_m"]),
                "djd3": DJD3.get(point),
            },
        })
    points = [feature["properties"]["point"] for feature in features]
    if len(points) != 27 or len(set(points)) != 27 or 8 not in points:
        raise ValueError(f"Expected the 27 legible points of pl. XX including 8; found {points}")
    if set(DJD3) - set(points) or set(CAVES) - set(points):
        raise ValueError("A site note names a point that is not in the CSV")
    features.sort(key=lambda feature: feature["properties"]["point"])
    collection = {"type": "FeatureCollection", "features": features}
    OUTPUT.write_text(json.dumps(collection, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Wrote {len(features)} survey points to {OUTPUT.relative_to(ROOT)}.")


if __name__ == "__main__":
    build()
