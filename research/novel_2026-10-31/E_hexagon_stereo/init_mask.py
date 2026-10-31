"""Provisional SULTAN-1 / Jericho-oasis mask in 1208-400636A015, set BEFORE any image read.

Store note: tell centre at full-res (33458, 21496), tile c, stored orientation.
Largest distance from the tell centre to the buffered exclusion boundary
(zones.py: 3 km circle + oasis envelope + 1 km buffer) is about 8.0 km.
At the smallest plausible scale (0.70 m/px; 1978 frame 0.82 m/px at Qumran)
that is 11,500 px, in any direction (rotation unknown).
Tile order across the film is not yet known, so the near part of tiles b and d
(x < 15000) is also blocked until A015 is located.
"""
import common as C

R = 11500
TX, TY = 33458, 21496
C.save_prot([])
C.add_prot("D3C1208-400636A015", "c", [TX - R, TY - R, TX + R, TY + R],
           "SULTAN-1/Jericho exclusion (provisional, before reading): tell centre +/- 11500 px")
for t in ("b", "d"):
    C.add_prot("D3C1208-400636A015", t, [0, TY - R, 15000, 24668 + 500],
               "SULTAN-1/Jericho exclusion (provisional): adjacent tile, tile order unknown")
print(open(C.PROT).read())
