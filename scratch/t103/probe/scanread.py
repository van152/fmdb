import sys, struct, json
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
def trace(func, payload, a7=1):
    mu=emu.mu; R=emu.REG
    mu.mem_write(m.THIS_BASE, b"\x00"*0x4000)
    mu.mem_write(m.STREAM_OBJ_ADDR+8, struct.pack("<I",1000)); mu.mem_write(m.STREAM_OBJ_ADDR+0x10, struct.pack("<I",0))
    emu.heap_ptr=m.HEAP_BASE; emu.payload=payload; emu.wire_pos=0; emu.reads=[]; emu.unhandled_calls=[]; emu.heap_allocs=[]
    rsp=m.STACK_BASE+m.STACK_SIZE-0x2000
    mu.mem_write(rsp, struct.pack("<Q", m.STOP_ADDR))
    ctx=emu._alloc(0x2000); emu._alloc(0x1000)
    mu.mem_write(ctx+0x588, struct.pack("<H", 0x0df1))
    mu.mem_write(rsp+0x28, struct.pack("<Q",0)); mu.mem_write(rsp+0x30, struct.pack("<Q",0))
    mu.mem_write(rsp+0x38, struct.pack("<Q",a7)); mu.mem_write(rsp+0x40, struct.pack("<Q",0))
    mu.reg_write(R["RSP"],rsp); mu.reg_write(R["RCX"],m.THIS_BASE); mu.reg_write(R["RDX"],m.STREAM_PTR_ADDR)
    mu.reg_write(R["R8"],0); mu.reg_write(R["R9"],ctx)
    err=None
    try: mu.emu_start(func, m.STOP_ADDR, count=300000)
    except Exception as e: err=str(e)
    return err, emu.wire_pos, list(emu.reads)

pl=dec('scratch/data/pl_hist_dt.dat'); npl=dec('scratch/data/non_pl_hist_dt.dat')
cands = {
 'tt14_slot19':0x144354210,'tt44_slot19':0x14437E8D0,'tt49_slot19':None,'tt12_slot19':None,'tt26_slot19':None,'tt34_slot19':None,'tt37_slot19':None,
}
ix=json.load(open('scratch/t95/vtable_index.json'))
for t in ix['tables']:
    key='tt%d_slot19'%t['table_type']
    if t['table_type'] in (12,26,34,37,49,52,64,1):
        cands[key]=int(t['slots_hex'][19],16)
for name,va in cands.items():
    if not va: continue
    for tag,dt,stride in (('pl',pl,44),('npl',npl,24)):
        for a7 in (1,0):
            err,used,reads = trace(va, dt[:400], a7)
            print('%-14s %-3s a7=%d err=%-40s used=%-3d (stride %d) reads=%d' % (name, tag, a7, (err or '-')[:40], used, stride, len(reads)))
