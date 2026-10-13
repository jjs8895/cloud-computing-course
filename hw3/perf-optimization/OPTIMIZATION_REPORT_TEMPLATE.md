# Performance Optimization Report

## Experiment Setup

- Cluster (kind version, node count):
- Image tag under test:
- Load generator settings (duration, concurrency):
- Host machine (CPU cores, RAM):

State anything you changed from the assignment defaults, and why.

## Baseline Measurements

Run the load generator against the **unmodified** starter before you change anything.

| Metric | hot pattern | unique pattern |
| --- | --- | --- |
| Throughput (req/s) | | |
| Latency p50 (ms) | | |
| Latency p95 (ms) | | |
| Latency p99 (ms) | | |
| Error rate (%) | | |
| Cache hit rate | | |
| Distinct pods observed | | |

Baseline configuration: replicas = ___, gunicorn workers = ___, threads = ___,
CPU request = ___, CPU limit = ___.

## Optimized Measurements

| Metric | hot pattern | unique pattern |
| --- | --- | --- |
| Throughput (req/s) | | |
| Latency p50 (ms) | | |
| Latency p95 (ms) | | |
| Latency p99 (ms) | | |
| Error rate (%) | | |
| Cache hit rate | | |
| Distinct pods observed | | |

Optimized configuration: replicas = ___, gunicorn workers = ___, threads = ___,
CPU request = ___, CPU limit = ___.

## What You Changed

### Optimization 1: Application-level cache
- What you implemented:
- Where the cache lives, and what its lifetime is:
- Measured effect (cite the numbers above):

### Optimization 2: Container-level concurrency
- Worker and thread count you chose, and why that number:
- Measured effect:

### Optimization 3: Kubernetes resources and replicas
- CPU request/limit you chose, and why:
- Replica count you chose, and why:
- Measured effect:

## Q1: Which optimization helped which workload?

For each of the three optimizations, state which load pattern it improved and which it
left roughly unchanged. Explain the mechanism in each case. An optimization that helps
one pattern and not the other is the expected result, not a mistake — explain the
asymmetry rather than apologizing for it.

## Q2: Throughput, workers, and threads

You measured throughput as you varied gunicorn workers and threads.

- Which of the two knobs increased throughput on the `unique` pattern, and which did not?
- Explain why, in terms of what a worker is versus what a thread is for a CPU-bound
  Python request handler.
- What did the knob that did *not* raise throughput actually improve, if anything?

## Q3: The CPU limit

- What happened to p95 latency when you raised gunicorn workers but left `limits.cpu`
  at the starter's `500m`? Report the numbers.
- Explain the mechanism. What is the scheduler doing to your container?
- What is the relationship between `requests.cpu`, `limits.cpu`, and the CPU the pod
  actually gets when the node is busy?

## Q4: Cache correctness and the cost of scaling out

- Your cache is per-process. How many independent copies of it exist when you run
  R replicas with W gunicorn workers each?
- What does that do to the hit rate you measured, compared to a single cache?
- The report for a given symbol never changes, which is why this cache is safe. Describe
  a change to `/api/report` that would make this exact caching strategy incorrect, and
  say what you would have to do instead.
- Your cache is almost certainly unbounded. Explain what would eventually happen to a pod
  running it for weeks under the `unique` access pattern, and how an LRU eviction policy
  of the kind Memcached uses would prevent it. Relate this to the memory limit you set in
  `deployment.yaml`: what would Kubernetes do to the pod?

## Q5: From the local cluster to GKE

Your Part C measurements come from a local `kind` cluster on one machine. Suppose you
deployed the optimized image to the GKE cluster from Part B and ran the same load test
against the LoadBalancer IP.

- Name two things that would make the *absolute* latency numbers worse, and explain each.
- Would your *relative* conclusions (which optimization helps which pattern) still hold?
  Why or why not?
- The HPA you wrote scales on CPU utilization. Under which of the two load patterns would
  it actually add replicas, and under which would it mostly sit idle? Explain.

## Q6: Cloud interpretation

- Map each of your three optimizations onto a layer of the stack (application code,
  container runtime, orchestration). Why does a real performance investigation have to
  consider all three rather than stopping at the first one that helps?
- Connect your results to one specific idea from the course readings on performance
  efficiency (for example: caching to remove redundant work, scaling out versus scaling
  up, or resource right-sizing). Be concrete about which of your numbers supports it.
