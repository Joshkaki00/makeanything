#!/bin/bash
# postToolUse / Write matcher
# Warns the agent when console.log is left in a JS/TS file after a write.

input=$(cat)

# Extract file path from tool_input (Cursor Write tool passes 'path')
file_path=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ti = d.get('tool_input', {})
if isinstance(ti, str):
    try:
        ti = json.loads(ti)
    except Exception:
        ti = {}
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
  locations=$(grep -n "console\.log" "$file_path" | head -5 | awk '{print "  line "$0}' | tr '\n' '|' | sed 's/|$//')
  msg="console.log check: $count occurrence(s) in $(basename "$file_path") — $locations — remove before shipping."
  printf '{"additional_context":"%s"}\n' "$msg"
fi

exit 0
