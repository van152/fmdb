#!/usr/bin/env bash
# wave7_fleet.sh — 三路并行:t24 club 全 cursor(sol)/ t25 nation client 放量(luna)/ t26 hist+people 普查(devseek)
# 指挥官在线监收,不自动 commit;产物到齐后独立抽验入账。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
log(){ echo "[wave7 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }

log "wave7 launch: t24(sol/gpt-6.2-sol) t25(hiyo-key2/gpt-6-luna) t26(devseek/deepseek-v4.1-flash-free)"

(
  bash scripts/launch.sh t24-club-cursor openai-codex gpt-6.2-sol prompts/t24_club_cursor.md scratch/t24/out 3 2700 >> "$FLEET_LOG" 2>&1
  log "L7 t24 launcher exited rc=$?"
) &
P24=$!

(
  bash scripts/launch.sh t25-nation-fields hiyo-key2 gpt-6-luna prompts/t25_nation_fields.md scratch/t25/out 3 2100 >> "$FLEET_LOG" 2>&1
  log "L7 t25 launcher exited rc=$?"
) &
P25=$!

(
  bash scripts/launch.sh t26-hist-people devseek deepseek-v4.1-flash-free prompts/t26_hist_people.md scratch/t26/out 4 1800 >> "$FLEET_LOG" 2>&1
  log "L7 t26 launcher exited rc=$?"
) &
P26=$!

wait "$P24" "$P25" "$P26"
log "wave7 all launchers finished at $(date '+%H:%M:%S')"
exit 0