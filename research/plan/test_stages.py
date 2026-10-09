"""Checks for the staged-objectives plan (research/plan).

Run from the repository root:
    python3 -I -m unittest discover -s research/plan -t research/plan
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
STAGES = HERE / "stages.json"
SCALE = HERE / "rating_scale.json"
PLAN_MD = HERE / "STAGED_OBJECTIVES.md"
OPEN_QUESTIONS = REPO / "research" / "OPEN_QUESTIONS.md"
ACTIVE_TEST = REPO / "research" / "ACTIVE_TEST.md"
LEDGER = REPO / "research" / "progress" / "outcome_ledger.json"
METHODS_LOG = REPO / "research" / "logs" / "methods_round_2026-10-08.md"

# The seven tools of the 9 October round (COMMON_BRIEF_R2, outside the repository).
NEW_TOOL_FOLDERS = {
    "research/models/search_effectiveness/",
    "research/text/edition_confusions/",
    "research/preregistration/arrivals/",
    "research/history/salvage_records/",
    "research/history/pef_qs_finds/",
    "research/comparanda/concealment_contexts/",
    "research/plan/",
}
MONEY_OK = re.compile(r"^(none|owner approval\b.*)$")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def r_numbers():
    text = OPEN_QUESTIONS.read_text(encoding="utf-8")
    return re.findall(r"^## (R\d\d) ", text, flags=re.M)


def active_questions():
    text = ACTIVE_TEST.read_text(encoding="utf-8")
    section = text.split("## Active questions", 1)[1].split("\n## ", 1)[0]
    return ["AQ" + n for n in re.findall(r"^(\d+)\. \*\*", section, flags=re.M)]


class PlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = load(STAGES)
        cls.scale = load(SCALE)
        cls.lanes = cls.plan["lanes"]
        cls.stage_ids = [s["id"] for s in cls.plan["stages"]]

    # Coverage of the backlog and the active test
    def test_sources_parse(self):
        self.assertEqual(r_numbers(), ["R%02d" % i for i in range(1, 13)])
        self.assertGreaterEqual(len(active_questions()), 1)

    def test_every_r_number_exactly_once(self):
        ids = [lane["id"] for lane in self.lanes]
        for r in r_numbers():
            self.assertEqual(ids.count(r), 1, r)
        extra = {i for i in ids if re.fullmatch(r"R\d\d", i)} - set(r_numbers())
        self.assertEqual(extra, set())

    def test_every_active_question_exactly_once(self):
        ids = [lane["id"] for lane in self.lanes]
        for aq in active_questions():
            self.assertEqual(ids.count(aq), 1, aq)
        extra = {i for i in ids if re.fullmatch(r"AQ\d+", i)} - set(active_questions())
        self.assertEqual(extra, set())

    def test_lane_ids_unique(self):
        ids = [lane["id"] for lane in self.lanes]
        self.assertEqual(len(ids), len(set(ids)))

    def test_methods_round_tools_covered(self):
        log = METHODS_LOG.read_text(encoding="utf-8")
        folders = set()
        for link in re.findall(r"\]\(\.\./([^)]+)\)", log.split("## Integration", 1)[0]):
            folder = link.rsplit("/", 1)[0] + "/" if link.endswith(".md") else link
            folders.add("research/" + folder)
        self.assertEqual(len(folders), 9)
        lane_folders = {lane.get("folder") for lane in self.lanes}
        self.assertEqual(folders - lane_folders, set())

    def test_new_tools_covered(self):
        lane_folders = [lane.get("folder") for lane in self.lanes]
        for folder in NEW_TOOL_FOLDERS:
            self.assertEqual(lane_folders.count(folder), 1, folder)

    def test_rarity_count_is_a_lane(self):
        self.assertEqual([l["id"] for l in self.lanes if l["kind"] == "registered result"], ["KOHLIT-RARITY"])

    # Ratings
    def test_scale_frozen(self):
        digest = hashlib.sha256(SCALE.read_bytes()).hexdigest()
        self.assertEqual(digest, self.plan["rating_scale_sha256"])
        self.assertIn(digest, (HERE / "README.md").read_text(encoding="utf-8"))

    def test_ratings_use_scale(self):
        allowed = set(self.scale["scale"])
        self.assertEqual(allowed, set(self.scale["order"]))
        for stage in self.plan["stages"]:
            self.assertIn(stage["rating"], allowed, stage["id"])
            self.assertTrue(stage["rating_evidence"], stage["id"])

    def test_ladder_never_rises(self):
        order = self.scale["order"]
        stages = sorted(self.plan["stages"], key=lambda s: s["order"])
        ranks = [order.index(s["rating"]) for s in stages]
        self.assertEqual(ranks, sorted(ranks))

    def test_reached_flags_follow_ledger(self):
        # S4 and S6 are defined by ledger counters, so their flags must agree with the ledger.
        counts = load(LEDGER)["outcome_counts"]
        reached = {s["id"]: s["reached"] for s in self.plan["stages"]}
        self.assertEqual(reached["S4"], counts["independently_discriminated_identifications"] > 0)
        deposit = (counts["confirmed_deposit_locations"] > 0
                   or counts["verified_negative_excavations_at_predicted_targets"] > 0)
        self.assertEqual(reached["S6"], deposit)
        for stage in self.plan["stages"]:
            self.assertIsInstance(stage["reached"], bool, stage["id"])

    # Lanes
    def test_lane_fields(self):
        for lane in self.lanes:
            with self.subTest(lane=lane["id"]):
                self.assertIn(lane["stage"], self.stage_ids)
                self.assertIn(lane["state_now"], self.plan["states"])
                for key in ("next_observation", "continue_if", "resume_on"):
                    self.assertTrue(lane[key].strip())
                cost = lane["cost"]
                for key in ("sessions", "outreach_messages", "library_items"):
                    self.assertIsInstance(cost[key], int)
                    self.assertGreaterEqual(cost[key], 0)
                self.assertRegex(cost["money"], MONEY_OK)

    def test_every_stop_rule_proposed(self):
        for lane in self.lanes:
            rule = lane["stop_rule"]
            self.assertEqual(rule["status"], "PROPOSED", lane["id"])
            self.assertTrue(rule["text"].startswith("PROPOSED: "), lane["id"])
        for rule in self.plan["rules"]:
            if rule["status"] != "EXISTING":
                self.assertEqual(rule["status"], "PROPOSED", rule["id"])
                self.assertTrue(rule["text"].startswith("PROPOSED"), rule["id"])

    def test_closed_tests_keep_their_criterion(self):
        ids = {lane["id"] for lane in self.lanes}
        self.assertEqual(len(self.plan["closed_tests"]), 6)
        for test in self.plan["closed_tests"]:
            self.assertEqual(test["result"], "not identifiable from available evidence")
            self.assertTrue(test["reopen_only_on"].strip())
            self.assertNotIn("stop_rule", test)
            self.assertTrue(set(test["related_lanes"]) <= ids, test["id"])
        existing = [r for r in self.plan["rules"] if r["status"] == "EXISTING"]
        self.assertEqual([r["id"] for r in existing], ["EXISTING-REOPEN"])

    def test_cited_files_exist(self):
        paths = set()
        for stage in self.plan["stages"]:
            paths.update(e["source"] for e in stage["rating_evidence"])
        for lane in self.lanes:
            paths.update(lane["sources"])
        for item in self.plan["closed_tests"] + self.plan["parked_elsewhere"]:
            paths.add(item["source"])
        for path in sorted(paths):
            self.assertTrue((REPO / path).is_file(), path)

    # Agreement with the ledger and the markdown page
    def test_counter_snapshot_matches_ledger(self):
        counts = load(LEDGER)["outcome_counts"]
        snap = self.plan["counters_at_writing"]
        for key, value in snap.items():
            if key != "source":
                self.assertEqual(counts[key], value, key)

    def test_markdown_lists_every_lane_and_stage(self):
        md = PLAN_MD.read_text(encoding="utf-8")
        rows = [line for line in md.splitlines() if line.startswith("| ")]
        for lane in self.lanes:
            mine = [r for r in rows if r.startswith("| %s |" % lane["id"])]
            self.assertEqual(len(mine), 1, lane["id"])
            self.assertIn("| %s |" % lane["stage"], mine[0], lane["id"])
            self.assertIn("PROPOSED", mine[0], lane["id"])
        for stage in self.plan["stages"]:
            heading = "### %s. %s (rating %s" % (stage["id"], stage["name"], stage["rating"])
            self.assertIn(heading, md, stage["id"])


if __name__ == "__main__":
    unittest.main()
