import unittest
from combine_pilot import combine,form_id,normalize


def fixture():
    pilot=[dict(record_id="r1",printed="1",viewer="28",column="left",D_lower="10",D_upper="10"),
           dict(record_id="r2",printed="2",viewer="29",column="right",D_lower="20",D_upper="20")]
    raw=[dict(record_id=r["record_id"],fields_raw={"s":"Independent source"},parser_flags=[]) for r in pilot]
    val=[dict(record_id=r["record_id"],status="accepted",greek_forms=["Βάβ"],source_independent=True,image_checked=True,flags=[]) for r in pilot]
    return pilot,raw,val


class MergeTests(unittest.TestCase):
    def test_forms_and_occurrences_are_distinct_units(self):
        forms,occ,dec,audit=combine(*fixture(),expected_count=2)
        self.assertEqual((len(forms),len(occ)),(1,2))
        self.assertEqual(forms[0]["name_id"],form_id("ΒΑΒ"))
        self.assertFalse(occ[0]["heading_used_for_form_identity"])

    def test_all_statuses_required(self):
        p,r,v=fixture()
        with self.assertRaises(ValueError):combine(p,r,v[:1],expected_count=2)

    def test_duplicate_validation_rejected(self):
        p,r,v=fixture()
        with self.assertRaises(ValueError):combine(p,r,v+[v[0]],expected_count=2)

    def test_extra_validation_rejected(self):
        p,r,v=fixture();v.append(dict(v[0],record_id="extra"))
        with self.assertRaises(ValueError):combine(p,r,v,expected_count=2)

    def test_flagged_unknown_not_a_form(self):
        p,r,v=fixture();v[0]["flags"]=["restored"]
        _,occ,dec,audit=combine(p,r,v,expected_count=2)
        self.assertEqual(len(occ),1);self.assertEqual(dec[0]["effective_status"],"unknown")

    def test_target_derived_excluded(self):
        p,r,v=fixture();r[0]["fields_raw"]["s"]="3Q15 DJD III"
        _,occ,dec,_=combine(p,r,v,expected_count=2)
        self.assertEqual(len(occ),1);self.assertEqual(dec[0]["effective_status"],"excluded")

    def test_unverified_source_or_image_unknown(self):
        p,r,v=fixture();v[0]["source_independent"]=None;v[1]["image_checked"]=False
        _,occ,_,_=combine(p,r,v,expected_count=2);self.assertFalse(occ)

    def test_normalization_never_repairs_restoration(self):
        for text in ("Β[Α]Β","Latin","ᾳ"):
            with self.assertRaises(ValueError):normalize(text)

    def test_source_page_mismatch_rejected(self):
        p,r,v=fixture();v[0]["source_page"]=99
        with self.assertRaises(ValueError):combine(p,r,v,expected_count=2)


if __name__=="__main__":unittest.main()
