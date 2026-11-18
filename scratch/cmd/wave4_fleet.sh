#!/usr/bin/env bash
# wave4_fleet.sh — 第四波:luna t18 偏移桥;devseek t15e 收尾。09:00 截止。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
DEADLINE=$(date -d "2026-11-19 09:00" +%s)
log(){ echo "[wave4 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }
left(){ echo $(( DEADLINE - $(date +%s) )); }
done_ok(){ grep -rqE '"status"[[:space:]]*:[[:space:]]*"complete' "$1" 2>/dev/null; }

(
  while [ "$(left)" -gt 900 ]; do sleep 300; done
  log "wave4 watchdog: deadline reached, killing stray pi processes"
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object {\$_.CommandLine -match 'pi-coding-agent'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }" >> "$FLEET_LOG" 2>&1
) &
WATCHDOG=$!

lane_luna(){
  log "L4 start t18 (luna) — 偏移桥"
  bash scripts/launch.sh t18-offset-bridge openai-codex gpt-6-luna prompts/t18_offset_bridge.md scratch/t18/out 3 3000 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t18/out || [ -f scratch/t18/out/bridge.json ]; then
    git add scratch/t18 prompts/t18_offset_bridge.md 2>/dev/null
    git add scripts/t18_*.py 2>/dev/null
    git commit -m "feat(t18): 行↔对象偏移桥 + 行侧重生成台账(夜跑,待晨裁)" >/dev/null 2>&1 || log "L4 t18 commit skipped"
    log "L4 t18 delivered"
  else
    log "L4 t18 FAILED/incomplete"
  fi
  log "L4 end"
}

lane_devseek(){
  log "D4 start t15e (devseek)"
  bash scripts/launch.sh t15e-finalize devseek deepseek-v4.1-flash-free prompts/t15e_dspot_finalize.md scratch/t15d/out 3 900 >> "$FLEET_LOG" 2>&1
  if [ -f scratch/t15d/out/dspot.md ]; then
    git add scratch/t15d/out/dspot.json scratch/t15d/out/dspot.md prompts/t15e_dspot_finalize.md 2>/dev/null
    git commit -m "feat(t15e): D-锚抽查收尾(夜跑,待晨裁)" >/dev/null 2>&1 || log "D4 t15e commit skipped"
    log "D4 t15e delivered"
  else
    log "D4 t15e FAILED/incomplete"
  fi
  log "D4 end"
}

log "wave4 start; deadline $(date -d @$DEADLINE '+%H:%M'); now $(date '+%H:%M')"
lane_luna & LPID=$!
lane_devseek & DPID=$!
wait $LPID; LRC=$?
wait $DPID; DRC=$?
kill "$WATCHDOG" 2>/dev/null
log "wave4 lanes finished: luna=$LRC devseek=$DRC at $(date '+%H:%M:%S')"
exit 0
