"""Entry 9 (II 7–9): the cistern opposite the East Gate, and its channel.

Worked example for the schematic kit. Sources: text/translation_en.json II 7–9;
text/readings.json e9-*; tables/phase5_assessments.csv; tables/feature_constraints.csv.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("9", "the cistern opposite the East Gate", "II 7–9")
mx, my, mw, mh = L["main"]

# ---------------- main plan: cistern inside the enclosure, facing the gate ----------------
S.panel(c, mx, my, mw, mh, "Main reading: one entry, the cistern inside the enclosure",
        ["The wall runs north–south; the court is to the west, the Kidron slope to the east."])
wall_x, gate_y = mx + 560, my + 330
c.rect(mx + 20, my + 60, wall_x - mx - 24, mh - 80, fill="#f4efe6")          # court
c.rect(wall_x + 4, my + 60, mx + mw - wall_x - 24, mh - 80, fill="url(#rockfill)", fill_opacity=0.7)  # slope
c.text(mx + 40, my + 90, "Temple court (inside)", 12, P["sub"], italic=True)
c.text(wall_x + 20, my + 90, "outside: slope to the Kidron", 12, P["sub"], italic=True)
S.gate(c, wall_x, gate_y, orient="v", length=260, wall_width=10)
S.label(c, wall_x + 16, gate_y - 26, ["East Gate", "(the gap in the wall)"], P["ink"], 12, 700)

px_per_cubit = 10  # 1 cubit ≈ 0.5 m drawn at 20 px per metre
cx = wall_x - 19 * px_per_cubit
S.cistern(c, cx, gate_y, r=36)
S.deposit(c, cx + 10, gate_y + 8, depth="vessels", text_dx=-62, text_dy=30)
S.label(c, cx - 30, gate_y + 62, ["cistern · בור", "“opposite the East Gate”"], P["water_d"], 12, 700)
# feeding channel from the north
S.channel(c, [(cx - 60, my + 120), (cx - 60, gate_y - 60), (cx - 20, gate_y - 30)], covered=False)
S.deposit(c, cx - 60, gate_y - 120, depth="ten talents", text_dx=10, text_dy=4)
S.label(c, cx - 150, my + 128, ["its channel · מזקא", "Allegro, Luria read", "other letters"], P["water_d"], 11.5, 700)
S.dim(c, cx + 36, gate_y + 92, wall_x - 5, gate_y + 92, "19 cubits ≈ 9 m (Lefkovits)", P["red_d"])
c.line(cx + 36, gate_y + 30, cx + 36, gate_y + 98, P["faint"], 0.8, dash="3 3")
c.line(wall_x - 5, gate_y + 20, wall_x - 5, gate_y + 98, P["faint"], 0.8, dash="3 3")
S.north_arrow(c, mx + 50, my + 150)
S.scale_bar(c, mx + 30, my + mh - 60, 100, "0", "5 m", "1 cubit taken as about 0.5 m; cistern drawn to a typical size")

# ---------------- side panels: variants ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

# V2: cistern outside the gate
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: cistern outside the gate",
                         ["“Opposite” could face the gate from the east side."],
                         "Same text, other side", "neutral")
wx, gy = ix + 110, iy + ih / 2 + 4
S.gate(c, wx, gy, orient="v", length=60, wall_width=8)
c.text(ix + 12, iy + 16, "court", 11, P["sub"], italic=True)
c.text(wx + 14, iy + 16, "slope", 11, P["sub"], italic=True)
S.cistern(c, wx + 120, gy, r=20)
S.deposit(c, wx + 126, gy + 4)
S.dim(c, wx + 5, gy + 34, wx + 100, gy + 34, "19 cubits", P["red_d"])

# V3: Puech's 15 cubits
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: 15 cubits (Puech)",
                         ["The editions differ on the number; the files give no preference."],
                         "Distance only", "neutral")
wx, gy = ix + iw - 80, iy + ih / 2 + 6
S.gate(c, wx, gy, orient="v", length=60, wall_width=8)
S.cistern(c, wx - 150, gy - 14, r=14)
S.cistern(c, wx - 190, gy + 22, r=14)
S.dim(c, wx - 136, gy - 40, wx - 5, gy - 40, "15 cubits ≈ 7 m", P["red_d"])
S.dim(c, wx - 176, gy + 50, wx - 5, gy + 50, "19 cubits ≈ 9 m", P["water_d"])

# V4: one hiding place or two
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "One hiding place or two?",
                         ["Milik and others split the channel into its own entry;",
                          "Puech and Lefkovits keep one entry."], "Changes the count, not the plan", "neutral")
S.cistern(c, ix + 70, iy + ih / 2 + 4, r=16)
S.deposit(c, ix + 74, iy + ih / 2 + 8)
S.channel(c, [(ix + 70, iy + 10), (ix + 70, iy + ih / 2 - 14)], flow_arrow=False)
S.deposit(c, ix + 70, iy + 22)
c.text(ix + 110, iy + ih / 2 - 10, "Two deposits either way: vessels in the", 11.5, P["sub"])
c.text(ix + 110, iy + ih / 2 + 6, "cistern, ten talents in its channel. The ΔΙ", 11.5, P["sub"])
c.text(ix + 110, iy + ih / 2 + 22, "letters close the line in all editions.", 11.5, P["sub"])

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (II 7–9)", "“In the cistern that is opposite the East Gate, nineteen cubits away: in it are vessels, "
     "and in its channel(?): ten talents.” ΔΙ."),
    ("What the plan assumes", "The East Gate of the Temple enclosure (all editions; Thiering's Qumran door not adopted). "
     "The distance is measured from the gate to the cistern. The channel feeds the cistern; its course is not given."),
    ("Project placement", "East Gate of the Temple enclosure: best-supported, medium. The gate is placed by texts "
     "(Middot; Neh 3:29); the scroll's cistern has not been identified."),
    ("What the records show", "Warren's plans show no recorded cistern within about 18 m of the Golden Gate; the "
     "nearest (No. 15) is 30 m away. Only open mouths were recorded, under 30–40 ft of debris (feature_constraints.csv)."),
])
print(c.save(S.out_path("9")))
