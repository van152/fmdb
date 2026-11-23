import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import importlib.util
spec = importlib.util.spec_from_file_location("tr", r"scripts/t95_unicorn_trace.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
emu = m.EditorEmulator()
emu.mu.mem_map(0, 0x10000); emu.mu.mem_write(0, b"\x00"*0x10000)
import zstandard as zstd
def dec(p):
    raw=open(p,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)
bp=dec('scratch/data/basic_people_db.dat')
def trace(func, payload, a3):
    mu=emu.mu; R=emu.REG
    mu.mem_write(m.THIS_BASE, b"\x00"*0x4000)
    mu.mem_write(m.STREAM_OBJ_ADDR+8, struct.pack("<I",1000)); mu.mem_write(m.STREAM_OBJ_ADDR+0x10, struct.pack("<I",0))
    emu.heap_ptr=m.HEAP_BASE; emu.payload=payload; emu.wire_pos=0; emu.reads=[]; emu.unhandled_calls=[]; emu.heap_allocs=[]
    rsp=m.STACK_BASE+m.STACK_SIZE-0x2000
    mu.mem_write(rsp, struct.pack("<Q", m.STOP_ADDR))
    ctx=emu._alloc(0x2000); emu._alloc(0x1000)
    mu.mem_write(ctx+0x588, struct.pack("<H", 0x0df1))
    mu.mem_write(rsp+0x28, struct.pack("<Q",0)); mu.mem_write(rsp+0x30, struct.pack("<Q",0))
    mu.mem_write(rsp+0x38, struct.pack("<Q",1)); mu.mem_write(rsp+0x40, struct.pack("<Q",0))
    mu.reg_write(R["RSP"],rsp); mu.reg_write(R["RCX"],m.THIS_BASE); mu.reg_write(R["RDX"],m.STREAM_PTR_ADDR)
    mu.reg_write(R["R8"],a3); mu.reg_write(R["R9"],ctx)
    err=None
    try: mu.emu_start(func, m.STOP_ADDR, count=400000)
    except Exception as e: err=str(e)
    return err
row=bp[5:5+83]
err=trace(0x140E4FD70, bp[6:6+200], 1)
print('a3=1 err', err, 'consumed', emu.wire_pos)
for x in emu.reads: print('  pos=%-3d n=%-2d off=%-6s hex=%s'%(x['wire_pos'],x['n'],x.get('obj_off'),x.get('hex')))
print('identity row[71:83]=', row[71:83].hex(' '))
print('un', emu.unhandled_calls[:4])
