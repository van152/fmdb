import importlib.util
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
        if raw is None:
            print(f"{arch:16s} t{tid:<3d} ABSENT"); continue
        cnt=int.from_bytes(raw[8:12],'little')
        print(f"{arch:16s} t{tid:<3d} len={len(raw):>9,d} count={cnt:>6d} avg={(len(raw)-22)/cnt:8.3f} first16={raw[14:30].hex(' ')}")
