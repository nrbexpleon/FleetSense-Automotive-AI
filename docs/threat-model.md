# Threat model

| Threat | Current control | Production work |
|---|---|---|
| Malformed/oversized telemetry | strict types, identity, ranges, ordering and hard bounds | JSON Schema, streaming validation, fuzzing |
| Vehicle identity spoofing | required identity/version/variant | certificates and authenticated ingestion |
| Data poisoning | contextual baselines, visible findings, evidence hash | signed telemetry, lineage, trusted lake and poisoning tests |
| Privacy leakage | synthetic public data and no location coordinates | aggregation, pseudonyms, retention and privacy review |
| False causal claim | hypothesis wording and visible concentration evidence | controlled experiments and expert review |
| Unsafe OTA action | advisory output and human approval flag; no write API | independent OTA authorization and separation of duties |
| Evidence tampering | SHA-256 and optional HMAC | KMS/HSM digital signatures and immutable storage |
| Unauthorized API | loopback and optional token | OIDC, RBAC, tenant isolation and audit |
| Resource exhaustion | body/record/run limits | rate limits, queues and isolated workers |

Never commit VINs, production telemetry, credentials, customer inventories, private thresholds or signing keys.
