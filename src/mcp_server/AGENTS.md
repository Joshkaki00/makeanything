# MCP Server Module — Agent Instructions

Scoped to `src/mcp_server/`. These instructions override root AGENTS.md for MCP work.

## Tool Design Rules
- One tool, one concern. `create_dockerfile` generates Dockerfiles. Nothing else.
- Pure functions in `tools.py`. No FastMCP import in `tools.py`. Tests import tools directly.
- `server.py` registers tools with `mcp.tool()(func)`. Do not duplicate logic there.
- Validate all inputs at the top of every function before any string construction.
- Return `str` only. Never return dicts, lists, or None from a tool.

## Input Validation
- Empty string → `raise ValueError(f"<param_name> must not be empty")`
- Port out of range → `raise ValueError(f"port must be 1–65535, got {port}")`
- Unknown trigger → `raise ValueError(f"trigger must be one of {VALID_TRIGGERS}, got '{trigger}'")`

## Logging
- **NEVER write to stdout.** stdout carries the JSON-RPC stream.
- Use `print("...", file=sys.stderr)` or Python `logging` to stderr only.

## Schema Quality
Tool docstrings are what Claude reads to decide when and how to call each tool.
- First sentence: what the tool does.
- Args section: one line per param with type and valid values.
- Raises section: what inputs cause errors.
Vague descriptions produce wrong calls.

## Resources
- Resources are read-only. `get_project_log` reads a file. Never modifies it.
- `append_to_project_log` is a helper — not an MCP resource, not an MCP tool.

## Testing
Import from `tools.py` and `resources.py` directly. Never instantiate `FastMCP` in tests.
