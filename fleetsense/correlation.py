from __future__ import annotations
from collections import defaultdict

def correlate(findings:list[dict],total_vehicles:int)->list[dict]:
    groups=defaultdict(list)
    for finding in findings:groups[(finding["software_version"],finding["variant"],finding["signal_id"])].append(finding)
    hypotheses=[]
    for (version,variant,signal),items in groups.items():
        vehicles={item["vehicle_id"] for item in items};affected=len(vehicles);fraction=affected/total_vehicles if total_vehicles else 0;max_score=max(item["score"] for item in items);confidence=min(.99,.25+.08*affected+.05*min(len(items),5));hypotheses.append({"software_version":version,"variant":variant,"signal_id":signal,"affected_vehicles":affected,"affected_fleet_fraction":fraction,"finding_count":len(items),"maximum_score":max_score,"confidence":confidence,"hypothesis":f"{signal} anomalies are concentrated in software {version}, variant {variant}"})
    return sorted(hypotheses,key=lambda value:(value["affected_vehicles"],value["finding_count"]),reverse=True)
