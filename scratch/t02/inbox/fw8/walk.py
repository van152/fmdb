import importlib.util, struct
from pathlib import Path
spec=importlib.util.spec_from_file_location("m", "D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DB=Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")

def get(arch):
    p,packed,layout=m._entries(db_path=DB, archive=arch)
    e=m._resolve_table(8, layout["entries"], p.name)
    return m._decompress_entry(packed, layout["data_base"], e)

for arch in ("client_db.dat","server_db.dat"):
    raw=get(arch); n=len(raw); count=struct.unpack_from("<I",raw,8)[0]
    pos=14; rows=[]
    ok=True; err=None
    for i in range(count):
        st=pos
        ln=struct.unpack_from("<I",raw,pos)[0]; pos+=4
        if ln>200 or not raw[pos:pos+ln].isascii():
            ok=False; err=f"row {i} at {st:#x}: bad len {ln} / non-ascii"; break
        s=raw[pos:pos+ln].decode(); pos+=ln+30
        rows.append((st,ln,s))
    print(arch, "count",count,"walk_end",pos,"payload",n,"end_ok",pos+8==n,"ok",ok,err)
    print("  first6", rows[:6])
    print("  last3", rows[-3:])
    names=[r[2] for r in rows]
    print("  all_names", names[:20])
