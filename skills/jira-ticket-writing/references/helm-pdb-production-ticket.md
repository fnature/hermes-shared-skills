# Helm chart PDB production-readiness ticket notes

Use these notes when drafting Jira tickets about adding PodDisruptionBudget support to a reusable Helm chart.

## Recommended implementation tasks

- Add a dedicated PDB Helm template, separate from the Deployment template.
- Render the PDB only for Deployment workloads; do not render it for Jobs.
- Select Deployment Pods via the chart's existing selector labels.
- Add default values similar to:

```yaml
replicaCount: 2

deployment:
  strategyType: RollingUpdate
  rollingUpdate:
    maxUnavailable: 25%
    maxSurge: 25%

podDisruptionBudget:
  enabled: true
  maxUnavailable: 1
```

- Define `deployment.rollingUpdate.maxUnavailable` and `deployment.rollingUpdate.maxSurge` by default when making `RollingUpdate` the default strategy.
- If HPA/autoscaling is supported, consider aligning `autoscaling.minReplicas` to `2` so autoscaling does not reduce the workload to a single replica.
- Acceptance criteria should include Helm render validation and a brief README/update note.
