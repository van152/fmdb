#!/usr/bin/env bash
# sol_burn2.sh — 修正版:额度耗尽按"耗尽期"计数(同一期内的重试不算新窗口)
# 停止条件:touch scratch/cmd/sol_burn.stop 或耗尽期达到 3 次
set -u
cd /d/tmp2b/fm24-db || exit 1
Q=scratch/cmd/sol_queue.txt
STOP=scratch/cmd/sol_burn.stop
LOG=scratch/cmd/fleet.log
WIN_COUNT=0
BLOCKED=0
SUCCESS_SEEN=0
log(){ echo "[solburn2 $(date +%m-%d\ %H:%M:%S)] $*" >> "$LOG"; }
log "sol burn runner v2 START (episode-based; SUCCESS_SEEN baseline=0: v1 already counted the 06:05 drain as window 1)"
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
  if grep -qiE "usage limit|Weekly limit" "scratch/t02/pi-logs/$task.log" 2>/dev/null; then
    if [ "$SUCCESS_SEEN" -eq 0 ]; then
      log "still blocked from previous (already-counted) drain; not counted; retry in 15 min"
    elif [ "$BLOCKED" -eq 0 ]; then
      BLOCKED=1
      WIN_COUNT=$((WIN_COUNT+1))
      log "QUOTA DRAIN EPISODE #$WIN_COUNT starts (blocked at $task)"
      if [ "$WIN_COUNT" -ge 2 ]; then
        log "ENOUGH DRAIN EPISODES REACHED (2 more after window 1 = 3 total) — user directive satisfied; dispatcher stops; task $task stays queued"
        break
      fi
    fi
    sleep 900
    continue
  fi
  SUCCESS_SEEN=1
  if [ "$BLOCKED" -eq 1 ]; then
    BLOCKED=0
    log "quota recovered after drain episode #$WIN_COUNT (window reset confirmed by successful relaunch)"
  fi
  if [ -s "$out/DONE.md" ]; then
    sed -i '1d' "$Q"
    log "$task delivered; commander acceptance pending"
    sleep 45
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
    log "$task attempt failed (non-quota); retry #$n in 120s"
    sleep 120
  fi
done
log "sol burn runner v2 EXIT (drain episodes: $WIN_COUNT; queue left: $(wc -l < "$Q" 2>/dev/null || echo 0))"
