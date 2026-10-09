"""Tests for the arrival register.

Run from the repository root:
    python3 -I -m unittest discover -s research/preregistration/arrivals -t research/preregistration/arrivals
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"arrivals_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BUILD = _load("build_register")
ARRIVAL = _load("arrival")
HEBREW = re.compile(r"[֐-׿]")
XII10_ITEMS = {"usc-wsrp-masters-cuts-21-22", "manchester-museum-allegro", "taylor-dqcaas-allegro-scans",
               "ebaf-edf-copy-and-xrays-21-22", "hogenhaven-independent-readings", "uml-tpa-1-132-wright-baker"}


class BuiltRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = BUILD.build()
        cls.committed = json.loads((HERE / "register.json").read_text(encoding="utf-8"))
        cls.items = {i["id"]: i for i in cls.register["items"]}

    def test_deterministic_and_matches_committed_when_sources_unchanged(self):
        again = BUILD.build()
        self.assertEqual(json.dumps(self.register, ensure_ascii=False), json.dumps(again, ensure_ascii=False))
        if self.register["sources"] != self.committed["sources"]:
            self.skipTest("upstream sources changed since registration; the frozen copy is kept")
        with tempfile.TemporaryDirectory() as tmp:
            BUILD.write_all(self.register, Path(tmp))
            for rel in ["register.json", "RANKING.md"] + [f"items/{p.name}" for p in (HERE / "items").glob("*.md")]:
                self.assertEqual((Path(tmp) / rel).read_bytes(), (HERE / rel).read_bytes(), rel)

    def test_all_listed_items_present_and_none_arrived(self):
        self.assertEqual(len(self.items), 22)
        for item in self.items.values():
            self.assertIn(item["status"], ARRIVAL.ALLOWED_STATUS, item["id"])
            if item["status"] == "partial":
                self.assertTrue(item["arrived_before_registration"], item["id"])

    def test_silence_is_an_outcome_and_never_a_fail(self):
        for item in self.items.values():
            ids = item["registered_outcome_ids"]
            self.assertIn("item:silent", ids)
            # Decision-row names come from discriminate.py (for example a reading gate that fails);
            # no other registered outcome may be a FAIL verdict.
            self.assertFalse(any("fail" in o.lower() for o in ids if not o.startswith("dec:")), item["id"])
            for link in item["chain_links"]:
                self.assertIn(f"chain:{link['link']}:silent", ids)
                if link["contradiction_strength"] == "one-sided":
                    self.assertNotIn(f"chain:{link['link']}:contradict", ids)

    def test_chain_links_match_chain_json(self):
        chain = json.loads((BUILD.REPO / "research/assessments/kohlit_chain/chain.json").read_text(encoding="utf-8"))
        specs = BUILD.load_specs()
        for spec in specs.ITEMS:
            wanted = set(spec.get("chain_record_ids", []))
            expected = {l["id"] for m in chain["models"] for l in m["next_links"] if wanted & set(l.get("record_ids", []))}
            expected |= {e["link"] for e in spec.get("extra_links", [])}
            got = {l["link"] for l in self.items[spec["id"]]["chain_links"]}
            self.assertEqual(expected, got, spec["id"])

    def test_xii10_mapping_rule(self):
        rows = self.items["usc-wsrp-masters-cuts-21-22"]["decision_rows"]
        self.assertEqual(len(rows), 29)
        janoah = {"kohlit-c08", "kohlit-c09", "kohlit-c10"}
        for r in rows:
            excluded = set(r["excluded"].get("kohlit", []))
            if "xii10-c04" in r["surviving"]["xii10"]:
                self.assertEqual(excluded, set(), r["id"])
            else:
                self.assertEqual(excluded, janoah, r["id"])

    def test_no_letter_predictions_in_reserved_items(self):
        for iid in XII10_ITEMS:
            item = self.items[iid]
            for pred in item.get("other_predictions", []):
                text = " ".join(str(v) for v in pred.values())
                self.assertIsNone(HEBREW.search(text), f"{iid}: Hebrew in a prediction")
            md = (HERE / "items" / f"{iid}.md").read_text(encoding="utf-8")
            self.assertNotIn("reads an extra stroke", md, iid)

    def test_l656_has_no_bearing_rows(self):
        for r in self.items["l656-field-file"]["decision_rows"]:
            comps = r["components"] or {}
            self.assertIn(comps.get("bearing"), (None, "undetermined"))

    def test_ranking(self):
        main = self.register["ranking"]["decisive_share_0.5"]
        ranked = {r["item"]: r for r in main}
        self.assertEqual(len(main), 21)
        self.assertNotIn("facsimile-editions-3d-scan", ranked)
        self.assertEqual(ranked["hogenhaven-independent-readings"]["E_total"], 0.0)
        self.assertEqual(ranked["garstang-museum-jg8"]["E_total"], 0.0)
        totals = [r["E_total"] for r in main]
        self.assertEqual(totals, sorted(totals, reverse=True))

    def test_expected_value_formulas(self):
        rows = [{"kind": "decisive", "n_excluded": 4}, {"kind": "decisive", "n_excluded": 0},
                {"kind": "partial", "n_excluded": 2}, {"kind": "not_obtained", "n_excluded": 0}]
        value, best = BUILD.e_dec(rows, 1.0, 0.5)
        self.assertAlmostEqual(value, 0.5 * 1.0 + 0.5 * 2.0)
        self.assertEqual(best, 4)
        self.assertEqual(BUILD.e_dec(rows, 0.0, 0.5), (0.0, 0))
        links = [{"model": "M-X", "branches_excludable": ["RB-M"], "coverage": 1.0},
                 {"model": "M-X", "branches_excludable": ["RB-M", "RB-P"], "coverage": 0.5}]
        value, best = BUILD.e_chain(links, set(), 0.5)
        p1, p2 = 0.25, 0.125
        self.assertAlmostEqual(value, ((1 - (1 - p1) * (1 - p2)) + p2) / 3)
        self.assertAlmostEqual(best, 2 / 3)

    def test_link_branches(self):
        self.assertEqual(BUILD.link_branches("RB-M only"), ["RB-M"])
        self.assertEqual(BUILD.link_branches("all branches using the historical basin"), ["RB-M", "RB-P", "RB-B"])
        self.assertEqual(BUILD.link_branches("RB-M, RB-P, RB-L"), ["RB-M", "RB-P"])


class Manifest(unittest.TestCase):
    def test_committed_manifest_checks(self):
        self.assertEqual(ARRIVAL.check(HERE), [])

    def test_tamper_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "a"
            shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("__pycache__", "outcomes"))
            self.assertEqual(ARRIVAL.check(dst), [])
            path = dst / "items" / "kochavi-1972.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nedited\n", encoding="utf-8")
            (dst / "items" / "extra.md").write_text("x", encoding="utf-8")
            problems = ARRIVAL.check(dst)
            self.assertIn("hash mismatch: items/kochavi-1972.md", problems)
            self.assertIn("present but not in manifest: items/extra.md", problems)


class OutcomeValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = json.loads((HERE / "register.json").read_text(encoding="utf-8"))

    def record(self, **over):
        rec = {"item_id": "kochavi-1972", "register_commit": "abc", "register_pushed_before_arrival": True,
               "arrived_utc": "2026-11-02T18:00:00Z", "opened_by": "r", "compared_by": "c", "manifest_check": "pass",
               "parts_received": ["Kallai pp. 172–173"], "parts_pending": [],
               "scores": [{"outcome_id": "dec:identity-only:east+undated", "evidence": "p. 173"},
                          {"outcome_id": "chain:S2376-1-pool-east:silent", "evidence": ""}],
               "unregistered_observations": []}
        rec.update(over)
        return rec

    def test_valid_record(self):
        self.assertEqual(ARRIVAL.validate(self.record(), self.register), [])

    def test_procedure_example_is_valid(self):
        text = (HERE / "ARRIVAL_PROCEDURE.md").read_text(encoding="utf-8")
        block = text.split("```json", 1)[1].split("```", 1)[0]
        self.assertEqual(ARRIVAL.validate(json.loads(block), self.register), [])

    def test_unknown_outcome_rejected(self):
        bad = self.record(scores=[{"outcome_id": "chain:S2376-1-pool-east:fail", "evidence": "x"}])
        self.assertTrue(any("not registered" in e for e in ARRIVAL.validate(bad, self.register)))

    def test_two_outcomes_for_one_prediction_rejected(self):
        bad = self.record(scores=[{"outcome_id": "chain:S2376-1-pool-east:silent"},
                                  {"outcome_id": "chain:S2376-1-pool-east:confirm", "evidence": "x"}])
        self.assertTrue(any("two outcomes" in e for e in ARRIVAL.validate(bad, self.register)))

    def test_not_pushed_requires_exploratory(self):
        bad = self.record(register_pushed_before_arrival=False)
        self.assertTrue(ARRIVAL.validate(bad, self.register))
        ok = self.record(register_pushed_before_arrival=False, test_status="exploratory")
        self.assertEqual(ARRIVAL.validate(ok, self.register), [])

    def test_silence_marked_fail_rejected(self):
        bad = self.record(scores=[{"outcome_id": "chain:S2376-1-pool-east:silent", "result": "FAIL"}])
        self.assertTrue(any("never a FAIL" in e for e in ARRIVAL.validate(bad, self.register)))

    def test_declined_item_rejected(self):
        bad = self.record(item_id="facsimile-editions-3d-scan", scores=[])
        self.assertTrue(any("declined" in e for e in ARRIVAL.validate(bad, self.register)))


if __name__ == "__main__":
    unittest.main()
