#!/usr/bin/env bash
# overnight_fleet.sh — 夜间舰队:双车道流水线,09:00 截止(2026-11-19)
# 车道 L(luna): t14 RTTI普查 → t16 序列化器引擎 → t17 台账回归
# 车道 D(devseek): t15 FK交叉 → t15b 档案清点
# 每波完成即 commit(消息带"待晨裁");截止前 15 分钟看门狗清残进程。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
DEADLINE=$(date -d "2026-11-19 09:00" +%s)
log(){ echo "[fleet $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }
left(){ echo $(( DEADLINE - $(date +%s) )); }
done_ok(){ grep -rqE '"status"[[:space:]]*:[[:space:]]*"complete' "$1" 2>/dev/null; }

# 看门狗:截止+15min 强制清 pi 残留(防止 timeout 杀不掉 node 导致整夜挂死)
(
  while [ "$(left)" -gt 900 ]; do sleep 300; done
  log "watchdog: deadline reached, killing stray pi processes"
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object {\$_.CommandLine -match 'pi-coding-agent'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }" >> "$FLEET_LOG" 2>&1
) &
WATCHDOG=$!

lane_luna(){
  log "L1 start t14 (luna)"
  bash scripts/launch.sh t14-rtti openai-codex gpt-6-luna prompts/t14_rtti_census.md scratch/t14/out 3 2700 >> "$FLEET_LOG" 2>&1
  if ! done_ok scratch/t14/out && [ ! -f scratch/t14/out/stage2_map.json ]; then
    log "L1 t14 FAILED/incomplete - lane stops"; return 1
  fi
  log "L1 t14 delivered -> commit"
  git add scratch/t14 prompts/t14_rtti_census.md scratch/t14/out/*.py 2>/dev/null
  git add scripts/t14_*.py 2>/dev/null
  git commit -m "feat(t14): RTTI census + stage2 全图(夜跑,待晨裁)" >/dev/null 2>&1 || log "L1 t14 commit skipped"

  if [ "$(left)" -lt 7200 ]; then log "L1 skip t16 (deadline margin)"; return 0; fi
  log "L1 start t16 (luna)"
  bash scripts/launch.sh t16-serializer openai-codex gpt-6-luna prompts/t16_serializer_walk.md scratch/t16/out 3 2700 >> "$FLEET_LOG" 2>&1
  if ! done_ok scratch/t16/out && [ ! -f scratch/t16/out/ledger.json ]; then
    log "L1 t16 FAILED/incomplete - lane stops"; return 1
  fi
  log "L1 t16 delivered -> commit"
  git add scratch/t16 prompts/t16_serializer_walk.md 2>/dev/null
  git add scripts/t16_*.py 2>/dev/null
  git commit -m "feat(t16): serializer walk 引擎(夜跑,待晨裁)" >/dev/null 2>&1 || log "L1 t16 commit skipped"

  if [ "$(left)" -lt 5400 ]; then log "L1 skip t17 (deadline margin)"; return 0; fi
  log "L1 start t17 (luna)"
  bash scripts/launch.sh t17-ledger openai-codex gpt-6-luna prompts/t17_ledger.md scratch/t17/out 3 2400 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t17/out || [ -f scratch/t17/out/regression.json ]; then
    git add scratch/t17 prompts/t17_ledger.md 2>/dev/null
    git commit -m "feat(t17): tier1 台账 + 全量回归(夜跑,待晨裁)" >/dev/null 2>&1 || log "L1 t17 commit skipped"
    log "L1 t17 delivered"
  else
    log "L1 t17 FAILED/incomplete"
  fi
  log "L1 end"
}

lane_devseek(){
  log "D1 start t15 (devseek)"
  bash scripts/launch.sh t15-fk devseek deepseek-v4.1-flash-free prompts/t15_fk_cross.md scratch/t15/out 3 1800 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t15/out || [ -f scratch/t15/out/fk.md ]; then
    log "D1 t15 delivered -> commit"
    git add scratch/t15/out/*.json scratch/t15/out/*.md scratch/t15/out/*.py prompts/t15_fk_cross.md 2>/dev/null
    git commit -m "feat(t15): FK 交叉佐证(夜跑,待晨裁)" >/dev/null 2>&1 || log "D1 t15 commit skipped"
  else
    log "D1 t15 FAILED/incomplete"
  fi
  if [ "$(left)" -lt 5400 ]; then log "D1 skip t15b (deadline margin)"; return 0; fi
  log "D1 start t15b (devseek)"
  bash scripts/launch.sh t15b-probe devseek deepseek-v4.1-flash-free prompts/t15b_archive_probe.md scratch/t15b/out 3 1800 >> "$FLEET_LOG" 2>&1
  if done_ok scratch/t15b/out || [ -f scratch/t15b/out/probe.md ]; then
    git add scratch/t15b/out/*.json scratch/t15b/out/*.md prompts/t15b_archive_probe.md 2>/dev/null
    git commit -m "feat(t15b): 未覆盖档案清点(夜跑,待晨裁)" >/dev/null 2>&1 || log "D1 t15b commit skipped"
    log "D1 t15b delivered"
  else
    log "D1 t15b FAILED/incomplete"
  fi
  log "D1 end"
}

log "fleet start; deadline $(date -d @$DEADLINE '+%H:%M'); now $(date '+%H:%M')"
lane_luna & LPID=$!
lane_devseek & DPID=$!
wait $LPID; LRC=$?
wait $DPID; DRC=$?
kill "$WATCHDOG" 2>/dev/null
log "fleet lanes finished: luna=$LRC devseek=$DRC at $(date '+%H:%M:%S')"
exit 0
