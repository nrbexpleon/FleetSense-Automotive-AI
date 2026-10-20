from __future__ import annotations
from .baselines import cohort_key
from .models import FleetDataset,SignalDefinition

def detect_anomalies(dataset:FleetDataset,catalogue:dict[str,SignalDefinition],baselines:dict,threshold:float=4.0)->list[dict]:
    findings=[]
    for record in dataset.records:
        cohort=cohort_key(record)
        for signal_id,value in record.values.items():
            baseline=baselines[cohort][signal_id];scale=baseline["mad"]*1.4826 or baseline["stdev"] or 1e-12;score=abs(value-baseline["median"])/scale
            if score>=threshold:
                safety=catalogue[signal_id].safety_relevant;severity="critical" if safety and score>=7 else "high" if score>=7 else "medium"
                findings.append({"id":f"{record.vehicle_id}:{signal_id}:{record.timestamp_ms}","vehicle_id":record.vehicle_id,"timestamp_ms":record.timestamp_ms,"signal_id":signal_id,"actual":value,"baseline":baseline["median"],"score":score,"severity":severity,"safety_relevant":safety,"software_version":record.software_version,"variant":record.variant,"region":record.region,"cohort":cohort})
    return findings
