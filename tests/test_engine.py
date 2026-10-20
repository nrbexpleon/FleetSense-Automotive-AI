from datetime import datetime, timezone
import unittest
from fleetsense.engine import FleetSenseEngine
from fleetsense.models import Telemetry
from fleetsense.synthetic import generate_fleet

def sample(vin="TEST001", **overrides):
    values=dict(vin=vin,timestamp=datetime(2026,10,20,tzinfo=timezone.utc),odometer_km=50000,speed_kph=60,coolant_temp_c=92,battery_voltage_v=12.7,oil_pressure_kpa=260,vibration_rms_g=.25,dtc_count=0,days_since_service=90); values.update(overrides); return Telemetry(**values)

class EngineTests(unittest.TestCase):
    def test_healthy_is_low(self):
        r=FleetSenseEngine().ingest(sample()); self.assertEqual("low",r.severity); self.assertEqual(0.0,r.risk_score)
    def test_critical_is_explained(self):
        r=FleetSenseEngine().ingest(sample(coolant_temp_c=120,battery_voltage_v=11.2,oil_pressure_kpa=100,vibration_rms_g=1.2,dtc_count=3,days_since_service=400)); self.assertEqual("critical",r.severity); self.assertEqual(100.0,r.risk_score); self.assertIn("COOLANT_HIGH",{d.code for d in r.drivers})
    def test_out_of_order_rejected(self):
        e=FleetSenseEngine(); e.ingest(sample(timestamp=datetime(2026,10,21,tzinfo=timezone.utc)))
        with self.assertRaisesRegex(ValueError,"older"): e.ingest(sample())
    def test_fleet_ranked(self):
        e=FleetSenseEngine(); e.ingest(sample("GOOD001")); e.ingest(sample("BAD001",coolant_temp_c=120)); s=e.fleet_summary(); self.assertEqual(2,s["vehicle_count"]); self.assertEqual("BAD001",s["maintenance_queue"][0]["vin"])
    def test_synthetic_deterministic(self): self.assertEqual(generate_fleet(3,2,7),generate_fleet(3,2,7))
    def test_validation(self):
        with self.assertRaises(ValueError): sample(speed_kph=400)
    def test_timestamp_serialisation(self): self.assertTrue(sample().to_dict()["timestamp"].endswith("Z"))
    def test_cohort_anomaly(self):
        e=FleetSenseEngine()
        for i in range(5): e.ingest(sample(f"CAR{i:03d}",coolant_temp_c=90+i*.1))
        r=e.ingest(sample("OUTLIER",coolant_temp_c=104)); self.assertIn("COHORT_ANOMALY",{d.code for d in r.drivers})
if __name__=="__main__": unittest.main()
