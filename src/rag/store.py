"""
ChromaDB vector store wrapper.

Persists to a local directory. In-process — no separate server needed.
See pyproject.toml for chromadb dependency.
"""
from typing import List

import numpy as np

from .chunker import Chunk

DEFAULT_PERSIST_DIR = ".chroma"


class VectorStore:
    """Thin wrapper around a ChromaDB collection."""

    def __init__(self, collection_name: str, persist_dir: str = DEFAULT_PERSIST_DIR) -> None:
        """
        Initialize or load a named ChromaDB collection.

        Args:
            collection_name: Name of the ChromaDB collection.
            persist_dir: Directory for on-disk persistence.
        """
        raise NotImplementedError

    def add(self, chunks: List[Chunk], embeddings: np.ndarray) -> None:
        """
        Add chunks and their embeddings to the store.

        Args:
            chunks: List of Chunk objects.
            embeddings: np.ndarray of shape (len(chunks), embedding_dim).

        Raises:
            ValueError: If chunks and embeddings lengths don't match.
        """
        raise NotImplementedError

    def query(self, embedding: np.ndarray, top_k: int = 5) -> List[Chunk]:
        """
        Return the top_k most similar chunks to the query embedding.

        Args:
            embedding: 1-D np.ndarray of shape (embedding_dim,).
            top_k: Number of results to return.

        Returns:
            List of Chunk objects, most similar first.
        """
        raise NotImplementedError
