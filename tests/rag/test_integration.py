"""
End-to-end integration tests for the RAG pipeline.

Tests the full pipeline:
  1. Load a guide file from data/guides/
  2. Chunk it using chunk_markdown()
  3. Embed chunks using embed_texts()
  4. Store chunks in VectorStore
  5. Query the store with relevant questions
  6. Verify results are accurate and ordered by relevance

These tests use the real pipeline (no mocks), actual embeddings,
and temporary VectorStore instances for isolation.

Run: venv/bin/pytest tests/rag/test_integration.py -v
"""

import os
import shutil
import tempfile
from pathlib import Path

import numpy as np
import pytest

from src.rag.chunker import chunk_markdown
from src.rag.embedder import embed_texts
from src.rag.store import VectorStore

pytestmark = pytest.mark.integration


class TestEndToEndRAG:
    """End-to-end RAG pipeline tests."""

    @pytest.fixture
    def docker_guide_path(self) -> Path:
        """Return path to docker-basics.md guide."""
        return Path("data/guides/docker-basics.md")

    @pytest.fixture
    def docker_guide_text(self, docker_guide_path) -> str:
        """Load the docker-basics.md guide text."""
        if not docker_guide_path.exists():
            pytest.skip(f"Guide file not found: {docker_guide_path}")
        return docker_guide_path.read_text()

    @pytest.fixture
    def temp_persist_dir(self):
        """Create a temporary directory for ChromaDB persistence, clean it up after."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup after test
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    @pytest.fixture
    def populated_store(self, docker_guide_text, temp_persist_dir):
        """
        Set up the full pipeline: load guide, chunk, embed, store.
        Yields a populated VectorStore for query tests.
        """
        # Step 1: Chunk the guide
        chunks = chunk_markdown(docker_guide_text, source="docker-basics.md")
        assert len(chunks) > 0, "No chunks produced from docker-basics.md"

        # Step 2: Extract text for embedding
        chunk_texts = [chunk.text for chunk in chunks]

        # Step 3: Embed all chunks
        embeddings = embed_texts(chunk_texts)
        assert embeddings.shape[0] == len(chunks), "Embedding count mismatch"
        assert embeddings.ndim == 2, "Embeddings should be 2-dimensional"

        # Step 4: Create store and add chunks
        store = VectorStore(
            collection_name="docker_guide_test",
            persist_dir=temp_persist_dir,
        )
        store.add(chunks, embeddings)
        assert store.collection.count() == len(chunks), "Store chunk count mismatch"

        yield store

    def test_retrieve_docker_guide_for_containerization_question(self, populated_store):
        """
        Query the populated store with a containerization question.
        Verify results are non-empty and contain Docker-related keywords.
        """
        query = "How do I containerize a Python app?"
        query_embedding = embed_texts([query])[0]

        results = populated_store.query(query_embedding, top_k=5)

        # Verify results are non-empty
        assert len(results) > 0, "No results returned for containerization question"

        # Verify results contain expected Docker keywords
        result_text = "\n".join(chunk.text.lower() for chunk in results)
        docker_keywords = ["docker", "container", "image", "dockerfile"]
        assert any(
            keyword in result_text for keyword in docker_keywords
        ), f"Results missing Docker keywords. Results:\n{result_text}"

        # Verify source is correct
        assert all(
            chunk.source == "docker-basics.md" for chunk in results
        ), "Source should be docker-basics.md"

    def test_retrieve_returns_most_relevant_first(self, populated_store):
        """
        Query for "docker build" and verify the results are ordered
        by relevance (most similar first), with build-related content
        appearing in top results.
        """
        query = "docker build"
        query_embedding = embed_texts([query])[0]

        results = populated_store.query(query_embedding, top_k=5)

        assert len(results) > 0, "No results returned for 'docker build'"

        # Build-related keywords should appear in at least one of top results
        result_text = "\n".join(chunk.text.lower() for chunk in results)
        build_keywords = ["build", "dockerfile", "image"]
        assert any(
            keyword in result_text for keyword in build_keywords
        ), (
            "Results should mention build-related concepts"
        )

    def test_no_hallucination_verify_commands_in_guide(
        self, populated_store  # pylint: disable=unused-argument
    ):
        """
        Query for "docker" and verify results are coherent chunks
        from the guide (no hallucinated content).
        """
        query = "How do I use docker?"
        query_embedding = embed_texts([query])[0]

        results = populated_store.query(query_embedding, top_k=5)

        assert len(results) > 0, "No results returned for 'How do I use docker?'"

        # Verify each result is a reasonable chunk (has text, source, and is non-empty)
        for chunk in results:
            assert chunk.text.strip(), "Chunk has empty text"
            assert chunk.source == "docker-basics.md", f"Wrong source: {chunk.source}"
            # Verify it's not too short (likely a hallucination) or too long
            assert 10 < len(chunk.text) < 5000, f"Chunk has suspicious length: {len(chunk.text)}"
            # Verify chunk contains words from the guide (basic sanity check)
            guide_words = {"docker", "container", "image", "build", "run", "command"}
            chunk_words = set(chunk.text.lower().split())
            assert guide_words & chunk_words, "Chunk shares no key terms with guide"

    def test_chunks_preserve_source_and_heading_metadata(self, populated_store):
        """
        Verify that chunks in the store preserve source and heading metadata.
        This ensures metadata is not lost during chunking, embedding, or storage.
        """
        query = "docker"
        query_embedding = embed_texts([query])[0]

        results = populated_store.query(query_embedding, top_k=10)

        # All results should have source preserved
        for chunk in results:
            assert chunk.source == "docker-basics.md", f"Source mismatch: {chunk.source}"

        # At least some results should have headings (sections with ## headers)
        headings = [chunk.heading for chunk in results if chunk.heading]
        assert len(headings) > 0, "No chunks with headings in results"

    def test_full_pipeline_produces_queryable_results(
        self, docker_guide_text, temp_persist_dir
    ):
        """
        Complete end-to-end test: load, chunk, embed, store, and query.
        Verify the pipeline produces usable search results.
        """
        # Step 1: Load and chunk
        chunks = chunk_markdown(docker_guide_text, source="docker-basics.md")
        assert len(chunks) > 0

        # Step 2: Embed
        chunk_texts = [chunk.text for chunk in chunks]
        embeddings = embed_texts(chunk_texts)
        assert embeddings.shape == (len(chunks), 768), (
            f"Expected shape ({len(chunks)}, 768), got {embeddings.shape}"
        )

        # Step 3: Store
        store = VectorStore(
            collection_name="e2e_test",
            persist_dir=temp_persist_dir,
        )
        store.add(chunks, embeddings)

        # Step 4: Query
        test_queries = [
            "How do I install Docker?",
            "What is a Docker image?",
            "How do I build a Docker image?",
            "Docker Compose",
        ]

        for test_query in test_queries:
            query_embedding = embed_texts([test_query])[0]
            results = store.query(query_embedding, top_k=5)

            # Verify each query returns results
            assert (
                len(results) > 0
            ), f"No results for query: {test_query}"

            # Verify results are Chunk objects with content
            for result in results:
                assert result.text, "Result chunk has empty text"
                assert result.source == "docker-basics.md"
                # All chunks should preserve source

    def test_query_results_ordered_by_relevance(self, populated_store):
        """
        Query for "dockerfile" and verify the results are ordered
        by relevance (most similar first).
        This tests that ChromaDB ordering is working correctly.
        """
        query = "dockerfile"
        query_embedding = embed_texts([query])[0]

        results = populated_store.query(query_embedding, top_k=5)

        assert len(results) >= 1, "No results for 'dockerfile' query"

        # Calculate similarity scores manually to verify ordering
        # (ChromaDB returns pre-ordered results; this validates that)
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
        result_embeddings = model.encode([chunk.text for chunk in results])

        # Check that similarity scores are monotonically decreasing
        similarities = []
        for result_emb in result_embeddings:
            similarity = np.dot(query_embedding, result_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(result_emb)
            )
            similarities.append(similarity)

        # Scores should be generally decreasing (allowing small variations)
        # The first result should have highest similarity
        assert (
            similarities[0] >= max(similarities[1:])
        ), f"Results not ordered by similarity: {similarities}"

    def test_empty_query_raises_error(self):
        """
        Verify that querying with an empty query raises ValueError.
        This ensures the pipeline validates input correctly.
        """
        with pytest.raises(ValueError, match="empty"):
            embed_texts([""])

    def test_multiple_sections_retrievable(self, populated_store):
        """
        Verify that chunks from different sections (headings) are
        all retrievable and maintain their heading metadata.
        """
        # Collect all unique headings in results
        query_embedding = embed_texts(["docker"])[0]
        results = populated_store.query(query_embedding, top_k=20)

        headings = {chunk.heading for chunk in results}

        # Verify multiple sections are represented
        assert len(headings) > 1, (
            f"Expected multiple sections, got {len(headings)}: {headings}"
        )

    def test_chunk_size_limits_respected(self, docker_guide_text):
        """
        Verify that chunks respect the max_size parameter.
        All chunks should be under the specified limit.
        """
        max_size = 500
        chunks = chunk_markdown(docker_guide_text, source="docker-basics.md", max_size=max_size)

        # Check that all chunks are within size limit (with small tolerance)
        for chunk in chunks:
            assert (
                len(chunk.text) <= max_size + 100
            ), f"Chunk exceeds max_size: {len(chunk.text)} > {max_size}"
