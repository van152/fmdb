#!/usr/bin/env bash
# wave3_fleet.sh — 第三波:luna 车道 t17c 回归 → t16b 台账;devseek 车道 t15d 抽查。09:00 截止。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
DEADLINE=$(date -d "2026-11-19 09:00" +%s)
log(){ echo "[wave3 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }
left(){ echo $(( DEADLINE - $(date +%s) )); }
done_ok(){ grep -rqE '"status"[[:space:]]*:[[:space:]]*"complete' "$1" 2>/dev/null; }

(
  while [ "$(left)" -gt 900 ]; do sleep 300; done
  log "wave3 watchdog: deadline reached, killing stray pi processes"
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object {\$_.CommandLine -match 'pi-coding-agent'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }" >> "$FLEET_LOG" 2>&1
) &
WATCHDOG=$!

lane_luna(){
  log "L3 start t17c (luna) — 回归套件优先"
  bash scripts/launch.sh t17c-regression openai-codex gpt-6-luna prompts/t17c_regression.md scratch/t17/out 2 2400 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t17/out || [ -f scratch/t17/out/regression.json ]; then
    git add scratch/t17 prompts/t17c_regression.md 2>/dev/null
    git commit -m "feat(t17c): 全量回归套件(夜跑,待晨裁)" >/dev/null 2>&1 || log "L3 t17c commit skipped"
    log "L3 t17c delivered"
  else
    log "L3 t17c FAILED (regression missing) — 继续试 t16b"
  fi
  if [ "$(left)" -lt 7200 ]; then log "L3 skip t16b (deadline margin)"; return 0; fi
  log "L3 start t16b (luna)"
  bash scripts/launch.sh t16b-ledger openai-codex gpt-6-luna prompts/t16b_ledger.md scratch/t16b/out 3 2700 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t16b/out || [ -f scratch/t16b/out/ledger.json ]; then
    git add scratch/t16b prompts/t16b_ledger.md 2>/dev/null
    git add scripts/t16b_*.py 2>/dev/null
    git commit -m "feat(t16b): 全实体台账 + 重校准命名桥(夜跑,待晨裁)" >/dev/null 2>&1 || log "L3 t16b commit skipped"
    log "L3 t16b delivered"
  else
    log "L3 t16b FAILED/incomplete"
  fi
  log "L3 end"
}

lane_devseek(){
  log "D3 start t15d (devseek)"
  bash scripts/launch.sh t15d-dspot devseek deepseek-v4.1-flash-free prompts/t15d_dspot.md scratch/t15d/out 3 1500 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t15d/out || [ -f scratch/t15d/out/dspot.md ]; then
    git add scratch/t15d/out/*.json scratch/t15d/out/*.md prompts/t15d_dspot.md 2>/dev/null
    git commit -m "feat(t15d): D-锚-only 表数据侧抽查(夜跑,待晨裁)" >/dev/null 2>&1 || log "D3 t15d commit skipped"
    log "D3 t15d delivered"
  else
    log "D3 t15d FAILED/incomplete"
  fi
  log "D3 end"
}

log "wave3 start; deadline $(date -d @$DEADLINE '+%H:%M'); now $(date '+%H:%M')"
lane_luna & LPID=$!
lane_devseek & DPID=$!
wait $LPID; LRC=$?
wait $DPID; DRC=$?
kill "$WATCHDOG" 2>/dev/null
log "wave3 lanes finished: luna=$LRC devseek=$DRC at $(date '+%H:%M:%S')"
exit 0
