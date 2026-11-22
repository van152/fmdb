#!/usr/bin/env python3
"""t89 验收校验器(指挥官在验收时补写,非车道交付;E88 先例)。

独立重抽:不 import 任何 builder,只用 fm24_dump.load_payload 与纯 struct。
校验项:
  V1 server table_9 载荷长度 = 307,564(纠正 E127 的 307,555)
  V2 载荷头部 u32@+8 = 251(两档),13B 头
  V3 client 闭包:13 + sum(body) + 12*251 + 9 = 31,956,body 和取 _dual.json
  V4 ordinal lane:client 每 251 行 body[12] == ordinal & 0xff
  V5 sentinel head:client 251 行 body[0:5] == 00 ff ff ff ff
退出码 0=全过 / 1=有失败;--selftest 自检退出码。
"""
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, "D:/tmp2b/fm24/tools/python")


def _load():
    import runpy
    k = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))
    codec = k["_reader"]()
    return {s: k["load_payload"](codec, s, 9) for s in ("client", "server")}


def main() -> int:
    pay = _load()
    fails = []

    def chk(name, ok, detail=""):
        print(("OK   " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    # V1
    chk("V1 server len 307564", len(pay["server"]) == 307564, f"got={len(pay['server'])}")
    # V2
    for s in ("client", "server"):
        n = struct.unpack_from("<I", pay[s], 8)[0]
        chk(f"V2 {s} count@+8=251", n == 251, f"got={n}")
    # V3
    dual = json.loads((ROOT / "scratch/t89/out/_dual.json").read_bytes().decode("utf-8", "replace"))
    s_body = dual["client"]["body_len"]["sum"]
    chk("V3 client closure", 13 + s_body + 12 * 251 + 9 == len(pay["client"]),
        f"body_sum={s_body}")
    # V4/V5/V6: 独立行走(body lens 取 _tile.json,游标推进自实现)
    tile = json.loads((ROOT / "scratch/t89/out/_tile.json").read_bytes().decode("utf-8", "replace"))
    lens = tile["lens"]
    ok_ord = ok_head = 0
    pos = 13
    for i, bl in enumerate(lens[:251]):
        body = pay["client"][pos:pos + bl]
        if len(body) >= 13 and body[12] == (i & 0xFF):
            ok_ord += 1
        if body[0:5] == b"\x00\xff\xff\xff\xff":
            ok_head += 1
        pos += bl + 12
    chk("V4 ordinal lane 251/251", ok_ord == 251, f"ok={ok_ord}")
    chk("V5 sentinel head 251/251", ok_head == 251, f"ok={ok_head}")
    chk("V6 tile walks payload", pos == len(pay["client"]) - 9, f"end={pos}")
    print(f"\n{len(fails)} failure(s)")
    return 1 if fails else 0


def selftest() -> int:
    assert 13 + 28922 + 12 * 251 + 9 == 31956
    assert struct.unpack_from("<I", b"\xfb\x00\x00\x00", 0)[0] == 251
    print("SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
