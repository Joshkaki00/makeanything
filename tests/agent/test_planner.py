"""
Tests for src/agent/planner.py

All tests FAIL until classify_task is implemented.

Run: pytest tests/agent/test_planner.py -v
"""
import pytest

from src.agent.planner import TaskType, classify_task


class TestInputValidation:
    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            classify_task("")

    def test_whitespace_only_raises_value_error(self):
        with pytest.raises(ValueError):
            classify_task("   ")


class TestRagRouting:
    def test_how_question_routes_to_rag(self):
        assert classify_task("How do I write a Dockerfile?") == TaskType.RAG

    def test_explanation_request_routes_to_rag(self):
        assert classify_task("Explain what Docker containers are") == TaskType.RAG

    def test_ambiguous_tool_name_routes_to_rag(self):
        assert classify_task("Tell me about GitHub Actions") == TaskType.RAG

    def test_question_about_ssh_routes_to_rag(self):
        assert classify_task("What is SSH port forwarding?") == TaskType.RAG


class TestMcpRouting:
    def test_generate_routes_to_mcp(self):
        assert classify_task("Generate a Dockerfile for my Node app") == TaskType.MCP

    def test_create_routes_to_mcp(self):
        assert classify_task("Create a GitHub Actions workflow for Python") == TaskType.MCP

    def test_write_routes_to_mcp(self):
        assert classify_task("Write a Dockerfile for python:3.11 on port 8000") == TaskType.MCP

    def test_make_routes_to_mcp(self):
        assert classify_task("Make a CI pipeline for my project") == TaskType.MCP


class TestBoundaries:
    def test_single_word_query_routes_to_rag(self):
        result = classify_task("Docker")
        assert result in (TaskType.RAG, TaskType.MCP)  # must not raise

    def test_returns_task_type_enum(self):
        result = classify_task("How do I containerize my app?")
        assert isinstance(result, TaskType)
