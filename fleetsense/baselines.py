from __future__ import annotations
from collections import defaultdict
from .models import FleetDataset
from .statistics import mad,mean,percentile,stdev

def cohort_key(record)->str:
    ambient_band="cold" if record.ambient_c<5 else "hot" if record.ambient_c>35 else "temperate"
    mileage_band="new" if record.mileage_km<10_000 else "high-mileage" if record.mileage_km>=100_000 else "mature"
    return f"{record.variant}|{record.software_version}|{record.region}|{ambient_band}|{mileage_band}"

def build_baselines(dataset:FleetDataset)->dict[str,dict[str,dict[str,float]]]:
    groups=defaultdict(lambda:defaultdict(list))
    for record in dataset.records:
        for signal_id,value in record.values.items():groups[cohort_key(record)][signal_id].append(value)
    output={}
    for cohort,signals in groups.items():
        output[cohort]={}
        for signal_id,values in signals.items():
            output[cohort][signal_id]={"count":float(len(values)),"mean":mean(values),"stdev":stdev(values),"median":percentile(values,.5),"mad":mad(values),"p05":percentile(values,.05),"p95":percentile(values,.95),"minimum":min(values),"maximum":max(values)}
    return output
