from __future__ import annotations

def compare_reports(baseline:dict,candidate:dict)->dict:
    before={(x["software_version"],x["variant"],x["signal_id"]):x for x in baseline["hypotheses"]};after={(x["software_version"],x["variant"],x["signal_id"]):x for x in candidate["hypotheses"]};keys=set(before)|set(after)
    return {"baseline_run_id":baseline["run_id"],"candidate_run_id":candidate["run_id"],"finding_count_delta":candidate["finding_count"]-baseline["finding_count"],"quality_score_delta":candidate["quality"]["score"]-baseline["quality"]["score"],"decision_changed":baseline["decision"]!=candidate["decision"],"cohort_changes":[{"software_version":key[0],"variant":key[1],"signal_id":key[2],"affected_vehicle_delta":after.get(key,{}).get("affected_vehicles",0)-before.get(key,{}).get("affected_vehicles",0),"finding_delta":after.get(key,{}).get("finding_count",0)-before.get(key,{}).get("finding_count",0)} for key in sorted(keys)]}
