#!/bin/bash
# PreToolUse / Bash matcher
# Blocks bare python/pip/pytest/ruff/pylint/mypy invocations that bypass the project venv.
# Exit code 2 = block. Message tells the agent exactly what to run instead.

input=$(cat)
command=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ti = d.get('tool_input', {})
if isinstance(ti, str):
    try: ti = json.loads(ti)
    except: ti = {}
print(ti.get('command', ''))
" 2>/dev/null)

# Allow if already targeting the venv
if echo "$command" | grep -qE '(venv/bin|\.venv/bin)'; then
  exit 0
fi

# Block and suggest the venv equivalent
# Order: longer names first (python3 before python, pip3 before pip)
block_if_bare() {
  local tool="$1"
  local venv_bin="${2:-venv/bin/${tool}}"
  if echo "$command" | grep -qE "^${tool}(\s|$)"; then
    local rest="${command#${tool}}"
    printf 'BLOCKED: Do not use global %s.\nRun instead: %s%s\n' \
      "$tool" "$venv_bin" "$rest" >&2
    exit 2
  fi
}

block_if_bare "python3" "venv/bin/python"
block_if_bare "python"  "venv/bin/python"
block_if_bare "pip3"    "venv/bin/pip"
block_if_bare "pip"     "venv/bin/pip"
block_if_bare "pytest"
block_if_bare "ruff"
block_if_bare "pylint"
block_if_bare "mypy"

exit 0
