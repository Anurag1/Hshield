from dataclasses import dataclass
import random
from .agents import make_agents
from .safety import SafetyPolicy

@dataclass(frozen=True)
class EpisodeConfig:
    anomaly_probability: float = 0.16
    benign_observation_probability: float = 0.20
    sensing_radius: int = 1

class Simulation:
    def __init__(self, infra, config=EpisodeConfig(), expected_agents=12):
        self.infra, self.config = infra, config
        self.expected_agents = expected_agents

    def run_episode(self, deployment, seed):
        rng = random.Random(seed)
        agents = make_agents(deployment.positions)
        safety = SafetyPolicy(expected_agents=self.expected_agents)
        safety.validate_deployment(self.infra, deployment)
        true_events = detected_events = false_alerts = 0
        benign_observations = true_alerts = total_alerts = 0

        for node in self.infra.nodes:
            is_anomaly = rng.random() < self.config.anomaly_probability
            observers = [a for a in agents if self.infra.distance(node, a.position) <= self.config.sensing_radius]
            if is_anomaly:
                true_events += 1
                votes = sum(a.observe(node, True, rng) for a in observers)
                if safety.emit(votes >= 1) == safety.allowed_output:
                    detected_events += 1
                    true_alerts += 1
                    total_alerts += 1
            elif rng.random() < self.config.benign_observation_probability:
                benign_observations += 1
                votes = sum(a.observe(node, False, rng) for a in observers)
                if safety.emit(votes >= 1) == safety.allowed_output:
                    false_alerts += 1
                    total_alerts += 1

        return {
            "true_events": true_events,
            "detected_events": detected_events,
            "false_alerts": false_alerts,
            "benign_observations": benign_observations,
            "recall": detected_events / true_events if true_events else 1.0,
            "false_positive_rate": false_alerts / benign_observations if benign_observations else 0.0,
            "precision": true_alerts / total_alerts if total_alerts else 1.0,
        }
