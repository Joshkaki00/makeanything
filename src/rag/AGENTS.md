# RAG Module — Agent Instructions

Scoped to `src/rag/`. These instructions override root AGENTS.md for RAG work.

## Chunking Rules
- Always split at `##` headings first. Never merge content from two different headings into one chunk.
- Use `MarkdownHeaderTextSplitter` for heading splits, `RecursiveCharacterTextSplitter` for secondary splits.
- The `source` field on every `Chunk` must be the filename — not a path, not a URL.
- Default `max_size=500` characters. Adjust in tests if guides have unusually long sections.

## Embedding Rules
- Model: `nomic-ai/nomic-embed-text-v1.5` only. **No OpenAI, no Cohere, no paid APIs.**
- Always validate input before calling `model.encode()`. Empty list → raise `ValueError`.
- Return `np.ndarray`, not a list. Shape must be `(n, dim)`.

## Store Rules
- ChromaDB only. No Pinecone, no Qdrant for this project.
- Persist to `.chroma/` (gitignored). Never hardcode an absolute path.
- IDs must be deterministic: `f"{source}::{heading}::{index}"`.

## Retriever Rules
- Default `top_k=5`. Never exceed `top_k=20`.
- Reranking is optional (`rerank=True` default). Skip with `rerank=False` for tests.
- Return `[]` for no results — never raise an exception when the store is empty.
- Raise `ValueError` for empty or whitespace-only queries.

## Test Pattern
Each function has its own test file. Tests mock the model — do not load real weights in unit tests.
