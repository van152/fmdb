import runpy, struct, collections
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
raw = m['load_payload']('server',6); n=115; S=40; H=14; B=27
rows=[raw[H+j*S:H+j*S+B] for j in range(n)]
def u(off,w): return [int.from_bytes(r[off:off+w],'little') for r in rows]
def s(off,w): return [int.from_bytes(r[off:off+w],'little',signed=True) for r in rows]
def f(off): return [struct.unpack_from('<f',r,off)[0] for r in rows]
print('Imnd@3 u16', min(u(3,2)),max(u(3,2)))
print('Iexd@5 u16', min(u(5,2)),max(u(5,2)))
print('Iiar@7 u8', min(u(7,1)),max(u(7,1)), sorted(set(u(7,1)))[:12])
print('Irec@8 u8', sorted(set(u(8,1))))
print('Iocr@13 f32', min(f(13)),max(f(13)), len(set(f(13))))
print('Imip@17', min(u(17,1)),max(u(17,1)), sorted(set(u(17,1))))
print('Icau@18 u16', min(u(18,2)),max(u(18,2)), sorted(set(u(18,2))))
print('Iagr@20', sorted(set(u(20,1))))
print('Icms@21', sorted(set(u(21,1))))
print('Icon@22', sorted(set(u(22,1))))
print('inSr@23', sorted(set(u(23,1))))
print('Igpr@24', sorted(set(u(24,1))))
print('Icdp@25', sorted(set(u(25,1))))
print('bits@26', sorted(set(u(26,1))))
print('icla@0', sorted(set(u(0,1))))
print('iscl@1', sorted(set(u(1,1))))
print('b2', sorted(set(u(2,1))))
print('b6', sorted(set(u(6,1))))
print('b19', sorted(set(u(19,1))))
print('b9..12', [sorted(set(u(x,1))) for x in (9,10,11,12)])
print('b14..16', [sorted(set(u(x,1))) for x in (14,15,16)])
print('Iocr raw u32@13', min(u(13,4)), max(u(13,4)))
