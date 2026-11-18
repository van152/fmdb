import importlib.util, json, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('m','../fm24/scripts/modding_read_dbdat.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DB=Path('Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm')
def get(arch,tid):
    path,packed,layout=m._entries(db_path=DB, archive=arch)
    e=m._resolve_table(tid, layout['entries'], path.name)
    if e is None: return None
    return m._decompress_entry(packed, layout['data_base'], e)
for arch in ('client_db.dat','server_db.dat'):
    for tid in (19,41,23,8,2,18,24,6):
        raw=get(arch,tid)
        if raw is None: continue
        print(f"{arch:16s} t{tid:<3d} len={len(raw):>10,d} hdr={raw[:14].hex(' ')}")
        cnt=int.from_bytes(raw[8:12],'little')
        print(f"   count={cnt}  (len-14-8)/cnt={(len(raw)-22)/cnt if cnt else 0}")
        print(f"   tail={raw[-24:].hex(' ')}")
        print(f"   first bytes after hdr={raw[14:46].hex(' ')}")
