import unittest
from hshield.model import Infrastructure, Deployment, coverage_counts, topology_metrics
from hshield.deployment import DeploymentManager, build_deployment
from hshield.simulation import Simulation
from hshield.safety import SafetyPolicy

class HShieldTests(unittest.TestCase):
    def setUp(self):
        self.infra = Infrastructure()
        self.manager = DeploymentManager(self.infra, n_agents=12)

    def test_deployment_has_12_unique_positions(self):
        d = self.manager.optimized()
        self.assertEqual(len(d.positions), 12)
        self.assertEqual(len(set(d.positions)), 12)

    def test_topology_is_static_and_valid(self):
        d = self.manager.optimized()
        before = d.positions
        Simulation(self.infra).run_episode(d, 123)
        self.assertEqual(before, d.positions)

    def test_random_deployment_reproducible(self):
        self.assertEqual(self.manager.random(77), self.manager.random(77))

    def test_coverage_counts_nonnegative(self):
        counts = coverage_counts(self.infra, self.manager.optimized())
        self.assertEqual(set(counts), set(self.infra.nodes))
        self.assertTrue(all(v >= 0 for v in counts.values()))

    def test_metrics_in_unit_interval(self):
        m = topology_metrics(self.infra, self.manager.optimized())
        self.assertTrue(0 <= m["weighted_coverage"] <= 1)
        self.assertTrue(0 <= m["weighted_redundancy"] <= 1)

    def test_episode_metrics_in_unit_interval(self):
        d = build_deployment("hshield", seed=4)
        result = Simulation(self.infra).run_episode(d, 999)
        for key in ("recall", "false_positive_rate", "precision"):
            self.assertTrue(0 <= result[key] <= 1)

    def test_safety_policy_rejects_wrong_agent_count(self):
        with self.assertRaises(ValueError):
            SafetyPolicy(expected_agents=12).validate_deployment(self.infra, Deployment((1, 2), "bad"))

    def test_safety_output_is_advisory_only(self):
        policy = SafetyPolicy()
        self.assertEqual(policy.emit(True), "ADVISORY_ALERT")
        self.assertEqual(policy.emit(False), "NO_ALERT")

    def test_simulation_rejects_wrong_configured_agent_count(self):
        d = Deployment((1, 2), "invalid-size")
        with self.assertRaises(ValueError):
            Simulation(self.infra).run_episode(d, 1)

    def test_invalid_duplicate_positions_rejected(self):
        with self.assertRaises(ValueError):
            Deployment((1, 1), "invalid")

if __name__ == "__main__":
    unittest.main()
