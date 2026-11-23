import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()

# --- old_save_25: marker split
b=get('table_for_old_save_25'); n=struct.unpack_from('<I',b,8)[0]
print('== old_save_25 len',len(b),'n',n,'footer9',b[-9:].hex())
mk=b'\x64\xff\xff\xff'
pos=[];p=12
while True:
    i=b.find(mk,p)
    if i<0:break
    pos.append(i);p=i+1
print('markers',len(pos),'first',pos[:3],'last',pos[-2:])
# rows as [12..marker+4)
ends=[p+4 for p in pos]
print('last end',ends[-1],'len-9',len(b)-9)
lens=[ends[0]-12]+[ends[i+1]-ends[i] for i in range(len(ends)-1)]
print('row len min',min(lens),'max',max(lens),'mode',collections.Counter(lens).most_common(6))
print('sum',sum(lens),'+12 =',sum(lens)+12)

# --- fantasy: find 40-row split candidates
f=get('fantasy_draft_future_regens'); fc=struct.unpack_from('<I',f,8)[0]
print('== fantasy len',len(f),'count',fc,'footer9',f[-9:].hex())
for pat in (b'\xff\xff\xff\xff',b'\x00\x00\x00\x00',b'\x01\x00\x6c\x07'):
    c=f.count(pat); print('  pat',pat.hex(),'count',c)
