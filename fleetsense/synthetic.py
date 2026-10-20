from __future__ import annotations
import random
from .models import FleetDataset,TelemetryRecord

def generate_fleet(vehicle_count:int=1000,samples_per_vehicle:int=20,seed:int=42)->FleetDataset:
    if not 2<=vehicle_count<=20_000 or not 5<=samples_per_vehicle<=10_000:raise ValueError("synthetic dimensions out of range")
    randomizer=random.Random(seed);records=[]
    for vehicle_index in range(vehicle_count):
        candidate=vehicle_index>=int(vehicle_count*.7);version="3.4.1" if candidate else "3.4.0";variant=["base","long-range","performance"][vehicle_index%3];region=["EU","NA","APAC"][vehicle_index%3];anomalous=candidate and variant=="performance";ambient=20+(vehicle_index%4)*7;mileage=5000+vehicle_index*150
        for sample_index in range(samples_per_vehicle):
            thermal_rise=18 if anomalous and sample_index>=samples_per_vehicle//2 else 0;vibration_rise=.65 if anomalous and sample_index>=samples_per_vehicle//2 else 0;latency_rise=30 if candidate and sample_index%7==0 else 0
            records.append(TelemetryRecord(f"vehicle-{vehicle_index:05d}",sample_index*1000,version,variant,region,float(mileage),float(ambient),{"Powertrain.Motor.Temperature":70+randomizer.gauss(0,1.5)+thermal_rise,"Powertrain.Motor.Vibration":1+randomizer.gauss(0,.06)+vibration_rise,"Battery.StateOfCharge":max(0,90-sample_index*.8+randomizer.gauss(0,.2)),"Network.ServiceLatency":8+randomizer.gauss(0,1)+latency_rise},f"trip-{vehicle_index}",{},"synthetic"))
    return FleetDataset("synthetic-ota-fleet","1.0",tuple(records))
