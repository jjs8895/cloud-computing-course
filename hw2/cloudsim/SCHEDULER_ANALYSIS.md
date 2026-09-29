Q1: Makespan
- What is the total completion time under FCFS?
222.01
- What is the total completion time under SJF?
236.01
- Which policy achieved the smaller makespan?
FCFS

Q2: Load Distribution
- How many cloudlets were assigned to each VM under each policy?
FCFS:
VM0 --> 3 cloudlets
VM1 --> 3 Cloudlets
VM2 --> 2 Cloudlets

SJF:
VM0 --> 3 Cloudlets
VM1 --> 3 Cloudlets
VM2 --> 2 Cloudlets
- Which policy produced a more balanced workload distribution?
SJF

Q3: Stragglers
- Which cloudlet finished last under each policy?
FCFS: Cloudlet 7
SJF: Cloudlet 3
- Did the scheduling policy reduce or worsen the straggler effect?
In this case SJF wrosened the straggler effect.

Q4: Fairness vs. Throughput
- Why can a shorter-job-first policy improve throughput?
SJF can improve throughput by completing shorter jobs first instead of having them wait for a longer job to complete first
- When might it be considered unfair?
SJF might be considered unfair to longer jobs because they can be pushed back for shorter jobs due to shorter jobs having a higher priority.

Q5: Cloud interpretation
- How does this small simulation connect to real cloud scheduling or load balancing decisions?
This simulation shows that scheduling and load balancing decisions can affect completion time, even if each VM has the same number of cloudlets. In the simulation the VM's recieved the same number of cloudlets for both FCFS and SJF, however the workload for each VM was different resulting in differing completion times.
- Which lecture concepts are visible here: stragglers, load balancing, barrier effects, or coarse-grained parallelism?
Each of these lecture concepts are visible in this simulation.
