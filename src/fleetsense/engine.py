"""Deterministic and explainable fleet-health analytics."""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from statistics import median
from threading import RLock
from typing import Iterable
from .models import Assessment, RiskDriver, Telemetry


@dataclass(frozen=True)
class Thresholds:
    coolant_warning_c: float = 105.0
    coolant_critical_c: float = 115.0
    battery_low_v: float = 12.0
    battery_critical_v: float = 11.5
    oil_low_kpa: float = 170.0
    oil_critical_kpa: float = 120.0
    vibration_warning_g: float = 0.65
    vibration_critical_g: float = 1.0
    service_warning_days: int = 180
    service_critical_days: int = 365


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _band(value: float, warning: float, critical: float, points: float, inverse: bool = False) -> float:
    if inverse:
        if value >= warning: return 0.0
        if value <= critical: return points
        return points * (warning - value) / (warning - critical)
    if value <= warning: return 0.0
    if value >= critical: return points
    return points * (value - warning) / (critical - warning)


class FleetSenseEngine:
    """Thread-safe in-memory engine suitable for an MVP or edge-side demo."""
    def __init__(self, history_size: int = 100, thresholds: Thresholds | None = None):
        if history_size < 5: raise ValueError("history_size must be >= 5")
        self.thresholds = thresholds or Thresholds()
        self._history: dict[str, deque[Telemetry]] = defaultdict(lambda: deque(maxlen=history_size))
        self._latest: dict[str, Assessment] = {}
        self._lock = RLock()

    def ingest(self, sample: Telemetry) -> Assessment:
        with self._lock:
            history = self._history[sample.vin]
            if history and sample.timestamp < history[-1].timestamp:
                raise ValueError("telemetry timestamp is older than the latest sample for this VIN")
            history.append(sample)
            assessment = self._assess(sample)
            self._latest[sample.vin] = assessment
            return assessment

    def ingest_many(self, samples: Iterable[Telemetry]) -> list[Assessment]:
        return [self.ingest(sample) for sample in samples]

    def get(self, vin: str) -> Assessment | None:
        with self._lock: return self._latest.get(vin.strip().upper())

    def _robust_z(self, value: float, name: str) -> float:
        values = [float(getattr(h[-1], name)) for h in self._history.values() if h]
        if len(values) < 5: return 0.0
        centre = median(values)
        mad = median(abs(item - centre) for item in values)
        return 0.0 if mad < 1e-9 else 0.6745 * (value - centre) / mad

    def _assess(self, s: Telemetry) -> Assessment:
        t = self.thresholds
        components = [
            ("COOLANT_HIGH", _band(s.coolant_temp_c, t.coolant_warning_c, t.coolant_critical_c, 25), f"coolant {s.coolant_temp_c:.1f} C"),
            ("BATTERY_LOW", _band(s.battery_voltage_v, t.battery_low_v, t.battery_critical_v, 15, True), f"battery {s.battery_voltage_v:.2f} V"),
            ("OIL_PRESSURE_LOW", _band(s.oil_pressure_kpa, t.oil_low_kpa, t.oil_critical_kpa, 25, True), f"oil pressure {s.oil_pressure_kpa:.1f} kPa"),
            ("VIBRATION_HIGH", _band(s.vibration_rms_g, t.vibration_warning_g, t.vibration_critical_g, 15), f"vibration RMS {s.vibration_rms_g:.3f} g"),
            ("DTC_PRESENT", min(s.dtc_count * 5.0, 15.0), f"{s.dtc_count} diagnostic trouble code(s)"),
            ("SERVICE_OVERDUE", _band(float(s.days_since_service), t.service_warning_days, t.service_critical_days, 10), f"{s.days_since_service} days since service")]
        zs = {name: round(self._robust_z(float(getattr(s, name)), name), 3) for name in ("coolant_temp_c", "battery_voltage_v", "oil_pressure_kpa", "vibration_rms_g")}
        max_z = max((abs(z) for z in zs.values()), default=0.0)
        anomaly_points = _clamp((max_z - 3.5) * 2.0, 0.0, 10.0)
        if anomaly_points: components.append(("COHORT_ANOMALY", anomaly_points, f"maximum robust cohort z-score {max_z:.2f}"))
        score = round(_clamp(sum(points for _, points, _ in components)), 1)
        drivers = tuple(RiskDriver(code, round(points, 1), observation) for code, points, observation in sorted(components, key=lambda i: i[1], reverse=True) if points > 0)
        if score >= 75: severity, action = "critical", "Stop and inspect as soon as safely possible; run OEM diagnostics."
        elif score >= 50: severity, action = "high", "Prioritise workshop inspection within 24 hours."
        elif score >= 25: severity, action = "medium", "Schedule inspection at the next available maintenance window."
        else: severity, action = "low", "Continue monitoring; follow the normal maintenance plan."
        sample_count, cohort_size = len(self._history[s.vin]), len(self._history)
        confidence = round(min(.95, .45 + min(sample_count, 20)*.02 + min(cohort_size, 20)*.01), 2)
        evidence = {"sample_count_for_vehicle": sample_count, "cohort_vehicle_count": cohort_size, "cohort_robust_z_scores": zs, "input": s.to_dict()}
        return Assessment(s.vin, s.timestamp, score, severity, confidence, action, drivers, evidence)

    def fleet_summary(self) -> dict:
        with self._lock:
            ranked = sorted(self._latest.values(), key=lambda i: (-i.risk_score, i.vin))
            counts = {name: 0 for name in ("critical", "high", "medium", "low")}
            for item in ranked: counts[item.severity] += 1
            average = round(sum(i.risk_score for i in ranked)/len(ranked), 1) if ranked else 0.0
            return {"vehicle_count": len(ranked), "average_risk_score": average, "severity_counts": counts,
                    "maintenance_queue": [i.to_dict() for i in ranked],
                    "disclaimer": "Fleet ranking is maintenance triage, not proof of failure or root cause."}
