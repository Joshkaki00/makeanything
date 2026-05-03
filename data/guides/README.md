# DevOps Guides

Knowledge base for the RAG pipeline. Each file is a beginner-focused guide on one DevOps tool.

## Corpus

| File | Topic | Status |
|------|-------|--------|
| `docker-basics.md` | Docker containers, images, Dockerfiles, Compose | ✅ Done |
| `github-actions.md` | CI/CD workflows, triggers, job steps | 🔲 TODO |
| `ssh-basics.md` | SSH keys, config, port forwarding, tunneling | 🔲 TODO |
| `nginx-basics.md` | Reverse proxy, SSL, server blocks | 🔲 TODO |
| `aws-ec2-basics.md` | Launching instances, security groups, deploying apps | 🔲 TODO |

## Chunking Notes

Files are chunked at `##` heading boundaries. Keep each `##` section focused on one concept.
Avoid writing sections that reference content from other sections within the same heading block —
the retriever sees only one chunk at a time.

## Adding a Guide

1. Create `<topic>-basics.md` in this directory.
2. Structure with `##` headings, one concept per heading.
3. Include code blocks with real commands (not pseudocode).
4. Test that chunking separates sections cleanly: `pytest tests/rag/test_chunker.py -v -k <topic>`.
