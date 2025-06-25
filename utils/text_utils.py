"""Utility functions for text manipulation."""


def summarize(text: str) -> str:
    """Return a short summary of the text."""
    words = text.split()
    return " ".join(words[:10]) + ("..." if len(words) > 10 else "")
