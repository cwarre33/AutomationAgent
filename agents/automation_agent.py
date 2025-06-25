"""Base classes for automation agents."""

from typing import Any, Dict
import os

import openai


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
    """Agent that generates captions and scripts using OpenAI."""

    def _build_prompt(self, content_type: str, audience: str, tone: str) -> str:
        """Return a prompt describing the desired content."""
        return (
            f"Create a catchy caption and short script for a {content_type}. "
            f"Audience: {audience}. Tone: {tone}. "
            "Provide the caption on the first line and the script on the next."\
        )

    def run(self) -> Dict[str, str]:
        content_type = self.config.get("content_type", "product")
        audience = self.config.get("audience", "general audience")
        tone = self.config.get("tone", "neutral")
        max_tokens = int(self.config.get("max_tokens", 100))

        prompt = self._build_prompt(content_type, audience, tone)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )

        message = response.choices[0].message["content"].strip()
        lines = message.splitlines()
        caption = lines[0] if lines else ""
        script = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        result = {"caption": caption, "script": script}
        self.log("Generated caption and script")
        return result


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
