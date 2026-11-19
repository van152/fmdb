#!/usr/bin/env python3
"""t43 build — 生成 integration_report.json(修前后对照 / 119 抽样 / 回归矩阵)。

本脚本是**证据生成器**,不是生产代码:它允许 import `fm24_dump` 与 `t38_multiframe`
以便做逐字节对照。产品化的加载器 `fm24_dump.load_payload` 本身没有对 t38 的任何依赖
(见 verify.py 的源码检查项)。

用法
----
  py -V:3.12 -I -B scratch/t43/build.py --build      # 跑回归 + 写 integration_report.json
  py -V:3.12 -I -B scratch/t43/build.py --help
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import runpy
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"


def find_root(start: pathlib.Path) -> pathlib.Path:
    for cand in (start, *start.parents):
        if (cand / "AGENTS.md").is_file():
            return cand
    return start.parents[3]


ROOT = find_root(HERE)
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data"))
UPSTREAM = pathlib.Path(r"D:\tmp2b\fm24")
REPORT = OUT / "integration_report.json"

# 对照目标:t33 七表 + 五锚点表 + client 0/2/3 + t29 其余(t29 十三表中未覆盖者)
MF_TARGETS: list[tuple[str, int]] = [
    ("server", 12), ("server", 39), ("server", 45), ("server", 48), ("server", 58),
    ("server", 59), ("server", 73),                      # t33 七表
    ("server", 34), ("server", 66), ("server", 43),      # 锚点表
    ("client", 0), ("client", 2), ("client", 3),
    ("server", 33), ("server", 37), ("server", 50), ("server", 51), ("server", 60),
    ("server", 61), ("server", 62), ("server", 63), ("server", 64), ("server", 70),
    ("client", 25), ("client", 47),
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(cmd: str, extra_env: dict | None = None) -> dict:
    env = dict(os.environ)
    env["FM24_DB_DIR"] = str(DB_DIR)
    if extra_env:
        env.update(extra_env)
    r = subprocess.run(cmd, cwd=str(ROOT), shell=True, capture_output=True, text=True, env=env,
                       encoding="utf-8", errors="replace")
    tail = (r.stdout or "").strip().splitlines()[-8:]
    return {"cmd": cmd, "rc": r.returncode, "tail": tail,
            "stdout_tail": (r.stdout or "")[-8000:], "stderr_tail": (r.stderr or "")[-2000:],
            "stdout_sha256": sha((r.stdout or "").encode("utf-8"))}


def parse_selftest(out: dict) -> dict:
    txt = out["stdout_tail"]
    m = re.search(r"--- fixed (\d+) PASS / (\d+) FAIL / (\d+) SKIP ---", txt)
    res = {"rc": out["rc"]}
    if m:
        res.update({"pass": int(m[1]), "fail": int(m[2]), "skip": int(m[3])})
    res["server34_line"] = next((l for l in out["tail"] if " 34 " in l or "server 34" in l), None)
    return res


def parse_count(out: dict, pattern: str) -> dict:
    m = re.search(pattern, out["stdout_tail"])
    return {"rc": out["rc"], "match": list(m.groups()) if m else None}


def head_selftest(script: str = "scripts/t38_multiframe.py") -> dict:
    """跑 git HEAD 版本的 t38 selftest(不写文件、不是当前工作区副本)。

    用于把「修复后 t38 PASS 计数为何从 25 变 24」钉死:那 1 条是记录旧法差异的
    信息行 `DIFF[EXPECTED(E66-family)] server#34: legacy=12B vs mf=313082B`,
    它被算进 `len(lines)-len(fails)`。修复后差异消失 → 少 1 行,PASS 从 25 变 24,
    FAIL 仍为 0。这是修复生效的**正向证据**,不是回归。
    """
    src = None
    for _attempt in range(3):
        r = subprocess.run(["git", "show", f"HEAD:{script}"], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 and r.stdout:
            src = r
            break
    if src is None:
        return {"git_show_rc": r.returncode, "git_show_stderr": (r.stderr or "").strip()[:400],
                "git_show_stdout_len": len(r.stdout or ""), "cwd": str(ROOT),
                "attempts": 3,
                "note": "git show 失败;HEAD 版本 selftest 未跑(不影响主证据)"}
    env_backup = os.environ.get("FM24_DB_DIR")
    os.environ["FM24_DB_DIR"] = str(DB_DIR)
    path = ROOT / script
    g = {"__name__": "t38_head", "__file__": str(path)}
    try:
        exec(compile(src.stdout, str(path), "exec"), g)
        rc = g["run_selftest"](verbose=False)
        return {"rc": rc, "git_blob": hashlib.sha256(src.stdout.encode()).hexdigest()[:16],
                "note": "HEAD 版本 + 修复后 fm24_dump:legacy 差异行消失 -> PASS 25->24,FAIL 0"}
    finally:
        if env_backup is None:
            os.environ.pop("FM24_DB_DIR", None)
        else:
            os.environ["FM24_DB_DIR"] = env_backup


def main() -> int:
    ap = argparse.ArgumentParser(description="t43 integration report builder")
    ap.add_argument("--build", action="store_true", help="跑回归并写 integration_report.json")
    ap.add_argument("--skip-regressions", action="store_true", help="跳过子进程回归,只算修前后对照")
    args = ap.parse_args()
    if not args.build:
        ap.print_help()
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(ROOT / "scripts"))
    import fm24_dump  # 被验对象

    codec = fm24_dump._reader()

    # ---------- 1 修前后单表对照(load_payload vs t38 mf vs legacy 复算)
    mf_ns = runpy.run_path(str(ROOT / "scripts/t38_multiframe.py"))
    load_payload_mf = mf_ns["load_payload_mf"]
    legacy_ns = runpy.run_path(str(OUT / "verify.py"))  # 只取 legacy/expected 复算函数
    legacy_payload = legacy_ns["legacy_payload"]

    compare_rows = []
    n_same = n_diff = n_raise = 0
    for arch, tid in MF_TARGETS:
        row = {"archive": arch, "table": tid}
        try:
            now = fm24_dump.load_payload(codec, arch, tid)
            row.update({"fixed_len": len(now), "fixed_sha256": sha(now)})
        except Exception as exc:
            row["fixed_error"] = f"{type(exc).__name__}: {exc}"
            n_raise += 1
            compare_rows.append(row)
            continue
        try:
            mf = load_payload_mf(codec, arch, tid)
            row.update({"mf_len": len(mf), "mf_sha256": sha(mf), "fixed_eq_mf": now == mf})
        except Exception as exc:
            row["mf_error"] = f"{type(exc).__name__}: {exc}"
            row["fixed_eq_mf"] = None
        try:
            old = legacy_payload(arch, str(tid))
            row.update({"legacy_len": old["len"], "legacy_sha256": old["sha256"],
                        "legacy_eq_fixed": old["sha256"] == row["fixed_sha256"],
                        "legacy_hit_delta": old.get("hit_delta_from_correct")})
        except Exception as exc:
            row["legacy_error"] = f"{type(exc).__name__}: {exc}"
        if row.get("fixed_eq_mf") is True:
            n_same += 1
        elif row.get("fixed_eq_mf") is False:
            n_diff += 1
        compare_rows.append(row)

    # ---------- 2 119 受影响条目抽样(全部入报告;报告摘要见 REPORT.md)
    affected_ns = legacy_ns["affected_entries"]
    expected_payload = legacy_ns["expected_payload"]
    affected_rows = []
    for name in ("server", "client", "lang_update"):
        for e in affected_ns(name):
            sel = pathlib.PurePosixPath(e["path"]).name
            exp = expected_payload(name, sel)
            old = legacy_payload(name, sel)
            affected_rows.append({
                "archive": name, "path": e["path"], "declared_size": e["size"],
                "prev_path": e["prev_path"], "prev_packed": e["prev_packed"],
                "member_start": exp["member_start"], "data_base": exp["data_base"],
                "fixed_len": exp["len"], "fixed_sha256": exp["sha256"],
                "legacy_len": old["len"], "legacy_sha256": old["sha256"],
                "legacy_bytes_differ": old["sha256"] != exp["sha256"],
                "len_equals_size": exp["len"] == e["size"],
            })

    # ---------- 3 回归矩阵
    regressions: dict[str, dict] = {}
    if not args.skip_regressions:
        o = run("py -V:3.12 -I -B scripts/fm24_dump.py --selftest")
        regressions["fm24_dump --selftest"] = {
            **parse_selftest(o),
            "baseline_before_fix": "49 PASS / 0 FAIL / 1 SKIP (server 34 SKIP: 12 != 313082)",
            "expected_after_fix": "50 PASS / 0 FAIL / 0 SKIP",
            "fixed": "server 34 SKIP -> PASS (payload 313082 == 上游 313082)",
            "tail": o["tail"],
        }
        o = run("py -V:3.12 -I -B scripts/t01_anchors.py")
        regressions["t01_anchors"] = {**parse_count(o, r"(\d+)/(\d+) checks passed"),
                                      "expect": "7/7", "tail": o["tail"]}
        o = run("py -V:3.12 -I -B scripts/t38_multiframe.py --selftest")
        regressions["t38_multiframe --selftest"] = {
            **parse_count(o, r"--- t38 multiframe selftest: (\d+) PASS / (\d+) FAIL ---"),
            "note": "参考加载器独立于本次修改(未 import/未修改);PASS 计数含诊断行,见 REPORT §4",
            "tail": o["tail"],
        }
        spots = {
            "t39_spot": r"--- (\d+) PASS / (\d+) FAIL ---",
            "t34_spot": r"=== t34 spot: (\d+)/(\d+) ===",
            "t36_spot": r"=== t36 spot: (\d+)/(\d+) ===",
        }
        for spot, pat in spots.items():
            o = run(f"py -V:3.12 -I -B scratch/cmd/{spot}.py")
            uses = "load_payload" if "load_payload" in (ROOT / f"scratch/cmd/{spot}.py").read_text(encoding="utf-8") else "own pick_frame"
            regressions[spot] = {**parse_count(o, pat), "uses": uses, "expect": "26/26" if spot == "t39_spot" else None,
                                 "tail": o["tail"]}
        o = run("py -V:3.12 -I -B scratch/t43/out/verify.py --selftest")
        regressions["t43 verify"] = {**parse_count(o, r"--- t43 verify: (\d+) PASS / (\d+) FAIL ---"),
                                     "tail": o["tail"]}

    doc = {
        "task": "t43 — 把 t38 data_base 修复集成进 fm24_dump.load_payload",
        "change_scope": {
            "file": "scripts/fm24_dump.py",
            "function": "load_payload",
            "signature_unchanged": "load_payload(codec, archive: str, tid: int) -> bytes",
            "other_functions_untouched": ["_reader", "fixed_specs", "walk_fixed", "walk_lrg",
                                          "walk_club_block", "dump", "main"],
            "no_import_of_t38": True,
            "fix": [
                "base = codec['_archive_layout'](db)['data_base']  (动态取,不硬编码 34)",
                "成员区 = db[base+offset : base+offset+packed_size)",
                "区内逐帧解压(zstd decompressobj + unused_data 推进),以 len(frame)==entry['size'] 选帧",
                "无吻合帧 → RuntimeError(不回落首帧,不静默截断)",
            ],
        },
        "single_frame_regression_vs_load_payload_mf": {
            "targets": len(MF_TARGETS),
            "byte_identical": n_same, "divergent": n_diff, "raised": n_raise,
            "rows": compare_rows,
        },
        "affected_entries_119": {
            "count": len(affected_rows),
            "per_archive": {a: sum(1 for r in affected_rows if r["archive"] == a)
                            for a in ("server", "client", "lang_update")},
            "all_len_equals_size_after_fix": all(r["len_equals_size"] for r in affected_rows),
            "legacy_bytes_differ": sum(1 for r in affected_rows if r["legacy_bytes_differ"]),
            "legacy_identical_12B_stub": [
                r for r in affected_rows if not r["legacy_bytes_differ"]
            ][:50],
            "rows": affected_rows,
        },
        "regression_matrix": regressions,
        "t38_selftest_accounting": {
            "why_count_changes": (
                "t38 selftest 的 PASS 数 = len(lines)-len(fails),而旧法差异的提示行 "
                "`DIFF[EXPECTED(E66-family)] server#34: legacy=12B vs mf=313082B` 也算一行。"
                "修复后该差异消失 -> 少 1 行:PASS 25->24,FAIL 仍 0。属正向证据。"
            ),
            "accepted_baseline": "25 PASS / 0 FAIL (含 1 条 server#34 legacy-vs-mf 差异行)",
            "after_fix_expected": "24 PASS / 0 FAIL (差异行消失;server 34 已不再是特例)",
            "head_version_run": head_selftest(),
            "working_tree_run": regressions.get("t38_multiframe --selftest", {}).get("match"),
            "working_tree_externally_modified": (
                "本任务期间 `scripts/t38_multiframe.py` 被另一会话追加了 145 行(check #10/#11:"
                "无界选帧对照 + 帧数构成证据),因此现场跑出 32 PASS。该文件不属于本任务改动范围,"
                "本次未触碰它;HEAD 版本与新版本均 0 FAIL。"
            ),
        },
        "evidence_level": {
            "integration_correctness": "L1 (自家解码自检:460 条目单帧 + len==size + packed 区 SHA 自证)",
            "anchors_cross_check": "L2 (t29/t33/t35 已落盘 payload size+sha256)",
            "data_base_structural_meaning": "候选(未做 L3 exe 静态确认;仅操作性偏移)",
            "L4": 0,
        },
    }
    REPORT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {REPORT}")
    print(f"  single-frame: {n_same} identical / {n_diff} divergent / {n_raise} raised (of {len(MF_TARGETS)})")
    print(f"  affected entries: {len(affected_rows)} (len==size: {doc['affected_entries_119']['all_len_equals_size_after_fix']})")
    for k, v in regressions.items():
        print(f"  [{k}] rc={v.get('rc')} {v.get('pass', v.get('match'))} {v.get('fail', '')} {v.get('skip', '')}")
    return 0 if n_diff == 0 and n_raise == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
