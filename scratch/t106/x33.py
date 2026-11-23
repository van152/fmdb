import pathlib,sys,struct,runpy,hashlib
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'scripts')
mf=runpy.run_path('scripts/t38_multiframe.py'); codec=mf['_codec']()
def pay(arch,name):
    inf=mf['archive_info'](codec,arch)
    e=codec['_resolve_table'](name,inf['tables'],f'{arch}_db.dat')
    return mf['inspect_entry'](codec,e,inf)['data']
names=['simple_vars.dat','name_table_0.dat','name_table_1.dat','name_table_2.dat','name_table_extra_0.dat','name_table_extra_1.dat','name_table_extra_2.dat']
for n in names:
    a=pay('server',n); b=pay('client',n)
    print(n,'srv',len(a),'cli',len(b),'same',a==b)
print()
for n in ('table_for_old_save_25.dat','table_for_old_save_23.dat'):
    a=pay('server',n); b=pay('client',n)
    print(n,'srv',len(a),'cli',len(b),'same',a==b)
print()
# name_table f1/f2 checks
for nm in ('name_table_0','name_table_1','name_table_2'):
    p=pay('server',nm+'.dat'); rc=struct.unpack_from('<I',p,8)[0]
    rows=[struct.unpack_from('<6H',p,12+i*12) for i in range(rc)]
    bad1=sum(1 for i,r in enumerate(rows) if r[1]!=i)
    bad2=sum(1 for i,r in enumerate(rows) if r[2]!=(i>>16))
    print(nm,'rows',rc,'f1!=i',bad1,'f2!=i>>16',bad2,'bytes',12+rc*12,'len',len(p))
