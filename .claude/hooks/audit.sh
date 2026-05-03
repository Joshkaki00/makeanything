#!/bin/bash
# PostToolUse (Bash) + Stop hook
# Appends all agent shell commands and session-stop events to logs/agent-audit.log.
# Always exits 0 — failures must never block the agent.

LOG_DIR="${CLAUDE_PROJECT_DIR:-.}/logs"
LOG_FILE="$LOG_DIR/agent-audit.log"

mkdir -p "$LOG_DIR"

input=$(cat)
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

event=$(echo "$input" | python3 -c "
import sys, json
d = json.load(sys.stdin)
# Distinguish Stop from PostToolUse
if 'tool_name' in d:
    cmd = d.get('tool_input', {}).get('command', '(no command)')
    print(f\"[bash] {cmd}\")
else:
    status = d.get('stop_reason', d.get('status', 'stopped'))
    print(f\"[stop] {status}\")
" 2>/dev/null || echo "[unknown]")

printf '[%s] %s\n' "$timestamp" "$event" >> "$LOG_FILE"

exit 0
