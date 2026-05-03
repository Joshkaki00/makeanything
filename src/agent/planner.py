"""
Planning agent — classifies user queries and routes them to RAG or MCP.

Routing logic:
- Queries containing action verbs ("generate", "create", "write", "make") → MCP tool call
- Everything else → RAG retrieval

This is a keyword classifier for the POC. Replace with an LLM classifier
if precision degrades on ambiguous inputs.

See architecture.md for the full planning agent design.
"""
from enum import Enum


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
