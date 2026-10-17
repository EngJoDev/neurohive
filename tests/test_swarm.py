"""
Unit Tests for NeuroHive Multi-Agent Swarm & Code Sandbox.
"""

import unittest
from neurohive.sandbox.executor import CodeSandbox
from neurohive.orchestrator.swarm import SwarmOrchestrator

class TestNeuroHive(unittest.TestCase):
    def setUp(self):
        self.sandbox = CodeSandbox(timeout_seconds=5)
        self.orchestrator = SwarmOrchestrator()

    def test_sandbox_python_execution(self):
        code = "print('NEURO_OK')"
        res = self.sandbox.execute(code, language="python")
        self.assertTrue(res["success"])
        self.assertEqual(res["stdout"], "NEURO_OK")

    def test_sandbox_security_blocking(self):
        malicious_code = "import os; os.system('rm -rf /')"
        res = self.sandbox.execute(malicious_code, language="python")
        self.assertFalse(res["success"])
        self.assertIn("Security Sandbox Violation", res["error"])

    def test_swarm_pipeline_orchestration(self):
        result = self.orchestrator.run_pipeline("Generate benchmark algorithm")
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(len(result["steps"]), 4)
        
        # Verify step agent roles
        agent_names = [s["agent"]["name"] for s in result["steps"]]
        self.assertIn("Atlas", agent_names)
        self.assertIn("Cygnus", agent_names)
        self.assertIn("Vanguard", agent_names)
        self.assertIn("Sentinel", agent_names)

if __name__ == "__main__":
    unittest.main()
