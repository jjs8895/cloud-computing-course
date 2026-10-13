# HW3 Kubernetes Deployment Guide

## Platform
Google Kubernetes Engine (GKE), plus a local `kind` cluster

## Account Setup
- Project ID:
- Region / zone:
- Artifact Registry repository:

## Image Details
- Image name and tag:
- Base image:
- Final image size (`docker images`):
- Runs as user:

## Local Cluster (kind)
- Cluster name:
- Kubernetes version (`kubectl version`):
- Service type and URL used for testing:

## GKE Cluster
- Cluster name:
- Machine type and node count:
- Service type and external IP:

## Deployment Steps Performed
1.
2.
3.
4.
5.
6.

## Reliability and Scaling Configuration
- Readiness probe (path, port, timings):
- Liveness probe (path, port, timings):
- CPU/memory requests:
- CPU/memory limits:
- HPA min/max replicas and target:
- `kubectl get hpa` output:

## Security Hardening
- Pod securityContext applied:
- Container securityContext applied:
- Writable `emptyDir` mount required by the read-only filesystem:
- How API_TOKEN is supplied to the pod:
- Command used to create the Secret:
- Evidence the token is no longer in plaintext in deployment.yaml:
- What an attacker who gained `kubectl get secret` access could still do:

## Testing Results
- `/health` on kind: ✅ / ❌
- `/api/report` on kind: ✅ / ❌
- `/health` on GKE external IP: ✅ / ❌
- `/api/report` on GKE external IP: ✅ / ❌

## Cost Analysis
- GKE nodes: ~$ /hour
- Load balancer: ~$ /hour
- Time the cluster was alive:
- **Estimated total cost for this assignment:**

## Cleanup Confirmation
- Command used to delete the GKE cluster:
- Verified deleted with `gcloud container clusters list` on [date]:

## Troubleshooting
[Document any bugs or blockers you hit and how you resolved them]
