"""
Shared pytest fixtures.

pyproject.toml sets pythonpath=["."] so imports like
`from src.rag.chunker import chunk_markdown` resolve without installation.
"""
import pytest


@pytest.fixture
def docker_guide_md() -> str:
    """Minimal two-section markdown guide for chunker tests."""
    return (
        "## Docker Basics\n\n"
        "Docker is a platform for running applications in containers.\n"
        "Use `docker build` to build an image and `docker run` to start a container.\n\n"
        "## GitHub Actions\n\n"
        "GitHub Actions automates CI/CD workflows defined in `.github/workflows/`.\n"
        "Trigger workflows on push, pull_request, or schedule.\n"
    )


@pytest.fixture
def single_section_md() -> str:
    """Single section for basic chunker tests."""
    return "## Docker Install\n\nRun `apt-get install docker.io` on Ubuntu.\n"
