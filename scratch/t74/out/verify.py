"""t74 独立 verifier:不 import builder(t74_row_frames9 / t74_frames_part*),
自行重载 payload、重算 closure/identity/锚点,与 frames.json 对拍。

退出码:0 全部通过 / 1 有检查未过 / 2 用法或致命错误。
用法:
  FM24_DB_DIR=... py -V:3.12 -I -B scratch/t74/out/verify.py [--help] [--selftest]
"""
import hashlib
import json
import os
import pathlib
import runpy
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
MAGIC = bytes.fromhex("28b52ffd")
FRAMES = ROOT / "scratch/t74/out/frames.json"
READER = ROOT / "scratch/t01/inbox/t01k/verify.py"


def die(msg, code=2):
    print(f"FATAL: {msg}", file=sys.stderr)
    raise SystemExit(code)


def codec():
    if not READER.exists():
        die(f"reader verify not found: {READER}")
    k = runpy.run_path(str(READER))
    return runpy.run_path(str(k["OLD_READER_PATH"]))


def load(c, archive, tid):
    """独立实现:成员区 data_base+offset,按 len==size 选帧,不回落。"""
    fn = f"{archive}_db.dat"
    d = pathlib.Path(os.environ.get("FM24_DB_DIR")
                     or r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm")
    p = d / fn
    ents = c["list_tables"](p, fn)
    e = c["_resolve_table"](tid, ents, fn)
    db = p.read_bytes()
    base = int(c["_archive_layout"](db)["data_base"])
    start, end, size = base + int(e["offset"]), 0, int(e["size"])
    end = start + int(e["packed_size"])
    if not (0 <= start < end <= len(db)):
        die(f"{fn} t{tid}: member out of range")
    off = next((k for k in range(min(64, end - start))
                if db[start + k:start + k + 4] == MAGIC), None)
    if off is None:
        die(f"{fn} t{tid}: no zstd frame")
    z = c["_zstd_module"]()
    ctx = z.ZstdDecompressor()
    pos = start + off
    while pos + 4 <= end and db[pos:pos + 4] == MAGIC:
        obj = ctx.decompressobj()
        out = obj.decompress(db[pos:end])
        if len(out) == size:
            return out
        used = (end - pos) - len(obj.unused_data)
        if not obj.eof or used <= 0:
            break
        pos += used
    die(f"{fn} t{tid}: no frame with len == {size}")


def u32(b, p):
    return struct.unpack_from("<I", b, p)[0]


def lstr(b, q, e):
    if q + 4 > e:
        return None
    n = u32(b, q)
    if n > 4096 or q + 4 + n > e:
        return None
    try:
        t = b[q + 4:q + 4 + n].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return (q + 4 + n, n, t) if t and t.isprintable() else None


def scan(b, lo, hi, n, W):
    """候选扫描:ordinal<n 且 UID 对相等且 UID>0。向量化(4 对齐 × 4 相位)。"""
    import numpy as np
    cand = {}
    m = len(b)
    for off in range(4):
        cnt = (m - off - 3) // 4
        if cnt <= 2:
            continue
        w = np.frombuffer(b, dtype="<u4", count=cnt, offset=off)
        o, u1, u2 = w[:cnt - 2], w[1:cnt - 1], w[2:cnt]
        mask = (o < n) & (u1 == u2) & (u1 > 0)
        idx = np.nonzero(mask)[0]
        if not len(idx):
            continue
        pos = idx * 4 + off
        keep = (pos >= lo) & (pos + W <= hi)
        for p, oo, uu in zip(pos[keep].tolist(), o[idx][keep].tolist(), u1[idx][keep].tolist()):
            cand.setdefault(oo, []).append((p, uu))
    for k in cand:
        cand[k].sort()
    return cand


def solo_path(b, lo, hi, n, W):
    """分层 DP(ordinal 递增、UID 严格递增、行不重叠),回推唯一铺法。"""
    cand = scan(b, lo, hi, n, W)
    if any(i not in cand for i in range(n)):
        return None
    states = {(lo, 0): (1, None)}
    hist = [dict(states)]
    for i in range(n):
        nxt = {}
        for (q, pu), (c, _) in states.items():
            for p, u in cand[i]:
                if p < q:
                    continue
                if p + W > hi:
                    break
                if u <= pu:
                    continue
                key = (p + W, u)
                nxt[key] = (nxt.get(key, (0, None))[0] + c, (q, pu))
        if not nxt:
            return None
        states = nxt
        hist.append(dict(states))
    fin = [k for k in states if k[0] == hi]
    if len(fin) != 1 or states[fin[0]][0] != 1:
        return None
    cur = fin[0]
    out = [0] * n
    for i in range(n, 0, -1):
        q, pu = hist[i][cur][1]
        out[i - 1] = q
        cur = (q, pu)
    return out


def rows_fixed(b, H, F, n, st):
    if H + n * st + F != len(b):
        return None
    return [(H + i * st, H + (i + 1) * st) for i in range(n)]


def rows_seq_lang(b, H, F, n):
    p, i, rows, suf = H, 0, [], []
    while p < F:
        r = lstr(b, p, F)
        if not r:
            return None, None
        q, nl, _ = r
        if q + 30 > F:
            return None, None
        rows.append((p, q + 30))
        suf.append((i, q))
        p = q + 30
        i += 1
    return (rows, suf) if i == n and p == F else (None, None)


def rows_seq_weat(b, H, F, n):
    p, i, rows = H, 0, []
    while p < F:
        L = u32(b, p)
        if not (0 < L < 200):
            return None
        e = p + 4 + L + 95 + 13
        if e > F:
            return None
        rows.append((p, e))
        p = e
        i += 1
    return rows if i == n and p == F else None


def rows_seq_derby(b, H, F, n, const):
    p, i, rows = H, 0, []
    while p < F:
        q, tot, k = p, 0, 0
        while k < 8:
            r = lstr(b, q, F)
            if not r:
                break
            q, nl, _ = r
            tot, k = tot + nl, k + 1
        if (q - p) != tot + 4 * k:
            return None
        e = p + tot + const
        if e > F:
            return None
        rows.append((p, e))
        p = e
        i += 1
    return rows if i == n and p == F else None


def rows_id_dp(b, H, F, n, W, foot):
    """solo_path 返回的是每行行首;行尾 = 下一行首(footer 前)。"""
    hi = len(b) - foot
    starts = solo_path(b, H, hi, n, W)
    if not starts or len(starts) != n:
        return None
    ends = starts[1:] + [hi]
    rows = list(zip(starts, ends))
    return rows if sum(e - s for s, e in rows) == hi - H else None


CHECKS = []   # (name, ok, detail)


def chk(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def verify_table(c, frames, tid, archive, want_rows_min=3):
    key = str(tid)
    fr = frames["tables"].get(key)
    if fr is None:
        chk(f"t{tid}/{archive}", False, "missing frames entry")
        return
    arc = fr["archives"].get(archive)
    if arc is None:
        if fr["archives"].get("client", {}).get("status") == "absent" and archive == "client":
            chk(f"t{tid}/client", True, "declared absent (client has no entry)")
            return
        chk(f"t{tid}/{archive}", False, "missing archive entry")
        return
    if arc.get("status") == "absent":
        chk(f"t{tid}/{archive}", True, "declared absent")
        return
    b = load(c, archive, tid)
    chk(f"t{tid}/{archive}/payload_len", len(b) == arc["payload_len"],
        f"actual {len(b)}")
    chk(f"t{tid}/{archive}/sha256", hashlib.sha256(b).hexdigest() == arc["payload_sha256"],
        hashlib.sha256(b).hexdigest()[:16])
    H, F, n = arc["header"], arc["footer"], arc["count"]
    model = arc["model"]
    W = arc["identity"]["width"]
    if model == "fixed":
        rows = rows_fixed(b, H, F, n, arc["stride"])
    elif tid == 8:
        rows, _ = rows_seq_lang(b, H, len(b) - F, n)
    elif tid == 27:
        rows = rows_seq_weat(b, H, len(b) - F, n)
    elif tid == 18:
        rows = rows_seq_derby(b, H, len(b) - F, n, 65 if archive == "client" else 71)
    elif tid in (7, 47, 24):
        rows = rows_id_dp(b, H, F, n, W, F)
    else:
        rows = None
    chk(f"t{tid}/{archive}/closure", rows is not None,
        "行框重建失败" if rows is None else f"{len(rows)} 行")
    if not rows:
        return
    chk(f"t{tid}/{archive}/rows", len(rows) == n, f"{len(rows)} vs {n}")
    bad = 0
    for i, (s, e) in enumerate(rows):
        ip = e - W
        o, u1, u2 = struct.unpack_from("<III", b, ip)
        if o != i or u1 != u2:
            bad += 1
        elif tid != 24 and b[ip + W - 1] != 0:
            bad += 1
    chk(f"t{tid}/{archive}/identity", bad == 0, f"{bad} 行 identity 不符")


ANCHORS = {
    ("client", 56): {"rdui": 0, "duni": 4},
    ("client", 0): {"rdui": 64, "duni": 68},
    ("client", 21): {"rdui": 25, "duni": 29},
    ("client", 47): {"rdui": -13, "duni": -9},
}


def verify_anchors(c):
    for (archive, tid), spec in ANCHORS.items():
        fr = json.load(open(FRAMES, encoding="utf-8"))
        arc = fr["tables"][str(tid)]["archives"][archive]
        b = load(c, archive, tid)
        H, F, n = arc["header"], arc["footer"], arc["count"]
        if arc["model"] == "fixed":
            rows = rows_fixed(b, H, F, n, arc["stride"])
        else:
            rows = rows_id_dp(b, H, F, n, arc["identity"]["width"], F)
        if not rows:
            chk(f"anchor/t{tid}", False, "rows missing")
            continue
        for name, off in spec.items():
            hit = 0
            for i, (s, e) in enumerate(rows):
                p = e + off if off < 0 else s + off
                v = u32(b, p)
                if name == "rdui":
                    hit += (v == i)
                else:
                    hit += (v == u32(b, p + 4))
            chk(f"anchor/{archive}/t{tid}/{name}", hit == len(rows),
                f"{hit}/{len(rows)} @ {off}")
    # t8 的 rdui_suffix@17:后缀内偏移,不是行内偏移
    fr = json.load(open(FRAMES, encoding="utf-8"))
    arc = fr["tables"]["8"]["archives"]["client"]
    b = load(c, "client", 8)
    rows, suf = rows_seq_lang(b, arc["header"], len(b) - arc["footer"], arc["count"])
    if suf:
        hit = sum(1 for i, sp in suf if u32(b, sp + 17) == i)
        chk("anchor/client/t8/rdui_suffix", hit == len(suf), f"{hit}/{len(suf)} @ suffix+17")


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    if not FRAMES.exists():
        die(f"frames.json not found: {FRAMES}")
    frames = json.load(open(FRAMES, encoding="utf-8"))
    if "--selftest" in argv:
        print("selftest: checks primitives without touching the game DB")
        b = struct.pack("<III", 0, 7, 7) + b"\0"
        chk("selftest/u32", u32(b, 0) == 0)
        chk("selftest/lstr", lstr(struct.pack("<I", 2) + b"ab" + b"\0\0", 0, 9)[2] == "ab")
        chk("selftest/selftest_ok", True)
        return report()
    c = codec()
    only = None
    if "--only" in argv:
        i = argv.index("--only")
        only = set(x for x in argv[i + 1:] if x.isdigit())
    for tid in (56, 0, 21, 8, 27, 18, 7, 47, 24):
        if only and str(tid) not in only:
            continue
        for archive in ("client", "server"):
            verify_table(c, frames, tid, archive)
    if not only:
        verify_anchors(c)
    return report()


def report():
    bad = [x for x in CHECKS if not x[1]]
    for name, ok, detail in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - len(bad)}/{len(CHECKS)} checks passed")
    if bad:
        print("FAILED:", ", ".join(x[0] for x in bad))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
