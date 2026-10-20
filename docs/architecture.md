# Architecture and scoring

The MVP is deterministic, auditable, dependency-free and safe to demonstrate offline. Every score is the sum of visible rule contributions, capped at 100.

| Signal | Warning | Critical | Maximum points |
|---|---:|---:|---:|
| Coolant temperature | 105 C | 115 C | 25 |
| Battery voltage (low) | 12.0 V | 11.5 V | 15 |
| Oil pressure (low) | 170 kPa | 120 kPa | 25 |
| Vibration RMS | 0.65 g | 1.0 g | 15 |
| DTC count | 1 | 3 | 15 |
| Days since service | 180 days | 365 days | 10 |
| Cohort anomaly | robust abs(z) > 3.5 | scaled | 10 |

These are demonstration defaults, not universal OEM limits. Calibrate by vehicle platform, powertrain and validated engineering data. Severity bands are low `<25`, medium `25–49.9`, high `50–74.9`, and critical `>=75`. Confidence reflects evidence volume only; it is not a calibrated probability of failure.

## Boundaries

- In-memory state is intentional; production requires durable storage, identity, authorisation and observability.
- Put the API behind TLS, an authenticated gateway and rate limiting.
- VINs may be sensitive operational data; apply retention and access controls.
- Signals can correlate but do not establish causation.
- Never connect recommendations directly to actuation.
