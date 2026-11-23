"""Exploration v2: locate NON_PLAYER rows by identity anchor, then probe get_prop/set_prop under Unicorn."""
import json, struct, sys, time
from pathlib import Path
import pathlib

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")

import t120_people_unicorn as t120

GET_PROP = 0x140DCA880
SET_PROP = 0x140DC8C00
NULL_VAR = 0x141B5A4A0
BASIC_WIDTH = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}


def decompress(p):
    import zstandard
    raw = Path(p).read_bytes()
    with zstandard.ZstdDecompressor().stream_reader(raw[8:]) as r:
        return r.read()


def call(ut, emu, fn, args, count=5_000_000):
    stop = ut.STOP_ADDR
    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu.mu.mem_write(rsp, struct.pack("<Q", stop))
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    for i, a in enumerate(args):
        emu.mu.reg_write(emu.REG[["RCX", "RDX", "R8", "R9"][i]], a)
    err = None
    try:
        emu.mu.emu_start(fn, stop, count=count)
    except Exception as exc:
        err = f"{type(exc).__name__}@{hex(emu.mu.reg_read(emu.REG['RIP']))}"
    return emu.mu.reg_read(emu.REG["RAX"]), err


def locate(buf, ordinal, uid, max_body=2600):
    E = buf.find(struct.pack("<III", ordinal, uid, uid))
    if E < 0:
        return None
    pat = struct.pack("<IB", ordinal, 1)
    s, cands = 0, []
    while True:
        i = buf.find(pat, s)
        if i < 0:
            break
        s = i + 1
        d = E - i - 5
        if 0 < d <= max_body:
            cands.append((i, d))
    return E, cands


def deser(ut, emu, buf, hit):
    obj, vt, s19, err = t120.call_people_factory(ut, emu, 1)
    if err:
        return None, f"factory:{err}"
    res = t120.run_person_row(ut, emu, obj, s19, buf[hit + 5: hit + 5 + 65536])
    if not res["ok"]:
        return None, f"row:{res['error']}"
    return (obj, res), None


def main():
    t0 = time.time()
    basic = decompress(ROOT / "scratch/data/basic_people_db.dat")
    n = struct.unpack_from("<I", basic, 0)[0]
    W = BASIC_WIDTH
    p, rows = 5, []
    for i in range(n):
        t = basic[p + 1]
        if t == 1:
            rows.append((i, struct.unpack_from("<I", basic, p + 75)[0],
                         struct.unpack_from("<H", basic, p + 48)[0],
                         struct.unpack_from("<H", basic, p + 50)[0]))
        p += W[t]
    rows.sort(key=lambda r: (-r[2], -r[3]))
    print("ptype1", len(rows), "top", rows[:3])

    buf = decompress(ROOT / "scratch/data/people_db.dat")
    m, ut, emu, _ = t120.setup_people_emulator()
    print("emu ready", f"{time.time()-t0:.1f}s", flush=True)

    ord_, uid, ca, pa = rows[0]
    E, cands = locate(buf, ord_, uid)
    print("target", ord_, uid, "CA/PA", ca, pa, "ident_at", E, "cands", cands[:4])
    got = None
    for i, d in cands:
        r, err = deser(ut, emu, buf, i)
        if err:
            print("  cand", i, "err", err); continue
        obj, res = r
        if res["bytes_consumed"] - 12 == d:
            got = (i, obj, res)
            print("  MATCH cand", i, "body_len", d, "obj", hex(obj), "reads", len(res["reads"]))
            break
    if not got:
        print("no match"); return
    hit, obj, res = got
    body = buf[hit + 5: hit + 5 + res["bytes_consumed"]]
    print("body[:32]", body[:32].hex(), "tail12", body[-12:].hex())
    lo = max(obj - 256, ut.HEAP_BASE)
    print("obj mem", hex(lo - obj), "..+64", bytes(emu.mu.mem_read(lo, obj + 64 - lo)).hex())
    nv = struct.unpack("<Q", bytes(emu.mu.mem_read(NULL_VAR, 8)))[0]
    print("*(0x141B5A4A0)=", hex(nv))
    print("null variant vtable mem:", bytes(emu.mu.mem_read(nv, 32)).hex() if 0x140000000 <= nv < 0x150000000 else "n/a")

    var = emu._alloc(0x40)
    emu.mu.mem_write(var, struct.pack("<Q", nv))
    import re
    reg = pathlib.Path('scratch/t124/out/funcs/140dc7180.c').read_text(encoding='utf-8', errors='replace')
    props = [int(x) for x in re.findall(r'v420 = (\d+);', reg)]
    snap = bytes(emu.mu.mem_read(lo, obj + 96 - lo))
    for pid in props:
        emu.mu.mem_write(var, struct.pack("<Q", nv) + b"\x00" * 8)
        emu.unhandled_calls = []
        rax, err = call(ut, emu, GET_PROP, [obj, pid, var])
        vraw = bytes(emu.mu.mem_read(var, 16))
        vtq, val = struct.unpack("<QI", vraw[:12])
        name = struct.pack(">I", pid).decode("ascii", "replace")
        post = bytes(emu.mu.mem_read(lo, obj + 96 - lo))
        diff = [k for k in range(len(snap)) if snap[k] != post[k]]
        print(f"GET {name} pid=0x{pid:08x} rax={rax} val={val} err={err} diff={diff[:6]}")
    print("done", f"{time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
