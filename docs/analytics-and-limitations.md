# Analytics semantics and limitations

- Cohorts combine variant, software version, region, ambient band and mileage band.
- Baselines report median, MAD, mean, deviation, extrema and P05/P95.
- Anomalies use absolute robust Z-score with scaled MAD and standard-deviation fallback.
- Hypotheses group findings by software version, variant and signal.
- Priorities visibly combine severity, fleet exposure, recurrence and confidence.
- Quality score combines completeness/validity and deducts explicit findings.

Cohort selection can introduce confounding. Statistical concentration is not causality. Production thresholds require false-positive/false-negative studies and authorized engineering approval.
