#!/usr/bin/env bash
# wave2_fleet.sh — 第二波:t16(前置已修)→ t17;luna 车道;devseek 车道 t15c 收尾。
# 09:00 截止(2026-11-19),复用 overnight_fleet 的纪律。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
DEADLINE=$(date -d "2026-11-19 09:00" +%s)
log(){ echo "[wave2 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }
left(){ echo $(( DEADLINE - $(date +%s) )); }
done_ok(){ grep -rqE '"status"[[:space:]]*:[[:space:]]*"complete' "$1" 2>/dev/null; }

(
  while [ "$(left)" -gt 900 ]; do sleep 300; done
  log "wave2 watchdog: deadline reached, killing stray pi processes"
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object {\$_.CommandLine -match 'pi-coding-agent'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }" >> "$FLEET_LOG" 2>&1
) &
WATCHDOG=$!

lane_luna(){
  log "L2 start t16 (luna)"
  bash scripts/launch.sh t16-serializer openai-codex gpt-6-luna prompts/t16_serializer_walk.md scratch/t16/out 3 2700 >> "$FLEET_LOG" 2>&1
  if ! done_ok scratch/t16/out && [ ! -f scratch/t16/out/ledger.json ]; then
    log "L2 t16 FAILED/incomplete - lane stops"; return 1
  fi
  log "L2 t16 delivered -> commit"
  git add scratch/t16 prompts/t16_serializer_walk.md 2>/dev/null
  git add scripts/t16_*.py 2>/dev/null
  git commit -m "feat(t16): serializer walk 引擎(夜跑,待晨裁)" >/dev/null 2>&1 || log "L2 t16 commit skipped"

  if [ "$(left)" -lt 5400 ]; then log "L2 skip t17 (deadline margin)"; return 0; fi
  log "L2 start t17 (luna)"
  bash scripts/launch.sh t17-ledger openai-codex gpt-6-luna prompts/t17_ledger.md scratch/t17/out 3 2400 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t17/out || [ -f scratch/t17/out/regression.json ]; then
    git add scratch/t17 prompts/t17_ledger.md 2>/dev/null
    git commit -m "feat(t17): tier1 台账 + 全量回归(夜跑,待晨裁)" >/dev/null 2>&1 || log "L2 t17 commit skipped"
    log "L2 t17 delivered"
  else
    log "L2 t17 FAILED/incomplete"
  fi
  log "L2 end"
}

lane_devseek(){
  log "D2 start t15c (devseek)"
  bash scripts/launch.sh t15c-finalize devseek deepseek-v4.1-flash-free prompts/t15c_fk_finalize.md scratch/t15/out 4 1200 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t15/out || [ -f scratch/t15/out/fk.md ]; then
    log "D2 t15c delivered -> commit"
    git add scratch/t15/out/fk.json scratch/t15/out/fk.md scratch/t15/out/people_diff.md prompts/t15c_fk_finalize.md 2>/dev/null
    git commit -m "feat(t15c): FK 交叉收尾汇总(夜跑,待晨裁)" >/dev/null 2>&1 || log "D2 t15c commit skipped"
  else
    log "D2 t15c FAILED/incomplete"
  fi
  log "D2 end"
}

log "wave2 start; deadline $(date -d @$DEADLINE '+%H:%M'); now $(date '+%H:%M')"
lane_luna & LPID=$!
lane_devseek & DPID=$!
wait $LPID; LRC=$?
wait $DPID; DRC=$?
kill "$WATCHDOG" 2>/dev/null
log "wave2 lanes finished: luna=$LRC devseek=$DRC at $(date '+%H:%M:%S')"
exit 0
