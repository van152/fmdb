import pathlib,sys,struct,runpy
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'scripts')
mf=runpy.run_path('scripts/t38_multiframe.py'); codec=mf['_codec']()
def pay(arch,name):
    inf=mf['archive_info'](codec,arch)
    e=codec['_resolve_table'](name,inf['tables'],f'{arch}_db.dat')
    return mf['inspect_entry'](codec,e,inf)['data']
for nm in ('name_table_0','name_table_1','name_table_2'):
    p=pay('server',nm+'.dat'); rc=struct.unpack_from('<I',p,8)[0]
    rows=[struct.unpack_from('<6H',p,12+i*12) for i in range(rc)]
    bad=sum(1 for i,r in enumerate(rows) if (r[1]|(r[2]<<16))!=i)
    print(nm,'f1|f2<<16 != i count',bad)
    f4=[r[4] for r in rows]; f5=[r[5] for r in rows]
    print('   f4 max',max(f4),'f5 distinct',len(set(f5)))
    # f0 duplicates check: is f0 monotone within blocks
    f0=[r[0] for r in rows]
    d=sum(1 for i in range(rc-1) if f0[i]>f0[i+1] and f0[i]!=65535)
    print('   f0 descents',d)
