import pathlib,sys,struct,re
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_fantasy_draft_future_regens.bin').read_bytes()
print('len',len(b),'count',struct.unpack_from('<I',b,8)[0])
# find all (u32 len)(utf8 string) tokens
toks=[]
for p in range(8,len(b)-4):
    L=struct.unpack_from('<I',b,p)[0]
    if 1<=L<=64 and p+4+L<=len(b):
        s=b[p+4:p+4+L]
        try:
            t=s.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if all(31<ord(c) for c in t) and any(c.isalpha() for c in t):
            toks.append((p,L,t))
# keep non-overlapping
keep=[]
last=-1
for p,L,t in toks:
    if p>last: keep.append((p,L,t)); last=p+4+L
for p,L,t in keep:
    print('%5d L=%2d prev_end_gap=%s %r'%(p,L,0 if not keep else '',t))
