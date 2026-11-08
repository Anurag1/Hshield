"""Simulation safety boundary: advisory monitoring only; no actuation APIs."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SafetyPolicy:
    expected_agents: int = 12
    allowed_output: str = "ADVISORY_ALERT"

    def validate_deployment(self, infra, deployment):
        if len(deployment.positions) != self.expected_agents:
            raise ValueError("Deployment violates configured agent-count limit")
        if len(set(deployment.positions)) != len(deployment.positions):
            raise ValueError("Duplicate deployment positions are prohibited")
        if any(p not in infra.nodes for p in deployment.positions):
            raise ValueError("Deployment contains an unknown infrastructure node")

    def emit(self, alert):
        return self.allowed_output if alert else "NO_ALERT"
