#!/usr/bin/env python3
"""Convert Old Israel/Palestine Grid (EPSG:28191, Cassini-Soldner, Palestine 1923 datum)
references to WGS84 lat/lon. Inputs are metres (E, N). Accuracy: datum transform
in PROJ for Palestine 1923 is approximate (tens of metres to ~100+ m)."""
from pyproj import Transformer
t = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)
pts = [
 ("Zissu 2001 p.150: Ein Samiya valley 'map ref. 181/155'", 181000, 155000),
 ("Zissu 2001 p.149: Kh. Yanun 18425/17385", 184250, 173850),
 ("Zissu 2001 p.149: Yanun village 18370/17245", 183700, 172450),
 ("Notley-Safrai 2005 p.104 n.550: Yanun 18440/17230", 184400, 172300),
]
import csv, sys
w = csv.writer(sys.stdout)
w.writerow(["label","E_m","N_m","lon","lat"])
for lab,e,n in pts:
    lon, lat = t.transform(e, n)
    w.writerow([lab, e, n, round(lon,5), round(lat,5)])
