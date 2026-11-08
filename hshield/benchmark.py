import argparse
import json
import statistics
from .model import Infrastructure, topology_metrics
from .deployment import build_deployment
from .simulation import Simulation

STRATEGIES = ("random", "degree", "hshield")

def run_benchmark(episodes=100, seed=20261108, n_agents=12):
    if episodes < 1:
        raise ValueError("episodes must be positive")
    infra = Infrastructure()
    sim = Simulation(infra, expected_agents=n_agents)
    results = {}
    episode_seeds = [seed + i for i in range(episodes)]
    for strategy in STRATEGIES:
        deployment = build_deployment(strategy, seed=seed, n_agents=n_agents)
        rows = [sim.run_episode(deployment, s) for s in episode_seeds]
        metrics = {}
        for key in ("recall", "false_positive_rate", "precision"):
            vals = [r[key] for r in rows]
            metrics[key] = statistics.mean(vals)
            metrics[key + "_sd"] = statistics.pstdev(vals)
        metrics.update(topology_metrics(infra, deployment))
        metrics["positions"] = list(deployment.positions)
        metrics["episodes"] = episodes
        results[strategy] = metrics
    return {
        "configuration": {"seed": seed, "episodes": episodes, "agents": n_agents,
                          "nodes": len(infra.nodes), "grid": [infra.width, infra.height]},
        "results": results,
    }

def main():
    parser = argparse.ArgumentParser(description="H-SHIELD reproducible benchmark")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20261108)
    parser.add_argument("--agents", type=int, default=12)
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()
    result = run_benchmark(args.episodes, args.seed, args.agents)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered + "\n")

if __name__ == "__main__":
    main()
