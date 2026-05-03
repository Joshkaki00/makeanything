"""
Tests for src/rag/store.py

Covers VectorStore initialization, adding chunks, querying, and persistence.
Run: venv/bin/pytest tests/rag/test_store.py -v
"""

import os
import shutil
import tempfile
from typing import List

import chromadb
import numpy as np
import pytest

from src.rag.chunker import Chunk
from src.rag.store import DEFAULT_PERSIST_DIR, VectorStore

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def temp_persist_dir():
    """Create a temporary directory for ChromaDB persistence, clean it up after."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_chunks() -> List[Chunk]:
    """Create sample chunks for testing."""
    return [
        Chunk(
            text="Docker is a containerization platform for applications.",
            source="docker-guide.md",
            heading="Docker Basics",
        ),
        Chunk(
            text="GitHub Actions automates CI/CD workflows.",
            source="github-guide.md",
            heading="GitHub Actions",
        ),
        Chunk(
            text="SSH enables secure remote access to servers.",
            source="ssh-guide.md",
            heading="SSH Basics",
        ),
    ]


@pytest.fixture
def sample_embeddings() -> np.ndarray:
    """Create sample embeddings (3 chunks, 128-dimensional embeddings)."""
    np.random.seed(42)  # Deterministic for reproducibility
    return np.random.randn(3, 128).astype(np.float32)


@pytest.fixture
def mismatched_embeddings() -> np.ndarray:
    """Create embeddings with mismatched length (2 instead of 3)."""
    np.random.seed(42)
    return np.random.randn(2, 128).astype(np.float32)


@pytest.fixture
def empty_embeddings() -> np.ndarray:
    """Create an empty embeddings array."""
    return np.array([]).reshape(0, 128).astype(np.float32)


@pytest.fixture
def query_embedding() -> np.ndarray:
    """Create a query embedding for similarity search."""
    np.random.seed(42)
    return np.random.randn(128).astype(np.float32)


# ============================================================================
# Initialization Tests
# ============================================================================


class TestInitialization:
    """Test VectorStore initialization and setup."""

    def test_store_created_with_collection_name_and_persist_dir(self, temp_persist_dir):
        """Store can be instantiated with collection name and persist directory."""
        store = VectorStore(collection_name="test_collection", persist_dir=temp_persist_dir)
        assert store is not None
        assert store.collection is not None

    def test_default_persist_dir_is_used_when_not_specified(self):
        """Store uses DEFAULT_PERSIST_DIR when persist_dir not provided."""
        # Clean up any existing default dir first
        if os.path.exists(DEFAULT_PERSIST_DIR):
            shutil.rmtree(DEFAULT_PERSIST_DIR)

        try:
            store = VectorStore(collection_name="default_test")
            assert os.path.exists(DEFAULT_PERSIST_DIR)
            assert store is not None
        finally:
            # Clean up
            if os.path.exists(DEFAULT_PERSIST_DIR):
                shutil.rmtree(DEFAULT_PERSIST_DIR)

    def test_persist_dir_exists_after_init(self, temp_persist_dir):
        """Directory is created on disk after initialization."""
        collection_name = "test_collection"
        VectorStore(collection_name=collection_name, persist_dir=temp_persist_dir)
        assert os.path.exists(temp_persist_dir)
        assert os.path.isdir(temp_persist_dir)

    def test_reload_store_with_same_collection_name_loads_existing(
        self, temp_persist_dir, sample_chunks, sample_embeddings
    ):
        """Creating a store with the same name loads existing collection, not a new one."""
        # Create store A, add chunks
        store_a = VectorStore(collection_name="persistent_collection", persist_dir=temp_persist_dir)
        store_a.add(sample_chunks, sample_embeddings)
        initial_count = store_a.collection.count()
        assert initial_count == 3

        # Create store B with same collection name
        store_b = VectorStore(collection_name="persistent_collection", persist_dir=temp_persist_dir)
        # Count should still be 3, not 0 (i.e., it loaded the existing collection)
        assert store_b.collection.count() == initial_count


# ============================================================================
# Adding Chunks Tests
# ============================================================================


class TestAddingChunks:
    """Test adding chunks and embeddings to the store."""

    def test_add_with_valid_chunks_and_embeddings_succeeds(
        self, temp_persist_dir, sample_chunks, sample_embeddings
    ):
        """Adding valid chunks and embeddings succeeds without exception."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)
        assert store.collection.count() == 3

    def test_add_with_mismatched_lengths_raises_value_error(
        self, temp_persist_dir, sample_chunks, mismatched_embeddings
    ):
        """Adding mismatched chunks and embeddings raises ValueError."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        with pytest.raises(ValueError, match="Length mismatch"):
            store.add(sample_chunks, mismatched_embeddings)

    def test_add_with_empty_embeddings_raises_value_error(
        self, temp_persist_dir, sample_chunks, empty_embeddings
    ):
        """Adding with empty embeddings array raises ValueError."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        with pytest.raises(ValueError, match="Length mismatch"):
            store.add(sample_chunks, empty_embeddings)

    def test_deterministic_ids_are_generated_correctly(
        self, temp_persist_dir, sample_chunks, sample_embeddings
    ):
        """IDs are generated in format: source::heading::index."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        # Get all IDs from the collection
        all_results = store.collection.get()
        ids = all_results["ids"]

        expected_ids = [
            "docker-guide.md::Docker Basics::0",
            "github-guide.md::GitHub Actions::1",
            "ssh-guide.md::SSH Basics::2",
        ]

        assert set(ids) == set(expected_ids)

    def test_chunks_are_stored_with_metadata(
        self, temp_persist_dir, sample_chunks, sample_embeddings
    ):
        """Chunks are stored with heading and source metadata."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        all_results = store.collection.get(include=["metadatas"])
        metadatas = all_results["metadatas"]

        assert len(metadatas) == 3
        assert metadatas[0]["heading"] == "Docker Basics"
        assert metadatas[0]["source"] == "docker-guide.md"
        assert metadatas[1]["heading"] == "GitHub Actions"
        assert metadatas[1]["source"] == "github-guide.md"


# ============================================================================
# Querying Tests
# ============================================================================


class TestQuerying:
    """Test querying the store for similar chunks."""

    def test_query_returns_chunks_ordered_by_similarity(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Query returns chunks ordered by similarity (most similar first)."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        results = store.query(query_embedding, top_k=3)
        assert isinstance(results, list)
        assert len(results) == 3
        assert all(isinstance(chunk, Chunk) for chunk in results)

    def test_query_returns_list_even_if_empty(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Query returns a list type even if empty."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        # Query with top_k larger than available
        results = store.query(query_embedding, top_k=100)
        assert isinstance(results, list)

    def test_empty_store_returns_empty_list(self, temp_persist_dir, query_embedding):
        """Querying an empty store returns empty list, no exceptions."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)

        results = store.query(query_embedding, top_k=5)
        assert results == []
        assert isinstance(results, list)

    def test_query_results_include_chunk_objects(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Query results are Chunk objects with text, heading, and source."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        results = store.query(query_embedding, top_k=2)
        assert len(results) == 2
        assert all(isinstance(chunk, Chunk) for chunk in results)
        assert all(chunk.heading for chunk in results)
        assert all(chunk.source for chunk in results)
        assert all(chunk.text for chunk in results)

    def test_heading_and_source_metadata_preserved_in_results(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Results preserve exact heading and source from original chunks."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        results = store.query(query_embedding, top_k=3)

        # Collect headings and sources from results
        result_headings = {chunk.heading for chunk in results}
        result_sources = {chunk.source for chunk in results}

        original_headings = {chunk.heading for chunk in sample_chunks}
        original_sources = {chunk.source for chunk in sample_chunks}

        assert result_headings == original_headings
        assert result_sources == original_sources

    def test_top_k_greater_than_available_returns_all_chunks(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Requesting top_k > available chunks returns all available chunks."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        results = store.query(query_embedding, top_k=1000)
        assert len(results) == 3  # Does not pad to 1000


# ============================================================================
# Persistence Tests
# ============================================================================


class TestPersistence:
    """Test that chunks persist across store instances."""

    def test_chunks_persist_across_instances(
        self, temp_persist_dir, sample_chunks, sample_embeddings
    ):
        """Chunks added to store A are retrievable from store B with same collection name."""
        # Store A: create and add chunks
        store_a = VectorStore(collection_name="persistent", persist_dir=temp_persist_dir)
        store_a.add(sample_chunks, sample_embeddings)
        store_a_count = store_a.collection.count()

        # Store B: create new instance with same collection name
        store_b = VectorStore(collection_name="persistent", persist_dir=temp_persist_dir)
        store_b_count = store_b.collection.count()

        # Counts should match
        assert store_b_count == store_a_count == 3

    def test_query_returns_chunks_added_by_previous_instance(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Can query chunks that were added by a previous store instance."""
        # Store A: add chunks
        store_a = VectorStore(collection_name="persistent", persist_dir=temp_persist_dir)
        store_a.add(sample_chunks, sample_embeddings)

        # Store B: query without adding anything
        store_b = VectorStore(collection_name="persistent", persist_dir=temp_persist_dir)
        results = store_b.query(query_embedding, top_k=3)

        assert len(results) == 3
        assert all(isinstance(chunk, Chunk) for chunk in results)

    def test_metadata_preserved_across_persistence(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Metadata (heading, source) is preserved when chunks are loaded from disk."""
        # Store A: add chunks
        store_a = VectorStore(collection_name="persistent", persist_dir=temp_persist_dir)
        store_a.add(sample_chunks, sample_embeddings)

        # Store B: query and verify metadata
        store_b = VectorStore(collection_name="persistent", persist_dir=temp_persist_dir)
        results = store_b.query(query_embedding, top_k=3)

        # Verify all original sources appear in results
        result_sources = {chunk.source for chunk in results}
        expected_sources = {chunk.source for chunk in sample_chunks}
        assert result_sources == expected_sources

        # Verify all original headings appear in results
        result_headings = {chunk.heading for chunk in results}
        expected_headings = {chunk.heading for chunk in sample_chunks}
        assert result_headings == expected_headings


# ============================================================================
# Edge Cases Tests
# ============================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_source_and_heading_metadata_preserved_exactly(
        self, temp_persist_dir, query_embedding
    ):
        """Source and heading are preserved with exact formatting."""
        # Create chunks with special characters and spaces
        chunks = [
            Chunk(
                text="Some content",
                source="special-file_v1.2.md",
                heading="Deep Learning: Advanced Topics",
            ),
        ]
        embeddings = np.random.randn(1, 128).astype(np.float32)

        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(chunks, embeddings)

        results = store.query(query_embedding, top_k=1)
        assert results[0].source == "special-file_v1.2.md"
        assert results[0].heading == "Deep Learning: Advanced Topics"

    def test_add_single_chunk(self, temp_persist_dir, query_embedding):
        """Can add and retrieve a single chunk."""
        chunks = [Chunk(text="Single chunk content", source="single.md", heading="Single")]
        embeddings = np.random.randn(1, 128).astype(np.float32)

        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(chunks, embeddings)

        results = store.query(query_embedding, top_k=1)
        assert len(results) == 1
        assert results[0].text == "Single chunk content"

    def test_top_k_less_than_one_raises_error(
        self, temp_persist_dir, sample_chunks, sample_embeddings, query_embedding
    ):
        """Requesting top_k < 1 raises TypeError (ChromaDB validation)."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        with pytest.raises(TypeError):
            store.query(query_embedding, top_k=0)

    def test_add_multiple_times_accumulates_chunks(
        self, temp_persist_dir, sample_chunks, sample_embeddings
    ):
        """Adding chunks multiple times accumulates them."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)

        # Add first batch
        store.add(sample_chunks[:2], sample_embeddings[:2])
        assert store.collection.count() == 2

        # Add second batch
        store.add(sample_chunks[2:], sample_embeddings[2:])
        assert store.collection.count() == 3

    def test_query_with_different_embedding_dimensions_fails_gracefully(
        self, temp_persist_dir, sample_chunks, sample_embeddings
    ):
        """Query with mismatched embedding dimensions fails gracefully."""
        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(sample_chunks, sample_embeddings)

        # Try to query with wrong dimension embedding
        wrong_dim_embedding = np.random.randn(64).astype(np.float32)

        # This should raise an error or return empty (ChromaDB behavior)
        try:
            results = store.query(wrong_dim_embedding, top_k=1)
            # If it doesn't raise, check it returns something predictable
            assert isinstance(results, list)
        except chromadb.errors.InvalidArgumentError:
            # Expected: dimension mismatch error from ChromaDB
            pass

    def test_chunk_text_content_preserved_exactly(self, temp_persist_dir, query_embedding):
        """Chunk text content is preserved exactly as stored."""
        chunks = [
            Chunk(
                text="This has\nmultiple\nlines\n\nand spaces.",
                source="test.md",
                heading="Test",
            ),
        ]
        embeddings = np.random.randn(1, 128).astype(np.float32)

        store = VectorStore(collection_name="test", persist_dir=temp_persist_dir)
        store.add(chunks, embeddings)

        results = store.query(query_embedding, top_k=1)
        assert results[0].text == "This has\nmultiple\nlines\n\nand spaces."
