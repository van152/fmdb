import importlib.util, struct, hashlib, collections
spec = importlib.util.spec_from_file_location("old_dbdat", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
raws={}
for arch in ("client_db.dat","server_db.dat"):
    path, packed, layout = old._entries(db_path=DB, archive=arch)
    e = old._resolve_table(0, layout["entries"], path.name)
    raws[arch]=old._decompress_entry(packed, layout["data_base"], e)
c,s=raws["client_db.dat"],raws["server_db.dat"]
print("identical:", c==s, "sha256:", hashlib.sha256(c).hexdigest())
count=struct.unpack_from("<I",c,8)[0]; stride=77; off=14
print("closure:", 14+count*stride+8, len(c), 14+count*stride+8==len(c))
print("row0 hex:", c[off:off+stride].hex(' '))
print("row1 hex:", c[off+stride:off+2*stride].hex(' '))
print("row2 hex:", c[off+2*stride:off+3*stride].hex(' '))
print("row-last hex:", c[off+(count-1)*stride:off+count*stride].hex(' '))
print("footer:", c[off+count*stride:].hex(' '), "len", len(c)-(off+count*stride))
# column stats: constant columns?
const=[]; 
for j in range(stride):
    vals={c[off+i*stride+j] for i in range(count)}
    if len(vals)==1: const.append((j, vals.pop()))
print("constant columns:", const)
# per-row leading u16 ordinal?
lead=[struct.unpack_from("<H",c,off+i*stride)[0] for i in range(5)]
print("first u16 per row:", lead)
rig=[struct.unpack_from("<H",c,off+i*stride+2)[0] for i in range(5)]
print("u16@+2 per row:", rig)
# last byte distribution
last=collections.Counter(c[off+i*stride+stride-1] for i in range(count))
print("last byte dist:", last.most_common(8))
# check byte -1 marker maybe 0x01 count
print("row0 +74..77:", c[off+74:off+77].hex(' '))
