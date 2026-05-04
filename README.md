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

## Module Progress

| Module | Score |
|---|---|
| Knowledge Check: MCP Fundamentals, Servers & Integrations | 100% |
| Knowledge Check: Retrieval-Augmented Generation (RAG) | 100% |
| End Course Knowledge Check: Building RAG and MCP Servers with Claude | 100% |

![MCP Fundamentals knowledge check — 100%](images/Screenshot%202026-05-03%20at%2017-09-50%20Knowledge%20Check%20MCP%20Fundamentals%20Servers%20%26%20Integrations%20Coursera.png)

![RAG knowledge check — 100%](images/Screenshot%202026-05-03%20at%2017-10-17%20Knowledge%20Check%20Retrieval-Augmented%20Generation%20(RAG)%20Coursera.png)

![End course knowledge check — 100%](images/Screenshot%202026-05-03%20at%2013-44-29%20End%20Course%20Knowledge%20Check%20Building%20RAG%20and%20MCP%20Servers%20with%20Claude%20Coursera.png)

## Certificate

![Mastering Claude AI: Prompting, APIs, RAG, and MCP — Specialization Certificate](images/Coursera%20UI5PSGN7SRGJ.jpg)
