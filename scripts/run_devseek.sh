#!/usr/bin/env bash
# run_devseek.sh — fire a pi task on devseek with retry on upstream_saturated / 503.
# usage: bash scripts/run_devseek.sh <task-name> <prompt-file> <outbox-dir> [max-retries]
set -u
cd /d/tmp2b/fm24-db || exit 1

TASK="${1:?task name}"
PROMPT="${2:?prompt file}"
OUTBOX="${3:?outbox dir}"
MAX="${4:-5}"

LOG="scratch/t02/pi-logs/${TASK}.log"
: > "$LOG"

for i in $(seq 1 "$MAX"); do
  echo "=== attempt $i/$MAX $(date) ===" >> "$LOG"
  if timeout 3600 pi --provider devseek --model deepseek-v4.1-flash-free \
      --thinking max --approve -p -n "$TASK" \
      --session-dir scratch/t02/pi-sessions --session-id "${TASK}-devseek" \
      -- "@${PROMPT}" "严格执行这份任务书。所有产物写到 ${OUTBOX}/。完成后打印清单：每个实体拿到几个字段、卡在哪。不要修改该目录之外的任何文件。" \
      >> "$LOG" 2>&1; then
    echo "=== SUCCESS attempt $i $(date) ===" >> "$LOG"
    exit 0
  fi
  RC=$?
  echo "=== attempt $i failed rc=$RC $(date) ===" >> "$LOG"
  if grep -qiE "upstream_saturated|temporarily unavailable|503|Please wait and consider throttling" "$LOG"; then
    WAIT=$(( 60 * i ))
    echo "--- upstream throttled, sleeping ${WAIT}s ---" >> "$LOG"
    sleep "$WAIT"
  else
    echo "--- non-throttle failure, aborting ---" >> "$LOG"
    exit "$RC"
  fi
done
echo "=== gave up after $MAX attempts $(date) ===" >> "$LOG"
exit 1
