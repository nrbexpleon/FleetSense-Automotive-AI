"""Typed domain models with explicit engineering units."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


def _finite(name: str, value: float) -> float:
    value = float(value)
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError(f"{name} must be finite")
    return value


def parse_timestamp(value: str | datetime) -> datetime:
    result = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if result.tzinfo is None:
        result = result.replace(tzinfo=timezone.utc)
    return result.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class Telemetry:
    vin: str
    timestamp: datetime
    odometer_km: float
    speed_kph: float
    coolant_temp_c: float
    battery_voltage_v: float
    oil_pressure_kpa: float
    vibration_rms_g: float
    dtc_count: int
    days_since_service: int

    def __post_init__(self) -> None:
        vin = self.vin.strip().upper()
        if not 3 <= len(vin) <= 32 or not all(c.isalnum() or c in "-_" for c in vin):
            raise ValueError("vin must be 3-32 alphanumeric, '-' or '_' characters")
        object.__setattr__(self, "vin", vin)
        object.__setattr__(self, "timestamp", parse_timestamp(self.timestamp))
        for name in ("odometer_km", "speed_kph", "coolant_temp_c", "battery_voltage_v", "oil_pressure_kpa", "vibration_rms_g"):
            object.__setattr__(self, name, _finite(name, getattr(self, name)))
        if self.odometer_km < 0 or not 0 <= self.speed_kph <= 350:
            raise ValueError("odometer_km must be >= 0 and speed_kph must be 0..350")
        if not -60 <= self.coolant_temp_c <= 250 or not 0 <= self.battery_voltage_v <= 100:
            raise ValueError("temperature or voltage outside plausible bounds")
        if self.oil_pressure_kpa < 0 or self.vibration_rms_g < 0 or self.dtc_count < 0 or self.days_since_service < 0:
            raise ValueError("pressure, vibration, counts and elapsed days must be >= 0")

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Telemetry":
        return cls(vin=str(value["vin"]), timestamp=parse_timestamp(value["timestamp"]),
                   odometer_km=float(value["odometer_km"]), speed_kph=float(value["speed_kph"]),
                   coolant_temp_c=float(value["coolant_temp_c"]), battery_voltage_v=float(value["battery_voltage_v"]),
                   oil_pressure_kpa=float(value["oil_pressure_kpa"]), vibration_rms_g=float(value["vibration_rms_g"]),
                   dtc_count=int(value["dtc_count"]), days_since_service=int(value["days_since_service"]))

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["timestamp"] = self.timestamp.isoformat().replace("+00:00", "Z")
        return value


@dataclass(frozen=True, slots=True)
class RiskDriver:
    code: str
    contribution: float
    observation: str
    def to_dict(self) -> dict[str, Any]: return asdict(self)


@dataclass(frozen=True, slots=True)
class Assessment:
    vin: str
    timestamp: datetime
    risk_score: float
    severity: str
    confidence: float
    recommended_action: str
    drivers: tuple[RiskDriver, ...]
    evidence: dict[str, Any]
    disclaimer: str = "Triage hypothesis only; confirm with OEM diagnostics and qualified personnel."

    def to_dict(self) -> dict[str, Any]:
        return {"vin": self.vin, "timestamp": self.timestamp.isoformat().replace("+00:00", "Z"),
                "risk_score": self.risk_score, "severity": self.severity, "confidence": self.confidence,
                "recommended_action": self.recommended_action, "drivers": [d.to_dict() for d in self.drivers],
                "evidence": self.evidence, "disclaimer": self.disclaimer}
