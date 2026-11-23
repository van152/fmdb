import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()
b=get('club_links'); n=struct.unpack_from('<I',b,8)[0]; st=47
rows=[b[12+i*st:12+(i+1)*st] for i in range(n)]
for off in range(0,44):
    v=[struct.unpack_from('<I',r,off)[0] for r in rows]
    ok=sum(1 for x in v if x<200000)
    if ok==n:
        print('u32@%2d ALL<200000 uniq=%d min=%d max=%d sample=%s'%(off,len(set(v)),min(v),max(v),v[:8]))
for off in range(0,45):
    v=[struct.unpack_from('<H',r,off)[0] for r in rows]
    ok=sum(1 for x in v if x<200000)
    if ok==n and max(v)>300:
        print('u16@%2d uniq=%d min=%d max=%d sample=%s'%(off,len(set(v)),min(v),max(v),v[:8]))
print()
# name pool f3 non-sentinel max
for nm in ('name_table_0','name_table_1','name_table_2'):
    bb=get(nm); rc=struct.unpack_from('<I',bb,8)[0]
    f3=[struct.unpack_from('<H',bb,12+i*12+6)[0] for i in range(rc)]
    nz=[x for x in f3 if x!=65535]
    print(nm,'f3 non-sentinel min',min(nz),'max',max(nz),'distinct',len(set(nz)),'sentinel',f3.count(65535))
    f0=[struct.unpack_from('<H',bb,12+i*12)[0] for i in range(rc)]
    print('   f0 non-sentinel distinct',len(set(x for x in f0 if x!=65535)),'max',max(x for x in f0 if x!=65535))
    f4=[struct.unpack_from('<H',bb,12+i*12+8)[0] for i in range(rc)]
    print('   f4 min',min(f4),'max',max(f4))
