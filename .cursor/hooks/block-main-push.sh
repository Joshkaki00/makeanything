#!/bin/bash
# Blocks direct git push to main or master.
# Non-negotiable: use a branch and open a PR.

input=$(cat)
command=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('command',''))" 2>/dev/null)

deny() {
  echo "{\"permission\":\"deny\",\"user_message\":\"$1\",\"agent_message\":\"$2\"}"
  exit 0
}

# Block explicit pushes naming main or master
if echo "$command" | grep -qE 'git push.+\b(main|master)\b'; then
  deny \
    "Direct push to main/master is blocked. Open a PR from a feature branch." \
    "Pushing directly to main or master is not allowed by project policy. Create a feature branch, push that branch, and open a pull request."
fi

# Block bare 'git push' or 'git push origin' when already on main/master
if echo "$command" | grep -qE '^git push(\s+origin)?$'; then
  branch=$(git -C "${CURSOR_PROJECT_DIR:-.}" branch --show-current 2>/dev/null)
  if [[ "$branch" == "main" || "$branch" == "master" ]]; then
    deny \
      "You are on $branch. Direct push blocked. Switch to a feature branch first." \
      "Currently on $branch branch. Direct pushes are blocked. Switch to a feature branch and push that instead."
  fi
fi

echo '{"permission":"allow"}'
exit 0
