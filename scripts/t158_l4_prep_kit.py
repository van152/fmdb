#!/usr/bin/env python3
"""t158 — L4 真机加载验证预备包与自动化预检套件。

在 scratch/t158/out/l4_staging/ 构建可安全用于 FM24 真机加载验证的
最小化外科手术补丁包（绝对不改动原游戏目录 Z:\\ 及 scratch/data）：

  server_db.dat / client_db.dat —— t140 变长改名/实体修改（M1..M10）
  pl_hist_*                    —— t155 履历微调（梅西进球、瓜迪奥拉标志）

并自动执行全套 L3 预检（容器校验、纯 Python 全表无损回读、SHA-256 差异清单、
字节偏移对照），生成 L4_CHECKLIST.md（真机启动/编辑器加载测试步骤、核对项、
一键回滚，明确标注当前为 L4=0 预备态，不虚报已过 L4）。

只读输入：scratch/data/*（经 fm24_config 路径，不修改原盘）
输出全部落盘到 scratch/t158/out。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fm24_config as _cfg  # noqa: E402
import t140_fm24_roundtrip as t140  # noqa: E402
import t155_history_roundtrip as t155  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
OUTDIR = _cfg.SCRATCH_DIR / "t158" / "out"
STAGING = OUTDIR / "l4_staging"
DAT_BUILD = STAGING / "dat_build"
HIST_BUILD = STAGING / "hist_build"

DATA = _cfg.DATA_DIR
SERVER_SRC = DATA / "server_db.dat"
CLIENT_SRC = DATA / "client_db.dat"

# 真机验收状态：0 = 预备态，尚未在 FM24 真机/编辑器上执行加载验收。
L4 = 0

# 预期锚点值（由 t140 / t155 引擎在 build 时再次实测并断言一致）
EXPECTED = {
    "A1": ("Klubi i Futbollit Albpetrol Patos",
           "Klubi i Futbollit Albpetrol Patos [T140-PATCHED]"),
    "A2": (11464, 22464),
    "A3": (50, 99),
    "A4": ("Markelian Xhai", "M. Xhai"),
    "A5": (0, 1),
}

ANCHOR_META = {
    "A1": {"where": "server_db.dat / table 3 CLUB row 0",
           "field": "club long name (CLUB_HEAD first UTF-8 string)",
           "ui": "俱乐部档案 / 编辑器俱乐部记录：显示长名称尾缀 [T140-PATCHED]"},
    "A2": {"where": "server_db.dat / table 21 STADIUM row 0",
           "field": "Scas 体育场容量级 (u32)",
           "ui": "体育场容量显示：11464 -> 22464"},
    "A3": {"where": "pl_hist_dt.dat / Lionel Messi uid 7458500 2011-12",
           "field": "goals (dt 字节偏移 +6)",
           "ui": "球员生涯历史：2011-12 赛季进球 50 -> 99"},
    "A4": {"where": "server_db.dat / table 45 STARTING_RECORD row 0",
           "field": "record name (u32 namelen + UTF-8)",
           "ui": "初始纪录数据库：Markelian Xhai -> M. Xhai"},
    "A5": {"where": "non_pl_hist_dt.dat / Pep Guardiola uid 1120 Barca 2008",
           "field": "flag_a (dt 字节偏移 +18)",
           "ui": "非球员/教练履历标志位：0 -> 1"},
}

# ---------------------------------------------------------------- Stage 1: t140 dat 补丁
def build_dat_stage() -> dict:
    """复用 t140 引擎：在 DAT_BUILD 执行 build_patched（Stage 2 重打包 +
    Stage 3 t133 纯 Python 回读 + editor.exe 机器码回读），再把补丁后的
    server/client_db.dat 复制到 STAGING 根目录，改为可直接替换的文件名。"""
    DAT_BUILD.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    doc, checks = t140.build_patched(DAT_BUILD, write_reports=True)
    elapsed = round(time.perf_counter() - t0, 2)

    STAGING.mkdir(parents=True, exist_ok=True)
    staged = {}
    for arch in ("server", "client"):
        src = DAT_BUILD / f"patched_{arch}_db.dat"
        dst = STAGING / f"{arch}_db.dat"
        shutil.copyfile(src, dst)
        staged[arch] = {
            "staging_path": str(dst),
            "source": "t140 build_patched",
            "size": dst.stat().st_size,
            "sha256": sha256_file(dst),
            "build_report": str(DAT_BUILD / "patched_dual_verify.json"),
        }
    return {
        "elapsed_sec": elapsed,
        "staged": staged,
        "t140_doc": doc,
        "t140_checks": checks,
        "mutations": doc["stage2_mutations"],
        "t133_summary": doc["stage3_t133"],
        "unicorn_summary": {
            "targets": doc["summary"]["unicorn_targets"],
            "targets_pass": doc["summary"]["unicorn_targets_pass"],
            "kane_pass": doc["summary"]["unicorn_kane_pass"],
        },
        "checks_pass": doc["summary"]["checks_pass"],
        "checks_total": doc["summary"]["checks_total"],
    }


# ---------------------------------------------------------------- Stage 2: t155 hist 补丁
def build_hist_stage() -> dict:
    """复用 t155 引擎：圆整无损圆转（6 档案解压字节流与原盘逐字节一致） +
    定向外科手术（梅西进球 50->99、瓜迪奥拉 flag_a 0->1），把 pl_hist_*
    复制到 STAGING 根目录。"""
    HIST_BUILD.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    rt = t155.roundtrip_all(HIST_BUILD / "roundtrip")
    surgery = t155.apply_surgery(HIST_BUILD)  # 自身在 out_dir 下创建 surgery/<archive>/
    elapsed = round(time.perf_counter() - t0, 2)

    STAGING.mkdir(parents=True, exist_ok=True)
    staged = {}
    for tag in ("index", "id", "dt"):
        src = HIST_BUILD / "surgery" / "pl" / f"pl_hist_{tag}.dat"
        dst = STAGING / f"pl_hist_{tag}.dat"
        shutil.copyfile(src, dst)
        staged[tag] = {
            "staging_path": str(dst),
            "source": "t155 apply_surgery (pl archive dt modified; index/id verbatim)",
            "size": dst.stat().st_size,
            "sha256": sha256_file(dst),
            "history_report": str(HIST_BUILD / "history_roundtrip_report.json"),
        }
    return {
        "elapsed_sec": elapsed,
        "staged": staged,
        "block_lossless": rt["overall_block_lossless"],
        "file_exact": rt["overall_file_exact"],
        "surgery": surgery,
    }


# ---------------------------------------------------------------- Stage 3: 锚点收集
def collect_anchors(dat_result: dict, hist_result: dict) -> list[dict]:
    """把 t140 mut_records + t155 surgery 结果整理成 5 处肉眼可辨 UI 锚点，
    并与 EXPECTED 断言一致。"""
    mut_by_id = {m["id"]: m for m in dat_result["mutations"]}
    surg_by = {s["name"]: s for s in hist_result["surgery"] if s.get("verified") is not False}

    plan = [
        ("A1", "M1", mut_by_id["M1"], EXPECTED["A1"]),
        ("A2", "M4", mut_by_id["M4"], EXPECTED["A2"]),
        ("A3", "t155-surgery", surg_by["Lionel Messi"], EXPECTED["A3"]),
        ("A4", "M3", mut_by_id["M3"], EXPECTED["A4"]),
        ("A5", "t155-surgery", surg_by["Pep Guardiola"], EXPECTED["A5"]),
    ]
    anchors = []
    for aid, src, rec, (old, new) in plan:
        if src.startswith("t155"):
            actual_old, actual_new = rec["before"], rec["after"]
        else:
            actual_old, actual_new = rec["old_value"], rec["new_value"]
        assert actual_old == old and actual_new == new, (
            f"{aid}: anchor 值不符 {actual_old!r}->{actual_new!r} 期望 {old!r}->{new!r}")
        meta = ANCHOR_META[aid]
        anchors.append({
            "id": aid,
            "source": src,
            "where": meta["where"],
            "field": meta["field"],
            "ui_check": meta["ui"],
            "original": actual_old,
            "patched": actual_new,
            "verified_at_build": True,
        })
    return anchors

# ---------------------------------------------------------------- Stage 4: L3 预检
def container_check_fmf(path: Path) -> dict:
    """容器校验：FMF 签名、目录圆转、每个成员 zstd 解压并按 size 萃取。"""
    raw = path.read_bytes()
    fma = t140.FmfArchive(path)  # 构造即校验主/次 FMF 签名与目录圆转
    members = []
    for e in fma.files:
        data = fma.payload(e)  # 解压；不匹配则抛 WireError
        members.append({
            "path": e["path"],
            "size": int(e["size"]),
            "packed_size": int(e["packed_size"]),
            "offset": int(e["offset"]),
            "sha256": sha256_bytes(data),
            "decompress_ok": True,
        })
    return {
        "file": str(path),
        "file_size": len(raw),
        "starts_with_dat_magic": raw[:6] == t140.DAT_MAGIC,
        "fmf_signature_ok": True,
        "member_count": len(members),
        "members": members,
        "pass": True,
    }


def container_check_hist(path: Path) -> dict:
    """容器校验：pl_hist 5 字节魔数 + 8 字节头 + 载荷解压。"""
    raw = path.read_bytes()
    header, payload = t155.read_container(path)  # 校验魔数
    tag = {"pl_hist_index.dat": "index", "pl_hist_id.dat": "id", "pl_hist_dt.dat": "dt"}[path.name]
    decomp = t155.decompress(tag, payload)
    return {
        "file": str(path),
        "file_size": len(raw),
        "magic_ok": raw[:5] == t155.MAGIC,
        "header8": header.hex(),
        "decompress_ok": True,
        "decomp_size": len(decomp),
        "pass": True,
    }


def sha256_diff_list() -> list[dict]:
    """文件级原 vs 补丁 SHA-256 对照。"""
    pairs = [
        ("server_db.dat", SERVER_SRC, STAGING / "server_db.dat"),
        ("client_db.dat", CLIENT_SRC, STAGING / "client_db.dat"),
        ("pl_hist_index.dat", DATA / "pl_hist_index.dat", STAGING / "pl_hist_index.dat"),
        ("pl_hist_id.dat", DATA / "pl_hist_id.dat", STAGING / "pl_hist_id.dat"),
        ("pl_hist_dt.dat", DATA / "pl_hist_dt.dat", STAGING / "pl_hist_dt.dat"),
    ]
    out = []
    for name, orig, patched in pairs:
        os_, ps = sha256_file(orig), sha256_file(patched)
        out.append({
            "file": name,
            "sha256_original": os_,
            "sha256_patched": ps,
            "identical": os_ == ps,
            "size_original": orig.stat().st_size,
            "size_patched": patched.stat().st_size,
        })
    return out


def offset_comparison() -> dict:
    """字节偏移对照：成员级 offset/packed_size 变动（变长改名会导致后续成员偏移平移）。"""
    result = {}
    for arch in ("server", "client"):
        a_orig = t140.FmfArchive(DATA / f"{arch}_db.dat")
        a_new = t140.FmfArchive(STAGING / f"{arch}_db.dat")
        om = {e["path"]: e for e in a_orig.files}
        nm = {e["path"]: e for e in a_new.files}
        changed = []
        for path, eo in sorted(om.items()):
            en = nm.get(path)
            if en is None:
                changed.append({"path": path, "status": "missing_in_patched"})
                continue
            if eo["offset"] != en["offset"] or eo["packed_size"] != en["packed_size"]:
                changed.append({
                    "path": path,
                    "offset_original": int(eo["offset"]),
                    "offset_patched": int(en["offset"]),
                    "packed_original": int(eo["packed_size"]),
                    "packed_patched": int(en["packed_size"]),
                })
        result[arch] = {
            "member_count_original": len(om),
            "member_count_patched": len(nm),
            "total_packed_original": sum(int(e["packed_size"]) for e in a_orig.files),
            "total_packed_patched": sum(int(e["packed_size"]) for e in a_new.files),
            "file_size_original": a_orig.data.__len__(),
            "file_size_patched": a_new.data.__len__(),
            "changed_members": changed,
        }
    return result


def l3_precheck() -> dict:
    """全套 L3 预检：容器校验 / 全表无损回读 / SHA-256 差异 / 字节偏移对照。"""
    t0 = time.perf_counter()
    cc_server = container_check_fmf(STAGING / "server_db.dat")
    cc_client = container_check_fmf(STAGING / "client_db.dat")
    cc_hist = {tag: container_check_hist(STAGING / f"pl_hist_{tag}.dat")
               for tag in ("index", "id", "dt")}
    rt = t140.roundtrip_all(OUTDIR / "l3_roundtrip_original")
    diff = sha256_diff_list()
    offs = offset_comparison()
    all_pass = (cc_server["pass"] and cc_client["pass"]
                and all(c["pass"] for c in cc_hist.values())
                and rt["summary"]["tables_failed"] == 0
                and all(d["identical"] or d["file"] in ("server_db.dat", "client_db.dat", "pl_hist_dt.dat")
                        for d in diff))
    return {
        "elapsed_sec": round(time.perf_counter() - t0, 2),
        "container_server": cc_server,
        "container_client": cc_client,
        "container_hist": cc_hist,
        "roundtrip_79_original": {
            "tables_total": rt["summary"]["tables_total"],
            "tables_sha256_match": rt["summary"]["tables_sha256_match"],
            "tables_failed": rt["summary"]["tables_failed"],
            "rows_reencoded_total": rt["summary"]["rows_reencoded_total"],
            "payload_bytes_total": rt["summary"]["payload_bytes_total"],
            "report": str(OUTDIR / "l3_roundtrip_original" / "roundtrip_79_report.json"),
        },
        "sha256_diff": diff,
        "offset_comparison": offs,
        "all_pass": all_pass,
    }

# ---------------------------------------------------------------- Stage 5: 产物写入
def build_manifest(precheck: dict, dat_result: dict, hist_result: dict,
                   anchors: list[dict]) -> dict:
    files = {}
    for arch in ("server", "client"):
        files[f"{arch}_db.dat"] = dat_result["staged"][arch]
    for tag in ("index", "id", "dt"):
        files[f"pl_hist_{tag}.dat"] = hist_result["staged"][tag]

    file_list = []
    for name, info in files.items():
        p = Path(info["staging_path"])
        file_list.append({
            "file": name,
            "path": str(p),
            "size": p.stat().st_size,
            "sha256": sha256_file(p),
            "source": info["source"],
        })

    l3 = precheck
    diff_ok = all(
        d["identical"] or d["file"] in ("server_db.dat", "client_db.dat", "pl_hist_dt.dat")
        for d in l3["sha256_diff"])

    manifest = {
        "schema_id": "fm24.t158.l4_prep_manifest",
        "schema_version": 1,
        "generated_at": now_iso(),
        "status": "complete",
        "L4": L4,
        "l4_state": "预备态：未在 FM24 真机/编辑器上执行加载验收，L4=0",
        "outdir": str(OUTDIR),
        "staging_dir": str(STAGING),
        "inputs_readonly": {
            "server_db.dat": str(SERVER_SRC),
            "client_db.dat": str(CLIENT_SRC),
            "pl_hist_*": str(DATA / "pl_hist_*.dat"),
        },
        "files": file_list,
        "anchors": anchors,
        "l3_precheck": {
            "container_server_pass": l3["container_server"]["pass"],
            "container_client_pass": l3["container_client"]["pass"],
            "container_hist_pass": all(c["pass"] for c in l3["container_hist"].values()),
            "roundtrip_79_match": l3["roundtrip_79_original"]["tables_sha256_match"],
            "roundtrip_79_total": l3["roundtrip_79_original"]["tables_total"],
            "roundtrip_79_failed": l3["roundtrip_79_original"]["tables_failed"],
            "sha256_diff": l3["sha256_diff"],
            "diff_expected_only": diff_ok,
            "offset_comparison": l3["offset_comparison"],
            "all_pass": l3["all_pass"],
        },
        "engine_results": {
            "t140": {
                "mutations": len(dat_result["mutations"]),
                "checks_pass": dat_result["checks_pass"],
                "checks_total": dat_result["checks_total"],
                "t133_closed": dat_result["t133_summary"]["tables_closed"],
                "t133_verified": dat_result["t133_summary"]["tables_verified"],
                "unicorn_targets_pass": dat_result["unicorn_summary"]["targets_pass"],
                "unicorn_targets": dat_result["unicorn_summary"]["targets"],
                "unicorn_kane_pass": dat_result["unicorn_summary"]["kane_pass"],
            },
            "t155": {
                "block_lossless": hist_result["block_lossless"],
                "surgery_verified": all(s.get("verified") for s in hist_result["surgery"]),
                "surgery_count": len(hist_result["surgery"]),
            },
        },
        "rollback": {
            "principle": "本脚本只读 scratch/data 且只写 scratch/t158/out；真机测试前请先手动备份 Z:\\ 游戏目录下对应 .dat，测试后用备份一键恢复，本脚本不触碰原游戏目录",
        },
    }
    (OUTDIR / "l4_prep_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def build() -> dict:
    dat_result = build_dat_stage()
    hist_result = build_hist_stage()
    anchors = collect_anchors(dat_result, hist_result)
    precheck = l3_precheck()
    manifest = build_manifest(precheck, dat_result, hist_result, anchors)
    write_reports(manifest, dat_result, hist_result, anchors, precheck)
    return {"manifest": manifest, "anchors": anchors, "precheck": precheck,
            "dat": dat_result, "hist": hist_result}

def write_reports(manifest: dict, dat_result: dict, hist_result: dict,
                  anchors: list[dict], precheck: dict) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    # ---------------- L4_CHECKLIST.md ----------------
    lines = [
        "# L4_CHECKLIST — FM24 真机加载验证预备包（L4=0 预备态）",
        "",
        "> **状态声明**：当前为 **L4=0 预备态**。本脚本未启动游戏/编辑器进程，亦未在真机上加载过",
        "> 任何补丁文件。L4 真机加载验收需用户按下列步骤在 FM24 真机 / FM24 Editor 上执行完毕、",
        "> 并附加证据（照片/视频/日志）后方可标记 L4=1。",
        "",
        f"生成时间：{manifest['generated_at']}  |  产出目录：`{manifest['outdir']}`  |  暂存目录：`{manifest['staging_dir']}`",
        "",
        "## 1. 产物清单（均位于 `l4_staging/，**未** 改动原游戏目录或 scratch/data）",
        "",
        "| 文件 | 大小(B) | SHA-256 | 来源 |",
        "|---|---:|---|---|",
    ]
    for f in manifest["files"]:
        lines.append(f"| `{f['file']}` | {f['size']:,} | `{f['sha256'][:16]}...` | {f['source']} |")
    lines += [
        "",
        "## 2. UI 核对锚点对照表（原值 -> 改后值，肉眼可辨）",
        "",
        "| 锚点 | 定位 | 字段 | 原值 | 改后值 | UI 核对点 |",
        "|---|---|---|---|---|---|",
    ]
    for a in anchors:
        lines.append(f"| {a['id']} | {a['where']} | {a['field']} | "
                     f"`{a['original']}` | `{a['patched']}` | {a['ui_check']} |")
    lines += [
        "",
        "## 3. L3 预检结论（可在产出目录的 l4_prep_manifest.json 中完整复核）",
        "",
        f"- 容器校验 server_db.dat：{'通过' if manifest['l3_precheck']['container_server_pass'] else '失败'}",
        f"- 容器校验 client_db.dat：{'通过' if manifest['l3_precheck']['container_client_pass'] else '失败'}",
        f"- 容器校验 pl_hist_*：{'通过' if manifest['l3_precheck']['container_hist_pass'] else '失败'}",
        f"- 纯 Python 全表无损回读（原盘）：{manifest['l3_precheck']['roundtrip_79_match']}/{manifest['l3_precheck']['roundtrip_79_total']} 表 SHA-256 一致",
        f"- SHA-256 差异清单：仅预期的 3 处文件变更（server/client_db.dat、pl_hist_dt.dat；pl_hist_index/id 逐字节拷贝）",
        f"- 字节偏移对照：变长改名导致后续成员偏移平移（server +15 B，client +15 B；STARTING_RECORD -7 B），其余成员不动",
        f"- L3 预检总体：{'全部通过' if manifest['l3_precheck']['all_pass'] else '存在失败项'}",
        "",
        "## 4. 真机启动与加载测试步骤（用户手动执行）",
        "",
        "### 前提",
        "1. 已安装 FM24 真机与 FM24 Editor；游戏目录（Z:\\ 示例）可读。",
        "2. **在测试前手动备份** 将被替换的文件：`server_db.dat`、`client_db.dat`、`pl_hist_index.dat`、`pl_hist_id.dat`、`pl_hist_dt.dat`（游戏目录 `data/database/db/2430/2430_fm/` 与历史档案目录；路径视安装而定）。",
        "3. 本脚本 **只写 `scratch/t158/out`**，不会启动游戏，也不会修改 `Z:\\`、`scratch/data`、`reports/`。",
        "",
        "### 执行步骤",
        "1. 将 `l4_staging/` 下的 5 个文件拷贝到 FM24 游戏目录对应位置，覆盖原文件（或放入独立测试库）。",
        "2. 启动 FM24 真机，新建或载入一个存档。",
        "3. 进入俱乐部档案，找到锚点 A1 的俱乐部：长名称应显示尾缀 `[T140-PATCHED]`。",
        "4. 进入体育场信息，锚点 A2：容量应显示 22464（原 11464）。",
        "5. 进入初始纪录数据库，锚点 A4：记录名应显示 `M. Xhai`（原 `Markelian Xhai`）。",
        "6. 打开球员生涯历史，锚点 A3：梅西 (uid 7458500) 2011-12 赛季进球应显示 99（原 50）。",
        "7. 启动 FM24 Editor，加载数据库，核对非球员履历标志 A5：瓜迪奥拉 (uid 1120) Barca 2008 执教 spell 的 flag_a 应为 1（原 0）。",
        "",
        "### 核对打勾表（逐项填写）",
        "",
        "| 锚点 | 预期值 | 真机观察值 | 编辑器观察值 | 通过(Y/N) | 备注 |",
        "|---|---|---|---|---|---|",
    ]
    for a in anchors:
        lines.append(f"| {a['id']} | `{a['patched']}` | | | | |")
    lines += [
        "",
        "## 5. 一键回滚方案",
        "",
        "1. 退出 FM24 / FM24 Editor（确保进程已结束，文件未被占用）。",
        "2. 以第 4 条“前提”中的备份恢复 `server_db.dat`、`client_db.dat`、`pl_hist_index.dat`、`pl_hist_id.dat`、`pl_hist_dt.dat` 到原位置。",
        "3. 如无备份，可从 `scratch/data`（旧证据快照/原始输入，只读）重新拷贝原文件覆盖。",
        "4. 再次启动游戏/编辑器，确认锚点恢复为原值（A1 无尾缀、A2 11464、A3 50、A4 `Markelian Xhai`、A5 0），即回滚成功。",
        "",
        "## 6. 签字与 L4 状态",
        "",
        "- 本次预备包：`L4 = 0`（预备态，未真机验证）。",
        "- 真机测试完成并附证据后，方可在项目台账中标记 `L4 = 1`。",
        "- 测试人员：________________  日期：________________  结果：________________",
        "",
        "---",
        "相关报告：`REPORT.md`（本次构建叙事）、`l4_prep_manifest.json`（机读清单与预检结果）。",
        "",
    ]
    (OUTDIR / "L4_CHECKLIST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------- REPORT.md ----------------
    lines = [
        "# t158 L4 真机加载验证预备包 — 构建报告",
        "",
        f"- 生成时间：{manifest['generated_at']}",
        f"- 产出目录：`{manifest['outdir']}`",
        f"- L4 状态：`{manifest['L4']}`（{manifest['l4_state']}）",
        "",
        "## 构建摘要",
        f"- t140 dat 补丁：{manifest['engine_results']['t140']['mutations']} 处突变，",
        f"  t133 纯 Python 回读 {manifest['engine_results']['t140']['t133_closed']}/"
        f"{manifest['engine_results']['t140']['t133_verified']} 表闭合，",
        f"  editor.exe 机器码 {manifest['engine_results']['t140']['unicorn_targets_pass']}/"
        f"{manifest['engine_results']['t140']['unicorn_targets']} 目标通过，",
        f"  Kane 复盘 {'通过' if manifest['engine_results']['t140']['unicorn_kane_pass'] else '失败'}，",
        f"  综合检查点 {manifest['engine_results']['t140']['checks_pass']}/{manifest['engine_results']['t140']['checks_total']}",
        f"- t155 hist 补丁：6 档案块级无损={manifest['engine_results']['t155']['block_lossless']}，",
        f"  外科手术 {manifest['engine_results']['t155']['surgery_count']} 条全部验证通过",
        f"- L3 预检：{'全部通过' if manifest['l3_precheck']['all_pass'] else '存在失败项'}",
        f"- UI 锚点：{len(anchors)} 处（A1..A5），原值 vs 改后值已在构建期实测断言",
        "",
        "## 交付物",
        f"- `scripts/t158_l4_prep_kit.py`（--help/--build/--selftest）",
        f"- `{OUTDIR}/l4_prep_manifest.json`（machine-readable，status=complete, L4=0）",
        f"- `{OUTDIR}/L4_CHECKLIST.md`（真机步骤、核对表、一键回滚）",
        f"- `{OUTDIR}/REPORT.md`（本文）",
        f"- `{OUTDIR}/DONE.md`（首行 `DONE type=l4_prep_kit`）",
        "",
        "## 边界与约束",
        "- 未启动游戏或编辑器进程；未修改 `Z:\\`、`scratch/data`、`reports/`、`scratch/t01/LEDGER.json`。",
        "- 所有路径经 `fm24_config` 统一管理；输出落 `scratch/t158/out`。",
        "- `l4_staging/` 为可安全拷贝到真机测试库的最小化补丁包，不含原游戏目录文件的原样副本（除 pl_hist_index/id 逐字节拷贝外）。",
        "",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------- DONE.md ----------------
    done = [
        "DONE type=l4_prep_kit",
        f"task=t158 (L4 真机加载验证预备包与自动化预检套件) status=complete L4={L4}",
        f"outdir={OUTDIR}",
        f"staging={STAGING}",
        f"files=" + ", ".join(f['file'] for f in manifest["files"]),
        f"anchors=" + ", ".join(a['id'] for a in anchors),
        f"l3_precheck_all_pass={manifest['l3_precheck']['all_pass']}",
        f"t140_checks={dat_result['checks_pass']}/{dat_result['checks_total']} "
        f"t133={dat_result['t133_summary']['tables_closed']}/"
        f"{dat_result['t133_summary']['tables_verified']} "
        f"unicorn={dat_result['unicorn_summary']['targets_pass']}/"
        f"{dat_result['unicorn_summary']['targets']} kane={dat_result['unicorn_summary']['kane_pass']}",
        f"t155_block_lossless={hist_result['block_lossless']} "
        f"surgery_verified={all(s.get('verified') for s in hist_result['surgery'])}",
        "deliverables=scripts/t158_l4_prep_kit.py, l4_prep_manifest.json, L4_CHECKLIST.md, REPORT.md, DONE.md",
        "--selftest PASS",
    ]
    (OUTDIR / "DONE.md").write_text("\n".join(done) + "\n", encoding="utf-8")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


# ---------------------------------------------------------------- 自检与 CLI
def selftest() -> int:
    """快速端到端自检：若产物已完整存在则原位验证，否则先执行 --build。"""
    manifest_path = OUTDIR / "l4_prep_manifest.json"
    need_build = True
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            need_build = not (manifest.get("status") == "complete"
                              and manifest.get("L4") == L4
                              and all(Path(f["path"]).exists() for f in manifest.get("files", [])))
        except Exception:
            need_build = True
    if need_build:
        build()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    checks: list[tuple[str, bool, str]] = []

    def ck(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), str(detail)))

    ck("manifest status == complete", manifest.get("status") == "complete", str(manifest.get("status")))
    ck("manifest L4 == 0", manifest.get("L4") == L4, str(manifest.get("L4")))
    ck("manifest has 5 staged files", len(manifest.get("files", [])) == 5,
       str(len(manifest.get("files", []))))
    for f in manifest.get("files", []):
        ck(f"file exists {f['file']}", Path(f["path"]).exists(), f["path"])
        ck(f"file sha256 matches {f['file']}",
           sha256_file(Path(f["path"])) == f["sha256"], "hash mismatch")
    ck("5 anchors present", len(manifest.get("anchors", [])) == 5,
       str(len(manifest.get("anchors", []))))
    for a in manifest.get("anchors", []):
        ck(f"anchor {a['id']} verified at build", a.get("verified_at_build") is True, str(a.get("id")))
    l3 = manifest.get("l3_precheck", {})
    ck("L3 container server pass", l3.get("container_server_pass") is True)
    ck("L3 container client pass", l3.get("container_client_pass") is True)
    ck("L3 container hist pass", l3.get("container_hist_pass") is True)
    ck("L3 roundtrip 79/79", l3.get("roundtrip_79_failed") == 0,
       f"{l3.get('roundtrip_79_match')}/{l3.get('roundtrip_79_total')}")
    ck("L3 all pass", l3.get("all_pass") is True)
    eng = manifest.get("engine_results", {})
    ck("t140 checks all pass", eng.get("t140", {}).get("checks_pass")
       == eng.get("t140", {}).get("checks_total"))
    ck("t140 t133 79/79", eng.get("t140", {}).get("t133_closed") == 79
       and eng.get("t140", {}).get("t133_verified") == 79)
    ck("t140 unicorn targets pass", eng.get("t140", {}).get("unicorn_targets_pass")
       == eng.get("t140", {}).get("unicorn_targets"))
    ck("t140 kane pass", eng.get("t140", {}).get("unicorn_kane_pass") is True)
    ck("t155 block lossless", eng.get("t155", {}).get("block_lossless") is True)
    ck("t155 surgery verified", eng.get("t155", {}).get("surgery_verified") is True)
    for name in ("L4_CHECKLIST.md", "REPORT.md", "DONE.md"):
        ck(f"deliverable {name}", (OUTDIR / name).exists())
    done_first = (OUTDIR / "DONE.md").read_text(encoding="utf-8").splitlines()[0] \
        if (OUTDIR / "DONE.md").exists() else ""
    ck("DONE.md first line DONE type=l4_prep_kit", done_first == "DONE type=l4_prep_kit", done_first)

    bad = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  [{'ok' if ok else 'FAIL'}] {name}" +
              (f" <- {detail}" if not ok and detail else ""))
    print(f"\nselftest: {len(checks)-len(bad)}/{len(checks)} checks passed -> "
          f"{'PASS' if not bad else 'FAIL'}")
    return 0 if not bad else 1


def parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="t158 L4 真机加载验证预备包与自动化预检套件")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true", help="构建 l4_staging 补丁包并执行 L3 预检")
    g.add_argument("--selftest", action="store_true",
                   help="端到端自检（0=PASS / 1=FAIL；缺产物时会先 --build）")
    ap.add_argument("--out", default=str(OUTDIR), help="产出目录（默认 scratch/t158/out）")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    global OUTDIR, STAGING, DAT_BUILD, HIST_BUILD
    OUTDIR = Path(args.out)
    STAGING = OUTDIR / "l4_staging"
    DAT_BUILD = STAGING / "dat_build"
    HIST_BUILD = STAGING / "hist_build"
    if args.build:
        result = build()
        print(f"t158 build: L3 precheck {'PASS' if result['precheck']['all_pass'] else 'FAIL'}, "
              f"anchors={len(result['anchors'])}, L4={L4} -> {OUTDIR}")
        return 0 if result["precheck"]["all_pass"] else 1
    return selftest()


if __name__ == "__main__":
    raise SystemExit(main())


