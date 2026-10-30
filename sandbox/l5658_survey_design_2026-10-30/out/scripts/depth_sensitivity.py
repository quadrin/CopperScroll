"""Run 24: rule ambiguity check. RULE.md fixes Z1 as 0-3 m but gives no depth
distribution. Score Z1 under three depth priors. Uses detect_model.py."""
import detect_model as m
for name, lo, hi in (("uniform 0-3 m (main)", 0, 3), ("shallow 0-1.5 m", 0, 1.5), ("deep 1.5-3 m", 1.5, 3)):
    for meth in ("PI_large_loop", "TDEM_EM61"):
        for t in ("Ta_5kg", "Ta_50kg"):
            r = m.em_reach(m.TARGET_DEFF[t], m.EM[meth]["z_ref"], m.EM[meth]["coil"])
            print(name, meth, t, "%.2f / %.2f / %.2f" % m.p_detect(r, m.depth_uniform(lo, hi), (0.6, 0.9), m.REC_METAL))
    g = m.gpr_reach(*m.SOIL["qumran_marl"]["rho"], *m.SOIL["qumran_marl"]["er"], clay_factor=m.SOIL["qumran_marl"]["clay"])
    print(name, "GPR", "Tb", "%.2f / %.2f / %.2f" % m.p_detect(g, m.depth_uniform(lo, hi), (0.6, 0.9), m.REC_VOID))
    # pair PI + GPR (union, metal): detected if within either reach
    rp = m.em_reach(m.TARGET_DEFF["Ta_50kg"], m.EM["PI_large_loop"]["z_ref"], 0.1)
    both = [max(a, b) for a, b in zip(rp, g)]
    print(name, "PI+GPR union", "Ta_50kg", "%.2f / %.2f / %.2f" % m.p_detect(both, m.depth_uniform(lo, hi), (0.6, 0.9), m.REC_METAL))
