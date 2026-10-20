from __future__ import annotations
from collections import Counter,defaultdict
from .models import FleetDataset,SignalDefinition

class DataQualityAnalyzer:
    def analyze(self,dataset:FleetDataset,catalogue:dict[str,SignalDefinition])->dict:
        findings=[];last_value={};last_change={};intervals=defaultdict(list);last_time={};validity=Counter();signal_counts=Counter()
        for record in dataset.records:
            for signal_id,definition in catalogue.items():
                status=record.validity.get(signal_id,"unavailable" if signal_id not in record.values else "valid");validity[status]+=1
                if signal_id not in record.values:
                    findings.append(finding(record.vehicle_id,record.timestamp_ms,signal_id,"missing","medium"));continue
                signal_counts[signal_id]+=1;key=(record.vehicle_id,signal_id);value=record.values[signal_id]
                if key in last_time:
                    interval=record.timestamp_ms-last_time[key];intervals[key].append(interval)
                    if interval>definition.freshness_ms:findings.append(finding(record.vehicle_id,record.timestamp_ms,signal_id,"freshness-gap","high" if definition.safety_relevant else "medium",{"gap_ms":interval,"limit_ms":definition.freshness_ms}))
                if key not in last_value or last_value[key]!=value:last_change[key]=record.timestamp_ms
                elif record.timestamp_ms-last_change.get(key,record.timestamp_ms)>definition.freshness_ms*5:findings.append(finding(record.vehicle_id,record.timestamp_ms,signal_id,"flatline","high" if definition.safety_relevant else "medium"))
                if status in {"stale","invalid"}:findings.append(finding(record.vehicle_id,record.timestamp_ms,signal_id,f"validity-{status}","high"))
                last_value[key]=value;last_time[key]=record.timestamp_ms
        total_slots=len(dataset.records)*len(catalogue);completeness=sum(signal_counts.values())/total_slots if total_slots else 0;valid_count=validity["valid"]
        return {"score":round(max(0.0,100*(.6*completeness+.4*(valid_count/total_slots if total_slots else 0))-min(40,len(findings)*.05)),2),"completeness":completeness,"validity_counts":dict(validity),"finding_count":len(findings),"findings":findings}

def finding(vehicle_id,timestamp_ms,signal_id,kind,severity,detail=None):return {"vehicle_id":vehicle_id,"timestamp_ms":timestamp_ms,"signal_id":signal_id,"type":kind,"severity":severity,"detail":detail or {}}
