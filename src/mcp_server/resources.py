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
    raise NotImplementedError


def append_to_project_log(entry: str) -> None:
    """
    Append a timestamped entry to the project log.

    Args:
        entry: Text to append. Must be non-empty.

    Raises:
        ValueError: If entry is empty.
    """
    raise NotImplementedError
