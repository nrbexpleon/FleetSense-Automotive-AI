import unittest
from fleetsense.api import DASHBOARD, make_handler
from fleetsense.engine import FleetSenseEngine
class ApiContractTests(unittest.TestCase):
    def test_handler_factory(self):
        h=make_handler(FleetSenseEngine()); self.assertTrue(hasattr(h,"do_GET")); self.assertTrue(hasattr(h,"do_POST"))
    def test_dashboard_contract(self): self.assertIn("/v1/fleet",DASHBOARD); self.assertIn("FleetSense Automotive AI",DASHBOARD)
if __name__=="__main__": unittest.main()
