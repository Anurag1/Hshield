from dataclasses import dataclass

@dataclass(frozen=True)
class Infrastructure:
    width: int = 6
    height: int = 4

    @property
    def nodes(self):
        return list(range(self.width * self.height))

    def xy(self, node):
        return node % self.width, node // self.width

    def neighbors(self, node):
        x, y = self.xy(node)
        out = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                out.append(ny * self.width + nx)
        return out

    def degree(self, node):
        return len(self.neighbors(node))

    def distance(self, a, b):
        ax, ay = self.xy(a)
        bx, by = self.xy(b)
        return abs(ax - bx) + abs(ay - by)

    def criticality(self):
        cx, cy = (self.width - 1) / 2, (self.height - 1) / 2
        return {
            n: 1.0 + 0.35 * (1.0 - (abs(self.xy(n)[0] - cx) + abs(self.xy(n)[1] - cy)) / (cx + cy))
            for n in self.nodes
        }

@dataclass(frozen=True)
class Deployment:
    positions: tuple
    strategy: str

    def __post_init__(self):
        if len(set(self.positions)) != len(self.positions):
            raise ValueError("Agent positions must be unique")
        if not self.positions:
            raise ValueError("Deployment must contain at least one agent")

def coverage_counts(infra, deployment, radius=1):
    return {
        node: sum(infra.distance(node, pos) <= radius for pos in deployment.positions)
        for node in infra.nodes
    }

def topology_metrics(infra, deployment, radius=1):
    counts = coverage_counts(infra, deployment, radius)
    weights = infra.criticality()
    total = sum(weights.values())
    covered = sum(weights[n] for n, c in counts.items() if c >= 1)
    redundant = sum(weights[n] for n, c in counts.items() if c >= 2)
    return {
        "weighted_coverage": covered / total,
        "weighted_redundancy": redundant / total,
        "mean_agents_per_node": sum(counts.values()) / len(counts),
    }
