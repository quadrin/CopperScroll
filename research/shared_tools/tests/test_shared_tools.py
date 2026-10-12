import csv
import json
import math
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import core
from benchmarks import fit_affine, registration_check, run
from review_capture import CAPTURE_FIELDS, export_review, validate_capture


class Retrieval(unittest.TestCase):
    def test_rebuild_recovers_a_corrupt_generated_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / 'research/sources/control.md'
            note.parent.mkdir(parents=True)
            note.write_text('Survey control')
            cache = root / 'cache'
            cache.mkdir()
            (cache / 'evidence.sqlite').write_bytes(b'broken database')
            core.build_index(root, cache)
            self.assertTrue(core.search('Survey control', destination=cache, root=root))

    def test_new_figure_links_use_the_build_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'research/assets/new/figure_manifest.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({'source_title': 'New control', 'figure': 'Plan 2',
                                        'repository_path': 'research/assets/new/plan.png',
                                        'visually_inspected': False}))
            with patch.object(core, 'repository_ref', return_value='a' * 40):
                core.build_index(root, root / 'cache')
            result = core.search('New control', destination=root / 'cache', root=root)[0]
            self.assertIn('/' + 'a' * 40 + '/', result['url'])
            self.assertIn('/' + 'a' * 40 + '/', result['locator']['asset_url'])
            self.assertFalse(result['locator']['inspection_as_recorded'])

    def test_exact_locators_and_no_inferred_page_offset(self):
        record = core.locator_record({'file': 'p74.png', 'printed_page': '74*', 'pdf_page': 5,
                                     'original_pdf': 'book.pdf'}, 'research/assets/book/manifest.json')
        self.assertEqual(record['printed_page'], '74*')
        self.assertEqual(record['pdf_page_one_based'], 5)
        self.assertEqual(record['original_pdf'], 'research/assets/book/book.pdf')
        record = core.locator_record({'printed_page': 74}, 'research/assets/book/manifest.json')
        self.assertIsNone(record['pdf_page_one_based'])
        self.assertIsNone(core.locator_record({'figure': 'Fig.1', 'pdf_page': True}, 'x.json')['pdf_page_one_based'])

    def test_search_unicode_literal_input_and_stale_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / 'research/sources/test.md'
            note.parent.mkdir(parents=True)
            note.write_text('# Evidence\nKoḥlit כּוֹחְלִית L-656\n')
            cache = root / 'cache'
            core.build_index(root, cache)
            for query in ('Kohlit', 'כוחלית', 'כּוֹחְלִית', 'L-656'):
                self.assertTrue(core.search(query, destination=cache, root=root), query)
            self.assertEqual(core.search('" OR *', destination=cache, root=root), [])
            note.write_text('changed')
            with self.assertRaisesRegex(ValueError, 'stale'):
                core.search('Kohlit', destination=cache, root=root)

    def test_nested_figure_metadata_keeps_original_inspection_scope(self):
        objects = list(core.walk_objects({'publication': 'Report', 'inspection': 'not inspected',
                                         'pages': [{'figure': 'Plan5', 'printed_page': '63', 'pdf_page': 21}]}))
        record = core.locator_record(objects[-1][1], 'research/assets/report/manifest.json')
        self.assertEqual(record['title'], 'Report')
        self.assertEqual(record['inspection_as_recorded'], 'not inspected')

    def test_multiline_csv_links_use_physical_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'catalog.csv'
            p.write_text('title,note\nfirst,"line one\nline two"\nsecond,last\n')
            data=list(core.rows_with_lines(p))
            self.assertEqual([n for n,_ in data],[2,4])

    def test_adapter_caches_reject_changed_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cache=root/'cache';cache.mkdir()
            source=root/'source.json';source.write_text('{}')
            core.dump({'builder_sha256':core.digest(core.HERE/'core.py'),
                       'datasets':{'entries':{'source.json':core.digest(source)}}},cache/'adapter_inputs.json')
            core.dump({'entries':[]},cache/'entries.json')
            self.assertEqual(core.cached_dataset('entries',root,cache),{'entries':[]})
            source.write_text('{"changed":true}')
            with self.assertRaisesRegex(ValueError,'stale'):
                core.cached_dataset('entries',root,cache)


class Adapters(unittest.TestCase):
    def test_catalog_is_complete_and_substrates_stay_separate(self):
        data = core.manuscript()
        self.assertEqual(len(data['images']), 942)
        self.assertEqual(sum(i['substrate'] == 'original' for i in data['images']), 294)
        self.assertEqual(len({i['id'] for i in data['images']}), 942)
        self.assertTrue(all(i['view_transform'] is None for i in data['images']))
        self.assertTrue(all(i['metric_depth_calibration'] is None for i in data['images']))
        result = core.image_query(data, line='VII:11', substrate='original')
        self.assertTrue(result['images'])
        self.assertTrue(all(i['cut_as_catalogued'] in (13, 14) for i in result['images']))
        self.assertTrue(all(c['original_roi'] is None for c in result['locus_claims']))
        self.assertEqual(core.image_query(data, line='VIII 99')['images'], [])

    def test_entry_import_retains_boundary_and_global_variants(self):
        data = core.entry_packets()
        self.assertEqual(len(data['entries']), 61)
        self.assertIn('12a', {e['entry'] for e in data['entries']})
        e = next(e for e in data['entries'] if e['entry'] == '3')
        self.assertIn('I 6', {r['line'] for r in e['translation_context']})
        self.assertIn('g-kk', e['global_variant_ids'])
        self.assertIsNone(e['measurement_origin'])
        self.assertIn('pending review', e['formal_constraint_status'])

    def test_replica_cannot_authenticate_an_original_locus(self):
        claim = {'status':'authenticated', 'neighboring_original_hebrew':'אב',
                 'original_roi':[0,0,10,10], 'view_id':'UC110814682', 'source':'citation'}
        with patch.object(core, 'read', return_value=[claim]):
            with self.assertRaisesRegex(ValueError, 'original-object'):
                core.manuscript()

    def test_notices_do_not_become_a_regional_denominator(self):
        data = core.control_packets()
        self.assertEqual(len(data['cave_controls']), 3)
        self.assertEqual(len(data['pool_notices']), 28)
        self.assertIsNone(data['eligible_regional_denominator'])
        self.assertIsNone(data['coverage_complete'])
        self.assertTrue(any(o['value'] is None for o in data['observations']))


class Calibration(unittest.TestCase):
    def test_rotation_and_mirror_and_bad_holdout(self):
        output = run()
        for item in output['synthetic_calibration'][:-1]:
            self.assertEqual(item['status'], 'within_tolerance')
            self.assertLess(item['heldout_error'], 1e-8)
        self.assertEqual(output['synthetic_calibration'][-1]['status'], 'outside_tolerance')
        for item in output['exposed_plan_calibration']:
            self.assertLess(item['reproduction_error_metres'], 1e-12)
        self.assertEqual(output['independent_empirical_benchmark']['status'], 'not_run')
        self.assertLess(output['exposed_registration_diagnostic']['local_reproduction_error_metres'], 1e-10)
        self.assertGreater(output['exposed_registration_diagnostic']['withheld_residual_metres_as_recorded'], 240)

    def test_collinear_and_nonfinite_control_rejection(self):
        with self.assertRaisesRegex(ValueError, 'Degenerate'):
            fit_affine([[0,0],[1,1],[2,2]], [[0,0],[1,1],[2,2]])
        for bad in (math.nan, math.inf, True):
            with self.assertRaises(ValueError):
                registration_check([[0,0],[1,0],[0,1]], [[0,0],[1,0],[0,1]], [0,0], [bad,0], 1)


class Acquisition(unittest.TestCase):
    def test_reviewer_packet_has_no_location_or_answer_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'packet'
            export_review(dest)
            reader = json.loads((dest / 'reviewer/items.json').read_text())
            self.assertTrue(reader)
            self.assertTrue(all(r['file'] is None for r in reader))
            rendered = json.dumps(reader)
            for leaked in ('XII', 'VII', 'UC152', 'candidate_cuts', 'cut_as_catalogued'):
                self.assertNotIn(leaked, rendered)
            with self.assertRaises(ValueError):
                export_review(dest)

    def test_capture_hash_permissions_and_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            file = folder / 'image.bin'; file.write_bytes(b'capture')
            row = {k:'' for k in CAPTURE_FIELDS}
            row.update(asset_id='A01', local_file='image.bin', object_or_document_id='OBJ1',
                       custodian='Archive', view_id='V1', substrate='original', reuse_permission='unknown')
            path = folder / 'capture.csv'
            def write():
                with path.open('w', newline='') as f:
                    w = csv.DictWriter(f, fieldnames=CAPTURE_FIELDS); w.writeheader(); w.writerow(row)
            write(); output = validate_capture(path)
            self.assertEqual(output['records'][0]['status'], 'incomplete')
            self.assertEqual(output['records'][0]['record']['computed_sha256'], core.digest(file))
            row['sha256'] = 'wrong'; write()
            self.assertEqual(validate_capture(path)['status'], 'invalid')
            row['sha256']=''; row['local_file']='../outside'; write()
            self.assertEqual(validate_capture(path)['status'], 'invalid')


if __name__ == '__main__':
    unittest.main()
