import sys, pathlib, struct
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
mod=load_old_decoder()
s=member(mod,'client_db.dat',2); r=s['_raw']
def row(i):
    o=14+i*43
    return r[o:o+43]
for i in (0,1,1061,1075,316,540,2,3):
    b=row(i)
    lat,lon=struct.unpack_from('<ff',b,1)
    print(f"row{i:6d} b0={b[0]:#04x} lat={lat:9.4f} lon={lon:9.4f} b9={b[9]:#04x} "
          f"@10={int.from_bytes(b[10:14],'little'):6d} @14={int.from_bytes(b[14:18],'little'):6d} "
          f"calt={int.from_bytes(b[18:20],'little'):5d} cinh={b[20]:3d} "
          f"clgi={int.from_bytes(b[21:25],'little'):6d} clri={int.from_bytes(b[25:29],'little'):6d} "
          f"b29={b[29]:#04x} ord={int.from_bytes(b[30:34],'little'):6d} id={int.from_bytes(b[34:38],'little')}")
