# H-SHIELD v0.1

Simulation-only prototype for hierarchical deployment and decentralized infrastructure monitoring.

## Research question
Does optimizing a static deployment topology improve weighted infrastructure coverage, redundancy, and anomaly-detection performance relative to random and degree-based placement?

## Architecture
- 24-node, 6x4 grid infrastructure graph.
- Central deployment manager selects 12 fixed monitoring positions once.
- Twelve local agents independently evaluate noisy observations.
- A safety policy validates deployment constraints and emits advisory-only alerts.
- Benchmark compares random, degree-based, and H-SHIELD greedy placement.

The agents do not actuate infrastructure, block traffic, move, or modify the graph. This is a research simulator, not a deployable protective control system.

## Run
```bash
python -m hshield.benchmark --episodes 100 --seed 20261108 --agents 12
python -m unittest discover -s tests -v
```

Python 3.10+; no third-party runtime dependencies.

## Benchmark
The checked-in `benchmark_results.json` contains the reproducible 100-episode run using seed `20261108`. The same episode seeds are used across strategies for paired comparisons.

| Strategy | Weighted coverage | Weighted redundancy | Recall | False-positive rate |
|---|---:|---:|---:|---:|
| Random | 95.67% | 63.95% | 91.82% | 4.14% |
| Degree-based | 92.63% | 52.58% | 85.37% | 5.63% |
| H-SHIELD greedy | 100.00% | 88.63% | 97.85% | 5.26% |

These are synthetic simulation results, not evidence of real-world security effectiveness. The graph, anomaly distribution, sensor model, and criticality weights are simplified assumptions. Results are hypothesis-generating and require broader graph families, ablations, uncertainty analysis, and independent review.

## Safety boundary
Only `ADVISORY_ALERT` and `NO_ALERT` outputs are exposed. There is no actuator, network-blocking, physical-control, or topology-mutation interface. Invalid deployments fail closed through validation errors.

## Current limitations
- The central deployment policy is greedy heuristic optimization, not PPO.
- The local agents use a simple probabilistic sensor model, not trained RL policies.
- The simulator uses a fixed grid graph and synthetic event generation.
- This release is a baseline prototype; hierarchical RL training and generalization experiments are future work.
