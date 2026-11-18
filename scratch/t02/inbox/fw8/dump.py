import importlib.util, sys
from pathlib import Path
ROOT=Path("D:/tmp2b/fm24-db")
spec=importlib.util.spec_from_file_location("m", "D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DB=Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
p,packed,layout=m._entries(db_path=DB, archive="client_db.dat")
e=m._resolve_table(8, layout["entries"], p.name)
raw=m._decompress_entry(packed, layout["data_base"], e)
print("len", len(raw))
for off in range(0, 640, 32):
    chunk=raw[off:off+32]
    print(f"{off:04x}  " + " ".join(f"{b:02x}" for b in chunk))
