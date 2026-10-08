"""Entry 14 (III 11–13): the tomb in ha-Melaḥ, on its east side, on its north side.

Sources: text/translation_en.json III 11–13; text/readings.json e14-tomb, e14-slab, e14-sum;
atlas record 14; tables/phase5_assessments.csv and phase5_reports.csv (JER, entries 3–14);
tables/landmark_lexicon_index.csv (qever, madaf, millo); research/text/deeper_analysis_2026-09-30.md §2.1, §3.4;
research/text/sequence_model_followup_2026-09-30.md §2; research/sites/leads_on_old_plans_2026-09-30.md §1, §3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
CUT = 15
c, L = S.page("14", "the Millo tomb", "III 11–13", height=1000,
              subtitle="Schematic plan, north up, with a section at the tomb. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
mh -= CUT
sx, sy, sw, sh = L["side"]
sh -= CUT


def platform(c, x0, y0, x1, y1, wall=12):
    """Walled platform with packed fill (the Esplanade as Milik describes it: retaining walls and fill)."""
    c.rect(x0, y0, x1 - x0, y1 - y0, fill="url(#earth)")
    S.wall(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], width=wall)


def grave_plan(c, x, y, w=34, h=14):
    c.rect(x - w / 2, y - h / 2, w, h, fill=P["grave"], stroke=P["grave_d"], width=1.2, rx=2)


def body(c, x, y, w=90, h=13):
    c.rect(x - w / 2, y - h / 2, w, h, fill="#cdbfa5", stroke=P["grave_d"], width=1, rx=6)
    c.circle(x - w / 2 + 8, y, 7, fill="#cdbfa5", stroke=P["grave_d"], width=1)


# ---------------- main plan ----------------
S.panel(c, mx, my, mw, mh, "Project reading: a tomb in ha-Melaḥ, on its east side, toward its north",
        ["ha-Melaḥ · מלח drawn as a walled platform with fill (Milik 1962; Puech 2006: the Millo, the Esplanade).",
         "Tomb drawn inside the east wall, in the north part; the records say “in or at” the platform."],
        "Project reading (atlas placement)", "counted")
x0, y0, x1, y1 = mx + 60, my + 130, mx + 420, my + 520
platform(c, x0, y0, x1, y1)
c.rect(x0 + 6, y0 + 6, x1 - x0 - 12, 120, fill=P["ochre"], fill_opacity=0.16)
c.rect(x1 - 126, y0 + 6, 120, y1 - y0 - 12, fill=P["blue"], fill_opacity=0.12)
c.text(x0 + 16, y0 + 26, "north side · בצפנו", 12, P["ochre_d"], 700)
c.text(x1 - 20, y1 - 120, "east side · ממזרחו", 12, P["water_d"], 700, anchor="middle", rotate=90)
S.label(c, (x0 + x1) / 2 - 60, y1 - 90, ["ha-Melaḥ · מלח", "retaining walls and fill"], P["ink"], 13, 700,
        anchor="middle")
c.text((x0 + x1) / 2, y1 + 22, "size and shape not given", 11, P["muted"], italic=True, anchor="middle")
tx, ty = x1 - 62, y0 + 66
grave_plan(c, tx, ty)
S.deposit(c, tx, ty, size=5)
S.label(c, tx - 30, ty - 8, ["tomb · קבר"], P["ink"], 12.5, 700, anchor="end")
S.label(c, tx - 30, ty + 10, ["13 talents; Puech reads 14", "dig 3 cubits under the dead(?)"], P["red_d"], 11.5, 600,
        anchor="end")
S.north_arrow(c, mx + 32, my + 170)

# section at the tomb
PXC = 40
bx0, by0, bw0 = mx + 460, my + 100, mw - 480
depth = 3 * PXC
bh0 = 110 + 30 + depth + 40 + 80
c.rect(bx0, by0, bw0, bh0, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(bx0 + 12, by0 + 22, "Section at the tomb", 12.5, P["ink"], 700)
c.text(bx0 + 12, by0 + 38, "depth to scale; 1 cubit ≈ 0.5 m", 11, P["muted"])
c.text(bx0 + 12, by0 + 54, "tomb form not given: drawn as a simple grave", 11, P["muted"])
g = by0 + 110
gx = bx0 + bw0 * 0.42
c.rect(bx0 + 1, g, bw0 - 2, 30 + depth + 40, fill="url(#earth)")
c.line(bx0 + 1, g, bx0 + bw0 - 1, g, P["ink"], 1.4)
c.text(bx0 + 12, g - 8, "surface", 11, P["sub"], italic=True)
c.rect(gx - 60, g, 120, 34, fill="#f3ece0", stroke=P["grave_d"], width=1.3)
body(c, gx, g + 20)
c.text(gx + 70, g + 24, "the dead(?) · המת", 11, P["grave_d"], 600)
c.rect(gx - 12, g + 27, 24, depth - 7, fill="#fbf6ee", stroke=P["red_d"], width=1, dash="4 3")
S.deposit(c, gx, g + 20 + depth - 8, size=6)
S.dim(c, gx + 40, g + 20, gx + 40, g + 20 + depth, "", P["red_d"])
S.label(c, gx + 50, g + 20 + depth / 2 + 8, ["dig 3 cubits", "≈ 1.5 m"], P["red_d"], 11.5, 700)
S.label(c, gx - 40, g + 20 + depth + 26, ["13 talents"], P["red_d"], 11, 600)
S.scale_bar(c, bx0 + 12, by0 + bh0 - 36, 2 * PXC, "0", "1 m")

# ---------------- side panels ----------------
ph = (sh - 20) / 3

# V1: under the slab
bx, by, bw, bh = S.panel(c, sx, sy, sw, ph, "Milik 1962, Puech 2006: under the slab · מדף",
                         ["A slab over a bone pit (Milik, DJD); Puech: “under the slab(?)”.",
                          "The lexicon rates “slab” low."],
                         "Alternative reading", "neutral")
gg = by + 34
x_a = bx + 20
c.rect(x_a, gg, 170, bh - 40, fill="url(#earth)")
c.line(x_a, gg, x_a + 170, gg, P["ink"], 1.2)
c.rect(x_a + 40, gg - 8, 90, 8, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.rect(x_a + 55, gg, 60, 26, fill="#e9dfcf", stroke=P["grave_d"], width=1)
c.text(x_a + 85, gg - 14, "slab", 10.5, P["ink"], 600, anchor="middle")
c.text(x_a + 85, gg + 18, "bones", 9.5, P["grave_d"], anchor="middle")
d1 = min(3 * 20, bh - 60)
S.deposit(c, x_a + 85, gg + d1)
S.dim(c, x_a + 140, gg, x_a + 140, gg + d1, "", P["red_d"])
c.text(x_a + 176, gg + d1 / 2 + 4, "3 cubits", 10.5, P["red_d"], 600)
S.label(c, x_a + 236, by + 18, ["Three cubits run down from", "the slab, not from a body.",
                                "The plan position on the east", "and north sides is unchanged."], P["sub"], 11.5)

# V2: "its north" is the grave's north
bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Lefkovits: “its north” is the grave’s own north",
                         ["The suffix is masculine: it can refer to the pit or grave",
                          "(leads_on_old_plans §1). Lefkovits: “below the corpse”."],
                         "Alternative reading", "neutral")
gx2, gy2 = bx + 95, by + bh / 2 + 6
c.rect(gx2 - 60, gy2 - 22, 120, 44, fill=P["grave"], stroke=P["grave_d"], width=1.4, rx=3)
c.rect(gx2 - 60, gy2 - 52, 120, 30, fill=P["ochre"], fill_opacity=0.2)
S.deposit(c, gx2, gy2 - 36)
c.text(gx2, gy2 + 5, "grave", 11, "#f3ece0", 600, anchor="middle")
S.north_arrow(c, bx + 20, gy2 + 4)
S.label(c, gx2 + 90, by + 18, ["The deposit lies on the grave’s north", "side; “on its east side” could then",
                               "still place the tomb in ha-Melaḥ.", "The files do not settle the suffix."],
        P["sub"], 11.5)

# V3: ha-Melaḥ as a named place
bx, by, bw, bh = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "ha-Melaḥ as a named place",
                         ["Lefkovits 2000 (conditional): the City of Salt. Research notes:",
                          "a tomb east of a Jericho-district site, in its north part."],
                         "Not adopted in the atlas", "warn")
qx, qy, R = bx + 68, by + bh / 2 + 4, min(bh / 2 - 2, 56)
S.quarters(c, qx, qy, R, highlight={"E": "blue", "N": "ochre"})
S.site(c, qx, qy, r=11)
tx3, ty3 = S.pt(qx, qy, 62, R * 0.68)
grave_plan(c, tx3, ty3, w=16, h=7)
S.deposit(c, tx3 + 10, ty3 - 8, size=4)
S.label(c, qx + R + 26, by + 18, ["At Kh. Qumran the main cemetery is", "east of the site (leads_on_old_plans",
                                  "§3); untested for this tomb. The",
                                  "follow-up (§2) calls a tomb at the", "Temple platform implausible: purity."],
        P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"] - CUT, [
    ("Text (III 11–13)", "“In the tomb that is in ha-Melaḥ, on its east side, on its north side, cubits under the "
     "dead(?): dig three: 13 talents.”"),
    ("What the plan assumes", "ha-Melaḥ read as the Esplanade (Milik; Puech 2006). “East side” and “north side” are "
     "taken as parts of ha-Melaḥ, so the tomb sits in its north-east part; the text gives no size or distance. "
     "Three cubits are measured down from the dead, as the project text reads המת."),
    ("Project placement", "Atlas: possible only, low. Candidate: Temple enclosure (Temple Mount), possible, low. "
     "Milik’s site list names Alexander Jannaeus’s tomb. The follow-up asks for a Jericho-area alternative; "
     "the atlas has none yet."),
    ("What the records show", "phase5_assessments.csv (JER, entries 3–14): a tomb by the esplanade is known only from "
     "texts (Josephus, Middot, 11QTemple, as cited by Milik, Puech and Høgenhaven), so it cannot be checked on the "
     "ground; the entry stays possible, low."),
])
print(c.save(S.out_path("14")))
