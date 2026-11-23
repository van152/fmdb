"""Exploration: call NON_PLAYER::get_prop / set_prop under Unicorn on a deserialized row."""
import json, struct, sys, time
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")

import t120_people_unicorn as t120

GET_PROP = 0x140DCA880
SET_PROP = 0x140DC8C00

def decompress(p):
    import zstandard
    raw = Path(p).read_bytes()
    with zstandard.ZstdDecompressor().stream_reader(raw[8:]) as r:
        return r.read()

def call(ut, emu, fn, args, stop=None):
    stop = stop or ut.STOP_ADDR
    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu.mu.mem_write(rsp, struct.pack("<Q", stop))
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    regs = ["RCX", "RDX", "R8", "R9"]
    for i, a in enumerate(args):
        emu.mu.reg_write(emu.REG[regs[i]], a)
    err = None
    try:
        emu.mu.emu_start(fn, stop, count=5_000_000)
    except Exception as exc:
        err = f"{exc}@{hex(emu.mu.reg_read(emu.REG['RIP']))}"
    return emu.mu.reg_read(emu.REG["RAX"]), err

def main():
    t0 = time.time()
    basic = decompress(ROOT / "scratch/data/basic_people_db.dat")
    n = struct.unpack_from("<I", basic, 0)[0]
    print("basic rows", n, "bytes", len(basic))
    W = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
    p, rows = 5, []
    for i in range(n):
        t = basic[p + 1]
        if t == 1:
            rows.append((i, p, struct.unpack_from("<I", basic, p + 75)[0],
                         struct.unpack_from("<H", basic, p + 48)[0],
                         struct.unpack_from("<H", basic, p + 50)[0],
                         struct.unpack_from("<H", basic, p + 52)[0]))
        p += W[t]
    print("ptype1 rows", len(rows), "closure", p - (len(basic) - 9), f"{time.time()-t0:.1f}s")
    top = sorted(rows, key=lambda r: (-r[3], -r[4]))[:20]
    for r in top[:5]:
        print("top", r)

    buf = decompress(ROOT / "scratch/data/people_db.dat")
    print("people_db", len(buf), f"{time.time()-t0:.1f}s")
    m, ut, emu, _ = t120.setup_people_emulator()
    print("emu ready", f"{time.time()-t0:.1f}s")

    # locate the first top row
    tgt = top[0]
    pat = struct.pack("<IB", tgt[0], 1)
    hits, s = [], 0
    while len(hits) < 6:
        i = buf.find(pat, s)
        if i < 0:
            break
        hits.append(i); s = i + 1
    print("hits", hits)

    obj = vt = s19 = None
    for hit in hits:
        o, v, s19v, err = t120.call_people_factory(ut, emu, 1)
        if err:
            print("factory err", err); continue
        res = t120.run_person_row(ut, emu, o, s19v, buf[hit + 5: hit + 5 + 65536])
        if not res["ok"]:
            print("row fail", hit, res["error"]); continue
        id_rd = next((r for r in reversed(res["reads"]) if r["n"] == 12), None)
        ident = struct.unpack("<III", bytes.fromhex(id_rd["hex"])) if id_rd and len(id_rd["hex"]) == 24 else None
        print("hit", hit, "ok consumed", res["bytes_consumed"], "ident", ident, "target", tgt[0], tgt[2])
        if ident and ident[0] == tgt[0] and ident[2] == tgt[2]:
            obj, vt, s19 = o, v, s19v
            body = buf[hit + 5: hit + 5 + res["bytes_consumed"]]
            print("body head", body[:40].hex())
            break
    print("obj", hex(obj), "vt", hex(vt), "s19", hex(s19), f"{time.time()-t0:.1f}s")
    print("obj mem -256..+64:", bytes(emu.mu.mem_read(obj - 256, 320)).hex())

    # null variant singleton
    nullvt = struct.unpack("<Q", bytes(emu.mu.mem_read(0x141B5A4A0, 8)))[0]
    print("qword_141B5A4A0 =", hex(nullvt))
    var = emu._alloc(64)
    emu.mu.mem_write(var, struct.pack("<Q", 0x141B5A4A0) + b"\x00" * 8)

    for pid in (0x4e637261, 0x4e707461, 0x4e777272, 0x4e637272, 0x4e686d72, 0x4e543031, 0x4e543135):
        rax, err = call(ut, emu, GET_PROP, [obj, pid, var])
        val = struct.unpack("<I", bytes(emu.mu.mem_read(var + 8, 4)))[0]
        vtq = struct.unpack("<Q", bytes(emu.mu.mem_read(var, 8)))[0]
        name = struct.pack(">I", pid).decode("ascii", "replace")
        print(f"prop {name} pid=0x{pid:08x} rax={rax} value={val} var_vt={hex(vtq)} err={err} unhandled={emu.unhandled_calls[:2]}")
        emu.unhandled_calls = []
    print("done", f"{time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
