"""Build atlas landscape assets from the owner's documented source intake.

Usage: python tools/build_landscape_data.py --intake-dir /path/to/intake
Requires Pillow and pyproj. Does not register photographs or identify features.
"""
import argparse
import csv
import hashlib
import json
import pathlib
import shutil
import sqlite3
import struct
import tempfile
import zipfile

from PIL import Image
from pyproj import Transformer

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "research/assets/plans/historical-landscapes"
MIRROR = ROOT / "atlas/research/assets/plans/historical-landscapes"
PUBLIC = ROOT / "atlas/public/landscapes"
SOURCES = [
    ("jericho-1942-full", "12SiWV0aliWn3eXJAIw4OR8Ciw3d3jhxe", "Survey of Palestine, Jericho 19-14, April 1942 overprint", "Survey of Palestine; Palestine Open Maps; National Library of Israel", "Public domain", "https://palopenmaps.org/en/about"),
    ("jericho-corona", "1WVgnQuUPUl5N9emRsqTzc6sZWVMuO7Bj", "CORONA DS1101-2168DF041, Jericho, 26 September 1967; project annotations", "USGS EROS; project annotations from the owner's library", "Underlying imagery public domain; project annotations", "https://www.usgs.gov/centers/eros/science/usgs-eros-archive-declassified-data-declassified-satellite-imagery-1"),
    ("buqeia-corona", "1pX6pgt1bsMFqVdMCWcXSO3qpEPX7MvYT", "CORONA DS1101-2168DF042, Buqeia / Hyrcania, 26 September 1967; project annotations", "USGS EROS; project annotations from the owner's library", "Underlying imagery public domain; project annotations", "https://www.usgs.gov/centers/eros/science/usgs-eros-archive-declassified-data-declassified-satellite-imagery-1"),
    ("qumran-corona", "1nMV0T3XCa_iwwml_MRan3WcXXi5PDXfH", "CORONA DS1101-2168DF042, Qumran, 26 September 1967; project annotations", "USGS EROS; project annotations from the owner's library", "Underlying imagery public domain; project annotations", "https://www.usgs.gov/centers/eros/science/usgs-eros-archive-declassified-data-declassified-satellite-imagery-1"),
    ("mar-saba-1918", "1Nmqd4LW9hLWevLqDJu9vHR5JKoxUBKbt", "BayHStA, BS Pal. 0923, Mar Saba, 3 January 1918", "Bayerisches Hauptstaatsarchiv, Abt. IV Kriegsarchiv, BS Pal. 0923", "CC0 / public-domain archival digital image", "https://www.gda.bayern.de/en/footer/nutzungsbedingungen/index.html"),
    ("jericho-road-1918", "1ZICJ6EAopnxhyh9zaGdGF_dheWtH8i9G", "BayHStA, BS Pal. 1002, Jericho–Besan road, 27 May 1918", "Bayerisches Hauptstaatsarchiv, Abt. IV Kriegsarchiv, BS Pal. 1002", "CC0 / public-domain archival digital image", "https://www.gda.bayern.de/en/footer/nutzungsbedingungen/index.html"),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wkb_lines(blob):
    # GeoPackage header: envelope code occupies flag bits 1–3.
    envelope_size = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(blob[3] >> 1) & 7]
    offset = 8 + envelope_size

    def read_geometry(pos):
        endian = "<" if blob[pos] else ">"
        kind = struct.unpack_from(endian + "I", blob, pos + 1)[0]
        pos += 5
        dimension = 2 + (1 if 1000 <= kind < 3000 else 2 if kind >= 3000 else 0)
        kind %= 1000
        count = struct.unpack_from(endian + "I", blob, pos)[0]
        pos += 4
        if kind == 2:
            points = []
            for _ in range(count):
                values = struct.unpack_from(endian + "d" * dimension, blob, pos)
                points.append(values[:2])
                pos += 8 * dimension
            return [points], pos
        if kind == 5:
            lines = []
            for _ in range(count):
                child, pos = read_geometry(pos)
                lines.extend(child)
            return lines, pos
        raise ValueError(f"Unsupported road geometry {kind}")

    return read_geometry(offset)[0]


def build(intake):
    for directory in (ARCHIVE, MIRROR, PUBLIC):
        directory.mkdir(parents=True, exist_ok=True)
    manifest = {"inspected": "2026-10-10", "scope": "Landscape display; no new feature identification or photographic registration", "assets": []}
    for stem, drive_id, title, credit, licence, rights_url in SOURCES:
        original = intake / (stem + ".jpg")
        target = ARCHIVE / original.name
        shutil.copy2(original, target)
        image = Image.open(original)
        size = list(image.size)
        image.thumbnail((2200, 2200), Image.Resampling.LANCZOS)
        derivative = PUBLIC / (stem + ".webp")
        image.save(derivative, "WEBP", quality=88, method=6)
        manifest["assets"].append({"title": title, "source_url": f"https://drive.google.com/file/d/{drive_id}/view", "credit": credit, "reuse": licence, "rights_url": rights_url, "original": target.name, "original_sha256": sha(target), "original_dimensions": size, "asset": f"atlas/public/landscapes/{derivative.name}", "asset_sha256": sha(derivative), "asset_dimensions": list(image.size), "extraction": "Entire image retained; Lanczos downsample to at most 2200 pixels, WebP quality 88. No crop or added annotation.", "registration": "Unregistered source image; source annotations are approximate."})
    # Reproduce already exposed map records; reserved/rejected Sultan geometry
    # stays out of the overlay. No position or assessment in the CSV is changed.
    with (ROOT / "research/regional/mandate_maps/features.csv").open() as file:
        features = []
        for row in csv.DictReader(file):
            if row["protected_zone"] != "no" or "sultan" in row["window"].lower():
                continue
            features.append({"type": "Feature", "id": row["item_id"], "geometry": {"type": "Point", "coordinates": [float(row["lon"]), float(row["lat"])]}, "properties": {key: row[key] for key in ["item_id", "place_id", "sheet", "feature_class", "label_as_printed", "anchor_kind", "position_error_m", "state_2025", "state_basis", "period_as_source", "notes"]}})
    collection = {"type": "FeatureCollection", "features": features}
    (ROOT / "atlas/app/atlas-landscape-features.json").write_text(json.dumps(collection, ensure_ascii=False, separators=(",", ":")) + "\n")
    road_zip = intake / "itinere_roads_gpkg.zip"
    shutil.copy2(road_zip, ARCHIVE / road_zip.name)
    to_mercator = Transformer.from_crs(4326, 3395, always_xy=True)
    to_wgs84 = Transformer.from_crs(3395, 4326, always_xy=True)
    xmin, ymin = to_mercator.transform(34.7, 31.25)
    xmax, ymax = to_mercator.transform(36.0, 32.8)
    roads = []
    with tempfile.TemporaryDirectory() as temporary:
        with zipfile.ZipFile(road_zip) as archive:
            archive.extract("itinere_roads.gpkg", temporary)
        db = sqlite3.connect(pathlib.Path(temporary) / "itinere_roads.gpkg")
        db.row_factory = sqlite3.Row
        table, geom, _, srs_id, _, _ = db.execute("select * from gpkg_geometry_columns").fetchone()
        if srs_id != 3395:
            raise ValueError("Road source CRS changed; review before rebuilding")
        query = f'SELECT a.* FROM "{table}" a JOIN "rtree_{table}_{geom}" b ON a.fid=b.id WHERE b.minx <= ? AND b.maxx >= ? AND b.miny <= ? AND b.maxy >= ?'
        for row in db.execute(query, (xmax, xmin, ymax, ymin)):
            coordinates = [[[round(x, 6), round(y, 6)] for x, y in (to_wgs84.transform(*point) for point in line)] for line in wkb_lines(row[geom])]
            properties = {key: row[key] for key in ["fid", "Name", "Type", "Lower_Date", "Low_Date_E", "Upper_Date", "Up_Date_E", "Bibliograp", "Cons_per_e", "Itinerary", "Segment_s"]}
            for key in ["Lower_Date", "Low_Date_E", "Upper_Date", "Up_Date_E"]:
                if properties[key] == 9999:
                    properties[key] = None
            roads.append({"type": "Feature", "geometry": {"type": "MultiLineString", "coordinates": coordinates}, "properties": properties})
        db.close()
    road_collection = {"type": "FeatureCollection", "features": roads}
    (ROOT / "atlas/app/atlas-landscape-roads.json").write_text(json.dumps(road_collection, ensure_ascii=False, separators=(",", ":")) + "\n")
    manifest["road_extract"] = {"source_url": "https://doi.org/10.5281/zenodo.17122148", "owner_library_url": "https://drive.google.com/file/d/1uUp38ngQvmTq-9z_Q5S2qOG3VCJ1sU7F/view", "source_sha256": sha(road_zip), "reuse": "CC BY 4.0; de Soto et al., Itiner-e (2025)", "source_crs": "EPSG:3395", "output_crs": "EPSG:4326", "selection_bbox": [34.7, 31.25, 36.0, 32.8], "method": "Select intersecting road bounding boxes, retain complete source segments and certainty/evidence metadata, transform vertices with pyproj, round to 6 decimal places; 9999 date sentinel converted to null.", "field_description_source": "https://drive.google.com/file/d/17bLUPLoanwhqj_J6t49f5v7pBNpASC43/view", "field_description_inspected": "2026-10-10; complete readable text and field table of the library's Data field description.docx", "field_semantics": {"Lower_Date": "Source start year; positive CE, negative BCE. Zero means uncertain.", "Low_Date_E": "Possible time span in years before Lower_Date when the road might already have existed. Zero means uncertain, not zero error.", "Upper_Date": "Source end year; positive CE, negative BCE. Zero means uncertain.", "Up_Date_E": "Possible time span in years after Upper_Date when the road might still have been used. Zero means uncertain, not zero error.", "Cons_per_e": "Construction-period field: ruler or magistrate associated with formalizing the road, with dates when supplied. This is not the paper's regional-incorporation table and does not independently establish first construction.", "Segment_s": "Certainty of the digitized road alignment, not chronological certainty."}, "limitations": "Roman-period context, not a reconstruction of roads in the scroll's period. Formalization attribution does not establish first construction or use in the scroll's period. No route or identification claim. The field-description document is linked; no reproduction licence for that document is asserted."}
    (ARCHIVE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    (ARCHIVE / "README.md").write_text("# Historical landscape source assets\n\nSix complete source images, their public display derivatives, and the Itiner-e intake are documented in manifest.json. Original captions, image margins, north arrows and scales are retained. The paired atlas/research archive is byte-identical.\n\nThe Jericho 19-14 full sheet identifies an April 1942 overprint; its margin defines R. as ruin, the cave symbol, Cem. as cemetery, C as cistern, and WT as water or watch tower. This source inspection supplies the legend previously unavailable to the tile review; it does not revise any registered positional result.\n\nCORONA project annotations are source annotations: Qumran is marked approximately ±150 m, Hyrcania ±500 m, and Jericho approximately. They are displayed as unregistered photographs. The 1918 aerials are also unregistered. No photographic coordinates are emitted.\n\nLive raster maps use the Palestine Open Maps published tile registration. The Tell es-Sultan feature registration was rejected in the existing review and contributes no relation geometry. Reserved Sultan map records are omitted from the feature overlay.\n\nThe roads are a regional context layer preserving Itiner-e certainty and source metadata. Unknown dates stay unknown; no segment is labeled as a Copper Scroll route.\n")
    with (ARCHIVE / "README.md").open("a") as file:
        file.write("\n## Verified road-field definitions\n\nThe library's [Data field description.docx](https://drive.google.com/file/d/17bLUPLoanwhqj_J6t49f5v7pBNpASC43/view), read in full on 10 October 2026, defines Lower_Date and Upper_Date as start/end years, with negative values for BCE. Low_Date_E is a possible span before the start year; Up_Date_E is a possible span after the end year. Zero denotes uncertainty in all four fields, including the span fields; it is not a zero-error estimate. The [dataset paper](https://www.nature.com/articles/s41597-025-06140-z) confirms CE/BCE units and 9999 as the missing-date sentinel. The extract retains 9999-to-null conversion.\n\nCons_per_e is the construction-period field naming a ruler or magistrate associated with formalizing the road. It is distinct from the paper's table of regional incorporation into Roman dominion. This attribution does not establish the road's first construction or use in the Copper Scroll's period. Segment_s describes alignment certainty, independently of chronology. The document is linked for retrieval; its reproduction licence remains unverified and no copy is published.\n")
    for file in ARCHIVE.iterdir():
        shutil.copy2(file, MIRROR / file.name)
    print(f"Prepared {len(SOURCES)} source images, {len(features)} exposed map records and {len(roads)} source road segments.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake-dir", type=pathlib.Path, required=True)
    build(parser.parse_args().intake_dir)
