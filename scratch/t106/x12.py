import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]
end=len(b)-9
def ok(p,L):
    if p+L>end: return False
    a=struct.unpack_from('<I',b,p+L-9)[0]; c=struct.unpack_from('<I',b,p+L-5)[0]
    return a==c and b[p+L-1]==0
# DP: reachable positions with row counts
from collections import defaultdict
reach={12:[0]}
# BFS by row count
pos={12:0}
for r in range(n):
    nxt={}
    for p in pos:
        for L in range(13,420):
            if ok(p,L):
                q=p+L
                if q not in nxt: nxt[q]=p
    pos=nxt
    if not pos:
        print('stuck at row',r); break
    if r%1000==0: print('row',r,'candidates',len(pos))
print('rows walked',r,'ends',sorted(pos)[:5],'target end',end,'len-9',end)
