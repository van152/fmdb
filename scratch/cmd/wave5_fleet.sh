#!/usr/bin/env bash
# wave5_fleet.sh — 收官波:luna t19 club/nation cursor 重建。09:00 截止,时间余量不足就不发。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
DEADLINE=$(date -d "2026-11-19 09:00" +%s)
log(){ echo "[wave5 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }
left(){ echo $(( DEADLINE - $(date +%s) )); }
done_ok(){ grep -rqE '"status"[[:space:]]*:[[:space:]]*"complete' "$1" 2>/dev/null; }

(
  while [ "$(left)" -gt 900 ]; do sleep 300; done
  log "wave5 watchdog: deadline reached, killing stray pi processes"
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object {\$_.CommandLine -match 'pi-coding-agent'} | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }" >> "$FLEET_LOG" 2>&1
) &
WATCHDOG=$!

if [ "$(left)" -lt 8400 ]; then
  log "wave5 skipped: only $(left)s left, not enough for t19"
  kill "$WATCHDOG" 2>/dev/null
  exit 0
fi

log "L5 start t19 (luna) — club/nation cursor"
bash scripts/launch.sh t19-club-cursor openai-codex gpt-6-luna prompts/t19_club_cursor.md scratch/t19/out 2 3300 >> "$FLEET_LOG" 2>&1
if done_ok scratch/t19/out || [ -f scratch/t19/out/cursor_club.json ]; then
  git add scratch/t19 prompts/t19_club_cursor.md 2>/dev/null
  git add scripts/t19_*.py 2>/dev/null
  git commit -m "feat(t19): club/nation cursor_layout 重建(夜跑,待晨裁)" >/dev/null 2>&1 || log "L5 t19 commit skipped"
  log "L5 t19 delivered"
else
  log "L5 t19 FAILED/incomplete"
fi
kill "$WATCHDOG" 2>/dev/null
log "wave5 finished at $(date '+%H:%M:%S')"
exit 0
