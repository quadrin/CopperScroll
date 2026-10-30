"""Run 24: write out/methods.csv and out/controls.csv.

P ranges are rounded from physics_model_output.txt and muon_output.txt
(detect_model.py, muon_estimate.py) and adjusted by the stated judgement.
Basis codes: PUB = published case in comparable setting; PHYS = physics
estimate with stated inputs (scripts); INF = inference.
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), "..")
HDR = ["site", "zone", "method", "target", "p_low", "p_high", "basis",
       "main_failure", "false_positives", "null_informative"]

GPR_FP_MARL = "wall footings, plaster floors and channel beds, stones in fill, crack edges, modern pipes"
EM_FP = "nails/coins/tools from 1950s and 1990s digs, walkway and railing metal, conservation fixtures, zinc or lead burial items"
EM_FP_Z3 = "graves and grave goods (2000 walk-over: strong metal signal over a grave was a zinc coffin), modern litter, survey pins"

rows = []


def add(site, zone, method, target, lo, hi, basis, fail, fp, null):
    rows.append([site, zone, method, target, f"{lo:.2f}", f"{hi:.2f}", basis, fail, fp, null])


def qumran_marl_block(site, zone, ta_labels, depth_note, coverage_note, muon_ok, extra_fp=""):
    ta_lo, ta_hi = ta_labels
    # GPR
    add(site, zone, "GPR 100/250/500 MHz", ta_lo[0], *ta_lo[1]["gpr"],
        "PHYS: marl <=~50 ohm-m (Bauman ERT, Freund 2012 Fig. 3.2); 60-80 dB budget; reach p10-p90 0.8-1.9 m at 250-500 MHz; 100 MHz reaches ~2-3 m at ~0.5 m resolution. T19/EAC p.15 warn of salty soils",
        f"signal attenuated before {depth_note}; small vessels below resolution", GPR_FP_MARL + extra_fp,
        "no (top ~1-1.5 m only)")
    add(site, zone, "GPR 100/250/500 MHz", ta_hi[0], *ta_hi[1]["gpr"],
        "PHYS as above; metal gives strong reflection where reached", f"reach shorter than {depth_note}",
        GPR_FP_MARL + extra_fp, "no (top ~1-1.5 m only)")
    add(site, zone, "GPR 100/250/500 MHz", "T-b", *ta_hi[1]["gpr_tb"],
        "PHYS as above; air void or jar gives a hyperbola if within reach", "reach; void likely collapsed or filled in marl",
        GPR_FP_MARL + extra_fp, "no")
    # ERT
    add(site, zone, "ERT (2D/3D, 0.25-0.5 m spacing)", ta_lo[0], *ta_lo[1]["ert"],
        "PHYS/INF: a body is resolved to ~3x its radius (Martinez-Lopez et al. 2013 via T19); metal in 20-50 ohm-m marl gives little contrast",
        "size and contrast too small", "stones, dry pockets, walls" + extra_fp, "no")
    add(site, zone, "ERT (2D/3D, 0.25-0.5 m spacing)", ta_hi[0], *ta_hi[1]["ert"],
        "PHYS/INF as above", "resolution limit ~1-1.5 m for a 0.6 m body", "stones, dry pockets, walls" + extra_fp, "no")
    add(site, zone, "ERT (2D/3D, 0.25-0.5 m spacing)", "T-b", *ta_hi[1]["ert_tb"],
        "PUB+PHYS: Bauman ERT imaged a cave-sized (several m) resistive body in Qumran marl at 2-9 m (Freund 2012 Fig. 3.2); a 0.6 m void only to ~1-1.5 m",
        "target too small for its depth; electrodes blocked by walls", "air in crack, rubble, dry fill, walls" + extra_fp,
        "no")
    # EMI
    add(site, zone, "EMI (EM38-type, conductivity + in-phase)", ta_lo[0], *ta_lo[1]["emi"],
        "PUB+PHYS: EM38 reach ~1.5 m (Bauman, Cave of Letters, via S34 notes); dipole scaling", "depth", EM_FP, "no")
    add(site, zone, "EMI (EM38-type, conductivity + in-phase)", ta_hi[0], *ta_hi[1]["emi"],
        "PUB+PHYS as above", "depth (reach ~0.9-1.6 m)", EM_FP, "no")
    add(site, zone, "EMI (EM38-type, conductivity + in-phase)", "T-b", *ta_hi[1]["emi_tb"],
        "INF: a void lowers conductivity slightly", "contrast tiny against marl variation", "fill and moisture variation", "no")
    # Metal detection
    add(site, zone, "Metal detection (PI large loop; TDEM EM61-type)", ta_lo[0], *ta_lo[1]["pi"],
        "PUB+PHYS: EM61 detects a 55-gal drum at 3.5 m and a 'substantially sized hoard' within ~3-3.5 m (Bauman, Cave of Letters, via S34 notes); response ~ size^3/z^6 (detect_model.py)",
        f"depth: 5 kg group reaches ~1.0-1.8 m, zone runs to {depth_note}; {coverage_note}", EM_FP + extra_fp,
        "no (top ~1.5 m only)")
    add(site, zone, "Metal detection (PI large loop; TDEM EM61-type)", ta_hi[0], *ta_hi[1]["pi"],
        "PUB+PHYS as above", f"lower part of zone beyond reach; {coverage_note}", EM_FP + extra_fp,
        "weak (only for the upper part of the zone)")
    add(site, zone, "Metal detection (PI large loop; TDEM EM61-type)", "T-b", 0.0, 0.05,
        "INF: a jar or chest without metal gives no EM response; metal contents fall under T-a", "no conductor",
        EM_FP, "no")
    # Magnetometry
    for t, lo, hi, why in ((ta_lo[0], 0.0, 0.02, "silver and bronze are non-ferrous"),
                           (ta_hi[0], 0.0, 0.05, "silver and bronze are non-ferrous; only iron fittings would show"),
                           ("T-b", 0.0, 0.10, "fired jar gives 0.3-3 nT at 1 m, ~0.1-0.4 nT at 2 m (detect_model.py)")):
        add(site, zone, "Magnetometry (fluxgate/caesium gradiometer)", t, lo, hi,
            "PUB+PHYS: Geometrics (via T19 draft): non-ferrous metals give no anomaly; dipole estimate",
            why, "kiln L66 and fired features, iron litter, railings" if zone == "Z1" else "iron litter, fired features",
            "no")
    # Muon
    if muon_ok:
        add(site, zone, "Muon imaging (method 5)", ta_lo[0], 0.0, 0.01,
            "PHYS: contrast 0.1-0.2%, years of exposure (muon_estimate.py); method-5 summary: finds chambers >=1 m, not objects",
            "far below resolution", "walls, plaster, density changes", "no")
        add(site, zone, "Muon imaging (method 5)", ta_hi[0], 0.0, 0.10,
            "PHYS: contrast 2-3%, 10-135 days per pixel; method-5 summary as above", "systematics from walls/crack fill exceed signal",
            "walls, plaster, crack fill", "no")
        add(site, zone, "Muon imaging (method 5)", "T-b", 0.0, 0.20,
            "PHYS: open void contrast 8-14%, days per pixel; below the 1 m chamber limit; detector space available on the pool floor",
            "0.6 m below stated resolution; a filled jar or collapsed void has no contrast", "walls (20-40% contrast), crack voids", "no")
    else:
        for t in (ta_lo[0], ta_hi[0], "T-b"):
            add(site, zone, "Muon imaging (method 5)", t, 0.0, 0.0,
                "method-5 summary: needs a space below the target", "no space below the zone", "n/a", "no")
    # Microgravity
    add(site, zone, "Microgravity", ta_lo[0], 0.0, 0.0, "PHYS: 5 kg silver gives <0.05 uGal", "signal far below noise", "terrain, walls", "no")
    add(site, zone, "Microgravity", ta_hi[0], 0.0, 0.01, "PHYS: 50 kg silver (net +40 kg) gives 0.03-0.5 uGal at 0.7-3 m; noise 3-5 uGal (INF)",
        "signal far below noise", "terrain, walls", "no")
    add(site, zone, "Microgravity", "T-b", 0.0, 0.10,
        "PHYS: 0.29 m3 void gives 3.6 uGal at 1 m, 0.9 uGal at 2 m; noise 3-5 uGal",
        "only a shallow open void shows; wall and terrain corrections among standing walls", "walls, pits, crack voids, terrain", "no")
    # T-c
    for m in ("GPR 100/250/500 MHz", "ERT (2D/3D, 0.25-0.5 m spacing)", "EMI (EM38-type, conductivity + in-phase)",
              "Metal detection (PI large loop; TDEM EM61-type)", "Magnetometry (fluxgate/caesium gradiometer)",
              "Muon imaging (method 5)", "Microgravity"):
        add(site, zone, m, "T-c", 0.0, 0.02, "INF: scroll-sized object (copper ~1-3 kg, or leather/papyrus) alone",
            "too small; copper sheet only to ~0.5-1 m with EM", "any small clutter", "no")


# ---------------- L56/58: Z1 (marl, 0-3 m, standing walls)
Z1 = {
    "gpr": (0.10, 0.25), "ert": (0.0, 0.05), "emi": (0.10, 0.20), "pi": (0.20, 0.35)}
Z1H = {
    "gpr": (0.20, 0.30), "gpr_tb": (0.15, 0.25), "ert": (0.05, 0.15), "ert_tb": (0.10, 0.25),
    "emi": (0.15, 0.30), "emi_tb": (0.0, 0.05), "pi": (0.35, 0.60)}
qumran_marl_block("L56/58", "Z1", (("T-a 5 kg", Z1), ("T-a 50 kg", Z1H)), "3 m",
                  "standing walls W607/W626, channel M25 and kiln L66 limit coverage to ~60-90%", True)

# ---------------- Z3 (marl strip toward heap, 3 cubits = 1.3-1.6 m + 0-0.5 m)
Z3L = {"gpr": (0.05, 0.15), "ert": (0.0, 0.05), "emi": (0.15, 0.30), "pi": (0.55, 0.75)}
Z3H = {"gpr": (0.10, 0.20), "gpr_tb": (0.05, 0.15), "ert": (0.0, 0.10), "ert_tb": (0.0, 0.05),
       "emi": (0.20, 0.35), "emi_tb": (0.0, 0.05), "pi": (0.60, 0.80)}
qumran_marl_block("L56/58", "Z3", (("T-a 10 kg/talent (230 kg)", Z3L), ("T-a 21.3 kg/talent (490 kg)", Z3H)),
                  "1.3-2.1 m", "open ground but strip position uncertain (run 17 C1 unknown)", False,
                  extra_fp="; graves (>100 GPR grave signatures, Jol et al. 2002 abstract)")

# ---------------- Z2 (aqueduct head; gravel/colluvium/limestone; under a boulder)
def z2():
    z = "Z2"; s = "L56/58"
    fp = "flood boulders, bedrock steps, aqueduct masonry, tunnel voids"
    add(s, z, "GPR 100/250/500 MHz", "T-a 10 kg/talent (70 kg)", 0.30, 0.55,
        "PHYS: dry gravel/limestone 50-300 ohm-m (INF), reach 3-12 m; EPA via T19: good in dry low-loss ground; Cave of Letters GPR ~3 m at 450 MHz, >10 m at 100 MHz (Jol, via S34 notes)",
        "the 'great stone' sits on top; which stone is unknown; coarse boulders scatter", fp, "partly (if the stone is identified)")
    add(s, z, "GPR 100/250/500 MHz", "T-a 21.3 kg/talent (149 kg)", 0.35, 0.60, "PHYS as above", "as above", fp, "partly")
    add(s, z, "GPR 100/250/500 MHz", "T-b", 0.30, 0.55, "PHYS as above", "as above", fp, "partly")
    add(s, z, "ERT (2D/3D, 0.25-0.5 m spacing)", "T-a 10 kg/talent (70 kg)", 0.05, 0.15, "PHYS/INF: resolution ~3x radius; poor contact on gravel", "depth 1.3-3.6 m vs resolution", fp, "no")
    add(s, z, "ERT (2D/3D, 0.25-0.5 m spacing)", "T-a 21.3 kg/talent (149 kg)", 0.05, 0.15, "PHYS/INF as above", "as above", fp, "no")
    add(s, z, "ERT (2D/3D, 0.25-0.5 m spacing)", "T-b", 0.05, 0.20, "PHYS/INF: air void in resistive gravel has low contrast", "low contrast; depth", fp, "no")
    add(s, z, "EMI (EM38-type, conductivity + in-phase)", "T-a 10 kg/talent (70 kg)", 0.0, 0.10, "PHYS: reach ~1.1-1.6 m from coil", "depth plus boulder stand-off", "iron litter", "no")
    add(s, z, "EMI (EM38-type, conductivity + in-phase)", "T-a 21.3 kg/talent (149 kg)", 0.0, 0.10, "PHYS as above", "as above", "iron litter", "no")
    add(s, z, "EMI (EM38-type, conductivity + in-phase)", "T-b", 0.0, 0.05, "INF", "no contrast", "-", "no")
    add(s, z, "Metal detection (PI large loop; TDEM EM61-type)", "T-a 10 kg/talent (70 kg)", 0.25, 0.45,
        "PUB+PHYS: EM61 drum at 3.5 m (Bauman via S34); 70 kg group reaches ~2.1-2.9 m", "boulder adds 0.5-1 m stand-off; aggradation unknown (run 23)", "iron litter, pipes or fences near the aqueduct", "weak")
    add(s, z, "Metal detection (PI large loop; TDEM EM61-type)", "T-a 21.3 kg/talent (149 kg)", 0.30, 0.50, "PUB+PHYS as above", "as above", "as above", "weak")
    add(s, z, "Metal detection (PI large loop; TDEM EM61-type)", "T-b", 0.0, 0.05, "INF", "no conductor", "-", "no")
    for t in ("T-a 10 kg/talent (70 kg)", "T-a 21.3 kg/talent (149 kg)", "T-b"):
        add(s, z, "Magnetometry (fluxgate/caesium gradiometer)", t, 0.0, 0.05, "PUB: non-ferrous metals give no anomaly (Geometrics via T19)", "no induced anomaly", "magnetic boulders, iron litter", "no")
        add(s, z, "Muon imaging (method 5)", t, 0.0, 0.20 if t == "T-b" else 0.05,
            "PHYS/INF: the aqueduct tunnel at the head could host a detector below the zone (M&P 2018 Figs. 86-87 p. 76); method-5 limit >=1 m chambers",
            "object below resolution; tunnel geometry unknown", "tunnel, fractures", "no")
        add(s, z, "Microgravity", t, 0.0, 0.05, "PHYS: void 0.9-3.6 uGal at 1-2 m; noise 3-5 uGal, worse in rough terrain", "terrain corrections", "boulders, tunnel", "no")
    for m in ("GPR 100/250/500 MHz", "ERT (2D/3D, 0.25-0.5 m spacing)", "EMI (EM38-type, conductivity + in-phase)",
              "Metal detection (PI large loop; TDEM EM61-type)", "Magnetometry (fluxgate/caesium gradiometer)",
              "Muon imaging (method 5)", "Microgravity"):
        add(s, z, m, "T-c", 0.0, 0.02, "INF", "too small", "any small clutter", "no")


z2()
order = {"Z1": 0, "Z2": 1, "Z3": 2}
rows.sort(key=lambda r: (order[r[1]], r[2], r[3]))
with open(os.path.join(OUT, "methods.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(HDR)
    w.writerows(rows)
n_methods = len(rows)

# ---------------- controls
rows = []
L71 = {"gpr": (0.10, 0.25), "ert": (0.0, 0.05), "emi": (0.10, 0.20), "pi": (0.25, 0.40)}
L71H = {"gpr": (0.20, 0.30), "gpr_tb": (0.15, 0.30), "ert": (0.05, 0.15), "ert_tb": (0.15, 0.25),
        "emi": (0.20, 0.30), "emi_tb": (0.0, 0.05), "pi": (0.40, 0.60)}
qumran_marl_block("L71 (control)", "crack zone east of L71 (eastern dump, M&P Figs. 71-74)",
                  (("T-a 5 kg", L71), ("T-a 50 kg", L71H)), "3 m",
                  "open dump ground, balks and the L71 railing; coverage ~70-95%", True,
                  extra_fp="; dump fill rich in pottery waste, ash and occupation metal; L71 railing")


def hyrcania():
    s = "Hyrcania double pool (control)"; z = "east of the double pool, 15 m x 4 m, 0-3 m"
    fp = "rock fractures, quarry steps, benches, plaster patches"
    add(s, z, "GPR 100/250/500 MHz", "T-a 5 kg", 0.30, 0.50,
        "PHYS: dry Hatrurim rock 200-2000 ohm-m (INF), reach >>3 m; PUB: Cave of Letters GPR ~3 m at 450 MHz (Jol via S34)",
        "rough rock-cut surface, benches and slope limit antenna coupling and coverage", fp, "partly")
    add(s, z, "GPR 100/250/500 MHz", "T-a 50 kg", 0.40, 0.65, "PHYS/PUB as above", "coverage on benches and path", fp, "partly")
    add(s, z, "GPR 100/250/500 MHz", "T-b", 0.35, 0.60, "PHYS/PUB as above", "a deposit in a rock fissure looks like other fissures", fp, "partly")
    add(s, z, "ERT (2D/3D, 0.25-0.5 m spacing)", "T-a 5 kg", 0.0, 0.05, "PHYS/INF", "poor electrode contact on bare rock", fp, "no")
    add(s, z, "ERT (2D/3D, 0.25-0.5 m spacing)", "T-a 50 kg", 0.05, 0.15, "PHYS/INF: conductive metal in resistive rock has good contrast but contact is poor", "contact, resolution", fp, "no")
    add(s, z, "ERT (2D/3D, 0.25-0.5 m spacing)", "T-b", 0.05, 0.15, "PHYS/INF: air void in resistive rock has low contrast", "low contrast", fp, "no")
    add(s, z, "EMI (EM38-type, conductivity + in-phase)", "T-a 5 kg", 0.05, 0.15, "PHYS", "depth; magnetic Hatrurim rock may add in-phase noise (INF)", "magnetic rock, iron litter", "no")
    add(s, z, "EMI (EM38-type, conductivity + in-phase)", "T-a 50 kg", 0.15, 0.25, "PHYS", "depth", "magnetic rock, iron litter", "no")
    add(s, z, "EMI (EM38-type, conductivity + in-phase)", "T-b", 0.0, 0.05, "INF", "no contrast", "-", "no")
    add(s, z, "Metal detection (PI large loop; TDEM EM61-type)", "T-a 5 kg", 0.20, 0.35, "PUB+PHYS as at Qumran", "depth; uneven rock limits loop placement", "iron litter, cross-marked rock with modern pegs", "no")
    add(s, z, "Metal detection (PI large loop; TDEM EM61-type)", "T-a 50 kg", 0.30, 0.55, "PUB+PHYS as at Qumran", "lower zone beyond reach; coverage", "iron litter", "weak")
    add(s, z, "Metal detection (PI large loop; TDEM EM61-type)", "T-b", 0.0, 0.05, "INF", "no conductor", "-", "no")
    for t in ("T-a 5 kg", "T-a 50 kg", "T-b"):
        add(s, z, "Magnetometry (fluxgate/caesium gradiometer)", t, 0.0, 0.02,
            "PUB: non-ferrous metals give no anomaly; Hatrurim combustion rocks are strongly and variably magnetic (Khesin et al. 2005, title only read)",
            "no induced anomaly; geological noise", "magnetic rock", "no")
        add(s, z, "Muon imaging (method 5)", t, 0.0, 0.20 if t == "T-b" else (0.10 if t == "T-a 50 kg" else 0.01),
            "PHYS: detector on the northern pool floor (up to 5 m deep, Patrich 1989 p. 255) looks up through rock; method-5 limit >=1 m chambers",
            "object below resolution", "quarry steps, fissures", "no")
        add(s, z, "Microgravity", t, 0.0, 0.05, "PHYS: void 0.9-3.6 uGal at 1-2 m; quarry relief needs cm terrain model", "terrain corrections dominate", "quarry relief, fissures", "no")
    for m in ("GPR 100/250/500 MHz", "ERT (2D/3D, 0.25-0.5 m spacing)", "EMI (EM38-type, conductivity + in-phase)",
              "Metal detection (PI large loop; TDEM EM61-type)", "Magnetometry (fluxgate/caesium gradiometer)",
              "Muon imaging (method 5)", "Microgravity"):
        add(s, z, m, "T-c", 0.0, 0.05 if m.startswith("GPR") else 0.02, "INF", "too small", "any small clutter", "no")


hyrcania()
rows.sort(key=lambda r: (r[0], r[2], r[3]))
with open(os.path.join(OUT, "controls.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(HDR)
    w.writerows(rows)
print("methods rows", n_methods, "controls rows", len(rows))
