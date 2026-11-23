import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()

def epilogue(b):
    """find canonical epilogue: [u32 x][u32 h][u32 h][u32 0][01][u32 h]"""
    out=[]
    for p in range(len(b)-40, len(b)-16):
        if b[p+12:p+16]==b'\x00\x00\x00\x00' and b[p+16]==1:
            x=struct.unpack_from('<I',b,p)[0]; h1=struct.unpack_from('<I',b,p+4)[0]
            h2=struct.unpack_from('<I',b,p+8)[0]; h3=struct.unpack_from('<I',b,p+17)[0]
            if h1==h2 and h3 in (h1,0) and p+21<=len(b):
                out.append((p,x,h1,len(b)-(p+21)))
    return out
for n in ('table_for_old_save_23','table_for_old_save_25','fantasy_draft_future_regens','name_table_0','simple_vars','club_links','common_name_links'):
    print(n, epilogue(get(n)))

print()
# old_save_23 index alignment scan
b=get('table_for_old_save_23'); cnt=struct.unpack_from('<I',b,8)[0]
for s in range(12,20):
    for k in range(12,16):
        n_ok=0
        for i in range(cnt):
            if s+i*k+4>len(b): break
            if struct.unpack_from('<I',b,s+i*k)[0]==i: n_ok+=1
            else: break
        print('start',s,'stride',k,'consecutive index rows',n_ok,'end',s+n_ok*k)
