import random
from .model import Infrastructure, Deployment, coverage_counts

class DeploymentManager:
    def __init__(self, infra, n_agents=12, radius=1):
        if not 1 <= n_agents <= len(infra.nodes):
            raise ValueError("n_agents must be between 1 and number of nodes")
        self.infra, self.n_agents, self.radius = infra, n_agents, radius

    def random(self, seed):
        rng = random.Random(seed)
        return Deployment(tuple(sorted(rng.sample(self.infra.nodes, self.n_agents))), "random")

    def degree_based(self):
        ordered = sorted(self.infra.nodes, key=lambda n: (-self.infra.degree(n), n))
        return Deployment(tuple(sorted(ordered[:self.n_agents])), "degree")

    def optimized(self):
        chosen = []
        remaining = set(self.infra.nodes)
        weights = self.infra.criticality()
        total = sum(weights.values())

        def score(candidate):
            trial = Deployment(tuple(chosen + [candidate]), "candidate")
            counts = coverage_counts(self.infra, trial, self.radius)
            covered = sum(weights[n] for n, c in counts.items() if c >= 1)
            redundant = sum(weights[n] for n, c in counts.items() if c >= 2)
            concentration = 0.0
            if chosen:
                nearest = min(self.infra.distance(candidate, p) for p in chosen)
                concentration = max(0.0, 2.0 - nearest) * 0.015 * total
            return (covered + 0.32 * redundant - concentration) / total

        while len(chosen) < self.n_agents:
            best = max(sorted(remaining), key=lambda n: (score(n), -n))
            chosen.append(best)
            remaining.remove(best)
        return Deployment(tuple(sorted(chosen)), "hshield")

def build_deployment(strategy, seed=0, n_agents=12):
    manager = DeploymentManager(Infrastructure(), n_agents=n_agents)
    if strategy == "random":
        return manager.random(seed)
    if strategy == "degree":
        return manager.degree_based()
    if strategy == "hshield":
        return manager.optimized()
    raise ValueError(f"Unknown strategy: {strategy}")
