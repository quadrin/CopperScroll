"""Semantic regression checks and deterministic reconstruction of the exploratory overlay."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('manual_overlay', HERE / 'rebuild.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


class ReviewTests(unittest.TestCase):
    def test_unconfirmed_is_missing_evidence_not_automatic_rejection(self):
        check = dict(id='pool', verdict='not confirmed')
        self.assertEqual(R.repaired_code(check, 'res|B-any', 'verified'), 'UNKNOWN')
        self.assertEqual(R.repaired_code(check, 'res|B-any', 'verified', {'corrected_code': 'FAIL'}), 'FAIL')

    def test_partly_confirmed_bracket_and_reading_specific_marker(self):
        check = dict(id='pool', verdict='partly confirmed')
        self.assertEqual(R.repaired_code(check, 'res|B-any', 'verified'), 'UNKNOWN')
        self.assertEqual(R.repaired_code(check, 'res|B-any', 'retain_partial'), 'MATCH')
        check['id'] = R.FROZEN_MARKER
        self.assertEqual(R.repaired_code(check, 'S-stone|F-flow', 'verified'), 'UNKNOWN')
        self.assertEqual(R.repaired_code(check, 'S-any|F-flow', 'verified'), 'MATCH')

    def test_head_error_reaches_derived_outlet_and_date(self):
        row = dict(id='aqueduct', type='aqueduct', entry='32', branch='O-built|K-Qelt|T-none',
                   clauses='outlet=MATCH;kozeba=MATCH', overall='MATCH', date_code='in')
        checks = {('aqueduct', k): dict(id='aqueduct', verdict='not confirmed', ledger='test', reason='wrong feature')
                  for k in ('head', 'date')}
        out, _ = R.repair_scores([row], checks, {})
        self.assertEqual(out[0]['clauses'], 'outlet=UNKNOWN;kozeba=MATCH')
        self.assertEqual(out[0]['overall'], 'UNKNOWN')
        self.assertEqual(out[0]['date_code'], 'undated')

    def test_omitted_duplicate_cannot_restore_a_match(self):
        common = dict(type='reservoir_pool', entry='46', branch='res|B-any', date_code='in')
        rows = [dict(common, id='preferred', clauses='entrance=UNKNOWN', overall='UNKNOWN'),
                dict(common, id='superseded', clauses='entrance=MATCH', overall='MATCH')]
        detail = R.aggregate(rows, {'unit': ['preferred']})
        self.assertEqual(detail[0]['overall'], 'UNKNOWN')

    def test_rebuild_reproduces_all_committed_overlay_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            R.main(tmp)
            generated = {p.name for p in Path(tmp).iterdir()}
            for name in generated:
                self.assertEqual((Path(tmp) / name).read_bytes(), (HERE / name).read_bytes(), name)

    def test_fourteen_new_unconfirmed_hits_do_not_remove_date_eligible_matches(self):
        checks = [r for r in R.read(R.LANE / 'phase4_posthoc_checks.csv') if r['verdict'] == 'not confirmed']
        self.assertEqual(len(checks), 14)
        original = {(r['entry'], r['branch'], r['lineage'], r['date_rule']): r
                    for r in R.read(R.LANE / 'phase4_counts.csv')}
        for r in R.read(HERE / 'phase4_unconfirmed_only_counts.csv'):
            key = (r['entry'], r['branch'], r['lineage'], r['date_rule'])
            if r['lineage'] == 'MERGED':
                self.assertEqual(r['k_match'], original[key]['k_match'], key)

    def test_full_match_counts_and_dated_entrance_keep_the_step_pool_separate(self):
        leads = R.read(HERE / 'surviving_leads.csv')
        armon = [r for r in leads if 'ATQ90-' in r['member_ids'] and r['entry'] == '46']
        self.assertTrue(armon)
        self.assertTrue(all('#142' in r['member_ids'] and '#141' not in r['member_ids'] for r in armon))
        self.assertTrue(all('2km' in r['branch'] or 'B-any' in r['branch'] for r in armon))
        self.assertTrue(all(r['sources'] and r['missing_fields'] and r['next_discriminating_or_rejecting_observation'] for r in leads))
        for path in HERE.glob('*counts.csv'):
            for r in R.read(path):
                n = int(r['k_match']) + int(r['f_fail']) + int(r['m_unknown']) + int(r.get('not_scored', '0'))
                self.assertEqual(n, int(r['N']), (path.name, r))


if __name__ == '__main__':
    unittest.main()
