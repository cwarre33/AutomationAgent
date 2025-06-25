"""Base classes for automation agents."""

from typing import Any, Dict


class AutomationAgent:
    """Generic automation agent with configurable parameters."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config: Dict[str, Any] = config or {}

    def run(self) -> None:
        """Execute the agent task. Must be overridden by subclasses."""
        raise NotImplementedError("run() must be implemented by subclasses")

    def log(self, message: str) -> None:
        """Simple logger for tracing execution."""
        print(f"[{self.__class__.__name__}] {message}")


class CreateContentAgent(AutomationAgent):
    """Agent responsible for generating content."""

    def run(self) -> None:
        self.log("Creating content...")
        # Placeholder for content creation logic


class EditContentAgent(AutomationAgent):
    """Agent responsible for editing existing content."""

    def run(self) -> None:
        self.log("Editing content...")
        # Placeholder for content editing logic


class PostContentAgent(AutomationAgent):
    """Agent responsible for posting content to platforms."""

    def run(self) -> None:
        self.log("Posting content...")
        # Placeholder for content posting logic
