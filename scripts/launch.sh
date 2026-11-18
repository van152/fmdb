#!/usr/bin/env bash
# launch.sh — 通用 pi 任务发射器(指挥官用,后台长跑 + 断流重试)
# usage: bash scripts/launch.sh <TASK> <PROVIDER> <MODEL> <PROMPT_FILE> <OUTBOX> [MAX_ATTEMPTS] [TIMEOUT_SEC]
set -u
cd /d/tmp2b/fm24-db || exit 1

TASK="${1:?task name}"; PROVIDER="${2:?provider}"; MODEL="${3:?model}"
PROMPT="${4:?prompt file}"; OUTBOX="${5:?outbox}"; MAX="${6:-4}"; TMO="${7:-900}"
mkdir -p "$OUTBOX"
LOG="scratch/t02/pi-logs/${TASK}.log"; ATT="scratch/t02/pi-logs/${TASK}.attempt.log"
: > "$LOG"

EXTRA=""
case "$PROVIDER" in
  openai-codex) EXTRA="--thinking high" ;;
  *) EXTRA="--thinking max" ;;
esac

for i in $(seq 1 "$MAX"); do
  echo "=== attempt $i/$MAX $(date) provider=$PROVIDER model=$MODEL ===" >> "$LOG"; : > "$ATT"
  timeout "$TMO" pi --provider "$PROVIDER" --model "$MODEL" $EXTRA --approve -p \
    -n "$TASK" --session-dir scratch/t02/pi-sessions --session-id "${TASK}-${PROVIDER}" \
    -p "$(cat "$PROMPT")

---

## 本次任务参数
- 输出目录 OUTDIR = ${OUTBOX}
- 若上文已有进度,接着做,不要从头开始。
- 完成后打印交付清单。" \
    >> "$ATT" 2>&1
  RC=$?; cat "$ATT" >> "$LOG"
  # 成功判据(宽):status 不再是 in_progress(允许 complete_*/partial_* 等带限定词的诚实标注)
  # 或 outbox 有 ≥2 个实质文件且含 status 字段 —— 模型常把结论写成 status:"complete_<caveat>",
  # 旧判据只认 complete/partial 精确字符串,会把已交付的任务误判为失败(t02p-pw 就是这个 bug)。
  if grep -rqE '"status"[[:space:]]*:[[:space:]]*"(complete|partial)[^"]*"|DONE type=' "$OUTBOX" 2>/dev/null; then
    echo "=== DONE $TASK attempt=$i rc=$RC $(date) ===" >> "$LOG"; exit 0
  fi
  NF=$(find "$OUTBOX" -maxdepth 1 -type f -size +1k 2>/dev/null | wc -l)
  if [ "$NF" -ge 2 ] && grep -rq '"status"' "$OUTBOX" 2>/dev/null; then
    echo "=== DONE(heuristic: $NF substantial files) $TASK attempt=$i rc=$RC $(date) ===" >> "$LOG"; exit 0
  fi
  echo "=== attempt $i rc=$RC $(date) ===" >> "$LOG"
  if grep -qiE "upstream_saturated|temporarily unavailable|503|throttling|upstream model failed|rate.limit|overloaded" "$ATT"; then
    W=$(( 45 * i )); echo "--- throttled, sleep ${W}s ---" >> "$LOG"; sleep "$W"
  else sleep 15; fi
done
echo "=== gave up $TASK after $MAX attempts $(date) ===" >> "$LOG"; exit 1
