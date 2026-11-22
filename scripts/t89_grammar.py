#!/usr/bin/env python3
"""t89_grammar — 由 t9_read 读取计划推出条目字节网格,并在真实载荷上闭环验证。

模型:read 顺序即 wire 字节顺序;每条 read 消费 width 字节;
      位于回边区间内的 read 按"最近一次计数字段"的次数重复。

用法:
  py -V:3.12 -I -B scripts/t89_grammar.py --trace client 0
  py -V:3.12 -I -B scripts/t89_grammar.py --validate
  py -V:3.12 -I -B scripts/t89_grammar.py --selftest
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
JCC = r"(?:ja|jae|jb|jbe|jg|jge|jl|jle|je|jne)"


def _mod(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def wire():
    return _mod("w", "scripts/t85_fix1_wire.py")


def blocks() -> list[dict]:
    """把 read 分成块:每个块 = 一串受同一 guard 覆盖的 read。"""
    P = _mod("p", "scripts/t89_probe.py")
    ins = P.parse("probe_t9_read")
    reads = []
    for i, x in enumerate(ins):
        if not re.match(r"^call qword ptr \[\w+ \+ 0x28\]$", x["text"]):
            continue
        w = dst = None
        for j in range(i - 1, max(i - 10, -1), -1):
            tt = ins[j]["text"]
            if w is None and re.match(r"^mov r8d, ", tt):
                w = int(tt.split(",")[1].strip(), 16)
            if dst is None and re.match(r"^(lea|mov) rdx, ", tt):
                dst = tt.split(",", 1)[1].strip()
            if w is not None and dst is not None:
                break
        reads.append({"i": i, "va": x["va"], "w": w, "dst": dst})

    # 回边(循环)
    loops = []
    for x in ins:
        m = re.match(r"^(j\w+) (0x[0-9a-f]+)$", x["text"])
        if m and int(m.group(2), 16) < x["va"]:
            loops.append({"to": int(m.group(2), 16), "from": x["va"]})
    loops.sort(key=lambda b: b["to"])

    # guard: 最近的 cmp eax/ecx,IMM + 紧随 jcc,且 jcc 目标在 read 之后
    def guard_of(i, va):
        for j in range(i - 1, max(i - 80, -1), -1):
            m = re.match(r"^cmp (eax|ecx), (0x[0-9a-f]+)$", ins[j]["text"])
            if not m:
                continue
            nxt = ins[j + 1]["text"] if j + 1 < len(ins) else ""
            jm = re.match(rf"^({JCC}) (0x[0-9a-f]+)$", nxt)
            if not jm:
                return None
            tgt = int(jm.group(2), 16)
            if tgt <= va:
                return None
            op = jm.group(1)
            # jcc 跳过 read => read 在条件不成立时执行
            skip_if = {"ja": "le", "jae": "lt", "jb": "ge", "jbe": "gt",
                       "jg": "le", "jge": "lt", "jl": "ge", "jle": "gt",
                       "je": "ne", "jne": "eq"}[op]
            return {"imm": int(m.group(2), 16), "skip_if": skip_if,
                    "va": ins[j]["va"]}
        return None

    out = []
    for r in reads:
        lp = None
        for b in loops:
            if b["to"] <= r["va"] < b["from"]:
                lp = b
        out.append({**r, "guard": guard_of(r["i"], r["va"]),
                    "loop": lp["to"] if lp else None,
                    "loop_from": lp["from"] if lp else None})
    return out


def active(r: dict, version: int) -> bool:
    g = r["guard"]
    if not g:
        return True
    imm, op = g["imm"], g["skip_if"]
    return {"le": version <= imm, "lt": version < imm, "ge": version >= imm,
            "gt": version > imm, "ne": version != imm, "eq": version == imm}[op]


def simulate(body: bytes, version: int, items: list[dict] | None = None) -> dict:
    """按读取计划消费 body,返回字段落点表。"""
    items = items if items is not None else blocks()
    fields, off = [], 0
    counts = {}
    i = 0
    n = len(items)
    while i < n:
        r = items[i]
        if not active(r, version):
            i += 1
            continue
        # 循环头:同一 loop 的第一条 read
        if r["loop"] is not None:
            cnt = counts.get(r["loop"], 0)
            grp = [x for x in items[i:] if x["loop"] == r["loop"]]
            for k in range(cnt):
                for g in grp:
                    if not active(g, version):
                        continue
                    fields.append({"off": off, "w": g["w"], "dst": g["dst"],
                                   "iter": k, "loop": r["loop"]})
                    off += g["w"]
            i += len(grp)
            continue
        if off + (r["w"] or 0) > len(body):
            return {"ok": False, "off": off, "fields": fields,
                    "reason": f"overflow at dst={r['dst']} w={r['w']}"}
        fields.append({"off": off, "w": r["w"], "dst": r["dst"]})
        # 计数字段:后随循环且宽度 4/2 => 记为该循环的次数
        counts["__last"] = (r["w"], int.from_bytes(body[off:off + r["w"]], "little"))
        nxt = next((x for x in items[i + 1:] if active(x, version)), None)
        if nxt is not None and nxt["loop"] is not None and r["w"] in (2, 4):
            counts[nxt["loop"]] = counts["__last"][1]
        off += r["w"] or 0
        i += 1
    return {"ok": off == len(body), "off": off, "body_len": len(body), "fields": fields}


def load_rows(arch: str):
    w = wire()
    sz = w.member_size(arch, f"{arch}_db/table_9.dat")
    raw = w.C.payload(arch, f"{arch}_db/table_9.dat", sz)
    rows, _ = w.strict_chain(raw, 251)
    return raw, rows


def validate(version: int) -> dict:
    items = blocks()
    res = {}
    for arch in ("client", "server"):
        raw, rows = load_rows(arch)
        ok = bad = 0
        first_bad = None
        lens = set()
        for r in rows:
            b = raw[r["body_start"]:r["body_start"] + r["body_len"]]
            s = simulate(b, version, items)
            lens.add(r["body_len"])
            if s["ok"]:
                ok += 1
            else:
                bad += 1
                if first_bad is None:
                    first_bad = {"row": r["row"], "body_len": r["body_len"],
                                 "sim": s["off"], "reason": s.get("reason")}
        res[arch] = {"rows": len(rows), "closed": ok, "open": bad,
                     "distinct_body_len": len(lens), "first_open": first_bad}
    return {"version": hex(version), "result": res}


def trace(arch: str, row: int, version: int) -> dict:
    raw, rows = load_rows(arch)
    r = rows[row]
    b = raw[r["body_start"]:r["body_start"] + r["body_len"]]
    s = simulate(b, version)
    return {"arch": arch, "row": row, "body_len": r["body_len"],
            "body_hex": b.hex(" "), "sim_off": s["off"], "closed": s["ok"],
            "fields": s["fields"]}


def selftest() -> int:
    bl = blocks()
    assert len(bl) == 150, len(bl)
    assert bl[0]["w"] == 2 and bl[0]["dst"] == "[rsi + 0x19c]", bl[0]
    loops = {x["loop"] for x in bl if x["loop"]}
    assert loops, "no loop reads"
    r = trace("client", 0, 0xDC3)
    assert r["body_len"] == 251, r["body_len"]
    v = validate(0xDC3)
    assert v["result"]["client"]["rows"] == 251
    print("selftest OK", {"blocks": len(bl), "loops": len(loops),
                          "client_closed": v["result"]["client"]["closed"],
                          "row0_sim_off": r["sim_off"]})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t9 条目文法模拟器")
    ap.add_argument("--trace", nargs=2, metavar=("ARCH", "ROW"))
    ap.add_argument("--validate", nargs="?", const="0xdc3", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.trace:
        import json
        t = trace(a.trace[0], int(a.trace[1]), 0xDC3)
        print(f"row={t['row']} body_len={t['body_len']} sim_off={t['sim_off']} closed={t['closed']}")
        for f in t["fields"][:40]:
            print(f"  +{f['off']:4d} w={f['w']} {f['dst']} iter={f.get('iter','-')}")
        return 0 if t["closed"] else 1
    if a.validate:
        import json
        v = validate(int(a.validate, 16))
        print(json.dumps(v, indent=1))
        return 0 if all(x["open"] == 0 for x in v["result"].values()) else 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
