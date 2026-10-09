"""Determinism: two builds give identical bytes, and the stored outputs match a fresh build.

Run from the repository root:
    python3 -I -m unittest discover -s research/text/edition_confusions/tests -v
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
import score  # noqa: E402


class TestDeterminism(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first = build.render(*build.build_all())
        cls.second = build.render(*build.build_all())

    def test_two_builds_identical(self):
        self.assertEqual(self.first, self.second)

    def test_stored_outputs_match(self):
        for name, text in self.first.items():
            self.assertEqual((HERE / name).read_text(encoding='utf-8'), text, name)

    def test_bootstrap_fixed_seed(self):
        t = {'ב–כ': {'I 1 w0', 'I 2 w0', 'I 3 w1'}, 'ד–ר': {'I 2 w0', 'II 1 w3'}}
        self.assertEqual(build.bootstrap(t), build.bootstrap(t))

    def test_scored_readings_match(self):
        text = score.render(score.apply_all())
        self.assertEqual((HERE / 'scored_readings.csv').read_text(encoding='utf-8'), text)

    def test_fresh_processes_agree(self):
        # Each `python3 -I` process gets its own string-hash seed, so set order differs between runs.
        import subprocess
        for _ in range(3):
            p = subprocess.run([sys.executable, '-I', str(HERE / 'build.py'), '--check'],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_plan_hash_recorded(self):
        import hashlib, json
        h = hashlib.sha256((HERE / 'PLAN.md').read_bytes()).hexdigest()
        meta = json.loads((HERE / 'confusions.json').read_text(encoding='utf-8'))['meta']
        self.assertEqual(meta['plan_sha256'], h)
        self.assertIn(h, (HERE / 'README.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
