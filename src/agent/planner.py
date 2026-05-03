"""
Planning agent — classifies user queries and routes them to RAG or MCP.

Routing logic:
- Queries containing action verbs ("generate", "create", "write", "make") → MCP tool call
- Everything else → RAG retrieval

This is a keyword classifier for the POC. Replace with an LLM classifier
if precision degrades on ambiguous inputs.

See architecture.md for the full planning agent design.
"""
import re
import shutil
import sys
from enum import Enum
from pathlib import Path

from src.mcp_server.tools import (  # pylint: disable=import-error
    create_dockerfile,
    create_github_actions_workflow,
)
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


def classify_task(query: str) -> TaskType:  # pylint: disable=redefined-outer-name
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
    return _run_mcp_pipeline(query)


def _extract_dockerfile_params(query: str) -> tuple[str, int]:  # pylint: disable=redefined-outer-name
    """
    Extract Dockerfile parameters from user query.

    Args:
        query: User's natural language input.

    Returns:
        Tuple of (base_image, port). Uses defaults if not found in query.
    """
    # Default values
    base_image = "python:3.11-slim"
    port = 8000

    normalized = query.lower()

    # Extract base image (look for patterns like "python:3.11", "node:18", etc.)
    # Match "word:digits" pattern
    image_match = re.search(r"\b([a-z]+):(\d+(?:\.\d+)?(?:-\w+)?)\b", normalized)
    if image_match:
        base_image = f"{image_match.group(1)}:{image_match.group(2)}"

    # Extract port number (look for "port XXXX" or just a 4-5 digit number)
    port_match = re.search(r"port\s+(\d+)", normalized)
    if port_match:
        extracted_port = int(port_match.group(1))
        # Validate port range
        if 1 <= extracted_port <= 65535:
            port = extracted_port

    return base_image, port


def _extract_workflow_params(query: str) -> tuple[str, str]:  # pylint: disable=redefined-outer-name
    """
    Extract GitHub Actions workflow parameters from user query.

    Args:
        query: User's natural language input.

    Returns:
        Tuple of (trigger, python_version). Uses defaults if not found in query.
    """
    # Default values
    trigger = "push"
    python_version = "3.11"

    normalized = query.lower()

    # Extract trigger type
    if "pull_request" in normalized or "pull request" in normalized:
        trigger = "pull_request"
    elif "schedule" in normalized or "scheduled" in normalized:
        trigger = "workflow_dispatch"  # Use workflow_dispatch for manual triggers
    # Default "push" is already set

    # Extract Python version (look for "python 3.X", "py 3.X", or just "3.X")
    version_match = re.search(r"(?:python|py)\s*(\d+\.\d+)", normalized)
    if version_match:
        python_version = version_match.group(1)
    else:
        # Try to find standalone version like "3.12"
        version_match = re.search(r"\b(\d+\.\d+)\b", normalized)
        if version_match:
            potential_version = version_match.group(1)
            # Only accept if it looks like a Python version (3.x, 4.x)
            if potential_version.startswith("3.") or potential_version.startswith("4."):
                python_version = potential_version

    return trigger, python_version


def _detect_tool_type(query: str) -> str:  # pylint: disable=redefined-outer-name
    """
    Detect which MCP tool to use based on query keywords.

    Args:
        query: User's natural language input.

    Returns:
        Tool name: "dockerfile" or "github_actions"
    """
    normalized = query.lower()

    # Dockerfile triggers
    dockerfile_triggers = {"dockerfile", "docker", "containerize", "container"}
    for trigger in dockerfile_triggers:
        if trigger in normalized:
            return "dockerfile"

    # GitHub Actions triggers
    github_triggers = {"github actions", "ci/cd", "workflow", "pipeline", "github"}
    for trigger in github_triggers:
        if trigger in normalized:
            return "github_actions"

    # Default to dockerfile if uncertain
    return "dockerfile"


def _run_mcp_pipeline(query: str) -> str:  # pylint: disable=redefined-outer-name
    """
    Execute MCP pipeline: detect tool, extract params, call tool, return formatted output.

    Args:
        query: User's natural language input.

    Returns:
        Formatted response with tool name and output.
    """
    try:
        tool_type = _detect_tool_type(query)

        if tool_type == "dockerfile":
            base_image, port = _extract_dockerfile_params(query)
            result = create_dockerfile(base_image=base_image, port=port)
            return f"MCP Tool: create_dockerfile\n\n{result}"

        # Default to GitHub Actions
        trigger, python_version = _extract_workflow_params(query)
        result = create_github_actions_workflow(trigger=trigger, python_version=python_version)
        return f"MCP Tool: create_github_actions_workflow\n\n{result}"
    except ValueError as e:
        return f"Error executing MCP tool: {e}"


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
