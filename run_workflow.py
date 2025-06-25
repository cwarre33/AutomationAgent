"""Run automation workflows defined in YAML files."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Dict, Mapping
import time

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


def execute_step(step: Mapping[str, Any], idx: int, debug: bool = False) -> Dict[str, Any]:
    """Run a single workflow step and return execution details."""
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

    start = time.perf_counter()
    success = True
    output: Any = None
    error: str | None = None
    try:
        output = agent.run()
    except Exception as exc:  # pylint: disable=broad-except
        success = False
        error = str(exc)
        agent.log(f"Error during step {idx}: {error}")
    end = time.perf_counter()

    result = {
        "index": idx,
        "agent": agent_name,
        "parameters": params,
        "output": output,
        "success": success,
        "error": error,
        "time_taken": end - start,
        "step": step,
    }

    if debug:
        print(result)

    return result


def run_workflow(path: str | Path, debug: bool = False) -> list[Dict[str, Any]]:
    """Execute all steps in the given workflow file."""
    steps = load_workflow(path)
    results = []
    for idx, step in enumerate(steps, 1):
        results.append(execute_step(step, idx, debug=debug))
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run an automation workflow")
    parser.add_argument("workflow", help="Path to workflow YAML file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    run_workflow(args.workflow, debug=args.debug)
