"""Tests for check_chain.py: the unused-relation rule, dependencies and ranking."""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("kc_check_chain", HERE / "check_chain.py")
CC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CC)


def tiny():
    """A minimal synthetic chain with one valid model."""
    return {
        "method": {"tiers": {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e"}},
        "relations": [
            {"id": "R-A", "dependencies": [], "reading": "agreed"},
            {"id": "R-B", "dependencies": ["D-X"], "reading": "disputed"},
            {"id": "R-C", "dependencies": ["D-Y"], "reading": "restored"},
        ],
        "reading_dependencies": [{"id": "D-X"}, {"id": "D-Y"}],
        "records": [
            {"id": "REC-1", "title": "seen", "access": "inspected", "pending_request": None},
            {"id": "REC-2", "title": "asked", "access": "requested_pending", "pending_request": "Somebody: something (date)."},
            {"id": "REC-3", "title": "library", "access": "library", "pending_request": None},
        ],
        "models": [{
            "id": "M-1", "label": "one", "rarity": None,
            "selection_relations": ["R-A"],
            "chain": [{"step": 1, "relation": "R-A", "status": "compatible", "feature": "f",
                       "evidence": [{"record": "REC-1", "lineage": "L1"}], "used_for_selection": True}],
            "next_links": [
                {"id": "L-1", "kind": "landmark", "relations": ["R-B"], "expect": "e", "where": "w", "record_ids": ["REC-3"],
                 "success": "s", "contradiction": "c", "contradiction_strength": "two-sided", "priority": 1},
                {"id": "L-2", "kind": "landmark", "relations": ["R-C"], "expect": "e", "where": "w", "record_ids": ["REC-2"],
                 "success": "s", "contradiction": "c", "contradiction_strength": "one-sided", "priority": 2},
            ],
        }],
    }


class RuleTests(unittest.TestCase):
    def test_valid_synthetic_chain(self):
        errors, warnings = CC.validate(tiny())
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_prediction_reusing_a_selection_relation_fails(self):
        doc = tiny()
        doc["models"][0]["next_links"][0]["relations"] = ["R-A"]
        errors, _ = CC.validate(doc)
        self.assertTrue(any("uses R-A, which selected the model" in e for e in errors), errors)

    def test_unknown_relation_record_and_dependency_fail(self):
        doc = tiny()
        link = doc["models"][0]["next_links"][0]
        link["relations"] = ["R-Z"]
        link["record_ids"] = ["REC-9"]
        link["reading_dependencies"] = ["D-Q"]
        errors, _ = CC.validate(doc)
        self.assertTrue(any("unknown relation R-Z" in e for e in errors))
        self.assertTrue(any("unknown record REC-9" in e for e in errors))
        self.assertTrue(any("unknown dependency D-Q" in e for e in errors))

    def test_missing_contradiction_fails(self):
        doc = tiny()
        doc["models"][0]["next_links"][0]["contradiction"] = " "
        errors, _ = CC.validate(doc)
        self.assertTrue(any("missing contradiction" in e for e in errors))

    def test_selection_and_used_steps_must_agree(self):
        doc = tiny()
        doc["models"][0]["selection_relations"] = ["R-A", "R-B"]
        errors, _ = CC.validate(doc)
        self.assertTrue(any("differ from used chain steps" in e for e in errors))

    def test_rarity_match_must_be_a_selection_relation(self):
        doc = tiny()
        doc["relations"].append({"id": "R-E11-POOL-EAST", "dependencies": [], "reading": "agreed"})
        doc["models"][0]["rarity"] = {"unit": "X", "C1": "MATCH", "C2": "UNKNOWN", "C3s": "UNKNOWN"}
        errors, _ = CC.validate(doc)
        self.assertTrue(any("C1 MATCH" in e for e in errors))

    def test_reading_gate_needs_dependency_and_no_relation(self):
        doc = tiny()
        gate = {"id": "G", "kind": "reading_gate", "relations": [], "expect": "e", "where": "w", "record_ids": ["REC-2"],
                "success": "s", "contradiction": "c", "contradiction_strength": "two-sided", "priority": 0}
        doc["models"][0]["next_links"].append(dict(gate))
        errors, _ = CC.validate(doc)
        self.assertTrue(any("reading gate" in e for e in errors))
        gate["id"] = "G2"
        gate["reading_dependencies"] = ["D-X"]
        doc["models"][0]["next_links"][-1] = gate
        errors, _ = CC.validate(doc)
        self.assertEqual([], errors)

    def test_shared_lineage_and_exposed_record_warn(self):
        doc = tiny()
        doc["relations"].append({"id": "R-D", "dependencies": [], "reading": "agreed"})
        doc["models"][0]["selection_relations"].append("R-D")
        doc["models"][0]["chain"].append({"step": 2, "relation": "R-D", "status": "compatible", "feature": "g",
                                          "evidence": [{"record": "REC-1", "lineage": "L1"}], "used_for_selection": True})
        doc["models"][0]["next_links"][0]["record_ids"] = ["REC-1"]
        errors, warnings = CC.validate(doc)
        self.assertEqual([], errors)
        self.assertTrue(any("share lineage 'L1'" in w for w in warnings))
        self.assertTrue(any("exploratory only" in w for w in warnings))

    def test_pending_request_consistency(self):
        doc = tiny()
        doc["records"][1]["pending_request"] = None
        errors, _ = CC.validate(doc)
        self.assertTrue(any("requested_pending without" in e for e in errors))

    def test_dependencies_flag_restored_and_disputed(self):
        deps = CC.dependencies(tiny())["M-1"]
        self.assertEqual(["D-X"], deps["predictions"]["L-1"]["reading_dependencies"])
        self.assertEqual(["disputed"], deps["predictions"]["L-1"]["restored_or_disputed"])
        self.assertEqual(["restored"], deps["predictions"]["L-2"]["restored_or_disputed"])

    def test_ranking_prefers_requested_record_over_library(self):
        rows = CC.ranking(tiny())
        self.assertEqual("L-2", rows[0]["link"])
        self.assertTrue(rows[0]["requested"])
        self.assertEqual(2, rows[0]["tier"])

    def test_workbench_listing_rules(self):
        doc = tiny()
        doc["models"][0]["workbench"] = {"surviving_assignments": ["a1"], "contradicted_assignments": ["a2"]}
        errors = []
        CC._check_workbench(doc, {"a1": ["unknown", "contradicted"], "a2": ["contradicted"], "a3": ["unknown"]}, errors)
        self.assertEqual(["workbench assignment a3 has no model"], errors)
        errors = []
        CC._check_workbench(doc, {"a1": ["contradicted"], "a2": ["unknown"]}, errors)
        self.assertEqual(2, len(errors))


class RealChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = CC.load()
        cls.branches = CC.workbench_branches()
        cls.errors, cls.warnings = CC.validate(cls.doc, CC.RARITY_CSV, cls.branches)

    def test_real_chain_has_no_errors(self):
        self.assertEqual([], self.errors)

    def test_workbench_has_forty_combinations(self):
        self.assertEqual(40, sum(len(v) for v in self.branches.values()))

    def test_required_models_present(self):
        ids = {m["id"] for m in self.doc["models"]}
        for required in ("M-SULTAN", "M-MARJAMA", "M-QUMRAN", "M-SARTABA"):
            self.assertIn(required, ids)
        units = {m["rarity"]["unit"] for m in self.doc["models"] if m.get("rarity")}
        self.assertEqual(27, len(units))  # 26 two-of-three units plus Kh. el-Marjama

    def test_no_prediction_reuses_a_selection_relation(self):
        for m in self.doc["models"]:
            for link in m["next_links"]:
                self.assertFalse(set(link["relations"]) & set(m["selection_relations"]), link["id"])

    def test_sultan_depends_on_the_disputed_second_word(self):
        deps = CC.dependencies(self.doc)["M-SULTAN"]
        self.assertIn("D-E60-SECOND-WORD", deps["predictions"]["SULTAN-1-precamp-mouth"]["reading_dependencies"])

    def test_entry15_is_excluded_for_the_model_that_restored_it(self):
        sultan = next(m for m in self.doc["models"] if m["id"] == "M-SULTAN")
        self.assertIn("R-E15-CISTERN-PILLAR-N", {x["relation"] for x in sultan["excluded_links"]})
        self.assertNotIn("R-E15-CISTERN-PILLAR-N", {r for l in sultan["next_links"] for r in l["relations"]})

    def test_ranking_file_is_current(self):
        self.assertEqual(CC.ranking_markdown(self.doc), (HERE / "next_links.md").read_text(encoding="utf-8"))

    def test_mutating_real_chain_is_caught(self):
        doc = copy.deepcopy(self.doc)
        sultan = next(m for m in doc["models"] if m["id"] == "M-SULTAN")
        sultan["next_links"][0]["relations"].append("R-E11-POOL-EAST")
        errors, _ = CC.validate(doc)
        self.assertTrue(any("R-E11-POOL-EAST, which selected the model" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
