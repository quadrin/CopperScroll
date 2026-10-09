"""Adversarial invariants and checks against the actual pinned model/protocol."""
from copy import deepcopy
import itertools
import json
from pathlib import Path
import unittest

from planner import (REPO_ROOT, analyze, build_inputs, collapse_hypotheses,
                     dependency_closure, outcome_set, separating_pairs, survivors)


def domain(hypotheses, observations):
    return {"hypotheses": hypotheses, "observations": observations}


class SetLogicTests(unittest.TestCase):
    def setUp(self):
        self.observation = {"id": "O", "outcomes": ["a", "b", "c"], "dependencies": []}

    def test_unknown_never_separates(self):
        d = domain([{"id":"A", "predictions":{"O":["a"]}},
                    {"id":"B", "predictions":{"O":None}}], [self.observation])
        classes = collapse_hypotheses(d["hypotheses"], d["observations"])
        self.assertFalse(separating_pairs(classes, self.observation))
        self.assertEqual(survivors(d,"O","b"), ["B"])
        self.assertEqual(survivors(d,"O","unresolved"), ["A","B"])

    def test_overlapping_sets_do_not_separate(self):
        d=domain([{"id":"A","predictions":{"O":["a","b"]}},
                  {"id":"B","predictions":{"O":["b","c"]}}],[self.observation])
        classes=collapse_hypotheses(d["hypotheses"],d["observations"])
        self.assertFalse(separating_pairs(classes,self.observation))
        self.assertEqual(survivors(d,"O","b"),["A","B"])
        self.assertEqual(survivors(d,"O",["a","b"]),["A","B"])

    def test_disjoint_sets_separate(self):
        classes=collapse_hypotheses([
            {"id":"A","predictions":{"O":["a"]}},
            {"id":"B","predictions":{"O":["b","c"]}},
        ],[self.observation])
        self.assertEqual(len(separating_pairs(classes,self.observation)),1)

    def test_identical_observable_signatures_collapse(self):
        classes=collapse_hypotheses([
            {"id":"A","predictions":{"O":["b","a"]}},
            {"id":"B","predictions":{"O":["a","b"]}},
        ],[self.observation])
        self.assertEqual(len(classes),1)
        self.assertEqual(len(classes[0]["families"]),2)

    def test_nuisance_duplication_cannot_inflate_pairs(self):
        hypotheses=[{"id":"A1","family_id":"A","predictions":{"O":["a"]}},
                    {"id":"B1","family_id":"B","predictions":{"O":["b"]}}]
        initial=analyze(domain(hypotheses,[self.observation]),[],"available_now")
        copies=[dict(hypotheses[0],id=f"A{i}") for i in range(2,20)]
        duplicated=analyze(domain(hypotheses+copies,[self.observation]),[],"available_now")
        self.assertEqual(initial["attainable_pairs"],duplicated["attainable_pairs"])
        self.assertEqual(initial["class_pair_count"],duplicated["class_pair_count"])

    def test_alternative_nuisance_branch_preserves_best_fit(self):
        hypotheses=[{"id":"A1","family_id":"A","predictions":{"O":["a"]}},
                    {"id":"A2","family_id":"A","predictions":{"O":["b"]}},
                    {"id":"B1","family_id":"B","predictions":{"O":["b"]}}]
        result=analyze(domain(hypotheses,[self.observation]),[],"available_now")
        self.assertEqual(result["attainable_pair_count"],0)

    def test_unknown_branch_broadens_family(self):
        hypotheses=[{"id":"A1","family_id":"A","predictions":{"O":["a"]}},
                    {"id":"A2","family_id":"A","predictions":{"O":None}}]
        result=collapse_hypotheses(hypotheses,[self.observation])
        self.assertEqual(result[0]["predictions"]["O"],["a","b","c"])

    def test_empty_or_invalid_prediction_rejected(self):
        for prediction in [[],["foreign"]]:
            with self.assertRaises(ValueError):
                outcome_set(prediction,["a","b"])

    def test_invalid_observed_outcome_rejected(self):
        d=domain([{"id":"A","predictions":{}}],[self.observation])
        for outcome in [[],"foreign"]:
            with self.assertRaises(ValueError):
                survivors(d,"O",outcome)

    def test_gate_failure_never_appears_as_model_category(self):
        d=domain([{"id":"A","predictions":{"O":["a"]}},
                  {"id":"B","predictions":{"O":["b"]}}],[self.observation])
        self.assertEqual(survivors(d,"O",["unresolved","a"]),["A","B"])

    def test_dependencies_block_now_and_unscoped_named(self):
        obs=dict(self.observation,dependencies=["G"])
        deps=[{"id":"F","kind":"acquisition","status":"pending","requires":[]},
              {"id":"G","kind":"gate","status":"future_gate","requires":["F"]}]
        d=domain([{"id":"A","predictions":{"O":["a"]}},
                  {"id":"B","predictions":{"O":["b"]}}],[obs])
        self.assertEqual(analyze(d,deps,"available_now")["attainable_pair_count"],0)
        self.assertEqual(analyze(d,deps,"named_dependencies")["attainable_pair_count"],1)
        deps[0]["status"]="unscoped"
        self.assertEqual(analyze(d,deps,"named_dependencies")["attainable_pair_count"],0)
        self.assertEqual(analyze(d,deps,"all_planning")["attainable_pair_count"],1)

    def test_dependency_errors_fail_closed(self):
        with self.assertRaises(ValueError):
            dependency_closure(["missing"],[])
        with self.assertRaises(ValueError):
            dependency_closure(["A"],[{"id":"A","requires":["B"]},{"id":"B","requires":["A"]}])

    def test_all_tied_minimum_covers_retained_and_shared_acquisition_counted_once(self):
        observations=[{"id":i,"outcomes":["a","b"],"dependencies":["F"]} for i in ["O1","O2"]]
        d=domain([{"id":"A","predictions":{"O1":["a"],"O2":["a"]}},
                  {"id":"B","predictions":{"O1":["b"],"O2":["b"]}}],observations)
        deps=[{"id":"F","status":"pending","kind":"acquisition","requires":[]}]
        minima=analyze(d,deps,"named_dependencies")["minimum_sets_for_all_attainable_pairs"]
        self.assertEqual(len(minima),2)
        self.assertTrue(all(m["acquisition_ids"]==["F"] for m in minima))

    def test_joint_correlations_are_retained_across_nuisance_branches(self):
        observations=[{"id":i,"outcomes":["a","b"],"dependencies":[]} for i in ["O1","O2"]]
        # Both families permit a/b for both marginal observations. Their ordered
        # joint outcomes differ: same/same versus different/different.
        hypotheses=[{"id":"A1","family_id":"A","predictions":{"O1":["a"],"O2":["a"]}},
                    {"id":"A2","family_id":"A","predictions":{"O1":["b"],"O2":["b"]}},
                    {"id":"B1","family_id":"B","predictions":{"O1":["a"],"O2":["b"]}},
                    {"id":"B2","family_id":"B","predictions":{"O1":["b"],"O2":["a"]}}]
        result=analyze(domain(hypotheses,observations),[],"available_now")
        self.assertEqual(result["class_count"],2)
        self.assertEqual(result["attainable_pair_count"],1)
        self.assertTrue(all(r["separated_pair_count"]==0 for r in result["capability_order"]))
        self.assertEqual(result["minimum_sets_for_all_attainable_pairs"][0]["observations"],["O1","O2"])

    def test_logically_redundant_nuisance_branches_do_not_change_equivalence(self):
        hypotheses=[{"id":"A1","family_id":"A","predictions":{"O":None}},
                    {"id":"A2","family_id":"A","predictions":{"O":["a"]}},
                    {"id":"B1","family_id":"B","predictions":{"O":None}}]
        classes=collapse_hypotheses(hypotheses,[self.observation])
        self.assertEqual(len(classes),1)


class RealDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=build_inputs(REPO_ROOT)
        cls.letters,cls.relationships=cls.inputs["domains"]
        cls.dependencies=cls.inputs["dependencies"]

    def test_three_components_needed_for_seven_registered_strings(self):
        result=analyze(self.letters,self.dependencies,"named_dependencies")
        self.assertEqual(result["class_count"],7)
        self.assertEqual(result["attainable_pair_count"],21)
        self.assertTrue(result["perfect_separation_conditional_on_decisive_results"])
        minima=result["minimum_sets_for_all_attainable_pairs"]
        self.assertEqual(len(minima),1)
        self.assertEqual(set(minima[0]["observations"]),{"xii10-box","xii10-medial","xii10-tail"})
        self.assertEqual(minima[0]["acquisition_ids"],["xii10-native"])
        counts={r["observation_id"]:r["separated_pair_count"] for r in result["capability_order"]}
        self.assertEqual(counts,{"xii10-box":12,"xii10-medial":18,"xii10-tail":14})

    def test_two_components_always_leave_a_registered_pair(self):
        classes=collapse_hypotheses(self.letters["hypotheses"],self.letters["observations"])
        for observations in itertools.combinations(self.letters["observations"],2):
            separated=set().union(*(separating_pairs(classes,o) for o in observations))
            self.assertLess(len(separated),21)

    def test_reading_preview_preserves_ambiguity_and_rejects_finite_set_for_other(self):
        self.assertEqual(survivors(self.letters,"xii10-medial","ינ"),["R4","R5"])
        self.assertEqual(survivors(self.letters,"xii10-medial",["נ","ינ"]),["R1","R2","R4","R5"])
        self.assertEqual(survivors(self.letters,"xii10-tail","other"),[])
        self.assertEqual(len(survivors(self.letters,"xii10-tail","unresolved")),7)

    def test_existing_contradictions_are_limited_to_named_assignments(self):
        excluded=self.relationships["excluded_by_existing_evidence"]
        self.assertEqual(len(excluded),12)
        self.assertEqual({b["assignment_id"] for b in excluded},{"jericho-modern-ns1","samiya-crypt"})
        self.assertEqual(len(self.relationships["hypotheses"]),28)
        self.assertEqual(len({h["family_id"] for h in self.relationships["hypotheses"]}),14)

    def test_archaeology_never_predicts_absence_at_alternative_site(self):
        for h in self.relationships["hypotheses"]:
            if h["assignment_id"].startswith("jericho-"):
                self.assertIsNone(h["predictions"]["kallai-pool-east"])
        result=analyze(self.relationships,self.dependencies,"all_planning")
        self.assertEqual(result["class_count"],5)
        self.assertEqual(result["attainable_pair_count"],0)
        self.assertFalse(result["perfect_separation_conditional_on_decisive_results"])

    def test_extended_window_is_not_lost_after_early_failure(self):
        selected=survivors(self.relationships,"historical-basin-window","extended-only")
        subset=[h for h in self.relationships["hypotheses"]
                if h["id"] in selected and h["assignment_id"]=="jericho-historical-ns1"]
        self.assertEqual({h["window_id"] for h in subset},{"extended"})
        self.assertEqual(len(subset),3)

    def test_buried_reading_does_not_require_tombs(self):
        selected=survivors(self.relationships,"quarry-graves-at-mouth","contradicted")
        quarry=[h for h in self.relationships["hypotheses"]
                if h["id"] in selected and h["assignment_id"]=="jericho-quarry"]
        self.assertEqual({h["reading_id"] for h in quarry},{"RB-B"})

    def test_available_now_is_not_promoted_by_pending_routes(self):
        for d in [self.letters,self.relationships]:
            r=analyze(d,self.dependencies,"available_now")
            self.assertEqual(r["attainable_pair_count"],0)
            self.assertEqual(r["capability_order"],[])

    def test_all_queue_outcomes_and_source_pointers_preserved(self):
        self.assertEqual(len(self.inputs["imported_queue"]),7)
        self.assertTrue(all(not o["recorded"] for task in self.inputs["imported_queue"] for o in task["outcomes"]))
        self.assertTrue(all((REPO_ROOT / source["repo_path"]).is_file() for source in self.inputs["input_sources"]))
        for d in self.inputs["domains"]:
            self.assertTrue(all(o["source_ids"] for o in d["observations"]))


if __name__=="__main__":
    unittest.main()
