#!/usr/bin/env python3
"""Regression checks on the reviewed T06 inputs. Run: python3 -I <this file>."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

HERE = Path(__file__).resolve().parent

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

jm = module("current_v1", HERE / "joint_model_v1.py")
j0 = module("current_t06", HERE.parents[2] / "wave1/T06_joint_model/scripts/joint_model.py")

class KernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = jm.Data(HERE.parent / "inputs", "v0")

    def mdl(self, **kw):
        return jm.Model(self.data, jm.cfg_with(w_A=0.0, w_L=0.995, rho=0.0, **kw))

    def test_normalization_and_independence(self):
        for mode in ("fixed", "sinkhorn"):
            m = self.mdl(transition=mode)
            for w in (0, .8, .995, 1):
                t = m.transition(w)
                np.testing.assert_allclose(t.sum(1), 1, atol=1e-12)
                self.assertGreaterEqual(t.min(), 0)
            t = m.transition(0)
            np.testing.assert_allclose(t, np.broadcast_to(m.pi, t.shape))
        m = jm.Model(self.data, jm.cfg_with(w_A=0, w_L=0, rho=0))
        r = m.run()
        for i, e in enumerate(r["order"]):
            np.testing.assert_allclose(r["post"][i], r["ev"][e][1], atol=1e-10)
        self.assertAlmostEqual(r["logml"], 0, places=9)

    def test_regression_tell_demoted_only_by_legacy_kernel(self):
        tell = {}
        north = {}
        for mode in ("fixed", "sinkhorn"):
            m = self.mdl(transition=mode)
            r = m.run()
            p = r["post"][r["order"].index("60")]
            tell[mode] = float(p[m.idx["tell_es_sultan"]])
            north[mode] = m.region_probs(p)["NORTH"]
        # Recorded W2B values, independent of defaults in the implementation.
        self.assertAlmostEqual(tell["sinkhorn"], .099, delta=.0005)
        self.assertAlmostEqual(tell["fixed"], .279, delta=.0005)
        self.assertAlmostEqual(north["sinkhorn"], .711, delta=.0005)
        self.assertAlmostEqual(north["fixed"], .104, delta=.0005)

    def test_t06_and_v1_agree_in_both_modes(self):
        d0 = j0.Data(HERE.parents[2] / "wave1/T06_joint_model/inputs")
        for mode in ("fixed", "sinkhorn"):
            cfg = dict(w_A=.4, w_L=.995, rho=.9, transition=mode)
            a = j0.Model(d0, j0.cfg_with(**cfg)).run()
            b = jm.Model(self.data, jm.cfg_with(**cfg)).run()
            np.testing.assert_allclose(a["post"], b["post"], atol=1e-10)
            self.assertAlmostEqual(a["logml"], b["logml"], places=9)
            if mode == "sinkhorn":
                self.assertAlmostEqual(a["logml"], 8.6831, delta=.00005)

    def test_fixed_chain_without_evidence_has_markov_drift(self):
        m = self.mdl()
        r = m.run(drop=self.data.order)
        q = m.pi.copy()
        for i, e in enumerate(r["order"]):
            if i:
                w = m.c["w_A"] if self.data.block[e] == self.data.block[r["order"][i-1]] == "A" else m.c["w_L"]
                q = q @ m.transition(w)
            np.testing.assert_allclose(r["post"][i], q, atol=1e-10)
        self.assertGreater(np.abs(q-m.pi).max(), .001)
        self.assertAlmostEqual(r["logml"], 0, places=9)

    def test_coincident_state_split_preserves_aggregate_transition(self):
        # Split one location into two labels while preserving its total prior mass.
        # This checks probability mass, not two newly independent pieces of evidence.
        k = np.array([[1., .3, .1], [.3, 1., .2], [.1, .2, 1.]])
        pi = np.array([.5, .3, .2])
        def synthetic(k, pi, mode):
            m = object.__new__(jm.Model)
            m.S = len(pi); m.pi = pi
            m.c = dict(transition=mode, scale_w=(1.,), scales=(1.,))
            m.kernel = lambda lam, ell: k
            return m.local_transition(2)
        mapping = [0, 0, 1, 2]
        kk = k[np.ix_(mapping, mapping)]
        pp = np.array([.2, .3, .3, .2])
        for mode in ("fixed", "sinkhorn"):
            t = synthetic(k, pi, mode)
            u = synthetic(kk, pp, mode)
            merged = np.column_stack((u[:, 0]+u[:, 1], u[:, 2], u[:, 3]))
            np.testing.assert_allclose(merged, t[mapping], atol=1e-12)

    def test_invalid_mode_fails(self):
        with self.assertRaisesRegex(ValueError, "unknown transition"):
            self.mdl(transition="fiexed").transition(.8)

if __name__ == "__main__":
    unittest.main()
