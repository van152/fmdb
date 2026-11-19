#!/usr/bin/env bash
# sol_burn.sh — 连续打空 gpt-6.2-sol 5h 窗口(用户指令:三窗口耗尽)
# 队列文件:scratch/cmd/sol_queue.txt,每行 task|prompt|timeout(第三段可省,默认 2400)
# 停止条件:touch scratch/cmd/sol_burn.stop 或额度耗尽事件达到 3 次
set -u
cd /d/tmp2b/fm24-db || exit 1
Q=scratch/cmd/sol_queue.txt
STOP=scratch/cmd/sol_burn.stop
LOG=scratch/cmd/fleet.log
WIN_COUNT=0
log(){ echo "[solburn $(date +%m-%d\ %H:%M:%S)] $*" >> "$LOG"; }
log "sol burn runner START (user directive: drain 3 x 5h sol windows)"
while true; do
  [ -e "$STOP" ] && { log "stop file seen; runner exit"; break; }
  line=$(head -n1 "$Q" 2>/dev/null)
  if [ -z "${line:-}" ]; then sleep 300; continue; fi
  task="${line%%|*}"; rest="${line#*|}"
  prompt="${rest%%|*}"
  tmo="${rest#*|}"; [ "$tmo" = "$rest" ] && tmo=2400
  tbl="${task%%-*}"
  out="scratch/$tbl/out"
  if [ -s "$out/DONE.md" ]; then
    sed -i '1d' "$Q"
    log "$task DONE.md present; dequeued (awaiting commander acceptance)"
    sleep 45
    continue
  fi
  log "$task LAUNCH provider=openai-codex model=gpt-6.2-sol prompt=$prompt timeout=$tmo"
  bash scripts/launch.sh "$task" openai-codex gpt-6.2-sol "$prompt" "$out" 6 "$tmo" \
    >> "scratch/t02/pi-logs/$task.log" 2>&1
  rc=$?
  log "$task launcher rc=$rc"
  if [ -s "$out/DONE.md" ]; then
    sed -i '1d' "$Q"
    log "$task delivered; commander acceptance pending"
    sleep 45
    continue
  fi
  if grep -qiE "usage limit|Weekly limit|rate.?limit" "scratch/t02/pi-logs/$task.log" 2>/dev/null; then
    WIN_COUNT=$((WIN_COUNT+1))
    log "QUOTA DRAIN #$WIN_COUNT detected (blocked at $task); waiting for window reset, then resume same session"
    if [ "$WIN_COUNT" -ge 3 ]; then
      log "THREE WINDOWS DRAINED — user directive satisfied; dispatcher stops (task $task stays queued for next window)"
      break
    fi
    sleep 900
    continue
  fi
  nfile="scratch/cmd/.requeue_$task"
  n=$(( $(cat "$nfile" 2>/dev/null || echo 0) + 1 ))
  echo "$n" > "$nfile"
  if [ "$n" -ge 4 ]; then
    log "$task failed $n attempts; dropping from queue (requeue manually if needed)"
    sed -i '1d' "$Q"
    rm -f "$nfile"
  else
    log "$task attempt failed; retry #$n in 120s"
    sleep 120
  fi
done
log "sol burn runner EXIT (windows drained: $WIN_COUNT; queue left: $(wc -l < "$Q" 2>/dev/null || echo 0) tasks)"
