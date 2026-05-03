#!/bin/bash
# preToolUse / Shell matcher
# Silently rewrites bare python/pip/pytest/ruff/pylint/mypy to use project venv.
# Uses updated_input — the command is corrected before it runs. No blocking, no retry needed.

input=$(cat)

python3 << 'PYEOF'
import sys, json, re

data = json.load(sys.stdin)
ti = data.get('tool_input', {})
if isinstance(ti, str):
    try:
        ti = json.loads(ti)
    except Exception:
        ti = {}

command = ti.get('command', '')

# Already using venv or an absolute path — allow as-is
if re.search(r'venv/bin|\.venv/bin|/usr/local/bin', command):
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

# Order matters: longer names first to avoid partial matches (python3 before python, pip3 before pip)
REWRITES = [
    ('python3', 'venv/bin/python'),
    ('python',  'venv/bin/python'),
    ('pip3',    'venv/bin/pip'),
    ('pip',     'venv/bin/pip'),
    ('pytest',  'venv/bin/pytest'),
    ('ruff',    'venv/bin/ruff'),
    ('pylint',  'venv/bin/pylint'),
    ('mypy',    'venv/bin/mypy'),
]

for bare, venv_bin in REWRITES:
    if re.match(rf'^{re.escape(bare)}(\s|$)', command):
        new_command = re.sub(rf'^{re.escape(bare)}', venv_bin, command, count=1)
        new_ti = dict(ti)
        new_ti['command'] = new_command
        print(json.dumps({"permission": "allow", "updated_input": new_ti}))
        sys.exit(0)

print(json.dumps({"permission": "allow"}))
PYEOF
