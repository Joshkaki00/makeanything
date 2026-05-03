# POC Notes

Living document. Update as the project evolves.

---

## What We Built

### Scaffold (current state)
- `src/rag/` — chunker, embedder, ChromaDB store, retriever. All stubs — interfaces defined, `NotImplementedError` raised until implemented.
- `src/mcp_server/` — FastMCP server with `create_dockerfile`, `create_github_actions_workflow`, and `project://log` resource. Tools stubbed.
- `src/agent/planner.py` — task classifier stub (`TaskType.RAG` vs `TaskType.MCP`).
- `tests/` — failing tests written first. All fail with `NotImplementedError`. Implementation makes them green.
- `data/guides/` — beginner Docker guide as the first RAG corpus document.
- `CLAUDE.md`, `.claude/`, `.cursor/` — project memory, hooks, and scoped rules committed.

### Libraries chosen
| Layer | Library | Reason |
|---|---|---|
| Embedding | `sentence-transformers` | Local, free, no API key |
| Model | `nomic-ai/nomic-embed-text-v1.5` | 137M params, runs on CPU |
| Vector store | `chromadb` | In-process, zero infra |
| Chunking | `langchain-text-splitters` | `MarkdownHeaderTextSplitter` splits at headings |
| Reranking | `sentence-transformers` cross-encoder | Same lib, free |
| MCP | `mcp[cli]` + FastMCP | Official SDK, decorator API |

---

## What Worked

_Fill in as implementation proceeds._

- [ ] Markdown heading-aware chunking cleanly separated Docker content from SSH content
- [ ] ChromaDB in-process mode persisted across Python process restarts
- [ ] FastMCP schema generation from type annotations was accurate
- [ ] `nomic-embed-text-v1.5` loaded without GPU and embedded 50 chunks in < N seconds

---

## What Surprised Us

_Fill in as implementation proceeds._

| Surprise | Impact | What we changed |
|---|---|---|
| _(add here)_ | | |

---

## Gotcha Log

_Add every time the agent produces incorrect code. Patterns go to CLAUDE.md._

| Date | Pattern | What happened |
|---|---|---|
| _(add here)_ | | |

---

## Code Documents

### Chunking Strategy
See `src/rag/chunker.py`. Split at `##` headings first via `MarkdownHeaderTextSplitter`, then apply `RecursiveCharacterTextSplitter` at `max_size` within each section. This prevents the core architecture risk: mixed-tool content in one chunk.

### Embedding Pipeline
See `src/rag/embedder.py`. Uses `SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")`. Model downloads once, then runs fully offline. Returns `np.ndarray` of shape `(n, 768)`.

### MCP Tools
See `src/mcp_server/tools.py`. Pure functions — no FastMCP dependency. `server.py` registers them. Tests import from `tools.py` directly.

### Task Routing
See `src/agent/planner.py`. Keyword classifier: phrases like "generate", "create", "write a" → `TaskType.MCP`. Everything else → `TaskType.RAG`. Replace with LLM classifier if precision degrades.
