"""Alignment, normalisation and class rules on toy strings.

Run from the repository root:
    python3 -I -m unittest discover -s research/text/edition_confusions/tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from align import align, letters, pair_key, levenshtein_ops, N_UNORDERED_PAIRS  # noqa: E402
from build import parse_reading, classify  # noqa: E402


def cls(a, b, note=''):
    return classify(parse_reading(a), parse_reading(b), note)[0]


class TestAlign(unittest.TestCase):
    def test_single_substitution(self):
        self.assertEqual(align('המדה', 'המרה'), [('=', 'ה', 'ה'), ('=', 'מ', 'מ'), ('S', 'ד', 'ר'), ('=', 'ה', 'ה')])

    def test_insertion_and_deletion(self):
        self.assertEqual([o for o in align('אבג', 'אג') if o[0] != '='], [('D', 'ב', None)])
        self.assertEqual([o for o in align('אג', 'אבג') if o[0] != '='], [('I', None, 'ב')])

    def test_final_forms_are_base_letters(self):
        self.assertEqual(letters('ךםןףץ'), 'כמנפצ')
        self.assertTrue(all(o[0] == '=' for o in align('שלום', 'שלומ')))

    def test_transliteration(self):
        self.assertEqual(letters('ḥpwr'), 'חפור')
        self.assertEqual(letters('ʾšwḥ'), 'אשוח')
        self.assertEqual(letters('ʿkwr'), 'עכור')
        self.assertEqual(letters('bśyʾ'), letters('bšyʾ'))
        self.assertEqual(letters('ṭwr ṣwq qdrwn'), 'טורצוקקדרונ')

    def test_frozen_tie_break(self):
        # Ties prefer substitution, then deletion, then insertion (PLAN.md section 7).
        ops = [o[:3] for o in levenshtein_ops('ני', 'מ')]
        self.assertEqual(ops, [('D', 'נ', None), ('S', 'י', 'מ')])

    def test_pair_key_unordered(self):
        self.assertEqual(pair_key('ר', 'ד'), 'ד–ר')
        self.assertEqual(pair_key('ך', 'ב'), 'ב–כ')
        self.assertEqual(N_UNORDERED_PAIRS, 231)


class TestClasses(unittest.TestCase):
    def test_shape(self):
        self.assertEqual(cls('כדין', 'בדין'), 'SHAPE')
        self.assertEqual(cls('wktbn', 'wbtkn'), 'SHAPE')

    def test_matres(self):
        self.assertEqual(cls('חפרות', 'חפורות'), 'MATRES')
        self.assertEqual(cls('ʾšyḥ', 'ʾšwḥ'), 'MATRES')

    def test_consonantal_waw_is_not_matres(self):
        self.assertEqual(cls('ʿsryn ʾrbʿ', 'ʿsryn wʾrbʿ', '[yw-consonantal]'), 'OTHER')

    def test_division(self):
        self.assertEqual(cls('בית המדה', 'ביתהמדה'), 'DIVISION')

    def test_restoration(self):
        self.assertEqual(cls('ש[ב]', 'ש[במערב]'), 'RESTORATION')

    def test_emendation_is_other(self):
        self.assertEqual(cls('tšʿ', 'ḥ[[m]]š'), 'OTHER')
        self.assertEqual(cls('mn hḥrm', 'mnḥh rb', '[emended]'), 'OTHER')

    def test_far_readings_are_other(self):
        self.assertEqual(cls('ים', 'דרום'), 'OTHER')

    def test_engraved_view_drops_corrections(self):
        a, b = parse_reading('ʿkwr'), parse_reading('ʿkwn(r)')
        self.assertEqual(classify(a, b)[0], 'OTHER')
        self.assertEqual(classify(a, b, engraved=True)[0], 'SHAPE')

    def test_numeral_has_no_letters(self):
        self.assertEqual(parse_reading('#numeral 1x100'), [])

    def test_sigla_states(self):
        seq = parse_reading('ח[[מ]]ש')
        self.assertEqual([x[0] for x in seq], ['ח', 'מ', 'ש'])
        self.assertEqual(seq[1][1], frozenset({'E'}))
        self.assertEqual(seq[0][1], frozenset())


if __name__ == '__main__':
    unittest.main()
