import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("text_concordance", Path(__file__).with_name("concordance.py"))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def word(surface, lemma=None, flags=""):
    return {"h": [[surface, flags]], "m": [[surface, lemma, "subs"]] if lemma else []}


class CorpusTests(unittest.TestCase):
    def inventory(self, words, extra_lines=None, rows=None):
        scroll = {"source": "synthetic fixture", "columns": [{"c": 1, "lines": [{"l": 1, "w": words}] + (extra_lines or [])}]}
        return c.inventory(scroll, {}, [], rows or [{"entry_puech": "1", "col_line": "I:1"}])

    def test_javascript_is_never_executed(self):
        self.assertEqual(c.parse_scroll('/* header */ window.SCROLL_TEXT = {"a":1};'), {"a": 1})
        with self.assertRaises((ValueError, json.JSONDecodeError)):
            c.parse_scroll('window.SCROLL_TEXT = {"a":1}; alert("bad");')

    def test_homonyms_do_not_collapse(self):
        out = self.inventory([word("אמות", "אַמָּה_1"), word("האמא", "אַמָּה_2")])
        self.assertEqual(out["occurrences"][0]["families"], ["cubit_unit"])
        self.assertEqual(out["occurrences"][1]["families"], ["conduit_lexeme"])

    def test_removed_and_restored_are_visible(self):
        out = self.inventory([word("תחת", "תַּחַת_1", "r"), word("תחת", "תַּחַת_1", "x"), word("תחת", "תַּחַת_1", "d")])
        self.assertEqual([o["flags"] for o in out["occurrences"]], [["r"], ["x"], ["d"]])
        self.assertEqual(out["occurrences"][1]["surface_without_removed_segments"], "")
        self.assertEqual(out["family_counts"]["beneath"], 3)  # encoded lexical triggers, not three secure readings

    def test_bigrams_do_not_bridge_missing_morphology(self):
        words = [word("תחת", "תחת_1"), word("…"), word("פתח", "פתח"),
                 word("תחת", "תחת_1"), word("…"), word("פתח", "פתח")]
        self.assertEqual(self.inventory(words)["repeated_word_pairs"], [])

    def test_bigrams_do_not_cross_entry_boundary(self):
        out = self.inventory([word("תחת", "תחת_1")],
                             [{"l": 2, "w": [word("פתח", "פתח")]},
                              {"l": 3, "w": [word("תחת", "תחת_1")]},
                              {"l": 4, "w": [word("פתח", "פתח")]}],
                             [{"entry_puech": str(i), "col_line": f"I:{i}"} for i in range(1, 5)])
        self.assertEqual(out["repeated_word_pairs"], [])

    def test_shared_line_has_ambiguous_owners_and_no_repeated_frame(self):
        rows = [{"entry_puech": "2", "col_line": "I:1"}, {"entry_puech": "3", "col_line": "I:1"}]
        out = self.inventory([word("תחת", "תחת_1"), word("פתח", "פתח")] * 2, rows=rows)
        self.assertEqual(out["occurrences"][0]["entries"], ["2", "3"])
        self.assertTrue(out["occurrences"][0]["shared_boundary_context"])
        self.assertEqual(out["repeated_word_pairs"], [])

    def test_variant_scope_word_and_also(self):
        variants = [{"id": "a", "line": "I 1", "words": [2], "also": [{"line": "I 2", "words": [0]}]},
                    {"id": "b", "line": "I 1"}]
        self.assertEqual([v["id"] for v in c.scoped_variants(variants, "I 1", 0)], ["b"])
        self.assertEqual([v["id"] for v in c.scoped_variants(variants, "I 2", 0)], ["a"])
        self.assertEqual(c.scoped_variants(variants, "I 2", 1), [])


class ConstraintTests(unittest.TestCase):
    def observation(self, name="east", asserted=True, reference="tell", relation="east_of", feature="pool"):
        return {"id": name, "feature_id": feature, "property": relation,
                "value": {"asserted": asserted, "reference_feature_id": reference}, "source_ids": ["source-1"]}

    def test_unknowns_are_not_failures(self):
        self.assertEqual(c.observation_status({"observations": []}, "pool", "east_of", "tell")["status"], "unknown")

    def test_role_reference_and_relation_cannot_be_substituted(self):
        model = {"observations": [self.observation(relation="north_of", feature="pit")]}
        for subject, relation, reference in [("pit", "opens_toward_north", None), ("pit", "north_of", "other-tell"), ("other-pit", "north_of", "tell")]:
            self.assertEqual(c.observation_status(model, subject, relation, reference)["status"], "unknown")

    def test_duplicate_observations_add_no_support(self):
        o = self.observation()
        one = c.observation_status({"observations": [o]}, "pool", "east_of", "tell")
        two = c.observation_status({"observations": [o, copy.deepcopy(o)]}, "pool", "east_of", "tell")
        self.assertEqual(one, two)

    def test_conflicting_assertions_stay_unknown(self):
        m = {"observations": [self.observation(), self.observation(name="other", asserted=False)]}
        out = c.observation_status(m, "pool", "east_of", "tell")
        self.assertEqual(out["status"], "unknown")
        self.assertTrue(out["conflicting_assertions"])

    def test_first_documentation_and_typology_do_not_backdate(self):
        m = {"observations": [{"id": "date", "feature_id": "pool", "property": "chronology",
                              "value": {"first_documented_state_year": 1856, "estimated_typological_interval": [-50, 70]}, "source_ids": ["s"]}]}
        self.assertEqual(c.observation_status(m, "pool", "exists_during", window=[-50, 70])["status"], "unknown")
        m["observations"][0]["value"]["secure_earliest_construction_year"] = 1898
        self.assertEqual(c.observation_status(m, "pool", "exists_during", window=[-50, 70])["status"], "contradicted")

    def test_real_inputs_keep_all_rows_and_unknown_aliases(self):
        out = c.build()
        rows = out["propagation"]["rows"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(sum(r["status"] == "rejected" for r in rows), 12)
        self.assertEqual(sum(r["status"] == "unresolved" for r in rows), 28)
        self.assertTrue(all(a["status"] == "unknown" for a in out["audited_parses"]["cross_entry_aliases"]))
        self.assertTrue(any(o["line"] == "IV 6" and "between" in o["families"] for o in out["concordance"]["occurrences"]))
        self.assertTrue(all(r["unknown_predicates"] for r in rows if r["status"] == "unresolved"))


if __name__ == "__main__":
    unittest.main()
