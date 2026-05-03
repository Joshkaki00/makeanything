# DevOps Learning Tracker

A beginner-friendly DevOps learning system that combines retrieval-augmented generation (RAG) over curated guides with code generation via tool execution.

## Core Patterns

**RAG Pipeline:** Retrieves relevant chunks from a corpus of DevOps guides, embeds them using nomic-embed-text-v1.5, and returns grounded answers with citations — no hallucinations.

**MCP Pipeline:** Detects generation requests (create, build, generate), extracts parameters from natural language, and executes tools to produce Dockerfiles and GitHub Actions workflows.

## Quick Start

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the demo:
```bash
venv/bin/python demo.py
```

Run tests:
```bash
venv/bin/pytest tests/
```

## Project Layout

| Directory/File | Purpose |
|---|---|
| `src/rag/` | Chunking, embedding, vector storage, retrieval (ChromaDB + nomic embeddings) |
| `src/mcp_server/` | FastMCP server, tool definitions, project log resource |
| `src/agent/` | Planning agent: task classification and pipeline routing |
| `tests/` | Unit tests (71 passing), integration tests (9 deselected by default) |
| `data/guides/` | 5 DevOps guides: Docker, GitHub Actions, SSH, Nginx, AWS EC2 |
| `spec.md` | Quality gates and acceptance criteria (all 3 verified) |
| `poc-notes.md` | Implementation decisions, gotcha log, what worked and surprised us |
| `demo.py` | Executable end-to-end demo: RAG, MCP, interactive, and single-query modes |
| `CLAUDE.md` | Project workflows, hard rules, testing discipline |
