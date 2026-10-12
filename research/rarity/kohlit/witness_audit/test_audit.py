import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("witness_audit", HERE / "audit.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)


class WitnessAuditTests(unittest.TestCase):
    def test_missing_grid_remains_unknown(self):
        f = {"position": {"kind": "grid", "ref": "S999"}}
        c = {"sectors_deg": {"C2_north": [315,45]}, "limits_m": {"C2": 1000}}
        self.assertIsNone(A.position_truth("S1", f, "C2", {"S1": (100,100)}, c))

    def test_north_reference_does_not_transfer(self):
        f = {"position": {"kind":"words", "direction":"N", "relative_to":"other"}}
        c = {"sectors_deg": {"C2_north": [315,45]}, "limits_m": {"C2":1000}}
        self.assertIsNone(A.position_truth("S1", f, "C2", {}, c))

    def test_same_condition_status_different_features(self):
        a = [{"documented_claim_id":"pool"}, {"documented_claim_id":"cave-cistern"}]
        b = [{"documented_claim_id":"pool"}, {"documented_claim_id":"robbing-pit"}]
        self.assertEqual(A.identity_agreement(a,b),["pool"])

    def test_two_distinct_pits_on_one_page_never_establish_identity(self):
        a = [{"documented_claim_id":None,"citation_class_key":"same-page|pit|cistern-group",
              "feature_id":"north-pit"}]
        b = [{"documented_claim_id":None,"citation_class_key":"same-page|pit|cistern-group",
              "feature_id":"south-pit"}]
        self.assertEqual(A.citation_compatibility(a,b),["same-page|pit|cistern-group"])
        self.assertEqual(A.identity_agreement(a,b),[])

    def test_unmatched_feature_has_no_documentary_identity(self):
        f = {"id":"f999","_coder":"A","source":"3","cite":"Mem II p.398",
             "type":"pit","subtype":"cistern"}
        self.assertIsNone(A.claim_key("S1283",f))

    def test_text_grave_must_attach_to_selected_pit(self):
        def w(fid,c,claim,mouth=None):
            return {"feature_id":fid,"condition":c,"documented_claim_id":claim,
                    "date_code":"U","mouth":mouth}
        ws = [w("p","C1","pool"),w("a","C2","pit-a"),w("b","C2","pit-b"),
              w("g","C3t","grave",{"pit_id":"b"})]
        choices = A.assignment_sets(ws,("C1","C2","C3t"))
        self.assertEqual(len(choices),1)
        self.assertEqual(choices[0]["condition_features"]["C2"],"b")
        self.assertEqual(choices[0]["contemporaneity"],"UNKNOWN")

    def test_append_preserves_and_renames_mouth(self):
        base = {"unit_id":"S1","sources":{"2":"not accessed"},"features":[],"explicit_absence":[]}
        add = {"features":[{"id":"a"},{"id":"b","mouth":{"pit_id":"a"}}]}
        merged = A.merge(base,add,"2","s2z_")
        self.assertEqual(merged["features"][1]["mouth"]["pit_id"],"s2z_a")
        self.assertEqual(base["features"],[])

    def test_sartaba_expected_curated_group_pairings(self):
        f = {"id":"f11","_coder":"A"}
        self.assertEqual(A.claim_key("S1283",f),"S1283:SWP-cemented-cave-cisterns")
        f = {"id":"f14","_coder":"B"}
        self.assertEqual(A.claim_key("S1283",f),"S1283:northern-robbing-pits")

    def test_real_snapshot_keeps_sartaba_assignment_disagreement(self):
        with tempfile.TemporaryDirectory(dir=HERE) as d:
            summary = A.run(Path(d))
            self.assertEqual(summary["positive_condition_records"],120)
            self.assertEqual(summary["unrecoverable_B_matches"],17)
            windows = summary["frozen_primary_branch_matches_by_window"]
            self.assertEqual(len(windows['R1_main_Hel_Rom']['B']),5)
            self.assertEqual(len(windows['R1_pre70']['B']),6)
            self.assertNotIn('E357',windows['R1_main_Hel_Rom']['B'])
            self.assertIn('E357',windows['R1_pre70']['B'])
            result = json.loads((Path(d)/"assignments.json").read_text())
            sartaba = next(x for x in result if x['unit_id']=='S1283')['branches']['B']
            self.assertEqual(sartaba['frozen_result'],'MATCH')
            self.assertEqual(len(sartaba['assignments']['A']),1)
            self.assertEqual(len(sartaba['assignments']['B']),1)
            self.assertEqual(sartaba['shared_documented_assignments'],[])
            self.assertEqual(sartaba['joint_phase'],'UNKNOWN')


if __name__ == "__main__":
    unittest.main()
