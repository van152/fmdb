import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()
for name in ('simple_vars','summary','table_for_old_save_25','fantasy_draft_future_regens'):
    b=get(name); L=len(b)
    print('==',name,L)
    hits=[]
    for o in range(8,300):
        if o+4>L: break
        cnt=struct.unpack_from('<I',b,o)[0]
        if cnt<2 or cnt>5_000_000: continue
        for st in range(2,80):
            tot=o+4+cnt*st
            if tot<=L and L-tot<=400:
                hits.append((o,st,cnt,L-tot))
    for h in hits[:25]: print('   u32@%d count=%d stride=%d trailer=%d'%(h[0],h[2],h[1],h[3]))
