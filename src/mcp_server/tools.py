"""
Pure tool implementations — no FastMCP dependency.

These functions are registered as MCP tools in server.py.
Tests import from here directly to avoid needing the MCP runtime.

Rules (see src/mcp_server/AGENTS.md):
- Validate all inputs before executing. Raise ValueError for bad inputs.
- One tool, one concern.
- Return strings only — no dicts, no lists.
"""


def create_dockerfile(base_image: str, port: int, working_dir: str = "/app") -> str:
    """
    Generate a production-ready Dockerfile.

    Args:
        base_image: Docker base image tag (e.g. "python:3.11-slim"). Must be non-empty.
        port: Port the application listens on. Must be 1–65535.
        working_dir: Working directory inside the container.

    Returns:
        Multi-line Dockerfile string.

    Raises:
        ValueError: If base_image is empty or port is out of range.
    """
    raise NotImplementedError


def create_github_actions_workflow(trigger: str, python_version: str = "3.11") -> str:
    """
    Generate a GitHub Actions CI workflow YAML.

    Args:
        trigger: Workflow trigger event ("push", "pull_request", "workflow_dispatch").
                 Must be non-empty.
        python_version: Python version string (e.g. "3.11", "3.12").

    Returns:
        Multi-line YAML string for .github/workflows/ci.yml.

    Raises:
        ValueError: If trigger is empty or not a recognized event name.
    """
    raise NotImplementedError
