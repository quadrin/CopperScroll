import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plan_benchmark import predict, grade, load_saved


class PlanPilot(unittest.TestCase):
    def setUp(self):
        self.case = {'id': 'control', 'scale': {'endpoints_px': [[0, 0], [100, 0]], 'metres': 2},
                     'targets': [{'id': 'axis_a', 'endpoints_px': [[0, 0], [0, 200]]},
                                 {'id': 'axis_b', 'endpoints_px': [[0, 0], [50, 0]]}]}

    def test_prediction_rejects_answers_and_invalid_scale(self):
        packet = {'schema': 1, 'cases': [self.case]}
        self.case['reference_metres'] = 4
        with self.assertRaisesRegex(ValueError, 'only'):
            predict(packet)
        del self.case['reference_metres']
        self.case['targets'][0]['expected_metres'] = 4
        with self.assertRaisesRegex(ValueError, 'coordinates only'):
            predict(packet)
        del self.case['targets'][0]['expected_metres']
        self.case['scale']['metres'] = True
        with self.assertRaises(ValueError):
            predict(packet)
        self.case['scale']['metres'] = 2
        self.case['scale']['endpoints_px'][1] = [2, 0]
        with self.assertRaisesRegex(ValueError, 'too short'):
            predict(packet)

    def test_wrong_reference_fails_and_missing_boundary_remains_unknown(self):
        predictions = predict({'schema': 1, 'cases': [self.case]})
        references = {'cases': [{'id': 'control', 'dimensions_metres': [5, 1]}]}
        self.assertEqual(grade(predictions, references)['cases'][0]['primary']['screening_flag'], 'outside_budget')
        self.case['targets'][1]['endpoints_px'] = None
        predictions = predict({'schema': 1, 'cases': [self.case]})
        result = grade(predictions, references)['cases'][0]
        self.assertEqual(result['screening_flag'], 'unmeasurable')
        self.assertNotIn('primary', result)
        self.assertEqual(len(result['available_chords']), 1)
        references['cases'][0]['id'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'match exactly'):
            grade(predictions, references)

    def test_saved_result_rejects_changed_reference_and_changed_grade(self):
        source = Path(__file__).resolve().parents[1] / 'plan_pilot'
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'pilot'
            shutil.copytree(source, folder)
            self.assertEqual(load_saved(folder)['status'], 'completed')
            refs = folder / 'references.json'
            original = refs.read_bytes()
            refs.write_bytes(original + b' ')
            with self.assertRaisesRegex(ValueError, 'stale'):
                load_saved(folder)
            refs.write_bytes(original)
            path = folder / 'results.json'
            result = json.loads(path.read_text())
            result['cases'][0]['primary']['absolute_error_metres'] = 0
            path.write_text(json.dumps(result))
            with self.assertRaisesRegex(ValueError, 'grades differ'):
                load_saved(folder)
