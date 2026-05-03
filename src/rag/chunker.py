"""
Markdown-aware chunking for DevOps guides.

Strategy: split at ## headings first, then recursively split oversized sections.
This prevents the core RAG risk: mixed-tool content in a single retrieval chunk.

See data/guides/ for the corpus this is designed to chunk.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Chunk:
    text: str
    source: str
    heading: str = ""
    metadata: dict = field(default_factory=dict)


def chunk_markdown(text: str, source: str, max_size: int = 500) -> List[Chunk]:
    """
    Split a markdown document into Chunks at heading boundaries.

    Args:
        text: Raw markdown string.
        source: Filename or identifier for the source document.
        max_size: Maximum character length per chunk before further splitting.

    Returns:
        List of Chunk objects. Returns [] for empty or whitespace-only input.

    Raises:
        TypeError: If text or source are not strings.
    """
    raise NotImplementedError
