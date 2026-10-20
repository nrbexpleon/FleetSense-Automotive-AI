# OTA feedback governance

FleetSense compares findings per vehicle in a candidate software cohort against a control cohort. The reference policy recommends:

- **continue-with-monitoring** when no stop condition is met;
- **pause-and-investigate** when candidate finding rate is at least 3.0× control with at least 3 candidate findings;
- **rollback** when at least 2 candidate critical findings are present.

These are demonstration thresholds. Every recommendation carries `human_approval_required: true`. Production use requires rollout-ring context, exposure normalization, minimum observation windows, safety and cybersecurity review, and integration with an independently controlled OTA platform.
