#!/usr/bin/env bash
# wave8_fleet.sh — 四路并行第 1 波:
#   车道1 t71(sol/gpt-6.2-sol) CLUB+0x100 跨对象链 + 22 cnst 转正
#   车道2 t72(devseek) club/nation/comp 未命名槽位清单 + 值域指纹(给 t75 铺路)
#   车道3 t73(devseek) 通用 table_slot_mapper.py + city/cont/regi/curr 四表闭环
#   车道4 t74(devseek) 九表双档行框闭合 + identity 自证(给 t76 铺路)
# 指挥官在线监收;各车道只写 scratch/tNN/ 与 scripts/tNN_*.py,互不抢文件。
set -u
cd /d/tmp2b/fm24-db || exit 1
export FM24_DB_DIR="D:/tmp2b/fm24-db/scratch/data"

FLEET_LOG=scratch/cmd/fleet.log
log(){ echo "[wave8 $(date '+%m-%d %H:%M:%S')] $*" >> "$FLEET_LOG"; }

log "wave8 launch: t71(sol) t72(ds#1) t73(ds#2) t74(ds#3)"

(
  bash scripts/launch.sh t71-clubcnst openai-codex gpt-6.2-sol prompts/t71_club100_cnst.md scratch/t71/out 3 3600 >> "$FLEET_LOG" 2>&1
  log "L8 t71 launcher exited rc=$?"
) &
P71=$!

(
  bash scripts/launch.sh t72-slotfp devseek deepseek-v4.1-flash-free prompts/t72_slot_fingerprint.md scratch/t72/out 4 2400 >> "$FLEET_LOG" 2>&1
  log "L8 t72 launcher exited rc=$?"
) &
P72=$!

(
  bash scripts/launch.sh t73-slotmapper devseek deepseek-v4.1-flash-free prompts/t73_slot_mapper.md scratch/t73/out 4 2400 >> "$FLEET_LOG" 2>&1
  log "L8 t73 launcher exited rc=$?"
) &
P73=$!

(
  bash scripts/launch.sh t74-frames9 devseek deepseek-v4.1-flash-free prompts/t74_row_frames9.md scratch/t74/out 4 2700 >> "$FLEET_LOG" 2>&1
  log "L8 t74 launcher exited rc=$?"
) &

P74=$!
wait "$P71" "$P72" "$P73" "$P74"
log "wave8 all launchers finished at $(date '+%H:%M:%S')"
exit 0
