"""t74 builder part 1: 载荷读取 + 帧定位原语(不依赖 fm24_dump 的 OVERRIDE 结论)。

用法:
  FM24_DB_DIR=... py -V:3.12 -I -B scripts/t74_row_frames9.py [--only 7 24] [--selftest] [--help]

退出码:0 全部闭合 / 1 有 (archive,table) 未闭合 / 2 用法或致命错误。
"""
import pathlib, runpy, struct, hashlib, os

ROOT = pathlib.Path(__file__).resolve().parents[1]
READER_VERIFY = ROOT / "scratch/t01/inbox/t01k/verify.py"
MAGIC = bytes.fromhex("28b52ffd")


def db_dir() -> pathlib.Path:
    return pathlib.Path(os.environ.get("FM24_DB_DIR")
                        or r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm")


def codec():
    k = runpy.run_path(str(READER_VERIFY))
    return runpy.run_path(str(k["OLD_READER_PATH"]))


def payload(c, archive: str, tid: int) -> bytes:
    fn = f"{archive}_db.dat"
    p = db_dir() / fn
    ents = c["list_tables"](p, fn)
    e = c["_resolve_table"](tid, ents, fn)
    db = p.read_bytes()
    base = int(c["_archive_layout"](db)["data_base"])
    start = base + int(e["offset"])
    end = start + int(e["packed_size"])
    size = int(e["size"])
    if not (0 <= start < end <= len(db)):
        raise RuntimeError(f"{fn} table_{tid}: member out of archive")
    d = next((d for d in range(min(64, end - start))
              if db[start + d:start + d + 4] == MAGIC), None)
    if d is None:
        raise RuntimeError(f"{fn} table_{tid}: no zstd frame")
    zstd = c["_zstd_module"]()
    dctx = zstd.ZstdDecompressor()
    pos = start + d
    while pos + 4 <= end and db[pos:pos + 4] == MAGIC:
        obj = dctx.decompressobj()
        out = obj.decompress(db[pos:end])
        if len(out) == size:
            return out
        consumed = (end - pos) - len(obj.unused_data)
        if not obj.eof or consumed <= 0:
            break
        pos += consumed
    raise RuntimeError(f"{fn} table_{tid}: no frame with len == size {size}")


def u32(b: bytes, p: int) -> int:
    return struct.unpack_from("<I", b, p)[0]


def lstr(b: bytes, q: int, e: int):
    """返回 (next, nbytes, text) 或 None。"""
    if q + 4 > e:
        return None
    n = u32(b, q)
    if n > 4096 or q + 4 + n > e:
        return None
    try:
        t = b[q + 4:q + 4 + n].decode("utf-8")
    except UnicodeDecodeError:
        return None
    if not t or not t.isprintable():
        return None
    return q + 4 + n, n, t


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ident_ok(b: bytes, p: int, i: int, pair=True) -> bool:
    o, u1, u2 = struct.unpack_from("<III", b, p)
    if o != i:
        return False
    return (u1 == u2) if pair else True


# ------------------------------------------------------------------ CLI
SPECS = [
    # (archive, table, n, kind)
    ("client", 56, 6, "fixed"), ("server", 56, 6, "fixed"),
    ("client", 0, 3545, "fixed"), ("server", 0, 3545, "fixed"),
    ("client", 21, 48413, "fixed"), ("server", 21, 48413, "fixed"),
    ("client", 8, 126, "lang"), ("server", 8, 126, "lang"),
    ("client", 27, 334, "weat"), ("server", 27, 334, "weat"),
    ("client", 18, 1567, "derby"), ("server", 18, 1567, "derby"),
    ("client", 7, 208, "media"), ("server", 7, 208, "media"),
    ("client", 47, 2488, "lcrg"), ("server", 47, 2488, "lcrg"),
    ("server", 24, 84507, "team"),
]


def build_one(c, archive, tid, n, kind):
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import t74_frames_part2 as P
    b = payload(c, archive, tid)
    if kind == "fixed":
        r = P.fixed_rows(b, P.FIXED[(archive, tid)])
    elif kind == "lang":
        r = P.seq_lang(b, n)
    elif kind == "weat":
        r = P.seq_weat(b, n)
    elif kind == "derby":
        r = P.seq_derby(b, n, const=65 if archive == "client" else 71)
    elif kind == "media":
        r = P.seq_media7(b, n)
    elif kind == "lcrg":
        r = P.seq_lcrg(b, n)
    elif kind == "team":
        r = P.seq_team24(b, n)
    else:
        raise ValueError(kind)
    if r is None:
        return dict(ok=False, payload_len=len(b), sha=sha(b))
    lens = [e - s for s, e in (r.get("rows") or [])] or r.get("lens")
    return dict(ok=True, payload_len=len(b), sha=sha(b), rows=r.get("rows_n", len(r.get("rows") or lens)),
                closure=r["closure"], bad_identity=r["bad_identity"],
                rowlen_min=min(lens), rowlen_max=max(lens),
                rowlen_mean=round(sum(lens) / len(lens), 3))


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    if "--selftest" in argv:
        b = struct.pack("<III", 0, 9, 9) + b"\0"
        assert u32(b, 4) == 9 and ident_ok(b, 0, 0)
        print("selftest OK: u32 / ident_ok")
        return 0
    only = None
    if "--only" in argv:
        i = argv.index("--only")
        only = set(x for x in argv[i + 1:] if x.isdigit())
    c = codec()
    rows = []
    for archive, tid, n, kind in SPECS:
        if only and str(tid) not in only:
            continue
        r = build_one(c, archive, tid, n, kind)
        rows.append((archive, tid, r))
        print(f"{'OK  ' if r['ok'] else 'FAIL'} {archive} t{tid} "
              f"payload={r['payload_len']} " +
              (f"rows={r['rows']} closure={r['closure']} bad={r['bad_identity']} "
               f"len={r['rowlen_min']}..{r['rowlen_max']} mean={r['rowlen_mean']}"
               if r["ok"] else "行框重建失败"))
    bad = [x for x in rows if not x[2]["ok"]]
    print(f"\n{len(rows) - len(bad)}/{len(rows)} (archive,table) 闭合")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
