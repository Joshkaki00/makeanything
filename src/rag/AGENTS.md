# RAG Module — Agent Instructions

Scoped to `src/rag/`. These instructions override root AGENTS.md for RAG work.

**One agent, one concern.** Work in this module only. If a task also touches `src/mcp_server/` or `src/agent/`, stop and split it — use a separate subagent for each module.

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

**Test boundaries, not the middle.** Happy path is the minimum. Required edge cases:
- `chunk_markdown("", source)` → returns `[]`, does not raise
- `embed_texts([])` → raises `ValueError`
- `embed_texts(["  "])` → raises `ValueError` (whitespace-only)
- `store.query(embedding, top_k=0)` → raises `ValueError`
- `retrieve("", store)` → raises `ValueError`

**Never trust library behavior.** If `MarkdownHeaderTextSplitter` or `SentenceTransformer` is upgraded, re-verify output shapes. Use context7 MCP to check current API if behavior changes unexpectedly.
