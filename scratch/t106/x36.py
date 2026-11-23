import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/('payload_summary.bin' if n=='summary' else f'payload_server_{n}.bin')).read_bytes()
def hx(b): return ' '.join(f'{c:02x}' for c in b)
for n in ('table_for_old_save_23','table_for_old_save_25','fantasy_draft_future_regens','simple_vars','club_links','common_name_links','summary','name_table_0','name_table_extra_0'):
    b=get(n)
    print(f'== {n} len={len(b)}')
    print('  head24:',hx(b[:24]))
    print('  tail40:',hx(b[-40:]))
    print('  tail u32s:',[hex(x) for x in struct.unpack_from('<5I',b,len(b)-20)])
