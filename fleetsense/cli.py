from __future__ import annotations
import argparse,json
from .config import default_catalogue
from .engine import FleetIntelligenceEngine
from .evidence import create_evidence,verify_evidence
from .io import load_json_dataset
from .synthetic import generate_fleet

def main()->int:
    parser=argparse.ArgumentParser(description="FleetSense Automotive Intelligence");parser.add_argument("--dataset");parser.add_argument("--vehicles",type=int,default=1000);parser.add_argument("--samples",type=int,default=20);args=parser.parse_args();dataset=load_json_dataset(args.dataset) if args.dataset else generate_fleet(args.vehicles,args.samples);report=FleetIntelligenceEngine(default_catalogue()).analyze(dataset,{"control_version":"3.4.0","candidate_version":"3.4.1"});evidence=create_evidence(report);print(json.dumps({"run_id":report["run_id"],"decision":report["decision"],"vehicles":report["dataset"]["vehicle_count"],"records":report["dataset"]["record_count"],"quality_score":report["quality"]["score"],"finding_count":report["finding_count"],"rollout":report["rollout"],"top_priorities":report["priorities"][:5],"evidence_valid":verify_evidence(evidence)},indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
