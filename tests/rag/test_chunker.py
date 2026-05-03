"""
Tests for src/rag/chunker.py

All tests FAIL until chunk_markdown is implemented (stubs raise NotImplementedError).
Run: pytest tests/rag/test_chunker.py -v
"""
import pytest

from src.rag.chunker import Chunk, chunk_markdown


class TestEmptyAndWhitespace:
    def test_empty_string_returns_empty_list(self):
        assert chunk_markdown("", source="test.md") == []

    def test_whitespace_only_returns_empty_list(self):
        assert chunk_markdown("   \n\n  \t  ", source="test.md") == []


class TestHeadingBoundaries:
    def test_two_sections_produce_two_chunks(self, docker_guide_md):
        chunks = chunk_markdown(docker_guide_md, source="test.md")
        assert len(chunks) == 2

    def test_headings_stored_on_chunks(self, docker_guide_md):
        chunks = chunk_markdown(docker_guide_md, source="test.md")
        headings = {c.heading for c in chunks}
        assert "Docker Basics" in headings
        assert "GitHub Actions" in headings

    def test_docker_chunk_does_not_contain_github_actions_text(self, docker_guide_md):
        chunks = chunk_markdown(docker_guide_md, source="test.md")
        docker_chunk = next(c for c in chunks if c.heading == "Docker Basics")
        assert "GitHub Actions" not in docker_chunk.text

    def test_github_chunk_does_not_contain_docker_text(self, docker_guide_md):
        chunks = chunk_markdown(docker_guide_md, source="test.md")
        gha_chunk = next(c for c in chunks if c.heading == "GitHub Actions")
        assert "docker build" not in gha_chunk.text.lower()


class TestSourcePreservation:
    def test_source_preserved_on_all_chunks(self, docker_guide_md):
        chunks = chunk_markdown(docker_guide_md, source="docker-guide.md")
        assert all(c.source == "docker-guide.md" for c in chunks)

    def test_source_preserved_single_section(self, single_section_md):
        chunks = chunk_markdown(single_section_md, source="ubuntu.md")
        assert chunks[0].source == "ubuntu.md"


class TestChunkType:
    def test_returns_list_of_chunk_objects(self, single_section_md):
        chunks = chunk_markdown(single_section_md, source="test.md")
        assert all(isinstance(c, Chunk) for c in chunks)

    def test_chunk_text_is_non_empty(self, single_section_md):
        chunks = chunk_markdown(single_section_md, source="test.md")
        assert all(c.text.strip() for c in chunks)


class TestMaxSize:
    def test_oversized_section_is_split_further(self):
        long_text = "## Big Section\n\n" + ("word " * 300) + "\n"
        chunks = chunk_markdown(long_text, source="test.md", max_size=200)
        assert len(chunks) > 1
        assert all(len(c.text) <= 200 + 50 for c in chunks)  # allow small overshoot
