import importlib.util, struct
from pathlib import Path
spec=importlib.util.spec_from_file_location("m", "D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DB=Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
def get(a):
    p,pk,l=m._entries(db_path=DB, archive=a)
    return m._decompress_entry(pk,l["data_base"],m._resolve_table(8,l["entries"],p.name))
for arch in ("client_db.dat","server_db.dat"):
    raw=get(arch); n=len(raw); cnt=struct.unpack_from("<I",raw,8)[0]
    pos=14; lens=[]; bad=[]
    for i in range(cnt):
        ln=struct.unpack_from("<I",raw,pos)[0]
        if ln>64 or pos+34+ln>n: bad.append((i,hex(pos),ln)); break
        tail=raw[pos+4+ln:pos+34+ln]
        lens.append(ln); pos+=34+ln
    print(arch,"count",cnt,"walk_end",pos,"n",n,"closure",pos+8==n,"sum_names",sum(lens),"bad",bad)
    print("  lens[:12]",lens[:12],"min",min(lens),"max",max(lens))
    # tail invariance check
    tails={raw[p:p] for p in ()}
