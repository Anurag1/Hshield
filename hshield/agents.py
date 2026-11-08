from dataclasses import dataclass
import random

@dataclass
class LocalAgent:
    agent_id: int
    position: int
    sensitivity: float = 0.88
    false_alarm_probability: float = 0.025

    def observe(self, node, is_anomaly, rng):
        if is_anomaly:
            return rng.random() < self.sensitivity
        return rng.random() < self.false_alarm_probability

def make_agents(positions):
    return [LocalAgent(i, pos) for i, pos in enumerate(positions)]
