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
import sys
tid=int(sys.argv[1]); arch=sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 4
raw=get(arch,tid)
cnt=int.from_bytes(raw[8:12],'little')
print(f"len={len(raw)} count={cnt} avg={(len(raw)-22)/cnt}")
stride=(len(raw)-22)//cnt
for i in range(n):
    s=14+i*stride
    print(f"row{i} @{s:#x}: {raw[s:s+stride].hex(' ')}")
print("last row:", raw[14+(cnt-1)*stride:14+cnt*stride].hex(' '))
print("tail 20:", raw[-20:].hex(' '))
