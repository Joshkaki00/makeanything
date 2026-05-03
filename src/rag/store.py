"""
ChromaDB vector store wrapper.

Persists to a local directory. In-process — no separate server needed.
See pyproject.toml for chromadb dependency.
"""
from typing import List

import chromadb
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
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=None,  # We provide embeddings explicitly
        )

    def add(self, chunks: List[Chunk], embeddings: np.ndarray) -> None:
        """
        Add chunks and their embeddings to the store.

        Args:
            chunks: List of Chunk objects.
            embeddings: np.ndarray of shape (len(chunks), embedding_dim).

        Raises:
            ValueError: If chunks and embeddings lengths don't match.
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Length mismatch: {len(chunks)} chunks but {len(embeddings)} embeddings"
            )

        # Create deterministic IDs
        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            # Deterministic ID: f"{source}::{heading}::{index}"
            chunk_id = f"{chunk.source}::{chunk.heading}::{i}"
            ids.append(chunk_id)
            documents.append(chunk.text)
            metadatas.append({"heading": chunk.heading, "source": chunk.source})

        # Convert embeddings to list of lists for ChromaDB
        embeddings_list = embeddings.tolist()

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings_list,
            metadatas=metadatas,
            documents=documents,
        )

    def query(self, embedding: np.ndarray, top_k: int = 5) -> List[Chunk]:
        """
        Return the top_k most similar chunks to the query embedding.

        Args:
            embedding: 1-D np.ndarray of shape (embedding_dim,).
            top_k: Number of results to return.

        Returns:
            List of Chunk objects, most similar first.
        """
        # Return empty list if collection is empty
        if self.collection.count() == 0:
            return []

        # Convert embedding to list for ChromaDB
        embedding_list = embedding.tolist()

        # Query the collection
        results = self.collection.query(
            query_embeddings=[embedding_list],
            n_results=top_k,
            include=["documents", "metadatas"],
        )

        # Reconstruct Chunk objects from results
        chunks = []
        if results["ids"] and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                document = results["documents"][0][i]
                metadata = results["metadatas"][0][i]

                chunk = Chunk(
                    text=document,
                    source=metadata.get("source", ""),
                    heading=metadata.get("heading", ""),
                )
                chunks.append(chunk)

        return chunks
