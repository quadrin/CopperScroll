"""Tests for the RAF 1940s layer record set.

    python3 -I -m unittest discover -s research/regional/raf_1940s -p 'test_*.py'
"""
import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
KC = REPO / "research/assessments/kohlit_chain"
REG = KC / "registrations"
DOC = "POM-aerial1940s-z16-jericho"

_spec = importlib.util.spec_from_file_location("kc_reg_raf", KC / "registration.py")
RG = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RG)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name):
    return json.loads((REG / name).read_text(encoding="utf-8"))


class Freeze(unittest.TestCase):
    def test_hashes_in_readme_match_files(self):
        readme = (HERE / "README.md").read_text(encoding="utf-8")
        for suffix in (".declaration.json", ".prepreview.json", ".checkpoint.json", ".gate.json", ".json"):
            self.assertIn(sha(REG / (DOC + suffix)), readme, suffix)
        self.assertIn(sha(HERE / "tile_manifest.txt"), readme)

    def test_chain_of_hashes(self):
        self.assertEqual(sha(REG / (DOC + ".declaration.json")), load(DOC + ".prepreview.json")["declaration_sha256"])
        self.assertEqual(sha(REG / (DOC + ".prepreview.json")), load(DOC + ".checkpoint.json")["prepreview_sha256"])
        self.assertEqual(sha(REG / (DOC + ".checkpoint.json")), load(DOC + ".gate.json")["checkpoint_sha256"])
        self.assertEqual(sha(HERE / "tile_manifest.txt"), load(DOC + ".json")["document"]["sha256"])
        self.assertEqual(sha(HERE / "source_record.json"),
                         load(DOC + ".declaration.json")["protocol_files_sha256"]["source_record.json"])

    def test_prediction_copied_verbatim(self):
        chain = json.loads((KC / "chain.json").read_text(encoding="utf-8"))
        link = next(l for m in chain["models"] for l in m.get("next_links", []) if l["id"] == "SULTAN-1-precamp-mouth")
        pred = load(DOC + ".declaration.json")["registered_prediction"]
        for key in ("expect", "where", "success", "contradiction", "contradiction_strength"):
            self.assertEqual(link[key], pred[key], key)


class Gate(unittest.TestCase):
    def test_gate_arithmetic(self):
        g = load(DOC + ".gate.json")
        counted = sorted(e["rise_m"] for e in g["edges"] if e["contrast_grey"] >= 30)
        self.assertEqual(g["n_counted"], len(counted))
        self.assertGreaterEqual(len(counted), 3)
        mid = len(counted) // 2
        med = counted[mid] if len(counted) % 2 else (counted[mid - 1] + counted[mid]) / 2
        self.assertAlmostEqual(g["median_edge_rise_m"], med, places=2)
        r_eff = max(g["nominal_ground_pixel_m"], med)
        self.assertAlmostEqual(g["R_eff_m"], r_eff, places=2)
        self.assertEqual("FAILED" if r_eff > g["threshold_m"] else "PASSED", g["gate"])

    def test_zone_not_opened_after_failed_gate(self):
        self.assertEqual("FAILED", load(DOC + ".gate.json")["gate"])
        self.assertTrue(load(DOC + ".zone.json")["zone_viewed"].startswith("no"))


class Record(unittest.TestCase):
    def test_result_matches_saved_output(self):
        rec = load(DOC + ".json")
        self.assertTrue(rec["declared_before_fit"])
        out = RG.register(rec, RG.load_reference_points())
        saved = load(DOC + ".result.json")
        self.assertEqual(saved["status"], out["status"])
        self.assertEqual("invalid", out["status"])
        self.assertEqual(saved["blocking"], out["blocking"])
        self.assertEqual([], out["accepted_for"])

    def test_check_point_withheld_and_listed(self):
        rec = load(DOC + ".json")
        cands = RG.load_reference_points()
        self.assertNotIn(rec["check"]["rp"], [c["rp"] for c in rec["controls"]])
        self.assertEqual([], RG.role_problems(rec, cands))


class NoImagery(unittest.TestCase):
    def test_no_image_files(self):
        bad = [p.name for p in HERE.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}]
        self.assertEqual([], bad)


if __name__ == "__main__":
    unittest.main()
