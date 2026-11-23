"""Probe: Unicorn GET/SET memory-diff verification of NON_PLAYER 4CC -> obj_off mapping."""
import re, struct, sys, time
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
import t120_people_unicorn as t120

GET_PROP = 0x140DCA880
SET_PROP = 0x140DC8C00
NULL_VAR = 0x141B5A4A0
W = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}


def decompress(p):
    import zstandard
    raw = Path(p).read_bytes()
    with zstandard.ZstdDecompressor().stream_reader(raw[8:]) as r:
        return r.read()


def call(ut, emu, fn, args, count=2_000_000):
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


def main():
    t0 = time.time()
    basic = decompress(ROOT / "scratch/data/basic_people_db.dat")
    n = struct.unpack_from("<I", basic, 0)[0]
    p, rows = 5, []
    for i in range(n):
        t = basic[p + 1]
        if t == 1:
            rows.append((i, struct.unpack_from("<I", basic, p + 75)[0],
                         struct.unpack_from("<H", basic, p + 48)[0],
                         struct.unpack_from("<H", basic, p + 50)[0]))
        p += W[t]
    rows.sort(key=lambda r: (-r[2], -r[3]))
    ord_, uid, ca, pa = rows[0]
    buf = decompress(ROOT / "scratch/data/people_db.dat")
    m, ut, emu, _ = t120.setup_people_emulator()
    E = buf.find(struct.pack("<III", ord_, uid, uid))
    hit = None
    pat = struct.pack("<IB", ord_, 1)
    s = 0
    while True:
        i = buf.find(pat, s)
        if i < 0:
            break
        s = i + 1
        d = E - i - 5
        if not (0 < d <= 2600):
            continue
        obj, vt, s19, err = t120.call_people_factory(ut, emu, 1)
        res = t120.run_person_row(ut, emu, obj, s19, buf[i + 5:i + 5 + 65536])
        if res["ok"] and res["bytes_consumed"] - 12 == d:
            hit = i
            break
    print("obj", hex(obj), "body", d, f"{time.time()-t0:.1f}s", flush=True)
    nv = struct.unpack("<Q", bytes(emu.mu.mem_read(NULL_VAR, 8)))[0]
    var = emu._alloc(0x40)
    lo = max(obj - 0x100, ut.HEAP_BASE)
    base = 0xf8
    codes = []
    for f in ("scratch/t124/out/funcs/140dca880.c", "scratch/t124/out/funcs/140dc8c00.c"):
        t = Path(f).read_text(encoding="utf-8", errors="replace")
        for mm in re.finditer(r"(?:case\s+|a2\s*[=!]=\s*)(1[0-9]{9})", t):
            v = int(mm.group(1))
            try:
                s4 = struct.pack(">I", v).decode("ascii")
            except Exception:
                continue
            if s4.isprintable() and s4 not in codes:
                codes.append(s4)
    print("codes", len(codes))
    span_hi = min(obj + 0x60, ut.HEAP_BASE + ut.HEAP_SIZE)
    snap = bytes(emu.mu.mem_read(lo, span_hi - lo))
    okget = 0
    results = []
    for c in codes:
        pid = int.from_bytes(c.encode(), "big")
        emu.mu.mem_write(var, struct.pack("<Q", nv) + b"\x00" * 8)
        emu.unhandled_calls = []
        rax, err = call(ut, emu, GET_PROP, [obj, pid, var])
        vraw = bytes(emu.mu.mem_read(var, 16))
        vtq, val = struct.unpack("<QI", vraw[:12])
        # set to 17
        emu.mu.mem_write(var, struct.pack("<Q", nv) + struct.pack("<I", 17) + b"\x00" * 4)
        rax2, err2 = call(ut, emu, SET_PROP, [obj, pid, var])
        post = bytes(emu.mu.mem_read(lo, span_hi - lo))
        diff = [lo + k - obj for k in range(len(snap)) if snap[k] != post[k]]
        results.append((c, rax, err, val, err2, diff))
        if not err and not err2:
            okget += 1
    print("clean calls", okget, "/", len(codes), f"{time.time()-t0:.1f}s")
    for c, rax, err, val, err2, diff in results:
        print(f"{c} get={rax} val={val} set_err={err2} diff={diff[:4]} err={err}")
    print("done", f"{time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
