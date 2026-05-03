"""
Markdown-aware chunking for DevOps guides.

Strategy: split at ## headings first, then recursively split oversized sections.
This prevents the core RAG risk: mixed-tool content in a single retrieval chunk.

See data/guides/ for the corpus this is designed to chunk.
"""
from dataclasses import dataclass, field
from typing import List

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


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
    if not isinstance(text, str) or not isinstance(source, str):
        raise TypeError("text and source must be strings")

    # Handle empty or whitespace-only input
    if not text.strip():
        return []

    # First pass: split at ## headings
    headers_to_split_on = [("##", "heading")]
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    header_splits = header_splitter.split_text(text)

    # Second pass: for sections exceeding max_size, use recursive splitting
    chunks = []
    for doc in header_splits:
        chunk_text = doc.page_content.strip()
        chunk_heading = doc.metadata.get("heading", "")

        if not chunk_text:
            continue

        # If the section is small enough, create a single chunk
        if len(chunk_text) <= max_size:
            chunks.append(
                Chunk(
                    text=chunk_text,
                    source=source,
                    heading=chunk_heading,
                )
            )
        else:
            # For oversized sections, use recursive character splitting
            recursive_splitter = RecursiveCharacterTextSplitter(
                chunk_size=max_size,
                chunk_overlap=50,
                separators=["\n\n", "\n", " ", ""],
            )
            sub_chunks = recursive_splitter.split_text(chunk_text)
            for sub_text in sub_chunks:
                if sub_text.strip():
                    chunks.append(
                        Chunk(
                            text=sub_text.strip(),
                            source=source,
                            heading=chunk_heading,
                        )
                    )

    return chunks
