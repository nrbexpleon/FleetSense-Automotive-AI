import unittest
from fleetsense.models import FleetDataset,SignalDefinition,TelemetryRecord
from fleetsense.statistics import correlation,mad,mean,percentile,stdev,variance

class ModelStatisticsTests(unittest.TestCase):
 def setUp(self):self.signal=SignalDefinition('speed','km/h',0,300,1000);self.catalogue={'speed':self.signal};self.records=(TelemetryRecord('v',0,'1','a','EU',0,20,{'speed':1}),TelemetryRecord('v',1,'1','a','EU',1,20,{'speed':2}))
 def test_signal_accepts_range(self):self.signal.validate(20)
 def test_signal_rejects_range(self):
  with self.assertRaises(ValueError):self.signal.validate(301)
 def test_signal_rejects_nan(self):
  with self.assertRaises(ValueError):self.signal.validate(float('nan'))
 def test_dataset_validates(self):FleetDataset('d','1',self.records).validate(self.catalogue)
 def test_dataset_rejects_unknown_signal(self):
  with self.assertRaises(ValueError):FleetDataset('d','1',(self.records[0],TelemetryRecord('v',1,'1','a','EU',1,20,{'x':1}))).validate(self.catalogue)
 def test_dataset_rejects_duplicate(self):
  with self.assertRaises(ValueError):FleetDataset('d','1',(self.records[0],self.records[0])).validate(self.catalogue)
 def test_dataset_rejects_order(self):
  with self.assertRaises(ValueError):FleetDataset('d','1',(self.records[0],TelemetryRecord('v',0,'1','a','EU',1,20,{'speed':2}))).validate(self.catalogue)
 def test_dataset_rejects_validity(self):
  bad=TelemetryRecord('v',1,'1','a','EU',1,20,{'speed':2},validity={'speed':'magic'})
  with self.assertRaises(ValueError):FleetDataset('d','1',(self.records[0],bad)).validate(self.catalogue)
 def test_mean(self):self.assertEqual(mean([1,2,3]),2)
 def test_variance(self):self.assertEqual(variance([1,2,3]),1)
 def test_stdev(self):self.assertEqual(stdev([1,2,3]),1)
 def test_mad(self):self.assertEqual(mad([1,2,100]),1)
 def test_percentile(self):self.assertEqual(percentile([1,2,3,4],.95),4)
 def test_correlation(self):self.assertAlmostEqual(correlation([1,2,3],[2,4,6]),1)

if __name__=='__main__':unittest.main()
