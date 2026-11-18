#!/usr/bin/env bash
# wave6_fleet.sh — 终波:luna t20 club 子表 cursor(t22)。09:00 截止。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
DEADLINE=$(date -d "2026-11-19 09:00" +%s)
log(){ echo "[wave6 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }
left(){ echo $(( DEADLINE - $(date +%s) )); }
done_ok(){ grep -rqE '"status"[[:space:]]*:[[:space:]]*"complete' "$1" 2>/dev/null; }

(
  while [ "$(left)" -gt 900 ]; do sleep 300; done
  log "wave6 watchdog: deadline reached, killing stray pi processes"
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object {\$_.CommandLine -match 'pi-coding-agent'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }" >> "$FLEET_LOG" 2>&1
) &
WATCHDOG=$!

if [ "$(left)" -lt 6000 ]; then
  log "wave6 skipped: only $(left)s left"
  kill "$WATCHDOG" 2>/dev/null
  exit 0
fi

log "L6 start t20 (luna) — t22 子表 cursor"
bash scripts/launch.sh t20-subtable-cursor openai-codex gpt-6-luna prompts/t20_subtable_cursor.md scratch/t20/out 2 2400 >> "$FLEET_LOG" 2>&1
if done_ok scratch/t20/out || [ -f scratch/t20/out/fields_t22.json ]; then
  git add scratch/t20 prompts/t20_subtable_cursor.md 2>/dev/null
  git add scripts/t20_*.py 2>/dev/null
  git commit -m "feat(t20): t22 子表 cursor 重建(夜跑,待晨裁)" >/dev/null 2>&1 || log "L6 t20 commit skipped"
  log "L6 t20 delivered"
else
  log "L6 t20 FAILED/incomplete"
fi
kill "$WATCHDOG" 2>/dev/null
log "wave6 finished at $(date '+%H:%M:%S')"
exit 0
