#!/usr/bin/env bash
# compact_all.sh — compact remaining sessions, 3 per minute, skip already-compacted.
cd /d/tmp2b/fm24-db || exit 1
LOG=scratch/pi-logs/compact_all.log
mkdir -p scratch/pi-logs
: > "$LOG"

# session_id:session_dir:provider:model  (empty provider = omit)
LIST=(
  "t01g-luna:scratch/t01/pi-sessions:openai-codex:gpt-6-luna"
  "t01h-luna:scratch/t01/pi-sessions:openai-codex:gpt-6-luna"
  "t01i-luna:scratch/t01/pi-sessions:openai-codex:gpt-6-luna"
  "t01j-luna:scratch/t01/pi-sessions:openai-codex:gpt-6-luna"
  "t01k-luna:scratch/t01/pi-sessions:openai-codex:gpt-6-luna"
  "t01l-luna:scratch/t01/pi-sessions:openai-codex:gpt-6-luna"
  "t01m-luna:scratch/t01/pi-sessions:openai-codex:gpt-6-luna"
  "t02a-devseek:scratch/t02/pi-sessions:devseek:deepseek-v4.1-flash-free"
  "fw41-devseek:scratch/t02/pi-sessions:devseek:deepseek-v4.1-flash-free"
  "fw8-devseek:scratch/t02/pi-sessions:devseek:deepseek-v4.1-flash-free"
  "fw23-devseek:scratch/t02/pi-sessions:devseek:deepseek-v4.1-flash-free"
  "fw18-devseek:scratch/t02/pi-sessions:devseek:deepseek-v4.1-flash-free"
  "t01d-logfare:scratch/t01/pi-sessions:logfare:deepseek-v4.1-flash-1017"
)

has_compaction() {
  grep -q '"type": *"compaction"\|"type":"compaction"' "$1" 2>/dev/null
}

i=0
for entry in "${LIST[@]}"; do
  IFS=':' read -r sid sdir prov model <<< "$entry"
  f=$(ls "$sdir"/*_"$sid".jsonl 2>/dev/null | tail -1)
  if [ -z "$f" ]; then echo "SKIP $sid (no file)" >> "$LOG"; continue; fi
  if has_compaction "$f"; then echo "SKIP $sid (already compacted)" >> "$LOG"; continue; fi
  before=$(stat -c%s "$f" 2>/dev/null || wc -c < "$f")
  i=$((i+1))
  echo "=== [$i] $sid ($before B) $(date) ===" >> "$LOG"
  py -V:3.12 -I scripts/compact_sessions.py --only "$sid" >> "$LOG" 2>&1
  after=$(stat -c%s "$f" 2>/dev/null || wc -c < "$f")
  if has_compaction "$f"; then
    echo "  OK $sid $before -> $after" >> "$LOG"
  else
    echo "  FAIL $sid $before -> $after" >> "$LOG"
  fi
  sleep 20
done
echo "=== ALL DONE $(date) ===" >> "$LOG"
