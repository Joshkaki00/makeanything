# Spec: DevOps Learning Tracker

## Quality Gates

### Gate 1 — Unit tests pass
**Invoke:** `pytest tests/ -v`
**Success:** All tests pass. Zero failures, zero errors. Exit code 0.
**Covers:** chunking logic, embedding shape, tool input validation, task classification.

### Gate 2 — MCP server tools are schema-valid
**Invoke:** `npx -y @modelcontextprotocol/inspector python -m src.mcp_server.server`
**Success:** Inspector lists `create_dockerfile`, `create_github_actions_workflow`, and resource `project://log`. Each tool shows typed parameters with descriptions. No "unknown" or empty schemas.

### Gate 3 — End-to-end grounded response
**Invoke:** `echo "How do I containerize a Python app?" | python -m src.agent.planner`
**Success:** Output contains at least one cited chunk from `data/guides/docker-basics.md`. Response does not hallucinate a Docker flag or command not present in the guide.

---

## Acceptance Criteria

**AC-1: RAG retrieval is grounded**
- Given the `docker-basics.md` guide is indexed in the vector store
- When the user queries "how do I write a Dockerfile for Python"
- Then at least one retrieved chunk originates from `docker-basics.md` and the response cites it

**AC-2: Empty input is rejected cleanly**
- Given an empty string is passed as a query
- When any pipeline entry point receives it (chunker, embedder, retriever, planner)
- Then a `ValueError` is raised with a message describing what was missing — no silent return, no AttributeError

**AC-3: Dockerfile generation is syntactically correct**
- Given `base_image="python:3.11-slim"` and `port=8000`
- When `create_dockerfile` is called
- Then the output string contains `FROM python:3.11-slim`, `EXPOSE 8000`, and `WORKDIR` — and `docker build` on the output exits 0

**AC-4: Chunker never crosses heading boundaries**
- Given a markdown file with three distinct `##` sections
- When `chunk_markdown` is called
- Then no returned `Chunk` contains text from more than one `##` section, verified by asserting each section's unique keyword appears in exactly one chunk

**AC-5: Retriever returns empty list — not an error — when nothing matches**
- Given a query about a topic not in the knowledge base (e.g., "kubernetes helm charts")
- When `retrieve` is called against the indexed DevOps guides
- Then the return value is an empty list `[]` and no exception is raised

**AC-6: MCP tools validate inputs before executing**
- Given `create_dockerfile` is called with `base_image=""` or `port=0`
- When the tool receives the call
- Then it raises `ValueError` before any string construction — no partial outputs

---

## Test Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Lint (style + imports)
ruff check .

# Lint (logic + errors)
pylint src/

# Type check (stretch goal)
mypy src/

# Inspect MCP server
npx -y @modelcontextprotocol/inspector python -m src.mcp_server.server
```
