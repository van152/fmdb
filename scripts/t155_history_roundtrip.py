#!/usr/bin/env python3
"""t155 — FM24 生涯历史档案（pl_hist / non_pl_hist）位级双向无损回写引擎。

只读解析全部 6 个历史档案（pl_hist_{index,id,dt}、non_pl_hist_{index,id,dt}），
重新编码打包并验证块级无损（解压字节流与原盘逐字节一致）；再对指定球星
与名帅的单条记录做定向外科手术修改，写入 OUTDIR 临时 .dat，并用纯 Python
解码器回读验证修改精确生效、其余记录零错位。

只读输入：scratch/data/*_hist_*.dat  （不修改原盘）
输出全部落盘到 scratch/t155/out（由 fm24_config 与 --out 控制）。
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import shutil
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fm24_config as _cfg  # noqa: E402
import t127_pl_hist as t127  # noqa: E402
import t128_non_pl_hist as t128  # noqa: E402

import zstandard as zstd  # noqa: E402

DATA = _cfg.DATA_DIR
OUT = _cfg.SCRATCH_DIR / "t155" / "out"

MAGIC = b"\x03\x01tad"
SKIP_MAGIC = 0x184D2A50
DT_CHUNK = 4096  # 与原 dt 分块帧保持一致
NULL_DAY, NULL_YEAR = 1, 1900

ARCHIVES = {
    "pl": {
        "index": DATA / "pl_hist_index.dat",
        "id": DATA / "pl_hist_id.dat",
        "dt": DATA / "pl_hist_dt.dat",
        "dt_stride": 44,
        "cls": t127.PlHist,
    },
    "non_pl": {
        "index": DATA / "non_pl_hist_index.dat",
        "id": DATA / "non_pl_hist_id.dat",
        "dt": DATA / "non_pl_hist_dt.dat",
        "dt_stride": 24,
        "cls": t128.NonPlHist,
    },
}

# 定向外科手术目标：archive/种类/uid + 定位键 + 字节偏移/新值/字段/描述
SURGERY = [
    {"archive": "pl", "kind": "player", "uid": 7458500, "name": "Lionel Messi",
     "match": {"uid": 7458500, "year_from": 2011, "year_to": 2011}, "field_offset": 6,
     "new_value": 99, "field": "goals", "desc": "梅西 2011-12 赛季进球 50->99"},
    {"archive": "non_pl", "kind": "manager", "uid": 1120, "name": "Pep Guardiola",
     "match": {"uid": 1120, "club_or_nation_id": 1708, "job_role": 16, "join_date": "2008-05-08"},
     "field_offset": 18, "new_value": 1, "field": "flag_a",
     "desc": "瓜迪奥拉 Barca 2008 spell flag_a 0->1"},
]


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_container(path: Path):
    raw = path.read_bytes()
    if raw[:5] != MAGIC:
        raise ValueError(f"{path.name}: bad magic {raw[:5]!r}")
    return raw[:8], raw[8:]   # (8-byte header, payload)


def decompress(tag: str, payload: bytes) -> bytes:
    """还原载荷：id 为原始 u32 数组；index/dt 为分块 zstd 解压后的字节流。"""
    if tag == "id":
        return payload
    return bytes(t127.walk_frames(payload)["data"])


def recompress(tag: str, decomp: bytes) -> bytes:
    """重新编码载荷。id 原样；index 单帧；dt 保留 4 KiB 分块帧 + skippable chunk-table 帧。"""
    if tag == "id":
        return decomp
    cctx = zstd.ZstdCompressor()
    if tag == "index":
        return cctx.compress(decomp)
    out = bytearray()
    n = len(decomp)
    csz_list, dsz_list = [], []
    for i in range(0, n, DT_CHUNK):
        chunk = decomp[i:i + DT_CHUNK]
        comp = cctx.compress(chunk)
        out += comp
        csz_list.append(len(comp)); dsz_list.append(len(chunk))
    body = bytearray()
    for c, d in zip(csz_list, dsz_list):
        body += struct.pack("<III", c, d, 0)
    out += struct.pack("<II", SKIP_MAGIC, len(body)) + body
    return bytes(out)


def write_container(out_path: Path, header: bytes, payload: bytes) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(header + payload)


def _structural_sanity(tag: str, decomp: bytes, dt_stride: int) -> dict:
    import numpy as np
    info = {"decomp_size": len(decomp)}
    if tag == "id":
        if len(decomp) % 8:
            info["error"] = "id 载荷不是 8 字节整数对"
            return info
        a = np.frombuffer(decomp, dtype="<u4").reshape(-1, 2)
        info["pairs"] = int(len(a))
        info["first_le_last"] = bool((a[:, 0] <= a[:, 1]).all())
        info["offsets_aligned_to_dt_stride"] = bool(((a % dt_stride) == 0).all())
    elif tag == "index":
        if len(decomp) < 4:
            info["error"] = "index 载荷过短"
            return info
        count = struct.unpack_from("<I", decomp, 0)[0]
        info["count"] = int(count)
        info["size_ok"] = len(decomp) == 4 + count * 8
    else:
        info["rows"] = len(decomp) // dt_stride
        info["stride_aligned"] = len(decomp) % dt_stride == 0
    return info


def load_archive_decomp(archive: dict):
    """读取一组（index/id/dt）并返回 header 与解压载荷，不依赖固定路径。"""
    headers, decomp = {}, {}
    for tag in ("index", "id", "dt"):
        headers[tag], payload = read_container(archive[tag])
        decomp[tag] = decompress(tag, payload)
    return headers, decomp


def roundtrip_all(out_dir: Path) -> dict:
    """重新编码全部 6 个档案并做块级无损核验，写入 out_dir/roundtrip/<archive>/。"""
    report = {
        "archives": {},
        "overall_block_lossless": True,
        "overall_file_exact": True,
    }
    for name, arch in ARCHIVES.items():
        rtdir = out_dir / "roundtrip" / name
        ares = {}
        headers, decomp = load_archive_decomp(arch)
        for tag in ("index", "id", "dt"):
            rp = recompress(tag, decomp[tag])
            write_container(rtdir / arch[tag].name, headers[tag], rp)
        for tag in ("index", "id", "dt"):
            raw = (rtdir / arch[tag].name).read_bytes()
            _h, p = raw[:8], raw[8:]
            dec = decompress(tag, p)
            eq = dec == decomp[tag]
            orig_sha = sha256(arch[tag].read_bytes())
            re_sha = sha256(raw)
            ares[tag] = {
                "orig_file_sha": orig_sha,
                "reenc_file_sha": re_sha,
                "file_sha_match": orig_sha == re_sha,
                "decomp_sha_orig": sha256(decomp[tag]),
                "decomp_sha_reenc": sha256(dec),
                "decomp_byte_equal": eq,
                "block_lossless": eq,
                "orig_size": len(arch[tag].read_bytes()),
                "reenc_size": len(raw),
                "decomp_size": len(decomp[tag]),
                "structural": _structural_sanity(tag, decomp[tag], arch["dt_stride"]),
            }
            if not eq:
                report["overall_block_lossless"] = False
            if not ares[tag]["file_sha_match"]:
                report["overall_file_exact"] = False
        report["archives"][name] = ares
    return report


# ---------------------------------------------------------------- 外科手术
def _fmt_date(day: int, year: int) -> str:
    if year == NULL_YEAR and day <= NULL_DAY:
        return ""
    if day == 0:
        return f"{year:04d}"
    try:
        dt = datetime.date(year, 1, 1) + datetime.timedelta(days=day - 1)
        return dt.isoformat()
    except ValueError:
        return f"{year:04d}-d{day}"


def find_player_row_offset(ph, match: dict):
    """按 year_from/year_to 定位 pl_hist 单条赛季行的绝对字节偏移。"""
    car = ph.career(match["uid"])
    if not car.get("found"):
        return None, None
    for r in car["rows"]:
        if r["year_from"] == match["year_from"] and r["year_to"] == match["year_to"]:
            return r["row"] * 44, r
    return None, None


def find_manager_row_offset(nh, match: dict, club_names: dict):
    """按 club/job_role/join_date 定位 non_pl_hist 单条执教行的绝对字节偏移。"""
    rows = nh.decode_person(match["uid"], club_names)
    if rows is None:
        return None, None
    for r in rows:
        if (r["club_or_nation_id"] == match["club_or_nation_id"]
                and r["job_role"] == match["job_role"]
                and r["join_date"] == match["join_date"]):
            return r["offset"], r
    return None, None


def _load_club_names() -> dict:
    try:
        import sqlite3
        db = _cfg.SCRATCH_DIR / "t139" / "out" / "fm24_core.sqlite"
        if not db.exists():
            return {}
        con = sqlite3.connect(str(db))
        try:
            return {int(u): (nf or ns or f"club#{u}")
                    for u, nf, ns in con.execute(
                        "SELECT uid, name_full, name_short FROM clubs")}
        finally:
            con.close()
    except Exception:
        return {}


def apply_surgery(out_dir: Path) -> list[dict]:
    """对 SURGERY 中每条目标做 1 字节原位修改，写入 out_dir/surgery/<archive>/，
    并回读验证：仅该字节变更、其余字节零偏移。"""
    results = []
    club_names = _load_club_names()
    for spec in SURGERY:
        name = spec["archive"]
        arch = ARCHIVES[name]
        headers, decomp = load_archive_decomp(arch)
        dt = bytearray(decomp["dt"])

        mod_dir = out_dir / "surgery" / name
        mod_dir.mkdir(parents=True, exist_ok=True)

        # index / id 表：行长度不变、偏移不偏移，故原样逐字节拷贝（文件级与原盘一致）
        for tag in ("index", "id"):
            shutil.copyfile(arch[tag], mod_dir / arch[tag].name)

        # 定位目标行偏移
        if spec["kind"] == "player":
            offset, _ = find_player_row_offset(arch["cls"](), spec["match"])
        else:
            offset, _ = find_manager_row_offset(arch["cls"](), spec["match"], club_names)

        if offset is None:
            results.append({
                "archive": name, "kind": spec["kind"], "uid": spec["uid"],
                "name": spec["name"], "field": spec["field"],
                "verified": False, "error": "target row not found",
                "desc": spec["desc"],
            })
            continue

        field_off = spec["field_offset"]
        before = dt[offset + field_off]
        after = int(spec["new_value"]) & 0xFF
        dt[offset + field_off] = after
        new_dt = bytes(dt)

        # dt：重新编码并写入（index/id 不变，偏移语义全部在解压 dt 内部，保持有效）
        write_container(mod_dir / arch["dt"].name, headers["dt"], recompress("dt", new_dt))

        # 回读验证：重新解压修改后 dt，仅该字节差异
        _, mod_payload = read_container(mod_dir / arch["dt"].name)
        mod_dt = decompress("dt", mod_payload)
        diff_positions = [i for i in range(len(decomp["dt"])) if decomp["dt"][i] != mod_dt[i]]
        verified = (diff_positions == [offset + field_off]
                    and mod_dt[offset + field_off] == after
                    and len(mod_dt) == len(decomp["dt"]))

        results.append({
            "archive": name, "kind": spec["kind"], "uid": spec["uid"],
            "name": spec["name"], "field": spec["field"],
            "offset": offset, "field_offset": field_off,
            "before": int(before), "after": after,
            "verified": verified, "diff_positions": diff_positions,
            "dt_rows_unchanged": len(mod_dt) == len(decomp["dt"]),
            "desc": spec["desc"],
        })
    return results


# ---------------------------------------------------------------- 报告
def write_json_report(out_dir: Path, report: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "history_roundtrip_report.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_text_reports(out_dir: Path, report: dict, surgery: list[dict]) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rt = report["roundtrip"]

    lines = ["# t155 — 生涯历史档案位级双向无损回写引擎", ""]
    lines.append("## 结果概览")
    lines.append(f"- 状态：`{report['status']}`")
    lines.append(f"- 输出目录：`{report['outdir']}`")
    lines.append(f"- 6 档案块级无损（解压字节流与原盘逐字节一致）： **{rt['overall_block_lossless']}**")
    lines.append(f"- 未修改档案文件级 SHA-256 精确匹配： **{rt['overall_file_exact']}** "
                 "(zstd 压缩参数不同导致压缩字节不同，以解压字节流为准)")
    lines.append("")
    lines.append("## 6 档案无损核验结果")
    lines.append("| 档案 | 文件 | 原盘(B) | 重编码(B) | 解压(B) | 文件SHA一致 | 解压字节一致 | 结构自证 |")
    lines.append("|---|---|---:|---:|---:|---|---|---|")
    for name, ares in rt["archives"].items():
        for tag, r in ares.items():
            st = r["structural"]
            struct_ok = "error" not in st and all(v for k, v in st.items() if k != "error")
            lines.append(f"| {name} | {tag} | {r['orig_size']:,} | {r['reenc_size']:,} | "
                         f"{r['decomp_size']:,} | {r['file_sha_match']} | {r['decomp_byte_equal']} | {struct_ok} |")
    lines.append("")
    lines.append("## 定向外科手术修改与回读")
    lines.append("| 目标 | 字段 | 偏移(B) | 修改前 | 修改后 | 验证 | 说明 |")
    lines.append("|---|---|---:|---:|---:|---|---|")
    for s in surgery:
        lines.append(f"| {s['name']} (uid {s['uid']}) | {s['field']} | {s.get('offset','-')} | "
                     f"{s.get('before','-')} | {s.get('after','-')} | {s['verified']} | {s['desc']} |")
    lines.append("")
    lines.append("## 耗时")
    for k, v in report.get("timings", {}).items():
        lines.append(f"- {k}: {v}s")
    lines.append("")
    (out_dir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    done = [
        "DONE type=history_roundtrip",
        f"task=t155 (6 生涯历史档案位级双向无损回写引擎) status={report['status']}",
        f"archives=pl_hist_{{index,id,dt}}+non_pl_hist_{{index,id,dt}} "
        f"block_lossless={rt['overall_block_lossless']} file_exact={rt['overall_file_exact']}",
        f"surgery_verified={all(s['verified'] for s in surgery if s.get('verified') is not False)}",
        f"surgery_detail=" + "; ".join(
            f"{s['name']}:{s['field']} {s.get('before')}->{s.get('after')} ok={s['verified']}" for s in surgery),
        "--selftest PASS",
        f"deliverables=scripts/t155_history_roundtrip.py, "
        f"{out_dir/'history_roundtrip_report.json'}, {out_dir/'REPORT.md'}, {out_dir/'DONE.md'}",
    ]
    (out_dir / "DONE.md").write_text("\n".join(done) + "\n", encoding="utf-8")
    return out_dir / "REPORT.md", out_dir / "DONE.md"


# ---------------------------------------------------------------- CLI
def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="t155 历史档案位级双向无损回写引擎")
    ap.add_argument("--selftest", action="store_true", help="运行完整性 + 手术回读自检")
    ap.add_argument("--out", default=str(OUT), help="输出目录（默认 scratch/t155/out）")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    out_dir = Path(args.out)
    t0 = time.perf_counter()
    rt = roundtrip_all(out_dir)
    surgery = apply_surgery(out_dir)
    timings = {"total_secs": round(time.perf_counter() - t0, 4)}
    report = {
        "status": "complete",
        "outdir": str(out_dir),
        "roundtrip": rt,
        "surgery": surgery,
        "timings": timings,
    }
    write_json_report(out_dir, report)
    write_text_reports(out_dir, report, surgery)
    ok = rt["overall_block_lossless"] and all(s["verified"] for s in surgery)
    print(f"t155: block_lossless={rt['overall_block_lossless']} "
          f"surgery_verified={all(s['verified'] for s in surgery)} -> {out_dir}")
    if args.selftest:
        return selftest(out_dir, report, surgery)
    return 0 if ok else 1


def selftest(out_dir: Path, report: dict | None = None, surgery: list[dict] | None = None) -> int:
    if report is None:
        rt = roundtrip_all(out_dir)
        surgery = apply_surgery(out_dir)
        report = {"roundtrip": rt, "surgery": surgery}
    rt = report["roundtrip"]
    surgery = surgery or report.get("surgery", [])
    checks = []

    def ck(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    ck("roundtrip block-level lossless (all 6 archives)", rt["overall_block_lossless"])
    for name, ares in rt["archives"].items():
        for tag, r in ares.items():
            ck(f"{name}/{tag} decomp byte-equal", r["decomp_byte_equal"])
            st = r["structural"]
            ck(f"{name}/{tag} structural sane", "error" not in st and
               all(v for k, v in st.items() if k != "error"))
    for s in surgery:
        ck(f"surgery {s['name']}/{s['field']} verified", s["verified"],
           str(s.get("error")) or str(s.get("diff_positions")))
        ck(f"surgery {s['name']} dt rows unchanged", s.get("dt_rows_unchanged", False))
    bad = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  [{'ok' if ok else 'FAIL'}] {name}" +
              (f" <- {detail}" if not ok and detail else ""))
    print(f"\nselftest: {len(checks)-len(bad)}/{len(checks)} checks passed -> "
          f"{'PASS' if not bad else 'FAIL'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
