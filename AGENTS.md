# Project Agent Instructions

## Project
Beginner DevOps Learning Tracker — RAG pipeline + MCP server. See `architecture.md` for design, `spec.md` for acceptance criteria.

## Test First
Write the failing test before the implementation. Commit the test. Then implement. Confirm red → green in commit history.

## Complexity Tiers

**Small** (single function or class, < 50 lines): Direct agent, no subagents.

**Medium** (one module, one concern): Single focused subagent. Scope: `src/rag/` OR `src/mcp_server/`, not both.

**Large** (cross-module or integration work): Orchestrator decomposes. Each subagent gets its own worktree:
```bash
claude -w rag-impl "implement src/rag/chunker.py to make tests/rag/test_chunker.py pass"
claude -w mcp-impl "implement src/mcp_server/tools.py to make tests/mcp_server/test_tools.py pass"
```
Orchestrator reviews and merges. Never implement across modules in one agent pass.

## Verification
Run `/verify` before merging. Run `/review` when touching external packages or APIs.

## Module Instructions
Each module has a scoped `AGENTS.md`:
- `src/rag/AGENTS.md` — chunking, embedding, retrieval conventions
- `src/mcp_server/AGENTS.md` — MCP tool design rules
