"""Deterministic synthetic telemetry for demos and tests."""
import random
from datetime import datetime, timedelta, timezone
from .models import Telemetry

def generate_fleet(vehicles: int = 12, samples: int = 20, seed: int = 42) -> list[Telemetry]:
    if vehicles < 1 or samples < 1: raise ValueError("vehicles and samples must be >= 1")
    rng, result = random.Random(seed), []
    start = datetime(2026, 10, 20, 8, 0, tzinfo=timezone.utc)
    for step in range(samples):
        for index in range(vehicles):
            d = step / max(samples - 1, 1)
            at_risk = index in {0, 3}
            result.append(Telemetry(vin=f"FLEET{index+1:04d}", timestamp=start+timedelta(minutes=5*step),
                odometer_km=30000+index*4000+step*6, speed_kph=max(0.0, rng.gauss(65,12)),
                coolant_temp_c=rng.gauss(92+(22*d if index==0 else 0),1.8),
                battery_voltage_v=rng.gauss(12.7-(1.0*d if index==3 else 0),.08),
                oil_pressure_kpa=rng.gauss(260-(145*d if index==0 else 0),8),
                vibration_rms_g=max(.05,rng.gauss(.3+(.65*d if index==3 else 0),.04)),
                dtc_count=2 if at_risk and d>.75 else 0, days_since_service=60+index*11+step))
    return result
