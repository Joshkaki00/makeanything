#!/bin/bash
# Appends every agent shell command and file edit to logs/agent-audit.log.
# Fire-and-forget: always exits 0 so failures never block the agent.

LOG_DIR="${CURSOR_PROJECT_DIR:-.}/logs"
LOG_FILE="$LOG_DIR/agent-audit.log"

mkdir -p "$LOG_DIR"

input=$(cat)
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
event=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('hook_event_name','unknown'))" 2>/dev/null)

printf '[%s] [%s] %s\n' "$timestamp" "$event" "$input" >> "$LOG_FILE"

exit 0
