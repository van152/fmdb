import importlib.util, struct, json
spec = importlib.util.spec_from_file_location("old_dbdat", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
for arch in ("client_db.dat","server_db.dat"):
    path, packed, layout = old._entries(db_path=DB, archive=arch)
    e = old._resolve_table(0, layout["entries"], path.name)
    if e is None:
        print(arch, "MISSING"); continue
    raw = old._decompress_entry(packed, layout["data_base"], e)
    n=len(raw); cnt=struct.unpack_from("<I",raw,8)[0]
    print(f"--- {arch} {e['path']} payload={n} count={cnt} hdr={raw[:14].hex(' ')} tail={raw[-16:].hex(' ')}")
    rem = n-14-8
    print("   rem/count =", rem/cnt if cnt else None, "rem%count=", rem%cnt if cnt else None)
    print("   first 96 row bytes:", raw[14:14+96].hex(' '))
