#!/usr/bin/env bash
# wave9_fleet.sh — 四路并行第 2 波(接第 1 波成果):
#   车道1 t75(sol/gpt-6.2-sol) 拿 t72 槽位清单做 wire-first xref 反查,收三主表尾
#   车道2 t76a(devseek) t73 工具 + t74 行框:stadium(21)+team(24)
#   车道3 t76b(devseek) award(0)+language(8)+media(7)
#   车道4 t76c(devseek) derby(18)+weather(27)+local_region(47)+agreement(56)
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
log(){ echo "[wave9 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }

log "wave9 launch: t75(sol) t76a/t76b/t76c(ds×3)"

(
  bash scripts/launch.sh t75-xrev openai-codex gpt-6.2-sol prompts/t75_slot_xref_reverse.md scratch/t75/out 3 3600 >> "$FLEET_LOG" 2>&1
  log "L9 t75 launcher exited rc=$?"
) &
P75=$!

(
  bash scripts/launch.sh t76a-stadteam devseek deepseek-v4.1-flash-free prompts/t76a_stadium_team.md scratch/t76a/out 4 2400 >> "$FLEET_LOG" 2>&1
  log "L9 t76a launcher exited rc=$?"
) &
P76a=$!

(
  bash scripts/launch.sh t76b-awdlmd devseek deepseek-v4.1-flash-free prompts/t76b_award_language_media.md scratch/t76b/out 4 2400 >> "$FLEET_LOG" 2>&1
  log "L9 t76b launcher exited rc=$?"
) &
P76b=$!

(
  bash scripts/launch.sh t76c-dbwllc devseek deepseek-v4.1-flash-free prompts/t76c_derby_weather_lcrg_agrm.md scratch/t76c/out 4 2400 >> "$FLEET_LOG" 2>&1
  log "L9 t76c launcher exited rc=$?"
) &
P76c=$!

wait "$P75" "$P76a" "$P76b" "$P76c"
log "wave9 all launchers finished at $(date '+%H:%M:%S')"
exit 0
