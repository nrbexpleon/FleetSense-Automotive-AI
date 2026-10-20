from __future__ import annotations
from dataclasses import dataclass, field
from math import isfinite
from typing import Any

@dataclass(frozen=True)
class SignalDefinition:
    id: str
    unit: str
    minimum: float
    maximum: float
    freshness_ms: int
    safety_relevant: bool = False
    def validate(self,value:float)->None:
        if not self.id or not self.unit:raise ValueError("signal id and unit required")
        if not isfinite(value):raise ValueError(f"{self.id} value must be finite")
        if not self.minimum<=value<=self.maximum:raise ValueError(f"{self.id} outside range")
        if self.freshness_ms<1:raise ValueError("freshness_ms must be positive")

@dataclass(frozen=True)
class TelemetryRecord:
    vehicle_id:str
    timestamp_ms:int
    software_version:str
    variant:str
    region:str
    mileage_km:float
    ambient_c:float
    values:dict[str,float]
    trip_id:str="default"
    validity:dict[str,str]=field(default_factory=dict)
    source:str="vehicle"
    metadata:dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True)
class FleetDataset:
    name:str
    version:str
    records:tuple[TelemetryRecord,...]
    def validate(self,catalogue:dict[str,SignalDefinition])->None:
        if not self.name or not self.version:raise ValueError("dataset identity required")
        if not 2<=len(self.records)<=2_000_000:raise ValueError("dataset requires 2..2000000 records")
        previous={};seen=set()
        for record in self.records:
            identity=(record.vehicle_id,record.timestamp_ms,record.source)
            if identity in seen:raise ValueError("duplicate telemetry record")
            seen.add(identity)
            if not all([record.vehicle_id,record.software_version,record.variant,record.region]):raise ValueError("record identity required")
            if record.timestamp_ms<0 or record.timestamp_ms<=previous.get(record.vehicle_id,-1):raise ValueError("vehicle timestamps must strictly increase")
            previous[record.vehicle_id]=record.timestamp_ms
            if record.mileage_km<0 or not isfinite(record.ambient_c):raise ValueError("invalid operating context")
            if not record.values:raise ValueError("signal values required")
            for signal_id,value in record.values.items():
                if signal_id not in catalogue:raise ValueError(f"unknown signal {signal_id}")
                catalogue[signal_id].validate(value)
                if record.validity.get(signal_id,"valid") not in {"valid","stale","invalid","unavailable"}:raise ValueError("invalid validity")
