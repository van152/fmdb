#!/usr/bin/env bash
# t15b 一键重跑(只读;全部写入 scratch/t15b/out/)
set -euo pipefail
cd "$(dirname "$0")/../.."
export FM24_DB_DIR="${FM24_DB_DIR:-D:/tmp2b/fm24-db/scratch/data}"
PY="py -V:3.12 -I -B"
$PY scratch/t15b/probe.py    --out scratch/t15b/out/probe_raw.json
$PY scratch/t15b/probe2.py   --out scratch/t15b/out/probe2.json
$PY scratch/t15b/probe3.py   --out scratch/t15b/out/probe3.json
$PY scratch/t15b/finalize.py
echo "done -> scratch/t15b/out/probe.json + probe.md"
