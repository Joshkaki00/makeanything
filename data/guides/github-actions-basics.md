# GitHub Actions Basics

## What is GitHub Actions

GitHub Actions is a continuous integration and continuous delivery (CI/CD) platform that allows you to automate your build, test, and deployment pipeline. You can write individual tasks, called actions, and combine them to create a custom workflow. Workflows are custom automated processes that you can set up in your repository to build, test, package, release, or deploy any code project on GitHub.

GitHub Actions uses YAML syntax to define the workflow. Each workflow is stored as a separate YAML file in your repository code, in a directory named `.github/workflows/`.

## Creating a Workflow

To create a workflow, you need to:

1. Create a `.github/workflows/` directory in your repository if it doesn't already exist
2. In the `.github/workflows/` directory, create a new file with a `.yml` or `.yaml` extension
3. Copy one of the starter workflow templates into your new file and modify it as needed
4. Commit your changes and push them to your GitHub repository

Workflows are triggered by events. For example, an event can be when someone pushes to a repository, when a pull request is created, or when a release is published. You can also trigger a workflow on a schedule.

## Workflow Triggers

Common GitHub Actions triggers include:

- `push` — The workflow runs every time someone pushes to the repository or merges a pull request
- `pull_request` — The workflow runs when someone opens a pull request or pushes a commit to an open pull request
- `schedule` — Run your workflow on a schedule using CRON syntax (e.g., `0 0 * * *` runs daily at midnight UTC)
- `workflow_dispatch` — This trigger lets you manually run a workflow from the GitHub UI
- `release` — Triggered when a release is created in the repository

## Basic Workflow Example

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest tests/
```

## Jobs and Steps

A workflow run is made up of one or more jobs. Jobs run in parallel by default. Each job runs inside its own runner instance and contains one or more steps. Steps are individual tasks that can run commands or use actions.

You can configure a job's dependencies with other jobs; by default, jobs have no dependencies and run in parallel with each other. When a job depends on another job, it will wait for the dependent job to complete before it can run.

## Runners

A runner is a server that runs your workflows when they're triggered. GitHub provides Ubuntu Linux, Microsoft Windows, and macOS runners for you to use. Each job in a workflow runs on a fresh instance of a virtual machine.

The most common runner is `ubuntu-latest`, which runs on Ubuntu 20.04 or later.
