#!/usr/bin/env python3
"""Bounded kernel/exclusion sensitivity; historical outputs remain untouched."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("jm", HERE / "joint_model_v1.py")
jm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jm)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE.parent / "outputs_fixed")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for suffix in ("v0", "v1"):
        d = jm.Data(HERE.parent / "inputs", suffix)
        for transition, grid in (("sinkhorn", 0), ("fixed", 0), ("fixed", 5)):
            # Retain old priors to isolate the kernel; no new archaeological odds.
            for rho, wa, wl, excl in ((0., 0., 0., ()), (0., 0., .995, ()),
                                     (.9, 0., .995, ()), (.9, .4, .995, ()),
                                     (0., 0., .8, ("documented", "likely"))):
                cfg = jm.cfg_with(transition=transition, grid_km=grid, grid_mass=10.,
                                  rho=rho, w_A=wa, w_L=wl, exclude_order_derived=excl)
                m = jm.Model(d, cfg)
                r = m.run()
                p = r["post"][r["order"].index("60")]
                T = m.transition(wl)
                rp = m.region_probs(p)
                rows.append(dict(inputs=suffix, transition=transition, grid_km=grid,
                                 rho=rho, w_A=wa, w_L=wl, excluded="|".join(excl),
                                 logml=float(r["logml"]),
                                 P_tell_es_sultan=float(p[m.idx["tell_es_sultan"]]),
                                 P_north_32_05=float(sum(p[i] for i, s in enumerate(m.states)
                                     if float(m.W[i] @ m.A[:, 0]) > 32.05)),
                                 R_north=rp["NORTH"], R_background=rp.get("BG", 0.),
                                 max_row_sum_error=float(np.max(np.abs(T.sum(1)-1))),
                                 stationarity_drift=float(np.max(np.abs(m.pi @ T-m.pi)))))
                print(suffix, transition, grid, rho, wa, wl, flush=True)
    jm.write_csv(a.out / "kernel_sensitivity.csv", rows)
    files = [HERE / "joint_model_v1.py", HERE / "check_order_kernel.py"]
    files += sorted((HERE.parent / "inputs").glob("*_v[01].csv"))
    hashes = {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    metadata = dict(date_utc="2026-10-08", source_ref="83230367bf6a592c35f8f8e060e744e3b5ff5604",
                    scope="30 bounded sensitivity runs; old numeric priors; no refit or new field evidence",
                    default="K2 fixed normalizer; pi need not be stationary",
                    input_and_code_sha256=hashes)
    (a.out / "kernel_validation.json").write_text(json.dumps(metadata, indent=2)+"\n")

if __name__ == "__main__":
    main()
