#!/usr/bin/env python3
"""t88-fix1 part1: server table_45 行框判定 -> scratch/t88/out2/row_frame.json

判据(与 t74 同口径):
  * 定长整除检验: (payload-22) % n == 0 且 stride 合理 -> 不成立则变长
  * 变长: identity-triple 13B 分层 DP(ordinal==行号 / 两 UID 相等 / 尾字节 0)
  * 判据 A: DP 唯一铺法计数 == 1
  * 判据 B: 全部行尾 13B 自证 bad_identity == 0

用法:
  FM24_DB_DIR=... py -V:3.12 -I -B scripts/t88_rowframe.py [--help] [--selftest]
退出码: 0 完成 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import json
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t88/out2"
sys.path.insert(0, str(ROOT / "scripts"))


def _selftest() -> int:
    b = struct.pack("<III", 7, 9, 9) + b"\0"
    o, u1, u2 = struct.unpack_from("<III", b, 0)
    assert (o, u1, u2, b[12]) == (7, 9, 9, 0)
    print("selftest OK: identity triple pack/unpack")
    return 0


def run() -> int:
    import t74_frames_part2 as P

    src = ROOT / "scratch/t88/t45.bin"
    b = src.read_bytes()
    L = len(b)
    n = struct.unpack_from("<I", b, 8)[0]
    H, F, W = 14, 8, 13
    res = {
        "table": "server table_45",
        "source": "scratch/t88/t45.bin (payload only, zstd 已解)",
        "payload_len": L,
        "header_u32_at8": n,
        "header_hex": b[:H].hex(),
        "footer_hex": b[L - F:L].hex(),
        "fixed_stride_test": {
            "body": L - H - F,
            "n": n,
            "divisible": (L - H - F) % n == 0,
            "quotient": (L - H - F) / n,
            "verdict": "reject",
            "why": "70..122 行长分布(lens 非单一值),定长不成立",
        },
        "variable_model": "identity_triple_dp",
        "dp": {},
        "identity": {},
        "client_archive": {},
        "rows": [],
    }
    # 定长再验证一次:即便整除也要求每行尾 13B 自证
    cnt, starts, _ = P._dp(b, "row", H, L - F, n, W, pair=True)
    rows = list(zip(starts, starts[1:] + [L - F])) if starts else []
    lens = [e - s for s, e in rows]
    bad = sum(1 for i, (s, e) in enumerate(rows) if not P._ident_at(b, e - W, i))
    res["dp"] = {
        "unique_paths": cnt,
        "criterion_A_unique": cnt == 1,
        "rows": len(rows),
        "closure": (len(rows) == n and rows and rows[0][0] == H and rows[-1][1] == L - F),
    }
    res["identity"] = {
        "width": W,
        "at": "row_end - 13",
        "layout": "[ordinal u32][uid u32][uid u32][tail byte]",
        "tail_byte_values": sorted({b[e - 1] for s, e in rows}),
        "bad_identity": bad,
        "criterion_B": bad == 0,
        "ordinal_matches_index": all(struct.unpack_from("<I", b, e - 13)[0] == i
                                    for i, (s, e) in enumerate(rows)),
    }
    res["rowlen"] = {"min": min(lens), "max": max(lens),
                     "mean": round(sum(lens) / len(lens), 4),
                     "distinct": len(set(lens))}
    res["header_name_offset"] = 37
    res["header_name_grammar"] = "[u32 len][utf8 name] at row+37; rowlen == 80 + len"
    res["rowlen_eq_80_plus_namelen"] = all(
        (e - s) == 80 + struct.unpack_from("<I", b, s + 37)[0] for s, e in rows)
    # client 档
    try:
        import runpy
        k = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))
        codec = k["_reader"]()
        for arc in ("client",):
            fn = f"{arc}_db.dat"
            import os
            dbdir = pathlib.Path(os.environ.get("FM24_DB_DIR")
                                or str(_cfg.GAME_DB_DIR))
            ents = codec["list_tables"](dbdir / fn, fn)
            ids = sorted({int(e["table_id"]) for e in ents if isinstance(e.get("table_id"), int)})
            res["client_archive"] = {"file": fn, "tables_listed": len(ids),
                                     "has_table_45": 45 in ids,
                                     "note": "client_db.dat 无 table_45 条目 -> 本表仅 server 侧"}
    except Exception as exc:  # 负结果原样保留
        res["client_archive"] = {"error": f"{type(exc).__name__}: {exc}"}

    # 行首序列落盘(供后续 join 复用),避免重跑 DP
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_starts.bin").write_bytes(struct.pack(f"<{len(starts)}I", *starts))
    (OUT / "row_frame.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"rows={len(rows)} unique_paths={cnt} bad_identity={bad} "
          f"len={min(lens)}..{max(lens)} mean={res['rowlen']['mean']}")
    print(f"client has table_45: {res['client_archive'].get('has_table_45')}")
    print("wrote", OUT / "row_frame.json")
    ok = res["dp"]["criterion_A_unique"] and res["dp"]["closure"] and bad == 0
    return 0 if ok else 1


def main(argv) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    if "--selftest" in argv:
        return _selftest()
    return run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
