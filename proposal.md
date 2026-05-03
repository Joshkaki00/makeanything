# Proposal: DevOps Learning Tracker

## Problem

Beginners learning DevOps get stuck on the same three problems:

1. **Information is scattered.** Docker docs, GitHub Actions docs, SSH guides, and Nginx references live on separate sites with inconsistent depth.
2. **Context doesn't carry.** Every new terminal session starts cold. There's no record of what the user already set up, what broke, or what they're trying next.
3. **Generic answers don't help.** Stack Overflow answers assume background knowledge. AI assistants hallucinate tool flags that don't exist in the installed version.

## Solution

A lightweight, local assistant that:
- Retrieves answers from a curated, version-aware knowledge base (RAG)
- Remembers what the user is working on across sessions (MCP project log)
- Generates correct config files on demand (MCP file creation tools)
- Breaks tasks into steps grounded in retrieved documentation (planning agent)

The user describes what they're trying to do. The system figures out whether they need information (RAG) or an action (MCP tool), then Claude reasons over the result and responds.

## Patterns

**RAG** — Retrieval-Augmented Generation over a local corpus of beginner DevOps guides. Chunks are split at heading boundaries to avoid mixing Docker content with SSH content in the same retrieval result.

**MCP** — Model Context Protocol server exposing three tools: generate a Dockerfile, generate a GitHub Actions workflow, and read the user's project log. Each tool has a typed schema so Claude calls them correctly.

## Success Criteria

1. A query about Docker returns steps grounded in the local Docker guide, not hallucinated flag names.
2. A request to "generate a Dockerfile for Python 3.11 on port 8000" produces a syntactically valid Dockerfile.
3. The project log persists across sessions and appears in Claude's context when relevant.
4. The chunker never produces a chunk that mixes content from two different H2 sections.
5. All tests pass with `pytest`. The linter passes with `ruff check .`.

## Scope

This is a local, single-user tool. No authentication, no deployment, no database beyond ChromaDB. The MCP server runs over `stdio`.
