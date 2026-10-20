from __future__ import annotations
from collections import defaultdict

def evaluate_rollout(findings:list[dict],control_version:str,candidate_version:str,vehicle_versions:dict[str,str],policy:dict|None=None)->dict:
    policy={"pause_rate_ratio":3.0,"minimum_candidate_findings":3,"critical_findings_to_rollback":2,**(policy or {})};vehicles=defaultdict(set);counts=defaultdict(int);critical=defaultdict(int)
    for vehicle,version in vehicle_versions.items():vehicles[version].add(vehicle)
    for finding in findings:counts[finding["software_version"]]+=1;critical[finding["software_version"]]+=int(finding["severity"]=="critical")
    control_rate=counts[control_version]/max(1,len(vehicles[control_version]));candidate_rate=counts[candidate_version]/max(1,len(vehicles[candidate_version]));ratio=candidate_rate/max(control_rate,1e-9)
    if critical[candidate_version]>=policy["critical_findings_to_rollback"]:recommendation="rollback"
    elif counts[candidate_version]>=policy["minimum_candidate_findings"] and ratio>=policy["pause_rate_ratio"]:recommendation="pause-and-investigate"
    else:recommendation="continue-with-monitoring"
    return {"control_version":control_version,"candidate_version":candidate_version,"control_vehicles":len(vehicles[control_version]),"candidate_vehicles":len(vehicles[candidate_version]),"control_finding_rate":control_rate,"candidate_finding_rate":candidate_rate,"rate_ratio":ratio,"candidate_critical_findings":critical[candidate_version],"recommendation":recommendation,"human_approval_required":True}
