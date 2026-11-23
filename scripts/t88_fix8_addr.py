#!/usr/bin/env python3
"""t88_fix8_addr — 用真 PE 节表换算 5 个关键地址,并复核 CBDa/CBWa cmp 位点。

用法:
  py -V:3.12 -I -B scripts/t88_fix8_addr.py --run
  py -V:3.12 -I -B scripts/t88_fix8_addr.py --selftest

输出 scratch/t88/out3/fixed_addresses.json
退出码 0 成功 / 1 检查未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from t88_pe import PE, EXE, disasm  # noqa: E402

OUT = pathlib.Path("scratch/t88/out3")

TARGETS = [
    ("cmp_CBDa_lea", 0x1411F0CA7),
    ("cmp_CBWa_lea", 0x1411F0CB6),
    ("tc_record_get", 0x143EBAD50),
    ("hub_11e8af0", 0x1411E8AF0),
    ("hub_11f2a76", 0x1411F2A76),
    ("global_STARTING_RECORD", 0x141B60190),
]


def le_4cc(s: str) -> int:
    """'CBDa' -> 内存小端 u32 (0x61444243)"""
    return struct.unpack("<I", s.encode("ascii"))[0]


def be_4cc(s: str) -> int:
    """'CBDa' -> cmp 立即数形式(按字节序 'C','B','D','a' 作 u32 大端) 0x43424461"""
    return struct.unpack(">I", s.encode("ascii"))[0]


def build() -> dict:
    pe = PE(EXE)
    rows = []
    for label, va in TARGETS:
        sec = pe.section_of_va(va)
        fo = pe.va_to_fo(va)
        rows.append({
            "label": label, "va": f"0x{va:x}",
            "rva": f"0x{va - pe.image_base:x}",
            "section": sec["name"] if sec else None,
            "section_idx": sec["idx"] if sec else None,
            "fo": f"0x{fo:x}" if fo is not None else None,
            "file_mapped": fo is not None,
            "in_raw": (fo is not None),
            "bytes": pe.read(va, 16).hex() if fo is not None else None,
            "note": ("BSS/未初始化区:无静态初值,运行期写入"
                     if fo is None else None),
        })
    # cmp 位点反汇编窗口
    cmp_win = disasm(pe, 0x1411F0C9B, 0x50)
    return {"pe": {"sha256": pe.sha256, "sha256_prefix": pe.sha256[:8],
                   "image_base": pe.image_base, "nsec": pe.nsec},
            "addresses": rows,
            "cmp_window": cmp_win}


def analyze(d: dict) -> dict:
    """从 cmp 窗口确认 lea/cmp/jbe 三元组与跳转目标。"""
    win = d["cmp_window"]
    res = {}
    for i, ins in enumerate(win):
        if ins["mn"] == "lea" and "rsi - 0x" in ins["op"]:
            imm = int(ins["op"].split("- 0x")[1], 16)
            nxt = win[i + 1] if i + 1 < len(win) else None
            res[ins["va"]] = {
                "lea": ins["text"], "imm": f"0x{imm:08x}",
                "imm_bytes_be": struct.pack(">I", imm).decode("latin-1"),
                "imm_bytes_le": struct.pack("<I", imm).decode("latin-1"),
                "next": nxt["text"] if nxt else None,
            }
    return res


def selftest() -> int:
    d = build()
    a = analyze(d)
    # 两个位点必须在窗口内且紧跟 cmp
    assert "0x1411f0ca7" in a, list(a)
    assert "0x1411f0cb6" in a, list(a)
    assert a["0x1411f0ca7"]["imm"] == "0x43424461", a["0x1411f0ca7"]
    assert a["0x1411f0cb6"]["imm"] == "0x43425761", a["0x1411f0cb6"]
    # 4CC 解码必须是 CBDa / CBWa
    assert a["0x1411f0ca7"]["imm_bytes_be"] == "CBDa"
    assert a["0x1411f0cb6"]["imm_bytes_be"] == "CBWa"
    # 五地址:四个有文件映射
    m = {r["label"]: r for r in d["addresses"]}
    assert m["cmp_CBDa_lea"]["section"] == ".rdata"
    assert m["cmp_CBWa_lea"]["section"] == ".rdata"
    assert m["tc_record_get"]["file_mapped"] is True
    assert m["hub_11e8af0"]["file_mapped"] is True
    assert m["global_STARTING_RECORD"]["file_mapped"] is False
    assert m["global_STARTING_RECORD"]["section"] == ".sbss"
    # 反例留档:LE 字节序不是 cmp 立即数形态
    assert le_4cc("CBDa") == 0x61444243
    print("selftest OK", {"n_addr": len(d["addresses"]),
                          "cbd_imm": a["0x1411f0ca7"]["imm"],
                          "cbw_imm": a["0x1411f0cb6"]["imm"]})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t88-fix8 地址换算 + cmp 复核")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.run:
        ap.print_help()
        return 2
    d = build()
    d["cmp_analysis"] = analyze(d)
    d["4cc_encoding_note"] = {
        "cmp_imm_form": "0x43424461  (= 'C','B','D','a' 顺序装入 u32)",
        "mem_le_form": "0x61444243  (若按 <I 解码字符串)",
        "conclusion": ("editor.exe 的 4CC 分发用 '字节顺序装入' 立即数,"
                       "即 ASCII 正序;fix6 以 <I 小端搜索才误判'字节缺席'"),
    }
    p = OUT / "fixed_addresses.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=1), encoding="utf-8")
    print("wrote", p)
    for r in d["addresses"]:
        print(f"  {r['label']:24s} {r['va']:>14s} {str(r['section']):8s} fo={r['fo']}")
    for k, v in d["cmp_analysis"].items():
        print(f"  {k} {v['imm']} -> {v['imm_bytes_be']} next={v['next']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
