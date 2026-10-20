import unittest
from fleetsense.anomalies import detect_anomalies
from fleetsense.baselines import build_baselines
from fleetsense.config import default_catalogue
from fleetsense.correlation import correlate
from fleetsense.engine import FleetIntelligenceEngine
from fleetsense.synthetic import generate_fleet

class EngineSyntheticTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.dataset=generate_fleet(60,12,42);cls.engine=FleetIntelligenceEngine(default_catalogue(),3);cls.report=cls.engine.analyze(cls.dataset,{'control_version':'3.4.0','candidate_version':'3.4.1'})
 def test_synthetic_size(self):self.assertEqual(len(self.dataset.records),720)
 def test_synthetic_reproducible(self):self.assertEqual(self.dataset.records,generate_fleet(60,12,42).records)
 def test_synthetic_bounds(self):
  with self.assertRaises(ValueError):generate_fleet(1,20)
 def test_engine_vehicle_count(self):self.assertEqual(self.report['dataset']['vehicle_count'],60)
 def test_engine_versions(self):self.assertEqual(self.report['dataset']['software_versions'],['3.4.0','3.4.1'])
 def test_engine_has_quality(self):self.assertGreater(self.report['quality']['score'],0)
 def test_engine_has_findings(self):self.assertGreater(self.report['finding_count'],0)
 def test_engine_has_hypotheses(self):self.assertTrue(self.report['hypotheses'])
 def test_engine_has_priorities(self):self.assertTrue(self.report['priorities'])
 def test_engine_rollout(self):self.assertIn(self.report['rollout']['recommendation'],{'pause-and-investigate','rollback','continue-with-monitoring'})
 def test_engine_decision(self):self.assertEqual(self.report['decision'],'investigation-required')
 def test_anomaly_threshold_validation(self):
  with self.assertRaises(ValueError):FleetIntelligenceEngine(default_catalogue(),0)
 def test_detector_returns_list(self):self.assertIsInstance(detect_anomalies(self.dataset,{s.id:s for s in default_catalogue()},build_baselines(self.dataset),3),list)
 def test_correlation_empty(self):self.assertEqual(correlate([],10),[])

if __name__=='__main__':unittest.main()
