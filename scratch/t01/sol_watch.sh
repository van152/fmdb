#!/usr/bin/env bash
# sol_watch: probe gpt-6.2-sol every 15 min; fire the t01f killer run on first success.
cd /d/tmp2b/fm24-db || exit 1
LOG=scratch/t01/pi-logs/sol_watch.log
echo "watch start $(date)" >> "$LOG"
for i in $(seq 1 40); do
  if timeout 180 pi --provider openai-codex --model gpt-6.2-sol --no-tools --no-session -p "reply with exactly: OK" >> "$LOG" 2>&1; then
    echo "MODEL LIVE at attempt $i $(date) — firing t01f killer run" >> "$LOG"
    pi --provider openai-codex --model gpt-6.2-sol --thinking max --approve -p -n t01f --session-dir scratch/t01/pi-sessions --session-id t01f-sol -- @prompts/t01f_breakthrough.md "严格执行这份突破任务书。所有产物写到 scratch/t01/inbox/t01f/。完成后打印交付文件清单。" > scratch/t01/pi-logs/t01f.log 2>&1
    echo "t01f run exited $(date)" >> "$LOG"
    exit 0
  fi
  echo "attempt $i not available $(date)" >> "$LOG"
  sleep 900
done
echo "gave up after 40 attempts $(date)" >> "$LOG"
