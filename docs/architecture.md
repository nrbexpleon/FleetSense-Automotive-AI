# Architecture

1. **Domain:** telemetry contracts, data quality, contextual cohorts, baselines, anomaly detection, correlation, prioritization, rollout feedback and evidence.
2. **Ingestion:** JSON and CSV adapters normalize source data into domain records.
3. **Application:** bounded campaign execution, report retention and comparison.
4. **Delivery:** standard-library CLI, loopback HTTP API and browser dashboard.
5. **Future adapters:** SmartVehicle, BatteryIQ, RustGuard, TSN, MQTT, Kafka, Parquet, OTA systems and data lakes.

The analytical domain has no database, cloud, web-framework or ML-library dependency. Accelerated implementations must preserve contracts and pass deterministic fixtures.
