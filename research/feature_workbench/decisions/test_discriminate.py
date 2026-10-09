"""Check the logical discrimination search: collapsing, worst case, inconclusive outcomes, determinism."""

import copy
import importlib.util
import itertools
import json
from pathlib import Path
import random
import unittest


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


disc = _load("decision_discriminate", HERE / "discriminate.py")
evaluator = _load("decision_evaluator_for_discrimination", HERE / "evaluate.py")
PLANS = json.loads((HERE / "plans.json").read_text())
SPEC = json.loads((HERE / "discrimination.json").read_text())


def fs(*items):
    return frozenset(items)


class GenericLogicTests(unittest.TestCase):
    """Synthetic families with known answers."""

    def test_identical_predictions_collapse_and_input_order_is_irrelevant(self):
        survivors = {
            "t1": {"hit": fs("a", "b"), "inconclusive": fs("a", "b", "c", "d")},
            "t2": {"hit": fs("a", "b", "c"), "inconclusive": fs("a", "b", "c", "d")},
        }
        self.assertEqual(disc.collapse(["d", "c", "b", "a"], survivors), [["a", "b"], ["c"], ["d"]])
        self.assertEqual(disc.collapse(["a", "b", "c", "d"], survivors), [["a", "b"], ["c"], ["d"]])

    def test_worst_case_needs_disjoint_outcomes_and_inconclusive_blocks_it(self):
        pred = {"x": {"t": fs("yes")}, "y": {"t": fs("no")}}
        self.assertEqual(disc.guaranteed_pairs(["x", "y"], pred, ["t"]), [("x", "y")])
        # An inconclusive outcome both classes survive removes the guarantee.
        pred = {"x": {"t": fs("yes", "inconclusive")}, "y": {"t": fs("no", "inconclusive")}}
        self.assertEqual(disc.guaranteed_pairs(["x", "y"], pred, ["t"]), [])
        self.assertEqual(disc.separated_pairs(["x", "y"], pred, ["t"]), [("x", "y")])
        # Counting only decisive outcomes restores it.
        self.assertEqual(disc.guaranteed_pairs(["x", "y"], pred, ["t"], {"t": fs("yes", "no")}), [("x", "y")])

    def test_one_sided_exclusion_never_guarantees_separation(self):
        # A compatible verdict leaves both branches; only the miss excludes one.
        pred = {"site_a": {"t": fs("compatible", "miss")}, "site_b": {"t": fs("compatible")}}
        self.assertEqual(disc.guaranteed_pairs(["site_a", "site_b"], pred, ["t"], {"t": fs("compatible", "miss")}), [])
        self.assertEqual(disc.separated_pairs(["site_a", "site_b"], pred, ["t"]), [("site_a", "site_b")])

    def test_minimal_sets_are_exact_and_minimal(self):
        def test(subset):
            return {"a", "b"} <= set(subset) or {"c"} <= set(subset) and "d" in subset
        found = disc.minimal_sets(["a", "b", "c", "d"], test)
        self.assertEqual(found, [("a", "b"), ("c", "d")])
        for subset in found:
            for smaller in itertools.combinations(subset, len(subset) - 1):
                self.assertFalse(test(smaller))
        self.assertEqual(disc.minimal_sets(["a"], lambda subset: False), [])

    def test_reachable_survivor_sets_cover_best_and_worst_case(self):
        reachable = disc.reachable_survivor_sets(["p", "q"], {"t": [fs("p", "q"), fs("p")]}, ["t"])
        self.assertEqual(reachable, {fs("p", "q"), fs("p")})


class RealQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = disc.analyse(REPO)
        cls.families = {family["id"]: family for family in cls.result["families"]}
        cls.table = {item["task_id"]: item for item in cls.result["observation_table"]}
        cls.search = cls.result["search"]["per_family"]

    def _class_of(self, family_id, predicate):
        hits = []
        for cls_ in self.families[family_id]["classes"]:
            members = cls_.get("members")
            if members is None:
                continue
            hits.extend(cls_["id"] for member in members if predicate(member))
        return hits

    def test_duplicated_parameter_choices_collapse(self):
        kohlit = self.families["kohlit"]
        member_class = {m: c["id"] for c in kohlit["classes"] for m in c["members"]}
        for model in member_class:
            if "-RB-M-" in model:
                self.assertEqual(member_class[model], member_class[model.replace("-RB-M-", "-RB-P-")],
                                 "Milik and Puech readings make identical predictions on every queued record")
        entry25 = self.families["entry25"]
        for cls_ in entry25["classes"]:
            for dimension in ("unit", "deposit", "direction"):
                self.assertIn(dimension, cls_["identical_on"], "No queued record separates cubit units, deposit positions or direction")
        self.assertLess(entry25["class_count"], entry25["surviving_models"])
        self.assertEqual(sum(c["member_count"] for c in kohlit["classes"]), kohlit["surviving_models"])

    def test_contradicted_models_stay_outside_the_classes(self):
        kohlit = self.families["kohlit"]
        excluded = {item["id"] for item in kohlit["excluded_models"]}
        members = {m for c in kohlit["classes"] for m in c["members"]}
        self.assertTrue(excluded)
        self.assertFalse(excluded & members)
        for item in kohlit["excluded_models"]:
            self.assertTrue(item["contradicted_predicates"])

    def test_distinct_classes_have_distinct_predictions(self):
        for fid, per in self.search.items():
            self.assertEqual(per["class_pairs_no_record_separates"], [], fid)

    def test_no_worst_case_guarantee_with_inconclusive_outcomes(self):
        self.assertTrue(self.result["search"]["every_record_has_an_outcome_leaving_every_class"])
        for fid, per in self.search.items():
            self.assertEqual(per["worst_case_all_outcomes"]["guaranteed_pairs_with_all_records"], 0, fid)
            if per["class_pair_count"]:
                self.assertEqual(per["worst_case_all_outcomes"]["minimal_sets"], [], fid)

    def test_decisive_reading_alone_guarantees_string_separation(self):
        self.assertEqual(self.search["xii10"]["worst_case_decisive_outcomes"]["minimal_sets"], [["decisions-xii10"]])
        self.assertEqual(self.search["xii10"]["worst_case_decisive_outcomes"]["guaranteed_pairs_with_all_records"],
                         self.search["xii10"]["class_pair_count"])
        # Archaeological records only exclude; even decisive outcomes guarantee nothing.
        for fid in ("kohlit", "entry25"):
            self.assertEqual(self.search[fid]["worst_case_decisive_outcomes"]["guaranteed_pairs_with_all_records"], 0)

    def test_every_record_keeps_inconclusive_and_not_obtained_outcomes(self):
        for task in PLANS["tasks"]:
            rows = self.table[task["id"]]["outcomes"]
            self.assertEqual({row["plans_outcome_id"] for row in rows}, {o["id"] for o in task["outcomes"]})
            self.assertTrue(any(row["every_class_survives"] for row in rows), task["id"])
            for row in rows:
                if row["row_kind"] == "not_obtained":
                    self.assertTrue(row["every_class_survives"], row["id"])
                if row["basis"] == "derived":
                    self.assertTrue(row["derivation_ids"])
                    self.assertTrue(all(d in self.result["derivations"] for d in row["derivation_ids"]))

    def test_janoah_branch_depends_only_on_rejecting_r4(self):
        l_classes = {c["id"] for c in self.families["kohlit"]["classes"] if c["identical_on"].get("reading") is None and "RB-L" in c["label"]}
        self.assertTrue(l_classes)
        r4_class = next(c["id"] for c in self.families["xii10"]["classes"] if c["members"] == ["R4"])
        for row in self.table["decisions-xii10"]["outcomes"]:
            strings_alive = set(row["surviving_classes"].get("xii10", []))
            r4_alive = r4_class in strings_alive
            excluded = set(row["excluded_classes"].get("kohlit", []))
            self.assertEqual(excluded, set() if r4_alive else l_classes, row["id"])

    def test_records_without_alternatives_separate_nothing(self):
        for task_id in ("decisions-jericho-contacts", "decisions-siloam-main-side", "decisions-wadi-bath-contact"):
            item = next(r for r in self.result["queue_rank"] if r["task_id"] == task_id)
            self.assertEqual(item["rank_key"]["all_separated_pairs"], 0)
        self.assertEqual(self.table["decisions-iv17-l656"]["families_affected"], ["entry25"])

    def test_minimal_sets_are_minimal_on_real_data(self):
        # Independent check: a record set separates every class pair in principle
        # exactly when it hits each pair's list of separating records.
        records = self.result["search"]["records"]
        for fid, per in self.search.items():
            pairs = [set(p["separating_records"]) for p in per["class_pairs"]]
            def hits(subset):
                return all(pair & set(subset) for pair in pairs)
            found = [tuple(s) for s in per["in_principle"]["minimal_sets"]]
            size = len(found[0])
            expected = [s for s in itertools.combinations(records, size) if hits(s)]
            self.assertEqual(sorted(found), sorted(expected), fid)
            self.assertFalse(any(hits(s) for k in range(size) for s in itertools.combinations(records, k)), fid)
            for subset in found:
                self.assertTrue(set(per["in_principle"]["necessary_records"]) <= set(subset))
        self.assertIn("decisions-xii10", self.search["kohlit"]["in_principle"]["necessary_records"])
        for subset in self.result["search"]["minimal_in_principle_sets_all_families"]:
            for fid in self.result["search"]["families_with_alternatives"]:
                self.assertTrue(set(self.search[fid]["in_principle"]["necessary_records"]) <= set(subset))

    def test_threshold_and_supplementary_questions_exclude_nothing(self):
        for item in self.result["question_summary"]:
            if item["question_type"] == "ancient_threshold" or not item["in_queue"]:
                self.assertEqual(item["can_exclude"], {}, item["task_id"])
        bearing = [i for i in self.result["question_summary"] if i["question_type"] == "entrance_bearing" and i["in_queue"]]
        self.assertEqual([i["task_id"] for i in bearing], ["decisions-iv17-l656"])

    def test_rank_is_computed_from_the_stated_key(self):
        ranks = self.result["queue_rank"]
        keys = [tuple(item["rank_key"].values()) for item in ranks]
        self.assertEqual(keys, sorted(keys, reverse=True))
        for a, b in zip(ranks, ranks[1:]):
            self.assertEqual(a["rank"] == b["rank"], tuple(a["rank_key"].values()) == tuple(b["rank_key"].values()))


class DeterminismAndLimitsTests(unittest.TestCase):
    def test_output_is_deterministic_and_independent_of_task_order(self):
        first = json.dumps(disc.analyse(REPO), ensure_ascii=False, sort_keys=True)
        self.assertEqual(first, json.dumps(disc.analyse(REPO), ensure_ascii=False, sort_keys=True))
        shuffled = copy.deepcopy(PLANS)
        random.Random(7).shuffle(shuffled["tasks"])
        spec = copy.deepcopy(SPEC)
        random.Random(11).shuffle(spec["observations"])
        self.assertEqual(first, json.dumps(disc.analyse(REPO, shuffled, spec), ensure_ascii=False, sort_keys=True))

    def test_no_numbers_beyond_counts(self):
        def walk(value, path="data"):
            self.assertNotIsInstance(value, float, path)
            if isinstance(value, dict):
                for key, item in value.items():
                    for word in ("probab", "likelihood", "entropy", "information_gain", "expected_value", "confidence", "score"):
                        self.assertNotIn(word, key.lower(), path + "." + key)
                    walk(item, path + "." + key)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    walk(item, f"{path}[{index}]")
        walk(disc.analyse(REPO))

    def test_stale_effect_reference_fails(self):
        spec = copy.deepcopy(SPEC)
        kallai = next(o for o in spec["observations"] if o["task_id"] == "decisions-kallai-pool")
        kallai["components"][0]["values"][1]["effects"][0]["subject"] = "invented-pool"
        with self.assertRaisesRegex(ValueError, "matches no model check"):
            disc.analyse(REPO, copy.deepcopy(PLANS), spec)

    def test_every_task_needs_one_observation_and_complete_mapping(self):
        spec = copy.deepcopy(SPEC)
        spec["observations"] = [o for o in spec["observations"] if o["task_id"] != "decisions-wadi-bath-contact"]
        with self.assertRaisesRegex(ValueError, "exactly one discrimination observation"):
            disc.analyse(REPO, copy.deepcopy(PLANS), spec)
        spec = copy.deepcopy(SPEC)
        kallai = next(o for o in spec["observations"] if o["task_id"] == "decisions-kallai-pool")
        kallai["rules"] = [rule for rule in kallai["rules"] if rule["plans_outcome_id"] != "identity-only"] + [{"when": {}, "plans_outcome_id": "east-period"}]
        with self.assertRaisesRegex(ValueError, "map onto exactly"):
            disc.analyse(REPO, copy.deepcopy(PLANS), spec)

    def test_build_includes_discrimination_without_changing_task_evidence(self):
        snapshot = evaluator.build(REPO)
        self.assertIn("discrimination", snapshot["data"])
        self.assertEqual(snapshot["data"]["discrimination"]["mode"], "planning_only")
        self.assertEqual(snapshot["data"]["tasks"], PLANS["tasks"])
        self.assertTrue(all(result["status"] == "unknown" for result in snapshot["results"]))
        source_ids = [source["id"] for source in snapshot["sources"]]
        self.assertEqual(len(source_ids), len(set(source_ids)))
        self.assertTrue(all(source_id.startswith("decisions-") for source_id in source_ids))


if __name__ == "__main__":
    unittest.main()
