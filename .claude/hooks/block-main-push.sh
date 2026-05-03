#!/bin/bash
# PreToolUse / Bash matcher
# Blocks git push targeting main or master.
# Exit code 2 = block the action.

input=$(cat)

# Claude Code PreToolUse: command is at tool_input.command
command=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('command', ''))
" 2>/dev/null)

block() {
  echo "$1" >&2
  exit 2
}

# Block explicit target: git push origin main / git push origin master
if echo "$command" | grep -qE 'git push.+\b(main|master)\b'; then
  block "BLOCKED: Direct push to main/master is not allowed. Push to a feature branch and open a PR."
fi

# Block bare push when already on main/master
if echo "$command" | grep -qE '^git push(\s+origin)?\s*$'; then
  branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" branch --show-current 2>/dev/null)
  if [[ "$branch" == "main" || "$branch" == "master" ]]; then
    block "BLOCKED: You are on $branch. Switch to a feature branch before pushing."
  fi
fi

exit 0
