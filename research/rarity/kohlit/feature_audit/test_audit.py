"""Tests for the feature-level audit. Run: python3 -I test_audit.py

The synthetic tests need nothing outside the repository. The integration tests need the packets
and merged coder sheets in the scratch folder (set KOHLIT_S2 to another s2 folder); they are
skipped if those are missing.
"""
import csv
import io
import json
import os
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import audit as AU  # noqa: E402

M = AU.M
S2 = Path(os.environ.get("KOHLIT_S2", "/tmp/claude-0/-home-claude/201682b2-ff3b-52e1-990e-2c01cceb77f0/scratchpad/s2"))
HAVE_DATA = (S2 / "final" / "packets").is_dir() and (S2 / "coded_v3" / "A").is_dir()


# ---------------- synthetic units ----------------

def geom(d, b, prec=50):
    return {"distance_m": d, "bearing_deg": b, "precision_m": prec, "bearing_valid": d >= 3 * prec}


def row(rid, name, x, y, d, b, comps="", sheet="Surveyed"):
    return {"row_id": rid, "sheet": sheet, "name": name, "other_names": "", "x": x, "y": y, "components": comps,
            "geom": geom(d, b)}


def packet(uid, rows=(), nigro=()):
    return {"unit": {"row_id": uid, "sheet": "Surveyed", "name": "Test site", "other_names": "", "x": 100000,
                     "y": 100000, "components": "", "main_set": True, "in_R2": False},
            "source1_wbadb_within_2km": list(rows),
            "source5_nigro_2011": {"status": "in oasis" if nigro else "not in oasis", "entries": list(nigro)}}


def feat(fid, source, ftype, quote, pos, code="U", basis="not dated", cite=None, **extra):
    f = {"id": fid, "source": source, "type": ftype, "quote": quote, "position": pos,
         "cite": cite or {"1": "WBADB", "2": "Survey p. 461", "3": "Mem II p. 398", "4": "Pub p. 10", "5": "Nigro 2011 cat. 1 p. 1"}[source],
         "date": {"code": code, "basis": basis}, "subtype": extra.pop("subtype", ftype)}
    if ftype == "pool":
        f["pool_def"] = extra.pop("pool_def", "yes")
    if ftype == "pit":
        f["is_tomb"] = extra.pop("is_tomb", False)
    if ftype == "grave":
        f["cavity_with_opening"] = extra.pop("cavity_with_opening", False)
    f.update(extra)
    return f


def sheet(uid, coder, feats):
    return {"unit_id": uid, "coder": coder, "sources": {k: "read" for k in "12345"}, "explicit_absence": [],
            "features": feats}


NONE = {"kind": "none"}


def words(d, rel="unit"):
    return {"kind": "words", "direction": d, "distance_m": None, "relative_to": rel}


def grid(ref):
    return {"kind": "grid", "ref": ref}


def run_audit(packets, A, B):
    frows, jrows, units = AU.audit(packets, A, B)
    return frows, jrows, units


def pick(rows, **kw):
    return [r for r in rows if all(r[k] == v for k, v in kw.items())]


class Synthetic(unittest.TestCase):

    def test_same_passage_links_coders_but_not_families(self):
        p = packet("T1")
        a = sheet("T1", "A", [feat("f1", "2", "pit", "A cistern and a small pool were also exposed.", NONE),
                              feat("f2", "2", "pool", "A cistern and a small pool were also exposed.", words("east part"))])
        b = sheet("T1", "B", [feat("f9", "2", "pool", "A cistern and a small pool were also exposed.", words("east part"))])
        gid, _ = AU.identity_groups("T1", p, {"A": a, "B": b})
        self.assertEqual(gid[("A", "f2")], gid[("B", "f9")])
        self.assertNotEqual(gid[("A", "f1")], gid[("A", "f2")])

    def test_duplicate_wbadb_rows_are_one_place(self):
        p = packet("T2", rows=[row("S9", "Kh. Foo", 100000, 100800, 800, 0.0, "cisterns; caves"),
                               row("E9", "Kh. Foo", 100000, 100800, 800, 0.0, "cisterns; caves", sheet="Excavations")])
        a = sheet("T2", "A", [feat("f1", "1", "pit", "cisterns", grid("S9"), cite="WBADB S9 Site_Components")])
        b = sheet("T2", "B", [feat("f1", "1", "pit", "cisterns; caves", grid("E9"), cite="WBADB E9 Site_Components")])
        gid, _ = AU.identity_groups("T2", p, {"A": a, "B": b})
        self.assertEqual(gid[("A", "f1")], gid[("B", "f1")])

    def test_wbadb_row_and_nigro_entry_are_not_joined(self):
        n = {"ref": "N1", "cat_no": 1, "name": "Birket Foo", "page": 1, "x": 100100, "y": 100800, "geom": geom(806, 7.1), "text": ""}
        p = packet("T3", rows=[row("S5", "Birket Foo", 100000, 100800, 800, 0.0, "pool")], nigro=[n])
        a = sheet("T3", "A", [feat("f1", "1", "pool", "pool", grid("S5"), cite="WBADB S5 Site_Components"),
                              feat("f2", "5", "pool", "Public architecture: pool", grid("N1"), cite="Nigro 2011 cat. 1 p. 1")])
        gid, _ = AU.identity_groups("T3", p, {"A": a})
        self.assertNotEqual(gid[("A", "f1")], gid[("A", "f2")])

    def s1283_like(self):
        """Both coders MATCH C1 on one pool; for C2 each uses a pit the other gives no position."""
        p = packet("T4")
        pool = "A cistern and a small pool were also exposed."
        swp = "It supplies large cemented cave-cisterns some 350 feet or more below"
        zer = "Five large circular robbing pits were dug in the northern area."
        a = sheet("T4", "A", [feat("p", "2", "pool", pool, words("east part"), "D", "Herodian peristyle", cite="Z p. 471"),
                              feat("c", "3", "pit", swp, words("N"), cite="Mem II p. 398"),
                              feat("r", "2", "pit", zer, NONE, cite="Z p. 461")])
        b = sheet("T4", "B", [feat("p", "2", "pool", pool, words("east part"), "D", "Herodian peristyle", cite="Z p. 471"),
                              feat("c", "3", "pit", swp, NONE, cite="Mem II pp. 396, 398"),
                              feat("r", "2", "pit", zer, words("N"), cite="Z p. 461")])
        return run_audit({"T4": p}, {"T4": a}, {"T4": b})

    def test_condition_match_on_different_features_is_flagged(self):
        frows, jrows, _ = self.s1283_like()
        c2 = pick(frows, variant="primary", nigro="with", condition="C2")
        self.assertEqual({(r["coder"], r["feature_id"]) for r in c2}, {("A", "c"), ("B", "r")})
        self.assertTrue(all(r["condition_flag"] == "NO SHARED FEATURE" for r in c2))
        self.assertTrue(all(r["merged"] == "MATCH" for r in c2))
        c1 = pick(frows, variant="primary", nigro="with", condition="C1")
        self.assertTrue(all(r["condition_flag"] == "shared feature" for r in c1))
        j = pick(jrows, variant="primary", nigro="with")[0]
        self.assertEqual(j["verdict"], "conditionally compatible")
        self.assertTrue(j["verdict_conditions"].startswith("No feature set that both coders accept"))
        self.assertEqual(j["consensus_valid_combinations"], 0)
        self.assertIn("disputed", j["A_conditions"])

    def _one_grave(self, subtype):
        p = packet("T5", rows=[row("S7", "Kh. Bar", 100100, 100500, 510, 11.3, "burial cave")])
        a = sheet("T5", "A", [feat("g", "1", "grave", subtype, grid("S7"), "D", "row records Rom",
                                   cite="WBADB S7 Site_Components", subtype=subtype, cavity_with_opening=True)])
        return run_audit({"T5": p}, {"T5": a}, {})

    def test_one_grave_cannot_be_pit_and_graves(self):
        _, jrows, _ = self._one_grave("burial cave")
        prim = pick(jrows, variant="primary", nigro="with")
        self.assertEqual(prim, [])  # C2 needs a tomb shaft: only the variant has two conditions
        j = pick(jrows, variant="C2_tomb_shafts", nigro="with")[0]
        self.assertEqual(j["matched_conditions"], "C2+C3s")
        self.assertEqual(j["verdict"], "not shown compatible")

    def test_plural_tomb_record_is_conditional(self):
        _, jrows, _ = self._one_grave("shaft tombs")
        j = pick(jrows, variant="C2_tomb_shafts", nigro="with")[0]
        self.assertEqual(j["verdict"], "conditionally compatible")
        self.assertIn("one record of several features", j["verdict_conditions"])

    def test_out_of_use_pit_is_not_compatible(self):
        p = packet("T6", rows=[row("S8", "Kh. Baz", 100000, 100900, 900, 0.0, "tombs")])
        a = sheet("T6", "A", [feat("s", "4", "pit", "a defunct pit, Silo B", words("N"), "D",
                                   "ca. 1650-1625 BCE; out of use in the next phase"),
                              feat("t", "1", "grave", "tombs", grid("S8"), "D", "row records Rom", cite="WBADB S8 Site_Components")])
        _, jrows, _ = run_audit({"T6": p}, {"T6": a}, {})
        j = pick(jrows, variant="primary", nigro="with")[0]
        self.assertEqual(j["verdict"], "not shown compatible")
        self.assertIn("out of use", j["verdict_conditions"])

    def test_dated_distinct_agreed_features_are_jointly_compatible(self):
        p = packet("T7", rows=[row("S1", "Kh. One", 100000, 100600, 600, 0.0, "cistern"),
                               row("S2", "Kh. Two", 100100, 100700, 707, 8.1, "tombs")])
        fs = [feat("c", "1", "pit", "cistern", grid("S1"), "D", "row records Rom", cite="WBADB S1 Site_Components"),
              feat("t", "1", "grave", "tombs", grid("S2"), "D", "source says Herodian", cite="WBADB S2 Site_Components")]
        _, jrows, _ = run_audit({"T7": p}, {"T7": sheet("T7", "A", fs)}, {"T7": sheet("T7", "B", fs)})
        j = pick(jrows, variant="primary", nigro="with")[0]
        self.assertEqual(j["verdict"], "jointly compatible")
        self.assertEqual(j["same_feature_both_coders"], "C2:yes C3s:yes")

    def test_same_words_read_two_ways_is_a_condition(self):
        p = packet("T8", rows=[row("S3", "Kh. Three", 100000, 100700, 700, 0.0, "tombs")])
        q = "cisterns and caves on the northern slope"
        a = sheet("T8", "A", [feat("c", "3", "pit", q, words("N"), subtype="cisterns"),
                              feat("v", "3", "pit", q, NONE, subtype="caves"),
                              feat("t", "1", "grave", "tombs", grid("S3"), "D", "row records Rom", cite="WBADB S3 Site_Components")])
        _, jrows, _ = run_audit({"T8": p}, {"T8": a}, {})
        j = pick(jrows, variant="primary", nigro="with")[0]
        self.assertIn("reads the same words as 'N' here but as 'no position' for v", j["verdict_conditions"])

    def test_date_classes(self):
        def dc(code, basis):
            return AU.date_class({"date": {"code": code, "basis": basis}})
        self.assertEqual(dc("U", "x"), "undated")
        self.assertEqual(dc("L", "x"), "after 135 CE")
        self.assertEqual(dc("D", "row S3835 is the cave; records Rom1"), "in window")
        self.assertEqual(dc("D", "source dates the tomb IA2c"), "before window")
        self.assertEqual(dc("D", "listed under Roman Period (post-Herodian, 2nd century AD)"), "straddles 135 CE")
        self.assertEqual(dc("D", "Silo B, ca. 1650-1625 BCE; out of use later"), "before window, out of use")
        self.assertEqual(dc("D", "source: burial place of the community, i.e. Periods Ib-II"), "in window")

    def test_short_quote(self):
        q = AU.short_quote(" ".join(f"w{i}" for i in range(20)))
        self.assertEqual(len(q.replace(" …", "").split()), AU.MAX_QUOTE_WORDS)
        self.assertEqual(AU.short_quote("a b c"), "a b c")

    def test_pages(self):
        self.assertEqual(AU.pages("Zertal p. 461 (section A.2; fig. 340 p. 475)"), {461, 475})
        self.assertEqual(AU.pages("Site 173, pp. 462, 471-472"), {462, 471, 472})
        self.assertEqual(AU.pages("Mem III p. 24 (packet page; printed p. 191)"), {24, 191})


# ---------------- integration with the real sheets ----------------

@unittest.skipUnless(HAVE_DATA, f"scratch packets and sheets not found under {S2}")
class Integration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.packets = M.load_packets(S2 / "final")
        cls.A = M.load_sheets(S2 / "coded_v3" / "A")
        cls.B = M.load_sheets(S2 / "coded_v3" / "B")
        cls.frows, cls.jrows, cls.units = AU.audit(cls.packets, cls.A, cls.B)

    def test_committed_chain_rebuilds_the_merged_sheets(self):
        a, b = AU.committed_sheets()
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(self.A, sort_keys=True))
        self.assertEqual(json.dumps(b, sort_keys=True), json.dumps(self.B, sort_keys=True))

    def test_rows_are_exactly_match_py_features(self):
        got = {}
        for r in self.frows:
            got.setdefault((r["unit_id"], r["variant"], r["nigro"], r["condition"], r["coder"]), set()).add(r["feature_id"])
        want = {}
        for uid in self.A:
            refs = M.refs_in_packet(self.packets[uid])
            for coder, sheets in (("A", self.A), ("B", self.B)):
                if uid not in sheets:
                    continue
                for (v, n), cv in M.unit_values(sheets[uid], refs).items():
                    for c in M.CONDITIONS:
                        if cv[c] == "MATCH":
                            want[(uid, v, n, c, coder)] = set(cv["_features"][c])
        self.assertEqual(got, want)

    def test_merged_values_equal_the_registered_results(self):
        path = AU.STAGE2 / "addendum_s2" / "results" / "unit_results.csv"
        with open(path, newline="", encoding="utf-8") as fh:
            reg = {(r["unit_id"], r["variant"], r["nigro"]): r for r in csv.DictReader(fh)}
        for uid, U in self.units.items():
            for key in AU.KEYS:
                for c in M.CONDITIONS:
                    self.assertEqual(U.merged(key, c), reg[(uid,) + key][c], (uid, key, c))

    def test_joint_rows_cover_every_merged_two_condition_unit(self):
        path = AU.STAGE2 / "addendum_s2" / "results" / "summary.json"
        two = {r["unit_id"] for r in json.loads(path.read_text(encoding="utf-8"))["two_of_three"]}
        prim = {r["unit_id"] for r in self.jrows if r["variant"] == "primary" and r["nigro"] == "with"}
        self.assertEqual(prim, two)
        self.assertEqual(set(AU.PRIORITY), two)

    def test_qarn_sartaba(self):
        c2 = pick(self.frows, unit_id="S1283", variant="primary", nigro="with", condition="C2")
        self.assertEqual({(r["coder"], r["feature_id"]) for r in c2}, {("A", "f11"), ("B", "f14")})
        self.assertTrue(all(r["condition_flag"] == "NO SHARED FEATURE" for r in c2))
        j = pick(self.jrows, unit_id="S1283", variant="primary", nigro="with")[0]
        self.assertEqual((j["same_feature_both_coders"], j["verdict"]), ("C1:yes C2:no", "conditionally compatible"))
        flagged = {(r["unit_id"], r["condition"]) for r in self.frows if r["variant"] == "primary" and r["nigro"] == "with"
                   and r["condition_flag"] == "NO SHARED FEATURE"}
        self.assertEqual(flagged, {("S1283", "C2")})

    def test_tell_es_sultan_tomb_shaft_match_reuses_one_cave(self):
        j = pick(self.jrows, unit_id="E334", variant="C2_tomb_shafts", nigro="with")[0]
        self.assertEqual((j["matched_conditions"], j["verdict"]), ("C1+C2+C3s", "not shown compatible"))

    def test_quotes_are_short(self):
        for r in self.frows:
            self.assertLessEqual(len(r["quote"].replace(" …", "").split()), AU.MAX_QUOTE_WORDS)

    def test_committed_csvs_are_current(self):
        for name, rows, fields in (("features_behind_matches.csv", self.frows, AU.FEATURE_FIELDS),
                                   ("joint_compatibility.csv", self.jrows, AU.JOINT_FIELDS)):
            buf = io.StringIO()
            w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in fields})
            self.assertEqual((HERE / name).read_text(encoding="utf-8"), buf.getvalue(), name)

    def test_readme_tables_are_current(self):
        text = (HERE / "README.md").read_text(encoding="utf-8")
        block = text[text.index(AU.MARK_START) + len(AU.MARK_START): text.index(AU.MARK_END)]
        self.assertEqual(block.strip(), AU.markdown_tables(HERE).strip())


if __name__ == "__main__":
    unittest.main(verbosity=1)
