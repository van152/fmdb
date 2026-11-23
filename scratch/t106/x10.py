import sys,runpy,struct
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'scripts')
mf=runpy.run_path('scripts/t38_multiframe.py'); codec=mf['_codec']()
info=mf['archive_info'](codec,'server')
for arch,tid in (('server',25),('client',25)):
    inf=mf['archive_info'](codec,arch)
    e=codec['_resolve_table'](tid,inf['tables'],f'{arch}_db.dat')
    d=mf['inspect_entry'](codec,e,inf)['data']
    print('==',arch,tid,'len',len(d),'count',struct.unpack_from('<I',d,8)[0])
    print('  head',d[:60].hex())
    print('  tail',d[-40:].hex())
