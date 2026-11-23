import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import importlib.util, unicorn
from unicorn import Uc, UC_HOOK_MEM_READ, UC_HOOK_CODE
spec = importlib.util.spec_from_file_location("tr", r"scripts/t95_unicorn_trace.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
emu = m.EditorEmulator()

def trace(func_va, payload, a3=0, a5=0, a6=0, a7=0, ver=0x0df1, max_insns=200000):
    """copy of trace_read with a3 (R8) param"""
    mu = emu.mu; REG = emu.REG
    mu.mem_write(m.THIS_BASE, b"\x00"*0x4000)
    mu.mem_write(m.STREAM_OBJ_ADDR+8, struct.pack("<I",1000))
    mu.mem_write(m.STREAM_OBJ_ADDR+0x10, struct.pack("<I",0))
    emu.heap_ptr = m.HEAP_BASE; emu.payload = payload; emu.wire_pos=0
    emu.reads=[]; emu.unhandled_calls=[]; emu.heap_allocs=[]
    rsp = m.STACK_BASE + m.STACK_SIZE - 0x2000
    mu.mem_write(rsp, struct.pack("<Q", m.STOP_ADDR))
    ctx = emu._alloc(0x2000); sub = emu._alloc(0x1000)
    mu.mem_write(ctx+0x588, struct.pack("<H", ver))
    mu.mem_write(rsp+0x28, struct.pack("<Q", a5))
    mu.mem_write(rsp+0x30, struct.pack("<Q", a6))
    mu.mem_write(rsp+0x38, struct.pack("<Q", a7))
    mu.mem_write(rsp+0x40, struct.pack("<Q", 0))
    mu.reg_write(REG["RSP"], rsp); mu.reg_write(REG["RCX"], m.THIS_BASE)
    mu.reg_write(REG["RDX"], m.STREAM_PTR_ADDR); mu.reg_write(REG["R8"], a3)
    mu.reg_write(REG["R9"], ctx)
    err=None
    try: mu.emu_start(func_va, m.STOP_ADDR, count=max_insns)
    except Exception as e: err=str(e)
    return {"ok": err is None, "error": err, "consumed": emu.wire_pos, "reads": list(emu.reads),
            "unhandled": emu.unhandled_calls[:10]}

import zstandard as zstd
def dec(path):
    raw=open(path,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)
bp=dec('scratch/data/basic_people_db.dat')
CL={1:83,2:83,3:83,4:34,5:22}
cnt=struct.unpack_from('<I',bp,0)[0]
pos=5; first={}
for i in range(cnt):
    cls=bp[pos+1]; L=CL[cls]
    if cls not in first: first[cls]=(i,pos)
    pos+=L
    if len(first)==5: break
for cls,(i,p0) in sorted(first.items()):
    row=bp[p0:p0+CL[cls]]
    for a3 in (0,1):
        r=trace(0x140E4FD70, row[1:], a3=a3)
        print(f'cls{cls} a3={a3} ok={r["ok"]} consumed={r["consumed"]} body={CL[cls]-1-12} reads={len(r["reads"])} err={r["error"]} un={r["unhandled"][:2]}')
    # base class hook function directly
    r=trace(0x141084540, row[1+46:], a3=0)
    print('   base 0x141084540 on tail: ok=%s consumed=%s reads=%s err=%s' % (r['ok'], r['consumed'], len(r['reads']), r['error']))
    for x in r['reads']:
        print('      pos=%-3d n=%-2d off=%-6s hex=%s' % (x['wire_pos'], x['n'], x.get('obj_off'), x.get('hex')))
