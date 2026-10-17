"""
NeuroHive - Autonomous Multi-Agent Swarm Personas & Tools.
"""

from typing import Dict, Any, List

class Agent:
    def __init__(self, name: str, role: str, expertise: str, icon: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.icon = icon

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "role": self.role,
            "expertise": self.expertise,
            "icon": self.icon
        }

# Pre-configured Expert Agents in the Swarm
ARCHITECT_AGENT = Agent(
    name="Atlas",
    role="System Architect",
    expertise="Breaks complex engineering tasks into modular, scalable specifications.",
    icon="🏛️"
)

CODER_AGENT = Agent(
    name="Cygnus",
    role="Lead Engineer",
    expertise="Synthesizes clean, high-performance algorithms in Python, JS, and Shell.",
    icon="⚡"
)

AUDITOR_AGENT = Agent(
    name="Vanguard",
    role="Cybersecurity Auditor",
    expertise="Inspects code for vulnerabilities, race conditions, memory leaks, and logic flaws.",
    icon="🛡️"
)

SANDBOX_AGENT = Agent(
    name="Sentinel",
    role="Execution & SRE Engine",
    expertise="Safely runs binaries in isolated runtimes and captures real telemetry.",
    icon="🚀"
)
