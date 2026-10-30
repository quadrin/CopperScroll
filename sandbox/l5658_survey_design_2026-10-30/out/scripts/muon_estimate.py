"""Run 24: order-of-magnitude muon transmission estimate (method 5).

Inputs (EVIDENCE from the project's method-5 summary): detector ~0.16 m^2;
resolves chambers >= 1 m, not objects; needs a space below the target.
Everything else is INFERENCE.

Geometry: detector on the floor of an adjacent deep pool (L58 4.40 m deep,
L71 5.40 m, Hyrcania northern pool up to 5 m), looking up and sideways
through 3-8 m of marl or rock at the target zone.
"""
import math

AREA_CM2 = 0.16 * 1e4
# integral muon intensity after ~10-15 m water-equivalent at 30-60 deg zenith,
# INFERENCE, order of magnitude only (cm^-2 s^-1 sr^-1)
I_RANGE = (5e-4, 2e-3)
PIXEL_DEG = 3.0                      # angular bin, INFERENCE
OMEGA = math.radians(PIXEL_DEG) ** 2
SLOPE = 2.0                          # |dlnI/dlnX| near 10-15 mwe, INFERENCE
PATH_GCM2 = (5 * 180, 8 * 200)       # 5-8 m of marl (1.8 g/cc) or rock (2.0)

cases = {
    "T-a 50 kg silver (0.3 m cluster, 100 g/cm2 if compact)": dict(dX=50, fill=0.3),
    "T-a 5 kg silver": dict(dX=10, fill=0.1),
    "T-b air void 0.6x0.6x0.8 m in marl (-0.6 m * 1.8 g/cc)": dict(dX=-108, fill=0.6),
    "Chamber 1 m (method-5 limit)": dict(dX=-180, fill=1.0),
}

for name, c in cases.items():
    for X in PATH_GCM2:
        contrast = SLOPE * abs(c["dX"]) / X * c["fill"]
        for I in I_RANGE:
            rate_day = AREA_CM2 * OMEGA * I * 86400
            # counts for a 3-sigma signal: (3/contrast)^2
            need = (3 / contrast) ** 2
            days = need / rate_day
            print(f"{name:55s} X={X:5d} g/cm2 I={I:.0e}: contrast {contrast*100:5.1f}%  "
                  f"rate {rate_day:6.0f}/day/pixel  days for 3 sigma {days:8.1f}")
print("Systematics: walls 0.5-1 m thick give 20-40% contrasts; crack fill, plaster and "
      "density changes of 5-10% over metres swamp the T-a and T-b signals (INFERENCE).")
