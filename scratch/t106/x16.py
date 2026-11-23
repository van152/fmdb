import pathlib,sys,struct,runpy
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'scripts')
mf=runpy.run_path('scripts/t38_multiframe.py'); codec=mf['_codec']()
inf=mf['archive_info'](codec,'server')
e=codec['_resolve_table'](25,inf['tables'],'server_db.dat')
s=mf['inspect_entry'](codec,e,inf)['data']
D=pathlib.Path('scratch/t106/out')
a=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
for o in range(0,260,16):
    print('%5d'%o,' '.join('%02x'%x for x in a[o:o+16]),'|',' '.join('%02x'%x for x in s[o:o+16]))
