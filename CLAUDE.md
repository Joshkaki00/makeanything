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

**One agent, one concern.** Split tasks that cross system boundaries (RAG vs MCP, frontend vs backend) into subagents. Each stays focused.

**Verify before trusting.** For every external package or API the agent uses, confirm: does the package exist? Does the method exist in that version? Check the live docs — do not accept the agent's description as proof.

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
