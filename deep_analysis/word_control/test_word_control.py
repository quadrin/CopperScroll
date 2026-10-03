import itertools
from fractions import Fraction
from pathlib import Path
import tempfile
import unittest

from benchmark_sample import exact_distribution
from extract_words import extract, normalized
from verify_distribution import distribution


class WordControlTests(unittest.TestCase):
    def test_two_algorithms_against_exhaustive_subsets(self):
        masks = [0, 1, 1, 2, 3, 4, 7]
        for n in [0, 1, 3, 7]:
            _, _, _, pmf, _, _ = exact_distribution(masks, n, 3)
            histogram = {m: masks.count(m) for m in set(masks)}
            self.assertEqual(pmf, distribution(histogram, n, 3))

    def test_normalization_preserves_same_rule_as_names(self):
        self.assertEqual(normalized('στέφανος'), 'ΣΤΕΦΑΝΟΣ')
        self.assertIsNone(normalized('λόγῳ'))
        self.assertIsNone(normalized('two words'))

    def test_semantics_status_empty_and_mixed_name_use(self):
        xml = '''<proiel><source id="greek-nt" language="grc"><div>
        <sentence status="reviewed">
          <token id="1" part-of-speech="Nb" lemma="καρπός" form="καρπός" citation-part="TOY 1.1"/>
          <token id="2" part-of-speech="Ne" lemma="Καρπός" form="Καρπός"/>
          <token id="3" part-of-speech="Nb" lemma="ὄνομα" form="ὄνομα"/>
          <token id="4" part-of-speech="Nb" lemma="λέξις" empty-token-sort="empty"/>
        </sentence><sentence status="unannotated">
          <token id="5" part-of-speech="Nb" lemma="καρπός" form="καρποῦ"/>
        </sentence></div></source></proiel>'''
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as d:
            p=Path(d)/'toy.xml'; p.write_text(xml)
            decisions={'καρπός': {'status':'common'}, 'ὄνομα':{'status':'unknown'},
                       'λέξις':{'status':'common'}}
            rows,audit=extract(p,decisions)
            self.assertEqual([r['greek_form'] for r in rows], ['ΚΑΡΠΟΣ'])
            self.assertTrue(rows[0]['mixed_Ne_use'])
            self.assertEqual(audit['exclusion_occurrence_counts']['semantic_unknown'],1)
            self.assertEqual(audit['exclusion_occurrence_counts']['empty_or_artificial'],1)
            self.assertEqual(audit['exclusion_occurrence_counts']['unannotated_or_unknown_sentence'],1)
            with self.assertRaises(AssertionError):
                extract(p,{})


if __name__=='__main__':
    unittest.main()
