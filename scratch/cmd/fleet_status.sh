#!/usr/bin/env bash
cd /d/tmp2b/fm24-db
date +%H:%M:%S
for d in t77 t81 t83 t84 t85; do
  n=$(ls scratch/$d/out/ 2>/dev/null | wc -l)
  recent=$(find scratch/$d -newermt "2026-11-21 06:00" -type f -not -path "*/pi-sessions/*" 2>/dev/null | wc -l)
  printf "%s out=%s recent=%s\n" "$d" "$n" "$recent"
done
echo "--- walls:"
grep -h "rc=124\|gave up\|DONE" scratch/t02/pi-logs/t77-schema-v11.log scratch/t02/pi-logs/t81-fkvar.log scratch/t02/pi-logs/t84-namepool.log scratch/t02/pi-logs/t83-award-lang-neon.log 2>/dev/null | tail -6
