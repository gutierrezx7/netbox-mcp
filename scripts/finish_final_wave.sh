#!/usr/bin/env bash
set -euo pipefail

APPROVALS_FILE=${1:-}

usage(){
  echo "Usage: $0 <approvals-file>"
  echo "Approvals file must contain lines: F1: APPROVE, F2: APPROVE, F3: APPROVE, F4: APPROVE"
  exit 2
}

if [ -z "$APPROVALS_FILE" ]; then
  usage
fi

if [ ! -f "$APPROVALS_FILE" ]; then
  echo "Approvals file not found: $APPROVALS_FILE" >&2
  exit 3
fi

check_ok(){
  grep -q "$1: APPROVE" "$APPROVALS_FILE"
}

for f in F1 F2 F3 F4; do
  if ! check_ok "$f"; then
    echo "Missing approval: $f: APPROVE" >&2
    echo "Please ensure the approvals file contains a line: $f: APPROVE" >&2
    exit 4
  fi
done

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
note="\n- [$timestamp] FINAL VERIFICATION: All reviewers APPROVED (F1,F2,F3,F4). See approvals file: $APPROVALS_FILE\n"

echo "Appending final verification note to notepad..."
printf "%s\n" "$note" >> .sisyphus/notepads/netbox-mcp-crud-implementation/learnings.md

echo "Writing finished flag: .sisyphus/final_wave_passed"
mkdir -p .sisyphus
printf "%s\n" "$timestamp" > .sisyphus/final_wave_passed

echo "Final verification recorded. You may now consider the plan's pass-final-wave completed." 
