"""
Planning agent — classifies user queries and routes them to RAG or MCP.

Routing logic:
- Queries containing action verbs ("generate", "create", "write", "make") → MCP tool call
- Everything else → RAG retrieval

This is a keyword classifier for the POC. Replace with an LLM classifier
if precision degrades on ambiguous inputs.

See architecture.md for the full planning agent design.
"""
import shutil
import sys
from enum import Enum
from pathlib import Path

from src.rag.chunker import chunk_markdown  # pylint: disable=import-error
from src.rag.embedder import embed_texts  # pylint: disable=import-error
from src.rag.retriever import retrieve  # pylint: disable=import-error
from src.rag.store import VectorStore  # pylint: disable=import-error


class TaskType(str, Enum):
    RAG = "rag"    # Needs documentation retrieval
    MCP = "mcp"    # Needs a tool action (file generation, log read)


MCP_TRIGGERS = frozenset({
    "generate", "create", "write", "make", "build",
    "produce", "output", "give me a", "show me a",
})


def classify_task(query: str) -> TaskType:
    """
    Classify a user query as needing RAG retrieval or an MCP tool call.

    Args:
        query: User's natural language input. Must be non-empty.

    Returns:
        TaskType.MCP if the query requests file generation or a project action.
        TaskType.RAG if the query requests information or explanation.

    Raises:
        ValueError: If query is empty or whitespace-only.
    """
    # Validate input
    if not query or not query.strip():
        raise ValueError("Query cannot be empty or whitespace-only")

    # Normalize query to lowercase for matching
    normalized = query.lower()

    # Check for RAG information triggers (higher priority)
    rag_triggers = {"how", "what", "explain", "tell", "guide"}
    for trigger in rag_triggers:
        if trigger in normalized:
            return TaskType.RAG

    # Check for MCP action triggers
    for trigger in MCP_TRIGGERS:
        if trigger in normalized:
            return TaskType.MCP

    # Fallback to RAG for ambiguous/single-word queries
    return TaskType.RAG


def run_agent(query: str) -> str:  # pylint: disable=redefined-outer-name
    """
    Execute the planning agent end-to-end: classify task, then run RAG or MCP.

    Args:
        query: User's natural language input. Must be non-empty.

    Returns:
        Formatted response string with cited chunks (RAG) or action status (MCP).

    Raises:
        ValueError: If query is empty or whitespace-only.
    """
    # Classify the query
    task_type = classify_task(query)

    if task_type == TaskType.RAG:
        return _run_rag_pipeline(query)
    return "MCP tasks not yet implemented"


def _run_rag_pipeline(query: str) -> str:  # pylint: disable=redefined-outer-name
    """
    Execute RAG pipeline: load guides, chunk, embed, retrieve, format response.

    Args:
        query: User's natural language input.

    Returns:
        Formatted response with cited chunks, or empty result if no guides found.
    """
    # Find all markdown guide files
    guides_dir = Path(__file__).parent.parent.parent / "data" / "guides"
    guide_files = sorted(guides_dir.glob("*.md"))

    # Handle missing guides gracefully
    if not guide_files:
        return "No guides available."

    # Chunk all guides
    all_chunks = []
    for guide_file in guide_files:
        try:
            text = guide_file.read_text(encoding="utf-8")
            chunks = chunk_markdown(text, source=guide_file.name)
            all_chunks.extend(chunks)
        except (OSError, ValueError):
            # Skip files that can't be read or chunked
            continue

    # Return early if no chunks were created
    if not all_chunks:
        return "No content found in guides."

    # Embed all chunks
    texts = [chunk.text for chunk in all_chunks]
    embeddings = embed_texts(texts)

    # Create temporary vector store
    temp_store_dir = ".chroma-planner"
    try:
        # Clean up any previous store
        if Path(temp_store_dir).exists():
            shutil.rmtree(temp_store_dir)

        # Initialize and populate store
        store = VectorStore(collection_name="guides", persist_dir=temp_store_dir)
        store.add(all_chunks, embeddings)

        # Retrieve top 3 chunks
        retrieved_chunks = retrieve(query, store, top_k=3, rerank=False)

        # Format response with citations
        if not retrieved_chunks:
            return "No relevant guides found for your query."

        response_parts = ["Based on the guides:\n"]
        for chunk in retrieved_chunks:
            response_parts.append(f"\n{chunk.text}")
            response_parts.append(f"\nSource: {chunk.source}\n")

        return "".join(response_parts)
    finally:
        # Clean up temporary store
        if Path(temp_store_dir).exists():
            shutil.rmtree(temp_store_dir)


if __name__ == "__main__":
    query = sys.stdin.read().strip()
    result = run_agent(query)
    print(result)
