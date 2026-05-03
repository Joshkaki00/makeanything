"""
Pure tool implementations — no FastMCP dependency.

These functions are registered as MCP tools in server.py.
Tests import from here directly to avoid needing the MCP runtime.

Rules (see src/mcp_server/AGENTS.md):
- Validate all inputs before executing. Raise ValueError for bad inputs.
- One tool, one concern.
- Return strings only — no dicts, no lists.
"""

VALID_TRIGGERS = {"push", "pull_request", "workflow_dispatch"}


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
    # Validate inputs before any string construction
    if not base_image or base_image.strip() == "":
        raise ValueError("base_image must not be empty")

    if port < 1 or port > 65535:
        raise ValueError(f"port must be 1–65535, got {port}")

    dockerfile = f"""FROM {base_image}

WORKDIR {working_dir}

EXPOSE {port}

RUN apt-get update && apt-get install -y --no-install-recommends \\
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
"""
    return dockerfile


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
    # Validate inputs before any string construction
    if not trigger or trigger.strip() == "":
        raise ValueError("trigger must not be empty")

    if trigger not in VALID_TRIGGERS:
        raise ValueError(f"trigger must be one of {VALID_TRIGGERS}, got '{trigger}'")

    workflow = f"""name: CI

on:
  {trigger}:
    branches:
      - main
      - develop

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python {python_version}
        uses: actions/setup-python@v4
        with:
          python-version: {python_version}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest

      - name: Run linter
        run: ruff check .
"""
    return workflow
