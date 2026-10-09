"""Tests for the location-language review. Run from the repository root:

    python3 -I -m unittest discover -s research/text/location_language -p 'test_*.py'
"""
import contextlib
import importlib.util
import io
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILD = load('location_build', 'build_occurrences.py')
CONS = load('location_consequences', 'consequences.py')


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.built = BUILD.build()
        cls.occ = {o['id']: o for e in cls.built['expressions'] for o in e['occurrences']}

    def test_committed_file_is_current(self):
        committed = (HERE / 'occurrences.json').read_text(encoding='utf-8')
        self.assertEqual(committed, BUILD.dumps(self.built), 'rebuild with build_occurrences.py')

    def test_build_is_deterministic(self):
        self.assertEqual(BUILD.dumps(BUILD.build()), BUILD.dumps(self.built))

    def test_every_search_match_is_listed_or_excluded(self):
        for e in self.built['expressions']:
            for c in e['search_coverage']:
                self.assertIn(c['state'], ('listed', 'excluded'), (e['id'], c))
            if e['search_patterns']:
                self.assertTrue(e['search_coverage'], e['id'])

    def test_hebrew_shown_comes_from_the_scroll_text(self):
        self.assertEqual(self.occ['melah@II 1']['hebrew_shown'], 'המלח')
        self.assertEqual(self.occ['melah@III 8']['hebrew_shown'], 'שבמלחמ')
        self.assertEqual(self.occ['al_pi@XII 11']['hebrew_shown'], 'על פיה')
        self.assertEqual(self.occ['dir_sheb@XII 10']['hebrew_shown'], 'שב{צח}צפון')
        self.assertEqual(self.occ['dig_n@III 2']['hebrew_shown'], '<חפר>')
        self.assertEqual(self.occ['kohlit@IV 1']['hebrew_shown'], '[כ]ח°לת°')

    def test_known_counts(self):
        counts = {e['id']: len([o for o in e['occurrences'] if o['link'] != 'proposed']) for e in self.built['expressions']}
        self.assertEqual(counts['tahat'], 21)
        self.assertEqual(counts['dig_n'], 26)
        self.assertEqual(counts['dir_tsofa'], 7)
        self.assertEqual(counts['yagar'], 3)
        self.assertEqual(counts['kohlit'], 5)

    def test_links_and_membership_are_complete(self):
        for o in self.occ.values():
            self.assertIn(o['link'], BUILD.LINK_KINDS)
            self.assertIn(o['membership'], BUILD.MEMBERSHIP)
            if o['link'] in ('restored', 'proposed'):
                self.assertTrue(o['proposer'], o['id'])
            if o['membership'] != 'certain':
                self.assertTrue(o['condition'], o['id'])

    def test_editions_and_pages(self):
        for o in self.occ.values():
            if o['link'] == 'proposed':
                continue
            for key in ('puech2015', 'puech2006', 'lefkovits2000'):
                self.assertIn(key, o['editions'], o['id'])
                self.assertTrue(o['editions'][key]['ref'].startswith(('p. ', 'pp. ')), (o['id'], key))

    def test_quotations_are_short(self):
        for o in self.occ.values():
            for v in o['editions'].values():
                self.assertLessEqual(len(v['rendering'].split()), 12, (o['id'], v))

    def test_verify_rejects_a_bad_quote(self):
        bad = {'id': 'x', 'source': 'atlas/app/atlas-data.json', 'locator': {'entry': '6', 'field': 'title'},
               'quote': 'The Esplanade cistern'}
        with self.assertRaises(ValueError):
            BUILD.verify(bad, BUILD.ROOT, {})


class ConsequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = CONS.Model(CONS.load())
        cls.audit = cls.model.audit()

    def status(self, result, rid):
        return next(r['status'] for r in result['records'] if r['id'] == rid)

    def test_esplanade_fixes_all_three_lines_and_strains_the_tyropoeon(self):
        res = self.model.choose({'melah': 'esplanade_temple'})
        self.assertEqual({o['line'] for o in res['occurrences'] if o['meaning']}, {'II 1', 'III 8', 'III 11'})
        self.assertEqual(self.status(res, 'atlas:13:jer_temple'), 'supports')
        self.assertEqual(self.status(res, 'atlas:6:jer_tyropoeon'), 'tension')
        self.assertEqual(self.status(res, 'analysis:melah-place'), 'contradicts')

    def test_place_at_qumran_forces_another_sekakah(self):
        res = self.model.choose({'melah': 'place_qumran'})
        rule = next(f for f in res['forced'] if f['rule'] == 'melah-qumran-vs-sekakah')
        self.assertEqual(rule['then'], {'sekakah': ['kh_es_samra']})
        self.assertIn('atlas:21:kh_qumran', rule['forced_effects']['sekakah=kh_es_samra']['contradicts'])

    def test_split_mode_lets_conditional_members_stand_apart(self):
        choice, overrides = self.model.parse_choice(['melah=salt_common', 'melah@III 8=esplanade_temple'])
        strict = self.model.choose(choice, overrides, split=False)
        split = self.model.choose(choice, overrides, split=True)
        self.assertTrue(strict['linear_b_violations'])
        self.assertFalse(split['linear_b_violations'])
        choice, overrides = self.model.parse_choice(['al_pi=at_beside', 'al_pi@VII 14=above_upon'])
        self.assertTrue(self.model.choose(choice, overrides, split=True)['linear_b_violations'])

    def test_al_pi_and_ad_are_inconsistent_in_the_project(self):
        v = self.audit['verdicts']
        self.assertEqual(v['al_pi'], 'inconsistent')
        self.assertEqual(v['ad'], 'inconsistent')
        self.assertEqual(v['melah'], 'inconsistent')
        self.assertEqual(self.audit['usage']['al_pi']['one_meaning_fits_all'], [])

    def test_consistent_and_conditional_verdicts(self):
        v = self.audit['verdicts']
        self.assertEqual(v['dir_tsofa'], 'consistent')
        self.assertEqual(v['kohlit'], 'consistent')
        self.assertTrue(v['tahat'].startswith('consistent only if'))
        self.assertTrue(v['migreh'].startswith('consistent only if'))
        self.assertEqual(v['yagar'], 'a candidate branch contradicts itself')
        self.assertTrue(v['tsofa_attach'].startswith('differs from line to line'))

    def test_dam_contradicts_the_preferred_cairns(self):
        res = self.model.choose({'yagar': 'dam'})
        self.assertEqual(self.status(res, 'atlas:20:wadi_qumran'), 'contradicts')
        self.assertEqual(self.status(res, 'atlas:35:mar_saba'), 'contradicts')
        self.assertEqual(self.status(res, 'atlas:28:jordan_ford'), 'tension')
        self.assertEqual(self.status(res, 'atlas:35:hyrcania'), 'supports')

    def test_candidate_audit(self):
        cands = {c['candidate']: c for c in self.audit['candidates']}
        self.assertEqual(cands['atlas:35:hyrcania']['verdict'], 'needs choices contradicted elsewhere')
        self.assertEqual(cands['atlas:21:kh_qumran']['verdict'], 'consistent with the project’s other records')
        self.assertIn('ad', cands['atlas:4:tell_es_sultan']['conflicting_expressions'])
        self.assertIn('shulei', cands['atlas:38:natuf']['conflicting_expressions'])

    def test_rarity_conditions_are_read_not_changed(self):
        res = self.model.choose({'dir_sheb': 'internal'})
        self.assertEqual(self.status(res, 'rarity:C1'), 'supports')
        self.assertEqual(self.status(res, 'active_test:Q3'), 'contradicts')
        res = self.model.choose({'al_pi': 'above_upon'})
        self.assertEqual(self.status(res, 'rarity:C3'), 'tension')

    def test_depth_choice_reports_metres(self):
        res = self.model.choose({'dig_n': 'depth'})
        row = next(o for o in res['occurrences'] if o['line'] == 'VIII 12')
        self.assertEqual(row['metres'], [10.68, 12.6])

    def test_rank_lists_multi_meaning_expressions_once(self):
        rows = self.model.rank()
        names = [r['expr'] for r in rows]
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(len(self.model.meanings[n]) >= 2 for n in names))
        self.assertEqual([r['rank'] for r in rows], list(range(1, len(rows) + 1)))

    def test_generated_report_is_current(self):
        md = CONS.report_markdown(self.model, self.audit)
        self.assertEqual((HERE / 'report.md').read_text(encoding='utf-8'), md, 'run consequences.py report --write')
        committed = json.loads((HERE / 'audit.json').read_text(encoding='utf-8'))
        self.assertEqual(committed, json.loads(json.dumps(self.audit, ensure_ascii=False)))

    def test_cli(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(CONS.main(['choose', 'yagar=dam', '--json']), 0)
        self.assertEqual(json.loads(buf.getvalue())['choice'], {'yagar': 'dam'})
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(CONS.main(['choose', 'yagar=bridge']), 2)


if __name__ == '__main__':
    unittest.main()
