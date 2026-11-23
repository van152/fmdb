import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/('payload_summary.bin' if n=='summary' else f'payload_server_{n}.bin')).read_bytes()
def hx(x): return ' '.join(f'{c:02x}' for c in x)
def occ(b,pat):
    out=[];i=b.find(pat)
    while i>=0: out.append(i); i=b.find(pat,i+1)
    return out
for n in ('simple_vars','table_for_old_save_25','fantasy_draft_future_regens'):
    b=get(n)
    o=occ(b,b'\x01\x00\x6c\x07')
    print(n,'len',len(b),'marker 01006c07 count',len(o),'first',o[:5],'last',o[-3:])
b=get('simple_vars')
o=occ(b,b'\x01\x00\x6c\x07')
print('gaps',collections.Counter([y-x for x,y in zip(o,o[1:])]).most_common(8))
print('body tail after last marker',len(b)-(o[-1]+4),hx(b[o[-1]:o[-1]+40]))
print('body start',hx(b[34:34+24]))
