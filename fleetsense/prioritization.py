from __future__ import annotations

def rank_hypotheses(hypotheses:list[dict],weights:dict|None=None)->list[dict]:
    weights={"severity":2.0,"fleet":4.0,"recurrence":1.0,"confidence":3.0,**(weights or {})};ranked=[]
    for hypothesis in hypotheses:
        severity=min(10,hypothesis["maximum_score"]);fleet=hypothesis["affected_fleet_fraction"]*10;recurrence=min(10,hypothesis["finding_count"]);confidence=hypothesis["confidence"]*10;score=weights["severity"]*severity+weights["fleet"]*fleet+weights["recurrence"]*recurrence+weights["confidence"]*confidence
        ranked.append({**hypothesis,"priority_score":round(score,3),"score_components":{"severity":severity,"fleet":fleet,"recurrence":recurrence,"confidence":confidence}})
    return sorted(ranked,key=lambda value:value["priority_score"],reverse=True)
