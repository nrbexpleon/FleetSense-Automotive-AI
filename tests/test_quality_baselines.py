import unittest
from fleetsense.baselines import build_baselines,cohort_key
from fleetsense.config import default_catalogue
from fleetsense.models import FleetDataset,TelemetryRecord
from fleetsense.quality import DataQualityAnalyzer

class QualityBaselineTests(unittest.TestCase):
 def records(self):return (TelemetryRecord('v',0,'1','base','EU',100,20,{'Powertrain.Motor.Temperature':70}),TelemetryRecord('v',1000,'1','base','EU',101,20,{'Powertrain.Motor.Temperature':71}))
 def test_cohort_key_contains_context(self):self.assertIn('base|1|EU|temperate|new',cohort_key(self.records()[0]))
 def test_baseline_builds(self):self.assertEqual(build_baselines(FleetDataset('d','1',self.records()))[cohort_key(self.records()[0])]['Powertrain.Motor.Temperature']['count'],2)
 def test_quality_reports_missing_signals(self):
  result=DataQualityAnalyzer().analyze(FleetDataset('d','1',self.records()),{s.id:s for s in default_catalogue()});self.assertGreater(result['finding_count'],0)
 def test_quality_perfect_for_complete_records(self):
  signal=default_catalogue()[0];catalogue={signal.id:signal};result=DataQualityAnalyzer().analyze(FleetDataset('d','1',self.records()),catalogue);self.assertEqual(result['score'],100)
 def test_quality_detects_gap(self):
  signal=default_catalogue()[0];catalogue={signal.id:signal};records=(self.records()[0],TelemetryRecord('v',6000,'1','base','EU',101,20,{'Powertrain.Motor.Temperature':71}));result=DataQualityAnalyzer().analyze(FleetDataset('d','1',records),catalogue);self.assertTrue(any(x['type']=='freshness-gap' for x in result['findings']))
 def test_quality_detects_invalid(self):
  signal=default_catalogue()[0];catalogue={signal.id:signal};records=(self.records()[0],TelemetryRecord('v',1000,'1','base','EU',101,20,{'Powertrain.Motor.Temperature':71},validity={signal.id:'invalid'}));result=DataQualityAnalyzer().analyze(FleetDataset('d','1',records),catalogue);self.assertTrue(any(x['type']=='validity-invalid' for x in result['findings']))

if __name__=='__main__':unittest.main()
