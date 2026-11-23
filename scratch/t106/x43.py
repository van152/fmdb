import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/f'payload_server_{n}.bin').read_bytes()

b=get('table_for_old_save_25'); cnt=struct.unpack_from('<I',b,8)[0]
print('old25 len',len(b),'count',cnt)
# candidate identity positions: u32==i and next two u32 equal
pos={}
for p in range(12,len(b)-12):
    v=struct.unpack_from('<I',b,p)[0]
    if v<cnt and struct.unpack_from('<I',b,p+4)[0]==struct.unpack_from('<I',b,p+8)[0]:
        pos.setdefault(v,[]).append(p)
print('ordinals with candidates',len(pos))
chain=[None]*cnt
p=min(pos.get(0,[-1]))
print('row0 identity at',p)
for i in range(cnt):
    cs=pos.get(i,[])
    if not cs: print('missing ordinal',i); break
    chain[i]=cs
    if i<cnt-1:
        nxt=pos.get(i+1,[])
        # pick smallest next > p
        c=[q for q in nxt if q>p]
        if not c: print('chain break at',i,'p',p); break
        p=c[0]
    if i in (0,1,2,cnt-2,cnt-1): print('row',i,'identity@',cs[:3], 'uids',struct.unpack_from('<II',b,cs[0]+4))
print('last identity',chain[cnt-1][:3] if chain[cnt-1] else None,'len',len(b))
