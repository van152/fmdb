import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/f'payload_server_{n}.bin').read_bytes()
def hx(x): return ' '.join(f'{c:02x}' for c in x)

# 1) old_save_25 DP path count
b=get('table_for_old_save_25'); cnt=struct.unpack_from('<I',b,8)[0]; N=len(b)
cand={}
for p in range(12,N-11):
    v=struct.unpack_from('<I',b,p)[0]
    if v<cnt and struct.unpack_from('<I',b,p+4)[0]==struct.unpack_from('<I',b,p+8)[0]:
        cand.setdefault(v,[]).append(p)
# DP over (row, endoffset) reachability counting
reach={12:1}
paths={12:1}
for k in range(cnt):
    nxt={}
    for start in list(reach):
        for q in cand.get(k,[]):
            if q>=start:
                e=q+12
                nxt[e]=nxt.get(e,0)+reach[start]
                break
    reach=nxt
print('old25 terminal states',{k:v for k,v in reach.items()},'len',N,'footer',N-1464942)

# 2) fantasy identity DP
f=get('fantasy_draft_future_regens'); fc=struct.unpack_from('<I',f,8)[0]; M=len(f)
print('fantasy count',fc,'len',M)
c2={}
for p in range(12,M-11):
    v=struct.unpack_from('<I',f,p)[0]
    if v<fc and struct.unpack_from('<I',f,p+4)[0]==struct.unpack_from('<I',f,p+8)[0]:
        c2.setdefault(v,[]).append(p)
print('fantasy identity cands',{k:len(v) for k,v in list(c2.items())[:6]},'missing',[k for k in range(fc) if k not in c2][:5])
reach={12:1}
for k in range(fc):
    nxt={}
    for start in list(reach):
        for q in c2.get(k,[]):
            if q>=start:
                nxt[q+12]=nxt.get(q+12,0)+reach[start]; break
    reach=nxt
print('fantasy terminals',reach,'footer bytes',M-max(reach) if reach else None, hx(f[max(reach):]) if reach else '')
