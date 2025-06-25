"""Run automation workflows defined in YAML files."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Dict, Mapping

import yaml

from agents import AutomationAgent


def _discover_agents() -> Mapping[str, type[AutomationAgent]]:
    """Return a mapping of available agent class names to their classes."""
    agents_module = importlib.import_module("agents")
    registry: Dict[str, type[AutomationAgent]] = {}
    for attr in dir(agents_module):
        obj = getattr(agents_module, attr)
        if (
            isinstance(obj, type)
            and issubclass(obj, AutomationAgent)
            and obj is not AutomationAgent
        ):
            registry[obj.__name__] = obj
    return registry


AGENT_REGISTRY = _discover_agents()


def load_workflow(path: str | Path) -> list[dict[str, Any]]:
    """Load steps from a YAML workflow file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        raise ValueError("'steps' must be a list in workflow file")
    return steps


def run_workflow(path: str | Path) -> None:
    """Execute all steps in the given workflow file."""
    steps = load_workflow(path)
    for idx, step in enumerate(steps, 1):
        if not isinstance(step, Mapping):
            raise ValueError(f"Step {idx} must be a mapping")
        agent_name = step.get("agent")
        if not agent_name:
            raise ValueError(f"Step {idx} missing 'agent' key")
        params = step.get("parameters") or {}
        cls = AGENT_REGISTRY.get(agent_name)
        if cls is None:
            raise ValueError(
                f"Agent '{agent_name}' not found. Available agents: {list(AGENT_REGISTRY)}"
            )
        agent = cls(params)
        agent.log(f"Executing step {idx}")
        agent.run()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_workflow.py <workflow.yaml>")
        sys.exit(1)
    run_workflow(sys.argv[1])
