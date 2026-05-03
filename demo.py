#!/usr/bin/env python3
"""
Demo script: DevOps Learning Tracker

Shows both RAG and MCP pipelines working end-to-end.

Usage:
    python demo.py          # Run interactive demo
    python demo.py "query"  # Run single query
"""
import os
import sys

# Suppress HuggingFace Hub unauthenticated-request warnings and tqdm progress
# bars before any library imports so they don't pollute demo output.
os.environ.setdefault("HF_HUB_VERBOSITY", "error")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TQDM_DISABLE", "1")

from src.agent.planner import run_agent  # noqa: E402


def demo_rag():
    """Demonstrate RAG pipeline with a query about Nginx."""
    print("\n" + "=" * 70)
    print("DEMO 1: RAG Pipeline — Knowledge Retrieval")
    print("=" * 70)
    print("\nQuery: 'How do I configure Nginx as a reverse proxy?'")
    print("\n--- Output (RAG Pipeline) ---\n")

    query = "How do I configure Nginx as a reverse proxy?"
    result = run_agent(query)
    print(result)


def demo_mcp():
    """Demonstrate MCP pipeline with a query about Dockerfile generation."""
    print("\n" + "=" * 70)
    print("DEMO 2: MCP Pipeline — Tool Execution")
    print("=" * 70)
    print("\nQuery: 'Create a Dockerfile for a Python 3.13 app on port 9000'")
    print("\n--- Output (MCP Pipeline) ---\n")

    query = "Create a Dockerfile for a Python 3.13 app on port 9000"
    result = run_agent(query)
    print(result)


def demo_mcp_github_actions():
    """Demonstrate MCP pipeline for GitHub Actions workflow generation."""
    print("\n" + "=" * 70)
    print("DEMO 3: MCP Pipeline — GitHub Actions Workflow")
    print("=" * 70)
    print("\nQuery: 'Setup GitHub Actions CI/CD for pull requests with Python 3.12'")
    print("\n--- Output (MCP Pipeline) ---\n")

    query = "Setup GitHub Actions CI/CD for pull requests with Python 3.12"
    result = run_agent(query)
    print(result)


def demo_interactive():
    """Run interactive demo mode."""
    print("\n" + "=" * 70)
    print("DevOps Learning Tracker — Interactive Demo")
    print("=" * 70)
    print("\nThe system automatically routes your query to either:")
    print("  • RAG Pipeline (information/knowledge questions)")
    print("  • MCP Pipeline (generation/tool action queries)")
    print("\nExamples:")
    print("  RAG: 'How do I containerize a Python app?'")
    print("  RAG: 'Explain SSH key authentication'")
    print("  MCP: 'Create a GitHub Actions workflow'")
    print("  MCP: 'Generate a Dockerfile for Node.js'")
    print("\nType 'exit' to quit.\n")

    while True:
        try:
            query = input("Enter query: ").strip()
            if query.lower() in ("exit", "quit"):
                print("\nGoodbye!")
                break
            if not query:
                continue

            result = run_agent(query)
            print("\n" + result + "\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


def main():
    """Run demo script."""
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        print(f"\nQuery: {query}\n")
        result = run_agent(query)
        print(result)
    else:
        # Automated demo mode
        print("\n" + "=" * 70)
        print("DevOps Learning Tracker — Automated Demo")
        print("=" * 70)

        demo_rag()
        demo_mcp()
        demo_mcp_github_actions()

        print("\n" + "=" * 70)
        print("Demo Complete!")
        print("=" * 70)
        print("\nThe system demonstrates:")
        print("  ✓ RAG Pipeline: Retrieves knowledge from 5 DevOps guides")
        print("  ✓ MCP Pipeline: Generates Dockerfiles and GitHub Actions workflows")
        print("  ✓ Automatic Routing: Classifies queries and routes to appropriate pipeline")
        print("  ✓ Grounded Responses: RAG cites exact guide sections (no hallucination)")
        print("  ✓ Parameterized Generation: MCP extracts parameters from natural language")


if __name__ == "__main__":
    main()
