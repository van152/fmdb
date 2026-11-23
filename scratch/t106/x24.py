import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()

b=get('club_links'); n=struct.unpack_from('<I',b,8)[0]; st=47
rows=[b[12+i*st:12+(i+1)*st] for i in range(n)]
print('== club_links u32 scan')
for off in range(0,st-3):
    v=[struct.unpack_from('<I',r,off)[0] for r in rows]
    mono=all(v[i]<=v[i+1] for i in range(n-1))
    print('u32@%2d min=%10d max=%10d uniq=%5d mono=%s'%(off,min(v),max(v),len(set(v)),mono))
print()
print('== club_links u16 scan')
for off in range(0,st-1):
    v=[struct.unpack_from('<H',r,off)[0] for r in rows]
    print('u16@%2d min=%5d max=%6d uniq=%4d'%(off,min(v),max(v),len(set(v))))
