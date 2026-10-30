"""Run 24: simple physics and coverage model for P(detect | target present).

Exploratory. Every input is a range; the script samples each uniformly and
reports the 10th-90th percentile of P. Inputs marked EVIDENCE come from a
source (see RESULT_DRAFT.md); the rest are INFERENCE.

P = coverage x P(target depth <= method reach) x P(anomaly recognised and
confirmed by a second method).

Run: python3 detect_model.py > ../physics_model_output.txt
"""
import math
import random

random.seed(24)
N = 20000
U = random.uniform


def pct(xs, q):
    xs = sorted(xs)
    return xs[int(q * (len(xs) - 1))]


# ---------------------------------------------------------------- GPR
def gpr_reach(rho_lo, rho_hi, er_lo, er_hi, budget_lo=60, budget_hi=80, clay_factor=(1.0, 2.0)):
    """Two-way attenuation budget (dB) / (2 * alpha). alpha = 1636*sigma/sqrt(er) dB/m
    (low-loss approximation). clay_factor multiplies alpha for dispersive clay losses
    at 250-500 MHz (INFERENCE)."""
    out = []
    for _ in range(N):
        sigma = 1.0 / U(rho_lo, rho_hi)
        er = U(er_lo, er_hi)
        alpha = 1636 * sigma / math.sqrt(er) * U(*clay_factor)
        out.append(U(budget_lo, budget_hi) / (2 * alpha))
    return out


# ---------------------------------------------------------------- EM (TDEM / PI / EMI)
def em_reach(d_eff, z_ref, coil_h, coupling=(0.3, 1.0), d_ref=0.65):
    """Dipole scaling: response ~ D^3 / z^6, threshold set by a reference target
    (55-gal steel drum, equivalent sphere ~0.65 m) detected at z_ref below ground.
    Distance is measured from the coil. coupling < 1 for a loose group of vessels
    (less coherent eddy-current paths than a closed drum)."""
    out = []
    for _ in range(N):
        D = U(*d_eff)
        zr = U(*z_ref) + coil_h
        c = U(*coupling)
        z = zr * (D / d_ref) ** 0.5 * c ** (1 / 6) - coil_h
        out.append(max(z, 0.0))
    return out


# ---------------------------------------------------------------- gravity, magnetics
G = 6.674e-11


def grav_ugal(mass_kg, z_m):
    return G * mass_kg / z_m ** 2 * 1e8  # 1 uGal = 1e-8 m/s^2


def mag_nT(M_A_per_m, vol_m3, r_m):
    m = M_A_per_m * vol_m3
    return 1e-7 * 2 * m / r_m ** 3 * 1e9


# ---------------------------------------------------------------- combine
def p_detect(reach, depth_sampler, coverage, recog):
    ps = []
    for i in range(N):
        r = reach[i]
        d = depth_sampler()
        ps.append((1.0 if d <= r else 0.0))
    # turn into probability by averaging in blocks, then multiply by coverage and recog ranges
    block = 200
    res = []
    for b in range(0, N, block):
        frac = sum(ps[b:b + block]) / block
        res.append(frac * U(*coverage) * U(*recog))
    return pct(res, 0.1), pct(res, 0.5), pct(res, 0.9)


def depth_uniform(lo, hi):
    return lambda: U(lo, hi)


def depth_z2():
    # 3 cubits (1.3-1.6 m) below the ancient surface, plus unknown aggradation 0-1 m,
    # plus the "great stone" if still in place (0-1 m), INFERENCE
    return U(1.3, 1.6) + U(0, 1.0) + U(0, 1.0)


def depth_z3():
    return U(1.3, 1.6) + U(0, 0.5)


# Soil inputs
# Qumran marl: ERT west of ruins (Bauman; Freund 2012 Fig. 3.2) shows marl in the
# lowest colour bin (<= ~50 ohm-m). Lower bound 20 ohm-m is INFERENCE (wetter or
# saltier spots). Hyrcania: dry quarried Hatrurim rock, INFERENCE 200-2000 ohm-m.
SOIL = {
    "qumran_marl": dict(rho=(20, 50), er=(9, 20), clay=(1.5, 3.0)),
    "hyrcania_rock": dict(rho=(200, 2000), er=(5, 9), clay=(1.0, 1.5)),
    "z2_gravel": dict(rho=(50, 300), er=(5, 12), clay=(1.0, 2.0)),
}

TARGET_DEFF = {  # equivalent-sphere size of a group of vessels, INFERENCE
    "Ta_5kg": (0.10, 0.20),
    "Ta_50kg": (0.25, 0.45),
    "Z2_70_149kg": (0.35, 0.60),
    "Z3_230_490kg": (0.50, 0.80),
}

EM = {  # z_ref = depth at which the reference drum is detected; coil height
    "TDEM_EM61": dict(z_ref=(3.0, 3.5), coil=0.4),   # Bauman: EM61 drum at 3.5 m; spec ~3 m
    "PI_large_loop": dict(z_ref=(3.0, 4.0), coil=0.1),
    "EMI_EM38_inphase": dict(z_ref=(1.5, 2.0), coil=0.2),
}

ZONES = {
    # coverage of open (non-wall, non-railing) ground; recognition ranges
    "Z1": dict(soil="qumran_marl", depth=depth_uniform(0, 3), cov=(0.6, 0.9)),
    "Z2": dict(soil="z2_gravel", depth=depth_z2, cov=(0.5, 0.9)),
    "Z3": dict(soil="qumran_marl", depth=depth_z3, cov=(0.7, 0.95)),
    "L71": dict(soil="qumran_marl", depth=depth_uniform(0, 3), cov=(0.7, 0.95)),
    "Hyrcania": dict(soil="hyrcania_rock", depth=depth_uniform(0, 3), cov=(0.5, 0.85)),
}

REC_METAL = (0.7, 0.95)
REC_VOID = (0.4, 0.8)

if __name__ == "__main__":
    print("== GPR reach (m) for a 0.6 m target ==")
    gpr = {}
    for k, s in SOIL.items():
        r = gpr_reach(*s["rho"], *s["er"], clay_factor=s["clay"])
        gpr[k] = r
        print(f"{k:14s} p10 {pct(r,0.1):.2f}  p50 {pct(r,0.5):.2f}  p90 {pct(r,0.9):.2f}")

    print("\n== EM reach (m below ground) ==")
    emr = {}
    for m, e in EM.items():
        for t, d in TARGET_DEFF.items():
            r = em_reach(d, e["z_ref"], e["coil"])
            emr[(m, t)] = r
            print(f"{m:18s} {t:14s} p10 {pct(r,0.1):.2f}  p50 {pct(r,0.5):.2f}  p90 {pct(r,0.9):.2f}")

    print("\n== Microgravity (uGal) ==")
    void_mass = 0.6 * 0.6 * 0.8 * 1850  # air-filled jar-sized void in marl, kg deficit
    for z in (0.7, 1.0, 1.5, 2.0, 3.0):
        print(f"void 0.29 m3 at centre depth {z} m: {grav_ugal(void_mass, z):.2f} uGal; "
              f"50 kg silver (net +40 kg): {grav_ugal(40, z):.3f} uGal")
    print("field noise with repeats: 3-5 uGal (INFERENCE); need >= ~2x noise")

    print("\n== Magnetometry: fired storage jar (0.015 m3 ceramic) ==")
    for M in (0.1, 1.0):
        print(f"M={M} A/m: " + ", ".join(f"r={r} m {mag_nT(M,0.015,r):.2f} nT" for r in (1.0, 1.5, 2.0, 3.0)))
    print("silver/bronze: non-ferrous, no induced anomaly (Geometrics, via T19)")

    print("\n== P(detect | present), p10 / p50 / p90 ==")
    for z, cfg in ZONES.items():
        soil = cfg["soil"]
        targets = ["Ta_5kg", "Ta_50kg"] if z in ("Z1", "L71", "Hyrcania") else (
            ["Z2_70_149kg"] if z == "Z2" else ["Z3_230_490kg"])
        for m in EM:
            for t in targets:
                lo, mid, hi = p_detect(emr[(m, t)], cfg["depth"], cfg["cov"], REC_METAL)
                print(f"{z:9s} {m:18s} {t:14s} {lo:.2f} / {mid:.2f} / {hi:.2f}")
        lo, mid, hi = p_detect(gpr[soil], cfg["depth"], cfg["cov"], REC_VOID)
        print(f"{z:9s} {'GPR_250_500MHz':18s} {'Tb_void_jar':14s} {lo:.2f} / {mid:.2f} / {hi:.2f}")
        lo, mid, hi = p_detect(gpr[soil], cfg["depth"], cfg["cov"], (0.6, 0.9))
        print(f"{z:9s} {'GPR_250_500MHz':18s} {'Ta_metal_refl':14s} {lo:.2f} / {mid:.2f} / {hi:.2f}")
        # ERT: a 0.6 m body is resolved to ~3x its radius (0.9-1.2 m) with 0.25-0.5 m spacing
        ert = [U(0.9, 1.5) for _ in range(N)]
        lo, mid, hi = p_detect(ert, cfg["depth"], cfg["cov"], REC_VOID)
        print(f"{z:9s} {'ERT_3D':18s} {'Tb_void_jar':14s} {lo:.2f} / {mid:.2f} / {hi:.2f}")
        # microgravity: void only, centre depth <= 0.8-1.1 m, void must survive (0.1-0.5)
        mg = [U(0.8, 1.1) for _ in range(N)]
        lo, mid, hi = p_detect(mg, cfg["depth"], cfg["cov"], (0.05, 0.4))
        print(f"{z:9s} {'microgravity':18s} {'Tb_void_only':14s} {lo:.2f} / {mid:.2f} / {hi:.2f}")
