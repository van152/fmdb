#!/usr/bin/env python3
"""t38_multiframe — 成员感知 payload 加载器(以目录条目为权威边界)。

背景
----
`scripts/fm24_dump.py:load_payload` 直接对 `entry["offset"]` 取字节并向前扫 64B
找首帧 MAGIC。该函数**忽略了 FMF 的 `data_base`**(实测 `server_db.dat` /
`client_db.dat` / `lang_update_db.dat` 均为 34),因此起点整体前移 34 字节:

* 若前一个成员 `packed_size < data_base`(实测:全部是 25B 的 `tad.` 空 stub),
  首帧落在**前一个成员**上 → 取到别人的 payload(12B 空 stub),真正表帧被跳过。
  这是 E66(`server_db/table_34.dat` 返回 12B 而非 313082B)的唯一成因。
* 若前一个成员较大,窗口内的首帧恰好是正确帧,WIN 不报错(掩盖了缺陷)。

本模块不修 `fm24_dump.py`,提供独立加载器:`load_payload_mf`。

选帧判据(权威字段来自 `codec["list_tables"]` / `codec["_resolve_table"]`)
------------------------------------------------------------------
* `offset`      —— 相对 `data_base` 的成员起点 ⇒ 成员绝对起点 = `data_base + offset`。
* `packed_size` —— 成员压缩区字节数,**帧枚举的硬上界**,不得越界进入后续成员。
* `size`        —— 真实解压 payload 字节数,**唯一选帧判据**。
* `sha256`      —— 实测为**压缩区** SHA-256(≠ payload SHA),用作成员边界校验。
* `payload_version` / `record_count_header` —— 多帧同长时的消歧辅助(取自 payload
  +6..8 / +8..12)。

无匹配帧一律 `raise`(诚实失败),绝不回落首帧凑数。

用法
----
  py -V:3.12 -I -B scripts/t38_multiframe.py --selftest
  py -V:3.12 -I -B scripts/t38_multiframe.py --dump server 34 --out /tmp/p.bin
  py -V:3.12 -I -B scripts/t38_multiframe.py --scan
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import runpy
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
UPSTREAM = pathlib.Path(r"D:\tmp2b\fm24")
ZSTD_DIR = UPSTREAM / "tools/python"
READER_VERIFY = ROOT / "scratch/t01/inbox/t01k/verify.py"
MAGIC = bytes.fromhex("28b52ffd")
DAT_MAGIC = b"\x03\x01tad."
MAX_PAYLOAD = 256 * 1024 * 1024

# 控制台编码:任务要求打印可读,Windows 默认 cp936 会把中文打成乱码
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DB_DIR = pathlib.Path(
    os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data")
)


class FrameError(RuntimeError):
    """成员内无帧满足选帧判据(诚实失败)。"""


def _zstd():
    if str(ZSTD_DIR) not in sys.path:
        sys.path.insert(0, str(ZSTD_DIR))
    import zstandard as zstd

    return zstd


def _codec():
    """上游只读解码器(与 fm24_dump._reader 同源,只读不改)。"""
    k = runpy.run_path(str(READER_VERIFY))
    return runpy.run_path(str(k["OLD_READER_PATH"]))


# ---------------------------------------------------------------- 成员定位


def archive_info(codec, archive: str, cache: dict | None = None) -> dict:
    """读归档一次,返回 data_base / 原始字节 / 条目表。"""
    key = archive
    if cache is not None and key in cache:
        return cache[key]
    fn = f"{archive}_db.dat"
    p = DB_DIR / fn
    if not p.is_file():
        raise FileNotFoundError(p)
    db = p.read_bytes()
    layout = codec["_archive_layout"](db)
    info = {
        "archive": archive,
        "path": str(p),
        "data": db,
        "data_base": int(layout["data_base"]),
        "toc_offset": int(layout["toc_offset"]),
        "entries": layout["entries"],
        "tables": codec["list_tables"](p, fn),
    }
    if cache is not None:
        cache[key] = info
    return info


def member_bounds(entry: dict, data_base: int) -> tuple[int, int]:
    """成员在文件中的 [start, end)。start 必须加 data_base —— load_payload 漏了这一步。"""
    start = data_base + int(entry["offset"])
    end = start + int(entry["packed_size"])
    return start, end


def decode_frames(region: bytes) -> tuple[list[dict], int, str | None]:
    """在给定字节区间内逐帧解压(unused_data 推进),**绝不读取 region 之外**。

    返回 (frames, leftover_len, error)。被 packed_size 截断的帧不丢弃已解字节,
    而是标记 eof=False 并让调用方决定是否扩边界重试 —— 避免“边界错→静默失败”。
    """
    zstd = _zstd()
    dctx = zstd.ZstdDecompressor()
    frames: list[dict] = []
    data = region
    pos = 0
    err: str | None = None
    while data[:4] == MAGIC:
        obj = dctx.decompressobj()
        try:
            chunk = obj.decompress(data)
        except Exception as exc:
            err = f"zstd decode failed at member+{pos}: {exc}"
            break
        frames.append(
            {
                "member_offset": pos,
                "length": len(chunk),
                "sha256": hashlib.sha256(chunk).hexdigest(),
                "eof": bool(obj.eof),
                "data": chunk,
            }
        )
        consumed = len(data) - len(obj.unused_data)
        if not obj.eof:
            err = f"truncated zstd frame at member+{pos} (region boundary cuts it)"
            break
        if consumed <= 0:
            err = f"zstd made no progress at member+{pos}"
            break
        pos += consumed
        data = obj.unused_data
        if not data:
            break
    return frames, len(data), err


def iter_frames(region: bytes) -> tuple[list[dict], int]:
    """严格模式:区间内必须全部是完整帧,否则 raise(供边界自证用)。"""
    frames, leftover, err = decode_frames(region)
    if err:
        raise FrameError(err)
    return frames, leftover


def next_member_start(info: dict, entry: dict) -> int | None:
    """同归档内下一个成员的起点(按 offset 升序)。末成员返回 None。"""
    base = info["data_base"]
    ents = sorted(info["entries"], key=lambda e: e["offset"])
    for i, e in enumerate(ents):
        if e["path"] == entry["path"]:
            nxt = ents[i + 1] if i + 1 < len(ents) else None
            return None if nxt is None else base + int(nxt["offset"])
    return None


def decode_frames_unbounded(db: bytes, start: int) -> list[dict]:
    """从 start 向文件末尾逐帧解压,**不设上界**(E77 指定的选帧方式)。

    会越过成员边界、把后续成员的帧也解出来。后果:若两成员 payload 同长且同 SHA
    则无法区分。本仓实测无此情形,但该方法对边界错误无自保护——仅供对照/取证,
    不是默认路径。默认仍是 `inspect_entry` 的 packed_size 有界选帧。
    """
    zstd = _zstd()
    dctx = zstd.ZstdDecompressor()
    frames: list[dict] = []
    data = db[start:]
    pos = 0
    while data[:4] == MAGIC:
        obj = dctx.decompressobj()
        chunk = obj.decompress(data)
        frames.append(
            {
                "member_offset": pos,
                "length": len(chunk),
                "sha256": hashlib.sha256(chunk).hexdigest(),
                "eof": bool(obj.eof),
                "data": chunk,
            }
        )
        if not obj.eof:
            break
        consumed = len(data) - len(obj.unused_data)
        if consumed <= 0:
            break
        pos += consumed
        data = obj.unused_data
        if not data:
            break
    return frames


def pick_frame_unbounded(codec, archive: str, tid: int, cache: dict | None = None) -> bytes:
    """E77 指定的「无界 size+SHA 匹配」选帧。

    在 `data_base+offset` 起一直走到文件末尾,取 `len == entry["size"]` 且
    SHA 匹配(`entry.sha256` 是 packed SHA,故 SHA 校验用**首个 size 命中**的
    唯一性来保证)的帧。仅作对照路径,默认请用 `load_payload_mf`。
    """
    info = archive_info(codec, archive, cache)
    base = info["data_base"]
    entry = codec["_resolve_table"](tid, info["tables"], f"{archive}_db.dat")
    start = base + int(entry["offset"])
    frames = decode_frames_unbounded(info["data"], start)
    hits = [f for f in frames if f["length"] == int(entry["size"])]
    if len(hits) != 1:
        raise FrameError(
            f"{archive}#{tid}: unbounded scan found {len(hits)} frames with length "
            f"{entry['size']} (scanned {len(frames)} frames across member boundaries)"
        )
    return hits[0]["data"]


def boundary_spanning_proof(codec, archive: str, tid: int, cache: dict | None = None) -> dict:
    """证明「成员边界 == 帧边界」:有界选帧与无界 size+SHA 选帧一致。

    若 `packed_size` 真的只覆盖真实帧而不覆盖整成员(即E77 的假设),
    则无界扫描会看到比有界更多的帧——本函数把两边帧数与首个 size 命中位置全部记录。
    """
    info = archive_info(codec, archive, cache)
    base = info["data_base"]
    db = info["data"]
    entry = codec["_resolve_table"](tid, info["tables"], f"{archive}_db.dat")
    start = base + int(entry["offset"])
    size = int(entry["size"])
    uframes = decode_frames_unbounded(db, start)
    bframes, _, _ = decode_frames(db[start:start + int(entry["packed_size"])])
    uhits = [i for i, f in enumerate(uframes) if f["length"] == size]
    bhits = [i for i, f in enumerate(bframes) if f["length"] == size]
    return {
        "archive": archive,
        "table_id": tid,
        "bounded_frame_count": len(bframes),
        "unbounded_frame_count": len(uframes),
        "bounded_size_hits": len(bhits),
        "unbounded_size_hits": len(uhits),
        "unbounded_extra_frames_from_later_members": len(uframes) - len(bframes),
        "first_size_hit_is_frame_0": (bhits[:1] == [0] and uhits[:1] == [0]),
        "same_payload": (
            len(bhits) == 1 and len(uhits) == 1
            and bframes[bhits[0]]["sha256"] == uframes[uhits[0]]["sha256"]
        ),
    }


def _header_fields(raw: bytes) -> tuple[int | None, int | None]:
    """payload 头里的 version(+6..8) 与 record_count(+8..12),非 tad. 则 None。"""
    if len(raw) < 12 or raw[:6] != DAT_MAGIC:
        return None, None
    return (
        struct.unpack_from("<H", raw, 6)[0],
        struct.unpack_from("<I", raw, 8)[0],
    )


def entry_table_id(entry: dict) -> int | None:
    """从路径推导 table_NNN（原始 layout 条目没有 table_id 字段）。"""
    if entry.get("table_id") is not None:
        return int(entry["table_id"])
    name = pathlib.PurePosixPath(entry["path"]).name
    if name.startswith("table_") and name.endswith(".dat"):
        mid = name[len("table_"):-len(".dat")]
        if mid.isdigit():
            return int(mid)
    return None


def inspect_entry(codec_or_info, entry: dict, info: dict | None = None) -> dict:
    """对单个条目做成员定位 + 帧枚举 + 选帧,返回完整证据字典。

    边界策略(两阶段,均不越过下一成员):
      P1 `packed_size` 区间 —— 稳当情形(实测所有成员均如此:单帧、len==size)。
      P2 仅当 P1 被截断或选不到 size 帧时,扩到**下一成员起点**重试。
         这样即使 `packed_size` 只覆盖真实帧而非整个成员区(若存在这种成员),
         也能选到帧,且仍然不跨成员。P2 触发与否全部落盘证据。
    """
    if info is None:
        raise ValueError("info required")
    base = info["data_base"]
    db = info["data"]
    start, end = member_bounds(entry, base)
    if start < 0 or end > len(db):
        raise FrameError(f"{entry['path']}: member [{start},{end}) outside archive")

    # entry.sha256 只有 list_tables 返回的条目有；raw layout 条目需回查
    want_sha = entry.get("sha256")
    if want_sha is None:
        for t in info.get("tables", ()):
            if t["path"] == entry["path"]:
                want_sha = t.get("sha256")
                break

    diag: dict = {
        "path": entry["path"],
        "table_id": entry.get("table_id"),
        "entry_offset": int(entry["offset"]),
        "data_base": base,
        "member_start": start,
        "packed_size": int(entry["packed_size"]),
        "declared_size": int(entry["size"]),
        "entry_sha256_is_packed_sha": hashlib.sha256(db[start:end]).hexdigest() == want_sha,
        "legacy_offset_delta": int(entry["offset"]) - start,  # 负数=旧法前移
    }

    def _attempt(bound: int, label: str):
        frames, leftover, err = decode_frames(db[start:bound])
        hits = [f for f in frames if f["length"] == int(entry["size"])]
        if len(hits) > 1:
            want_ver = entry.get("payload_version")
            want_rc = entry.get("record_count_header")
            narrowed = []
            for f in hits:
                ver, rc = _header_fields(f["data"])
                f["payload_version"], f["record_count_header"] = ver, rc
                if want_ver is not None and ver is not None and ver != want_ver:
                    continue
                if want_rc is not None and rc is not None and rc != want_rc:
                    continue
                narrowed.append(f)
            hits = narrowed
        return {
            "phase": label,
            "bound": bound,
            "frames": frames,
            "leftover": leftover,
            "error": err,
            "hits": hits,
        }

    p1 = _attempt(end, "packed_size")
    chosen_phase = p1
    diag["phase1"] = {
        "bound": end,
        "frame_count": len(p1["frames"]),
        "frame_lengths": [f["length"] for f in p1["frames"]],
        "frame_eof": [f["eof"] for f in p1["frames"]],
        "leftover": p1["leftover"],
        "error": p1["error"],
        "size_hits": len(p1["hits"]),
    }
    diag["escalated"] = False

    if not (p1["error"] is None and len(p1["hits"]) == 1 and p1["leftover"] == 0):
        nxt = next_member_start(info, entry)
        if nxt is not None and nxt > end:
            p2 = _attempt(nxt, "next_member_start")
            diag["phase2"] = {
                "bound": nxt,
                "frame_count": len(p2["frames"]),
                "frame_lengths": [f["length"] for f in p2["frames"]],
                "frame_eof": [f["eof"] for f in p2["frames"]],
                "leftover": p2["leftover"],
                "error": p2["error"],
                "size_hits": len(p2["hits"]),
            }
            diag["escalated"] = True
            if p2["error"] is None and len(p2["hits"]) == 1:
                chosen_phase = p2

    frames = chosen_phase["frames"]
    hits = chosen_phase["hits"]
    diag["surface"] = chosen_phase["phase"]
    diag["frame_count"] = len(frames)
    diag["frame_lengths"] = [f["length"] for f in frames]
    diag["frame_shas"] = [f["sha256"] for f in frames]
    diag["leftover_bytes"] = chosen_phase["leftover"]
    diag["multi_frame_member"] = len(frames) != 1
    diag["size_matches"] = len(hits)
    diag["disambiguation"] = "payload_version+record_count_header" if len(hits) > 1 or (
        len([f for f in frames if f["length"] == int(entry["size"])]) > 1) else None

    if not frames:
        raise FrameError(
            f"{entry['path']}: no zstd frame in member [{start},{end}) ({chosen_phase['phase']})"
            + (f": {chosen_phase['error']}" if chosen_phase["error"] else "")
        )
    if len(hits) != 1:
        raise FrameError(
            f"{entry['path']}: no unique frame with decompressed length == size "
            f"({entry['size']}); phase={chosen_phase['phase']} frames={diag['frame_lengths']} "
            f"kept={len(hits)}"
        )

    chosen = hits[0]
    diag["selected_member_offset"] = chosen["member_offset"]
    diag["selected_length"] = chosen["length"]
    diag["selected_sha256"] = chosen["sha256"]
    diag["selected_is_first_frame"] = chosen["member_offset"] == 0
    ver, rc = _header_fields(chosen["data"])
    diag["selected_payload_version"] = ver
    diag["selected_record_count_header"] = rc
    diag["payload_max"] = len(chosen["data"]) <= MAX_PAYLOAD
    return {"data": chosen["data"], "diag": diag}


def load_payload_mf(codec, archive: str, tid: int, cache: dict | None = None) -> bytes:
    """多帧/成员感知加载:返回解压长度 == entry["size"] 的那一帧。

    与 fm24_dump.load_payload 的差异:使用 data_base + offset 定位成员、用
    packed_size 严格界定帧枚举区间、以 size 选帧。无匹配帧 raise FrameError。
    """
    info = archive_info(codec, archive, cache)
    fn = f"{archive}_db.dat"
    entry = codec["_resolve_table"](tid, info["tables"], fn)
    return inspect_entry(codec, entry, info)["data"]


def e77_repro(codec, archive: str = "server", tid: int = 34, cache: dict | None = None) -> dict:
    """把 E77 报告的“截断真实帧”现象完整复现并归因。

    E77 的观测(`BOUNDED frame2=287410 eof=False` / `UNBOUNDED 313082 eof=True`)
    在这里必然重现 —— 但原因是坐标系差 34B,不是 packed_size 语义:
      * E77 起点 = `entry.offset + 9`  —— **漏加 data_base** 的绝对坐标,
        落在前一个 12B stub 成员里(它自己首帧就在此);
      * 终点 = `entry.offset + packed_size` —— 也是绝对坐标。
    两者合并后区域 = 12B stub + 25B stub-frame + 真实帧的前 89073 字节 -> 自然被截断。
    正确坐标 `data_base + offset` 下同一成员是**单帧**且长度恰为 size。
    本函数把三个坐标系都算出来对比,作为可执行证据。
    """
    info = archive_info(codec, archive, cache)
    base = info["data_base"]
    db = info["data"]
    entry = codec["_resolve_table"](tid, info["tables"], f"{archive}_db.dat")
    off = int(entry["offset"])
    packed = int(entry["packed_size"])
    size = int(entry["size"])
    correct_start = base + off

    def summarize(start: int, end: int) -> dict:
        frames, left, err = decode_frames(db[start:end])
        return {
            "start": start,
            "end": end,
            "region_bytes": end - start,
            "frames": [{"member_offset": f["member_offset"], "length": f["length"],
                        "eof": f["eof"], "sha256": f["sha256"][:16]} for f in frames],
            "leftover": left,
            "error": err,
            "size_hits": sum(1 for f in frames if f["length"] == size),
        }

    # E77 坐标:起点 entry.offset+9(首 MAGIC 在 entry.offset 起 9B 处)
    e77_hit = next((d for d in range(64) if db[off + d: off + d + 4] == MAGIC), None)
    out = {
        "archive": archive,
        "table_id": tid,
        "data_base": base,
        "entry_offset": off,
        "packed_size": packed,
        "declared_size": size,
        "correct_member_start": correct_start,
        "e77_coordinate_delta_from_correct": (off + (e77_hit or 0)) - correct_start,
        "e77_bounded": summarize(off + (e77_hit or 0), off + packed),
        "e77_unbounded": summarize(off + (e77_hit or 0), len(db)),
        "correct_bounded": summarize(correct_start, correct_start + packed),
    }
    cb = out["correct_bounded"]
    out["conclusion"] = {
        "e77_symptom_reproduced": any(not f["eof"] for f in out["e77_bounded"]["frames"]),
        "packed_size_is_whole_member": cb["error"] is None
        and cb["leftover"] == 0
        and len(cb["frames"]) == 1
        and cb["frames"][0]["length"] == size,
        "explanation": (
            "E77 起点漏加 data_base(-%d B),落在前一 12B stub 成员内;" % abs(
                out["e77_coordinate_delta_from_correct"])
            + "正确坐标下该成员为单帧且长度==size,packed_size 覆盖整个成员区。"
        ),
    }
    return out


# ---------------------------------------------------------------- 回归基线

T33_PROFILES = ROOT / "scratch/t33/out/profiles"
T29_INVENTORY = ROOT / "scratch/t29/out/subtable_inventory.json"

# 硬锚点(任务书给定,来自 t29 / t35 已落盘证据)
ANCHORS = [
    ("server", 34, 313082, "a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812"),
    ("client", 3, 6932082, "db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f"),
    ("server", 73, 45, None),
    ("server", 66, 18094, None),
    ("server", 43, 24632, None),
]


def _legacy_load_payload():
    """惰性取 fm24_dump.load_payload(只读引用,用于差异回归)。"""
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    import fm24_dump

    return fm24_dump.load_payload


def regression_targets() -> list[tuple[str, int, int, str]]:
    """t33 七表 + t29 十三表 → [(archive, tid, payload_size, payload_sha)]。"""
    out: list[tuple[str, int, int, str]] = []
    if T33_PROFILES.is_dir():
        for f in sorted(T33_PROFILES.glob("*.profile.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            p = d["payload"]
            out.append((p["archive"], int(d["table_type"]), int(p["payload_size"]), p["payload_sha256"]))
    if T29_INVENTORY.is_file():
        inv = json.loads(T29_INVENTORY.read_text(encoding="utf-8"))
        for t in inv["tables"]:
            key = (t["archive"], int(t["table_type"]))
            if any((o[0], o[1]) == key for o in out):
                continue
            out.append((t["archive"], int(t["table_type"]), int(t["payload_size"]), t["payload_sha256"]))
    return out


# ---------------------------------------------------------------- selftest


def run_selftest(verbose: bool = False) -> int:
    if sys.version_info[:2] != (3, 12):
        print("FAIL: 需要 py -V:3.12 -I -B", file=sys.stderr)
        return 2
    if not DB_DIR.is_dir():
        print(f"FAIL: DB_DIR 不存在 {DB_DIR}", file=sys.stderr)
        return 2

    codec = _codec()
    cache: dict = {}
    fails: list[str] = []
    lines: list[str] = []

    def ck(name: str, ok: bool, detail: str = "") -> None:
        lines.append(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        if not ok:
            fails.append(f"{name}: {detail}")

    # --- 1 硬锚点
    for arch, tid, size, sha in ANCHORS:
        try:
            raw = load_payload_mf(codec, arch, tid, cache)
        except Exception as exc:
            ck(f"anchor {arch}#{tid}", False, f"raise {exc}")
            continue
        got_sha = hashlib.sha256(raw).hexdigest()
        ok = len(raw) == size and (sha is None or got_sha == sha)
        ck(f"anchor {arch}#{tid}", ok, f"len={len(raw)}/{size} sha={got_sha[:16]}" + ("" if sha is None else f"/{sha[:16]}"))

    # --- 2 选帧证据:size 必须是唯一命中
    for arch, tid, size, _ in ANCHORS:
        info = archive_info(codec, arch, cache)
        entry = codec["_resolve_table"](tid, info["tables"], f"{arch}_db.dat")
        try:
            r = inspect_entry(codec, entry, info)
        except Exception as exc:
            ck(f"select {arch}#{tid}", False, f"raise {exc}")
            continue
        d = r["diag"]
        ck(
            f"select {arch}#{tid}",
            d["size_matches"] == 1 and d["selected_is_first_frame"] and d["leftover_bytes"] == 0,
            f"frames={d['frame_count']} lens={d['frame_lengths']} size_hits={d['size_matches']} "
            f"first_frame={d['selected_is_first_frame']} member+{d['selected_member_offset']}",
        )
        # 成员边界自证:packed 区 SHA == entry["sha256"]
        ck(f"member-boundary {arch}#{tid}", d["entry_sha256_is_packed_sha"], "sha256(packed region) == entry.sha256")

    # --- 3 单帧回归:mf 必须命中 size+SHA;与 legacy 的差异只允许出现在
    #        可预测的“旧法漏 data_base”条目上(即 E66 家族),其它一律算失败。
    legacy = _legacy_load_payload()
    reg = regression_targets()
    same = 0
    diff_rows = []
    bad = []
    for arch, tid, size, sha in reg:
        try:
            mf = load_payload_mf(codec, arch, tid, cache)
        except Exception as exc:
            bad.append(f"{arch}#{tid} mf raise {exc}")
            continue
        if len(mf) != size or hashlib.sha256(mf).hexdigest() != sha:
            bad.append(f"{arch}#{tid} mf {len(mf)}/{size} sha mismatch")
            continue
        try:
            old = legacy(codec, arch, tid)
        except Exception as exc:
            diff_rows.append((arch, tid, "legacy-raise", str(exc)[:40]))
            continue
        if old == mf:
            same += 1
        else:
            diff_rows.append((arch, tid, f"legacy={len(old)}B", f"mf={len(mf)}B"))
    # 旧法错帧集合(由 packed_size < data_base 预测),回归差异必须落在其中
    predicted_bad = set()
    for arch in ("server", "client", "lang_update"):
        info = archive_info(codec, arch, cache)
        base = info["data_base"]
        ents = sorted(info["entries"], key=lambda e: e["offset"])
        for i, e in enumerate(ents):
            prev = ents[i - 1] if i else None
            tid_e = entry_table_id(e)
            if prev is not None and int(prev["packed_size"]) < base and tid_e is not None:
                predicted_bad.add((arch, tid_e))
    explained = [(a, t) for a, t, *_ in diff_rows if (a, t) in predicted_bad]
    unexplained = [(a, t) for a, t, *_ in diff_rows if (a, t) not in predicted_bad]
    ck("single-frame regression", not bad and not unexplained,
       f"targets={len(reg)} identical_to_legacy={same} divergent={len(diff_rows)} "
       f"explained_by_legacy_bug={len(explained)} unexplained={len(unexplained)}")
    for row in diff_rows:
        tag = "EXPECTED(E66-family)" if (row[0], row[1]) in predicted_bad else "UNEXPLAINED"
        lines.append(f"       DIFF[{tag}] {row[0]}#{row[1]}: {row[2]} vs {row[3]}")

    # --- 4 全库普查:每个条目都必须单帧且长度吻合(负结果如实记录)
    total = nonconf = 0
    multi_frames = 0
    nonconf_rows = []
    escalated_rows = []
    for arch in ("server", "client", "lang_update"):
        try:
            info = archive_info(codec, arch, cache)
        except Exception:
            continue
        for entry in info["entries"]:
            total += 1
            try:
                r = inspect_entry(codec, entry, info)
            except Exception as exc:
                nonconf += 1
                nonconf_rows.append((arch, entry["path"], "raise", str(exc)[:60]))
                continue
            d = r["diag"]
            if d["escalated"]:
                escalated_rows.append((arch, entry["path"], d.get("phase2", {})))
            if d["multi_frame_member"]:
                multi_frames += 1
            if len(r["data"]) != int(entry["size"]) or d["leftover_bytes"] != 0:
                nonconf += 1
                nonconf_rows.append(
                    (arch, entry["path"], f"frames={d['frame_lengths']}",
                     f"size={entry['size']} left={d['leftover_bytes']}")
                )
    ck("archive census single-frame", nonconf == 0 and multi_frames == 0,
       f"entries={total} nonconforming={nonconf} multi_frame_members={multi_frames} "
       f"escalated_to_next_member={len(escalated_rows)}")
    for row in nonconf_rows[:10]:
        lines.append(f"       NONCONF {row[0]} {row[1]}: {row[2]} {row[3]}")

    # --- 5 E77 复现与归因(可执行证据)
    try:
        rep = e77_repro(codec, "server", 34, cache)
        c = rep["conclusion"]
        ck("E77 symptom reproduced", c["e77_symptom_reproduced"],
           f"e77_bounded frames={[(f['length'], f['eof']) for f in rep['e77_bounded']['frames']]}")
        ck("E77 root cause = coordinate", c["packed_size_is_whole_member"],
           f"delta={rep['e77_coordinate_delta_from_correct']}B; correct_bounded="
           f"{[(f['length'], f['eof']) for f in rep['correct_bounded']['frames']]}")
        ck("E77 unbounded 2nd frame matches size",
           any(f["length"] == 313082 and f["eof"] for f in rep["e77_unbounded"]["frames"]),
           f"unbounded lens={[f['length'] for f in rep['e77_unbounded']['frames']][:3]}")
    except Exception as exc:
        ck("E77 repro", False, f"raise {exc}")

    # --- 6 负结果:size 无命中必须 raise,不能静默返回首帧
    info = archive_info(codec, "server", cache)
    entry = dict(next(e for e in info["entries"] if e["path"].endswith("table_34.dat")))
    entry["size"] = int(entry["size"]) + 1
    try:
        inspect_entry(codec, entry, info)
    except FrameError:
        ck("negative no-match raises", True, "size+1 -> FrameError (no fallback to first frame)")
    except Exception as exc:
        ck("negative no-match raises", False, f"wrong exception {type(exc).__name__}: {exc}")
    else:
        ck("negative no-match raises", False, "returned a frame for an impossible size")

    # --- 7 负结果:packed_size 人为截断 -> 首帧不闭合,必须 escalate 且不得返回错帧
    entry2 = dict(next(e for e in info["entries"] if e["path"].endswith("table_34.dat")))
    entry2["packed_size"] = 100
    r2 = inspect_entry(codec, entry2, info)
    ck("truncated packed_size escalates",
       r2["diag"]["escalated"] and r2["diag"]["surface"] == "next_member_start"
       and len(r2["data"]) == int(entry2["size"]),
       f"phase1_error={r2['diag']['phase1']['error']!r} -> surface={r2['diag']['surface']} "
       f"len={len(r2['data'])}")

    # --- 8 负结果:截断且无下一成员(末成员)必须 raise
    info_lu = archive_info(codec, "lang_update", cache)
    last = sorted(info_lu["entries"], key=lambda e: e["offset"])[-1]
    entry3 = dict(last)
    entry3["packed_size"] = 20
    try:
        inspect_entry(codec, entry3, info_lu)
    except FrameError:
        ck("truncated last member raises", True, "no next member to escalate to -> FrameError")
    except Exception as exc:
        ck("truncated last member raises", False, f"wrong exception {type(exc).__name__}: {exc}")
    else:
        ck("truncated last member raises", False, "accepted a truncated frame")

    # --- 9 legacy 漏 data_base 的判定式(100% 可预测)
    bad_prev = 0
    pred_ok = True
    for arch in ("server", "client", "lang_update"):
        info = archive_info(codec, arch, cache)
        base = info["data_base"]
        ents = sorted(info["entries"], key=lambda e: e["offset"])
        for i, e in enumerate(ents):
            prev = ents[i - 1] if i else None
            predicted = prev is not None and int(prev["packed_size"]) < base
            off = int(e["offset"])
            hit = next((d for d in range(64) if info["data"][off + d: off + d + 4] == MAGIC), None)
            observed = hit != base
            if predicted:
                bad_prev += 1
            if predicted != observed:
                pred_ok = False
    ck("legacy-bug predicate", pred_ok,
       f"entries whose predecessor packed_size < data_base are exactly the ones legacy mis-reads; "
       f"count={bad_prev} predicted==observed={pred_ok}")

    # --- 10 无界 size+SHA 选帧对照(E77 指定方法):记录它何时会选错
    #     无界方法会越过成员边界;当后续成员的 payload 与目标同长时,size-only
    #     选帧不再唯一,且 entry.sha256 是 packed SHA **无法消歧**。这是 E77
    #     方案的真实缺陷,必须落盘而不是假装等价。
    collisions = []      # bounded 路径失败的条目(应永远为空)
    bounded_bad = []     # 无界 size-only 不唯一的条目
    verified = 0
    extra_total = 0
    for arch in ("server", "client", "lang_update"):
        info = archive_info(codec, arch, cache)
        for entry in info["entries"]:
            tid = entry_table_id(entry)
            if tid is None:
                continue
            verified += 1
            pr = boundary_spanning_proof(codec, arch, tid, cache)
            extra_total += pr["unbounded_extra_frames_from_later_members"]
            if not (pr["bounded_frame_count"] == 1 and pr["bounded_size_hits"] == 1
                    and pr["first_size_hit_is_frame_0"]):
                bounded_bad.append((arch, tid, pr))
            if pr["unbounded_size_hits"] > 1:
                collisions.append(
                    {
                        "archive": arch,
                        "table_id": tid,
                        "bounded_frames": pr["bounded_frame_count"],
                        "unbounded_frames": pr["unbounded_frame_count"],
                        "unbounded_size_hits": pr["unbounded_size_hits"],
                        "same_payload_sha": pr["same_payload"],
                    }
                )
    ck("bounded selection unique everywhere", not bounded_bad,
       f"tables={verified} bounded_path_failures={len(bounded_bad)}")
    ck("unbounded method collisions documented", not bounded_bad,
       f"unbounded_size_ambiguous_tables={len(collisions)} "
       f"[{', '.join(c['archive'] + '#' + str(c['table_id']) for c in collisions)}] "
       f"extra_frames_beyond_member={extra_total}")
    for c in collisions:
        lines.append(
            f"       E77-AMBIGUOUS {c['archive']}#{c['table_id']}: bounded={c['bounded_frames']} "
            f"unbounded={c['unbounded_frames']} size_hits={c['unbounded_size_hits']} "
            f"same_payload={c['same_payload_sha']}")

    # --- 11 「28 帧 / 3 帧」的构成:无界扫描数的是后续成员,不是同成员多帧
    proof34 = boundary_spanning_proof(codec, "server", 34, cache)
    proof3 = boundary_spanning_proof(codec, "client", 3, cache)
    ck("client3 28 frames are later members",
       proof3["bounded_frame_count"] == 1 and proof3["unbounded_frame_count"] == 28
       and proof3["unbounded_size_hits"] == 1,
       f"bounded={proof3['bounded_frame_count']} unbounded={proof3['unbounded_frame_count']} "
       f"size_hits={proof3['unbounded_size_hits']} extra={proof3['unbounded_extra_frames_from_later_members']}")
    ck("server34 has no stub first frame",
       proof34["bounded_frame_count"] == 1 and proof34["first_size_hit_is_frame_0"],
       f"bounded={proof34['bounded_frame_count']} unbounded={proof34['unbounded_frame_count']} "
       f"size_hits={proof34['unbounded_size_hits']}")

    print("\n".join(lines) if verbose or len(lines) <= 400 else "\n".join(lines[:400]))
    print(f"--- t38 multiframe selftest: {len(lines) - len(fails)} PASS / {len(fails)} FAIL ---")
    return 0 if not fails else 1


# ---------------------------------------------------------------- CLI


def cmd_scan() -> int:
    codec = _codec()
    cache: dict = {}
    rows = []
    for arch in ("server", "client", "lang_update"):
        try:
            info = archive_info(codec, arch, cache)
        except FileNotFoundError:
            continue
        base = info["data_base"]
        for entry in info["entries"]:
            start, end = member_bounds(entry, base)
            try:
                frames, left = iter_frames(info["data"][start:end])
            except Exception as exc:
                rows.append({"archive": arch, "path": entry["path"], "error": str(exc)})
                continue
            rows.append(
                {
                    "archive": arch,
                    "path": entry["path"],
                    "table_id": entry.get("table_id"),
                    "data_base": base,
                    "entry_offset": int(entry["offset"]),
                    "member_start": start,
                    "packed_size": int(entry["packed_size"]),
                    "declared_size": int(entry["size"]),
                    "frame_count": len(frames),
                    "frame_lengths": [f["length"] for f in frames],
                    "leftover": left,
                }
            )
    print(json.dumps({"entries": rows}, ensure_ascii=False, indent=1)[:200000])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="多帧/成员感知 FM24 payload 加载器(以目录条目 packed_size/size 为权威边界)"
    )
    ap.add_argument("--selftest", action="store_true", help="跑全部自检(锚点/选帧/回归/负结果)")
    ap.add_argument("--dump", nargs=2, metavar=("ARCHIVE", "TID"), help="导出该表 payload 并打印元数据")
    ap.add_argument("--out", help="与 --dump 合用,把 payload 写到该文件")
    ap.add_argument("--scan", action="store_true", help="普查所有归档条目的帧结构(JSON)")
    ap.add_argument("--verbose", action="store_true", help="selftest 打印全部行")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest(verbose=args.verbose)
    if args.scan:
        return cmd_scan()
    if args.dump:
        arch, tid_s = args.dump
        if arch not in ("server", "client", "lang_update"):
            ap.error("archive 须为 server / client / lang_update")
        try:
            tid = int(tid_s)
        except ValueError:
            ap.error("TID 必须是整数")
        try:
            codec = _codec()
            info = archive_info(codec, arch)
            entry = codec["_resolve_table"](tid, info["tables"], f"{arch}_db.dat")
            r = inspect_entry(codec, entry, info)
        except (FrameError, FileNotFoundError, KeyError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        raw = r["data"]
        meta = {k: v for k, v in r["diag"].items()}
        if args.out:
            pathlib.Path(args.out).write_bytes(raw)
            meta["written"] = args.out
        print(json.dumps(meta, ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
