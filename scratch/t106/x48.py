import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()
N=len(b)
def trial(base, idw, lenw, label):
    off=base; recs=0; ids=[]
    while off+idw+lenw<=N:
        i=int.from_bytes(b[off:off+idw],'little'); L=int.from_bytes(b[off+idw:off+idw+lenw],'little')
        nxt=off+idw+lenw+L
        if nxt>N: return None
        ids.append(i); off=nxt; recs+=1
    if off!=N: return None
    return (label,recs,len(set(ids)),min(ids),max(ids),ids[:6])
for base in (34,36,38):
    for idw in (1,2,4):
        for lenw in (1,2,4):
            r=trial(base,idw,lenw,f'base={base} id={idw} len={lenw}')
            if r: print(r)
print()
# count-driven: count at 34 as u16/u32, entries (id,lenw,payload)
for cw in (2,4):
    cnt=int.from_bytes(b[34:34+cw],'little')
    print('count@34 width',cw,'=',cnt)
    for idw in (1,2,4):
        for lenw in (1,2):
            for unit in (1,):
                off=34+cw; ok=True; ids=[]
                for k in range(cnt):
                    if off+idw+lenw>N: ok=False;break
                    i=int.from_bytes(b[off:off+idw],'little'); L=int.from_bytes(b[off+off*0+idw:off+idw+lenw],'little')
                    off+=idw+lenw+L*unit; ids.append(i)
                    if off>N: ok=False;break
                if ok and off==N:
                    print(f'  CLOSE idw={idw} lenw={lenw} unit={unit} recs={len(ids)} uniq={len(set(ids))} first={ids[:6]}')
