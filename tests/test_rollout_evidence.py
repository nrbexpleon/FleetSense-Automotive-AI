import unittest
from fleetsense.comparison import compare_reports
from fleetsense.evidence import create_evidence,sign_evidence,verify_evidence,verify_signed_evidence
from fleetsense.prioritization import rank_hypotheses
from fleetsense.rollout import evaluate_rollout

class RolloutEvidenceTests(unittest.TestCase):
 def test_continue_recommendation(self):self.assertEqual(evaluate_rollout([], 'a','b',{'v1':'a','v2':'b'})['recommendation'],'continue-with-monitoring')
 def test_pause_recommendation(self):
  findings=[{'vehicle_id':'v2','software_version':'b','severity':'high'} for _ in range(3)];self.assertEqual(evaluate_rollout(findings,'a','b',{'v1':'a','v2':'b'})['recommendation'],'pause-and-investigate')
 def test_rollback_recommendation(self):
  findings=[{'vehicle_id':'v2','software_version':'b','severity':'critical'} for _ in range(2)];self.assertEqual(evaluate_rollout(findings,'a','b',{'v1':'a','v2':'b'})['recommendation'],'rollback')
 def test_rollout_requires_human(self):self.assertTrue(evaluate_rollout([], 'a','b',{})['human_approval_required'])
 def test_priority_order(self):
  values=[{'maximum_score':4,'affected_fleet_fraction':.1,'finding_count':2,'confidence':.5},{'maximum_score':8,'affected_fleet_fraction':.2,'finding_count':5,'confidence':.8}];self.assertGreater(rank_hypotheses(values)[0]['priority_score'],rank_hypotheses(values)[1]['priority_score'])
 def test_evidence_verifies(self):self.assertTrue(verify_evidence(create_evidence({'x':1})))
 def test_evidence_tamper_fails(self):
  evidence=create_evidence({'x':1});evidence['report']['x']=2;self.assertFalse(verify_evidence(evidence))
 def test_signed_evidence_verifies(self):
  key=b'x'*32;self.assertTrue(verify_signed_evidence(sign_evidence(create_evidence({'x':1}),key),key))
 def test_short_key_rejected(self):
  with self.assertRaises(ValueError):sign_evidence(create_evidence({}),b'short')
 def test_comparison(self):
  a={'run_id':'a','finding_count':1,'quality':{'score':90},'decision':'x','hypotheses':[]};b={'run_id':'b','finding_count':3,'quality':{'score':80},'decision':'y','hypotheses':[]};result=compare_reports(a,b);self.assertEqual(result['finding_count_delta'],2);self.assertTrue(result['decision_changed'])

if __name__=='__main__':unittest.main()
