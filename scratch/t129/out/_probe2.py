import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm, tid in [("8_9.dat", 9), ("8_3.dat", 3), ("8_21.dat", 21), ("8_25.dat", 25)]:
    raw = m._decompress_entry(data, base, ent[nm])
    print(nm, "hdr", raw[:24].hex(" "), "count", struct.unpack_from("<I", raw, 8)[0])
    # walk from 13
    g = L.TABLE_GRAMMARS[tid]
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 13; ok = True; first = None
    for i in range(n):
        got = L._grammar_walk_row(raw, pos, len(raw), g)
        if got is None:
            ok = False; print("  fail at row", i, "pos", pos); break
        nxt, dbid, fields, variants = got
        if i == 0:
            first = (dbid, fields[:2])
        pos = nxt
    print("  walk-from-13", ok, "end", pos, "len", len(raw), "first", first)
