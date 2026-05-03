#!/bin/bash
# PostToolUse / Write|Edit matcher
# Warns when console.log is present in a JS/TS file after a write or edit.
# Output goes to stdout — Claude Code includes it in the tool result context.

input=$(cat)

# Extract file path from tool_input (Write uses 'path', Edit uses 'path' too)
file_path=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ti = d.get('tool_input', {})
print(ti.get('path', '') or ti.get('file_path', ''))
" 2>/dev/null)

# Only check JS/TS source files
if [[ ! "$file_path" =~ \.(js|jsx|ts|tsx)$ ]]; then
  exit 0
fi

if [[ ! -f "$file_path" ]]; then
  exit 0
fi

count=$(grep -c "console\.log" "$file_path" 2>/dev/null || echo 0)

if [[ "$count" -gt 0 ]]; then
  echo ""
  echo "⚠ console.log check: $count occurrence(s) in $(basename "$file_path")"
  grep -n "console\.log" "$file_path" | head -5 | while IFS= read -r line; do
    echo "  $line"
  done
  echo "  Remove these before shipping to production."
  echo ""
fi

exit 0
