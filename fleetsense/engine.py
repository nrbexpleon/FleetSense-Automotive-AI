from __future__ import annotations
from dataclasses import asdict
from uuid import uuid4
from .anomalies import detect_anomalies
from .baselines import build_baselines
from .correlation import correlate
from .models import FleetDataset,SignalDefinition
from .prioritization import rank_hypotheses
from .quality import DataQualityAnalyzer
from .rollout import evaluate_rollout

class FleetIntelligenceEngine:
    def __init__(self,catalogue:list[SignalDefinition],anomaly_threshold:float=4.0):
        self.catalogue={signal.id:signal for signal in catalogue};self.anomaly_threshold=anomaly_threshold
        if anomaly_threshold<=0:raise ValueError("anomaly_threshold must be positive")
    def analyze(self,dataset:FleetDataset,rollout:dict|None=None)->dict:
        dataset.validate(self.catalogue);quality=DataQualityAnalyzer().analyze(dataset,self.catalogue);baselines=build_baselines(dataset);findings=detect_anomalies(dataset,self.catalogue,baselines,self.anomaly_threshold);vehicles={record.vehicle_id for record in dataset.records};hypotheses=correlate(findings,len(vehicles));priorities=rank_hypotheses(hypotheses);versions={record.vehicle_id:record.software_version for record in dataset.records};rollout_result=None
        if rollout:rollout_result=evaluate_rollout(findings,str(rollout["control_version"]),str(rollout["candidate_version"]),versions,rollout.get("policy"))
        decision="investigation-required" if priorities or quality["score"]<90 else "eligible-for-human-review"
        return {"run_id":str(uuid4()),"schema_version":"1.0","dataset":{"name":dataset.name,"version":dataset.version,"record_count":len(dataset.records),"vehicle_count":len(vehicles),"software_versions":sorted({r.software_version for r in dataset.records}),"variants":sorted({r.variant for r in dataset.records})},"catalogue":[asdict(signal) for signal in self.catalogue.values()],"quality":quality,"baselines":baselines,"findings":findings,"finding_count":len(findings),"hypotheses":hypotheses,"priorities":priorities,"rollout":rollout_result,"decision":decision}
