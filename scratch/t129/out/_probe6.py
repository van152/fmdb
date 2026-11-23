import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}

# which base files fail for t3/t2/t21
for e in lay["entries"]:
    nm = e["path"].split("/")[1][:-4]
    if "person" in nm: continue
    tid = int(nm.split("_")[1])
    if tid in (3, 2, 21):
        raw = m._decompress_entry(data, base, e)
        if L.grammar_walk(raw, tid) is None:
            print("FAIL", nm, "len", len(raw), "count", struct.unpack_from("<I", raw, 8)[0])
            # find failing row
            g = L.TABLE_GRAMMARS[tid]
            n = struct.unpack_from("<I", raw, 8)[0]; pos = 12
            for i in range(n):
                got = L._grammar_walk_row(raw, pos, len(raw), g)
                if got is None:
                    print("  row", i, "pos", pos, "ctx", raw[pos:pos+60].hex(" "))
                    break
                nxt, dbid, fields, variants = got
                if i+1 < n and (nxt+4 > len(raw) or struct.unpack_from("<I", raw, nxt)[0] <= dbid):
                    print("  order break row", i, "dbid", dbid, "next", struct.unpack_from('<I',raw,nxt)[0], "pos", pos)
                    break
                pos = nxt

# t56 full dump
raw = m._decompress_entry(data, base, ent["8_56.dat"])
print("t56 len", len(raw), "count", struct.unpack_from("<I", raw, 8)[0])
pos = 12
for i in range(6):
    dbid = struct.unpack_from("<I", raw, pos)[0]; p = pos+4
    parts=[]
    for k in range(2):
        got = L._try_string(raw, p, len(raw))
        if got is None: parts.append("<none>"); break
        size, txt = got; parts.append(txt); p += size
    print("  row", i, "dbid", dbid, parts, "then", raw[p:p+4].hex(" "))
    # advance: after 2 strings + 2 scalars +? guess via next dbid
    # brute: scan next valid increasing dbid
    for q in range(p, min(p+40, len(raw))):
        if q+8 <= len(raw):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid and L._try_string(raw, q+4, len(raw)) is not None:
                print("     next row at", q, "gap", q-p, raw[p:q].hex(" ")); pos=q; break
