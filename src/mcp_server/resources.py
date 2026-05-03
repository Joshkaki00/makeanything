"""
MCP resource implementations.

Resources are read-only data sources Claude can reference.
The project log tracks what the user is currently working on.

Log file location: data/project-log.md (created on first write).
"""
from pathlib import Path

PROJECT_LOG_PATH = Path("data/project-log.md")


def get_project_log() -> str:
    """
    Return the current project task log.

    Returns the contents of data/project-log.md.
    Returns a default message if the log file doesn't exist yet.
    """
    if PROJECT_LOG_PATH.exists():
        return PROJECT_LOG_PATH.read_text(encoding="utf-8")
    return "# Project Log\n\nNo tasks logged yet. Start by describing what you're building.\n"


def append_to_project_log(entry: str) -> None:
    """
    Append a timestamped entry to the project log.

    Args:
        entry: Text to append. Must be non-empty.

    Raises:
        ValueError: If entry is empty.
    """
    if not entry or not entry.strip():
        raise ValueError("entry must not be empty")
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    PROJECT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROJECT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}] {entry}")
