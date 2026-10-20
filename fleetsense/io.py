from __future__ import annotations
import csv,json
from pathlib import Path
from .models import FleetDataset,TelemetryRecord

def dataset_from_dict(payload:dict)->FleetDataset:
    records=tuple(TelemetryRecord(str(row["vehicle_id"]),int(row["timestamp_ms"]),str(row["software_version"]),str(row["variant"]),str(row["region"]),float(row["mileage_km"]),float(row["ambient_c"]),{str(k):float(v) for k,v in row["values"].items()},str(row.get("trip_id","default")),dict(row.get("validity",{})),str(row.get("source","vehicle")),dict(row.get("metadata",{}))) for row in payload["records"]);return FleetDataset(str(payload.get("name","dataset")),str(payload.get("version","0")),records)
def load_json_dataset(path:str|Path)->FleetDataset:return dataset_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
def load_csv_dataset(path:str|Path,name="csv-fleet",version="0")->FleetDataset:
    records=[]
    with Path(path).open(newline="",encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            identity={key:row.pop(key) for key in ["vehicle_id","timestamp_ms","software_version","variant","region","mileage_km","ambient_c","trip_id"]};records.append(TelemetryRecord(identity["vehicle_id"],int(identity["timestamp_ms"]),identity["software_version"],identity["variant"],identity["region"],float(identity["mileage_km"]),float(identity["ambient_c"]),{key:float(value) for key,value in row.items() if value!=""},identity["trip_id"]))
    return FleetDataset(name,version,tuple(records))
