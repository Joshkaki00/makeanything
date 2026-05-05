# makeanything

## Project
Beginner DevOps Learning Tracker — RAG pipeline over curated DevOps guides (Docker, GitHub Actions, SSH, Nginx, AWS EC2) + MCP server for file generation and project logging. See `architecture.md` for the full design.

## Stack
- Python (RAG pipeline: chunking, embedding, retrieval, reranking)
- MCP server (project log resource, file creation tools, external docs API)
- Planning agent that routes tasks to RAG or MCP

## Key Files
- `spec.md` — quality gates and acceptance criteria
- `proposal.md` — problem statement and success criteria
- `poc-notes.md` — what worked, surprises, gotcha log
- `src/rag/` — chunker, embedder, ChromaDB store, retriever
- `src/mcp_server/` — FastMCP server, tools, resources
- `src/agent/planner.py` — task classifier (RAG vs MCP)
- `data/guides/` — DevOps guide corpus for RAG
- `tests/` — failing tests written before implementation

## Workflow

**Test first.** Write the failing test before the implementation. Commit the test before the code that makes it pass.

**Test boundaries, not the middle.** Agents handle the happy path. They miss edge cases: empty inputs, null values, large data, concurrent access, timezone edge cases. Cover those explicitly.

**One agent, one concern.** Split tasks that cross system boundaries (RAG vs MCP, frontend vs backend) into subagents. Each stays focused and produces cleaner output.

**Never trust, always verify.** AI-generated code can look correct and be subtly wrong — hallucinated imports, deprecated methods, silent error swallowing. Read every diff. Run the code with real inputs.

**Check external references.** If the agent uses a library you haven't seen, verify it exists and does what the agent claims. Use [context7] MCP to fetch live docs — do not accept the agent's description as proof.

**Run `/verify` before merging** any code that touches an external package, API endpoint, or service.

## Gotcha Log
Add failures here when patterns emerge. Keep this current.

| Pattern | What happened |
|---------|---------------|
| _(none yet — add as they occur)_ | |

## Commands
- `/verify` — pre-merge verification checklist
- `/review` — structured review focused on boundaries and edge cases

## Environment
**Always use the project venv.** Never use global `python`, `pip`, `pytest`, `ruff`, or `pylint`.
```
venv/bin/python    venv/bin/pip
venv/bin/pytest    venv/bin/ruff    venv/bin/pylint
```
Venv: Python 3.13.3 at `venv/`. Hooks enforce this — bare tool calls are auto-corrected (Cursor) or blocked (Claude Code).

## Hard Rules
These are enforced by hooks. They are listed here only so the agent knows not to attempt them:
- No direct push to `main` or `master`
- No `console.log` left in production JS/TS paths
- No bare `python`/`pip`/`pytest` — always use `venv/bin/`

## Formatting
Formatting rules live in the linter config, not here. Do not add style guidance to this file.
