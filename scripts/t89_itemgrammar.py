#!/usr/bin/env python3
"""t89_itemgrammar — 条目读取器 0x1408386a0 的 28-case 文法分类。

条目 = [tag u8][subtype u8][payload],subtype 经跳转表分发到 28 个 case。
本模块反汇编该函数(只读 editor.exe),逐 case 抽出:
  width   : 该 case 直读的标量字节数(可能多次)
  field_id: `add rax, 0xNN` 的字段枚举偏移(标量类型 id)
  nested  : 是否递归调用条目读取器(嵌套对象)
  vector  : 是否走 0x140839290 / 0x140839480(向量容器,元素 stride 4/16 或 8)

用法:
  py -V:3.12 -I -B scripts/t89_itemgrammar.py --json
  py -V:3.12 -I -B scripts/t89_itemgrammar.py --table
  py -V:3.12 -I -B scripts/t89_itemgrammar.py --selftest
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ITEM_READER = 0x1408386A0
JUMP_LEA = 0x140838726       # lea rax, [rip + 0xaeb]
DISPATCH_END = 0x140838CE2   # 所有 case 收敛点之外
LOOP_BODY = 0x140838736      # case 0/6/7 的"无载荷"落点
RET_OK = 0x140838701


def _mod(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def cases() -> list[dict]:
    D = _mod("d", "scripts/t89_disasm.py")
    S = _mod("s", "scripts/t89_scan.py")
    db = S.load()
    tbl_va = JUMP_LEA + 7 + 0xAEB
    tbl_fo = S.va_to_fo(tbl_va)
    targets = []
    for k in range(0x1C):
        rel = struct.unpack_from("<i", db, tbl_fo + 4 * k)[0]
        targets.append(tbl_va + rel)

    # 反汇编整段,按 VA 建索引
    code = D.disasm(ITEM_READER, DISPATCH_END - ITEM_READER + 0x40)
    idx = {x["va"]: i for i, x in enumerate(code)}

    out = []
    for k, tva in enumerate(targets):
        if tva not in idx:
            out.append({"case": k, "va": f"0x{tva:x}", "status": "outside_window"})
            continue
        i = idx[tva]
        widths, field_ids, nested, vectors = [], [], False, []
        # 线性扫描到 case 收敛(jmp LOOP_BODY / RET_OK)或遇到下一个 case 起点
        stop = min(idx[v] for v in targets if v in idx and v > tva) if any(
            v in idx and v > tva for v in targets) else len(code)
        while i < stop:
            x = code[i]
            t = x["text"]
            m = re.search(r"mov r8d, (0x[0-9a-f]+|\d+)", t)
            if m:
                # 宽度在前导 4 条内跟到 call [rax+0x28] 即计为一次直读
                for j in range(i + 1, min(i + 5, len(code))):
                    if "call qword ptr [rax + 0x28]" in code[j]["text"]:
                        widths.append(int(m.group(1), 0))
                        break
            m = re.search(r"^add rax, (0x[0-9a-f]+)$", t)
            if m:
                field_ids.append(int(m.group(1), 16))
            m = re.search(r"^call (0x[0-9a-f]+)$", t)
            if m:
                callee = int(m.group(1), 16)
                if callee == ITEM_READER:
                    nested = True
                elif callee in (0x140839290, 0x140839480):
                    vectors.append({"helper": f"0x{callee:x}",
                                    "stride": 16 if callee == 0x140839290 else 8})
            if t in (f"jmp 0x{LOOP_BODY:x}", f"jmp 0x{RET_OK:x}"):
                break
            i += 1
        out.append({"case": k, "va": f"0x{tva:x}", "widths": widths,
                    "payload": sum(widths), "field_ids": [f"0x{v:x}" for v in field_ids],
                    "nested": nested, "vectors": vectors,
                    "kind": ("vector" if vectors else "nested" if nested else
                             "scalar" if widths else "empty")})
    return out


def grammar() -> dict:
    cs = cases()
    return {
        "item_reader": {"va": f"0x{ITEM_READER:x}", "fo": "0x837ca0"},
        "dispatch": {"jump_table_va": "0x140839218", "cases": 0x1C,
                     "subtype_byte": "[rbp-0x41]", "tag_byte": "[rbp-0x42]"},
        "items": cs,
        "summary": {
            "empty": sum(1 for c in cs if c.get("kind") == "empty"),
            "scalar": sum(1 for c in cs if c.get("kind") == "scalar"),
            "nested": sum(1 for c in cs if c.get("kind") == "nested"),
            "vector": sum(1 for c in cs if c.get("kind") == "vector"),
            "payload_widths": sorted({c["payload"] for c in cs if c.get("payload")}),
        },
    }


def selftest() -> int:
    g = grammar()
    it = g["items"]
    assert len(it) == 0x1C, len(it)
    # case 0/6/7 = 无载荷
    for k in (0, 6, 7):
        assert it[k]["kind"] == "empty", (k, it[k])
    # case 1 = u32 (width 4)
    assert it[1]["payload"] == 4, it[1]
    # case 3 = u8
    assert it[3]["payload"] == 1, it[3]
    # case 5 = f64
    assert it[5]["payload"] == 8, it[5]
    # case 10/11 = 向量容器
    assert it[10]["kind"] == "vector" and it[11]["kind"] == "vector", (it[10], it[11])
    assert it[10]["vectors"][0]["stride"] == 16
    assert it[11]["vectors"][0]["stride"] == 8
    print("selftest OK", g["summary"])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="条目读取器 28-case 文法")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    g = grammar()
    if a.json:
        print(json.dumps(g, indent=1, ensure_ascii=False))
        return 0
    if a.table:
        for c in g["items"]:
            print(f"{c['case']:2d} 0x{int(c['va'],16):x} {c['kind']:7s} "
                  f"payload={c.get('payload','-')} field={','.join(c.get('field_ids') or []) or '-'} "
                  f"vec={c.get('vectors') or '-'}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
