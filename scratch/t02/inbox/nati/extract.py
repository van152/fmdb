"""t02-g nati: extract table_10 payload from client_db (read-only)."""
from __future__ import annotations
import hashlib, importlib.util, json, struct, sys
from pathlib import Path

OLD = Path("D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
DB = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
OUT = Path("D:/tmp2b/fm24-db/scratch/t02/inbox/nati")

def old():
    spec = importlib.util.spec_from_file_location("old_dbdat", OLD)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def member(mod, archive, tid):
    path, packed, layout = mod._entries(db_path=DB, archive=archive)
    e = mod._resolve_table(tid, layout["entries"], path.name)
    return mod._decompress_entry(packed, layout["data_base"], e), e["path"]

if __name__ == "__main__":
    mod = old()
    for arch in ("client_db.dat", "server_db.dat"):
        raw, name = member(mod, arch, 10)
        print(arch, name, len(raw), hashlib.sha256(raw).hexdigest()[:12])
        (OUT / (arch.replace(".dat","") + "_t10.bin")).write_bytes(raw)
        print("  header:", raw[:14].hex(" "))
        print("  footer:", raw[-8:].hex(" "))
        print("  count:", struct.unpack_from("<I", raw, 8)[0])
