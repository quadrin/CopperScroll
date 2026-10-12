#!/usr/bin/env python3
"""Failure-oriented tests for datum/count/phase transfer and reproducibility."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('entry46_alternatives',HERE/'evaluate.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


class Alternatives(unittest.TestCase):
    def metric(self, **change):
        # Synthetic fixture, never ancient evidence or a selected cubit value.
        d = dict(phase_join=E.M,left_origin=E.M,datum_identified=E.M,
                 kind='entrance-to-target-horizontal',unit_source='fixture',target_source='fixture',
                 unit_interval_m=[0.5,0.5],measured_interval_m=[5,5],tolerance_m=0.1)
        return dict(d,**change)

    def test_horizontal_and_vertical_are_distinct(self):
        self.assertEqual(E.numeric(self.metric(),'ten-cubits-distance'),E.M)
        self.assertEqual(E.numeric(self.metric(),'ten-cubits-depth'),E.U)
        vertical=self.metric(kind='ancient-datum-to-target-vertical')
        self.assertEqual(E.numeric(vertical,'ten-cubits-depth'),E.M)
        self.assertEqual(E.numeric(vertical,'ten-cubits-distance'),E.U)

    def test_basin_depth_and_excavation_reach_are_not_deposit_depth(self):
        for kind in ('basin-depth','shaft-height','excavation-reach','modern-surface-to-floor'):
            self.assertEqual(E.numeric(self.metric(kind=kind),'ten-cubits-depth'),E.U)

    def test_unknown_datum_phase_and_unit_stay_unknown(self):
        for k,v in [('datum_identified',E.U),('phase_join',E.U),('left_origin',E.U),
                    ('unit_source',''),('target_source',''),('unit_interval_m',None)]:
            self.assertEqual(E.numeric(self.metric(**{k:v}),'ten-cubits-distance'),E.U)

    def test_metric_interval_boundaries(self):
        self.assertEqual(E.numeric(self.metric(measured_interval_m=[6,6.2]),'ten-cubits-distance'),E.F)
        self.assertEqual(E.numeric(self.metric(measured_interval_m=[4.8,5]),'ten-cubits-distance'),E.U)

    def test_ten_pits_requires_complete_distinct_same_phase_set(self):
        d=dict(phase_join=E.M,left_origin=E.M,kind='left-side-pit-set',count_complete=True,
               members_small_pits=E.M,distinct_count=10)
        self.assertEqual(E.numeric(d,'ten-small-pits'),E.M)
        self.assertEqual(E.numeric(dict(d,distinct_count=2),'ten-small-pits'),E.F)
        self.assertEqual(E.numeric(dict(d,count_complete=False,distinct_count=2),'ten-small-pits'),E.U)
        self.assertEqual(E.numeric(dict(d,members_small_pits=E.U),'ten-small-pits'),E.U)
        self.assertEqual(E.numeric(self.metric(),'ten-small-pits'),E.U)

    def test_source_total_does_not_supply_ten_pits(self):
        r=dict(row_uid='fixture',site_name='Fixture',series='Fixture',volume='1',year='1',pages='1',url='fixture',
               source_file='fixture',report_group='fixture',site_id='fixture',feature_type='rockcut_installation',
               feature_subtype='ten quarrying areas and one hewn pit',quote='',lat='31.74',lon='35.219',precision_m='1',
               n_features='10',period_as_given='area pottery Early Roman',dated_in_window='yes')
        r.update(map_ref_as_given='',crs_used='',easting_m='',northing_m='')
        p=E.pit_record(r)
        self.assertEqual(p['original_n_features'],'10')
        self.assertEqual(p['reported_pit_count_phrases'],'one hewn pit')
        self.assertEqual(p['configuration_in_window'],E.U)
        self.assertEqual(p['numerical_target'],E.U)

    def test_same_measurement_opportunity_for_control_and_candidate(self):
        r=dict(phase_id='fixture',origin_row='fixture',lat='31.74',lon='35.219',precision_m='1',
               contained_water=E.M,storage_use=E.U,reported_contained_water=E.M,
               entrance=E.M,same_phase=E.M,configuration_in_window=E.M,reported_window=E.M)
        scores=E.evaluate([('pool','contained-water',r),('pool','contained-water',dict(r,phase_id='control'))],
                          {'fixture':(31.74,35.219)}, {})
        a=[s for s in scores if s['phase_id']=='fixture']
        b=[s for s in scores if s['phase_id']=='control']
        self.assertEqual([{k:v for k,v in s.items() if k!='phase_id'} for s in a],
                         [{k:v for k,v in s.items() if k!='phase_id'} for s in b])
        self.assertTrue(all(s['full_branch']==E.U for s in scores))

    def test_coordinate_envelope(self):
        self.assertEqual(E.place(dict(lat='',lon='',precision_m=''),(31.74,35.219),1),E.U)
        self.assertEqual(E.place(dict(lat='31.74',lon='35.219',precision_m='5'),(31.74,35.219),1),E.M)
        self.assertEqual(E.place(dict(lat='31.74',lon='35.219',precision_m='2000'),(31.74,35.219),1),E.U)

    def test_report_range_endpoints_and_old_grid_scale(self):
        self.assertEqual(E.axis_range('220793–1134','220793'),(220793,221134,1))
        self.assertEqual(E.axis_range('214734–7272','214734'),(214734,217272,1))
        self.assertEqual(E.axis_range('1672—4','167200'),(167200,167400,100))
        self.assertIsNone(E.axis_range('1672—4',''))

    def test_unresolved_range_cannot_use_old_point(self):
        r=dict(lat='31.74',lon='35.219',precision_m='1',map_ref_as_given='214734–7272/630785–1313',
               crs_used='UNKNOWN',easting_m='214734',northing_m='630785')
        p=E.position_envelope(r)
        self.assertEqual(p['lat'],'')
        self.assertEqual(E.place(p,(31.74,35.219),2),E.U)

    def test_native_feature_measurements_supply_no_deposit_target(self):
        import json
        n=json.loads((HERE/'numerical_observations.json').read_text())
        self.assertEqual(n['observations'],[])
        self.assertTrue(all(o.get('deposit_target_observed') is not True for o in n['source_measurements']))
        self.assertFalse(next(o for o in n['source_measurements'] if o['id']=='RR-census')['count_complete'])

    def test_committed_results_reproduce(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            E.main(tmp)
            for name in ('pit_source_records.csv.gz','scores.csv.gz','counts.csv','pit_followup.csv',
                         'pit_morphology_shortlist.csv','audited_bath_scores.csv','reading_branches.csv',
                         'position_corrections.csv.gz','summary.json'):
                self.assertEqual((Path(tmp)/name).read_bytes(),(HERE/name).read_bytes(),name)


if __name__=='__main__':
    unittest.main()
