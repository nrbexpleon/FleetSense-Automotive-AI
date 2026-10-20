# FleetSense Automotive AI

FleetSense is a dependency-free Python 3.11+ MVP for explainable fleet-health monitoring. It ingests vehicle telemetry, detects robust cohort anomalies, calculates a transparent 0–100 health-risk score, prioritises maintenance, and serves results through a CLI, JSON API, and browser dashboard.

> **Engineering aid, not a safety controller.** FleetSense produces hypotheses and maintenance triage recommendations. It does not prove root cause, predict guaranteed remaining useful life, or replace OEM diagnostics, qualified personnel, or vehicle safety mechanisms.

## Capabilities

- Typed telemetry with explicit units and validation
- Rolling per-vehicle history and robust median/MAD cohort anomalies
- Explainable thermal, electrical, vibration, oil, DTC and service risk
- Severity, confidence, evidence, recommended action and risk drivers
- Fleet summary and ranked maintenance queue
- Deterministic synthetic fleet/demo data
- CSV, JSON and JSONL ingestion
- CLI, REST API, dashboard and health endpoint
- Dependency-free runtime, tests, CodeQL, CI and Dependabot

## Quick start

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m fleetsense.cli demo --vehicles 12 --samples 20
PYTHONPATH=src python -m fleetsense.cli serve --host 127.0.0.1 --port 8080
```

Open http://127.0.0.1:8080. No third-party runtime package is required.

## CLI

```bash
PYTHONPATH=src python -m fleetsense.cli demo --seed 42 --output report.json
PYTHONPATH=src python -m fleetsense.cli analyze telemetry.csv --output report.json
PYTHONPATH=src python -m fleetsense.cli serve --input telemetry.jsonl
```

Input fields: `vin,timestamp,odometer_km,speed_kph,coolant_temp_c,battery_voltage_v,oil_pressure_kpa,vibration_rms_g,dtc_count,days_since_service`.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness and version |
| POST | `/v1/telemetry` | Ingest one object or a JSON array |
| GET | `/v1/fleet` | Fleet summary and ranked vehicles |
| GET | `/v1/vehicles/{vin}` | Latest explainable assessment |
| GET | `/` | Dashboard |

## Architecture

```text
CSV / JSONL / REST -> validation -> FleetSenseEngine -> assessment -> CLI / API / dashboard
                                         |-> per-VIN history + fleet cohort
```

Risk thresholds are centralised in `src/fleetsense/engine.py`. See `docs/architecture.md` for scoring and limitations.

## Licence

Current and future versions are proprietary source-available software. Earlier versions released under MIT remain governed by that historical grant. See `LICENSE`.
