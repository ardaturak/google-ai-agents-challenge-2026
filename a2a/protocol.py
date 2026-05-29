"""A2A Protocol — Agent-to-Agent communication interface.

Implements the Agent-to-Agent protocol for inter-service communication.
Allows PRONUVE agents to communicate with external AI agent systems.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class A2AMessage:
    sender: str
    recipient: str
    action: str
    payload: dict[str, Any]
    priority: str = "normal"
    requires_response: bool = False


class A2AProtocol:
    """Agent-to-Agent protocol handler for external integrations.
    
    Allows PRONUVE to communicate with:
    - Municipal management systems
    - IoT gateway agents
    - External weather service agents
    - Partner data platforms
    """

    def __init__(self, agent_id: str, registry_url: str | None = None):
        self.agent_id = agent_id
        self.registry_url = registry_url or "http://localhost:9000/a2a/registry"
        self._message_queue: list[A2AMessage] = []

    def send(self, recipient: str, action: str, payload: dict) -> A2AMessage:
        msg = A2AMessage(
            sender=self.agent_id,
            recipient=recipient,
            action=action,
            payload=payload,
        )
        self._message_queue.append(msg)
        return msg

    def receive(self) -> list[A2AMessage]:
        messages = self._message_queue.copy()
        self._message_queue.clear()
        return messages

    def register_capability(self, capability: str, description: str) -> dict:
        return {
            "agent_id": self.agent_id,
            "capability": capability,
            "description": description,
            "status": "registered",
        }

    def discover_agents(self, capability_filter: str | None = None) -> list[dict]:
        known_agents = [
            {"agent_id": "municipal_mgmt", "capabilities": ["work_orders", "budget"]},
            {"agent_id": "iot_gateway", "capabilities": ["sensor_data", "valve_control"]},
            {"agent_id": "weather_service", "capabilities": ["forecast", "historical"]},
        ]
        if capability_filter:
            return [a for a in known_agents if capability_filter in a["capabilities"]]
        return known_agents
