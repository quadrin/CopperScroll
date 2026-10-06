import unittest
from parse_ilan import date_interval, split_fields, is_heading


class ParsingTests(unittest.TestCase):
    def test_point_ce(self):
        d=date_interval("67 CE")
        self.assertEqual((d["lower"],d["upper"]),(67,67))
        self.assertIn("unvalidated",d["status"])

    def test_bce_range_sorted(self):
        d=date_interval("53-27 BCE")
        self.assertEqual((d["lower"],d["upper"]),(-53,-27))

    def test_cross_era(self):
        d=date_interval("40 BCE-67 CE")
        self.assertEqual((d["lower"],d["upper"]),(-40,67))

    def test_century_no_year_zero(self):
        a=date_interval("1st C BCE");b=date_interval("1st C CE")
        self.assertEqual((a["lower"],a["upper"]),(-100,-1))
        self.assertEqual((b["lower"],b["upper"]),(1,100))

    def test_open_bound_never_invents_lower(self):
        d=date_interval("Pre-70 CE")
        self.assertIsNone(d["lower"])
        self.assertFalse(d["upper_inclusive"])

    def test_uncertain_annotation_not_repaired(self):
        self.assertEqual(date_interval("67 CE?")["status"],"unresolved")
        self.assertEqual(date_interval("0 CE")["status"],"unresolved")

    def test_fields_not_final_Ds_split(self):
        fields,flags=split_fields("1. O: RAW Ds: description F: find S: ref E: Second name D: 67 CE")
        self.assertEqual(fields["ds"],"description")
        self.assertEqual(fields["d"],"67 CE")
        self.assertFalse(flags)

    def test_duplicate_labels_fail_closed(self):
        self.assertIn("duplicate_field_label",split_fields("O: one O: two")[1])

    def test_explicit_ocr_label_recovery_keeps_raw_form(self):
        for label in ("0:","():"):
            fields,flags=split_fields("1. "+label+" RAW Ds: x F: x S: x E: — D: 67 CE")
            self.assertEqual(fields["o"],"RAW")
            self.assertFalse(flags)

    def test_heading_font_and_shape(self):
        self.assertTrue(is_heading({"ends_italic":True,"text":"RAW - Synthetic"}))
        self.assertFalse(is_heading({"ends_italic":False,"text":"a passage - Synthetic"}))
        self.assertFalse(is_heading({"ends_italic":True,"text":"1. O: RAW - Synthetic"}))


if __name__=="__main__":unittest.main()
