"""Base A2AAgent classes for cross-agent automation."""

from __future__ import annotations

from typing import Any, Dict, Iterable


class A2AAgent:
    """Base class for agents that transform JSON input to JSON output."""

    name: str = "a2a_base"
    version: str = "0.1"
    required_fields: Iterable[str] = ()

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}

    def log(self, message: str) -> None:
        """Log helper."""
        print(f"[{self.name}] {message}")

    def validate(self, input_data: Dict[str, Any]) -> None:
        """Validate that required fields exist in the input."""
        missing = [f for f in self.required_fields if f not in input_data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input and return output.

        Subclasses must implement this method.
        """
        raise NotImplementedError


class ContentCreationAgent(A2AAgent):
    """Generate initial content based on a prompt."""

    name = "content_creation"
    version = "0.1"
    required_fields = ("prompt",)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate(input_data)
        self.log("Generating content")
        prompt = input_data["prompt"]
        # Placeholder generation logic
        content = f"Generated content for: {prompt}"
        return {"content": content}


class EditAndEffectsAgent(A2AAgent):
    """Apply edits and effects to existing content."""

    name = "edit_and_effects"
    version = "0.1"
    required_fields = ("content",)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate(input_data)
        self.log("Editing content and adding effects")
        content = input_data["content"]
        # Placeholder editing logic
        edited = f"Edited and enhanced: {content}"
        return {"content": edited}


class PostSchedulerAgent(A2AAgent):
    """Schedule a post to publish on a platform."""

    name = "post_scheduler"
    version = "0.1"
    required_fields = ("content", "platform")

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate(input_data)
        self.log("Scheduling post")
        # Placeholder scheduling logic
        output = {
            "scheduled": True,
            "platform": input_data["platform"],
            "content": input_data["content"],
        }
        return output
