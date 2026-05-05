# Project Agent Instructions

## Project
Beginner DevOps Learning Tracker — RAG pipeline + MCP server. See `architecture.md` for design, `spec.md` for acceptance criteria.

## Test First
Write the failing test before the implementation. Commit the test. Then implement. Confirm red → green in commit history.

## Test Boundaries, Not the Middle
Agents handle the happy path well. They miss the edges. Every test suite must cover:
- Empty inputs, null/None values, whitespace-only strings
- Boundary values (off-by-one, max/min int, port 0, port 65536)
- Large data (many chunks, long strings)
- Invalid types and malformed inputs

If your test passes immediately without implementation, the test is wrong or already covered elsewhere.

## Run the Code
Reading AI-generated code is not enough. Execute it. Watch what happens with real inputs. Many bugs only surface at runtime — wrong shapes, silent exception swallowing, unexpected None returns.

## Never Trust, Always Verify
AI-generated code can look correct and be subtly wrong:
- Hallucinated imports (library doesn't exist or doesn't export what was called)
- Deprecated or nonexistent API methods
- Silent error swallowing in except blocks
- Wrong assumptions about return shapes or types

## Check External References
If the agent uses a library or API you haven't seen, verify it before using it:
1. Does the package exist on PyPI?
2. Does the function/method exist in the installed version?
3. Does it behave as described — or just as the agent claimed?

Use the **context7 MCP** to fetch live documentation. Do not rely on the agent's description alone.

## One Agent, One Concern
If a task touches multiple unrelated systems (RAG pipeline, MCP server, planning agent), split it across subagents. Each one stays focused and produces cleaner output. Never implement across modules in a single agent pass.

## Complexity Tiers

**Small** (single function or class, < 50 lines): Direct agent, no subagents.

**Medium** (one module, one concern): Single focused subagent. Scope: `src/rag/` OR `src/mcp_server/`, not both.

**Large** (cross-module or integration work): Orchestrator decomposes. Each subagent gets its own worktree:
```bash
claude -w rag-impl "implement src/rag/chunker.py to make tests/rag/test_chunker.py pass"
claude -w mcp-impl "implement src/mcp_server/tools.py to make tests/mcp_server/test_tools.py pass"
```
Orchestrator reviews and merges. Never implement across modules in one agent pass.

## Python Environment
**Always use the project venv.** Never invoke global `python`, `pip`, `pytest`, `ruff`, `pylint`, or `mypy`.

| Task | Command |
|------|---------|
| Run tests | `venv/bin/pytest tests/ -v` |
| Lint | `venv/bin/ruff check . && venv/bin/pylint src/` |
| Install a package | `venv/bin/pip install <pkg>` |
| Run a script | `venv/bin/python src/...` |

Hooks enforce this. Cursor silently rewrites bare calls. Claude Code blocks them with the correct command.

## Verification
Run `/verify` before merging. Run `/review` when touching external packages or APIs.

## Module Instructions
Each module has a scoped `AGENTS.md`:
- `src/rag/AGENTS.md` — chunking, embedding, retrieval conventions
- `src/mcp_server/AGENTS.md` — MCP tool design rules
