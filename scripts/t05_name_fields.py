"""t05_name_fields — 自动命名: 用 4CC getter 把 reader 布局挂上字段名。

完整链条(三段全部机械化):
    1) reader  : `lea rdx,[obj+OFF]` + `mov r8d,W` + `call [rax+0x28]`
                 -> (row_off, W, OFF)            [t05_reader_widths.py]
    2) 分发链  : `cmp edx, <4CC imm32>` + `je <target>`
                 -> (4CC, getter_target)
    3) getter  : `mov/movzx/movsx reg, [reg+OFF]`
                 -> (4CC, OFF, access_size)
    用 OFF 把 1) 与 3) 连接, 得到 (4CC, row_off, W)。

用法:
    py -V:3.12 -I -B scripts/t05_name_fields.py                # 全部实体
    py -V:3.12 -I -B scripts/t05_name_fields.py --type 6       # 详表
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "scratch/t05/layouts.json"
OUT = ROOT / "scratch/t05/named_fields.json"

# getter 分发链搜索窗口(相对 reader body)
DISPATCH_WINDOW = 0x6000
GETTER_BODY_BYTES = 72

ACCESS_SIZE = {"byte": 1, "word": 2, "dword": 4, "qword": 8}

# movzx/movsx/mov reg, [reg + OFF]
RE_MEM = re.compile(r"^(?:mov|movzx|movsx|movsxd)\s+([a-z0-9]+),\s*(byte|word|dword|qword)?\s*ptr\s*\[([a-z0-9]+)\s*\+\s*(0x[0-9a-f]+)\]$")
RE_JE = re.compile(r"^j(?:e|z)\s+(0x[0-9a-f]+)$")


def is_4cc(v: int) -> bool:
    b = v.to_bytes(4, "little", signed=False)
    return all(32 <= c < 127 for c in b)


def code4cc(v: int) -> str:
    """imm32 -> 4CC 字符串(generator 里 cmp edx,0x49636470 表示 'Icdp')。"""
    return v.to_bytes(4, "little", signed=False)[::-1].decode("latin1")


def parse_dispatch(md, raw: bytes, pe, body_off: int, window: int = DISPATCH_WINDOW):
    """在 reader body 之后找 `cmp <reg>, <4CC>; je <target>` 链。"""
    base_va = pe.f2va(body_off)
    if base_va is None:
        return []
    start = body_off
    end = min(body_off + window, len(raw))
    ins = list(md.disasm(raw[start:end], base_va))
    out = []
    for i, x in enumerate(ins):
        if x.mnemonic != "cmp":
            continue
        o = x.op_str.replace(" ", "")
        m = re.match(r"^([a-z0-9]+),0x([0-9a-f]+)$", o)
        if not m:
            continue
        val = int(m.group(2), 16)
        if not (0 <= val <= 0xFFFFFFFF) or not is_4cc(val):
            continue
        # 向后 1-3 条内找 je
        for k in range(i + 1, min(i + 4, len(ins))):
            jm = RE_JE.match(ins[k].mnemonic + " " + ins[k].op_str)
            if jm:
                out.append({"code": code4cc(val), "cmp_va": hex(x.address),
                            "target_va": jm.group(1)})
                break
    return out


def parse_getter(md, raw: bytes, pe, target_va: int):
    """在 getter 目标处找 `mov reg, [reg + OFF]`, 返回 (OFF, size)。"""
    off = pe.va2f(target_va)
    if off is None:
        return None
    ins = list(md.disasm(raw[off:off + GETTER_BODY_BYTES], target_va))
    for x in ins:
        if x.mnemonic not in ("mov", "movzx", "movsx", "movsxd"):
            continue
        m = RE_MEM.match(x.mnemonic + " " + x.op_str)
        if not m:
            continue
        size = ACCESS_SIZE.get(m.group(2) or "dword", 4)
        return {"object_off": int(m.group(4), 16), "access_size": size,
                "va": hex(x.address), "insn": f"{x.mnemonic} {x.op_str}"}
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", type=int, default=None)
    ap.add_argument("--layouts", default=str(LAYOUTS))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    import importlib.util
    spec = importlib.util.spec_from_file_location("_pe", ROOT / "scripts/t05_pe.py")
    pm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pm)
    pe = pm.default()

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    lay = json.loads(Path(args.layouts).read_text(encoding="utf-8"))

    # layouts.json 里的 fields 尚未带 object_off, 回读 reader_widths.json 补上
    rw = json.loads((ROOT / "scratch/t05/reader_widths.json").read_text(encoding="utf-8"))
    objmap = {}
    for r in rw["results"]:
        if r.get("reader") is None:
            continue
        objmap[r["type_id"]] = (r.get("obj_seq") or [], r.get("hits") or [])

    results = []
    for L in lay["layouts"]:
        tid = L["type_id"]
        if args.type is not None and tid != args.type:
            continue
        body = L.get("reader_body")
        if not body:
            continue
        body_off = int(body, 16)
        disp = parse_dispatch(md, pe.raw, pe, body_off)
        if not disp:
            results.append({"type_id": tid, "entity": L["entity"], "dispatch": 0,
                            "named": [], "note": "no 4CC dispatch chain found"})
            continue

        # 4CC -> object_off
        code2off = {}
        for d in disp:
            g = parse_getter(md, pe.raw, pe, int(d["target_va"], 16))
            if g:
                code2off.setdefault(d["code"], g)
        obj2code = {}
        for code, g in code2off.items():
            obj2code.setdefault(g["object_off"], code)

        # 用 reader 的 obj_seq 连接
        obj_seq, hits = objmap.get(tid, ([], []))
        archives = {}
        for arch, v in L["archives"].items():
            # 找该 archive 对应的窗口, 取其 start 以对齐 obj_seq
            win = v.get("window") or [0, 0]
            start_i = win[0]
            named = []
            for f in v["fields"]:
                gi = start_i + f["idx"]
                oo = obj_seq[gi] if gi < len(obj_seq) else None
                code = obj2code.get(oo) if isinstance(oo, int) else None
                named.append({
                    "idx": f["idx"], "row_off": f["row_off"], "width": f["width"],
                    "object_off": oo, "code": code,
                    "confidence": "readpair" if code else "layout_only",
                })
            archives[arch] = {"business_width": v["business_width"], "fields": named}

        n_named = sum(1 for a in archives.values() for f in a["fields"] if f["code"])
        results.append({"type_id": tid, "entity": L["entity"],
                        "reader_body": body, "dispatch": len(disp),
                        "codes": sorted(code2off.keys()),
                        "named_count": n_named, "archives": archives})

    Path(args.out).write_text(json.dumps({
        "note": "code 来自 exe 的 `cmp edx,<4CC>; je <getter>` 分发链, 由 getter 内 [reg+OFF] 与 "
                "reader 的 lea rdx,[obj+OFF] 同 OFF 连接。confidence=readpair 表示两侧指令均已核对。",
        "exe_sha256": pe.__class__ and __import__("hashlib").sha256(pe.raw).hexdigest(),
        "results": results,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    tot = sum(r.get("named_count", 0) for r in results)
    print(f"实体 {len(results)}, 命名字段合计 {tot}")
    print()
    for r in results:
        if args.type is not None:
            print(f"type {r['type_id']} {r['entity']} body={r.get('reader_body')} dispatch={r.get('dispatch')}")
            print(f"  codes({len(r.get('codes') or [])}): {r.get('codes')}")
            for arch, a in (r.get("archives") or {}).items():
                print(f"  [{arch}] {a['business_width']}B")
                for f in a["fields"]:
                    print(f"    row+{f['row_off']:<3} w={f['width']}  obj={f['object_off']}  "
                          f"{f['code'] or '?'}")
            print()
        else:
            print(f"{r['type_id']:>4} {str(r['entity']):<12} dispatch={r.get('dispatch', 0):>3} "
                  f"codes={len(r.get('codes') or []):>3} named={r.get('named_count', 0):>3}")
    print()
    print(f"写出 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
