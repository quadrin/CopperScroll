"""Unit tests for the recovery procedure's predicates and decision rule.

Run: python3 -I -m unittest discover -s research/benchmarks/recovery/tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import procedure as P  # noqa: E402


def cand(cid, type_="cistern", bearing=None, distance=None, rel="site_centre", direction=None,
         opening=None, date="U", kind=None, precision=None):
    pos = {"bearing_deg": bearing, "distance_m": distance, "relative_to": rel}
    if direction is not None:
        pos["direction"] = direction
    if kind:
        pos["kind"] = kind
    if precision:
        pos["precision_m"] = precision
    return {"id": cid, "features": {"type": type_, "position": pos, "opening": opening, "date": date}}


def case(instruction, cands, q="Which side of the chosen feature has its entrance?",
         opts=("north", "east", "south", "west", "unknown")):
    return {"case_id": "t-001", "instruction": instruction, "candidates": cands,
            "withheld_question": q, "withheld_options": list(opts)}


class Parsing(unittest.TestCase):
    def test_numbers_and_cubits(self):
        c = P.parse_instruction("In the tomb west of the wall, at one hundred and twenty cubits.")
        self.assertEqual(c["distance"]["min_m"], 48.0)
        self.assertEqual(c["distance"]["max_m"], 72.0)
        self.assertEqual(c["distance"]["kind"], "band")
        self.assertEqual(P.words_to_number(["twelve", "hundred"]), 1200)

    def test_within_is_a_limit(self):
        c = P.parse_instruction("In the cistern on the north side, within 40 cubits.")
        self.assertEqual((c["distance"]["min_m"], c["distance"]["max_m"], c["distance"]["kind"]), (0.0, 24.0, "limit"))

    def test_metres_use_benchmark_tolerance(self):
        c = P.parse_instruction("In the pool north of the gate, about 35 m.")
        self.assertEqual((c["distance"]["min_m"], c["distance"]["max_m"]), (31.5, 38.5))

    def test_opening_kept_apart_from_position(self):
        c = P.parse_instruction("In the cave in the west of the field, whose mouth opens to the south.")
        self.assertEqual((c["direction"], c["opening"], c["reference"]), ("W", "S", "the field"))

    def test_type_is_the_first_feature_not_the_reference(self):
        c = P.parse_instruction("In the great cave south of the cave in the quarry, at twenty cubits.")
        self.assertEqual(c["target_class"], "cave")
        c = P.parse_instruction("In the watchtower of the farm, at twelve hundred cubits.")
        self.assertEqual((c["target_class"], c["direction"], c["reference"]), ("tower", None, "the farm"))

    def test_depth_is_not_a_distance(self):
        c = P.parse_instruction("In the cistern north of the gate, at forty cubits; dig three cubits.")
        self.assertEqual(c["distance"]["stated"], "40 cubits")
        self.assertIsNone(P.parse_instruction("In the cave, dig three cubits.")["distance"])

    def test_compound_direction(self):
        self.assertEqual(P.parse_instruction("In the pool north-east of the gate.")["direction"], "NE")


class Predicates(unittest.TestCase):
    def c(self, text):
        return P.parse_instruction(text)

    def test_quadrant_rule_for_words(self):
        con = self.c("In the cistern north of the ruin.")
        self.assertIsNone(P.pred_direction(cand("a", direction="NE", rel="ruin")["features"], con)[0])
        self.assertIsNone(P.pred_direction(cand("a", direction="southwest", rel="ruin")["features"], con)[0])
        self.assertTrue(P.pred_direction(cand("a", direction="NNE", rel="ruin")["features"], con)[0])
        self.assertFalse(P.pred_direction(cand("a", direction="south", rel="ruin")["features"], con)[0])

    def test_numeric_sector_edges_are_inclusive(self):
        con = self.c("In the cistern north of the ruin.")
        self.assertTrue(P.pred_direction(cand("a", bearing=45, distance=50, rel="ruin")["features"], con)[0])
        self.assertFalse(P.pred_direction(cand("a", bearing=45.5, distance=50, rel="ruin")["features"], con)[0])

    def test_bearing_needs_three_times_precision(self):
        con = self.c("In the cistern north of the ruin.")
        f = cand("a", bearing=10, distance=20, rel="ruin", precision=10)["features"]
        self.assertIsNone(P.pred_direction(f, con)[0])

    def test_words_without_distance_within_limit(self):
        con = self.c("In the cistern north of the ruin.")
        self.assertTrue(P.pred_distance(cand("a", direction="N", rel="ruin")["features"], con)[0])
        con = self.c("In the cistern north of the ruin, at forty cubits.")
        self.assertIsNone(P.pred_distance(cand("a", direction="N", rel="ruin")["features"], con)[0])

    def test_plan_without_distance_is_unknown(self):
        con = self.c("In the cistern north of the ruin, at forty cubits.")
        self.assertIsNone(P.pred_distance(cand("a", bearing=0, rel="ruin")["features"], con)[0])

    def test_other_reference_is_unknown(self):
        con = self.c("In the cave in the west of the field.")
        self.assertIsNone(P.pred_direction(cand("a", direction="W", rel="cave_3")["features"], con)[0])
        self.assertTrue(P.pred_direction(cand("a", direction="W", rel="survey_area")["features"], con)[0])

    def test_dates(self):
        con = self.c("In the cistern.")
        self.assertTrue(P.pred_date(cand("a", date="D")["features"], con)[0])
        self.assertTrue(P.pred_date(cand("a", date="U")["features"], con)[0])
        self.assertFalse(P.pred_date(cand("a", date="L")["features"], con)[0])

    def test_types(self):
        con = self.c("In the tomb west of the wall.")
        self.assertTrue(P.pred_type(cand("a", type_="burial cave with rock-hewn courtyard")["features"], con)[0])
        self.assertFalse(P.pred_type(cand("a", type_="large cave")["features"], con)[0])
        con = self.c("In the watchtower of the farm.")
        self.assertIsNone(P.pred_type(cand("a", type_="structure, probably a field watchtower")["features"], con)[0])
        con = self.c("In the cistern of the farm.")
        self.assertIsNone(P.pred_type(cand("a", type_="reservoir")["features"], con)[0])

    def test_opening_edge_word_is_unknown(self):
        con = self.c("In the cave, its entrance is on the north.")
        self.assertIsNone(P.pred_opening(cand("a", opening="north-east")["features"], con)[0])
        self.assertTrue(P.pred_opening(cand("a", opening="north")["features"], con)[0])


class Decision(unittest.TestCase):
    INS = "In the cistern north of the ruin, at one hundred cubits."

    def test_single_supported_survivor_is_selected(self):
        out = P.run_case(case(self.INS, [cand("c1", bearing=10, distance=50, rel="ruin", opening="west"),
                                        cand("c2", bearing=180, distance=50, rel="ruin")]))
        self.assertEqual((out["selected"], out["withheld_prediction"]), ("c1", "west"))

    def test_unknown_survivor_gives_insufficient(self):
        out = P.run_case(case(self.INS, [cand("c1", direction="NE", distance=50, rel="ruin"),
                                        cand("c2", bearing=180, distance=50, rel="ruin")]))
        self.assertEqual(out["selected"], "insufficient_evidence")

    def test_unknown_is_never_absence(self):
        # c2 has no position at all: it is not eliminated, so the output cannot be c1.
        out = P.run_case(case(self.INS, [cand("c1", bearing=10, distance=50, rel="ruin"),
                                        cand("c2", rel="ruin")]))
        self.assertEqual(out["selected"], "insufficient_evidence")

    def test_two_survivors_give_insufficient(self):
        out = P.run_case(case(self.INS, [cand("c1", bearing=10, distance=50, rel="ruin"),
                                        cand("c2", bearing=350, distance=45, rel="ruin")]))
        self.assertEqual(out["selected"], "insufficient_evidence")

    def test_all_contradicted_gives_none(self):
        out = P.run_case(case(self.INS, [cand("c1", bearing=10, distance=50, rel="ruin", date="L"),
                                        cand("c2", bearing=180, distance=50, rel="ruin")]))
        self.assertEqual((out["selected"], out["withheld_prediction"]), ("none", "unknown"))

    def test_withheld_from_instruction_even_when_abstaining(self):
        ins = "In the cistern north of the ruin; its opening faces west."
        out = P.run_case(case(ins, [cand("c1", bearing=10, distance=50, rel="ruin"),
                                   cand("c2", bearing=350, distance=45, rel="ruin")]))
        self.assertEqual((out["selected"], out["withheld_prediction"]), ("insufficient_evidence", "west"))

    def test_withheld_option_mapping(self):
        self.assertEqual(P.map_to_option("north-east", ["north", "east", "south", "west", "unknown"]), "unknown")
        self.assertEqual(P.map_to_option("northeast", ["north", "north-east", "east", "unknown"]), "north-east")
        self.assertEqual(P.map_to_option(80.3, ["north", "east", "south", "west", "unknown"]), "east")
        self.assertEqual(P.map_to_option(45.0, ["north", "east", "south", "west", "unknown"]), "unknown")


if __name__ == "__main__":
    unittest.main()
