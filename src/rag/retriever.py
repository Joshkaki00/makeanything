"""
Retrieve and rerank chunks for a query.

Pipeline:
  1. Embed the query with embed_texts()
  2. Query the VectorStore for top_k candidates
  3. Rerank with a cross-encoder (cross-encoder/ms-marco-MiniLM-L-6-v2)
  4. Return reranked list

Reranking is optional — pass rerank=False to skip for speed during development.
"""
from typing import List

from .chunker import Chunk
from .embedder import embed_texts
from .store import VectorStore

DEFAULT_RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def retrieve(
    query: str,
    store: VectorStore,
    top_k: int = 5,
    rerank: bool = True,
    rerank_model: str = DEFAULT_RERANK_MODEL,
) -> List[Chunk]:
    """
    Retrieve and optionally rerank the top_k chunks most relevant to query.

    Args:
        query: User's natural language query. Must be non-empty.
        store: Populated VectorStore to search.
        top_k: Number of chunks to return.
        rerank: Whether to apply cross-encoder reranking after retrieval.
        rerank_model: HuggingFace cross-encoder model identifier.

    Returns:
        List of Chunk objects ordered by relevance (most relevant first).
        Returns [] if the store is empty or no chunks match.

    Raises:
        ValueError: If query is empty or whitespace-only.
    """
    raise NotImplementedError
