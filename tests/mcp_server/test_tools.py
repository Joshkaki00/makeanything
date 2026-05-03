"""
Tests for src/mcp_server/tools.py

All tests FAIL until tools are implemented.
Tests import pure functions from tools.py — no MCP runtime required.

Run: pytest tests/mcp_server/test_tools.py -v
"""
import pytest

from src.mcp_server.tools import create_dockerfile, create_github_actions_workflow


class TestCreateDockerfile:
    def test_contains_from_instruction(self):
        result = create_dockerfile(base_image="python:3.11-slim", port=8000)
        assert "FROM python:3.11-slim" in result

    def test_contains_expose(self):
        result = create_dockerfile(base_image="python:3.11-slim", port=8000)
        assert "EXPOSE 8000" in result

    def test_contains_workdir(self):
        result = create_dockerfile(base_image="python:3.11-slim", port=8000)
        assert "WORKDIR" in result

    def test_custom_working_dir(self):
        result = create_dockerfile(base_image="node:18-slim", port=3000, working_dir="/srv")
        assert "/srv" in result

    # --- boundary / validation tests ---
    def test_empty_base_image_raises(self):
        with pytest.raises(ValueError):
            create_dockerfile(base_image="", port=8000)

    def test_port_zero_raises(self):
        with pytest.raises(ValueError):
            create_dockerfile(base_image="python:3.11-slim", port=0)

    def test_port_negative_raises(self):
        with pytest.raises(ValueError):
            create_dockerfile(base_image="python:3.11-slim", port=-1)

    def test_port_above_65535_raises(self):
        with pytest.raises(ValueError):
            create_dockerfile(base_image="python:3.11-slim", port=65536)

    def test_returns_string(self):
        result = create_dockerfile(base_image="python:3.11-slim", port=8000)
        assert isinstance(result, str)


class TestCreateGithubActionsWorkflow:
    def test_contains_on_trigger_push(self):
        result = create_github_actions_workflow(trigger="push")
        assert "push" in result

    def test_contains_python_version(self):
        result = create_github_actions_workflow(trigger="push", python_version="3.11")
        assert "3.11" in result

    def test_contains_on_key(self):
        result = create_github_actions_workflow(trigger="pull_request")
        assert "on:" in result

    def test_empty_trigger_raises(self):
        with pytest.raises(ValueError):
            create_github_actions_workflow(trigger="")

    def test_invalid_trigger_raises(self):
        with pytest.raises(ValueError):
            create_github_actions_workflow(trigger="not_a_real_event")

    def test_returns_string(self):
        result = create_github_actions_workflow(trigger="push")
        assert isinstance(result, str)
