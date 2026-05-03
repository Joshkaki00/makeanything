"""
FastMCP server entry point.

Registers tools and resources. Run with:
    python -m src.mcp_server.server

Test schema with:
    npx -y @modelcontextprotocol/inspector python -m src.mcp_server.server

IMPORTANT: Always log to stderr, never stdout.
           stdout carries the JSON-RPC stream; writing to it corrupts the protocol.
"""
import sys

from mcp.server.fastmcp import FastMCP

from .resources import get_project_log
from .tools import create_dockerfile, create_github_actions_workflow

mcp = FastMCP("devops-tracker")

# Register tools — descriptions are what Claude reads to decide when/how to call them.
mcp.tool()(create_dockerfile)
mcp.tool()(create_github_actions_workflow)

# Register resources
mcp.resource("project://log")(get_project_log)


if __name__ == "__main__":
    print("devops-tracker MCP server starting on stdio", file=sys.stderr)
    mcp.run(transport="stdio")
